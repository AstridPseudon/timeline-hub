Implemented F-D86 projection9 fixture repair.

- Preserved authored opaque payloads by syncing `base_payload`/`base_internal_timeline` before duplication.
- Removed fabricated empty-item fallback; direct source indexing remains.
- No assertions, predicates, topology expectations, refusal/no-write guards, or production files changed.
- Only modified `tests/sdk/test_timeline_capture_projection.py`.

Checks:

- In-memory compile: PASS
- Ruff baseline/candidate: PASS
- Mypy baseline/candidate: PASS
- AST conservation: 11 test ASTs identical
- `git diff --check`: PASS
- Behavioral tests intentionally not run per source-only brief; MAIN qualification remains.

Commit message and `DONE` marker created.