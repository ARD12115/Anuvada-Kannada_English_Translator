import pytest

from src.engines.router import translate
from src.utils.errors import EmptyInputError, EngineUnavailableError, FileTooLargeError


class Engine:
    def __init__(self, name, result=None, failure=False):
        self.name = name
        self.result = result
        self.failure = failure
        self.calls = []

    def available(self):
        return not self.failure

    def translate(self, text, src, tgt):
        self.calls.append((text, src, tgt))
        if self.failure:
            raise EngineUnavailableError("unavailable")
        return self.result if self.result is not None else text


def test_router_detects_languages_preserves_lines_and_glossary_terms():
    online = Engine("online")
    result = translate("ನಮಸ್ಕಾರ ವಿದ್ಯಾರ್ಥಿಗಳೇ.\nCIE tomorrow.", engines={"online": online})
    assert result.source_lang == "kn"
    assert result.target_lang == "en"
    assert result.text == "ನಮಸ್ಕಾರ ವಿದ್ಯಾರ್ಥಿಗಳೇ.\nCIE tomorrow."
    assert online.calls[0][1:] == ("kn", "en")


def test_router_falls_back_from_online_to_offline():
    online = Engine("online", failure=True)
    offline = Engine("offline", result="ಹಲೋ")
    result = translate(
        "Hello", "online", "en", "kn", {"online": online, "offline": offline}
    )
    assert result.engine == "offline"
    assert result.fell_back


def test_offline_failure_never_sends_text_to_online_engine():
    offline = Engine("offline", failure=True)
    online = Engine("online")
    with pytest.raises(EngineUnavailableError):
        translate(
            "Sensitive notice",
            "offline",
            "en",
            "kn",
            {"offline": offline, "online": online},
        )
    assert online.calls == []


def test_router_rejects_empty_input_and_same_direction():
    with pytest.raises(EmptyInputError):
        translate(" ")
    with pytest.raises(EmptyInputError):
        translate("Hello", source_lang="en", target_lang="en")


def test_router_rejects_over_limit_input_before_engine_call():
    online = Engine("online")
    with pytest.raises(FileTooLargeError):
        translate("x" * 5001, engines={"online": online})
    assert online.calls == []
