Implemented AG03 fixture repair.

- Uses Main `tiny.json` data and Runtime’s existing `seed_trusted_legacy_parent` helper.
- Proves startup admission, public SDK open, authenticated NativeSheet `timing.for.card` edit, disjoint rebase, restart readback, and undo.
- No product/schema changes.

Tests:

- Central native HTTP node: `1 passed in 2.98s`
- Ruff: passed
- `git diff --check`: passed
- No full suite run.

Artifacts:

- [Test change](/home/user/work/wt/agt-m2-sheet-legacy-cut-fixture-gate/tests/editing_conformance/test_native_sheet_current_runtime.py)
- [Design](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-sheet-legacy-cut-native-gate.md)
- [Worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-sheet-legacy-cut-fixture-gate/report.md)

DONE and commit message files created.