Implemented the bounded clear fix; all four original xfails now pass. Tagged ancestor presence, leaf intent, replay, standalone undo/redo and ABA guards are covered.

Targeted tests: **448 passed, 2 xfailed**. Ruff and `git diff --check` passed. No full suite run.

**Blocked:** clear-then-set batch undo exposes a generic `inverse._patch` defect. Two new strict xfails preserve the positive expectations. Scope clarification is pending because the task explicitly limits product changes to State/Recording/scalar.

[Report with exact commands and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-clear-absent/notes/report.md). Both commit-message files are written. Integration remains held.