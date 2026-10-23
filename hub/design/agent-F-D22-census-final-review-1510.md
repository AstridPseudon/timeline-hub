# F-D22 final census-return review

## Decision

**FAIL for the return artifact; PASS separately for the corrected
classification and exact terminal inventory.**

The retained service is `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`,
terminal FAIL, exit 1, with 185 failed, 19 errors, 16,733 passed, 4 skipped,
565 passed subtests, 86 warnings, and elapsed 3712.16 s. Preserved identity is
Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, Runtime
`3b926efab2eed122d374540baee297d4cdcec62a`, profile archive
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, and raw
terminal SHA-256
`e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.

## Inventory and classification PASS findings

The corrected JSON contains 204 unique entries. Exact groups are:

| group | count |
|---|---:|
| child-probe | 17 |
| child-import-or-recipe | 87 |
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

The 11 direct custody/process IDs are correctly split from the former
97-node environment group and remain source-backed but **unconfirmed**:

1. `tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]`
2. `tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]`
3. `tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]`
4. `tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]`
5. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]`
6. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]`
7. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]`
8. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]`
9. `tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]`
10. `tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context`
11. `tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]`

Trace/source samples cover all changed custody causes: denied=False and
engine_fd mismatch at raw 1972–2087 (`custody_broker.py:child_exec_from_environment`);
empty observation at 12988–13083 (`generic_host.py` review cancellation);
absent shutdown markers at 13084–13332 (`GenericPackHost.run_task`,
`shutdown`, `_ManagedTaskAdapter`, `process_group.py:verify_tree_absent`); and
unexpected `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` at 14790–14924
(`_child_environment`, `_launch_worker_probe_environments`,
`_run_command_definition`, `remotion_runtime.py:_registry_context`).

The Remotion node
`tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root`
is correctly moved from profile to environment, with source
`tests/packs/rendering/test_remotion_backend.py:672–700`, raw traceback
14927–14960, summary line 22648, and `ModuleNotFoundError: runtime_protocol`.
The remaining 37 profile nodes correctly remain **unconfirmed causal
profile/oracle mismatches**: archive 80-vs-77 (14), composition 0.0.14-vs-0.0.13
(9), missing `chunk-SE4TPVLW.js` (11), and unmapped generated scopes (3).

Guardrails are preserved: four skip IDs unavailable; xfail/xpass and
deselection zero; D14/D23 unexercised; Base583 distinct from actual 8c355;
no upstream, pre-existing, deferred, or PASS credit added.

## FAIL findings in the return artifact

1. The moved Remotion entry in the corrected JSON contains
   `raw-terminal.log:2252x`, which is not its raw failure window. The correct
   window is 14927–14960, with summary line 22648. The flat handoff is correct,
   but the JSON evidence is not exact.
2. The return reused and overwrote the original
   `agent-F-D22-terminal-classify-1442-e0036c850d1a7b7c.json` path. There is no
   separately named return JSON with a new content hash, so the completed-1442
   artifact is not independently retained.

The corrected JSON’s current SHA-256 is
`cc8b7d96dadaa6f9022a064fcd5a5db3d72f008b1565afc1f63c72e4adbcc397`.

## Checks

No tests, type checks, lint, provisioning, environment qualification, or full
suite were run. Read-only checks only:

- Python JSON/raw/source audit: **PASS** — entries 204, unique 204, group sum
  204, all 11 custody IDs and the moved ID present in JSON/flat/raw, identity
  and guardrails match.
- `sha256sum` of raw log: **PASS** with the preserved e0036…c60a5 hash.
- `git diff --check`: **PASS**; no product/test/schema/pin/dependency changes.

Recommended repair is documentation-only: preserve the original 1442 JSON,
write a distinct return JSON named with its new content hash, correct `2252x`,
and rerun the static audit.
