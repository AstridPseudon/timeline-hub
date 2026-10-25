## D118a report

- No code or test changes made; target remains byte-identical to base/original2016 (`c0379c95…`).
- Static checks passed: Ruff, mypy, `py_compile`, `git diff --check`.
- AST conservation passed: 16 function bodies and 35 assertions unchanged.
- Exact D120 node was not behaviorally rerun: approved Runtime `42aad0e…` checkout is unavailable; held D111b Runtime and copying it were forbidden.
- Remaining unapplied owner: Agent SDK timing/word-binding implementation. The exact `"second"` setup lacks an authenticated captured word binding; adding one would alter the required document/history.
- Created `BLOCKED` with details, evidence facts, node log/XML, and D118a commit message. Worktree is clean.

Recommended next step: restore the approved Runtime checkout, then rerun the unchanged node after the Agent timing/word-binding seam is addressed.