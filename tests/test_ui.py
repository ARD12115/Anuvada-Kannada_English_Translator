from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.engines.online import OnlineEngine


def test_results_and_listen_buttons_remain_separate_across_tab_reruns(monkeypatch):
    monkeypatch.setattr(
        OnlineEngine,
        "translate",
        lambda self, text, source, target: f"{source}>{target}:{text}",
    )
    monkeypatch.setattr("src.input.tts.text_to_speech", lambda text, lang: b"audio")
    app_path = Path(__file__).resolve().parents[1] / "src" / "ui" / "app.py"
    app = AppTest.from_file(str(app_path)).run()
    app.text_area[0].set_value("Hello from text")
    app.button(key="text_translate").click().run()
    assert not app.exception
    assert app.session_state["text_result"]["source"] == "Hello from text"

    app.button(key="listen_text_result").click().run()
    assert not app.exception
    assert app.session_state["text_result"]["translated"] == "en>kn:Hello from text"

    app.text_area(key="voice_editor").set_value("ನಮಸ್ಕಾರ")
    app.button(key="voice_translate").click().run()
    assert not app.exception
    assert app.session_state["voice_result"]["source"] == "ನಮಸ್ಕಾರ"
    assert app.session_state["text_result"]["source"] == "Hello from text"
    assert "listen_voice_result" in {button.key for button in app.button}


def test_extracted_text_updates_existing_editors_on_repeated_reruns():
    app_path = Path(__file__).resolve().parents[1] / "src" / "ui" / "app.py"
    app = AppTest.from_file(str(app_path)).run()
    for key in ("voice_editor", "ocr_editor", "notice_editor"):
        for value in (f"first {key}", f"second {key}"):
            app.session_state[key] = value
            app.run()
            assert app.text_area(key=key).value == value
