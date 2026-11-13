from src.glossary import apply_post, apply_pre


def test_glossary_protects_case_insensitive_campus_terms():
    prepared, replacements = apply_pre("Ask the HOD about CIE and semester dates.")
    assert "HOD" not in prepared
    assert "CIE" not in prepared
    assert (
        apply_post(prepared, replacements)
        == "Ask the HoD about CIE and semester dates."
    )
