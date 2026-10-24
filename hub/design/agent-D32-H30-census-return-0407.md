# F-count report

Created corrected evidence JSON:

[evidence/agent-D32-current-node-reconciliation-H30-corrected.json](/home/user/work/wt/agt-F-census-return-0407/evidence/agent-D32-current-node-reconciliation-H30-corrected.json)

SHA-256: `e311e7ba31dc93a468a24c6574f5417e30f1dee9de0297a5b85f6686aa575bbb`

Changes:

- Corrected census to 142 closed / 125 open.
- Credited six exact render-wire originals from service 27934.
- Retained seven H3 originals open due D40 source drift.
- Preserved all 267 IDs, body mappings, and `ours` tags.
- Preserved exact 33-node Viewing subset.
- Updated obsolete worker labels to Agent/Runtime/Viewing lane ownership.
- Farm checkpoint remains pending.
- No product, test, design, or suite changes.

Checks:

- `python3 -m json.tool ...`: PASS
- Custom census audit: PASS
- 267 unique IDs; 262 call / 5 setup: PASS
- Counts, mappings, tags, Viewing subset, proof references, and Farm-pending checks: PASS

No new suite or test-body execution was performed. Completion marker and F-count commit message were written; harness should commit the worktree.