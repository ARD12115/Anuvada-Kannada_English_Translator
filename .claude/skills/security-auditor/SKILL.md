---
name: security-auditor
description: Audits Anuvada for upload handling, privacy of translated text, and dependency risks against docs/security.md.
---
# Audit
- Image/PDF/TXT uploads: extension + magic bytes + size limit.
- Online-engine privacy notice is shown; offline mode works with no network.
- No `unsafe_allow_html` with user/translated text; no eval/exec/pickle on user data.
- Temp files (audio, images) deleted in `finally`.
- Logs contain no source or translated text.
Report: file, line, severity, fix.
