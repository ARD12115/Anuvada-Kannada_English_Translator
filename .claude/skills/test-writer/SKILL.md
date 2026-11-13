---
name: test-writer
description: Writes pytest tests for Anuvada modules including Kannada edge cases. Use when adding or changing input handling or engines.
---
# Rules
- One test file per module. Mock engines, OCR, speech and network.
- Cover: Kannada-only, English-only, mixed text, empty string, very long text, punctuation, digits, Kanglish (Kannada in Latin script).
- Language detection tests use real Kannada strings.
- Assert behaviour (language detected, engine called with right codes, fallback triggered), not exact translation wording.
