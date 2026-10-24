## SDK-map0603 corrected report

The historical `11 qualified` count was wrong. The two schema selectors were explicitly excluded from this review and are not qualified.

Qualified: exactly 9 selectors.

- Capture closure:
  - `test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies[False]`
  - `test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies[True]`
  - Receipts: `agent-F-capture-integrated-0052`, `agent-F-capture-review-0037`; retained 6-case run passed.
- Contiguous helpers:
  - `test_contiguous_helpers_keep_sequential_steps[False]`
  - `test_contiguous_helpers_keep_sequential_steps[True]`
  - Receipt: `agt-F-helper-map-review-0224`; both accepted/merged; durable evidence SHA `b2044948…`.
- Persistence originals:
  - `test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`
  - `test_a_writer_that_dies_holding_the_lock_does_not_block_the_next_writer`
  - `test_a_truncated_temp_file_is_never_read_as_the_working_copy`
  - `test_publish_after_a_restart_refuses_a_clip_both_sides_changed`
  - `test_a_discard_in_one_process_leaves_the_next_process_with_no_working_copy`
  - Receipts: `agent-F-persistence-fixture-0008`, `agent-F-persistence-helper-sol-0037`; the merge-positive remains the sole failure.

Unqualified: exactly 24 reviewed SDK selectors, with existing limits and owners unchanged:

- scalar ABA: 1
- commit-graph-root selectors: 5
- scalar sibling inverse: 1
- occurrence-delete selectors: 2
- conflict `[same]`: 1
- guarded cut-input selectors: 3
- cut-restart selectors `[second]`, `[+1s]`, `[None]`: 3
- genuine anchor capture: 1
- lost-ACK: 1
- journal-tamper selectors: 4
- peer-clip restart: 1
- persistence merge-positive: 1

Schema selectors excluded/pending separate fix: exactly 2.

- `test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden`
- `test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort`

The separate `schema-original-evidence-0600` result is a finite FAIL: production commit `544d589ca6` added `media.admit`, while both provider-only censuses remain stale and need fixture mapping. Author `0605` owns that fix. The original review brief explicitly excluded these two selectors.

Arithmetic: `9 + 24 + 2 = 35` exact assignment. This review independently covered 33 selectors; 2 were delegated and are not qualified. Candidate full count is therefore 9, not 11, pending this corrected independent report.

The retained source/receipt finding remains that current production callers use the v2 request fields, idempotency key, accepted/merged/preview receipts, and structured failures: `api_version`, scope IDs, exact base revision/publication pair, commands, label, complete steps, merge, reads, dry-run, source, and idempotency; replies retain canonical receipts, records, dependencies, bindings/effects, undo/history/actor, preview `would_status`/null receipt, and conflict/invalid details.

No product, test, schema, client, pin, evidence, or design files changed. No pytest, host, full, browser, probe, or AST re-audit was run. Worktree remains clean. Existing map0554 and map0603 remain immutable historical reports with their mistaken headers.

Recommended next step: author0605 adds the required `media.admit` fixture mapping, then perform the single permitted count delta.