Implemented scoped semantic ID retirement for seeded rows and implicit aggregate children, preserving inverse/redo and separate owner namespaces.

- **482 targeted tests passed**, including 20 new regressions.
- **2 existing real Runtime qualification tests passed.**
- Ruff and `git diff --check` passed.
- Full suites were not run, as directed.

New retirement scenarios have unit-port coverage; real Runtime qualification remains a follow-up. Integration stays held pending the required M1 PLAN record.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-semantic-reservations/notes/report.md). Both commit-message files are written. No Git mutations performed.