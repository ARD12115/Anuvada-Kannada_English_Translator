# Anuvada — Kannada-English Translation Assistant

Translate text, speech, signboards and campus notices between Kannada and English. Built for CSE-HackSpark-2026 (Canara Engineering College).

## Quick start

The app runs on Python 3.11+. On macOS/Linux/WSL:

```bash
bash scripts/setup.sh
bash scripts/run.sh
```

On Windows, create the environment and install dependencies in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/ui/app.py
```

For the Signboard tab, install Tesseract with both English and Kannada language data. Voice recognition and Listen require internet. Online translation and speech features send text/audio to Google; use Offline mode for private translations. Offline translation requires downloading the NLLB model (~2.4 GB) before use. Offline mode will not silently send text to the online engine.

To download the offline model on Windows after installing dependencies:

```powershell
.\.venv\Scripts\python.exe -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; m='facebook/nllb-200-distilled-600M'; AutoTokenizer.from_pretrained(m); AutoModelForSeq2SeqLM.from_pretrained(m)"
```

Uploads are limited to 5 MB and text translation to 5,000 characters. Scanned PDFs are not OCR'd; use the Signboard tab for images.

## Translation evaluation

Add a UTF-8 `data/eval/pairs.csv` with `direction,source,reference` columns. References should be reviewed by a Kannada-fluent speaker; the repository intentionally contains no unverified evaluation examples or claimed scores. Then run `python -m src.evaluate data/eval/pairs.csv --engine offline` (or `--engine online`).

## Docs
Start with `docs/prd.md`, then `docs/trd.md`. Claude Code config: `CLAUDE.md`, `.claude/`.

## Team
<Team name> — <leader>, <members> · Mentor: <faculty guide>
