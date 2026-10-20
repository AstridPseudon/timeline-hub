Implemented on `tl/agt-m2-recover-facade-ledger-first` (base `afcb326c`).

- Removed facade preflight rejection of historical versions.
- Forwarded explicit `version`, `expected_version`, and idempotency key unchanged.
- Updated tests for exact replay after catalog advance and Runtime-owned historical refusal.

Tests:

- `pytest -q tests/sdk/test_native_timeline_facades.py tests/sdk/test_workspace_client_timeline_commit.py` — 38 passed.
- Focused Ruff test file — passed.
- `git diff --check` — passed.
- Full/HTTP catalog gate not run; awaiting fixed Runtime SHA.

Wrote commit message and empty `DONE` marker as required.