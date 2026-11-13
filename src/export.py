import csv
from io import StringIO


def bilingual_text(original: str, translated: str) -> str:
    return f"ORIGINAL\n{original}\n\nTRANSLATION\n{translated}\n"


def history_csv(history: list[dict[str, object]]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=history[0].keys())
    writer.writeheader()
    for entry in history:
        safe_entry = {
            key: _spreadsheet_safe(value) if isinstance(value, str) else value
            for key, value in entry.items()
        }
        writer.writerow(safe_entry)
    return output.getvalue()


def _spreadsheet_safe(value: str) -> str:
    if value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value
