import pytest

from src.input.documents import read_notice
from src.utils.errors import EmptyInputError, UnsupportedFileError


def test_reads_utf8_text_and_rejects_non_utf8():
    assert read_notice("notice.txt", b"\xef\xbb\xbfHello \xe0\xb2\xa8") == "Hello ನ"
    with pytest.raises(UnsupportedFileError, match="UTF-8"):
        read_notice("notice.txt", b"\xff")


def test_rejects_empty_or_scanned_pdf(monkeypatch):
    class Page:
        def extract_text(self):
            return None

    class Pdf:
        def __init__(self):
            self.pages = [Page()]

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    monkeypatch.setattr("src.input.documents.pdfplumber.open", lambda stream: Pdf())
    with pytest.raises(EmptyInputError, match="Scanned PDFs"):
        read_notice("scan.pdf", b"%PDF-1.7")


def test_invalid_pdf_is_returned_as_a_typed_error():
    with pytest.raises(UnsupportedFileError, match="PDF could not be read"):
        read_notice("broken.pdf", b"%PDF-not-a-document")
