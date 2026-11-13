from io import BytesIO

from src.models import Lang
from src.utils.errors import SpeechError


def text_to_speech(text: str, lang: Lang) -> bytes:
    if not text.strip():
        raise SpeechError("There is no translated text to read.")
    try:
        from gtts import gTTS
        from gtts.tts import gTTSError
        from requests.exceptions import RequestException
    except ImportError as exc:
        raise SpeechError("Text-to-speech dependencies are not installed.") from exc
    try:
        output = BytesIO()
        gTTS(text=text, lang="kn" if lang == "kn" else "en").write_to_fp(output)
        return output.getvalue()
    except (gTTSError, RequestException, OSError, ValueError) as exc:
        raise SpeechError(
            "Text-to-speech is unavailable. Check your connection."
        ) from exc
