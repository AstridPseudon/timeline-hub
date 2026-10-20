Ported exactly the twelve approved paths, preserving current integration work.

- Focused lane: **427 passed, 1 inherited facade failure**, reproduced on the unmodified base.
- Original/independent recovery probes: **20 passed**.
- Central renderer-blocked Runtime lane: **4 passed** on Agent tree `73fd67c0` + Runtime `94114269`.
- Diff check passed; Ruff reproduced three inherited diagnostics.

No history-port blocker. Separate writer migrations remain open; route the facade failure to the timing owner.

[Detailed report and exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-history-current-gate/notes/report.md). Commit message and `DONE` written.