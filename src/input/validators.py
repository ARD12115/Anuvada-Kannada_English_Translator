from pathlib import PurePath

from src.utils.errors import FileTooLargeError, UnsupportedFileError

_SIGNATURES = {
    ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".pdf": lambda data: data.startswith(b"%PDF-"),
    ".txt": lambda data: True,
    ".wav": lambda data: data.startswith(b"RIFF") and data[8:12] == b"WAVE",
}


def validate_upload(
    name: str, data: bytes, kinds: set[str] | None = None, max_mb: int = 5
) -> str:
    extension = PurePath(name).suffix.lower()
    allowed = kinds or set(_SIGNATURES)
    if extension not in allowed or extension not in _SIGNATURES:
        raise UnsupportedFileError("Choose a supported file type.")
    if len(data) > max_mb * 1024 * 1024:
        raise FileTooLargeError(f"File is larger than the {max_mb} MB limit.")
    if not _SIGNATURES[extension](data):
        raise UnsupportedFileError(
            "The file contents do not match the selected file type."
        )
    return extension
