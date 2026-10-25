## Report

Implemented F-D86 in [test_commit_runtime_m1.py](/home/user/work/wt/agt-F-M1-legacy-baseline-0355/tests/editing_conformance/test_commit_runtime_m1.py).

- Reused the genuine accepted legacy `film` baseline.
- Removed the empty-target duplicate/remapping setup.
- Kept registered provider commits, original topology, pins, opaque fields, and consumer tests.
- Corrected only the setup-history expectation to `legacy_unknown` for the preserved baseline.
- No product or other test files changed.

Checks:

- In-memory AST/compile: PASS
- Ruff candidate and parent via stdin: PASS
- Mypy: PASS
- AST test inventory/conservation: PASS
- `git diff --check`: PASS
- Pytest, collection, services, and MAIN affected-23 suite: not run per source-only brief.

Protected review and exact MAIN23 qualification remain pending. `DONE` and the F-D86 commit message were created.