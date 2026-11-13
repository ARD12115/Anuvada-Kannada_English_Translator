import re
from collections.abc import Callable

from src.utils.errors import EmptyInputError

_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?।])\s+")


def split_sentences(text: str) -> list[str]:
    """Split non-empty lines into sentences, preserving punctuation."""
    sentences: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        sentences.extend(part.strip() for part in _SENTENCE_BOUNDARY.split(line) if part.strip())
    return sentences


def translate_preserving_lines(text: str, translate: Callable[[str], str]) -> str:
    """Translate each sentence independently while retaining original line breaks."""
    if not text.strip():
        raise EmptyInputError("Enter text to translate.")
    translated_lines = []
    for line in text.splitlines():
        if not line.strip():
            translated_lines.append("")
            continue
        parts = [part.strip() for part in _SENTENCE_BOUNDARY.split(line.strip()) if part.strip()]
        translated_lines.append(" ".join(translate(part) for part in parts))
    return "\n".join(translated_lines)
