# Agent supported-env baseline: 109-node cut list

Worker: agt-baseline-109-cutlist (read-only analysis; no product or test changes; no suite requested).
Set analysed: the 109 non-passing nodes of `agent full-remotion-integration` (79 FAILED, 30 ERROR) from `tests/agent-full-remotion-integration-1020031037-28578/log.txt`, identical to the f6 baseline (1020030741-1883) and to the M1 a610 run (`full-a610-classification.json`).
Code read at: worktree `/home/user/work/wt/agt-baseline-109-cutlist` (HEAD `ef6eec55`). File:line references are into that tree. The traces were produced on the 8f046 / 4a75f68f trees; a610 recorded identical blobs for the pixel, host-bootstrap, worker-process, stage1, host-recovery and runpod-staging files, but I did not diff every cited file against 8f046.

## Method and confidence

- Every node ID comes from the log's short summary, so the 109 IDs are exact.
- Causes come from the traceback in the log where one was kept (pytest only kept a subset of tracebacks, so for the rest the cluster evidence applies), then from reading the cited code.
- I did **not** run any node. The central runner builds its environment from a fixed command, and the code-level causes below do not need a run to establish. The three items marked *hypothesis* need one confirming run.
- Classification rules: **FIX** = the product is right and the test (or its fixture, harness or doc) is wrong or stale. **ENVIRONMENT** = the supported env lacks a prerequisite the test assumes. **DELETE** = the behaviour is gone; none found.

## Summary

| class | nodes | groups |
|---|---:|---|
| FIX | 86 | A, B, C, D, E, F, I, J, K, L |
| ENVIRONMENT | 23 | G (1, provisional), H (7), M (15) |
| DELETE | 0 | none; no node tests behaviour that has been removed |

Groups A to M are defined in the table below. The 86 + 23 split is exact against the 109-node set.

## Group table

| Grp | Nodes | Node ids / pattern | Cause (evidence) | Class | Smallest fix (or deletion reason) | Owner | Effort |
|---|---:|---|---|---|---|---|---|
| **A** | 27 | 13 × `tests/sdk/test_host_bootstrap_source_identity.py` (`RemotionValidationError`) + 14 × `tests/sdk/test_host_recovery.py` (ERROR at setup) | **Test-harness pollution.** `tests/conftest.py:15-18` sets `PYTHONPYCACHEPREFIX` into `os.environ` whenever `sys.pycache_prefix` is unset (always true under `env -i`). That key is in `_UNSUPPORTED_PYTHON_STARTUP` (`astrid/core/rendering/remotion_runtime.py:200-202`), so `probe_context` refuses it (`remotion_runtime.py:216-222`). The host copies `os.environ` whole (`astrid/sdk/host_bootstrap.py:734`), and the probe runs whenever `ASTRID_REMOTION_PROJECT_DIR` is set (`host_bootstrap.py:767-780`). Chain in log: `host_bootstrap.py:1576 → :780 → remotion_runtime.py:475 (_registry_context) → :222`. Only the remotion env sets that variable, which is why the 63-node normal baseline never reached it. | FIX | Stop exporting the pycache prefix into `os.environ` in conftest (keep `sys.pycache_prefix`; `PYTHONDONTWRITEBYTECODE=1` already set at conftest:13 covers bytecode). Do not loosen the probe. Expect the host-recovery harness to then run the real Remotion probe, which needs node/remotion present in this env (that is the point of the suite). | agent | S |
| **B** | 4 | `tests/stage1/test_pack_host_interpreter_identity.py::test_bootstrap_reuses_only_the_selected_interpreter[False-selected-False-False]`, `[False-selected-True-False]`, `[True-selected-False-False]`, `[True-selected-True-False]` (all `previous_python=selected`) | **Fixture gap under an ambient Remotion env.** The fake prior host writes `generic-host.json` / `.ready.json` without a `remotion_validation` marker (`tests/stage1/test_pack_host_interpreter_identity.py:63-64`). With `ASTRID_REMOTION_PROJECT_DIR` set, the reuse path refuses such a host: `astrid/sdk/host_bootstrap.py:1500-1503` raises `prior Remotion host lacks launch validation`. The test is about interpreter identity, not Remotion. | FIX | `monkeypatch.delenv("ASTRID_REMOTION_PROJECT_DIR", raising=False)` in the test, so the interpreter-identity test does not depend on ambient Remotion provisioning. The Remotion gate keeps its own tests. (Alternative: write a valid marker; larger.) | agent | S |
| **C** | 3 | `tests/sdk/test_host_bootstrap_source_identity.py`; exact membership not confirmed (see note under the table) | **Stale fake shape.** The test fakes `active_source_inventory()` with `sources=(managed,)`, a bare `Path` (line 141, inside `test_bootstrap_passes_inventory_identity_and_restarts_on_change`, lines 119-255). `astrid/core/pack/discovery.py:296` reads `source.pack_root`. Log: `AttributeError: 'PosixPath' object has no attribute 'pack_root'` at log lines 5187 and 5436. | FIX | Make the fake source record carry `pack_root` (and the fields `_add` reads at discovery.py ~:5158-5163: `revision`, `manifest_sha256`, `tree_sha256`), e.g. `SimpleNamespace(pack_root=managed, ...)`. | agent | S |
| **D** | 11 | `tests/packs/astrid_motion/test_pixel_shape_geometry.py`: AmPixelShapeGeometryTest ×4 (`test_arrow_points_right`, `test_dot_three_by_three_is_a_full_square`, `test_ring_is_hollow_and_inside_the_box`, `test_underline_is_bottom_rows_only`), AmPixelShapeRectTest ×5 (`test_corners_are_stepped`, `test_radius_is_clamped_and_stroke_thicker_than_half_is_safe`, `test_rounded_tile_has_expected_cell_counts`, `test_shape_rect_returns_the_silhouette`, `test_square_rect_is_the_full_box_and_outline_is_the_border`), AmPixelShapeBlinkTest ×2 (`test_blink_hides_for_two_frames_at_each_listed_frame`, `test_single_number_and_missing_blink_at`) | **Test assumes Node 22.** The helper runs `node --input-type=module -e "await import(<shape-cells.ts>)"` (lines 14-22, 53-58, 105-110). The supported pin is Node `=20.19.4` (`remotion/package.json:6`), which cannot import `.ts` (`ERR_UNKNOWN_FILE_EXTENSION`, per log `CalledProcessError` traces and the a610 Node 22 probe). The repo already has the supported-env pattern: `tests/packs/rendering/test_remotion_render_contract.py:367-375` bundles TS with the Remotion project's esbuild (`remotion/node_modules/esbuild/lib/main.js`). | FIX | Re-point `_cells` (and the two other helpers) to bundle `shape-cells.ts` with the Remotion esbuild, following the 367-375 precedent, keeping the `skipUnless` gating. Do not "fix" by requiring Node 22: that contradicts the pin. Note the blink class has its own skip gate (line 115); confirm it calls the same helper. | agent | S |
| **E** | 34 | `tests/packs/runpod/test_pack_executors.py` ×30 (all 30 nodes in that file that fail: outer_adapter ×2, launcher_preserves ×2, attached_claim, datacenter, pod_handle_builder, provision_writes, provision_persists ×2, provisional_handle, forwards_cuda, empty_cuda, storage_required, named_storage_missing, configured_storage_name, session_storage_required, exec_reads, exec_nonzero, exec_success, teardown_terminates, teardown_idempotent, session_writes_breadcrumb, session_transient, session_captures, session_mocked_artifact, session_breadcrumb_survives, session_keeps_breadcrumb, session_nonzero, cost_summation); `tests/packs/runpod/test_ensure_storage.py` ×2; `tests/packs/runpod/test_provision_ports.py` ×2 | **Stale module path.** Every test imports `astrid.packs.runpod.executors` (`test_pack_executors.py:27, 89, 138, 162, 376, 440, ...`; `test_provision_ports.py:35`), which does not exist (`ModuleNotFoundError`, 33 traces). The logic moved to `astrid/packs/runpod/shared/common.py` (`_build_pod_handle` :499, `_cost_amount` :171, `_resolve_compute_profile` :375, `cmd_*` :1031+). `astrid/packs/runpod/actions/*/run.py` are 18-line shims. `_RUNPOD_COMPUTE_DEFAULTS` (used at test line 30) is not in the shim's `__all__`, so tests must import `shared.common`, not the shim. `test_ensure_storage.py:130` reads `astrid/packs/runpod/executors/provision/run.py` as source (`FileNotFoundError`, log 3190) and must target `shared/common.py`. Env prerequisite: the tests patch `runpod_lifecycle.*` (`test_pack_executors.py:246-249`); that package is a dev-extra pinned from git (`pyproject.toml:44-48`) and is **not installed** in `/home/user/work/venv-agent`. | FIX (+ ENV prerequisite) | Repoint imports and source paths to `astrid.packs.runpod.shared.common` (and `actions.*.run` only for `cmd_*` if desired). The source-scan assertion in `test_ensure_storage.py` must keep its meaning (no ensure_storage call in the provision/session path). Ask the env owner to install the pinned `runpod-lifecycle` dev-extra wheel into venv-agent (a wheel already exists in the central pip cache; do not reinstall the venv yourself). Expect real behavioural diffs once imports resolve; treat them as FIX unless the product is shown wrong. | agent (env for the wheel) | M |
| **F** | 3 | `tests/packs/runpod/test_worker_process.py::test_stop_pins_process_and_never_signals_after_identity_drift`, `::test_stop_requires_pinned_exit_proof_before_stopped_receipt[True]`, `::test_stop_requires_pinned_exit_proof_before_stopped_receipt[False]` | **Missing import in the test.** `signal` is used at lines 185 and 635 (`monkeypatch.setattr(signal, "pidfd_send_signal", ...)`); the import block (lines 5-19) has no `import signal`. `NameError: name 'signal' is not defined`. | FIX | Add `import signal` to the test. | agent | S |
| **G** | 1 | `tests/packs/runpod/test_worker_process.py::test_linux_owned_host_survives_launcher_and_exact_stop` | **Hypothesis (provisional ENVIRONMENT; UNKNOWN until confirmed).** `launch_owned_process` starts `python worker_process.py --owned-host` with stderr discarded (`astrid/packs/runpod/worker_process.py:529-534`). That file imports `astrid` at module top (`:42`). `astrid` is not installed in venv-agent (no dist-info and no `.pth`), and the Popen inherits `os.environ` with no `PYTHONPATH`, so the child exits at import. The parent then raises `WorkerOwnerConflict: host did not acquire physical pod ownership` (`:546-549`). Same root as group H. Not confirmed: the child's stderr is discarded, so this is inference from the code. | ENVIRONMENT (provisional) | Confirm: run the node with `PYTHONPATH=<checkout>` in the env, or install astrid into the venv (env decision). If confirmed, the test is correct and the env is the fix. If it still fails with `PYTHONPATH` set, it is a product or test defect and needs the child's stderr captured. | env (confirm: agent) | S to confirm |
| **H** | 7 | `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[{success,missing_revision,missing_content,revision_drift,content_drift,checkout_drift,profile_hash_drift}]` | **Environment: no installed astrid.** The child runs `sys.executable -I -c <script>` (line 88). The script's first line is `import astrid` (line 65). The test pops `PYTHONPATH` (line 87) and `-I` ignores cwd and user site, so `astrid` must be installed in the interpreter. venv-agent does not install it. Log: `ModuleNotFoundError: No module named 'astrid'` (7 traces). These 7 were also failing in the 63-node normal baseline, so this is not caused by the remotion env. | ENVIRONMENT | Decide the installed-profile fixture. Either the env owner installs astrid (editable) into the supported venv, or the test builds a throwaway installed overlay (M). Do not just delete the child check: it is the installed-profile guard. | env (test overlay: agent) | M |
| **I** | 1 | `tests/packs/test_vibecomfy_metadata.py::VibeComfyStructuredMetadataTest::test_run_rejects_missing_or_empty_engine_inventory` | **xdist serialisation.** `self.subTest(inventory=inventory)` (line 171) passes `pathlib.Path` objects, which execnet cannot send from a worker (`DumpError: can't serialize PosixPath`, log ~5002). The real subtest outcome is masked. | FIX | Pass `str(...)` (or a repr) as the subtest parameter. Then read the real assertion result; it may reveal a second failure. | agent | S |
| **J** | 1 | `tests/test_generic_host.py::test_failed_worker_release_retains_original` | **Exception-type contract drift.** The test expects `CleanupUncertainError` from `host.invoke_capability` (lines 4268-4269). The product deliberately wraps cleanup failures in `CommandCleanupUnresolved(HostError)` (`astrid/core/execution/generic_host.py:8166-8172, 8387-8393`), with the original as the chained cause. Log: `CommandCleanupUnresolved: capability 'test.echo' cleanup unresolved: retained worker release failure`. | FIX (decision: agent) | Expect `CommandCleanupUnresolved` and assert `exc.__cause__` (or `execution_error`) is the `CleanupUncertainError` with the same message. This keeps the "retains original" intent. If the owner decides the wrapper is wrong, it becomes a product fix instead; that is the only alternative I see. | agent | S |
| **K** | 1 | `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` | **Stale doc metadata.** Rationale says `generic_host.py` is 13,598 lines (`docs/giant-file-rationale.md:18`); on disk it is 13,798 (log: `assert 200 <= 50`). Line 58 already documents `remotion/run.py` (2,158 vs 1,868) and `host_bootstrap.py` (1,601 vs 1,717) as "intentionally red" drift. | FIX | Refresh the three counts to the tree that lands, and delete the "intentionally red" note at line 58. Do not change the 50-line tolerance. Do this last: the counts move with every commit. | agent | S |
| **L** | 1 | `tests/sdk/test_admission_recovery.py` (ERROR, collection) | **Test loads Runtime's generated client as a bare module.** Lines 26-30 load `packages/python/astrid_runtime_client/generated.py` through `spec_from_file_location` with no package. The Runtime file uses a package-relative import (`.timeline_commit_types`), which raises `ImportError: attempted relative import with no known parent package`. The module is marked `integration` (line 18), so it is only collected in the integration lane. | FIX | Import the generated client as a submodule of its package (for example `astrid_runtime_client.generated` via the Runtime `packages/python` path), keeping the assertion at line 47 that the loaded file is the Runtime one. | agent | S-M |
| **M** | 15 | `tests/packs/runpod/test_worker_staging.py`: `test_preparation_runs_real_child_probe_and_reuses_verified_content`, `test_materialized_h3_bundle_stages_as_an_owned_workflow_root`, `test_interrupted_upload_reconciles_remote_bytes_without_reupload`, `test_remote_drift_fails_closed_then_explicit_refresh_repairs_owned_source`, `test_workflow_pack_requires_its_unique_lock_pin_and_exact_checkout`, `test_manifest_pinned_workflow_pack_cannot_omit_its_checkout_root`, `test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[{lock_leaf,lock_parent,node_leaf,node_parent}]`, `test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse`, `test_empty_remote_observation_and_model_shadow_remain_unresolved`, `test_release_manifest_datacenter_and_account_reference_are_mandatory`, `test_manifest_volume_alias_is_optional_but_mismatch_and_effective_path_drift_fail_closed`, `test_json_selection_uses_production_composition_and_real_cpu_staging` | **Environment: no sibling VibeComfy checkout.** `VIBECOMFY = ROOT.parents[2].parent / "vibecomfy"` (line 39) is derived from the agent checkout's location. The module-scoped `source_fixture` copies from it (line 211) and errors with `FileNotFoundError: /home/vibecomfy/vibecomfy` (15 traces). No VibeComfy checkout exists under `/home/user`. The derivation only resolves for one checkout depth. | ENVIRONMENT | Provide a VibeComfy checkout at the path the test expects, or (test-side, S) give the path an explicit override variable. Do not skip the fixture: that would be a silent weakening of 15 nodes. | env (override: agent) | S-M |

Note on A and C: the 14 host-recovery nodes all error in the shared `Harness.ensure()` (`tests/sdk/test_host_recovery.py:103, 149`), the same `host_bootstrap` path. The 16 nodes of `test_host_bootstrap_source_identity.py` split into A (13, `RemotionValidationError`) and C (3, `PosixPath.pack_root`), per a610. I could not map the individual node IDs to A or C from the short summary. The code only lets `test_bootstrap_passes_inventory_identity_and_restarts_on_change` reach `.pack_root` (line 141 is its only fake with bare paths; the other fakes use `sources=()`). The second `PosixPath` trace (log 5436) falls in a section whose header is `test_bootstrap_stops_on_correlated_terminal_registration_failure`, which does not use that fake. So either the trace attribution is off or the C count is off by one or two. Resolve by one targeted run of the 16 with the group A fix applied (C then shows as the only remaining `pack_root` failures).

## Per-group node lists

**A (27)**
- `tests/sdk/test_host_bootstrap_source_identity.py`: 13 of these 16 nodes (the exact split with C is open, see note). The 16 are `test_bootstrap_passes_inventory_identity_and_restarts_on_change`, `test_bootstrap_stops_on_correlated_terminal_registration_failure`, `test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`, and the 13 `test_startup_budget_polling_preserves_identity_and_original_cleanup[...]` parametrisations `None-25-ready-True-25-None`, `None-None-ready-False-300.0-None`, `120-25-ready-True-25-None`, `120-None-ready-False-120-None`, `120-1-terminal-False-1-None`, `120-1-foreign_pid-False-1-None`, `120-1-foreign_birth-False-1-None`, `120-1-foreign_instance-False-1-None`, `120-1-foreign_source-False-1-None`, `120-None-exit-False-1-None`, `120-400-ready-True-400-400`, `120-None-ready-False-150.3-30`, `120-None-exit-False-1-30`.
- `tests/sdk/test_host_recovery.py` (14 ERROR): `test_launcher_attaches_to_healthy_host_from_another_checkout`, `test_launcher_replaces_cross_checkout_host_when_resident_is_unhealthy[unready-registration]`, `[changed-registration-generation]`, `[changed-resident-source]`, `test_gone_host_with_empty_group_is_dropped_and_relaunched`, `test_dead_leader_with_surviving_member_is_killed_then_dropped`, `test_live_host_with_stale_source_is_retired_by_registration_when_idle`, `test_busy_live_host_is_deferred_and_untouched`, `test_live_matching_host_is_reused`, `test_spawn_env_excludes_job_lease`, `test_pid_reused_by_unrelated_process_is_never_signalled`, `test_host_whose_validation_does_not_cover_this_caller_is_replaced_not_refused`, `test_host_helper_in_its_own_group_is_not_work`, `test_published_busy_record_decides`.

**B (4)**: see the group table.

**C (3)**: three nodes from `tests/sdk/test_host_bootstrap_source_identity.py`; membership to be confirmed (see note). Totals are unaffected by the split.

**D (11)**: see group table.

**E (34)**: see group table. Full IDs in `tests/packs/runpod/test_pack_executors.py` and the two files as listed.

**F (3)**: see group table.

**G (1)**: `tests/packs/runpod/test_worker_process.py::test_linux_owned_host_survives_launcher_and_exact_stop`.

**H (7)**: see group table.

**I (1)**, **J (1)**, **K (1)**, **L (1)**: see group table.

**M (15)**: see group table.

## Prioritised work-down order

1. **A: conftest pycache pollution** (27 nodes, S). Highest yield; unblocks the host-bootstrap and host-recovery clusters. Do it first; re-check the 27 before anything else, since they may then reveal further failures.
2. **B: stage1 Remotion isolation** (4, S). Same remotion-env cause family; do with A.
3. **D: pixel shape loader** (11, S). Pure test change, no env needed.
4. **F: `signal` import** (3, S). Trivial.
5. **C: fake inventory shape** (3, S).
6. **I: subtest params** (1, S). Do it early so any masked real failure shows up.
7. **J: generic-host exception contract** (1, S). Needs an owner decision on the wrapper.
8. **L: admission-recovery loader** (1, S-M).
9. **E: runpod executors path migration** (34, M). Largest single block of FIX work. Ask the env owner for the runpod-lifecycle wheel first, or the path fix will just move the failure to `ModuleNotFoundError: runpod_lifecycle`.
10. **G: confirm owned-host cause** (1, S): one run with `PYTHONPATH` set. Decide FIX or ENV from the result.
11. **H: installed-astrid profile** (7, M). Env decision: install astrid into the supported venv, or build an overlay in the test. Also resolves G if confirmed.
12. **M: VibeComfy sibling** (15, S-M). Env decision: provision the checkout, or add an explicit path override.
13. **K: giant-file doc refresh** (1, S). Last, against the final tree, because the counts move with every commit.

## Count by classification

- **FIX: 86** (A 27, B 4, C 3, D 11, E 34, F 3, I 1, J 1, K 1, L 1)
- **ENVIRONMENT: 23** (G 1 provisional, H 7, M 15)
- **DELETE: 0**

Reasons for no deletions: each failing node tests live behaviour that the product still has (the executors moved rather than disappeared; the Remotion gate, the installed-profile guard and the generic-host cleanup contract are all still in the code). A deletion would need a replacing test, and none is needed.

## Notes for the orchestrator

- a610's label `valid-supported-env-fixture-problem` is too coarse. Most of its 46 "additional" nodes are test-side defects that the remotion env exposed (groups A, B, C, D, L). Only the H and M families (and possibly G) are environment in the strict sense.
- Group A (the 27) is one shared root cause, and it is the single most useful change in this set. Its effect is expected from code reading, not verified by a run.
- Nothing here changes the M1 HOLD status. The 109-node set is not green, and this doc is a classification, not a pass.

## Unverified

- Group A: conftest change expected to unblock the 27, not run.
- Group E: after the import move, behavioural diffs in the 34 are unknown.
- Group G: cause is an inference from code; child stderr is discarded.
- Group C: the 3 node IDs are not identified individually from the summary.
- No run was requested. Optional confirming run, if the orchestrator wants one: `bin/request-test agt-baseline-109-cutlist remotion-env-nodes --files "<the G node>"` with the PYTHONPATH question answered by the env owner. It cannot set env by itself, so it will not confirm G on its own.

## Appendix: all 109 node IDs with group

A (27): test_host_bootstrap_source_identity.py ×13 `RemotionValidationError` nodes; test_host_recovery.py ×14 ERRORs (see per-group list).
B (4): test_pack_host_interpreter_identity.py ×4 (see per-group list).
C (3): test_host_bootstrap_source_identity.py ×3 `PosixPath.pack_root` nodes.
D (11): test_pixel_shape_geometry.py ×11.
E (34): test_pack_executors.py ×30, test_ensure_storage.py ×2, test_provision_ports.py ×2.
F (3): test_worker_process.py `signal` nodes ×3.
G (1): test_worker_process.py::test_linux_owned_host_survives_launcher_and_exact_stop.
H (7): test_character_swap_cpu_boundary.py ×7.
I (1): test_vibecomfy_metadata.py.
J (1): test_generic_host.py::test_failed_worker_release_retains_original.
K (1): test_structure_contracts.py::test_giant_file_inventory_matches_rationale.
L (1): tests/sdk/test_admission_recovery.py (collection ERROR).
M (15): test_worker_staging.py ERRORs ×15.

Full ID lists for every group are in the failure short summary of `tests/agent-full-remotion-integration-1020031037-28578/log.txt`; the per-file counts above add to 109 (27 + 4 + 3 + 11 + 34 + 3 + 1 + 7 + 1 + 1 + 1 + 1 + 15).
