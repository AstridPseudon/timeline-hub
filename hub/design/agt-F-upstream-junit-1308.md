## D30 Report

- Updated only `full-upstream-25359` in `suites.conf`, adding the single durable `--junitxml` argument.
- Preserved all guards, environment, source/tree checks, and unfiltered `pytest -q -n 3`.
- Used guarded atomic replacement with UTC backup.
- Evidence: [upstream-junit-instrumentation.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-upstream-baseline-1254/evidence/upstream-junit-instrumentation.json)

Validation:

- `bash -n .../tests/suites.conf` — PASS
- Byte/argv/environment/path validator — PASS
- Baseline row count: 1; JUnit argument count: 1
- Worktree status — clean
- No full suite or test service request made, as instructed.

Commit message and `DONE` marker are written.