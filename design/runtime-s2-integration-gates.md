# Runtime S2 integration gates

This page records the post-merge qualification contract for the approved S2 Runtime tree.

## Exact source under test

- source commit: `f7081c14efd9a5b834987e7a1e2abf597b66313b`
- integration merge: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- source and integration tree: `7ab412cc4bcbe517efcfa806e092336390312e18`

The integration tree must remain byte-for-byte equal to the approved source tree before interpreting any test result.

## Required gates

1. `full-restore-integration` — one central full run only, with exact failure nodes classified against the prior baseline and the approved tree identity checked.
2. `commit-integration` — Runtime door commit integration tests.
3. `ts-client-check` — generated TypeScript client tests.

The central test service owns full-suite execution and serializes it machine-wide. A queued full request is not evidence of a pass or failure.

## Baseline comparison

Baseline ID: `runtime-full-restore-integration-1020095412-22308`.

Baseline counts: 5194 passed, 7 failed, 18 skipped, 25 xfailed. Baseline failures:

- `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit`
- `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty`
- `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause`
- `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll`
- `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal`
- `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait`
- `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child`

These labels are inherited only after matching the current full-run node and traceback; unrelated failures must be classified separately.

## Current result record

- full: `runtime-full-restore-integration-1020112501-27435` — fail, 7 failed / 5491 passed / 18 skipped / 24 xfailed; snapshot tree `330ea3969cb9cce77271404f31793c21abd5993f`, so non-qualifying for approved tree `7ab412cc…`
- commit: `runtime-commit-integration-1020112501-17354` — pass, 9 passed
- TypeScript: `runtime-ts-client-check-1020112501-16056` — pass, 61 passed, 0 failed

## Gate disposition

The commit and TypeScript gates pass on the approved tree. The full gate is blocked because the single permitted full request ran after `tl/integration` advanced to a different tree. Its seven exact nodes match the previous baseline and are listed in `DetailedReport.md`, but no full-pass or approved-tree failure classification is claimed.

