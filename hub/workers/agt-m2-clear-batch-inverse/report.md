Implemented the generic `_patch` fix. Both strict xfails now pass; 100 new cases cover nested presence, orderings, replay, exact undo/redo, ABA, and disjoint guards.

- **576 targeted tests passed**; Ruff and `git diff --check` passed.
- M1 goldens remain byte-equal.
- Optional structural overlay was unnecessary.
- No blockers; full/integration suites were not run. M2 integration remains held.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-clear-batch-inverse/notes/report.md). Both `commit-msg` and `commit-msg.txt` are written and identical.