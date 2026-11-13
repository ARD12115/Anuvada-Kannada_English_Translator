# CLAUDE.md — Anuvada (Kannada-English Translation Assistant)

Project memory for Claude Code. Keep it short; link to docs, don't copy them.

## What this is
Anuvada translates between Kannada and English with four inputs: typed text, voice, signboard photos (OCR) and campus notices (paste/.txt/.pdf).
CSE-HackSpark-2026, Stage 1, Theme 3 (AI for Everyday Life): "Kannada-English Text Translation Assistant".
Core theme across stages: **language accessibility for everyday digital and civic life in Karnataka**.

## Stack
Python 3.11 · Streamlit · online engine (Google Translate via deep-translator) · offline engine (NLLB-200 distilled 600M via Hugging Face transformers) · pytesseract + Tesseract (kan+eng) · SpeechRecognition + gTTS · pdfplumber · sacrebleu · pytest · ruff.

## Commands
- Setup: `bash scripts/setup.sh`
- Run: `streamlit run src/ui/app.py`
- Tests: `pytest -q`
- Eval (translation quality): `python -m src.evaluate data/eval/pairs.csv`
- Lint: `ruff check . --fix && ruff format .`

## Conventions
- Layers: `input` (text/voice/ocr/pdf -> text) -> `engines` (translate) -> `ui`. UI has no logic.
- All engines implement `TranslationEngine` (`src/engines/base.py`). The UI picks one by name; failures fall back online -> offline.
- Detect language with the Unicode range (U+0C80-U+0CFF = Kannada) before calling any engine.
- Typed errors from `src/utils/errors.py`; UI shows friendly messages.
- Kannada text must render with a Kannada-capable font (Noto Sans Kannada) in any export.

## Testing
Unit tests per module; a fixed eval set in `data/eval/` (sentence pairs + signboard images). Never test against live network in unit tests: mock engines.

## Security (docs/security.md)
Online engine sends text to Google: show a notice and offer offline mode. Validate uploads. No `unsafe_allow_html` with user text. Don't log translated or source text.

## Scope guard
Stage 1 window is 9:30 AM - 4:30 PM (~7 h). Build only **Must/Should** from docs/prd.md. Stage 2/3 ideas stay in docs/roadmap.md.

## Docs index
prd · trd · design · security · architecture · problem-definition · testing · tickets · demo-script · roadmap · onboarding (all in docs/)
