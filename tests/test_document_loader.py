from app.document_loader import load_document

def test_markdown(tmp_path):
    file = tmp_path / "test.md"
    file.write_text("# DNS\nDNS resolves domain names.", encoding="utf-8")
    pages = load_document(file)
    assert len(pages) == 1
    assert pages[0].page_number is None
    assert "DNS resolves" in pages[0].text
