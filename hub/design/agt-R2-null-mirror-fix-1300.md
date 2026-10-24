## Report

Implemented the strict `logical_parent` normalization and added one focused regression file.

Tests/checks:

- Focused regression: `7 passed`
- Direct clip-delete shape tests: `5 passed`
- M1 suite: `124 passed, 2 failed`
  - `null-payload`: downstream `validation.py` rejects retained `None`
  - `null-config`: protected emitter rejects retained `None`
- Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`: passed.

I tightened the proposed hunk to accept only explicit `None`/list pairs, preserving scalar and registry refusals.

Blocked: the remaining failures require changes outside the assigned `logical_parent/effect_diff` scope or protected helpers/tests. Evidence XML is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-null-mirror-fix-1300/evidence/`

Commit message and `BLOCKED` marker were written; no `DONE` marker was created.