## Report

Restored both exact upstream tests in [tests/test_skip_guard.py](/home/user/work/wt/rt-U1-D69-restore-guard-1613/tests/test_skip_guard.py). All existing test bodies were retained; upstream body, parameter, and assertion hashes match exactly.

Tests:

- `15 passed, 2 failed` in affected-file suite.
- Failures expose actual product seams:
  - `DeclaredSkip` lacks upstream `no_ci`.
  - Skip guard does not reject declared skips whose condition is false.
- `py_compile`, Ruff, Pyright, and `git diff --check`: passed.

Evidence: [restore-hashes.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D69-restore-guard-1613/evidence/restore-hashes.json), [JUnit XML](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D69-restore-guard-1613/evidence/test_skip_guard.junit.xml).

Commit message and `DONE` marker created. Independent protected review remains pending.