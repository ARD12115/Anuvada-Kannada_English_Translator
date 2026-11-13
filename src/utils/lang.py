import unicodedata

from src.models import Lang

KANNADA_START = 0x0C80
KANNADA_END = 0x0CFF


def detect(text: str) -> Lang:
    """Detect Kannada when it is a meaningful majority of the letters."""
    kannada = 0
    latin = 0
    for char in text:
        if not unicodedata.category(char).startswith("L"):
            continue
        codepoint = ord(char)
        if KANNADA_START <= codepoint <= KANNADA_END:
            kannada += 1
        elif "LATIN" in unicodedata.name(char, ""):
            latin += 1

    if kannada > latin:
        return "kn"
    return "en"
