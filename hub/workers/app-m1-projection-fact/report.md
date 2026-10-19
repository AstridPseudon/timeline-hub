Implemented the atomic `editProjection` producer and published the Viewing contract.

- Focused Vitest: **421 passed, 1 failed**. Retained regression proves recovery after A’s ACK replaces B’s original basis incorrectly; session-core owner must fix it.
- ESLint and `git diff --check`: passed.
- App tsc: four errors—two baseline errors plus separately owned client/lifecycle fixes.
- No full/browser suites or git mutations performed.

Compose lifecycle/client fixes first, then resolve the recovery regression before acceptance. Commit message written.

[Report with exact commands and findings](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-projection-fact/report.md)