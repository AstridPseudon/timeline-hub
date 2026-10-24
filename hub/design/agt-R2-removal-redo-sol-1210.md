Fixed all three legitimate R2 redo failures through the production commit caller.

- `_step_undo.py` reconstructs complete ancestor-config inputs from exact recorded descendant writes.
- `_commit_patch.py` recognizes unchanged retained physical pins when no root-write effect exists.
- Added one focused test file; existing tests and fixtures remain unchanged.

Validation:

- Identical baseline: **327 passed, 7 failed**.
- Fixed source: **334 passed**, including all 43 R1 removal cases and 270 existing cases.
- **17 strict refusal controls pass on both versions; zero lost passes.**
- Nearby inverse tests: **189 passed**.
- Scoped Ruff, qualified mypy, vendor/artifact checks and `git diff --check`: **passed**.

[Exact commands](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-removal-redo-sol-1210/evidence/commands.txt>), XML results, source blobs and comparison evidence are retained in the same directory.

No blockers. No full, gate or live-HTTP runs; durable Runtime behavior remains unverified. Next: independent security review and integration qualification.

Commit message and `DONE` written; no git mutations performed.