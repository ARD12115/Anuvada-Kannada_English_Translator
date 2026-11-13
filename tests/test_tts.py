import gtts

from src.input.tts import text_to_speech


def test_gtts_uses_finite_connect_read_timeouts_and_requested_language(monkeypatch):
    calls = {}

    class FakeGtts:
        def __init__(self, **kwargs):
            calls.update(kwargs)

        def write_to_fp(self, output):
            output.write(b"audio")

    monkeypatch.setattr(gtts, "gTTS", FakeGtts)
    assert text_to_speech("ನಮಸ್ಕಾರ", "kn") == b"audio"
    assert calls["lang"] == "kn"
    assert calls["timeout"] == (3.05, 10.0)
