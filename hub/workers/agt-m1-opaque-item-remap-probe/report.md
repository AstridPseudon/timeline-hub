Confirmed accepted opaque-data mutation on both M1 and reviewed candidate paths. Applied the authorized context-aware remapper, preserving known identities and source links.

- Focused tests: **178 passed**.
- Actual M1 Runtime tests: **8 passed, 3 strict xfailed** for the separate exact-undo issue.
- Reviewed candidate plus this helper: **6 passed**, including exact undo.
- Ruff and diff checks passed. No full suite run.

[Report with exact commands, decisions, limitations, and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-opaque-item-remap-probe/notes/report.md).

Both commit-message files are ready. Next: compose with the reviewed historical-image reuse fix and remove the restored undo xfails.