## Report

Implemented genuine current-API setup in [test_authoring_media.py](/home/user/work/wt/agt-F-D92-genuine-unused-0242/tests/timeline/test_authoring_media.py:425):

- Real media import and authenticated current Runtime baseline.
- Commit A: real consumer + `media.admit`.
- Commit B: normal consumer removal; retained pin remains in canonical manifest.
- Migrated all three compound paths; original assertions preserved.

Verification:

- Ruff: passed.
- Mypy: passed.
- Python compile: passed.
- `git diff --check`: passed.
- No pytest/helper/full/service suites run per brief.
- Independent bounded API transcript and exact current pairs: [evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D92-genuine-unused-0242/evidence/d92-genuine-setup.md>).

No ledger deletion mapping is needed: the state is reachable through the current API. Protected review remains the next step.