Fixed the redo regression with **2 net product lines**, porting reviewed M2’s exact reverse source-alias guard.

The four-revision comparison confirmed old M1 accepted redo; exact-image undo introduced the refusal. Permanent exact undo→redo→undo/rematerialization tests now pass, alongside source-identity and ABA refusal controls.

Validation:

- Focused suite: **189 passed, 1 integration deselected**.
- Actual Runtime9f provider tests: **21 passed**.
- Central final-candidate M1 lane: **23 passed**.
- Ruff and diff checks passed.

[Report with exact commands and revision comparison](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-shared-redo-compat/notes/report.md). Coordination and both commit-message files are ready.

No blockers. Full suite was not run. Recommend manager review and harness integration.