## SDK proof-map report

Base: Agent `2007cf7aaf5d304964e68a33e967502a16de1d24`; tree `68b0309c…`. No product/test files changed. Qualified candidates: **11**. Unqualified: **24**.

### Qualified

Receipt refs: `capture0052`, `schema0037`, `helper-map-review-0224`, `persistence-fixture-0008`, `persistence-helper-sol-0037`, `G5-publisher-fidelity-1320`.

- `test_capture_closure_source.py::test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies[False]`
- `test_capture_closure_source.py::test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies[True]`  
  Exact saved/candidate receipt: 6 passed; current capture/test surfaces equal reviewed source.

- `test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden`  
  Exact receipt: 6 passed; schema/current source equality confirmed.

- `test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort`  
  Exact receipt: 3 union/oracle selectors passed; frozen schema unchanged.

- `test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[False]`
- `test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[True]`  
  Exact original receipts: 1 passed each; current helper source surface equals reviewed source.

- `test_timeline_persistence.py::test_a_discard_in_one_process_leaves_the_next_process_with_no_working_copy`
- `test_timeline_persistence.py::test_a_truncated_temp_file_is_never_read_as_the_working_copy`
- `test_timeline_persistence.py::test_a_writer_that_dies_holding_the_lock_does_not_block_the_next_writer`
- `test_timeline_persistence.py::test_publish_after_a_restart_refuses_a_clip_both_sides_changed`
- `test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`  
  Retained persistence receipts pass. The refusal case is also in the dedicated 4-pass publisher-fidelity run.

### Unqualified mappings

Each has a finite missing fact and next owner:

- Clip scalar ABA selector: no current Agent receipt; same-alias ABA is explicitly Viewing-owned. Next: Viewing/F-authoring-ABA-0101.
- All five commit-graph-roots selectors: only aggregate controls/root-assignment coverage exists, not exact selector receipts. Next: Agent current-root/R2 owner.
- Scalar sibling inverse selector: R2’s exact 56-pass receipt is against older production source; current `_commit_patch.py`/`inverse.py` differ. Next: Agent/A4 IMAGE-0043.
- Both occurrence-delete selectors: same current-source mismatch; exact old R2 receipt cannot be carried forward without current-source equivalence. Next: Agent R2 inverse owner.
- `test_conflicts_and_uncaptured_edits_never_write[same]`: aggregate neighbor coverage only; no exact retained receipt. Next: Agent helper owner.
- Three guarded cut-input selectors: no exact current receipts. Next: Agent helper owner.
- Three cut-restart selectors: `[second]` remains blocked by missing authenticated word binding; `[+1s]` and `[None]` lack exact current receipts. Next: Agent/F-helper-review-0107.
- Genuine anchor capture: included only in the retained fixture-control aggregate; no current exact selector/source-equality receipt. Next: Agent G2/helper fixture owner.
- Lost-ACK selector and all four journal-tamper selectors: no exact retained current receipts; aggregate controls do not earn selector credit. Next: Agent helper owner.
- Peer-clip restart selector: prior exact fixture proof predates current `_commit_preview.py` changes; current-source equivalence is missing. Next: Agent helper owner.
- Persistence merge selector: explicitly failed as the sole failure in the 9-pass/1-fail fixture run with Runtime `atomic_scope_changed`; no write occurred. Next: G5/persistence production caller owner.

No Runtime H32, normal-publish, connection, CLI-label, or Viewing-ABA claims were imported.

### Checks

Read-only checks passed:

- PLAN §3 and `contract/commit-v2.md` reviewed.
- Python AST parsing: all 22 selector function families found.
- Stdlib JSON parsing: passed.
- SHA-256/source comparisons and targeted `git diff --quiet`: passed.
- `git diff --check`: passed.
- Worktree remains clean.
- No pytest, Ruff, mypy, full suite, browser/live run, or Git mutation performed for this review.

Commit message and `DONE` marker were written.