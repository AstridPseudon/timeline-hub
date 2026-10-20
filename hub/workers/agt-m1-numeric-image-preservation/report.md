Implemented the 21-line exact-image reuse correction after reproducing both M1 numeric move failures. Added six real Runtime move cases and nine pure conversion cases.

Validation against Runtime `9f9b25c0`:

- Focused suite: **194 passed**, 1 integration deselected.
- Direct Runtime checks: **25 passed**.
- Final central integration: **29 passed**.
- Ruff and diff checks passed.

[Report with exact commands, logs and provenance](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-numeric-image-preservation/notes/report.md).

No blockers. Full suite was not run. Coordination and both commit-message files are written; ready for manager review and queued integration.