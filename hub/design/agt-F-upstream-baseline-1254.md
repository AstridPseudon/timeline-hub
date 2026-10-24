## D54a report

Prepared:

- Candidate: `evidence/suites.conf.candidate`
- Install input: `evidence/install-input.txt`
- Suite: `full-upstream-25359`
- Exact Agent source: `25359ed…`, tree `f17171ac…`

Changes from existing `agent full` row:

- Removed only the D09 `ce4fb6…` blob guard; the fixture is absent upstream.
- Added exact baseline HEAD/tree/clean-source guards.
- Preserved environment/module-origin guards and unfiltered `pytest -q -n 3`.

Validation:

- Candidate `bash -n`: PASS
- Baseline preflight/module origins/environment: PASS
- Normalized original-row comparison: PASS
- `git diff --check`: PASS
- Worktrees clean and supplied checkout matches exactly: PASS
- Live registry unchanged; outside-row hash preserved.

No tests, full suite, typecheck, or lint were run. Next step: manager performs sanctioned atomic installation, then queues exactly one service full run.