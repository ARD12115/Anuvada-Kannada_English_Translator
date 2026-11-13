import wave
from io import BytesIO

from src.models import Lang
from src.utils.errors import SpeechError


def speech_to_text(audio: bytes, lang: Lang = "en") -> str:
    try:
        import speech_recognition as sr

        with wave.open(BytesIO(audio), "rb") as wav:
            frames = wav.readframes(wav.getnframes())
            audio_data = sr.AudioData(frames, wav.getframerate(), wav.getsampwidth())
        recognizer = sr.Recognizer()
        return recognizer.recognize_google(
            audio_data, language="kn-IN" if lang == "kn" else "en-IN"
        )
    except (ImportError, OSError, EOFError, ValueError, wave.Error) as exc:
        raise SpeechError(
            "The audio recording could not be read. Record again or type the text instead."
        ) from exc
    except sr.UnknownValueError as exc:
        raise SpeechError(
            "Speech could not be understood. Try again or type the text instead."
        ) from exc
    except sr.RequestError as exc:
        raise SpeechError(
            "Speech recognition failed. Check your connection or type the text instead."
        ) from exc
