from src.export import bilingual_text


def test_bilingual_export_is_utf8_friendly_and_includes_both_texts():
    output = bilingual_text("ನಮಸ್ಕಾರ", "Hello")
    assert "ನಮಸ್ಕಾರ" in output
    assert "Hello" in output
    assert "ORIGINAL" in output
    assert "TRANSLATION" in output
