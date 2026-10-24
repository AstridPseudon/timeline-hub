## Report

Implemented a Runtime-only compatibility fix for Agent’s authenticated local fork-owner projection.

- Updated `runtime_protocol/timeline_commit_auth.py`.
- Added focused owner projection tests in `tests/test_timeline_popup_fork_owner_projection.py`.
- Preserved canonical source, sibling, foreign, forged-owner, and no-write guards.
- Reproduced the original 422 with the actual Agent emitter; production acceptance now passes.

Tests:

- `pytest ... popup tests` — 9 passed.
- Production acceptance selector with `ASTRID_CHECKOUT=/home/user/work/agent` — 1 passed.
- Production negative controls — 4 passed.
- Ruff, Pyright, compileall, and diff checks — passed.
- `--timeout=45` was unavailable in this environment; reran without it.
- Full suite not run.

Commit message written and `DONE` marker created. Independent security review remains the next step before merge.