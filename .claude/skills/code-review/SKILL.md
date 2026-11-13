---
name: code-review
description: Reviews Python changes in Anuvada for correctness, layering, Unicode handling and tests. Use when asked to review code or a diff.
---
# Checklist
1. UI contains no logic; engines never import UI.
2. Every engine implements `TranslationEngine`; errors are typed.
3. Kannada text: no ASCII-only regexes, no `.encode("ascii")`, files opened with `encoding="utf-8"`.
4. Long text is split into sentences before translation (model length limits).
5. Network and model calls are mockable; tests cover failure and fallback.
6. No PII or text content in logs.
Output: Must fix / Should fix / Nice to have.
