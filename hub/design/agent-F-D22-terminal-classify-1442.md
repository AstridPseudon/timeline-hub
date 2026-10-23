# F-agent D22 terminal inventory — corrected return

## Decision and preserved evidence

Classification: **FAIL**. Inventory completeness: **PASS** separately. The
sole authorized service `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`
is terminal FAIL, exit 1: 185 failed, 16,733 passed, 4 skipped, 19 errors,
86 warnings, and 565 passed subtests. The marker census is `.=16,733,
F=185, E=19, s=4, u=565`; `u` means passed subtests.

The adjacent JSON preserves every 204 failed/error node ID and now has one
corrected classification for each. Raw terminal SHA-256:
`e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.

- Agent actual: commit `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree
  `c4d72b065d6e68c92e4335120cc016cadf53b06a`.
- Runtime: `3b926efab2eed122d374540baee297d4cdcec62a`.
- Profile: `agent-remotion-v3-819acf-1110`, archive SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`,
  composition `0.0.14`.
- Comparison base remains Base583
  `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`; the 8c355 actual snapshot is
  not relabelled as Base583.

## Corrected exact groups

| group | count |
|---|---:|
| child-probe | 17 |
| child-import-or-recipe | 87 (86 old environment-trace nodes + the moved Remotion owning-pack-root node) |
| custody-process-assertion | 11 |
| fixture-declared-gap | 2 |
| g5-inverse | 23 |
| profile-fixture | 37 |
| child-import | 9 |
| d13-preflight | 1 |
| r1-private | 7 |
| g5-publisher | 2 |
| g5-schema | 2 |
| r3-docs | 1 |
| d09-probe | 3 |
| r5-retired-route | 2 |
| **total** | **204** |

The 11 custody/process nodes are source-backed assertion mismatches but remain
**UNCONFIRMED**; they are not assumed to be environment failures or product
regressions. Owner handoff: `childenv1454` LIVE plus the owning source owners.

1. `tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]` — raw `1972-2028`; `custody_broker.py:child_exec_from_environment`; allowed `astrid/core/execution/custody_broker.py`; observed `denied=False`; acceptance: first endpoint allowed, second denied with `NetworkPolicyError`, custody keys cleared, exit 0, child stderr/env captured.
2. `tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]` — raw `2031-2087`; same function/file; observed `denied=False`, `engine_fd=False`; acceptance additionally requires `engine_fd=True`.
3. `tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]` — raw `12988-13035`; `_run_command_definition`, `_observe_owned_review_session`, `_retire_owned_review_session`; allowed `astrid/core/execution/generic_host.py`; `observed=[]`; acceptance: observe one owned URL, cancel, settle, retain attempt.
4. `tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]` — raw `13036-13083`; same owner/file; `observed=[]`; acceptance: observe one URL, preserve foreign drift marker, raise `HostError`, settle owner.
5. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]` — raw `13084-13133`; `GenericPackHost.run_task/shutdown`, `_ManagedTaskAdapter`; allowed `generic_host.py`, `process_group.py`; shutdown marker absent; acceptance: real worker enters, one process settles, cancelled result/no failures, attempt removed.
6. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]` — raw `13134-13183`; same owner/files; marker absent; acceptance is the keep-attempt variant and retains the attempt.
7. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]` — raw `13184-13233`; same owner/files; marker absent; acceptance is claim-slot accounting with removal.
8. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]` — raw `13234-13283`; same owner/files; marker absent; acceptance is claim-slot accounting with retention.
9. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]` — raw `13284-13332`; `run_task/shutdown`, `verify_tree_absent`; allowed `generic_host.py`, `process_group.py`; uncertain marker absent; acceptance: prove tree or refuse with `CleanupUncertainError` without claiming cleanup.
10. `tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context` — raw `14790-14828`; `_child_environment`, `_launch_worker_probe_environments`, `_registry_context`; allowed `generic_host.py`, `remotion_runtime.py`; unexpected `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`; acceptance: observed context equals a projected context with isolation preserved.
11. `tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]` — raw `14870-14924`; `_child_environment`, `_run_command_definition`, `_registry_context`; same allowed files; unexpected schema Pythonpath versus projection; acceptance: actual command context equals projection without PYTHONPATH/ASTRID_PACKS_PATH leakage.

The Remotion node `tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root` moved from `profile-fixture` to the unconfirmed environment group: raw `14927-14960`/summary `22648`, `ModuleNotFoundError: runtime_protocol`, owner `childenv1454` LIVE.

## Profile and guardrails

The remaining 37 `profile-fixture` nodes are **UNCONFIRMED causal
profile/oracle mismatch**, owner `profile1454` LIVE: 14 show archive 80 vs
expected 77, 9 show composition 0.0.14 vs 0.0.13, 11 show missing
`chunk-SE4TPVLW.js`, and 3 show unmapped generated scopes. These facts do not
prove pre-existing behavior, non-regression, deferred credit, or PASS.

The four skipped IDs remain unavailable; no xfail/xpass or deselection
identities were retained. D14 and D23 exact nodes are not exercised. No new
deferred or PASS claim is made. Live handoffs are `childenv1454`, `profile1454`,
`inventory1456`, and the existing inverse/private owners.

No tests, full suites, provisioning, type checks, lint, or environment changes
were run for this evidence-only return. The actual full result remains FAIL;
the production caller/full-v2-shapes guardrails are unchanged.
