# F-D22 independent terminal census review

## Decision

**FAIL for the submitted classification; inventory completeness PASS separately.**

The sole reviewed service is terminal **FAIL**, exit 1. The 204 failure/error
inventory and run identity are exact, but the handoff overclaims the
`profile-fixture` non-regression status and mixes 11 direct custody/process
assertion failures into `child-import-or-recipe`.

## Exact service evidence

- service: `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`
- retained run: `pytest -q -n 3`
- result: 185 failed, 16,733 passed, 4 skipped, 19 errors, 86 warnings,
  565 passed subtests; elapsed 3712.16 s; exit 1
- terminal markers: `.=16,733, F=185, E=19, s=4, u=565`; `u` is passed
  subtests, not missing outcomes
- JSON inventory: 204 unique IDs = 185 FAILED + 19 ERROR; one summary line
  has a pytest ` - ...` suffix, but JSON/traceback preserve the exact ID
- service tree/identity: Agent commit `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`,
  tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`; Runtime `3b926efab2eed122d374540baee297d4cdcec62a`;
  profile `agent-remotion-v3-819acf-1110`, archive hash beginning
  `819acf6b3815...`, composition `0.0.14`
- comparison/base is `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`; it is not the
  tested `8c355...` snapshot and is not relabelled as the run result
- raw terminal SHA-256:
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`

## Classification audit

Trace samples from every group support the bounded evidence labels for
child-probe (probe exit/child launch), fixture-declared-gap (`audio.render_source`
None against the fixture's explicit prepared-envelope gap), g5-inverse
(history/binding failures), child-import (isolated `astrid` import), D13
preflight (missing required inputs), R1 private (capture/inverse assertions),
G5 publisher/schema (helper/archive and union mismatches), R3 docs (missing
giant-file rationale), D09 probe (original wait exit 1), and R5 (Runtime's
RetiredRouteError). These are not upstream/preexisting or D14/D23 credits.

The following corrections are required:

1. Of 97 `child-import-or-recipe` IDs, 86 have the claimed runtime_protocol
   import or missing child result evidence. These 11 do not and must be split
   or remain unconfirmed:

   ```text
   tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
   tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
   tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]
   tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]
   tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]
   tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]
   tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]
   tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]
   tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]
   tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context
   tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
   ```

   Their trace shows `denied=False`, no observed process, missing shutdown
   marker files, or an unexpected `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`, not the
   group's stated import/result pattern (raw log around 2027, 13031, 13278,
   14824, 14923).

2. The 38-node `profile-fixture` non-regression assignment is unproven. Of
   those nodes, 37 show a run-local mismatch: 14 archive length 80 vs expected
   77, 9 composition `0.0.14` vs expected `0.0.13`, 11 missing
   `chunk-SE4TPVLW.js`, and 3 unmapped generated scopes. This does not prove
   pre-existing/non-product behavior. The remaining node,
   `tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root`,
   fails with `ModuleNotFoundError: runtime_protocol` and is misbucketed.

## Skips and limitations

The four skipped IDs cannot be recovered from retained artifacts. Read-only
search covered the D22 service/worker/queue logs and retained xdist/registry
paths; only the count and final summary remain. No xfail/xpass or deselection
lines remain. D14 exact-two-equal-text-anchor and D23 child-word-anchor nodes
do not occur in this log, so neither receives pass/deferred/cleared credit.

No test or service command was invoked by this review; no product/test/source
files were changed. Next step is to correct the two classification defects
and retain per-node skip output on the next authorized qualification run.
