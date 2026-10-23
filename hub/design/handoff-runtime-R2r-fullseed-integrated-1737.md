# Runtime R2r actual-integrated qualification — 1737

**Bounded PASS on the actual merged Runtime tree.**

- Runtime: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Immutable Agent: `/home/user/work/wt/agt-pin-bac09418`, `bac094180aef38a77b86ab165962e6159f873c60`, tree `3c9296e3670586e920f921c9b1b95bbb99b53b82`.
- Actual merged tree is identical to reviewed author `a00e009df4f568b2496291d3357b65dcfee8ca7c`; both worktrees were clean before/after.
- Exact required command passed: **67 passed in 63.80s, exit 0**.
- The focused run retained the public `RuntimeService.commit_timeline` → coordinator → private request commit port → store path, 21 commands, 21 steps, 21 raw assertions, receipt/history/restart/retry/no-write checks, and the sequential scope negatives.
- `git diff --check d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b HEAD`: exit 0.
- Ruff/Pyright were reused from the independent review (0 diagnostics) because the actual source is unchanged; no source or test edits were made here.

Known limits remain unchanged: the broader exact cohort is **437 passed / 1 known Agent-owned transcript-pin failure**, and the original-nine is **9 passed** from prior evidence. No cohort/full/browser/native/P2/P3 rerun or HTTP PASS claim is made here. The known failure must remain a strict Runtime refusal and go to the Agent capture owner.

Durable evidence and the exact command output are in [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-fullseed-integrated-1737/report.md) and its evidence directory.
