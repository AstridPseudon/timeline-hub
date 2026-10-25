Implemented D134 source-only import.

- Imported the donor test byte-exactly: blob `e63d777f…`.
- Donor parent and receiving HEAD both: `a30e74e…`.
- Only changed file: `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`
- Runtime lockfiles unchanged.
- Preserved all 23 assertions and exact `source_bytes`, `'swap'`, and `'parent'` forwarding.
- Commit message written for harness: `test(timeline): import D134 manifest media fixture plumbing`

Validation:

- Python 3.11 AST/compile: passed
- Ruff: passed
- mypy: passed
- `git diff --check`: passed
- Integration test: 2 expected fixture-setup errors from the known managed-edge rejection; no behavior closure claimed.

Evidence is under the requested worker `evidence/` directory. DONE marker created.