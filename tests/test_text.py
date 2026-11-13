import pytest

from src.utils.errors import EmptyInputError
from src.utils.text import split_sentences, translate_preserving_lines


def test_split_sentences_keeps_punctuation_and_handles_newlines():
    assert split_sentences("One. Two!\nಮೂರು। ನಾಲ್ಕು?") == [
        "One.",
        "Two!",
        "ಮೂರು।",
        "ನಾಲ್ಕು?",
    ]


def test_translate_preserving_lines_retains_blank_lines():
    assert (
        translate_preserving_lines("First.\n\nSecond!", str.upper)
        == "FIRST.\n\nSECOND!"
    )


def test_empty_input_is_rejected():
    with pytest.raises(EmptyInputError):
        translate_preserving_lines(" \n ", str.upper)
