import csv
from io import StringIO

from src.export import bilingual_text, history_csv


def test_bilingual_export_is_utf8_friendly_and_includes_both_texts():
    output = bilingual_text("ನಮಸ್ಕಾರ", "Hello")
    assert "ನಮಸ್ಕಾರ" in output
    assert "Hello" in output
    assert "ORIGINAL" in output
    assert "TRANSLATION" in output


def test_history_csv_neutralizes_formula_cells_without_changing_normal_text():
    history = [
        {
            "source": ' \t=HYPERLINK("https://example.com")',
            "translated": "@SUM(1,2)",
            "engine": "online",
        },
        {"source": "Hello", "translated": "ನಮಸ್ಕಾರ", "engine": "offline"},
    ]

    rows = list(csv.DictReader(StringIO(history_csv(history))))

    assert rows[0]["source"] == '\' \t=HYPERLINK("https://example.com")'
    assert rows[0]["translated"] == "'@SUM(1,2)"
    assert rows[1]["source"] == "Hello"
    assert rows[1]["translated"] == "ನಮಸ್ಕಾರ"
