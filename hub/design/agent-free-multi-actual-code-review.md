# APPROVE SOURCE FOR PEER ACK — Agent free-multi ABA / rational-FPS codefix

Reviewed actual codefix commit `a19192ea789a209260da46bfbdd5b616fc7cc4ac`
(`fix(timeline): preserve forward move-set guards and rational fps`) against
base `922317bd58aa4db8f7cced85b37dd96038ae17df`, using the settled plan and
the prior source-contract review. The six-file diff is scoped to rebase,
rational-FPS parsing, and focused regressions; no repository files were
changed by this review.

## Findings

- `rebase.py:12-28` restores the forward identity-only history path for
  move-set plans, then adds a second strict history check for move-set
  membership/order, source, structure, activity, and identity reads. Ordinary
  clip values remain verified against the final head by the original command
  claims. The plan, commands, records, and claims are not refreshed or
  mutated.
- A genuine equal-final-value/identity ABA using the captured input as the
  head is accepted and reproduces the original bundle/records. The prior
  literal probe that used `head = deepcopy(plan.bundle)` is an already-applied
  head, not an equal-state rebase head; it correctly refuses with
  `identity_collision` because the created track is occupied. This is not a
  product failure.
- Inverse/later-intent history remains strict (`intervening_write`), while
  changed membership, source reads/dependencies, lane/clip identity, ordering,
  activity, and created identities remain guarded. The old incorrect forward
  `read-aba` refusal was converted one-for-one to an equal-state success;
  `test_forward_changed_membership_refuses_atomically` supplies the genuine
  changed-state negative. No assertions were skipped, deleted, or weakened.
- `units._rational_fps` accepts both Main spellings (mapping and two-item list),
  preserves the positive-integer policy, and is reused by capture and timing
  evaluation. Move-set quantization still uses the existing common frame grid;
  no default or clamp was added. Mapping and list forms produce identical
  rows, writes, dependencies, bindings, selections, and created IDs.
- Schema and floors are unchanged: the floor serialization hash remains
  `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`, with
  60 definitions, 34 clauses, and 12 v2 clauses. Removing move-set still
  reconstructs the `84fc0863...` floor.

## Tests and checks

All commands ran from the assigned worktree with shared dependencies read-only.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py tests/sdk/test_timing_compiler.py
138 passed in 16.56s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py::test_full_move_set_schema_is_a_new_source_descendant_of_the_84fc_floor tests/sdk/test_timeline_materialization_schema_union.py::test_private_extent_proposal_is_one_addition_on_voiceover_floor tests/sdk/test_timeline_materialization_schema_union.py::test_removing_group_and_project_data_additions_reconstructs_private_carrier_bytes tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden tests/editing_conformance/test_pristine_initialize.py::test_complete_s2_schema_is_retained_additively tests/editing_conformance/test_materialization_map.py::test_product_capture_json_recovery_and_exact_source_pin_across_stale_heads tests/editing_conformance/test_materialization_map.py::test_source_bound_batch_preserves_earlier_stages_and_strict_inverse_guards tests/editing_conformance/test_materialization_version_boundary.py::test_source_bound_v2_cannot_use_an_unverified_legacy_bundle tests/editing_conformance/test_materialization_version_boundary.py::test_complete_public_s2_v1_keeps_original_capture_records_output_and_map
13 passed in 1.21s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec tests/editing_conformance/test_recipe_m1_commands.py::test_replay_permits_disjoint_and_equal_state_while_inverse_guards_aba tests/editing_conformance/test_recipe_m1_commands.py::test_disjoint_same_child_rebase_and_original_guards_after_materialization tests/editing_conformance/test_recipe_m1_commands.py::test_semantic_owner_refuses_actual_source_change_and_inverse_source_aba tests/editing_conformance/test_recipe_m1_commands.py::test_collection_selection_detects_structural_publications_even_when_json_returns tests/editing_conformance/test_recipe_m1_commands.py::test_member_and_container_aliases_share_overlap_for_replay_and_inverse tests/editing_conformance/test_recipe_m1_commands.py::test_staged_inverse_keeps_opaque_strings_and_refuses_all_unchanged_overlap tests/editing_conformance/test_recipe_m1_commands.py::test_overlapping_read_is_verified_at_input_and_bad_late_stage_is_atomic
14 passed in 1.16s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/rebase.py astrid/sdk/timeline/capture.py astrid/sdk/timeline/units.py astrid/sdk/timeline/_timing_evaluators.py && git diff --check
All checks passed; diff check passed.
```

The three targeted invocations total 165 passing tests. No full, Runtime,
generation, pin/freeze, browser, live-socket, or integration suite was run, as
required by the brief. No blocking finding remains. Recommended next step is
peer acknowledgement and harness commit; broader qualification remains a
separate task.
