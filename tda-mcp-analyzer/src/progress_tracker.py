"""Track analysis progress across books and chunks."""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict

_PROGRESS_FILE = ".progress.json"


@dataclass
class EntityCounts:
    profils: int = 0
    competences: int = 0
    traits: int = 0
    pnj: int = 0
    lieux: int = 0
    bestiaire: int = 0
    equipement: int = 0
    sorts: int = 0
    autres: int = 0


@dataclass
class BookProgress:
    book_id: str
    total_chunks: int
    processed_chunks: int = 0
    done: bool = False


@dataclass
class Progress:
    vault_path: str = ""
    books: list[BookProgress] = field(default_factory=list)
    entities: EntityCounts = field(default_factory=EntityCounts)
    files_written: int = 0
    conflicts: list[str] = field(default_factory=list)


def load(vault_path: str) -> Progress:
    p = Path(vault_path) / _PROGRESS_FILE
    if not p.exists():
        return Progress(vault_path=vault_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    progress = Progress(
        vault_path=data.get("vault_path", vault_path),
        entities=EntityCounts(**data.get("entities", {})),
        files_written=data.get("files_written", 0),
        conflicts=data.get("conflicts", []),
    )
    progress.books = [BookProgress(**b) for b in data.get("books", [])]
    return progress


def save(progress: Progress) -> None:
    p = Path(progress.vault_path) / _PROGRESS_FILE
    data = asdict(progress)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def register_book(progress: Progress, book_id: str, total_chunks: int) -> None:
    for book in progress.books:
        if book.book_id == book_id:
            return
    progress.books.append(BookProgress(book_id=book_id, total_chunks=total_chunks))


def mark_chunk_done(progress: Progress, book_id: str, files_created: int, new_conflicts: list[str]) -> None:
    for book in progress.books:
        if book.book_id == book_id:
            book.processed_chunks += 1
            if book.processed_chunks >= book.total_chunks:
                book.done = True
    progress.files_written += files_created
    progress.conflicts.extend(new_conflicts)


def update_entity_counts(progress: Progress, vault_path: str) -> None:
    vault = Path(vault_path)
    mapping = {
        "profils": "01-Regles/Personnage/Profils",
        "competences": "01-Regles/Personnage/Competences",
        "traits": "01-Regles/Personnage/Traits",
        "pnj": "04-PNJ",
        "lieux": "02-Lieux",
        "bestiaire": "05-Bestiaire",
        "equipement": "06-Equipement",
        "sorts": "07-Magie/Sorts",
    }
    for attr, folder in mapping.items():
        target = vault / folder
        if target.exists():
            count = len([f for f in target.rglob("*.md") if f.name != "INDEX.md"])
            setattr(progress.entities, attr, count)


def summary(progress: Progress) -> dict:
    total_chunks = sum(b.total_chunks for b in progress.books)
    processed = sum(b.processed_chunks for b in progress.books)
    percent = round(100 * processed / total_chunks) if total_chunks else 0
    current = next((b.book_id for b in progress.books if not b.done), "done")
    return {
        "books_processed": sum(1 for b in progress.books if b.done),
        "total_books": len(progress.books),
        "current_book": current,
        "chunks_processed": processed,
        "total_chunks": total_chunks,
        "percent": percent,
        "entities_found": asdict(progress.entities),
        "files_written": progress.files_written,
        "conflicts_count": len(progress.conflicts),
    }
