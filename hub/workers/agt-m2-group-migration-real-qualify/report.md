## Report

- Updated only the trusted Runtime helper pin in `tests/sdk/test_timeline_group_migration_runtime.py` from `7c6e4e...` to `382f523...`.
- Helper SHA256: `5e152bfa716b9003b831648cad16f6adb9c334cd18a6a7cf32a31accefe82617`.
- Agent: `746440c4...`; Runtime: `d691ddad...`.

Tests:

- Pinned Runtime migration file: **7 passed, 2 failed**. Both failures reach Agent provider, then fail with `semantic identity boundary differs from writes` / `semantic identity history is unavailable` before migration acceptance.
- Neighbor migration/provider/retained-source tests: **68 passed**.
- Ruff and `git diff --check`: passed.

No accepted migration, undo/redo, or same-created-ID proof is claimed. Minimal fix recommendation: reconcile trusted bootstrap’s parent-replacement record with the Agent boundary bundle used by `_check_reservations`/`_load`, preserving existing guards.

Reports:

- [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-migration-real-qualify/notes/report.md)
- [m2-group-contract.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-group-contract.md)

Commit message written; harness should commit the worktree.