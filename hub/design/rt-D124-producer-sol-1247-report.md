**D124 is held.** Exact owned cases improved from **5 failures to 1 pass / 4 failures** on Agent `238ee` + Runtime `5e9ad`.

- Fixed `_commit_patch.py` to capture newly materialized input roots and retain effect-image pins for synthesized ABI-1 steps.
- Preserved original tests, requests, timing, and Runtime guards. Used the exact reviewed scalar setup without editing its fixture.
- New regressions: **2 RED on base → 5 GREEN**, including strict tampering/no-write checks.
- Mounted/source guards: **6 passed**.
- Targeted neighbors/producer controls: **28 passed, 1 failed**; that failure reproduces on base.
- Ruff, mypy, `py_compile`, and diff checks passed. No full suite ran.

Remaining: grouped occurrence fails during undo after occurrence removal; scalar cases fail allocation/materialization authentication. Raw/config seed and typed redo `1755` remain separate and unclaimed.

[Exact commands, results, source hashes, and boundary facts]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D124-producer-sol-1247/evidence/checks.json).

Created `commit-msg` and `BLOCKED`. Next: remaining-owner source review, independent core/security review, then the single farm Agent batch core before adoption.