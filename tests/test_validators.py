import pytest

from src.input.validators import validate_upload
from src.utils.errors import FileTooLargeError, UnsupportedFileError


@pytest.mark.parametrize(
    ("name", "data", "extension"),
    [
        ("notice.txt", b"Kannada notice", ".txt"),
        ("photo.jpg", b"\xff\xd8\xffdata", ".jpg"),
        ("photo.png", b"\x89PNG\r\n\x1a\ndata", ".png"),
        ("notice.pdf", b"%PDF-1.7 data", ".pdf"),
        ("recording.wav", b"RIFF1234WAVEdata", ".wav"),
    ],
)
def test_accepts_valid_supported_upload_signatures(name, data, extension):
    assert validate_upload(name, data) == extension


def test_rejects_bad_signatures_extensions_and_oversized_files():
    with pytest.raises(UnsupportedFileError):
        validate_upload("photo.png", b"not an image")
    with pytest.raises(UnsupportedFileError):
        validate_upload("photo.exe", b"anything")
    with pytest.raises(FileTooLargeError):
        validate_upload("large.txt", b"x" * 11, max_mb=0)
