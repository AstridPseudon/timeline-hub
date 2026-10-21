# Agent full21969 exhaustive terminal partition

Date: 2026-10-21 UTC

## Scope and result

This is a read-only partition of the retained terminal log. No test was
rerun, and no source, test, dependency, fixture, suite, or environment was
changed.

Retained result directory:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-venv-agent-child-published14-b9797941-full-1021045238-21969

Retained summary:

    138 failed, 15840 passed, 456 skipped, 4 xfailed, 85 warnings,
    4 errors, 565 subtests passed in 3351.03s (0:55:51); exit 1

The sets below are disjoint and exhaustive.

| partition | failed | errors | total |
|---|---:|---:|---:|
| DIRECT — terminal trace names missing runtime_protocol | 73 | 0 | 73 |
| DERIVED — wrapper/child trace identifies the same cause | 34 | 3 | 37 |
| UNCLASSIFIED — another terminal cause, including one fixture error | 31 | 1 | 32 |
| **total** | **138** | **4** | **142** |

DIRECT means the retained node's failure trace or captured child traceback
ends at the missing-module failure. DERIVED means the terminal exception is a
wrapper, but the retained traceback or payload gives a chain to the same
missing-module failure. UNCLASSIFIED records what the terminal log actually
shows; it does not claim that these nodes are environment-only or
product-owned.

## Evidence and source locations

The repeated generic-host chain is:

    astrid/core/execution/__init__.py:2
      -> astrid/core/execution/persistent_supervisor.py:17
         from runtime_protocol import platform
         ModuleNotFoundError: No module named 'runtime_protocol'

Other direct chains identify the same missing package at
astrid/core/foundation/atomic_io.py:16, astrid/packs/vibecomfy/production_engine.py:19,
or the child rendering launcher before it reaches
astrid/core/execution/persistent_supervisor.py:17.

The derived rendering chain is retained as a renderer payload or probe trace,
not reclassified as a direct node:

    astrid/core/rendering/transport.py:328
      -> astrid/core/rendering/errors.py:110
         RendererInternalError / RendererError payload contains the child
         ModuleNotFoundError from runtime_protocol

    astrid/packs/rendering/actions/render/task_adapter.py:466
      -> astrid/packs/rendering/actions/render/run.py:9
         -> astrid/core/execution/persistent_supervisor.py:17
            ModuleNotFoundError: No module named 'runtime_protocol'

    tests/sdk/test_timeline_commit_provider.py:101
      -> astrid/sdk/timeline/commit.py:1017
         -> astrid/core/element/project_packs.py:27
            -> astrid/sdk/documents.py:19
               ImportError: cannot import name 'platform' from runtime_protocol

The managed-scene and bootstrap derived nodes surface the child probe failure
as RemotionValidationError at astrid/core/rendering/remotion_runtime.py:632.
The retained probe evidence identifies the underlying import at
astrid/core/rendering/remotion_runtime.py:26, with original_wait_exit_code=1
and phase=registry_discovery.

The independent fixture error is explicit:

    tests/sdk/test_scene_real_public_summary_rle.py:51
    fixture 'native_host' not found

This remains separate from the missing-module partition.

## DIRECT (73 failed nodes)

    tests/core/execution/test_custody_broker.py::test_isolated_wrapper_reaches_fake_peer_without_workload_startup_hook
    tests/core/execution/test_generic_host_actions_v3.py::test_static_discover_admit_dry_run_and_owned_child
    tests/core/execution/test_generic_host_actions_v3.py::test_python_action_receives_original_host_bridge_before_import
    tests/core/pack/test_source_setup.py::test_real_outer_command_inventory_route_retains_sibling_creator_waits_and_graph
    tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]
    tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-m]
    tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[script]
    tests/core/pack/test_source_setup.py::test_real_filtered_command_root_cf_pin_preserves_all_four_inventory_operations
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[None]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[False]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[0]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[value4]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[value5]
    tests/core/execution/test_generic_host_actions_v3.py::test_strict_json_results_are_nested_data[value6]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[float('nan')]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[float('inf')]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[object()]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[(1, 2)]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[{1: 'bad'}]
    tests/core/execution/test_generic_host_actions_v3.py::test_non_json_result_fails[__import__('pathlib').Path('/fake')]
    tests/core/execution/test_generic_host_actions_v3.py::test_output_schema_validates_return_without_file_ports
    tests/core/execution/test_generic_host_actions_v3.py::test_input_schema_before_import_and_only_effective_kwargs
    tests/core/execution/test_generic_host_actions_v3.py::test_relative_helpers_initializers_and_source_only_bytecode[actions/hello.py-from .helper import value\nfrom ..shared import extra\n]
    tests/core/execution/test_generic_host_actions_v3.py::test_relative_helpers_initializers_and_source_only_bytecode[actions/larger/run.py-from ..helper import value\nfrom ...shared import extra\n]
    tests/core/execution/test_remotion_host_session.py::test_two_public_command_workers_settle_task_leases_then_host_drains_original
    tests/core/execution/test_generic_host_actions_v3.py::test_malformed_entrypoint_rejected_without_import[/tmp/escape.py-run]
    tests/core/execution/test_generic_host_actions_v3.py::test_malformed_entrypoint_rejected_without_import[actions/../escape.py-run]
    tests/core/execution/test_generic_host_actions_v3.py::test_malformed_entrypoint_rejected_without_import[actions/hello.py-bad-name]
    tests/core/execution/test_generic_host_actions_v3.py::test_action_failure_uses_existing_host_error[other = 1\n-missing or not callable]
    tests/core/execution/test_generic_host_actions_v3.py::test_action_failure_uses_existing_host_error[run = 1\n-missing or not callable]
    tests/core/execution/test_generic_host_actions_v3.py::test_action_failure_uses_existing_host_error[def run(value):\n    raise RuntimeError('intentional failure')\n-intentional failure]
    tests/core/execution/test_generic_host_actions_v3.py::test_condition_skip_and_public_runner_bypass_are_import_free
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[typed-cancel_requested-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[typed-cancelled-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[canonical-cancel_requested-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[canonical-cancelled-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[wrapped-cancel_requested-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[wrapped-cancelled-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[legacy-cancel_requested-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[legacy-cancelled-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_runtime_cancellation_contains_owned_action_without_terminal_ack[canonical-cancel_requested-True]
    tests/core/execution/test_generic_host_actions_v3.py::test_canonical_running_state_wins_over_legacy_cancelled_field[False]
    tests/core/execution/test_generic_host_actions_v3.py::test_canonical_running_state_wins_over_legacy_cancelled_field[True]
    tests/core/execution/test_generic_host_actions_v3.py::test_canonical_punctuation_paths_use_opaque_module_names[actions/hello-world.py]
    tests/core/execution/test_generic_host_actions_v3.py::test_canonical_punctuation_paths_use_opaque_module_names[actions/a-folder/script.v1.py]
    tests/core/execution/test_generic_host_actions_v3.py::test_python_return_settles_with_trusted_evidence_and_no_files
    tests/core/execution/test_generic_host_actions_v3.py::test_python_declared_files_require_real_attempt_output[False]
    tests/core/execution/test_generic_host_actions_v3.py::test_python_declared_files_require_real_attempt_output[True]
    tests/core/execution/test_generic_host_actions_v3.py::test_private_imports_add_no_repository_or_pack_pythonpath
    tests/core/execution/test_generic_host_actions_v3.py::test_legacy_child_command_and_ancestor_import_fence
    tests/core/execution/test_generic_host_actions_v3.py::test_schema_required_value_preserves_json_semantics[None]
    tests/core/execution/test_generic_host_actions_v3.py::test_schema_required_value_preserves_json_semantics[]
    tests/core/execution/test_generic_host_actions_v3.py::test_cancellation_after_child_result_blocks_success
    tests/core/execution/test_generic_host_actions_v3.py::test_legacy_orchestrator_child_command_route
    tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[False-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[False-True]
    tests/reshape/test_compare_baselines.py::test_structure_baseline_script_runs_directly_from_outside_the_checkout
    tests/packs/test_vibecomfy_ir_bridge.py::test_t9_actual_executor_child_loads_pinned_callable_and_settles_output
    tests/packs/test_vibecomfy_ir_bridge.py::test_t9_absent_explicit_activation_preserves_production_dispatch[False]
    tests/packs/test_vibecomfy_ir_bridge.py::test_t9_absent_explicit_activation_preserves_production_dispatch[True]
    tests/packs/test_vibecomfy_ir_bridge.py::test_t9_child_uses_explicit_pinned_fixture_outside_product_root[None]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_revision]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_content]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[revision_drift]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[content_drift]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[checkout_drift]
    tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[profile_hash_drift]
    tests/stage1/test_media_handoff_render_boundary.py::test_host_derived_registry_executes_canonical_ffmpeg_executor
    tests/stage1/test_pack_host_interpreter_identity.py::test_selected_vibecomfy_checkout_survives_generic_host_worker_boundary
    tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack
    tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen

## DERIVED (37 nodes: 34 failed, 3 errors)

These nodes have a wrapper or a captured child result. The retained log still
identifies the same missing-module chain described above.

    tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client
    tests/core/rendering/test_freeze.py::test_freeze_real_ffmpeg_transport_one_video_one_committed_sidecar
    tests/core/rendering/test_service.py::test_real_ffmpeg_renders_through_generic_service[nominal]
    tests/core/rendering/test_service.py::test_real_ffmpeg_renders_through_generic_service[with-audio]
    tests/core/rendering/test_service.py::test_real_ffmpeg_audio_reactive_through_generic_service
    tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root
    tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable
    tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_empty_and_exact_text_fields
    tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
    tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_non_rendered_audio_ownership
    tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_window_and_rejects_fps_mismatch
    tests/packs/rendering/test_threejs_backend.py::test_threejs_identity_invariants_never_claim_remotion
    tests/packs/rendering/test_threejs_backend.py::test_threejs_own_namespace_config_is_strict
    tests/packs/rendering/test_builtin_registration.py::test_real_ffmpeg_render_through_registered_backend
    tests/packs/rendering/test_ffmpeg_backend.py::test_manifest_command_dispatches_from_pack_root
    tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
    tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_passes_inventory_identity_and_restarts_on_change
    tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure
    tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30]
    tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30]
    tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]
    tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[True-1]
    tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]
    tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]
    tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result

## UNCLASSIFIED (32 nodes: 31 failed, 1 error)

These nodes are not silently attributed to the child environment. Their
independent terminal causes and source locations are:

| cause shown by retained log | nodes | source location |
|---|---:|---|
| Network-hook assertion observed denied: false | 2 | tests/core/execution/test_custody_broker.py:189 |
| Expected pidfd mock call was absent | 4 | tests/core/execution/test_pidfd_callers.py:138 |
| Native-process/lock inventory reports actual product violations | 1 | tests/core/execution/test_platform_boundary.py:70; reported astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:48 and astrid/sdk/timeline/outbox.py:4,35 |
| Windows attempt directory did not call the patched private-directory helper | 2 | tests/core/execution/test_platform_helpers.py:85 |
| Rendering conformance consumer could not find sdk/result.json | 6 | tests/core/rendering/test_conformance.py:203,234,282,300,318,357 (shared producer setup at :108-146) |
| Managed-review cancellation assertion | 2 | tests/core/execution/test_generic_host_actions_v3.py:1497 |
| CPU shutdown/release assertions | 5 | tests/core/execution/test_generic_host_actions_v3.py:1770,1816 |
| Installer service snapshots differ by trailing newline | 3 | tests/test_installer_platforms.py:73 |
| Remotion lock inventory lacks the transitive schema key | 1 | tests/test_installer_schema.py:101 (KeyError: node_modules/@banodoco/timeline-schema) |
| Public diagnostic bundle expected structured output but got the gateway wrapper | 4 | tests/test_public_boundary.py:141-142; status retains ModuleNotFoundError text, doctor retains UnboundLocalError, without a traceback chain to classify further |
| Timeout monkeypatch signature does not accept the request shape | 1 | tests/test_generic_host.py:1511 |
| Missing pytest fixture native_host | 1 error | tests/sdk/test_scene_real_public_summary_rle.py:51 |

Exact node IDs:

    tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
    tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
    tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-register]
    tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-bind-launch]
    tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-register]
    tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-bind-launch]
    tests/core/execution/test_platform_boundary.py::test_agent_native_process_and_lock_boundary
    tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[False]
    tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[True]
    tests/core/rendering/test_conformance.py::test_minimal_render_wire_parity
    tests/core/rendering/test_conformance.py::test_request_sensitive_support_wire_parity
    tests/core/rendering/test_conformance.py::test_passthrough_audio_wire_parity
    tests/core/rendering/test_conformance.py::test_no_audio_wire_parity
    tests/core/rendering/test_conformance.py::test_attachment_wire_parity
    tests/core/rendering/test_conformance.py::test_intentional_failure_wire_parity
    tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]
    tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]
    tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]
    tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]
    tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]
    tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[darwin-launchd.plist]
    tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[linux-systemd.service]
    tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[win32-task.xml]
    tests/test_installer_schema.py::test_remotion_lock_pins_the_transitive_schema_package
    tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-healthy-local]
    tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unavailable-shared]
    tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unknown-local]
    tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[doctor-unknown-shared]
    tests/test_generic_host.py::test_vendored_runtime_client_timeout_is_bounded_and_request_correlated
    tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary

## Historical comparison and follow-up boundary

The old full5664 result had six absent terminal nodes. That historical absence
is not a classification of this current run. The current qualification has
the 142 nodes above; no current node is removed or replaced by the old
six-node fact.

This report proposes no source fix and requests no suite. The child-environment
worker owns the installed-profile map; the Viewing handoff worker owns its
scoped rendering/managed-scene map. Those ownership boundaries do not convert
the unclassified nodes into environment failures.
