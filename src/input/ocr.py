from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

from src.utils.errors import OcrUnavailableError, UnsupportedFileError

MAX_IMAGE_SIDE = 2000


def image_to_text(data: bytes, languages: str = "kan+eng") -> str:
    try:
        image = Image.open(BytesIO(data))
        image.verify()
        image = Image.open(BytesIO(data))
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise UnsupportedFileError("Choose a valid JPG or PNG image.") from exc
    if image.format not in {"JPEG", "PNG"}:
        raise UnsupportedFileError("Only JPG and PNG images are supported.")
    if image.width * image.height > 40_000_000:
        raise UnsupportedFileError("Image dimensions are too large to process safely.")
    image = ImageOps.grayscale(image)
    image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))
    try:
        import pytesseract

        installed = pytesseract.get_languages(config="")
        required = set(languages.split("+"))
        missing = required - set(installed)
        if missing:
            raise OcrUnavailableError(
                "Tesseract language data is missing. Install the Kannada and English language packs."
            )
        return pytesseract.image_to_string(image, lang=languages).strip()
    except OcrUnavailableError:
        raise
    except (ImportError, OSError) as exc:
        raise OcrUnavailableError(
            "OCR is unavailable. Install Tesseract with Kannada and English language packs."
        ) from exc
    except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError) as exc:
        raise OcrUnavailableError(
            "OCR is unavailable. Install Tesseract with Kannada and English language packs."
        ) from exc
