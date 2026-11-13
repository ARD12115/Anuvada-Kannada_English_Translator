# Onboarding — Anuvada

## Setup (needs internet once, ~15 minutes plus the downloads)
```bash
git clone https://github.com/ARD12115/Anuvada-Kannada_English_Translator.git anuvada
cd anuvada
bash scripts/setup.sh        # venv, deps, caches NLLB (~2.4 GB)
bash scripts/run.sh
```

## Tesseract with Kannada (for the Signboard tab)
- Ubuntu/WSL: `sudo apt install tesseract-ocr tesseract-ocr-kan`
- macOS: `brew install tesseract tesseract-lang`
- Windows: install Tesseract (UB Mannheim build) and tick Kannada in the language list; add it to PATH.
Check: `tesseract --list-langs` should include `kan`.

## Using Claude Code (optional)
```bash
npm i -g @anthropic-ai/claude-code
claude
```
Commands: `/review`, `/test-all`, `/bootstrap engines/offline`, `/eval`, `/demo-check`.
Subagents: `code-reviewer`, `test-writer`, `security-auditor`. Read `CLAUDE.md` first.

## Workflow
1. Pick a ticket from `docs/tickets.md`; branch `feat/T-07-offline-engine`.
2. Build + tests; `ruff check . --fix` and `pytest -q`.
3. Commit, merge, tell the team.

## Rules of the road
- Follow `docs/security.md`; no personal photos or documents in git.
- Don't build Stage 2/3 features now.
- Voice, Listen and the online engine need internet; the offline engine and OCR don't.
- Unclear requirement: `docs/prd.md` wins; technical question: `docs/trd.md` wins.
