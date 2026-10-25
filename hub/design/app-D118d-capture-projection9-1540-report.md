# D118d report

Implemented the source-only fixture correction in `tests/sdk/test_timeline_capture_projection.py`.

- Added the registered `commit_timeline` `doc.patch` setup to seed the real saved shot item.
- Preserved all original assertions, authored opaque fields, pins, ordering, and opener checks byte-for-byte.
- Static checks passed: `py_compile`, Ruff, mypy, `git diff --check`.
- AST conservation passed; change exactly matches reviewed setup commit `28081580dc95f02470d82ad81b826335d8e4bd09`.
- Own failing-node tests were NOTRUN because free space was below the required 5 GB floor.
- Frozen R4 candidate-sdk lacks the target test path, so no upstream exact-node comparison was possible.
- Evidence and commit message are present at the required absolute paths. Independent protected review remains pending.