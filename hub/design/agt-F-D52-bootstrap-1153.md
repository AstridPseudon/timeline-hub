## D52 report

Read PLAN §3 R1/R2/G2, BOARD-HEADER, `commit-v2.md` §§1–5, D52 JSON276, retained full9758 tracebacks, and current source. No source or tests were executed. Worktree remains unchanged.

Current production callers are live:

- `autobootstrap.py:496–502` → `host_bootstrap.ensure_pack_host`
- `services.py:81–90` → `run_pack_host_foreground` → `ensure_pack_host`
- `generic_host.py:8462–8463` → `generic_host_worker`
- `generic_host.py:14054–14065` → startup identity attestation

No dormant/no-caller deletion boundary exists.

| # | Node | Classification | Assessment |
|---:|---|---|---|
| 1 | `test_private_child_command_preserves_entrypoint_and_original_bridge[-c]` | Authentic environment gap | Retained traceback shows `ModuleNotFoundError: runtime_protocol` before child payload execution. Test supplies Agent checkout + temp path only. |
| 2 | Same `[-m]` | Authentic environment gap | Same retained missing Runtime import; no product failure shown. |
| 3 | Same `[script]` | Authentic environment gap | Same retained missing Runtime import; no product failure shown. |
| 4 | `test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client` | Authentic environment gap | Retained traceback shows missing `runtime_protocol` in the sanitized child. The current host startup path imports it through the worker/runtime surface. |
| 5 | `test_bootstrap_passes_inventory_identity_and_restarts_on_change` | Unknown | Summary-only D52/full9758 evidence; exact exception, phase, environment, and whether `_prepare_render_validation` ran are missing. |
| 6 | `test_bootstrap_stops_on_correlated_terminal_registration_failure` | Unknown | Same: summary-only; no causal traceback or exact fixture boundary. |
| 7 | `test_startup_budget... [None-25-ready-True-25-None]` | Owner-deferred relay/provider | Retained failure occurs in Remotion registry discovery before fake host launch: provider probe exit 1, while census/custody are true. |
| 8 | `...[None-None-ready-False-300.0-None]` | Owner-deferred relay/provider | Same provider boundary and `original_wait_exit_code=1`. |
| 9 | `...[120-25-ready-True-25-None]` | Owner-deferred relay/provider | Same. |
| 10 | `...[120-None-ready-False-120-None]` | Owner-deferred relay/provider | Same. |
| 11 | `...[120-1-terminal-False-1-None]` | Owner-deferred relay/provider | Same; terminal fixture branch is not reached. |
| 12 | `...[120-1-foreign_pid-False-1-None]` | Owner-deferred relay/provider | Same; identity mismatch branch is not reached. |
| 13 | `...[120-1-foreign_birth-False-1-None]` | Owner-deferred relay/provider | Same. |
| 14 | `...[120-1-foreign_instance-False-1-None]` | Owner-deferred relay/provider | Same. |
| 15 | `...[120-1-foreign_source-False-1-None]` | Owner-deferred relay/provider | Same. |
| 16 | `...[120-None-exit-False-1-None]` | Owner-deferred relay/provider | Same; process-exit branch is not reached. |
| 17 | `...[120-400-ready-True-400-400]` | Owner-deferred relay/provider | Same; progress/reset behavior is not reached. |
| 18 | `...[120-None-ready-False-150.3-30]` | Owner-deferred relay/provider | Same. |
| 19 | `...[120-None-exit-False-1-30]` | Owner-deferred relay/provider | Same. |

The 13 retained provider failures cite `astrid/sdk/host_bootstrap.py:1654–1656` → `prepare_remotion_validation` and `remotion_runtime._require_completed_probe`. Prior environment facts identify a stale/malformed renderer profile, but the retained probe stderr and exact profile-to-failure binding are absent. Therefore this is not evidence of a bootstrap identity bug.

No row qualifies as a live product seam or faithful fixture seam, and none qualifies for dormant removal.

### Next actions

1. Child-environment owner: qualify the current Agent tree with an immutable Runtime-enabled child environment, then run the four exact nodes in rows 1–4:

```text
tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge
tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client
```

Acceptance: all variants pass with recorded child import origins and no test/source changes.

2. Renderer/provider owner: qualify the exact renderer profile and retain underlying probe stderr; run the 13 row-7–19 selectors from `tests/sdk/test_host_bootstrap_source_identity.py`.

Acceptance: provider qualification completes before the fake host launch; bootstrap identity assertions remain unchanged.

3. Evidence follow-up: rerun only rows 5–6 with full traceback retention and exact environment/profile metadata before assigning ownership or proposing deletion.

Tests run: none, as prohibited by the brief. No code, registry, package, environment, credential, or test changes made.