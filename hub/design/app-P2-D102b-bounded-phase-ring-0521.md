Implemented bounded phase-ring repair in:

- `tests/helpers/p2_commit_phase_capture.py` — blob `65850646f260f2214aaa90d94355ce788776aec5`
- `tests/test_p2_commit_phase_capture.py` — blob `26ca4039aa1d3bcd183689d522186a5689220b23`

Behavior: rolling last-N ring, final failed/pending request retention, byte-bound truth metadata, deterministic shutdown snapshots, thread-safe sequencing, unchanged privacy/watchdog behavior.

Tests:

- Central exact targeted suite: `17 passed`
- In-process local controls: `15 passed`
- Compile, Ruff, helper-only Pyright, and `git diff --check`: passed
- Full two-file Pyright reports only missing `pytest` import in the test environment.
- No full suite run.

Commit message and `DONE` marker created. Independent Luna review is still required before normal Runtime merge.