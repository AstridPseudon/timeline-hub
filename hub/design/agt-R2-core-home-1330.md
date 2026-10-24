## D30 report

Read-only qualification completed on Agent `47b744dfe908dba1b9b09251d7fa2da3eb0530a6`, Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06`. Worktree remained clean; no source changes.

- R2 reviewed source custody: PASS. Reviewed R2 blobs are present in actual home; all 46 original M1 test ASTs/parameters/assertions match.
- Strict R2 controls: `17 passed`.
- Reviewed null/validation controls: `46 passed`.
- Ordinary core checkpoint: `152 passed, 6 failed`.
  - Required blocking core: `152/158 PASS`; `5 FAIL`; `1 UNKNOWN`.
  - D23 order 170 visibly failed as expected/deferred.
  - D13 order 162 is UNKNOWN: no qualified current-tuple existing profile/binding carrier; incompatible child profile was not used.
- Remaining required core open: `6` (five failures plus D13 unknown).

Failures and owner seams:

- Orders 11, 98, 99: G4 fork reservation/replay seam, `commit.py:821–833`, `fork source binding changed`.
- Order 13: same G4 seam, `commit.py:834–837`, `fork predecessor boundary changed`.
- Order 213: helper/persistence timing seam, `_timing_evaluators.py:385–387`, missing exact word binding.
- D23 order 170: same timing seam, retained as expected deferred failure.

Static checks: qualified mypy, vendor lock, artifact manifest, and `git diff --check` passed. Ruff reported eight existing import-order findings; none were changed.

Durable evidence:

- [core159-old276-map.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-home-1330/evidence/core159-old276-map.tsv)
- [core159-ordinary.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-home-1330/evidence/core159-ordinary.xml)
- [r2-strict-17.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-home-1330/evidence/r2-strict-17.xml)
- [r2-null-validation-46.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-home-1330/evidence/r2-null-validation-46.xml)

No full/gate/HTTP/child run performed. Commit message and `DONE` marker created.