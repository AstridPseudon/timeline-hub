# agt-F-provider-undo-review-0959

## Verdict

**Causal classification: PASS.** The six failures are one real Agent provider undo defect, not fixture misuse or stale-collaborator setup. Product behavior remains failing and belongs solely to HARD Sol `agt-R2-historical-source-sol-0959`.

## Evidence

- Retained R1 author/reviewer packet: **19 passed, 6 failed**, identical before/after.
- Current retained R1 lane: **167 passed, 4 failed**; all new R1 tests passed.
- Exact failures:
  - Four `test_provider_occurrence_fork.py` selectors.
  - Two `test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[1/2]`.
- All six are absent from the exact **267-node census**; census count unchanged.
- Passing source-copy controls exercised the production inverse caller and accepted receipts, but do not cover fork identity reversal.

## Causal seam

The smallest seam is:

- `astrid/sdk/timeline/inverse.py:842–843,1054`: `_validate_inputs()` validates historical inverse scratch state through `_physical_state()`.
- `astrid/sdk/timeline/_command_state.py:290–304`: `State.shot_item_map()` requires the current occurrence source to equal the occurrence in immutable `_runtime_document`.

A valid accepted fork has `_runtime_document` pointing to the forked publication. Undo legitimately restores the historical occurrence to its prior source while retaining that accepted publication as the immutable runtime document. The guard therefore compares two legitimate evaluation boundaries as though they were the same source and raises `identity_conflict: shot item source changed`.

The smallest repair boundary is historical-source handling in the Agent R2 inverse path, preserving authenticated materialization/provenance and all existing guards. No Runtime defect was identified.

## Checks

- Offline source-boundary control with pinned Runtime: passed; reproduced the exact `identity_conflict`.
- Census selector audit: 267 nodes; all six absent.
- `git diff --check`: passed.
- Worktree: clean; no tracked edits.
- No full suite, five-file lane, browser, HTTP, live service, or ABA rerun performed.

`DONE` and the task-specific commit message were written.