## D127 report

Completed a read-only source/caller/persistence trace for Actual10721.

- Exact element joined to request 3 via key SHA; 352 samples, 3 lost; last phase `authorization`; outcome remains `PENDING`.
- Only bounded routing-frame retention was observed. Provider leaf, wall denominator, response, and final duration remain unknown.
- Proposed minimum fix: helper-only bounded leaf projection plus explicit lifecycle states (`completed`, `raised`, `returned_without_response`, `pending_at_stop`). No product, collector, C0, or privacy-path changes.
- Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-leaf-retention-trace-1600/evidence/`

Tests/checks:

- Targeted pytest: `4 passed, 15 deselected in 1.58s`
- `facts.json`: valid JSON
- `git diff --check`: passed
- Worktree: clean
- No full/live/browser/profile/probe/body tests run.

Unverified: provider dominance, leaf cost, native comparison, SWAP outcome, handler completion, response, and request wall time. Recommended next step is bounded authoring and protected review before any helper activation.