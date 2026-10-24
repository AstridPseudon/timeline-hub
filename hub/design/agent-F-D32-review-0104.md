## D32 review: PASS with limits

- Published artifact: 260,092 bytes; unchanged.
- Raw shards: 511 failure records → 267 unique `(nodeid, phase)` rows.
- Exact match: artifact `267/267`; phases `262 call`, `5 setup`.
- Full result: `17,159 passed, 262 failed, 5 errors, 4 skipped, 17,430 collected`.
- Tags: `ours=267`, `pre-existing=0`; conservative ownership, not project-blame.

Pre-existing comparison is pending: `git cat-file -t 90d469808` returned exit 128 because the upstream object is absent. No false upstream proof was claimed. D14/D23/H9 remain visible and receive no PASS credit.

Separate bounded reports qualify 37 exact raw IDs (D13, P4 symbol, installer/bootstrap, 7 CLI-surface nodes, 23 skip-guard nodes, and 2 lane nodes). These are current-head proofs only; they do not change the raw full-run FAIL or artifact counts.

Unassigned independent families:

- `D32-RUNTIME-FAILOVER-01`: 62 Runtime child-import/OPS nodes.
- `D32-VIEWING-FAILOVER-01`: 6 missing-render-result nodes. The proposed “renderer/threejs remainder” needs exact partitioning; the 22 execution/rendering nodes split into 7 generic-host, 1 freeze, 3 service, 1 builtin, 1 ffmpeg, 1 Remotion, 1 export-adapter, 6 Three.js, and 1 Stage1 node.

Existing `F-authoring-publish-writer` and `F-authoring-ABA` rows are already assigned and should not be duplicated.

No product, test, schema, pin, environment, Git, baseline, full-suite, or body rerun was performed. `DONE` and the required commit message were created.