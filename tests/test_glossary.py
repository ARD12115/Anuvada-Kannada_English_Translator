from src.glossary import apply_post, apply_pre


def test_glossary_segments_terms_without_sending_them_for_translation():
    parts = apply_pre("Ask the HOD about CIE and semester dates.", "en", "kn")
    preserved = [text for text, is_term in parts if is_term]
    assert preserved == ["HoD", "CIE", "ಸೆಮಿಸ್ಟರ್"]
    assert all("ANUVADA" not in text for text, _ in parts)
    assert apply_post([text for text, _ in parts]) == (
        "Ask the HoD about CIE and ಸೆಮಿಸ್ಟರ್ dates."
    )


def test_glossary_uses_target_language_terms_in_both_directions():
    forward = apply_pre("Pay the fee receipt.", "en", "kn")
    reverse = apply_pre("ಶುಲ್ಕ ರಸೀದಿ", "kn", "en")
    assert [text for text, is_term in forward if is_term] == ["ಶುಲ್ಕ ರಸೀದಿ"]
    assert [text for text, is_term in reverse if is_term] == ["fee receipt"]
