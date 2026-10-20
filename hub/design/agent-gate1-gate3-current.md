# Agent Gate 1 / Gate 3 current proof track

Date: 2026-10-20
Base: current Agent `tl/integration` (`a8a40afd3` before the worker snapshot)
Qualification cohort: current Agent snapshot with Runtime `/home/user/work/runtime`, public Composition 0.0.13 Remotion tree `/home/user/work/runtimes/agent-remotion-0013`, and the central child environment `/home/user/work/venv-agent-child-s2`.

## Suites and results

The two allow-list entries were added to `scratchpad/orch/tests/suites.conf`:

- `agent gate1-current-integration`
- `agent gate3-agent-current-integration`

Both were requested once through the central test service, after the final suite edits. No full suite was requested.

| Suite | Central result | Test-service result |
|---|---:|---|
| `gate1-current-integration` | 83 passed, 127 deselected, 19.88s | PASS, exit 0; run `agt-m2-gate13-current-proof-track-gate1-current-integration-1020212417-23926` |
| `gate3-agent-current-integration` | 26 passed, 8.69s | PASS, exit 0; run `agt-m2-gate13-current-proof-track-gate3-agent-current-integration-1020212417-13895` |

Logs:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-gate13-current-proof-track-gate1-current-integration-1020212417-23926/log.txt`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-gate13-current-proof-track-gate3-agent-current-integration-1020212417-13895/log.txt`

The exact environment and pytest commands are the two named lines in `suites.conf`; both disable pytest cache writes and use the current Runtime checkout/public 0.0.13 paths.

## Gate 1 inventory

Existing tests selected, without modifying assertions:

- CLI/Python/sheet cross-front-end runner: `tests/editing_conformance/test_conformance.py -k timing` (the timing scenarios exercise each declared front end and the runner's exact after/undo/redo comparisons).
- Opaque and explicit clear preservation: `test_recipe_m2_clip_add.py::{test_literal_seconds_and_opaque_json_exact_reload_inverse_redo,test_canonical_schema_closes_the_operation_and_preserves_opaque_row_fields}`, `test_recipe_m2_placement.py::{test_preserves_raw_identity_source_media_order_opaque_and_sibling,test_absence_null_and_relation_clears_roundtrip}`, `test_recipe_text_binding_spike.py::{test_empty_text_is_present_zero_byte_and_distinct_from_clear_and_absent,test_clear_of_absent_binding_is_refused_not_a_silent_noop}`, `test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`, `test_timing_compiler.py::test_explicit_clears_empty_formulas_and_opaque_maps_survive`, and the native sheet clear matrix.
- Occurrence identity/isolation and source metadata: `test_recipe_occurrence_media.py::{test_provider_exact_reload_inverse_redo_and_retired_asset_reservation,test_noninteger_positive_speed_preserves_source_units_and_half_open_boundary}`, `test_recipe_occurrence_delete.py::{test_delete_reload_exact_guarded_inverse_redo_order_and_metadata,test_explicit_single_occurrence_identity_only,test_exact_opaque_and_tagged_metadata_survive_last_consumer_history_inverse}`, and `test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo`.
- Transcript/source binding identity and replay: `test_recipe_text_binding_spike.py::{test_set_round_trip_records_exact_identity_and_dependency,test_inverse_restores_absence_and_redo_restores_exact_row}`, `test_word_binding_recipe.py::{test_undo_recovers_before_binding_even_when_text_writes_are_equal,test_phrase_records_all_consecutive_main_word_ids,test_same_word_in_reused_cas_clips_retains_raw_source_through_undo}`, and `test_timing_retained_inputs.py::test_retained_v1_and_explicit_v2_keep_window_and_raw_source_identity`.
- Rational fps, half-open boundaries, and deterministic compiler behavior: `test_word_binding_recipe.py::{test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance,test_typed_second_offset_preserves_main_precision_at_rational_frame_boundary}` plus `test_timing_compiler.py::{test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears,test_fixed_source_window_and_rational_half_frame_ties,test_after_word_end_at_source_out_is_included_and_onset_at_source_out_is_refused,test_rational_fps_anchor_and_exact_frame_offset,test_compilation_has_no_io_random_clock_renderer_or_mutable_checkout_dependency}`.
- Sheet-native retry/inverse path: `test_timeline_sheet_native.py::{test_label_clear_is_distinct_from_empty_and_literal_clear,test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases}`.

The suite's 83 passes cover the requested semantic cases. The first local selector probe had one typo in an ad hoc node id; it was corrected before central submission. No product or assertion change was made.

## Gate 3 inventory

Existing tests selected:

- Renderer-independent save fences: all tests in `tests/sdk/test_scene_save_core.py`; they block renderer/scene imports, process launches, and diagnostics while exercising save, publish, transaction, dry-run, reload, and undo.
- Real provider reload/inverse without renderer: `tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer` and `::test_restore_undo_redo_exact_full_closure_and_unknown_fields`.
- Runtime restart/retry/inverse: `tests/sdk/test_timeline_commit_provider_runtime.py::{test_structural_reservations_and_receipt_retry_survive_runtime_restart,test_restore_inverse_redo_and_exact_retry_survive_runtime_restart}`.
- Working-copy restart persistence: `tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`.
- Honest preview/unavailability reporting: `tests/packs/timeline/test_visualize_drafts.py::{test_visualize_summary_uses_rendered_snapshot_label_for_candidate_and_unavailable,test_render_draft_without_checkout_fails_before_rendering}`, `tests/sdk/test_project_render_rrp.py::test_missing_publication_association_is_an_explicit_dependency_failure`, and `tests/sdk/test_workspace_client_timeline_commit.py::{test_workspace_client_commit_preserves_preview_null_receipt,test_workspace_client_absent_commit_method_is_actionable}`.

## Uncovered or not claimed

- Gate 1 is bounded; the full editing-conformance corpus was intentionally not run. Non-timing CLI/Python/sheet scenarios, including the broader structure/look/audio set, remain outside this result. The focused occurrence/source/transcript checks are recipe/provider tests rather than a new three-front-end scenario for every one of those data shapes.
- Gate 3 proves renderer independence with import/process fences and provider restart/reload tests. It does not prove a live browser, a real Composition frame, a physical preview artifact, or a stopped external renderer process behind the Runtime door.
- No full suite, localhost/browser/live-socket journey, or cross-product App journey was run. Runtime restart cases are the existing bounded provider/runtime fixtures, not a new full Runtime-door qualification.
