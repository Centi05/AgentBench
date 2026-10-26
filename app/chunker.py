from dataclasses import dataclass
from app.document_loader import Page

@dataclass(frozen=True)
class Chunk:
    source: str
    page_number: int | None
    chunk_index: int
    text: str

def chunk_pages(pages: list[Page], size: int = 900, overlap: int = 150) -> list[Chunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    chunks = []
    for page in pages:
        text = " ".join(page.text.split())
        start, idx = 0, 0
        while start < len(text):
            end = min(start + size, len(text))
            # Prefer breaking at a word boundary near the end of a chunk.
            if end < len(text):
                boundary = text.rfind(" ", start + size // 2, end)
                if boundary > start:
                    end = boundary
            content = text[start:end].strip()
            if content:
                chunks.append(Chunk(page.source, page.page_number, idx, content))
                idx += 1
            if end == len(text):
                break
            next_start = max(start + 1, end - overlap)
            start = next_start
    return chunks
