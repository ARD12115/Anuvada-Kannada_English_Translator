from typing import ClassVar

import deep_translator.google as google_module
import pytest

from src.engines.online import OnlineEngine
from src.utils.errors import EngineUnavailableError


class FakeTranslator:
    responses: ClassVar[list[str]] = []
    calls: ClassVar[list[tuple[str, str]]] = []

    def __init__(self, source, target):
        self.calls.append((source, target))

    def translate(self, text):
        self.responses.append(text.upper())
        return text.upper()


def test_online_engine_uses_requested_language_codes_and_splits_large_text():
    FakeTranslator.responses = []
    FakeTranslator.calls = []
    engine = OnlineEngine(FakeTranslator, retries=0)
    engine.max_chunk_length = 8
    result = engine.translate("hello world", "en", "kn")
    assert result.replace(" ", "") == "HELLOWORLD"
    assert FakeTranslator.calls == [("en", "kn"), ("en", "kn")]


def test_online_engine_retries_then_raises_a_typed_error():
    class BrokenTranslator:
        def __init__(self, source, target):
            pass

        def translate(self, text):
            raise RuntimeError("provider detail")

    with pytest.raises(EngineUnavailableError, match="Online translation failed"):
        OnlineEngine(BrokenTranslator, retries=1).translate("Hello", "en", "kn")


def test_online_engine_applies_finite_timeouts_at_requests_boundary(monkeypatch):
    class FakeRequests:
        def __init__(self):
            self.kwargs = []

        def get(self, url, **kwargs):
            self.kwargs.append(kwargs)
            return object()

    requests = FakeRequests()
    monkeypatch.setattr(google_module, "requests", requests)

    class Translator:
        def __init__(self, source, target):
            pass

        def translate(self, text):
            google_module.requests.get("https://example.invalid", timeout=None)
            return text

    assert OnlineEngine(Translator, retries=0).translate("Hello", "en", "kn") == "Hello"
    assert requests.kwargs == [{"timeout": (3.05, 10.0)}]
