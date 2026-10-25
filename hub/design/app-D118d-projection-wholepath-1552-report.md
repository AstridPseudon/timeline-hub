# D118d report

- Audited finalized source `e02180cedafa581bc8105d77341456b8b1c50b5b` read-only.
- Confirmed the failure boundary: `_saved_document()` supplied scoped child rows; `bundle_from_document()` correctly rejects them. The registered `doc.patch` was never reached.
- Confirmed finalized fixture conversion matches the genuine current canonical converter and preserved all test bodies, assertions, pins, ordering, and goldens.
- Traced the Runtime provider, persistence, saved projection, and opener routes. Post-fix behavior remains unverified; no pytest or own9 rerun was performed.
- Pair-16 source is byte-identical to captured Agent `120d...`; all 16 historical outcomes were PASS. Current Runtime `5e9ad...` remains unverified.

Checks:

- Ruff, mypy, py_compile: PASS on inspected files.
- JSON parsing, AST/source comparison, diff check: PASS.
- Repository worktree: clean.

Artifacts written under the required evidence directory, with empty `DONE` marker and commit message. Next gate is the exact 9-node run against `e02180c` after disk reaches 5 GB, followed by protected review.