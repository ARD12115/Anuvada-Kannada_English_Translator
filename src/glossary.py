import csv
import re
from pathlib import Path

_GLOSSARY_PATH = Path(__file__).resolve().parents[1] / "data" / "glossary.csv"
_DEFAULT_TERMS = {
    "HoD": "HoD",
    "CIE": "CIE",
    "semester": "ಸೆಮಿಸ್ಟರ್",
    "fee receipt": "ಶುಲ್ಕ ರಸೀದಿ",
    "internal assessment": "ಆಂತರಿಕ ಮೌಲ್ಯಮಾಪನ",
    "principal": "ಪ್ರಾಂಶುಪಾಲರು",
}


def _terms() -> dict[str, str]:
    try:
        with _GLOSSARY_PATH.open(encoding="utf-8", newline="") as glossary_file:
            rows = csv.DictReader(glossary_file)
            terms = {
                row["english"].strip(): row["kannada"].strip()
                for row in rows
                if row.get("english", "").strip() and row.get("kannada", "").strip()
            }
            return terms or _DEFAULT_TERMS
    except FileNotFoundError:
        return _DEFAULT_TERMS


def apply_pre(
    text: str, source_lang: str = "en", target_lang: str = "kn"
) -> list[tuple[str, bool]]:
    glossary = _terms()
    terms = {}
    for english, kannada in glossary.items():
        source_term = english if source_lang == "en" else kannada
        target_term = kannada if target_lang == "kn" else english
        terms[source_term.casefold()] = target_term
    alternatives = sorted(terms, key=len, reverse=True)
    if not alternatives:
        return [(text, False)]
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(term) for term in alternatives) + r")(?!\w)",
        re.IGNORECASE,
    )
    parts = []
    position = 0
    for match in pattern.finditer(text):
        if match.start() > position:
            parts.append((text[position : match.start()], False))
        parts.append((terms[match.group().casefold()], True))
        position = match.end()
    if position < len(text):
        parts.append((text[position:], False))
    return parts or [(text, False)]


def apply_post(translated_parts: list[str]) -> str:
    return "".join(translated_parts)
