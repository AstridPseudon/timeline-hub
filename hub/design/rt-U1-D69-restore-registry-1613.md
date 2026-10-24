## Report

- Restored the five exact upstream tests and required same-file helpers in [tests/test_skip_registry.py](/home/user/work/wt/rt-U1-D69-restore-registry-1613/tests/test_skip_registry.py).
- Protected AST review passed: exact upstream bodies, parameters, assertions; all 7 existing test bodies retained.
- Collection: 12 tests; 5 newly restored selectors.

Tests:

- 4 restored selectors passed; `test_an_entry_with_neither_a_job_nor_no_ci_is_rejected` fails because current `DeclaredSkip` lacks `no_ci`.
- Full file: `11 passed, 1 failed`.
- Compile and `git diff --check`: passed.
- Ruff: no new issues; 2 pre-existing B023 findings.
- Pyright: 2 pre-existing findings plus the expected `no_ci` missing-field diagnostic.

Evidence is under [evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D69-restore-registry-1613/evidence/).

Blocked seam: upstream defines `DeclaredSkip.no_ci`; this integration base removed it from `tests/lanes.py`, which was outside the allowed file scope. No workaround or test weakening was made.

Commit message and `DONE` marker created.