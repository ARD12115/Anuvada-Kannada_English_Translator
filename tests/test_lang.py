from src.utils.lang import detect


def test_detect_kannada_and_english():
    assert detect("ನಮಸ್ಕಾರ, ಹೇಗಿದ್ದೀರಿ?") == "kn"
    assert detect("Good morning, students.") == "en"


def test_mixed_text_uses_majority_script():
    assert detect("ನಮಸ್ಕಾರ ಎಲ್ಲರೂ everyone") == "kn"
    assert detect("Hello ಎಲ್ಲರೂ, welcome to CIE") == "en"
    assert detect("ಅಆಇಈ ABCDEF") == "en"


def test_digits_punctuation_empty_and_kanglish_default_to_english():
    assert detect("123!?") == "en"
    assert detect("") == "en"
    assert detect("namaskara hegiddira") == "en"


def test_detect_handles_long_kannada_input():
    assert detect("ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಪರೀಕ್ಷೆಯ ವೇಳಾಪಟ್ಟಿ ಪ್ರಕಟಿಸಲಾಗಿದೆ. " * 300) == "kn"
