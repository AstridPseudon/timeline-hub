**agt-d09-caller-join is blocked.** I made no changes to the worktree, wrote no commit-msg, and did not create DONE. I wrote the reason to `.../workers/agt-d09-caller-join/BLOCKED`.

The spec describes code and inputs that don't exist on this base (`tl/integration` at 4a75f68f):

- **Viewing's inputs are missing.**
  - Both `tl/vw-m3-d09-known-caller-preservation` and `tl/vw-m3-d09-current-deletion-unit` point at 4a75f68f, so they are empty.
  - There is no `workers/vw-m3-d09-*` directory, so there is no REPORT, `proposal.patch` or `donor-amendment.patch` to read.
- **The scene check and labels aren't in `run.py`.**
  - The only remotion `run.py` is `astrid/packs/rendering/rendering/renderers/remotion/run.py`, which has no scene-check or label code.
  - It has no post-resolve candidate or revision/occurrence identity to join.
  - The scene-check code (`core/timeline/scene_answers.py`, `core/execution/authoring_scene_*.py`) exists only on the frozen R4 candidate-sdk branch, not on integration.
- **The ledger doesn't exist.**
  - There is no `design/` directory and no `design/deletion-ledger.agent.md`.
  - There is no D09 row anywhere in the tree, so I can't find the 5 old blocking-policy assertions to reconcile.
- **Current `onscreen` callers have nothing to reuse.** `sdk/timeline/check.py`, `sdk/timeline/reflow.py` and `overlays/labels.py` call `onscreen.element_coverage(types)`. It reads the element manifests directly, with no registry, theme or props inputs.

To unblock, I need one of these from you:

- Viewing's patches, or the base that contains the ledger file.
- Confirmation that I should port the scene-check from R4 candidate-sdk as part of this task. That is much larger than a join, so it is your call.
