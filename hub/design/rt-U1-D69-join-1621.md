## Report

Imported the exact `tests/test_skip_registry.py` blob from `tl/rt-U1-D69-restore-registry-1613`. Only that file changed; `tests/lanes.py` and `tests/test_skip_guard.py` remain identical to policy1616.

Tests:

- Required suite: **28 passed, 1 failed**
- Failure: restored `no_ci` acceptance test; the exact registry blob still rejects entries whenever `ci` is empty because its checker lacks the policy branch’s `no_ci` handling.
- Compile: passed
- `git diff --check`: passed
- Ruff: two inherited B023 findings
- Pyright: environment-unresolved pytest imports plus inherited optional-regex diagnostics; not cleanly qualifying

Evidence: `workers/rt-U1-D69-join-1621/evidence/`.

Blocked marker and conventional commit message were written. No `DONE` marker was created. Next step requires reconciling the exact registry blob with `no_ci` enforcement.