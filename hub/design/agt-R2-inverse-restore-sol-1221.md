Implemented the assigned inverse correction in the three owned files plus one new regression file. Authenticated aggregate restoration preserves literal IDs; redundant projection images are removed only after exact canonical-closure comparison. Source/history evidence remains intact.

Results:

- New regressions: **2 failed/7 passed → 9 passed**.
- M1 exact ten: **10 failed → 10 passed**.
- Requested M1 126: **121 passed, 5 failed**; all five reproduce with unchanged HEAD implementations.
- Adjacent cohort: **422 passed, 1 known failure**, 19 integration cases deselected. Two separately owned fork-redo failures also remain.
- Strict foreign/corrupt/ABA controls: **17 passed**.
- Additional neighbours: **224 passed, 7 failed**; all seven reproduce unchanged as fixture-helper lookup failures.
- Scoped Ruff, qualified mypy, vendor/artifact checks, compilation and diff checks passed. All **46 original test ASTs remain identical**.

[Exact commands, results and XML evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-inverse-restore-sol-1221/evidence/commands.txt>).

**Not merge-qualified.** Next: join the separately owned redo correction and resolve the baseline fixture failures. Direct slash-ID leaf addressing also exposes an unowned native-parser failure, left untouched.

No full/gate/live-HTTP qualification. Commit message and `DONE` written; no git mutations.