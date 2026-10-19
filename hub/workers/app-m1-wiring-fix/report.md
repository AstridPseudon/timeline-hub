Fixed disposal durability, history ownership, scope cleanup, and response narrowing against official 0.2.1 types. Submit → dispose now preserves the original intent; late ACK/error and project-switch cases pass.

- Focused tests: **25 passed**.
- Neighbour tests: **174 passed**.
- ESLint and `git diff --check`: passed.
- Actual App typecheck: only the two documented baseline errors remain.
- No full/browser tests or git mutations performed.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-wiring-fix/report.md) and commit message are written. Ready for manager composition and the separately assigned browser journey.