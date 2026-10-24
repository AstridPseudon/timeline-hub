## Completed

- Added [d32-failure-map.json](/home/user/work/wt/agt-F-D32-tags-0057/d32-failure-map.json), containing all 267 exact unique failure nodes.
- Tags: `ours=267`, `pre-existing=0` because upstream object `90d469808` is unavailable.
- Phases: `call=262`, `setup=5`.
- Corrected the prior census discrepancy: duplicate Stage-1 entry removed; 3 D09 setup nodes and 1 isolated-import node restored.
- Preserved D14/D23/H9 as visible, unskipped, non-PASS scope.
- Included scoped G2/R2/fixture/capture/env/CLI qualifications without claiming full-suite PASS.
- Added independent Runtime and Viewing failover follow-up suggestions, excluding active Agent rows.

Validation:

- Shard-to-map equality: **PASS**, 267/267 unique rows.
- JSON/count/tag validation: **PASS**.
- `git diff --check`: **PASS**.
- No tests or full reruns performed; this was read-only classification.
- Upstream check: `git cat-file -t 90d469808` → object absent.

Commit message and `DONE` marker created.