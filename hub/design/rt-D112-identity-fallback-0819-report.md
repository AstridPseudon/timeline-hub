## D112 report

Implemented identity fallback in `TimelineCommitStore`:

- Rebinds verified replacement connections.
- Reopens replaced DB/WAL through `RealmStore._open`.
- Clears memo/baseline before cold full verification.
- Preserves refusal for closed, missing, transactional, invalid, or tampered state.
- Added DB/WAL recovery and post-recovery tamper tests.

Source: `tl/integration` / `c91626f5e905f9336b51aae0486a071d83f0bac7`  
Own commit: pending harness commit.  
Modified pair hashes:

- `timeline_commit_store.py`: `34d0f401...775e56`
- `test_timeline_history_state.py`: `788e1280...ba838b`

Tests passed:

- `tests/test_timeline_history_state.py`: 53 passed
- Verification/routes/lifecycle controls: 98 passed
- Commit port/execution/auth/validation: 246 passed
- `ruff --select E9,F`: passed
- `compileall`, `git diff --check`: passed

The broader acceptance run had 2 baseline failures caused by SQLite authorizer denial of `PRAGMA data_version`; reproducing with the pre-change method showed the same failure.

No full/browser/live-socket suite requested. DONE marker and commit message are present.