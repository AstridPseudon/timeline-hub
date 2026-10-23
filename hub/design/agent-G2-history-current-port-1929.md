# G2 current historical-sheet basis port

Applied only the requested `697c8fd3b` product change onto actual base `92d0413ae`: `Checkout.open` accepts and forwards `publication_id`, and `find_version` passes each retained history row's exact revision/publication pair. Added `tests/sdk/test_g5_retained_sheet_basis.py` byte-for-byte from `697c8fd3b` (94 lines). No other source, test, Runtime, schema, pin, or repository files changed.

## Evidence

- Targeted SDK/history selection: **19 passed**.
- Authentic current-pair control: **16 passed** using Runtime pin `2a9e347f` and the existing flat orchestrator archive.
- `git diff --check`: passed.
- Scoped Ruff: 7 inherited production findings, 0 new identities; new test clean.
- Scoped mypy: 1 inherited production finding, 0 new identities; new test clean.
- Credential-shaped scan of all three changed files: **0 findings**.

The first current-pair invocation used a stale archive path and failed only at fixture setup; the rerun used the flat orchestrator archive and passed all 16 tests. No full, browser, HTTP, original FOUR, first-node, c271, or other excluded qualification was run.

Changed-file hashes and the worker report are at `workers/agt-G2-history-current-port-1929/`. Commit message is prepared at that worker's `commit-msg`; no commit, merge, or request was made.
