from src.models import Lang
from src.utils.errors import SpeechError


def text_to_speech(text: str, lang: Lang) -> bytes:
    if not text.strip():
        raise SpeechError("There is no translated text to read.")
    try:
        from gtts import gTTS
        from io import BytesIO

        output = BytesIO()
        gTTS(text=text, lang="kn" if lang == "kn" else "en").write_to_fp(output)
        return output.getvalue()
    except Exception as exc:
        raise SpeechError("Text-to-speech is unavailable. Check your connection.") from exc
