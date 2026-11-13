import csv
import logging
import os
from io import StringIO

import streamlit as st

from src.engines.offline import OfflineEngine
from src.engines.online import OnlineEngine
from src.engines.router import translate
from src.export import bilingual_text
from src.input.documents import read_notice
from src.input.ocr import image_to_text
from src.input.speech import speech_to_text
from src.input.tts import text_to_speech
from src.input.validators import validate_upload
from src.models import Lang
from src.utils.errors import AnuvadaError, FileTooLargeError
from src.utils.lang import detect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
MAX_TEXT_LENGTH = 5000


@st.cache_resource
def get_offline_engine() -> OfflineEngine:
    return OfflineEngine(os.getenv("OFFLINE_MODEL", "facebook/nllb-200-distilled-600M"))


def _show_error(error: AnuvadaError) -> None:
    st.error(str(error))


def _translate(
    text: str,
    preferred: str,
    source: Lang | None = None,
    target: Lang | None = None,
    result_key: str = "text_result",
) -> None:
    if len(text) > MAX_TEXT_LENGTH:
        raise FileTooLargeError(
            f"Text exceeds the {MAX_TEXT_LENGTH:,} character limit."
        )
    engines = {"online": OnlineEngine(), "offline": get_offline_engine()}
    with st.spinner(f"Translating with the {preferred.title()} engine…"):
        result = translate(text, preferred, source, target, engines)
    record = {
        "source": text,
        "translated": result.text,
        "source_lang": result.source_lang,
        "target_lang": result.target_lang,
        "engine": result.engine,
        "fell_back": result.fell_back,
    }
    st.session_state.history.insert(0, record)
    if len(st.session_state.history) > 100:
        del st.session_state.history[100:]
    st.session_state[result_key] = record


def _engine_result(key: str) -> None:
    record = st.session_state.get(key)
    if not record:
        return
    st.caption(
        f"{record['source_lang'].upper()} → {record['target_lang'].upper()} · {record['engine'].title()} engine"
    )
    if record["fell_back"]:
        st.info("The selected engine was unavailable; the other engine was used.")
    st.code(record["translated"], language=None)
    if st.button("Listen to translation · online", key=f"listen_{key}"):
        try:
            audio = text_to_speech(record["translated"], record["target_lang"])
            st.audio(audio, format="audio/mp3")
        except AnuvadaError as exc:
            _show_error(exc)


def _direction(selection: str, text: str) -> tuple[Lang | None, Lang | None]:
    if selection == "Auto-detect":
        source = detect(text)
        return source, "en" if source == "kn" else "kn"
    if selection == "Kannada → English":
        return "kn", "en"
    return "en", "kn"


def main() -> None:
    st.set_page_config(
        page_title="Anuvada · Kannada-English", page_icon="ಅ", layout="wide"
    )
    if "history" not in st.session_state:
        st.session_state.history = []
    for editor in ("voice_editor", "ocr_editor", "notice_editor"):
        if editor not in st.session_state:
            st.session_state[editor] = ""

    st.title("Anuvada · ಅನುವಾದ")
    st.write(
        "Kannada ↔ English translation for text, notices, speech and public signboards."
    )
    engine = st.radio(
        "Translation engine",
        ("Online", "Offline"),
        horizontal=True,
        index=0 if os.getenv("DEFAULT_ENGINE", "online").lower() == "online" else 1,
        key="preferred_engine",
    ).lower()
    if engine == "online":
        st.info(
            "Privacy: Online translation sends your text to Google. Choose Offline for private text; model setup is required."
        )
    else:
        st.caption(
            "Offline mode keeps translation on this device after the NLLB model is downloaded."
        )

    text_tab, voice_tab, signboard_tab, notice_tab, history_tab = st.tabs(
        ("Text", "Voice", "Signboard", "Notice", "History")
    )

    with text_tab:
        left, right = st.columns(2)
        with left:
            direction = st.selectbox(
                "Direction",
                ("Auto-detect", "Kannada → English", "English → Kannada"),
                key="text_direction",
            )
            text = st.text_area(
                "Text to translate",
                height=220,
                placeholder="Type or paste Kannada or English text",
            )
            if st.button("Translate", type="primary", key="text_translate"):
                try:
                    source, target = _direction(direction, text)
                    _translate(text, engine, source, target, "text_result")
                except AnuvadaError as exc:
                    _show_error(exc)
        with right:
            st.subheader("Translation")
            _engine_result("text_result")
        st.caption(
            "Machine translation may be inaccurate. Check important information against the original."
        )

    with voice_tab:
        st.caption(
            "Speech recognition and text-to-speech use Google services and require internet."
        )
        audio = st.audio_input("Record a sentence")
        speech_language = st.selectbox(
            "Spoken language", ("English", "Kannada"), key="speech_language"
        )
        if audio and st.button("Recognize speech", key="recognize_speech"):
            try:
                audio_data = audio.getvalue()
                if len(audio_data) > MAX_UPLOAD_MB * 1024 * 1024:
                    raise FileTooLargeError(
                        f"Audio recording exceeds the {MAX_UPLOAD_MB} MB limit."
                    )
                st.session_state.voice_editor = speech_to_text(
                    audio_data, "en" if speech_language == "English" else "kn"
                )
            except AnuvadaError as exc:
                _show_error(exc)
        voice_text = st.text_area(
            "Recognized text (edit before translating)",
            key="voice_editor",
            height=130,
        )
        if st.button("Translate recognized text", key="voice_translate"):
            try:
                _translate(voice_text, engine, result_key="voice_result")
            except AnuvadaError as exc:
                _show_error(exc)
        _engine_result("voice_result")

    with signboard_tab:
        st.caption(
            "Use photos of public signs. OCR is performed locally; review the recognized text before translation."
        )
        image_file = st.file_uploader(
            "Upload a JPG or PNG signboard", type=("jpg", "jpeg", "png")
        )
        camera_image = st.camera_input("Or take a photo")
        selected_image = camera_image or image_file
        if selected_image and st.button("Read signboard", key="read_signboard"):
            try:
                validate_upload(
                    getattr(selected_image, "name", "camera.png"),
                    selected_image.getvalue(),
                    {".jpg", ".jpeg", ".png"},
                    MAX_UPLOAD_MB,
                )
                st.session_state.ocr_editor = image_to_text(selected_image.getvalue())
                if not st.session_state.ocr_editor:
                    st.warning("No text found. Try a clearer, closer photo.")
            except AnuvadaError as exc:
                _show_error(exc)
        ocr_text = st.text_area(
            "Recognized text (edit before translating)",
            key="ocr_editor",
            height=130,
        )
        if st.button("Translate signboard", key="signboard_translate"):
            try:
                _translate(ocr_text, engine, result_key="signboard_result")
            except AnuvadaError as exc:
                _show_error(exc)
        _engine_result("signboard_result")

    with notice_tab:
        notice_file = st.file_uploader(
            "Upload a UTF-8 .txt or text-based .pdf notice", type=("txt", "pdf")
        )
        if notice_file and st.button("Read notice file", key="read_notice"):
            try:
                st.session_state.notice_editor = read_notice(
                    notice_file.name, notice_file.getvalue(), max_mb=MAX_UPLOAD_MB
                )
            except AnuvadaError as exc:
                _show_error(exc)
        notice = st.text_area(
            "Or paste a notice",
            height=200,
            key="notice_editor",
        )
        if st.button("Translate notice", type="primary", key="notice_translate"):
            try:
                _translate(notice, engine, result_key="notice_result")
            except AnuvadaError as exc:
                _show_error(exc)
        _engine_result("notice_result")
        record = st.session_state.get("notice_result")
        if record and record["source"] == notice:
            original_col, translation_col = st.columns(2)
            with original_col:
                st.subheader("Original")
                st.text(record["source"])
            with translation_col:
                st.subheader("Translation")
                st.text(record["translated"])
            st.download_button(
                "Download bilingual notice",
                bilingual_text(record["source"], record["translated"]),
                file_name="anuvada-bilingual-notice.txt",
                mime="text/plain; charset=utf-8",
                key="download_notice",
            )

    with history_tab:
        st.caption(
            "History is stored only for this browser session and is cleared when the session ends."
        )
        history = st.session_state.history
        if history:
            st.dataframe(
                [
                    {
                        "Source language": entry["source_lang"],
                        "Target language": entry["target_lang"],
                        "Engine": entry["engine"],
                        "Original": entry["source"],
                        "Translation": entry["translated"],
                    }
                    for entry in history
                ],
                width="stretch",
            )
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=history[0].keys())
            writer.writeheader()
            writer.writerows(history)
            st.download_button(
                "Download history CSV",
                output.getvalue(),
                "anuvada-history.csv",
                "text/csv",
            )
            if st.button("Clear history", key="clear_history"):
                st.session_state.history = []
                st.rerun()
        else:
            st.write("No translations yet.")


if __name__ == "__main__":
    main()
