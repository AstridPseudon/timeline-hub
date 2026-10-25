## Report

Implemented physical DB/WAL identity recovery in `runtime_protocol/timeline_commit_store.py` and additive security/history tests.

- Reopens the verified canonical path after DB/WAL replacement instead of trusting stale untracked handles.
- Preserves valid current-handle rebinding.
- Fails closed on active transactions, foreign handles, reopen races, tampered swaps, and resets memo state before fresh verification.

Tests:

- History controls: `86 passed`
- Adjacent runtime controls: `247 passed, 40 deselected`
- Targeted state suite: `61 passed`
- Compileall and `git diff --check`: passed
- Ruff: 10 inherited diagnostics, zero new
- Pyright: inherited diagnostics only, none on changed lines

The genuine source-constructed SWAP replay remains NOTRUN: the published recipe lacks the historical private provider/binding payload. Exact historical identity remains UNKNOWN.

Commit message written and `DONE` created.