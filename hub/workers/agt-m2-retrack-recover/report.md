Recovered the interrupted source exactly and completed atomic occurrence move/retrack, guarded inverse/redo, lane-membership ABA checks, and portable goldens.

- Targeted regressions: **476 passed, 1 strict xfail**.
- Actual Runtime restart/retry/inverse/redo: **4 passed**.
- Scoped Ruff and `git diff --check`: passed.
- No full suites or browser tests run.

The strict xfail exposes missing shared-source shot/item creation records. That remains an integration blocker; M2 merges stay held pending M1.

[Report with exact test commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-retrack-recover/notes/report.md) · [App contract and golden handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-occurrence-move-contract.md)

Both commit-message files are written. No commits or ref changes made.