Implemented the admission fix: unchanged A retains its old record/blob; only new B receives a new full-pack snapshot. Manifest-only no-ops and legacy refusal remain intact.

- Pack/PARAM neighbors: **425 passed, 4 unchanged xfailed**.
- New real Runtime b3 custody/PARAM test: **1 passed**.
- No new lint findings; `git diff --check` passed.
- No blockers or policy deviations. Full/host suites were not run.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-mixed-admissions/notes/report.md)

Both commit-message files and the absolute Runtime coordination handoff are ready. Next: harness commit and composer review; **M2 integration remains held**.