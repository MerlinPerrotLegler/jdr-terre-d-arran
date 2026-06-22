#!/usr/bin/env python3
"""Script d'extraction autonome — Terre d'Arran.

Usage:
    ANTHROPIC_API_KEY=sk-... python extract_all.py
    ANTHROPIC_API_KEY=sk-... python extract_all.py --book livret-joueur --start 5
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).parent))
from src import pdf_handler, entity_parser, obsidian_writer, progress_tracker

SOURCES_PATH = os.environ.get("SOURCES_PATH", "../obsidian/00-Sources")
VAULT_PATH   = os.environ.get("VAULT_PATH",   "../obsidian")
PROMPT_PATH  = os.environ.get("PROMPT_PATH",  "../prompt-extraction-tda.md")
CHUNK_SIZE   = int(os.environ.get("CHUNK_SIZE", "12000"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "1500"))
MODEL        = os.environ.get("TDA_MODEL", "claude-sonnet-4-6")

_GREEN  = "\033[32m"
_YELLOW = "\033[33m"
_RED    = "\033[31m"
_RESET  = "\033[0m"
_BOLD   = "\033[1m"

BOOK_ALIASES = {
    "livret-joueur": "Les Règles - TdA_LivretJoueur_compressed",
    "livre-meneur":  "Les Règles - tda-02-livre-du-meneur-arran-web-v1_compress_compressed",
}


def load_prompt() -> str:
    p = Path(PROMPT_PATH)
    if p.exists():
        return p.read_text(encoding="utf-8")
    print(f"{_RED}⚠ Prompt non trouvé : {PROMPT_PATH}{_RESET}")
    sys.exit(1)


def analyze_chunk(client: anthropic.Anthropic, prompt: str, chunk: pdf_handler.PdfChunk, known: list[str]) -> str:
    known_str = ", ".join(known) if known else "aucune"
    user_msg = (
        f"## Prompt d'extraction\n\n{prompt}\n\n"
        f"---\n\n"
        f"## Entités déjà extraites (ne pas dupliquer inutilement)\n\n{known_str}\n\n"
        f"---\n\n"
        f"## Texte à analyser\n\n"
        f"**Source :** Livre `{chunk.book_id}`, pages {chunk.page_start}–{chunk.page_end}\n"
        f"**Section :** {chunk.section_hint or 'Non détectée'}\n"
        f"**Chunk ID :** {chunk.id}\n\n"
        f"```\n{chunk.text}\n```"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": user_msg}],
    )
    return response.content[0].text


def process_book(client: anthropic.Anthropic, book_id: str, start_chunk: int = 0) -> None:
    prompt = load_prompt()
    print(f"\n{_BOLD}📚 Livre : {book_id}{_RESET}")

    print("  Extraction des chunks...")
    chunks = pdf_handler.extract_and_chunk(book_id, SOURCES_PATH, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"  {len(chunks)} chunks ({len(chunks) - start_chunk} à traiter depuis chunk {start_chunk + 1})")

    progress = progress_tracker.load(VAULT_PATH)
    progress_tracker.register_book(progress, book_id, len(chunks))
    progress_tracker.save(progress)

    known_entities: list[str] = []

    for i, chunk in enumerate(chunks):
        if i < start_chunk:
            continue

        print(f"\n  [{i+1}/{len(chunks)}] {chunk.id} — p{chunk.page_start}-{chunk.page_end} — {len(chunk.text)} chars")
        if chunk.section_hint:
            print(f"         Section : {chunk.section_hint[:60]}")

        try:
            markdown = analyze_chunk(client, prompt, chunk, known_entities)

            entities = entity_parser.parse_entities(markdown, chunk.id)
            result = obsidian_writer.write_entities(entities, VAULT_PATH)

            new_names = [e.name for e in entities]
            known_entities.extend(new_names)
            known_entities = known_entities[-200:]  # garde les 200 derniers pour éviter un prompt trop long

            progress = progress_tracker.load(VAULT_PATH)
            progress_tracker.mark_chunk_done(
                progress, book_id,
                len(result["files_created"]),
                result["conflicts_detected"],
            )
            progress_tracker.update_entity_counts(progress, VAULT_PATH)
            progress_tracker.save(progress)

            created = len(result["files_created"])
            updated = len(result["files_updated"])
            conflicts = len(result["conflicts_detected"])
            print(f"         {_GREEN}✓ {created} créés, {updated} mis à jour{_RESET}"
                  + (f", {_YELLOW}{conflicts} conflits{_RESET}" if conflicts else ""))
            if result["files_created"]:
                for f in result["files_created"][:5]:
                    print(f"           + {f}")
                if created > 5:
                    print(f"           ... et {created - 5} autres")

        except anthropic.RateLimitError:
            print(f"  {_YELLOW}⏳ Rate limit — pause 60s{_RESET}")
            time.sleep(60)
            # retry
            markdown = analyze_chunk(client, prompt, chunk, known_entities)
            entities = entity_parser.parse_entities(markdown, chunk.id)
            obsidian_writer.write_entities(entities, VAULT_PATH)

        except Exception as e:
            print(f"  {_RED}✗ Erreur chunk {chunk.id} : {e}{_RESET}")
            continue

        # Petite pause pour éviter le rate limit
        time.sleep(1)

    print(f"\n{_GREEN}{_BOLD}✅ Livre terminé : {book_id}{_RESET}")
    _print_summary()


def _print_summary() -> None:
    progress = progress_tracker.load(VAULT_PATH)
    s = progress_tracker.summary(progress)
    print(f"\n{'─'*50}")
    print(f"  Livres : {s['books_processed']}/{s['total_books']}")
    print(f"  Chunks : {s['chunks_processed']}/{s['total_chunks']} ({s['percent']}%)")
    print(f"  Fichiers écrits : {s['files_written']}")
    print(f"  Conflits : {s['conflicts_count']}")
    entities = s['entities_found']
    print(f"  Entités :")
    for k, v in entities.items():
        if v > 0:
            print(f"    {k}: {v}")
    print(f"{'─'*50}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extraction TdA vers vault Obsidian")
    parser.add_argument("--book", choices=list(BOOK_ALIASES.keys()) + ["all"], default="all",
                        help="Livre à traiter (défaut: all)")
    parser.add_argument("--start", type=int, default=0, metavar="N",
                        help="Commencer à partir du chunk N (0-indexé)")
    parser.add_argument("--summary", action="store_true", help="Afficher uniquement le résumé de progression")
    args = parser.parse_args()

    if args.summary:
        _print_summary()
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"{_RED}❌ ANTHROPIC_API_KEY manquante.{_RESET}")
        print("  Lancer avec : ANTHROPIC_API_KEY=sk-... python extract_all.py")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Assurer que la structure du vault existe
    obsidian_writer.create_vault_structure(VAULT_PATH)

    books_to_process = list(BOOK_ALIASES.values()) if args.book == "all" else [BOOK_ALIASES[args.book]]

    for book_id in books_to_process:
        start = args.start if len(books_to_process) == 1 else 0
        process_book(client, book_id, start_chunk=start)

    print(f"\n{_BOLD}🎉 Extraction complète !{_RESET}")
    _print_summary()


if __name__ == "__main__":
    main()
