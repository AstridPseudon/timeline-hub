# Agent full12 classification — 2026-10-20

## Result and comparison

Target: `agent-full-remotion12-integration-1020093757-4565`, snapshot commit
`5c3f0c9905d79247f0fa4528c0777908e9ccaa18` (tree
`36773419020503ba8c69672277e2d851a48e8a73`). The central result was **13
failed, 58 errors, 13,390 passed, 453 skipped, 18 xfailed**.

The exact short-summary set contains 71 nodes. Compared with the supported-env
109-node baseline in `agent-baseline-109-cutlist.md`:

| comparison | nodes |
|---|---:|
| exact target set | 71 |
| target ∩ 109-node baseline | 23 |
| target-only | 48 |
| baseline-only | 86 |

This is not a 71-node baseline. The prior supported-env full
`agent-full-remotion-integration-1020031037-28578` had the exact 109-node set
(79 failed/30 errors), as did the recorded f6 comparison. The older normal-env
fulls are not interchangeable with this pinned Remotion-12 run.

## Classification

### Baseline/environment — 23 exact baseline nodes

These are the baseline cutlist's environment groups G, H, and M; no later
product change is inferred.

**H — installed Astrid missing (7):**

- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_revision]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_content]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[revision_drift]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[content_drift]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[checkout_drift]`
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[profile_hash_drift]`

The target traceback is `python -I` with `PYTHONPATH` removed, followed by
`ModuleNotFoundError: No module named 'astrid'`. This is the same root and same
nodes as the 109-node normal/supported comparisons. The test is intentionally
checking an installed profile, so do not weaken it.

**G — owned-host child environment, provisional (1):**

- `tests/packs/runpod/test_worker_process.py::test_linux_owned_host_survives_launcher_and_exact_stop`

The target reaches `WorkerOwnerConflict: host did not acquire physical pod
ownership`. `worker_process.py:529-534` starts the child with the same Python
executable, no `PYTHONPATH`, and discards stderr; therefore the cutlist's
missing-installed-Astrid explanation remains the best environment diagnosis,
but the discarded child stderr leaves this one provisional rather than proved.

**M — missing VibeComfy sibling checkout (15):**

- `tests/packs/runpod/test_worker_staging.py::test_preparation_runs_real_child_probe_and_reuses_verified_content`
- `tests/packs/runpod/test_worker_staging.py::test_materialized_h3_bundle_stages_as_an_owned_workflow_root`
- `tests/packs/runpod/test_worker_staging.py::test_interrupted_upload_reconciles_remote_bytes_without_reupload`
- `tests/packs/runpod/test_worker_staging.py::test_remote_drift_fails_closed_then_explicit_refresh_repairs_owned_source`
- `tests/packs/runpod/test_worker_staging.py::test_workflow_pack_requires_its_unique_lock_pin_and_exact_checkout`
- `tests/packs/runpod/test_worker_staging.py::test_manifest_pinned_workflow_pack_cannot_omit_its_checkout_root`
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_leaf]`
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_parent]`
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_leaf]`
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_parent]`
- `tests/packs/runpod/test_worker_staging.py::test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse`
- `tests/packs/runpod/test_worker_staging.py::test_empty_remote_observation_and_model_shadow_remain_unresolved`
- `tests/packs/runpod/test_worker_staging.py::test_release_manifest_datacenter_and_account_reference_are_mandatory`
- `tests/packs/runpod/test_worker_staging.py::test_manifest_volume_alias_is_optional_but_mismatch_and_effective_path_drift_fail_closed`
- `tests/packs/runpod/test_worker_staging.py::test_json_selection_uses_production_composition_and_real_cpu_staging`

The target trace is `FileNotFoundError: /home/vibecomfy/vibecomfy`. The fixture
derives that path at `test_worker_staging.py:39` and copies it at `:86`.

### Baseline/environment — target-only renderer setup root (43)

These are not in the 109-node baseline because the renderer-native cohort was
not part of that earlier failure set. They share one setup cause, not 43
independent source failures:

- 9 nodes in `tests/packs/rendering/test_capture_scene_labels.py` (all nine target `ERROR` nodes).
- 15 nodes in `tests/packs/rendering/test_scene_host.py` (all 15 target `ERROR` nodes).
- 19 nodes in `tests/packs/rendering/test_scene_source_carry.py` (all 19 target `ERROR` nodes; the `native` parametrizations consume the failed native fixture).

The trace roots are `missing provisioned peer: .../remotion/node_modules/react`
from `test_capture_scene_labels.py:48`, and `requires provisioned renderer
peers` from `test_scene_host.py:39`. The source-carry native fixture aliases
the same capture-label host, so its 19 errors are downstream of that root.

Evidence: the target full command did not set `ASTRID_TEST_NODE_MODULES`; the
central runner's Agent snapshot setup only links `remotion/node_modules` when
`/home/user/work/agent/remotion/node_modules` exists (`orch/bin/test-run:40-42`).
That path is absent. The pinned runtime actually exists at
`/home/user/work/runtimes/agent-remotion-0012/node_modules` and contains all
six required peers (`react`, `react-dom`, `remotion`, `@remotion/media`,
`@remotion/layout-utils`, `esbuild`). This is a test-service dependency
provisioning failure; no renderer behavior should be classified from these
43 setup errors.

### Already fixed later — 2

- `tests/sdk/test_timeline_occurrence_delete_provider.py::test_provider_equal_state_and_aba_child_publications_refuse_stale_delete[False]`
- `tests/sdk/test_timeline_occurrence_delete_provider.py::test_provider_equal_state_and_aba_child_publications_refuse_stale_delete[True]`

The target uses the old `refuse_stale_delete` expectation and fails with
`DID NOT RAISE CommitRejected`. Integrated commit `6e2ce05c` changes this
exact test to `accept_stale_delete` and asserts the rebased canonical result,
including the A→B→A case. This is a settled equal-state delete policy change,
not a remaining target-tree product regression.

### New source/contract issues needing a narrow fix — 3

**Runtime text-selection strict-xfail is stale (1):**

- `tests/editing_conformance/test_recipe_text_binding_spike.py::test_runtime_port_declares_exact_text_selection`

The target report explicitly says `XPASS(strict)`, not an implementation
failure. Runtime commit `b981ce6` (present in the Runtime integration checkout)
added `RuntimeCommitPort.text_selection` and `RequestCommitPort.text_selection`;
the target test still carries the strict xfail at `test_recipe_text_binding_spike.py:322-325`.
Agent follow-up `cb1e907c` updates this check to an integration test using
`tests.helpers.runtime.use_runtime`, but that commit is not an ancestor of the
current Agent integration head. Land/review that narrow follow-up; do not
restore the xfail or weaken the Runtime behavior.

**Checked-in TypeScript catalog is stale (1):**

- `tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current`

The target traceback says `catalog.ts is stale; run scripts/gen_element_catalog.py`.
Generating in the worker without writing product files changes only the
`am-presenter` descriptor revision from
`sha256:f1eb6f33000a3cdbea322048da7bea24094f47ff578582b86183535b7ecda57e`
to `sha256:72048692b1229384e8ace7ec52fd3a631cf9cc103ee022b3a025059c64ba996f`.
This is a real checked-in projection mismatch, not an environment setup error.

**Bare environment string in core (1):**

- `tests/test_env_vars_conformance.py::TestNoBareStringAccess::test_no_catalogued_bare_strings_in_core`

The target traceback identifies `astrid/core/timeline/scene_answers.py:70`,
where `os.environ["ASTRID_PACKS_PATH"]` uses a literal instead of the
catalogued `ASTRID_PACKS_PATH` constant. This remains unchanged after the
target snapshot and needs the minimal import/constant substitution.

### Unknown

None. The 71 nodes have either an exact prior-baseline match, a shared setup
trace, an actual later integrated diff, or a directly reproducible source/
contract mismatch.

## Exact target-only node inventory

The 43 renderer setup nodes are enumerated by their complete file-level groups
above. The remaining target-only nodes are:

Exact renderer setup node IDs (all classified to the one missing-peer root):

- `tests/packs/rendering/test_capture_scene_labels.py::test_real_host_labels_are_retained_once_and_drawn_without_private_math`
- `tests/packs/rendering/test_capture_scene_labels.py::test_mixed_or_missing_capture_cannot_retain_facts`
- `tests/packs/rendering/test_capture_scene_labels.py::test_other_source_or_uncaptured_frame_never_falls_back`
- `tests/packs/rendering/test_capture_scene_labels.py::test_unknown_public_geometry_is_an_answer_and_unavailability_is_not_empty`
- `tests/packs/rendering/test_capture_scene_labels.py::test_real_media_bounds_use_public_canvas_and_keep_uncertain_alpha`
- `tests/packs/rendering/test_capture_scene_labels.py::test_mismatched_public_response_is_not_relabelled[frame]`
- `tests/packs/rendering/test_capture_scene_labels.py::test_mismatched_public_response_is_not_relabelled[width]`
- `tests/packs/rendering/test_capture_scene_labels.py::test_mismatched_public_response_is_not_relabelled[height]`
- `tests/packs/rendering/test_capture_scene_labels.py::test_mismatched_public_response_is_not_relabelled[clipId]`
- `tests/packs/rendering/test_scene_host.py::test_native_host_default_custom_alias_capability_and_immutable_props`
- `tests/packs/rendering/test_scene_host.py::test_native_host_uses_exact_assets_and_runtime_theme`
- `tests/packs/rendering/test_scene_host.py::test_native_host_resolves_custom_transition_defaults_and_boundaries[start]`
- `tests/packs/rendering/test_scene_host.py::test_native_host_resolves_custom_transition_defaults_and_boundaries[center]`
- `tests/packs/rendering/test_scene_host.py::test_native_host_resolves_custom_transition_defaults_and_boundaries[end]`
- `tests/packs/rendering/test_scene_host.py::test_large_native_batch_is_not_truncated`
- `tests/packs/rendering/test_scene_host.py::test_native_host_rational_frame_clock_is_half_open`
- `tests/packs/rendering/test_scene_host.py::test_native_host_preserves_root_painter_order_and_current_roles`
- `tests/packs/rendering/test_scene_host.py::test_native_host_passes_public12_compiled_transitions_unchanged`
- `tests/packs/rendering/test_scene_host.py::test_missing_host_input_is_unavailable_not_an_empty_scene[theme]`
- `tests/packs/rendering/test_scene_host.py::test_missing_host_input_is_unavailable_not_an_empty_scene[assets]`
- `tests/packs/rendering/test_scene_host.py::test_missing_host_input_is_unavailable_not_an_empty_scene[tracks]`
- `tests/packs/rendering/test_scene_host.py::test_source_metadata_does_not_supply_missing_host_inputs`
- `tests/packs/rendering/test_scene_host.py::test_declared_background_has_known_empty_content`
- `tests/packs/rendering/test_scene_host.py::test_unknown_animation_diagnostics_and_root_tail_are_preserved`
- `tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[native-text-card]`
- `tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[native-text]`
- `tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[native-am-snap-plate]`
- `tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[native-image]`
- `tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[native-frame-overlay]`
- `tests/packs/rendering/test_scene_source_carry.py::test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames[native]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-capture]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-missing]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-copy]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-query]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-frames]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-no_callback]`
- `tests/packs/rendering/test_scene_source_carry.py::test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files[native-extra]`
- `tests/packs/rendering/test_scene_source_carry.py::test_canonical_basis_uses_whole_partial_canvas_and_rational_rate[native]`
- `tests/packs/rendering/test_scene_source_carry.py::test_candidate_retains_real_compiled_candidate_and_base_label[native]`
- `tests/packs/rendering/test_scene_source_carry.py::test_execute_handoff_uses_actual_provider_and_public_labels_in_exported_pack[native]`
- `tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[native-text-card]`
- `tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[native-image]`
- `tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[native-frame-overlay]`

- `tests/editing_conformance/test_recipe_text_binding_spike.py::test_runtime_port_declares_exact_text_selection`
- `tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current`
- `tests/test_env_vars_conformance.py::TestNoBareStringAccess::test_no_catalogued_bare_strings_in_core`
- `tests/sdk/test_timeline_occurrence_delete_provider.py::test_provider_equal_state_and_aba_child_publications_refuse_stale_delete[False]`
- `tests/sdk/test_timeline_occurrence_delete_provider.py::test_provider_equal_state_and_aba_child_publications_refuse_stale_delete[True]`

## Recommended next narrow work

1. Fix the central Agent test setup to expose the pinned 0012 peer graph via
   `ASTRID_TEST_NODE_MODULES` (or an equivalent private snapshot link), then
   rerun only the 43 renderer files as a named targeted cohort.
2. Provision the supported installed-Astrid profile and the VibeComfy sibling
   fixture/override for the 8 G/H/M environment nodes; keep their behavior
   assertions live.
3. Land/review the text-selection Agent integration follow-up, regenerate the
   checked-in catalog, and replace the bare env literal with the env constant.
4. Treat `6e2ce05c` as already handled; no new delete patch is indicated by
   this result.

No full suite was requested by this worker.
