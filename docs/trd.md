# Technical Requirements Document (TRD) — Anuvada

## 1. Stack
| Concern | Choice | Reason |
|---|---|---|
| Language / UI | Python 3.11, Streamlit | Fast to build, built-in camera/audio/file widgets |
| Online engine | deep-translator (GoogleTranslator) | Instant start, no API key |
| Offline engine | NLLB-200 distilled 600M (Hugging Face transformers) | Open-source, supports Kannada (`kan_Knda`) and English (`eng_Latn`), runs on CPU |
| OCR | Tesseract via pytesseract (`kan+eng`) | Open-source, Kannada pack available |
| Speech to text | SpeechRecognition (Google web API) | Simple; needs internet |
| Text to speech | gTTS | Simple; needs internet |
| PDF text | pdfplumber | Reliable for text PDFs |
| Evaluation | sacrebleu (chrF, BLEU) | Standard metrics |
| Tests / lint | pytest / ruff | Standard |

Alternative offline model if NLLB underperforms on Kannada: IndicTrans2 (check licence and size first).

## 2. Pipeline
```
text / mic audio / image / .txt / .pdf
   -> input.* (to plain text; OCR and STT outputs editable by user)
   -> utils.lang.detect (Unicode range)
   -> utils.text.split_sentences
   -> glossary.pre (protect campus terms)
   -> engines.<selected>.translate (fallback online -> offline)
   -> glossary.post
   -> ui renders result (+ optional TTS, history, export)
```

## 3. Data contracts (`src/engines/base.py`, `src/models.py`)
```python
Lang = Literal["kn", "en"]

@dataclass
class TranslationResult:
    text: str
    source_lang: Lang
    target_lang: Lang
    engine: str            # "online" | "offline"
    fell_back: bool = False

class TranslationEngine(Protocol):
    name: str
    def translate(self, text: str, src: Lang, tgt: Lang) -> str: ...
    def available(self) -> bool: ...
```
NLLB codes: `kn -> kan_Knda`, `en -> eng_Latn`.

## 4. Modules
| Module | Function | Notes |
|---|---|---|
| `utils/lang.py` | `detect(text) -> Lang` | Kannada if >30% of letters are in U+0C80-U+0CFF, else English |
| `utils/text.py` | `split_sentences(text) -> list[str]`, `join_preserving_lines(...)` | Splits on `. ! ? ।` and newlines; keeps paragraph breaks |
| `engines/online.py` | `OnlineEngine` | Chunks text under the provider's length limit; retries once |
| `engines/offline.py` | `OfflineEngine` | Lazy-loads model, batch of sentences, `max_length` capped |
| `engines/router.py` | `translate(text, src, tgt, preferred) -> TranslationResult` | Falls back to the other engine on error/network loss |
| `input/validators.py` | `validate_upload(name, data, kinds)` | Extension, magic bytes, size |
| `input/ocr.py` | `image_to_text(data: bytes) -> str` | Grayscale + upscale + threshold; `kan+eng`; raises `OcrUnavailableError` if Tesseract/pack missing |
| `input/speech.py` | `speech_to_text(audio: bytes, lang) -> str` | Online only; returns text the user can edit |
| `input/tts.py` | `text_to_speech(text, lang) -> bytes` | Optional |
| `input/documents.py` | `read_notice(name, data) -> str` | .txt (utf-8) and .pdf |
| `glossary.py` | `apply_pre(text)`, `apply_post(text, lang)` | CSV of campus terms (`data/glossary.csv`) |
| `export.py` | `bilingual_text(original, translated) -> str` | Side-by-side or alternating blocks |
| `evaluate.py` | `python -m src.evaluate pairs.csv` | chrF/BLEU per engine/direction |
| `ui/app.py` | Streamlit tabs | No logic |

## 5. Language detection details
Count letters in the Kannada block vs Latin letters. Mixed text: choose the majority script, allow manual override in the UI. Kanglish (Kannada in Latin script) is detected as English in Stage 1 (known limitation).

## 6. Error handling
`EmptyInputError`, `UnsupportedFileError`, `FileTooLargeError`, `OcrUnavailableError`, `EngineUnavailableError`, `SpeechError`. UI maps them to friendly messages. Unexpected errors show a generic message; logs hold only event types and counts.

## 7. Performance
- Model loaded once (`st.cache_resource`), sentences translated in batches.
- Cap input at ~5,000 characters per request; show progress for long notices.
- OCR images resized to a max side length (e.g. 2000 px).

## 8. Configuration (`.env`)
`MAX_UPLOAD_MB`, `DEFAULT_ENGINE`, `OFFLINE_MODEL`, `OCR_LANGS`.

## 9. Testing (see testing.md)
Unit tests with mocked engines, OCR and speech; eval script with a fixed pair set.

## 10. Out of scope now
Kanglish transliteration, other languages, fine-tuning, deployment/Docker, user accounts.
