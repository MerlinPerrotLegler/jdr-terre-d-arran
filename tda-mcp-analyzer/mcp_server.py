#!/usr/bin/env python3
"""MCP Server — Terre d'Arran Rulebook Analyzer.

Exposes 6 tools for an LLM orchestrator to:
  1. list_pdf_books        — discover available PDFs
  2. extract_and_chunk_pdf — extract text + split into chunks
  3. get_chunk_for_analysis — load prompt + format chunk for LLM
  4. parse_and_write_entities — write extracted entities to vault
  5. create_obsidian_structure — init vault folders and INDEX files
  6. get_progress          — report current analysis progress
"""

import json
import os
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

from src import pdf_handler, entity_parser, obsidian_writer, progress_tracker

SOURCES_PATH = os.environ.get("SOURCES_PATH", "./00-Sources")
VAULT_PATH = os.environ.get("VAULT_PATH", "./obsidian")
PROMPT_PATH = os.environ.get("PROMPT_PATH", "./prompt-extraction-tda.md")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "12000"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "1500"))

_chunk_cache: dict[str, pdf_handler.PdfChunk] = {}

server = Server("tda-analyzer")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_pdf_books",
            description="Liste tous les PDFs disponibles dans le dossier sources.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="extract_and_chunk_pdf",
            description="Extrait le texte d'un PDF et le découpe en chunks analysables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "book_id": {"type": "string", "description": "Identifiant du livre (nom de fichier sans .pdf)"},
                    "chunk_size": {"type": "integer", "description": "Taille max d'un chunk en caractères (défaut: 12000)"},
                    "chunk_overlap": {"type": "integer", "description": "Overlap entre chunks (défaut: 1500)"},
                },
                "required": ["book_id"],
            },
        ),
        types.Tool(
            name="get_chunk_for_analysis",
            description="Retourne le texte d'un chunk et le prompt d'extraction, prêts à envoyer à un LLM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "chunk_id": {"type": "string", "description": "ID du chunk (ex: tda-joueur_p001_c001)"},
                    "already_known_entities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Noms d'entités déjà extraites pour éviter les doublons",
                    },
                },
                "required": ["chunk_id"],
            },
        ),
        types.Tool(
            name="parse_and_write_entities",
            description="Parse le markdown avec marqueurs ENTITY et écrit les fichiers dans le vault Obsidian.",
            inputSchema={
                "type": "object",
                "properties": {
                    "markdown": {"type": "string", "description": "Markdown retourné par le LLM avec marqueurs <!-- ENTITY: ... -->"},
                    "chunk_id": {"type": "string", "description": "ID du chunk source"},
                },
                "required": ["markdown", "chunk_id"],
            },
        ),
        types.Tool(
            name="create_obsidian_structure",
            description="Crée la structure de dossiers et les fichiers INDEX du vault Obsidian.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_progress",
            description="Retourne l'avancement de l'analyse (livres, chunks, entités).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    match name:
        case "list_pdf_books":
            return _list_pdf_books()
        case "extract_and_chunk_pdf":
            return _extract_and_chunk_pdf(arguments)
        case "get_chunk_for_analysis":
            return _get_chunk_for_analysis(arguments)
        case "parse_and_write_entities":
            return _parse_and_write_entities(arguments)
        case "create_obsidian_structure":
            return _create_obsidian_structure()
        case "get_progress":
            return _get_progress()
        case _:
            return [types.TextContent(type="text", text=f"Outil inconnu: {name}")]


def _list_pdf_books() -> list[types.TextContent]:
    try:
        books = pdf_handler.list_books(SOURCES_PATH)
        result = {
            "books": [{"id": b.id, "path": b.path, "pages": b.pages, "size_mb": b.size_mb} for b in books],
            "total_books": len(books),
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur: {e}")]


def _extract_and_chunk_pdf(args: dict) -> list[types.TextContent]:
    book_id = args["book_id"]
    chunk_size = args.get("chunk_size", CHUNK_SIZE)
    overlap = args.get("chunk_overlap", CHUNK_OVERLAP)

    try:
        chunks = pdf_handler.extract_and_chunk(book_id, SOURCES_PATH, chunk_size, overlap)
        for chunk in chunks:
            _chunk_cache[chunk.id] = chunk

        progress = progress_tracker.load(VAULT_PATH)
        progress_tracker.register_book(progress, book_id, len(chunks))
        progress_tracker.save(progress)

        result = {
            "book_id": book_id,
            "total_chunks": len(chunks),
            "chunks": [
                {
                    "id": c.id,
                    "page_start": c.page_start,
                    "page_end": c.page_end,
                    "section_hint": c.section_hint,
                    "char_count": len(c.text),
                }
                for c in chunks
            ],
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur extraction: {e}")]


def _get_chunk_for_analysis(args: dict) -> list[types.TextContent]:
    chunk_id = args["chunk_id"]
    known = args.get("already_known_entities", [])

    chunk = _chunk_cache.get(chunk_id)
    if not chunk:
        return [types.TextContent(type="text", text=f"Chunk {chunk_id!r} non trouvé. Appelle d'abord extract_and_chunk_pdf.")]

    prompt = _load_prompt()
    known_str = ", ".join(known) if known else "aucune"

    output = (
        f"## Prompt d'extraction\n\n{prompt}\n\n"
        f"---\n\n"
        f"## Entités déjà extraites (ne pas dupliquer inutilement)\n\n{known_str}\n\n"
        f"---\n\n"
        f"## Texte à analyser\n\n"
        f"**Source:** Livre `{chunk.book_id}`, pages {chunk.page_start}–{chunk.page_end}\n"
        f"**Section:** {chunk.section_hint or 'Non détectée'}\n"
        f"**Chunk ID:** {chunk.id}\n\n"
        f"```\n{chunk.text}\n```"
    )
    return [types.TextContent(type="text", text=output)]


def _parse_and_write_entities(args: dict) -> list[types.TextContent]:
    markdown = args["markdown"]
    chunk_id = args.get("chunk_id", "")
    book_id = chunk_id.split("_")[0] if chunk_id else ""

    try:
        entities = entity_parser.parse_entities(markdown, chunk_id)
        result = obsidian_writer.write_entities(entities, VAULT_PATH)

        progress = progress_tracker.load(VAULT_PATH)
        progress_tracker.mark_chunk_done(
            progress,
            book_id,
            len(result["files_created"]),
            result["conflicts_detected"],
        )
        progress_tracker.update_entity_counts(progress, VAULT_PATH)
        progress_tracker.save(progress)

        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur écriture: {e}")]


def _create_obsidian_structure() -> list[types.TextContent]:
    try:
        result = obsidian_writer.create_vault_structure(VAULT_PATH)
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur structure: {e}")]


def _get_progress() -> list[types.TextContent]:
    try:
        progress = progress_tracker.load(VAULT_PATH)
        return [types.TextContent(type="text", text=json.dumps(progress_tracker.summary(progress), ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur progression: {e}")]


def _load_prompt() -> str:
    p = Path(PROMPT_PATH)
    if p.exists():
        return p.read_text(encoding="utf-8")
    return "Prompt non trouvé. Vérifiez PROMPT_PATH."


async def _main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import anyio
    anyio.run(_main)
