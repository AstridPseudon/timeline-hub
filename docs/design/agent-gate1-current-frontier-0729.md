# Agent Gate1/Gate3 current frontier (PLAN6)

Date: 2026-10-21 UTC  
Scope: bounded Agent evidence inventory and source-owned M2 follow-up.  
Current Agent source: `ac9a9357921eb8af0cedffa241f8c4416865f0e1`, tree
`7a5c6e5c4a5f650049f8aa76758c5347ef69459f`.  
Current Runtime checkout observed by the manager: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`.

## Frontier verdict

This is a bounded Gate1/Gate3 evidence map, not a complete-foundation claim.
The current Agent source has broad CLI/Python/NativeSheet conformance evidence
and the renderer-independent save evidence below, but the evidence is spread
across older current snapshots, staged candidates, and alternate Runtime
cohorts. It must not be relabelled as one all-current pass.

The highest-priority current source gap is the document-diff presence plane.
The merged stopgap `a362c7fd`/`ac9a93579` closes some row-presence losses, but
the manager's current review still finds parent/config/registry/container and
mirror-deletion cases that can return zero commands. The exact diagnosis and
independent reviews are `design/agent-document-presence-complete-cause.md`,
`design/agent-document-diff-presence-track-safety-review.md`, and
`design/agent-document-diff-second-presence-safety-review.md`; the deletion
ledger records this as `AG-DOC-PRESENCE`, IN PROGRESS.

The other current-head boundary is transcript/source binding: the existing
fresh three-frontend transcript test is not present in this `ac9a93579` source
tree. Its successful candidate runs remain staged evidence, not current-head
evidence. The retained-transcript read also has a normal-95bd public-boundary
mismatch; its one passing result uses the explicitly compatible Runtime
successor `3dcae183`.

## Behavior-to-selector map

The selectors below are existing tests. A result is only claimed where the
source tree, Runtime identity, and central result are stated in the evidence
row; collection or source inspection is not a pass.

| Required behavior | Current selectors | Frontier status |
|---|---|---|
| Opaque values and literal seconds survive add/reload/inverse/redo | `tests/editing_conformance/test_recipe_m2_clip_add.py::test_literal_seconds_and_opaque_json_exact_reload_inverse_redo`; `::test_canonical_schema_closes_the_operation_and_preserves_opaque_row_fields`; `tests/editing_conformance/test_recipe_m2_placement.py::test_preserves_raw_identity_source_media_order_opaque_and_sibling`; `tests/editing_conformance/test_conformance.py` IDs `look.clear.plate-asset-opaque-{cli,python,sheet}` | Covered by the Gate1 conformance slice and the non-timing slice. The current frontier still does not claim a full corpus. |
| Explicit null, empty, clear, and absent are distinct | `tests/editing_conformance/test_recipe_m2_placement.py::test_absence_null_and_relation_clears_roundtrip`; `tests/editing_conformance/test_recipe_text_binding_spike.py::test_empty_text_is_present_zero_byte_and_distinct_from_clear_and_absent`; `::test_clear_of_absent_binding_is_refused_not_a_silent_noop`; `tests/editing_conformance/test_recipe_text_binding_native.py::test_empty_clear_and_original_noncanonical_order`; `::test_absent_collection_is_restored_exactly`; `tests/sdk/test_timing_compiler.py::test_explicit_clears_empty_formulas_and_opaque_maps_survive` | Pure/native recipe evidence is present. Document-view presence is not closed: the current adapter must refuse or encode every added/deleted/null field atomically. |
| Presence changes cannot disappear as zero-command success | `tests/timeline/test_authoring_feedback.py::test_document_view_adapter_refuses_matched_row_presence_changes` (seven parametrized row families); `::test_document_view_adapter_refuses_presence_loss_masked_by_a_valid_move` | Existing row tests are present in `ac9a93579`; only collection was checked in this task. Remaining parent/config/registry/container/mirror gaps are documented diagnosis, not a pass. |
| Occurrence isolation and shared-source retention | `tests/editing_conformance/test_recipe_occurrence_media.py::test_provider_exact_reload_inverse_redo_and_retired_asset_reservation`; `tests/editing_conformance/test_recipe_occurrence_delete.py::test_explicit_single_occurrence_identity_only`; `::test_exact_opaque_and_tagged_metadata_survive_last_consumer_history_inverse`; `tests/editing_conformance/test_conformance.py` IDs `timing.occurrence.source-isolation-{cli,python,sheet}`; connected selector `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends` | Staged connected proof: 4 passed on Agent tree `fe6f0f1558da7a2dabdeb50b7394fd70b2e6ab3d`, Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, result `agt-m2-gate1-connected-occurrence-source-gate1-connected-occurrence-source-main95bd-1021002529-87`. Latest current-head `ac9a93579` has not been requalified by that result; do not rerun this passed HTTP evidence in this task. |
| Transcript/source binding identity, source retention, inverse/redo | Pure selectors: `tests/editing_conformance/test_recipe_text_binding_spike.py::test_set_round_trip_records_exact_identity_and_dependency`, `::test_inverse_restores_absence_and_redo_restores_exact_row`; `tests/editing_conformance/test_word_binding_recipe.py::test_phrase_records_all_consecutive_main_word_ids`, `::test_same_word_in_reused_cas_clips_retains_raw_source_through_undo`, `::test_last_write_clear_undo_restore_and_restore_inverse`; retained-input selector `tests/editing_conformance/test_timing_retained_inputs.py::test_retained_v1_and_explicit_v2_keep_window_and_raw_source_identity` | Pure/retained recipe evidence exists. The current tree has no `test_gate1_fresh_word_transcript_frontends.py`; the staged candidate's fresh test passed Python only (`1 passed, 2 xfailed`) before the carrier fix, then passed all three frontends on candidate tree `2000b0bc2a05928bda54d4869fc06f03a8ca85de` (`3 passed`, result `agt-m2-gate1-anchor-native-frontends-fix-gate1-fresh-word-transcript-frontends-1021020618-14833`) with Runtime `3dcae1836a609363135d07ee435ce9beea975504`. This is not current normal-cohort proof. |
| Rational fps and exact frame boundaries | `tests/editing_conformance/test_word_binding_recipe.py::test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance`; `::test_typed_second_offset_preserves_main_precision_at_rational_frame_boundary`; `tests/sdk/test_timing_compiler.py::test_rational_fps_anchor_and_exact_frame_offset`; connected selector `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends`; direct CLI/sheet selector `tests/packs/timeline/test_cli_native_sheet.py::test_rational_explicit_occurrence_move_is_lossless_across_native_frontends` | Connected staged result: 3 passed on Agent tree `daa420916ad5138e3899cdcf78b6fd1e98ac350c`, result `agt-m2-gate1-rational-connected-timing-gate1-rational-connected-timing-1020234021-15851`. The current source contains the selector but this result is not an `ac9a93579` qualification. |
| Half-open intervals and source-window timing | `tests/editing_conformance/test_recipe_occurrence_media.py::test_noninteger_positive_speed_preserves_source_units_and_half_open_boundary`; `tests/sdk/test_timing_compiler.py::test_after_word_end_at_source_out_is_included_and_onset_at_source_out_is_refused`; `::test_fixed_source_window_and_rational_half_frame_ties`; `tests/editing_conformance/test_word_binding_recipe.py::test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance` | Included in the bounded Gate1 timing slice (83-pass result below). No full timing corpus or new HTTP replay is claimed. |
| Deterministic timing without I/O/clock/renderer | `tests/sdk/test_timing_compiler.py::test_compilation_has_no_io_random_clock_renderer_or_mutable_checkout_dependency`; `::test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears` | Included in the bounded Gate1 timing slice. |
| Exact inverse/redo, guarded rebase, and ABA safety | `tests/editing_conformance/test_recipe_occurrence_delete.py::test_delete_reload_exact_guarded_inverse_redo_order_and_metadata`; `tests/editing_conformance/test_recipe_text_binding_spike.py::test_inverse_restores_absence_and_redo_restores_exact_row`; `tests/sdk/test_timeline_sheet_native.py::test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases`; `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo`; `::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba` | Covered by the bounded Gate1/Gate3 slices and published014/WC6 evidence. Current document presence remains the only known lossless adapter hole; do not infer inverse safety for unrepresented fields. |
| CLI/Python/sheet scenario coverage | `tests/editing_conformance/test_conformance.py::test_conformance[...]` for every selected scenario/path; current named `agent gate1-nontiming-current-integration` uses `-k 'audio or code or look or structure'`; current named `agent gate1-current-integration` uses the explicit timing/recipe/compiler selectors recorded in `tests/suites.conf` | Nontiming result: 130 passed, 24 deselected, coverage `(44 scenarios, 130 nodes, 44 CLI, 43 Python, 43 sheet)` on Agent tree `e159563aa4cb0310ef96380ed85ff88402f96c8a`, result `agt-m2-gate1-nontiming-current-proof-gate1-nontiming-current-integration-1020221836-8218`. Timing/recipe result: 83 passed, 127 deselected on tree `b614c4d7036ad8b93517969fc595e9f43c9f8ff4`, result `agt-m2-gate13-current-proof-track-gate1-current-integration-1020212417-23926`. These are bounded snapshots, not current `ac9a93579`. |

## Gate3 evidence boundary

The renderer-independent save proof is retained and deliberately not rerun:

- Existing named `gate3-agent-current-integration`: 26 passed on Agent tree
  `b614c4d7036ad8b93517969fc595e9f43c9f8ff4`, result
  `agt-m2-gate13-current-proof-track-gate3-agent-current-integration-1020212417-13895`.
  It covers `tests/sdk/test_scene_save_core.py`, provider reload/inverse,
  Runtime restart/retry, working-copy restart persistence, honest preview
  unavailability, and related workspace-client refusal selectors.
- Existing named `main95bd-real-fixture-qualification`: 11 passed on Agent
  tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`, Runtime
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`), C13/public Composition 0.0.13
  profile, result
  `agt-m2-gate13-published014-current-proof-main95bd-real-fixture-qualification-1021031102-23927`.
  This is the published014 renderer-off/door cohort and is retained evidence.
- The current document proof owned by worker 0727 had a snapshot identity
  failure before pytest: original Agent `e51732a644f632830a06499807b4d98a4a7bc163`,
  tree `f157ce2451296d8de1ba59a8567a46f4e112bd75`; synthetic snapshot commit
  `9bcacb83ef7e65c2af72c33790f8a4d0bf15ddb8`, same tree; Runtime `b92d3e7a`.
  The bad guard compared `HEAD` to the original commit instead of comparing
  `HEAD^` and the exact tree. No pytest, HTTP acceptance, reload, inverse, or
  renderer assertion ran. That worker owns the corrected one-node proof; this
  page does not rerun or replace it.

Gate3 does not prove a live browser, physical Composition render, external
renderer process, or full cross-product journey. Those remain outside this
bounded track.

## Existing named commands and remaining work

No new suite name is needed. The existing commands are the only proposed
follow-up lanes:

1. **Document presence, source-owned first.** Complete the existing
   `document_diff.py` partition repair for parent/config/registry/container
   presence, config-mirror key deletion, and mixed supported-edit plus
   unsupported-presence atomic refusal. Preserve the positive hold/params/
   label clear tests. Run the local adapter neighbors first with
   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py -k document_view_adapter`.
   Only after repair/review should the already named
   `agent document-diff-null-track-http-integration` command be considered;
   the prior HTTP attempt failed during fixture seeding (`destination_occupied`)
   on Agent tree `20b3093d…`, and the 0721 approved proof stopped before
   pytest on its identity guard. Neither is a pass.
2. **Transcript/source current cohort.** Restore or port the existing fresh
   transcript scenario and its exact CLI/Python/NativeSheet carrier assertions
   onto the current source. Then use the existing named
   `agent gate1-fresh-word-transcript-frontends` command. It must have no
   strict xfail for the three frontend paths, and the normal Runtime boundary
   must expose the exact retained transcript pin; the alternate `3dcae183`
   result remains separate evidence.
3. **Current-head semantic requalification when authorized.** The exact
   existing commands are `agent gate1-rational-connected-timing`,
   `agent gate1-connected-occurrence-source-main95bd`, and
   `agent gate1-current-integration`. Their selectors are already present and
   collected in the current source. Do not replay the already passed HTTP,
   renderer-off, retained-sheet, WC1, or private/native-body evidence merely
   to relabel it. Requalification is needed only after a relevant source
   change or when the orchestrator explicitly schedules the current-head lane.

This is the minimum source-owned M2 work visible from the current frontier:
close the complete document-presence partition, land the current normal-cohort
transcript carrier/read proof, and preserve the existing CLI/Python/sheet
selectors. No product source, lock, marker, or assertion change is part of
this document update.

## Collection check performed for this update

The proposed missing selectors were collected only; no selected test body was
executed. The corrected command was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest --collect-only -q \
  -p no:cacheprovider \
  tests/timeline/test_authoring_feedback.py::test_document_view_adapter_refuses_matched_row_presence_changes \
  tests/timeline/test_authoring_feedback.py::test_document_view_adapter_refuses_presence_loss_masked_by_a_valid_move \
  tests/editing_conformance/test_recipe_text_binding_native.py::test_exact_capture_inverse_and_same_value_write \
  tests/editing_conformance/test_recipe_text_binding_native.py::test_empty_clear_and_original_noncanonical_order \
  tests/editing_conformance/test_recipe_text_binding_native.py::test_absent_collection_is_restored_exactly \
  'tests/editing_conformance/test_conformance.py::test_conformance[timing.occurrence.source-isolation-cli]' \
  'tests/editing_conformance/test_conformance.py::test_conformance[timing.occurrence.source-isolation-python]' \
  'tests/editing_conformance/test_conformance.py::test_conformance[timing.occurrence.source-isolation-sheet]' \
  tests/editing_conformance/test_word_binding_recipe.py::test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance \
  tests/editing_conformance/test_word_binding_recipe.py::test_typed_second_offset_preserves_main_precision_at_rational_frame_boundary \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_noninteger_positive_speed_preserves_source_units_and_half_open_boundary \
  tests/sdk/test_timing_compiler.py::test_after_word_end_at_source_out_is_included_and_onset_at_source_out_is_refused \
  tests/sdk/test_timing_compiler.py::test_rational_fps_anchor_and_exact_frame_offset \
  tests/sdk/test_timing_compiler.py::test_compilation_has_no_io_random_clock_renderer_or_mutable_checkout_dependency
```

The first attempt omitted the Runtime checkout and failed at collection with
`ModuleNotFoundError: runtime_protocol`; it executed no tests. The corrected
command collected 18 selected tests (20 total including two deselected
parametrized items) in 1.54s. This collection result is not behavioral
evidence.

