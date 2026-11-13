import sys
import types
from io import BytesIO

import pytest
from PIL import Image

from src.input.ocr import image_to_text
from src.utils.errors import OcrUnavailableError, UnsupportedFileError


def _png():
    buffer = BytesIO()
    Image.new("RGB", (20, 10), "white").save(buffer, format="PNG")
    return buffer.getvalue()


def test_ocr_uses_requested_languages_and_returns_text(monkeypatch):
    fake = types.SimpleNamespace(
        get_languages=lambda config: ["eng", "kan"],
        image_to_string=lambda image, lang: f"{lang}: billboard",
        TesseractError=RuntimeError,
        TesseractNotFoundError=FileNotFoundError,
    )
    monkeypatch.setitem(sys.modules, "pytesseract", fake)
    assert image_to_text(_png()) == "kan+eng: billboard"


def test_ocr_reports_missing_language_pack(monkeypatch):
    fake = types.SimpleNamespace(
        get_languages=lambda config: ["eng"],
        image_to_string=lambda image, lang: "unused",
        TesseractError=RuntimeError,
        TesseractNotFoundError=FileNotFoundError,
    )
    monkeypatch.setitem(sys.modules, "pytesseract", fake)
    with pytest.raises(OcrUnavailableError, match="language data is missing"):
        image_to_text(_png())


def test_ocr_rejects_invalid_image():
    with pytest.raises(UnsupportedFileError):
        image_to_text(b"not an image")


def test_grayscale_decode_errors_are_typed_as_unsupported_file(monkeypatch):
    def fail_grayscale(image):
        raise OSError("decode failed")

    monkeypatch.setattr("src.input.ocr.ImageOps.grayscale", fail_grayscale)
    with pytest.raises(UnsupportedFileError):
        image_to_text(_png())
