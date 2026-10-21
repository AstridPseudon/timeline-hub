# Agent full21969 child-environment failure map

Date: 2026-10-21 UTC. This is a read-only follow-up to
`agent-full21969-classification.md`; it does not replace the overall
classification or attribute the full suite to one cause.

## Terminal evidence and identity boundary

The retained job is
`agent-venv-agent-child-published14-b9797941-full-1021045238-21969`:

```text
138 failed, 15840 passed, 456 skipped, 4 xfailed, 4 errors
565 subtests passed; exit 1
```

The command was:

```text
env -i HOME=/root LANG=C.UTF-8 PATH=... \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-published14-b9797941/lib/python3.13/site-packages \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent-child-published14-b9797941/bin/python -m pytest -q -n 3
```

The captured Agent source was tree `0698a30b3eb42d47db84ed5ed2e21221158795c4`
on integration commit `cc37291af12ac6504eb48dd71ea39b9dfdb56d71`. The child
was a separate read-only install whose marker is `b97979411`; it is not an
installed copy of the exact `cc37291`/`0698a30` source snapshot. This is the
important `cc372` versus `b979` boundary: the run used current source in the
checkout, but the selected Python and installed Agent bytes came from the
older `b979` child. Do not call the child an exact source fixture for
`cc372`.

The fixture selected the child interpreter, not a shared interpreter:

* xdist reports Python 3.13.16 at
  `/home/user/work/venv-agent-child-published14-b9797941/bin/python`;
* renderer receipts and subprocess arguments repeat that same executable;
* the child-process code uses `sys.executable` and then rebuilds `PYTHONPATH`;
* `/home/user/work/runtime` is an `ASTRID_RUNTIME_CHECKOUT` and parent import
  path only. It is not the interpreter and does not make Runtime packages
  installed in the child.

The child has `astrid` and the vendored `astrid_runtime_client`, but no
`runtime_protocol` or `astrid_runtime`. Its sanitized child environments also
discard the parent checkout path. The first direct child traceback is the
`sitecustomize`/worker import failure:

```text
ModuleNotFoundError: No module named 'runtime_protocol'
```

The same missing import appears at `astrid/core/execution/persistent_supervisor.py:17`,
`astrid/core/foundation/atomic_io.py:16`, `astrid/sdk/documents.py:19`, and
`astrid/core/gateway/diagnostics.py:13`. The public `doctor` wrapper can mask
the latter with its existing `UnboundLocalError`; that wrapper is a consequence,
not a second package diagnosis. No traceback in this terminal run names
`astrid_runtime` as the missing module; the installed-profile probes establish
that it is absent as well.

## Exact environment-blocked node sets

These are the failed nodes whose child/CLI traceback is the missing Runtime
package boundary. Parameter sets are expanded exactly as printed by the
terminal summary.

### Child host, pack, and subprocess boundary

```text
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
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]
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
tests/reshape/test_compare_baselines.py::test_structure_baseline_script_runs_directly_from_outside_the_checkout
```

The `test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client`
node belongs in this same environment set even though its first assertion is
the `CalledProcessError` wrapper: the child stderr immediately ends at
`persistent_supervisor.py:17` with the same missing `runtime_protocol` import.

The CLI/SDK environment set is:

```text
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-healthy-local]
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unavailable-shared]
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unknown-local]
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[doctor-unknown-shared]
tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
```

The first three CLI nodes report `No module named 'runtime_protocol'`; the
doctor node reports the wrapper `UnboundLocalError`. The SDK node reports
`ImportError: cannot import name 'platform' from 'runtime_protocol' (unknown
location)`. That last form is an environment/protocol-origin failure, but it
is not evidence that the Agent source changed Runtime's API; preserve it as a
separate focused check after the coherent install.

### Rendering and managed-scene dependent set

These nodes fail below the same child prerequisite, either as a renderer
transport error whose embedded child stderr is the missing import or as a
managed-probe exit with `original_wait_exit_code=1`. They should be retested
only after the installed pair is coherent, and should not be counted as
independent rendering regressions now:

```text
tests/core/rendering/test_conformance.py::test_minimal_render_wire_parity
tests/core/rendering/test_conformance.py::test_request_sensitive_support_wire_parity
tests/core/rendering/test_conformance.py::test_passthrough_audio_wire_parity
tests/core/rendering/test_conformance.py::test_no_audio_wire_parity
tests/core/rendering/test_conformance.py::test_attachment_wire_parity
tests/core/rendering/test_conformance.py::test_intentional_failure_wire_parity
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
```

The following host-bootstrap nodes expose the same failed managed Remotion
probe rather than the inner module line in their top-level traceback:

```text
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
```

The three managed-scene setup errors are the same probe cascade:

```text
tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]
tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
```

Their receipt records child `b979` and exit code 1 during
`registry_discovery`; the retained probe stderr is the missing Runtime import.

## Unrelated counterexamples retained separately

These are concrete counterexamples to treating every terminal failure as the
missing Runtime package. They have a different first failure and remain
unclassified by this handoff:

```text
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-register]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-bind-launch]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-register]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-bind-launch]
tests/core/execution/test_platform_boundary.py::test_agent_native_process_and_lock_boundary
tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[False]
tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[True]
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[darwin-launchd.plist]
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[linux-systemd.service]
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[win32-task.xml]
tests/test_installer_schema.py::test_remotion_lock_pins_the_transitive_schema_package
tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]
tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[True-1]
tests/test_generic_host.py::test_vendored_runtime_client_timeout_is_bounded_and_request_correlated
tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary
```

The RLE node is a collection error, not a Runtime import failure:
`fixture 'native_host' not found`. The installer snapshot nodes show trailing
newline differences; the installer-schema node reports a missing
`node_modules/@banodoco/timeline-schema` key; the generic-host timeout node
reports a fixture callback `TypeError`. These observations are deliberately
not converted into source or dependency conclusions here.

## Exact private follow-up for the staged pair owner

A separate worker already staged the Runtime/client half at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging
```

Its recorded inputs and checks are:

* Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`;
* generated client/artifacts `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
* the frozen 164-pin digest `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`;
* 23,720 dependency files matched the read-only parent byte-for-byte, with
  zero symlinks and zero RECORD-containment errors.

The staged Agent installation is intentionally absent because no
`agent-source.sha` was supplied. The owner follow-up is therefore:

1. Freeze one explicit final Agent source SHA in `agent-source.sha`. Do not
   substitute the child marker `b97979411`, and do not silently claim the
   `cc37291` source tree is the installed child.
2. Build one non-editable Agent wheel from that exact private source copy and
   install it only into the staged private environment. Keep Runtime b92,
   client/artifact 95bd, all 164 pins, and the existing profile carrier; do
   not alter shared venvs, checkouts, node installs, or package metadata.
3. Before any focused test, from a neutral directory and with no
   `PYTHONPATH`, require the selected private interpreter to resolve
   `astrid`, `astrid_runtime_client`, `runtime_protocol`, `astrid_runtime`,
   and `banodoco_timeline_schema` inside that private environment. Also verify
   the Agent marker/source SHA, wheel RECORD containment, symlink-free profile,
   Runtime/client contract and artifact digests, and `sys.executable` identity.
4. Run only the normal read-only CLI preflight through that interpreter:
   `python -I -B -m astrid --help` and
   `python -I -B -m astrid doctor --json`. A valid prerequisite result has
   direct Runtime imports and either normal Runtime observation or an explicit
   normal Runtime-unavailable result; it must not show the b979 missing import
   or the masked doctor `UnboundLocalError`.
5. Only after all prerequisite checks pass should the manager request the one
   later focused qualification check. The current full21969 result is not
   qualification evidence and must not be replayed by this worker.

No source, dependency, suite, or test edits were made for this map.
