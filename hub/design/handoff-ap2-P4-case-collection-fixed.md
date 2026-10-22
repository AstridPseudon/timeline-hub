# Handoff: P4 case-collection provenance repair

Result: **collection repaired; execution remains pending**. No P4 proof claim is made before G2/G3/R2 integration.

Changes:

- Replaced the CLI provenance mapping with the existing single-edit test `tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_literal_move_uses_native_outbox`, whose command is one literal clip move.
- Replaced the Python `initial_bundle` setup mapping with the existing edit test `tests/sdk/test_timeline_sync.py::test_failed_ack_write_recovers_the_original_flight`, which calls `TimelineSession.move` once.
- Added source-symbol and single-edit AST validation so a missing/non-edit symbol or multi-command source is rejected without depending on the corrected test names.
- Preserved the ten ordered note steps, one-commit/ten-command expectation, show/history assertions, independent guarded undo, same-field conflict, bounded rerun, and pending execution status unchanged.
- Deleted the candidate root `report.md` as requested. No production, generated, schema, pin, or shared-dependency files changed.

Checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py
2 passed, 2 warnings in 0.75s

/root/.local/bin/ruff check tests/sdk/test_p4_commit_cases.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_cases.py
Success: no issues found in 1 source file

git diff --check
pass
```

The pytest warnings are the existing unknown `timeout` and `timeout_method` configuration warnings from the available venv. No full/live/socket/browser suite was run. The case execution is blocked on the planned G2/G3/R2 seams; C0b and the adopted C0c unique-physical-root principle remain the governing contract context.

Next step: review/merge this fixture-only change, then execute the cases only after G2/G3/R2 integration and their targeted evidence is available.
