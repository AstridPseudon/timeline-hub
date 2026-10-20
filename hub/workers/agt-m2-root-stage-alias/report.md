Fixed both root-stage xfails without changing their positive assertions. Created-root child bindings and root/child alias guards now survive replay, compile/reload, undo, and redo.

- Targeted tests: **770 passed, 3 held xfails**.
- Central official Runtime lane: **52 passed, 1 existing xfail**.
- Ruff, diff checks, and M1/parent-label byte goldens passed.

[Report with exact commands, decisions, and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-root-stage-alias/notes/report.md). Both commit-message files are written.

No code blockers. Full suite and new root-wire qualification remain unrun. Ready for manager review; M2 remains held pending PLAN M1.