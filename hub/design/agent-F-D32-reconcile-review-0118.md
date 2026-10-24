Completed evidence-only reconciliation in [agent-D32-current-node-reconciliation-0110.json](/home/user/work/wt/agt-F-D32-reconcile-review-0118/agent-D32-current-node-reconciliation-0110.json).

- Preserved exact identity: 267/267 nodes, 262 call + 5 setup, all `ours`.
- Preserved pass credit: exactly 136; no arithmetic-inferred passes.
- Reconciled original 76 owners plus 55 formerly unowned rows: 131 active-owner rows, 0 genuinely unowned.
- Assigned the seven isolated import-source gaps to Runtime 0118; proof remains explicitly missing.
- Recorded capture, R2, schema, helper, fixture, G5, G2/G3/G4, and manager additional-owner evidence without duplicating product authors.
- Upstream object `90d469` remains absent; raw full result remains `17159 passed / 262 failed / 5 errors / 4 skipped`.

Validation passed:

- Read-only source-map/head/count audit.
- `python3 -m json.tool agent-D32-current-node-reconciliation-0110.json`
- `git diff --check`
- JSON-only diff confirmed.

No product tests, full runs, installs, or Git mutations were performed. Commit message and `DONE` marker were created.