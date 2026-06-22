"""PDF extraction and chunking for Terre d'Arran rulebooks."""

import re
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


@dataclass
class PdfChunk:
    id: str
    book_id: str
    page_start: int
    page_end: int
    text: str
    section_hint: str = ""


@dataclass
class BookInfo:
    id: str
    path: str
    pages: int
    size_mb: float


_HEADING_RE = re.compile(r"^([A-ZÀÂÄÉÈÊËÎÏÔÙÛÜ][A-ZÀÂÄÉÈÊËÎÏÔÙÛÜ\s\-:]{3,})$", re.MULTILINE)


def list_books(sources_path: str) -> list[BookInfo]:
    """Return metadata for all PDFs found in sources_path."""
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed. Run: pip install PyMuPDF")

    folder = Path(sources_path)
    books = []
    for pdf_path in sorted(folder.glob("*.pdf")):
        doc = fitz.open(str(pdf_path))
        size_mb = round(pdf_path.stat().st_size / 1_048_576, 1)
        books.append(BookInfo(
            id=pdf_path.stem,
            path=str(pdf_path),
            pages=len(doc),
            size_mb=size_mb,
        ))
        doc.close()
    return books


def extract_and_chunk(book_id: str, sources_path: str, chunk_size: int = 12000, overlap: int = 1500) -> list[PdfChunk]:
    """Extract text from a PDF and split into overlapping chunks."""
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed. Run: pip install PyMuPDF")

    pdf_path = _find_pdf(book_id, sources_path)
    doc = fitz.open(str(pdf_path))

    pages_text: list[tuple[int, str]] = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if not text.strip():
            text = _ocr_page(page)
        pages_text.append((page_num + 1, text.strip()))
    doc.close()

    full_text = "\n".join(text for _, text in pages_text)
    page_offsets = _build_page_offsets(pages_text)

    raw_chunks = _split_text(full_text, chunk_size, overlap)

    chunks = []
    for i, (start, end) in enumerate(raw_chunks):
        chunk_text = full_text[start:end]
        page_start, page_end = _offsets_to_pages(start, end, page_offsets)
        section = _detect_section(chunk_text)
        chunk_id = f"{book_id}_p{page_start:03d}_c{i+1:03d}"
        chunks.append(PdfChunk(
            id=chunk_id,
            book_id=book_id,
            page_start=page_start,
            page_end=page_end,
            text=chunk_text,
            section_hint=section,
        ))
    return chunks


def _find_pdf(book_id: str, sources_path: str) -> Path:
    folder = Path(sources_path)
    direct = folder / f"{book_id}.pdf"
    if direct.exists():
        return direct
    matches = list(folder.glob(f"*{book_id}*.pdf"))
    if not matches:
        raise FileNotFoundError(f"No PDF found for book_id={book_id!r} in {sources_path}")
    return matches[0]


def _build_page_offsets(pages_text: list[tuple[int, str]]) -> list[tuple[int, int, int]]:
    offsets = []
    pos = 0
    for page_num, text in pages_text:
        length = len(text) + 1
        offsets.append((page_num, pos, pos + length))
        pos += length
    return offsets


def _offsets_to_pages(start: int, end: int, page_offsets: list[tuple[int, int, int]]) -> tuple[int, int]:
    page_start = page_end = 1
    for page_num, pg_start, pg_end in page_offsets:
        if pg_start <= start < pg_end:
            page_start = page_num
        if pg_start < end <= pg_end:
            page_end = page_num
            break
    return page_start, page_end


def _split_text(text: str, chunk_size: int, overlap: int) -> list[tuple[int, int]]:
    chunks = []
    pos = 0
    length = len(text)

    while pos < length:
        end = min(pos + chunk_size, length)

        if end < length:
            search_zone = text[pos:end]
            last_heading = _last_heading_pos(search_zone)
            if last_heading and last_heading > chunk_size // 3:
                end = pos + last_heading

        chunks.append((pos, end))
        if end >= length:
            break
        pos = max(pos + 1, end - overlap)

    return chunks


def _last_heading_pos(text: str) -> int | None:
    matches = list(_HEADING_RE.finditer(text))
    if not matches:
        return None
    return matches[-1].start()


def _detect_section(text: str) -> str:
    for line in text.splitlines()[:10]:
        line = line.strip()
        if _HEADING_RE.match(line) and len(line) > 4:
            return line[:80]
    return ""


def _ocr_page(page) -> str:
    try:
        import pytesseract
        from PIL import Image
        import io

        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        return pytesseract.image_to_string(img, lang="fra")
    except Exception:
        return ""
