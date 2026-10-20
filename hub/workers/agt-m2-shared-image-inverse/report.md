Added four permanent real-provider regression cases. The existing candidate fix already restores exact shared-source closures; qualified M1 reproduces the failure. No product changes needed.

Validation: **356 targeted tests**, **9 Runtime 6be tests**, **7 Runtime 9f tests**, and **52 central paired M1 tests** passed. Ruff and diff checks passed; no full suite run.

Exact commands, limitations, and next steps are in [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shared-image-inverse/notes/report.md). Both commit-message files are written. No blockers. Recommend Runtime-owner review of its existing strict xfail against this candidate.