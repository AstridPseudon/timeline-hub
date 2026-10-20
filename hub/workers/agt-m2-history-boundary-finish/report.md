Completed the boundary fixes and permanent regressions.

- Targeted tests: **386 passed**, including all four boundary requirements and both lost-ACK probes.
- Central renderer-blocked provider tests: **4 passed**, including real retained A→B→A restore.
- Restore writes now preserve undo sources until atomic replacement succeeds.
- No full suite requested. Ruff baseline and mypy remain unqualified; AG01/AG03/WC7–8 remain open.

[Report with exact commands and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-history-boundary-finish/report.md). Commit message and `DONE` written. Recommend narrow-porting onto current integration.