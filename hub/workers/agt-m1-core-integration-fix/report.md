Implemented the M1 core corrections: stable source/ownership guards, recorded clip mirrors and retained input pins, empty semantic events, corrected parent intent, and refreshed App goldens.

- Recipe + authoring/structure tests: **120 passed, 1 existing lane deselection**.
- Real provider source tests: **50 passed**, including shared-sibling rebase.
- Ruff, scoped mypy, whitespace checks, and both schema comparisons passed.
- Product delta: **+37 Python lines net**; registry and schema unchanged.

Fixed moves clear anchors without evaluating them. Unconsumed extent/snap queries remain absent; the App restrictions are documented.

No focused blockers remain. Full/live/browser validation awaits the central integration batch. Commit messages are written; no git mutations performed.

[Detailed report with exact commands, decisions, and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-core-integration-fix/report.md)