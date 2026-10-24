## Report

Completed documentation-only E2/D81 deliverables:

- [E2 design](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-E2-net-lines-plan-2008/evidence/E2-net-lines-design.md>)
- [Inventory TSV](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-E2-net-lines-plan-2008/evidence/E2-net-lines-inventory.tsv>)
- [Sizing](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-E2-net-lines-plan-2008/evidence/sizing.md>)

Key decisions:

- Conservative post-ZIP migration using existing Runtime authority.
- Preserve schema-1 markers, `Recording`, `prepared_records`, exact retries, and immutable history.
- Missing facts become `legacy_unknown`; no synthetic v2 facts or unsafe undo.
- Estimated net reduction: 87 removable lines − 64 additions = ~23 fewer lines.
- Implementation/review estimate: 52 worker-hours; risk high.

Validation:

- All TSV citations and source ranges verified at pinned SHAs.
- `git diff --exit-code` — passed.
- `git diff --cached --exit-code` — passed.
- No tests run; task explicitly required no code/test work.
- No repository/design/report files modified.

Commit message written and `DONE` marker created.