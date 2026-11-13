import pytest

from src.evaluate import evaluate_pairs


class FakeEngine:
    def __init__(self):
        self.calls = []

    def translate(self, text, source, target):
        self.calls.append((text, source, target))
        return "translated"


def test_evaluate_pairs_scores_each_direction_without_network():
    engine = FakeEngine()
    result = evaluate_pairs(
        [
            {"direction": "KN->EN", "source": "ನಮಸ್ಕಾರ", "reference": "Hello"},
            {"direction": " EN -> KN ", "source": "Good morning", "reference": "ಶುಭೋದಯ"},
        ],
        engine,
    )
    assert [row["n"] for row in result] == [1, 1]
    assert engine.calls == [("ನಮಸ್ಕಾರ", "kn", "en"), ("Good morning", "en", "kn")]
    assert all(row["chrf"] >= 0 and row["bleu"] >= 0 for row in result)


def test_evaluation_rejects_unknown_direction_and_empty_pairs():
    engine = FakeEngine()
    with pytest.raises(ValueError, match="Unsupported"):
        evaluate_pairs(
            [{"direction": "KN-KN", "source": "ನಮಸ್ಕಾರ", "reference": "Hello"}], engine
        )
    with pytest.raises(ValueError, match="must not be empty"):
        evaluate_pairs(
            [{"direction": "KN-EN", "source": "", "reference": "Hello"}], engine
        )
