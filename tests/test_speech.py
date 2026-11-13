import sys
import types
import wave
from io import BytesIO

import pytest

from src.input.speech import speech_to_text
from src.utils.errors import SpeechError


def _wav():
    output = BytesIO()
    with wave.open(output, "wb") as recording:
        recording.setnchannels(1)
        recording.setsampwidth(2)
        recording.setframerate(16000)
        recording.writeframes(b"\x00\x00" * 16)
    return output.getvalue()


def test_speech_recognition_uses_requested_locale(monkeypatch):
    calls = []

    class Recognizer:
        def recognize_google(self, audio, language):
            calls.append(language)
            return "recognized"

    fake = types.SimpleNamespace(
        Recognizer=Recognizer,
        AudioData=lambda *args: args,
        UnknownValueError=type("UnknownValueError", (Exception,), {}),
        RequestError=type("RequestError", (Exception,), {}),
    )
    monkeypatch.setitem(sys.modules, "speech_recognition", fake)
    assert speech_to_text(_wav(), "kn") == "recognized"
    assert calls == ["kn-IN"]


def test_invalid_audio_is_reported_as_typed_error():
    with pytest.raises(SpeechError):
        speech_to_text(b"invalid")
