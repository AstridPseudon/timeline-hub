## Report

Implemented the scoped visual-seam union in:

- `runtime_protocol/visual_seam.py`
- `docs/visual-seam-policy.md`

Preserved base canonical clip mismatch and rational-FPS guards; adopted incoming full-frame coverage, occurrence seam spans, cue filtering, and shared policy documentation.

Tests/checks:

- `python -m py_compile ...` — passed
- `ruff check runtime_protocol/visual_seam.py` — passed
- `git diff --check` — passed
- Compatible focused tests — **17 passed**
- Incoming shared fixture, read-only — **10 cases passed**
- Base guard checks — passed

The broader stale base admission file remains known-red: 53 passed, 37 failed, due assetless fixtures expecting pre-refresh behavior. The independent test worker owns those updates; no tests were modified here. No full suite run.

Resolved hashes:

- `runtime_protocol/visual_seam.py`: `9bb0bfb04c4cb17c539ffc3f8565f4987df0bb65`
- `docs/visual-seam-policy.md`: `dca6a01c79472c713edfa35d7e98a5299cb91619`

Commit message and `DONE` marker written.