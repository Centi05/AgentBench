from dataclasses import dataclass
from pathlib import Path
import fitz

SUPPORTED = {".pdf", ".md", ".txt"}

@dataclass(frozen=True)
class Page:
    source: str
    page_number: int | None
    text: str

def load_document(path: Path) -> list[Page]:
    path = Path(path)
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    if path.suffix.lower() == ".pdf":
        with fitz.open(path) as pdf:
            return [Page(str(path), i + 1, page.get_text("text"))
                    for i, page in enumerate(pdf) if page.get_text("text").strip()]
    text = path.read_text(encoding="utf-8")
    return [Page(str(path), None, text)] if text.strip() else []

def load_directory(directory: Path) -> list[Page]:
    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    pages = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            pages.extend(load_document(path))
    return pages
