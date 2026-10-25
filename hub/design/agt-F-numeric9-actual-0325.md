## F-D86 report

Updated only `tests/editing_conformance/test_commit_runtime_numeric_move.py`.

- Replaced unsupported `capture_clip_set` setup with guarded `emit_document_commands`.
- Preserved all numeric values, opaque null/boolean/precision cases, topology, selectors, and assertions.
- Preserved the single provider registration correction.
- Step patches now accurately claim emitted `doc.patch` changes.

Checks passed:

- In-memory compile
- Ruff candidate and parent
- Mypy candidate and parent
- AST assertion/input conservation
- `git diff --check`

Live MAIN6/inverse3 pytest runs were not performed per the source-only restriction; functional behavior remains unverified. Commit message and `DONE` marker are present.