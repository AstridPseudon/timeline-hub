# Agent baseline — 2026-10-19

## Run identity and counts

The authoritative replacement for the stopped original default run was the
central Linux run `agent-full-1019191532-6465`:

```text
command: /home/user/work/venv-agent/bin/python -m pytest -q -n 3
source: main + Viewing labels, a650280634de105641561c3475e37b2e5f77c4ef
test snapshot: e475f212efff430149cbc2e6fa834980106aaf13
result: 48 failed, 11503 passed, 456 skipped, 15 errors,
        13 warnings, 563 subtests passed in 3433.42s (0:57:13)
```

This is the pre-port Agent baseline. It contains no Agent M1
core/provider/frontend changes. The later current integration head is
`a8eb28af`; relevant RunPod, generic-host, H3 CPU, structure-test, and
VibeComfy paths are unchanged from `a6502806`, so that later head is used only
for read-only comparison, not attribution. The full suite was not rerun.

## Classification of every non-passing node

All 63 nodes are accounted for below. Counts are pytest nodes, including
parameterized cases.

### Environment/setup/toolchain — 23 failures and 15 errors

* **15 errors, missing external VibeComfy fixture:** every node in
  `tests/packs/runpod/test_worker_staging.py` failed in the module-scoped
  `source_fixture` before test code ran. The traceback is the same for all:
  `shutil.copytree(VIBECOMFY / "vibecomfy", ...)` raises
  `FileNotFoundError` for `/home/vibecomfy/vibecomfy` (also requiring the
  sibling `pyproject.toml` and `README.md`). Exact nodes: `test_preparation_runs_real_child_probe_and_reuses_verified_content`,
  `test_materialized_h3_bundle_stages_as_an_owned_workflow_root`,
  `test_interrupted_upload_reconciles_remote_bytes_without_reupload`,
  `test_remote_drift_fails_closed_then_explicit_refresh_repairs_owned_source`,
  `test_workflow_pack_requires_its_unique_lock_pin_and_exact_checkout`,
  `test_manifest_pinned_workflow_pack_cannot_omit_its_checkout_root`,
  `test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_leaf]`,
  `[lock_parent]`, `[node_leaf]`, `[node_parent]`,
  `test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse`,
  `test_empty_remote_observation_and_model_shadow_remain_unresolved`,
  `test_release_manifest_datacenter_and_account_reference_are_mandatory`,
  `test_manifest_volume_alias_is_optional_but_mismatch_and_effective_path_drift_fail_closed`,
  and `test_json_selection_uses_production_composition_and_real_cpu_staging`.
  This is an external RunPod/VibeComfy fixture/setup limitation, not an Agent
  timeline failure.
* **7 failures, uninstalled-source child probe:** all parameterizations of
  `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard`
  (`success`, `missing_revision`, `missing_content`, `revision_drift`,
  `content_drift`, `checkout_drift`, `profile_hash_drift`) fail at the child
  `python -I -c` probe's `import astrid` with
  `ModuleNotFoundError`. The shared `/home/user/work/venv-agent` is
  dependency-only and has no installed Astrid package; isolated mode also
  removes the worktree source path. This does not test the installed artifact
  contract and is not a source regression.
* **1 failure, missing Runtime package in the test environment:**
  `tests/packs/runpod/test_worker_preparation.py::test_runtime_activation_checkpoints_restore_only_the_exact_process`
  reaches `worker_owner.py:1293`, then cannot import
  `runtime_protocol.remote_worker_activation`. The Runtime checkout exists at
  `/home/user/work/runtime`, but the full command did not expose it and the
  dependency-only Agent venv does not install `runtime_protocol`. This needs
  Runtime/test-environment wiring, not an Agent product change.

### Pre-existing main product/test or documentation issues outside Timeline M1 — 25 failures

* **34 RunPod executor-path failures (one shared stale path mismatch):**
  `tests/packs/runpod/test_ensure_storage.py` has 2 nodes
  (`test_provision_does_not_auto_create_storage`, which gets
  `FileNotFoundError` reading `astrid/packs/runpod/executors/provision/run.py`,
  and `test_storage_free_provision_and_session_do_not_probe_or_create_storage`,
  which gets `ModuleNotFoundError`); `tests/packs/runpod/test_pack_executors.py`
  has 30 nodes (`test_outer_adapter_allocation_unknown_keeps_identity_and_blocks_another_launch[provision|session]`,
  `test_launcher_preserves_known_pod_from_nonretryable_launch_failure[provision|session]`,
  `test_attached_claim_without_exclusive_authority_refuses_teardown`,
  `test_datacenter_is_forwarded_only_when_lifecycle_config_supports_it`,
  `test_pod_handle_builder_keeps_durable_and_transient_shapes_compatible`,
  `test_provision_writes_pod_handle_and_cost`,
  `test_provision_persists_allocation_before_readiness_and_marks_cleanup_pending[readiness-failure0|ssh-failure1]`,
  `test_provisional_handle_retains_cleanup_pending_until_reconciliation`,
  `test_provision_forwards_and_persists_allowed_cuda_versions`,
  `test_empty_explicit_cuda_filter_fails_before_launch`,
  `test_provision_storage_required_fails_before_launch_with_ensure_storage_hint`,
  `test_provision_named_storage_missing_fails_before_launch_without_creation`,
  `test_provision_configured_storage_name_is_recorded_in_canonical_handle`,
  `test_session_storage_required_fails_before_launch_with_ensure_storage_hint`,
  `test_exec_reads_handle_and_writes_result`,
  `test_exec_nonzero_remote_exit_keeps_artifacts_diagnostics_result_and_cost`,
  `test_exec_success_copies_only_substrate_returned_artifact_root`,
  `test_teardown_terminates_and_writes_receipt`,
  `test_teardown_idempotent_pod_not_found`,
  `test_session_writes_breadcrumb_and_deletes_on_teardown`,
  `test_session_transient_handle_exists_during_detached_exec_and_is_removed_after`,
  `test_session_captures_pod_id_before_readiness_failure_and_terminates`,
  `test_session_mocked_artifact_smoke_uses_substrate_output_directory`,
  `test_session_breadcrumb_survives_on_crash`,
  `test_session_keeps_breadcrumb_when_teardown_fails`,
  `test_session_nonzero_remote_exit_writes_diagnostics_artifacts_result_and_cost`,
  and `test_cost_summation_invariant`); `tests/packs/runpod/test_provision_ports.py`
  has 2 nodes (`test_ports_flag_appears_in_snapshot` and
  `test_ports_default_unchanged_when_omitted`). Every node expects
  `astrid.packs.runpod.executors[.provision.run]`; both `e51595c6` and
  `a6502806`, and current integration, provide `astrid/packs/runpod/actions/`
  instead. The relevant source/tests have no diff in `e51595c6..a6502806`.
  These are pre-existing RunPod/main path drift, outside Timeline M1 ownership.
* **3 test-code failures, omitted import:**
  `tests/packs/runpod/test_worker_process.py::test_stop_pins_process_and_never_signals_after_identity_drift`,
  `::test_stop_requires_pinned_exit_proof_before_stopped_receipt[True]`, and
  `[False]` fail before exercising the subject because the test references
  `signal` without importing it. The product module itself imports `signal`.
* **1 xdist/execnet reporting failure:**
  `tests/packs/test_vibecomfy_metadata.py::VibeComfyStructuredMetadataTest::test_run_rejects_missing_or_empty_engine_inventory`
  reaches `subTest(inventory=...)`, then xdist cannot serialize its
  `PosixPath` value (`execnet.gateway_base.DumpError`). This is a
  Python3.13/pytest9.0.2/xdist3.8.0 reporting/toolchain incompatibility, not
  the asserted production behavior.
* **1 pre-existing generic-host contract mismatch:**
  `tests/test_generic_host.py::test_failed_worker_release_retains_original`
  expects `CleanupUncertainError`, but unchanged `generic_host.py` converts the
  cleanup exception to `CommandCleanupUnresolved` at the finalizer. The test
  and implementation are unchanged across `e51595c6..a6502806`; this belongs
  to core execution, outside Timeline M1.
* **1 stale documentation gate:**
  `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`
  reports `docs/giant-file-rationale.md` claims 13,598 lines for
  `astrid/core/execution/generic_host.py`, while the tree has 13,798 (delta
  200, over the allowed 50). Neither the source nor rationale changed in
  `e51595c6..a6502806`; this is a pre-existing core documentation drift.

The arithmetic is 23 setup/toolchain failures + 25 pre-existing main/core
failures + 15 setup errors = 48 failures and 15 errors.

## Ownership and Viewing check

* **Timeline Agent ownership:** none of these 63 nodes is a proved Agent
  timeline regression. The 34 executor-path nodes and the generic-host,
  structure, and RunPod test issues are outside the Timeline M1 surface and
  should not be fixed by changing timeline code.
* **Runtime:** the single `runtime_protocol` import failure needs Runtime
  checkout/package exposure in the full-suite environment. It is not evidence
  against the Agent commit/provider contract.
* **Viewing:** no baseline failure is in the Viewing-modified files. The only
  `e51595c6..a6502806` source changes are the six
  `astrid/packs/rendering/actions/timeline_visualize/*` / fast-lane files and
  `tests/packs/rendering/test_fast_lane.py`; none appears in the 48/15 node
  list. Candidate Viewing regressions: **0**.
* **Platform limit:** this was Linux only. No macOS, live RunPod/provider,
  browser, socket, or renderer-availability conclusion is claimed from this
  run.

## Other recorded evidence (separate from the full baseline)

| Command / check | Recorded outcome |
| --- | --- |
| `make check` | Blocked before typecheck/parity by the locked Remotion prerequisite: exact Node20.19.4/npm10.8.2 receives GitHub HTTP 403 for `@banodoco/timeline-theme-2rp` v0.1.1. |
| `python -m pytest -q tests/editing_conformance` | 179 passed, 4 existing parity skips in 19.72s. This remains a separate conformance baseline. |
| Central real M1 CLI/Python lane | 3 passed in 18.51s (`agent-commit-integration-1019195539-21968`). This is not part of the 11,503 full-run passes. |
| Normal-source integrated M1 batch | 233 passed in 17.78s. This is also separate from the pre-port full baseline. |

Doctor's hermetic subprocess drops `PYTHONPATH` and uses a temporary cwd; the
dependency-only shared environment has no installed Astrid. Mypy in this
Python3.13.16/NumPy2.5.2 environment cannot parse NumPy stubs for the repo's
target Python3.11, and the environment lacks `types-PyYAML`; main CI uses
Python3.11 and NumPy2.4.6. These are setup/toolchain observations, not green
gate claims and not Agent timeline regressions.

The one merged full request `agent-full-1019193420-11899` began after this
baseline. It is not a baseline rerun; this report does not wait for it or
use it to alter the counts above.
