PASS — bounded source/capture review.

- Reviewed author report, peer handoff, PLAN §3/R1/R2, and contract §§1–5.
- Only `_commit_patch.py` and new `test_authoring_undo_projection.py` changed. No preview, commit, schema, wire, Runtime, pin, or original fixture changes.
- Authenticated parent reuse, inverse-stage root boundaries, six-key private captures, owner/revision/digest/order/range/history/ABA guards are covered.
- New focused tests: `55 passed`.
- Neighbor tests: `112 passed`.
- Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`: passed.

Known limits:

- Old-HEAD RED result is author evidence: 2 expected failures; I did not recreate an old-source bench.
- Original live/full/browser/HTTP/SDK4/c271 qualification remains intentionally unrun.
- Author’s broader Runtime probes still fail for transient redo alias projection and existing-child native-effect coverage; these are outside this bounded patch and remain unverified.
- Source0248 reorder commit is not an ancestor. Its exact pending hunk is `_managed_boundaries`: add `apply_change` import and guarded `list.move` handling around lines 713/743. Port it in Agent home without overwriting this review’s `_materialization_sites` changes.

No worktree changes were made. Commit message and `DONE` marker were created.