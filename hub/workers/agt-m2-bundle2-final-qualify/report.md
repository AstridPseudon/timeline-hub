Applied the approved numeric delta and normal Runtime pin to `4c145dc6`.

- Central qualification: **207 passed**, including the complete 29-case M1 cohort.
- Focused tests: **290 passed**; import fence: **1 passed**.
- Ruff, vendor, CLI generation and invariant checks passed. Mypy retains two identical baseline errors.
- Removed only the nullable-speed xfail after both unchanged cases passed.

Final tree: `1434f42b48fd062248faf1f4abef7ff467186377`. Commit messages are ready; harness commit remains pending.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-final-qualify/notes/report.md).

Candidate is **COMPOSED/REVIEWABLE**. Next: harness finalization, manager review and App qualification. Custom-pack CLI capture inputs remain unsupported; integration awaits PLAN’s M1 record.