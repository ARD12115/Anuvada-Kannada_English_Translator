---
description: Run lint and the full test suite, then summarize failures
---
Run `ruff check .` and `pytest -q`. For each failure give the root cause in one or two lines and the smallest fix. Never weaken a test just to pass.
