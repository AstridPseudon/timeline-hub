Implemented the minimal fix.

- Renamed `_timing_evaluators._number` to `_timing_number` and updated 18 local references.
- Preserved facade names, identity, count, and compiler behavior.
- No tests or facade files changed.

Tests:

- Targeted Agent tests: **81 passed**
- Pinned integration neighbors: **89 passed, 5 unrelated existing Stage1 failures**
- Ruff: passed
- `git diff --check`: passed
- No full suite run.

Report: [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-timing-facade-name-fix/notes/report.md)

Commit message and `DONE` marker created.