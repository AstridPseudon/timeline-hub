Implemented [test_timeline_restore_effect_order_runtime.py](/home/user/work/wt/agt-R2-restore-order-control-0415/tests/sdk/test_timeline_restore_effect_order_runtime.py).

- Covers real registered Runtime provider, ordinary restore, public undo, exact source/inverse order, canonical document, head/history, dry-run no-write, and idempotent retry.
- Added evidence at `/tmp/.../evidence/restore-order-regression.md`.
- Commit message written with `F-D86/R2`.
- Created `DONE`.

Checks passed:

- AST parse/compile
- Ruff
- Mypy
- `git diff --check`

No pytest or service execution was run, per source-only instructions. Functional MAIN proof remains pending.