Implemented on exact base `f91ad0089e`.

`inverse.py` now validates historical payload reads using the selected command’s authenticated input codec. The live publication stays intact. Redo requires the exact recorded root restoration. Ordinary `State` checks and all existing tests remain unchanged; one focused regression file was added.

Validation:

- Original acceptance files: **6 failed / 37 passed → 43 passed**.
- Acceptance files plus 24 new regressions: **67 passed**.
- Neighboring source-copy, identity, sequential, step-undo and corruption controls: **244 passed**.
- Scoped Ruff/mypy and `git diff --check`: **PASS**.
- Normal `make mypy`: **1902/1902**; normal `make ruff`: **2143/2143**, both PASS.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-historical-source-sol-0959/evidence/commands.txt), JUnit XML and before/after source identities are retained in the same evidence directory (**256 KB**).

No blockers or outside-seam changes. No full/browser/HTTP or Runtime durable-acceptance claim; no census credit or ABA20732 timeout claim.

Commit message and `DONE` created. Next: independent review, then harness commit and normal merge.