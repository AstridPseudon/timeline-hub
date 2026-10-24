# D52 Bootstrap Return — Source/Evidence Report

No product or test files changed. Worktree is clean.

## Corrected 19-node mapping

| # | Exact node | Classification | Evidence |
|---:|---|---|---|
| 1 | `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]` | Environment: child runtime import surface | Canonical JSON is summary-only. Raw full9758 lines 2883–3020 show `ModuleNotFoundError: runtime_protocol`. |
| 2 | `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-m]` | Environment: child runtime import surface | Same raw traceback range, distinct parametrized node. |
| 3 | `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[script]` | Environment: child runtime import surface | Same raw traceback range, distinct parametrized node. |
| 4 | `tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client` | Environment: child runtime import surface | Retained traceback, raw lines 3021–3248; missing `runtime_protocol`. |
| 5 | `tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_passes_inventory_identity_and_restarts_on_change` | Unknown | Canonical summary-only record; no traceback or exact phase/profile binding. |
| 6 | `tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure` | Unknown | Canonical summary-only record; no traceback or exact phase/profile binding. |
| 7 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]` | Unknown: local Remotion profile/probe boundary | Traceback 19366–19535; registry discovery probe exit 1 before fake launch. |
| 8 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None]` | Unknown: local Remotion profile/probe boundary | Traceback 19535–19707; same boundary. |
| 9 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None]` | Unknown: local Remotion profile/probe boundary | Traceback 19707–19876; same boundary. |
| 10 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None]` | Unknown: local Remotion profile/probe boundary | Traceback 19876–20048; same boundary. |
| 11 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20048–20220; terminal fixture is not reached. |
| 12 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20220–20392; identity branch is not reached. |
| 13 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20392–20564; identity branch is not reached. |
| 14 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20564–20736; identity branch is not reached. |
| 15 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20736–20908; identity branch is not reached. |
| 16 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None]` | Unknown: local Remotion profile/probe boundary | Traceback 20908–21093; process-exit branch is not reached. |
| 17 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]` | Unknown: local Remotion profile/probe boundary | Traceback 21093–21262; progress/reset behavior is not reached. |
| 18 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30]` | Unknown: local Remotion profile/probe boundary | Traceback 21262–21434; same boundary. |
| 19 | `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30]` | Unknown: local Remotion profile/probe boundary | Traceback 21434–22880; same boundary. |

Rows 7–19 all stop at local `ensure_pack_host → _prepare_render_validation → registry_discovery → _require_completed_probe`, with `original_wait_exit_code=1`, `census_complete=true`, and `custody_admitted=true`. There is no evidence of paired relay, RunPod, remote authority, or D46-deferred scope.

The canonical JSON276 artifact and its retrospective counts were not rewritten.

## Caller attribution

- Actual bootstrap callers: `astrid/sdk/autobootstrap.py:496–502` and `astrid/services.py:81–90 → run_pack_host_foreground → host_bootstrap.py:1815–1818`.
- `astrid/core/execution/generic_host.py:8462–8463` constructs the child-worker command.
- `generic_host.py:14054–14065` performs downstream startup identity attestation.

## Next actions

1. After owner admission, use only the existing immutable Runtime-enabled child environment for rows 1–4; rerun exact selectors and record child import origins.
2. Re-capture rows 5–6 with complete traceback plus exact environment/profile metadata before assigning ownership or proposing deletion.
3. After owner admission, use only the qualified immutable `agent-remotion-v3-819acf-1110` profile for rows 7–19, retaining probe stderr and exact profile metadata. No overlay or installation.

Tests were not run per the evidence-only brief. `git diff --check`: PASS.