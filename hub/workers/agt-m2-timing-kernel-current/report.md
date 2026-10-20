Ported the pure compiler and authoritative stable-ID evaluator correction. Current units, commands, pins, and default timing paths remain unchanged.

Validation:

- Kernel/cycle/checkout/reflow/transcript neighbors: **201 passed, 17 deselected**. Current D07 accounts for the donor’s 202→201 count.
- Word-reference and retained-input neighbors: **97 passed**, plus **2 new V1/V2 cases passed**.
- Current D07 trim replacement tests: **93 passed**.
- Ruff and focused mypy: **passed**.

Exact commands, diagnostic results, and decisions are in [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-timing-kernel-current/notes/report.md). The [API handoff](/home/user/work/wt/agt-m2-timing-kernel-current/design/agent-timing-kernel-current.md) includes source SHAs, types, and missing wiring/parity work.

No blocker. Native authored-reference/default wiring remains separate; no full suite or Runtime default-activation claim. `commit-msg` and `DONE` are written.