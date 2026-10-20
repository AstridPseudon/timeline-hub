Implemented the three test-only isolation fixes.

- Persistence checkout loads before the live holder starts.
- VibeComfy environment variables are cleared before the fake subprocess probe.
- Generic-host expectations use the explicit test environment.

Validation:

- Targeted tests: **3 passed** in isolated and full-profile environments.
- Persistence/history suite: **64 passed, 1 skipped** in both environments.
- Adjacent stage1/generic-host tests: **15 passed** in both environments.
- `git diff --check`: passed.
- No full suite or shared dependencies modified.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-tests-lock-env-isolation/notes/report.md)

Commit message and `DONE` marker created.