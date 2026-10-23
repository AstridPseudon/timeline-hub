# G5 native-qualified join handback

Status: scoped source join complete; final bounded evidence is **82 passed, 5 failed**. The detached-duration target is green after repairing the retained fixture from the generated head pair.

Source provenance: base `cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6`; source commits `3996822a0`, `be2b83ae5`. Only these four test files changed:
- `tests/packs/timeline/test_cli_commit_move.py`
- `tests/packs/timeline/test_cli_commit_trim.py`
- `tests/packs/timeline/test_cli_native_sheet.py`
- `tests/packs/timeline/test_verbs_working_copy.py`

The detached fixture now copies `generated.head` into the generated `r0` base pair and saved checkout, re-renders the retained sheet, and passes `test_original_detached_apply_uses_retained_duration_target`. No product change or guessed publication was added.

Evidence:
- Four-file collection: 87 collected.
- Final bounded four-file pytest: 82 passed, 5 failed.
- Detached target follow-up: 1 passed.
- Scoped Ruff, compileall, mypy, and `git diff --check`: passed.
- No full/live/browser/integration suite.

Remaining five are recorded in the worker report: one trim accepted-bundle base metadata mismatch, three rational inverse base metadata mismatches, and one imported legacy draft-flow next-step wording assertion. They remain unmodified real failures.
