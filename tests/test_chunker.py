import pytest
from app.chunker import chunk_pages
from app.document_loader import Page

def test_chunks_preserve_metadata():
    pages = [Page("docs/linux.md", None, "Linux networking " * 100)]
    chunks = chunk_pages(pages, size=120, overlap=20)
    assert len(chunks) > 1
    assert all(c.source == "docs/linux.md" for c in chunks)
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))

def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_pages([], size=100, overlap=100)
