import csv
import re
from pathlib import Path

_GLOSSARY_PATH = Path(__file__).resolve().parents[1] / "data" / "glossary.csv"
_DEFAULT_TERMS = (
    "HoD",
    "CIE",
    "semester",
    "fee receipt",
    "internal assessment",
    "principal",
)


def _terms() -> tuple[str, ...]:
    try:
        with _GLOSSARY_PATH.open(encoding="utf-8", newline="") as glossary_file:
            rows = csv.DictReader(glossary_file)
            terms = tuple(
                row["term"].strip() for row in rows if row.get("term", "").strip()
            )
            return terms or _DEFAULT_TERMS
    except FileNotFoundError:
        return _DEFAULT_TERMS


def apply_pre(text: str) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}
    terms = sorted(_terms(), key=len, reverse=True)
    for index, term in enumerate(terms):
        token = f"ANUVADATERM{index}TOKEN"
        pattern = re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", re.IGNORECASE)
        text, count = pattern.subn(token, text)
        if count:
            replacements[token] = term
    return text, replacements


def apply_post(text: str, replacements: dict[str, str]) -> str:
    for token, original in replacements.items():
        text = re.sub(re.escape(token), original, text, flags=re.IGNORECASE)
    return text
