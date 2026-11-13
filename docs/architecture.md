# Architecture — Anuvada

## Layers
```
             +----------------------+
             |   ui (Streamlit)     |  tabs, rendering only
             +----------+-----------+
                        |
             +----------v-----------+
             |  engines/router      |  pick engine, fallback
             |  online | offline    |  TranslationEngine contract
             +----------+-----------+
                        |
             +----------v-----------+
             |  input               |  ocr, speech, documents, validators
             +----------------------+
   shared: utils (lang detect, sentence split, errors), glossary, export
   data:   glossary.csv, eval/pairs.csv, eval/signboards/, samples/ (gitignored)
```
Dependencies point downward. Engines know nothing about the UI.

## Folder layout
```
anuvada/
├── CLAUDE.md  README.md
├── .claude/ (settings.json, commands/, skills/, agents/)
├── docs/
├── src/ { engines/, input/, ui/, utils/, glossary.py, export.py, evaluate.py, models.py }
├── tests/
├── data/ { glossary.csv, eval/, samples/ }
├── scripts/ { setup.sh, run.sh }
├── requirements.txt  .env.example
```

## Key decisions
| Decision | Why |
|---|---|
| Engine interface + router | Swap Google/NLLB/IndicTrans2 without touching UI; Online may fall back to Offline, never vice versa |
| Online default, offline bonus | Instant start; offline adds the privacy and no-internet story |
| Unicode-range language detection | Zero dependencies, exact for Kannada vs Latin script |
| Editable OCR/voice text | Recognition errors don't become translation errors silently |
| Campus glossary | Cheap, visible quality gain on domain terms |
| Session-only history | No persistence, less privacy risk |

## Extension points (Stage 2/3)
- `classifiers/` for scam/fraud detection on top of translated + original text (Stage 2).
- `documents/` + RAG over Kannada notices and forms (Stage 3).
- Kanglish normalizer in `utils/` feeding both.
