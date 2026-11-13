# Anuvada — Kannada-English Translation Assistant

Translate text, speech, signboards and campus notices between Kannada and English. Built for CSE-HackSpark-2026 (Canara Engineering College).

## Quick start

The app runs on Python 3.11+. On macOS/Linux/WSL:

```bash
bash scripts/setup.sh
streamlit run src/ui/app.py
```

On Windows, create the environment and install dependencies in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run src/ui/app.py
```

For the Signboard tab, install Tesseract with both English and Kannada language data. Voice recognition and Listen require internet. Online translation and speech features send text/audio to Google; use Offline mode for private translations. Offline translation requires downloading the NLLB model (~2.4 GB) before use. Offline mode will not silently send text to the online engine.

Uploads are limited to 5 MB and text translation to 5,000 characters. Scanned PDFs are not OCR'd; use the Signboard tab for images.

## Docs
Start with `docs/prd.md`, then `docs/trd.md`. Claude Code config: `CLAUDE.md`, `.claude/`.

## Team
<Team name> — <leader>, <members> · Mentor: <faculty guide>
