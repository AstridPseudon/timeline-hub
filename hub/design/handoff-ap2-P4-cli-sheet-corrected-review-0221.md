# Handoff: ap2-P4-cli-sheet-corrected-review-0221

## Verdict

**FAIL for the independent-review gate; targeted checks are green.**

The correction is valid on the production semantic sheet route and correctly
abandons the rejected `doc.patch`/`atomic` expectation. It changes only
`tests/sdk/test_p4_cli_sheet_v2.py` relative to `68f2b23f` and has no markers,
skips, product/fixture/pin/generated changes. The parser → handler →
`NativeSheet` → semantic `capture_move` → `TimelineSession` → durable outbox
path is real; only the generated client transport boundary is fake. The test
proves one call, exact semantic command and v2 request metadata, base/source/
label/step/key, presence of accepted canonical/digest/revision/commands fields
and a receipt, and full accepted-bundle equality to the native execute oracle.
It does not compare the accepted reply field values to the expected command or
bundle.

The gate is not met because the test does not also directly assert an unchanged
sibling/raw field against `original`; it only uses oracle equality plus direct
assertions for the authored `at` and derived `app` fields. Add explicit sibling
and raw/closure assertions while retaining the oracle. Reply-field assertions
are also presence-only, not value-level wire checks.

The fake does not prove Runtime, merged/explicit-head/steps/dependencies/
`merge_mode` replies, conflict reason/head, invalid structured errors, preview
`would_status`/history, show/history readback, response-value equality for the
presence-only fields, or ten-note/per-step undo. No H3/P4DONE/native-history
claim is made. Prior e73813PASS/755d3PASS remains
scoped and was not broadly repeated.

## Checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_cases.py
3 passed, 1 warning (pre-existing unknown pytest timeout option)
/root/.local/bin/ruff check tests/sdk/test_p4_cli_sheet_v2.py
PASS
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_cli_sheet_v2.py
PASS
git diff --check
PASS
```

No full/browser/socket/Runtime suite was run.
