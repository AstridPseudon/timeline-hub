# Report

Completed readonly H30/D43 census reconciliation.

- Totals: **267 nodes; 172 closed, 95 open**.
- Delta: **30 exact closures** — 24 Sheet, 4 CLI, 2 Scene.
- Artifact: [corrected JSON](/home/user/work/wt/agt-F-count-delta-0509/evidence/agent-D32-current-node-reconciliation-H30-corrected.json)
- SHA-256: `990f231afced56377202ff9d7d3fa2705d075f30a09bdd96c58ce962c2fe047f`
- Mapping: [CSV](/home/user/work/wt/agt-F-count-delta-0509/evidence/agent-D32-current-node-reconciliation-H30-delta.csv), [JSON](/home/user/work/wt/agt-F-count-delta-0509/evidence/agent-D32-current-node-reconciliation-H30-delta-mapping.json)
- Limits: [human-readable summary](/home/user/work/wt/agt-F-count-delta-0509/evidence/agent-D32-current-node-reconciliation-H30-limits.md)

Validation:

- JSON parsing: PASS.
- Structural preservation audit: PASS — exact IDs, phases, tags, body/assertion mappings, and prior proof records preserved.
- No product tests run, per task.
- `git diff --check`: PASS.

Kept open: three track-label rows, ABA 11466, IMAGE inverse, D40, H3 0508, renderer timeout 0509, Farm checkpoint, and all unrelated nodes. D44 and historical Runtime evidence receive no census credit.

Commit message written and `DONE` marker created.