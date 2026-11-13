from io import BytesIO

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from pdfplumber.utils.exceptions import PdfminerException

from src.input.validators import validate_upload
from src.utils.errors import EmptyInputError, UnsupportedFileError


def read_notice(name: str, data: bytes, max_mb: int = 5, max_pages: int = 100) -> str:
    extension = validate_upload(name, data, {".txt", ".pdf"}, max_mb)
    if extension == ".txt":
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise UnsupportedFileError("Text files must use UTF-8 encoding.") from exc
    else:
        try:
            with pdfplumber.open(BytesIO(data)) as pdf:
                if len(pdf.pages) > max_pages:
                    raise UnsupportedFileError(f"PDF has more than {max_pages} pages.")
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except UnsupportedFileError:
            raise
        except (OSError, ValueError, PDFSyntaxError, PdfminerException) as exc:
            raise UnsupportedFileError("This PDF could not be read.") from exc
    if not text.strip():
        raise EmptyInputError(
            "No selectable text was found. Scanned PDFs need OCR first."
        )
    if len(text) > 5000:
        raise UnsupportedFileError(
            "Notice exceeds the 5,000 character translation limit."
        )
    return text
