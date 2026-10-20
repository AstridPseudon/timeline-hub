## Completed

- Fixed native and legacy trim to store `hold = to - from` in source seconds.
- Added speed-2/rational-speed, FPS/half-open geometry, inverse/redo, and stored-hold preservation tests.
- Updated portable golden and provider expectations.
- Added the required design note.
- Wrote [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-trim-source-units/notes/report.md) and both commit-message files.

Tests:

- Trim tests: **91 passed**
- Neighbor timing/model tests: **58 passed**
- Shared editing/checkouts: **210 passed, 17 deselected**
- Ruff passed for new/changed non-model files; `git diff --check` passed.
- Existing `model.py` import-order warning confirmed present on base.

Full/integration suites were not run per assignment.