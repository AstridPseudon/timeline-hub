# Agent full compare: M2 stack vs 109-node baseline and integration

Read-only. No repo changes, no full* suite requested, no test run. Sources are the logs and summaries under `$ORCH/tests/`.

## Runs compared

| | Baseline (109) | Integration | M2 stack (Run B) |
|---|---|---|---|
| Run dir | `agent-full-remotion-integration-1020031037-28578` | `agent-full-remotion-integration-1020062923-20811` | `agt-m2-stack-sync-2-full-remotion-integration-1020063510-102` |
| Agent tree | 4a75f68f | `1d140ead` (integration:agent 481e600b) | `0afb198d` (agt-m2-stack-sync-2) |
| Status | not green | fail, exit 1 | fail, exit 1 (`status` = fail, `exit` = 1) |
| Failed | 79 | 81 | 81 |
| Errors | 30 | 30 | 30 |
| Passed | 11732 | 11783 | 12998 |
| Skipped | 453 | 453 | 453 |
| xfailed | not recorded | 16 | 14 |
| Subtests passed | not recorded | 563 | 563 |
| Duration | 2387 s | 3030.79 s | 2413.25 s |
| Unique FAILED+ERROR nodes | 109 | 111 | 111 |

Command (M2, same as integration): `env -i ... ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion ASTRID_NODE_EXECUTABLE=.../node-v20.19.4 ... /home/user/work/venv-agent/bin/python -m pytest -q -n 3` (suite `full-remotion-integration`).

## Set diff (sorted FAILED/ERROR node IDs, `diff` exit codes)

- **M2 vs integration: identical.** `diff` returned exit 0. The M2 stack adds nothing relative to the integration tree.
- **M2 vs baseline:** M2 is a strict superset. Two nodes added, none removed.
  - `+ tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`
  - `+ tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene`
- **FIXED vs baseline: 0.** Every one of the 109 baseline nodes still fails in M2.

## NEW failures caused by the M2 stack: none

The M2 stack adds **0 new failures** relative to integration. Both nodes that are new relative to baseline also fail in the integration run with identical tracebacks, so they are inherited from integration and not from the M2 stack.

| Node (new vs baseline, also in integration) | Trace in M2 log | Cause | Owner (not an M2 stack area) |
|---|---|---|---|
| `test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` | `tests/packs/rendering/test_remotion_render_contract.py:95` (`assertEqual(runtime_package, snapshot_package)`) | `ASTRID_REMOTION_PROJECT_DIR` runtime `/home/user/work/runtimes/agent-remotion/package.json` pins `@banodoco/timeline-composition` at `...-0.0.8.tgz`. Snapshot `remotion/package.json:18` pins `...-0.0.10.tgz`, from `fc6c1f26` (Composition 0.0.10 adoption, per the 0720 compare). The runtime checkout was not moved to the new pin. | Runtime checkout / env pin (Composition adoption), not M2 |
| `test_repo_hygiene.py::test_live_tree_passes_repo_hygiene` | `tests/reshape/test_repo_hygiene.py:227` (`find_unknown_root_entries(tracked) == []`, actual `['design/']`) | A tracked root `design/` dir is not in `ROOT_DIR_ALLOWLIST` (`scripts/reshape/check_repo_hygiene.py`). `design/` is tracked in the M2 tree `0afb198d` (confirmed with `git ls-tree`), from `fd82c36c`, trimmed by `ac1c7db1`, per the 0720 compare. | Docs / hygiene policy, not M2 |

## Full M2 FAILED/ERROR set (111 nodes)

Grouped by the cutlist label (`agent-baseline-109-cutlist.md`). Every node in M2 is also in integration (identical set). `NEW` marks the two nodes that are new relative to baseline. The baseline-109 nodes are in the cutlist group column.

**ERROR (30)**
- `tests/sdk/test_admission_recovery.py` (collection ImportError), group L
- `tests/sdk/test_host_recovery.py` ×14 (group A)
  - `test_busy_live_host_is_deferred_and_untouched`
  - `test_dead_leader_with_surviving_member_is_killed_then_dropped`
  - `test_gone_host_with_empty_group_is_dropped_and_relaunched`
  - `test_host_helper_in_its_own_group_is_not_work`
  - `test_host_whose_validation_does_not_cover_this_caller_is_replaced_not_refused`
  - `test_launcher_attaches_to_healthy_host_from_another_checkout`
  - `test_launcher_replaces_cross_checkout_host_when_resident_is_unhealthy[changed-registration-generation]`
  - `test_launcher_replaces_cross_checkout_host_when_resident_is_unhealthy[changed-resident-source]`
  - `test_launcher_replaces_cross_checkout_host_when_resident_is_unhealthy[unready-registration]`
  - `test_live_host_with_stale_source_is_retired_by_registration_when_idle`
  - `test_live_matching_host_is_reused`
  - `test_pid_reused_by_unrelated_process_is_never_signalled`
  - `test_published_busy_record_decides`
  - `test_spawn_env_excludes_job_lease`
- `tests/packs/runpod/test_worker_staging.py` ×15 (group M)
  - `test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse`
  - `test_empty_remote_observation_and_model_shadow_remain_unresolved`
  - `test_interrupted_upload_reconciles_remote_bytes_without_reupload`
  - `test_json_selection_uses_production_composition_and_real_cpu_staging`
  - `test_manifest_pinned_workflow_pack_cannot_omit_its_checkout_root`
  - `test_manifest_volume_alias_is_optional_but_mismatch_and_effective_path_drift_fail_closed`
  - `test_materialized_h3_bundle_stages_as_an_owned_workflow_root`
  - `test_preparation_runs_real_child_probe_and_reuses_verified_content`
  - `test_release_manifest_datacenter_and_account_reference_are_mandatory`
  - `test_remote_drift_fails_closed_then_explicit_refresh_repairs_owned_source`
  - `test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_leaf|lock_parent|node_leaf|node_parent]` (4)
  - `test_workflow_pack_requires_its_unique_lock_pin_and_exact_checkout`

**FAILED (81)**
- `tests/packs/astrid_motion/test_pixel_shape_geometry.py` ×11, group D
  - `AmPixelShapeGeometryTest` ×4 (`test_arrow_points_right`, `test_dot_three_by_three_is_a_full_square`, `test_ring_is_hollow_and_inside_the_box`, `test_underline_is_bottom_rows_only`)
  - `AmPixelShapeRectTest` ×5 (`test_corners_are_stepped`, `test_radius_is_clamped_and_stroke_thicker_than_half_is_safe`, `test_rounded_tile_has_expected_cell_counts`, `test_shape_rect_returns_the_silhouette`, `test_square_rect_is_the_full_box_and_outline_is_the_border`)
  - `AmPixelShapeBlinkTest` ×2 (`test_blink_hides_for_two_frames_at_each_listed_frame`, `test_single_number_and_missing_blink_at`)
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[...]` ×7, group H (`success`, `missing_revision`, `missing_content`, `revision_drift`, `content_drift`, `checkout_drift`, `profile_hash_drift`)
- `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`, **NEW vs baseline, inherited from integration**
- `tests/packs/runpod/test_ensure_storage.py` ×2 (group E)
  - `test_provision_does_not_auto_create_storage`
  - `test_storage_free_provision_and_session_do_not_probe_or_create_storage`
- `tests/packs/runpod/test_pack_executors.py` ×30 (group E)
  - `test_attached_claim_without_exclusive_authority_refuses_teardown`
  - `test_cost_summation_invariant`
  - `test_datacenter_is_forwarded_only_when_lifecycle_config_supports_it`
  - `test_empty_explicit_cuda_filter_fails_before_launch`
  - `test_exec_nonzero_remote_exit_keeps_artifacts_diagnostics_result_and_cost`
  - `test_exec_reads_handle_and_writes_result`
  - `test_exec_success_copies_only_substrate_returned_artifact_root`
  - `test_launcher_preserves_known_pod_from_nonretryable_launch_failure[provision|session]` (2)
  - `test_outer_adapter_allocation_unknown_keeps_identity_and_blocks_another_launch[provision|session]` (2)
  - `test_pod_handle_builder_keeps_durable_and_transient_shapes_compatible`
  - `test_provision_configured_storage_name_is_recorded_in_canonical_handle`
  - `test_provision_forwards_and_persists_allowed_cuda_versions`
  - `test_provision_named_storage_missing_fails_before_launch_without_creation`
  - `test_provision_persists_allocation_before_readiness_and_marks_cleanup_pending[readiness-failure0|ssh-failure1]` (2)
  - `test_provision_storage_required_fails_before_launch_with_ensure_storage_hint`
  - `test_provision_writes_pod_handle_and_cost`
  - `test_provisional_handle_retains_cleanup_pending_until_reconciliation`
  - `test_session_breadcrumb_survives_on_crash`
  - `test_session_captures_pod_id_before_readiness_failure_and_terminates`
  - `test_session_keeps_breadcrumb_when_teardown_fails`
  - `test_session_mocked_artifact_smoke_uses_substrate_output_directory`
  - `test_session_nonzero_remote_exit_writes_diagnostics_artifacts_result_and_cost`
  - `test_session_storage_required_fails_before_launch_with_ensure_storage_hint`
  - `test_session_transient_handle_exists_during_detached_exec_and_is_removed_after`
  - `test_session_writes_breadcrumb_and_deletes_on_teardown`
  - `test_teardown_idempotent_pod_not_found`
  - `test_teardown_terminates_and_writes_receipt`
- `tests/packs/runpod/test_provision_ports.py` ×2 (group E): `test_ports_default_unchanged_when_omitted`, `test_ports_flag_appears_in_snapshot`
- `tests/packs/runpod/test_worker_process.py` ×4 (group F ×3, group G ×1)
  - `test_stop_pins_process_and_never_signals_after_identity_drift` (F)
  - `test_stop_requires_pinned_exit_proof_before_stopped_receipt[False|True]` (F, 2)
  - `test_linux_owned_host_survives_launcher_and_exact_stop` (G)
- `tests/packs/test_vibecomfy_metadata.py::VibeComfyStructuredMetadataTest::test_run_rejects_missing_or_empty_engine_inventory`, group I
- `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene`, **NEW vs baseline, inherited from integration**
- `tests/sdk/test_host_bootstrap_source_identity.py` ×16 (groups A ×13 and C ×3, per the cutlist split)
  - `test_bootstrap_passes_inventory_identity_and_restarts_on_change`
  - `test_bootstrap_stops_on_correlated_terminal_registration_failure`
  - `test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`
  - `test_startup_budget_polling_preserves_identity_and_original_cleanup[...]` ×13
- `tests/stage1/test_pack_host_interpreter_identity.py::test_bootstrap_reuses_only_the_selected_interpreter[...]` ×4, group B
- `tests/test_generic_host.py::test_failed_worker_release_retains_original`, group J
- `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`, group K

## Group status: the brief's "fixed on integration" premise does not hold

The brief lists groups A, B, C, D, E, F, I, K, L as baseline failures "since fixed on integration". The logs show **none of them are fixed**: all of their nodes fail on integration and in M2, with the same causes. The 0720 compare reported the same result (FIXED: 0).

Cause evidence in the M2 log (kept tracebacks, line numbers in `tests/agt-m2-stack-sync-2-full-remotion-integration-1020063510-102/log.txt`):

| Group | Nodes | Still failing in M2 | Trace evidence (log line) |
|---|---:|---|---|
| A | 27 | yes (13 host_bootstrap + 14 host_recovery) | `RemotionValidationError: runtime validation refuses unsupported loader/interpreter override` (1349 onward, 14 kept) |
| B | 4 | yes | in the stage1 node set; "prior Remotion host lacks launch validation" not in the kept tracebacks |
| C | 3 | yes | `PosixPath ... pack_root` not in the kept tracebacks; the 3 nodes are inside the 16 host_bootstrap nodes |
| D | 11 | yes | `ERR_UNKNOWN_FILE_EXTENSION` (2169 onward), Node 20 cannot import `.ts` |
| E | 34 | yes | `ModuleNotFoundError: No module named 'astrid.packs.runpod.executors'` (3987 onward) |
| F | 3 | yes | `NameError: name 'signal' is not defined` (3240, 3341, 3362) |
| G | 1 | yes | in the node set (env / child-stderr question, unchanged) |
| H | 7 | yes | in the node set (`No module named 'astrid'` per cutlist, unchanged) |
| I | 1 | yes | in the node set; `DumpError` not in the kept tracebacks |
| J | 1 | yes | in the node set; `CommandCleanupUnresolved` not in the kept tracebacks |
| K | 1 | yes | in the node set; `assert 200 <= 50` not in the kept tracebacks |
| L | 1 | yes | `ImportError ... attempted relative import with no known parent package` (213) |
| M | 15 | yes | in the node set (VibeComfy sibling checkout, unchanged) |

"Not in the kept tracebacks" means pytest did not keep that trace in the log. The node is still in the FAILED/ERROR set, and the cause comes from the cutlist, not from this run.

## Verdict

**stack adds 0 new failures** (relative to integration; identical set).

- Relative to the 109 baseline: **2 new**, both already present in the integration run and so not caused by the M2 stack:
  1. `test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`: runtime checkout pins Composition 0.0.8, snapshot 0.0.10 (`fc6c1f26`).
  2. `test_repo_hygiene.py::test_live_tree_passes_repo_hygiene`: root `design/` dir is not allowlisted.
- Relative to baseline: **FIXED 0**. All 109 baseline nodes still fail in M2.

## Recommended next steps

- Fix the two inherited NEW items on the integration side, not in the M2 stack: align the runtime checkout's Composition pin to 0.0.10 (or the test environment), and either allowlist `design/` or move the two contracts under `docs/`.
- Confirm that the cutlist FIX commits for groups A–L are not yet on integration or M2. The data says they are not present in either run.

## Unverified

- No test was re-run. The verdict relies on set-diff of the logs' FAILED/ERROR short summaries and on the kept tracebacks.
- The M2 run has 12998 passed and 14 xfailed, against 11783 passed and 16 xfailed on integration. The +1215 passed and the −2 xfailed are not explained by the summaries. Check which tests moved from xfailed to passed before accepting the M2 tree; this does not change the failure verdict.
- Group C node membership is not confirmed individually (per the cutlist note).
