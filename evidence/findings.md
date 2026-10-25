# F/D134 whole-path findings

## Finite boundary

The first retained host-bootstrap failure in 18455 is the unknown extra node
`test_bootstrap_passes_inventory_identity_and_restarts_on_change`; the first
REG14 node immediately after it is
`test_bootstrap_stops_on_correlated_terminal_registration_failure`. Both reach
the same exception. The stack is:

`ensure_pack_host` (`astrid/sdk/host_bootstrap.py:1651`) →
`_prepare_render_validation` (`:836`) → `_registry_context`
(`astrid/core/rendering/remotion_runtime.py:445`) → `probe_context` (`:236`).

`probe_context` rejects `PYTHONNOUSERSITE`, which the retained D73 launcher
exports as `1`. The launcher also exports `ASTRID_REMOTION_PROJECT_DIR`, so the
host path does not take the no-Remotion early return. The retained failure is
before the mocked `popen` call and before any Runtime child/module execution.
This is one proven common boundary for all 14 REG14 IDs.

The current host bootstrap, Remotion runtime, and exact host-test blobs are
identical between Agent `a4e016b6` and bounded candidate `96df3f5b`. The full
run therefore does not prove a product regression in those files. The current
tuple’s Runtime and schema/module origin receipts are valid preflight controls,
but Runtime is not reached at the REG14 first failure.

## Why bounded PASS differs

The bounded 1345 packet has a durable 14/14 PASS XML and records
`PYTHONNOUSERSITE=1`, but its complete command/environment receipt is absent.
The source itself makes the branch condition explicit: with no
`ASTRID_REMOTION_PROJECT_DIR`, `_prepare_render_validation` returns before the
strict probe; with that variable present, the same unchanged source reaches the
probe and rejects `PYTHONNOUSERSITE`. The current full launcher definitely sets
that variable. Thus the current failure is an environment/launcher-path
difference, while the exact absence of the variable in the prior PASS remains
EXACTMISSING rather than a claimed raw receipt.

Pristine 26621 is independently 14/14 PASS and is not used to close current
REG14. The extra host-bootstrap node and the other 11 UNKNOWN IDs remain
separate; no REG0/core closure is manufactured.

## Ownership

The proved next scope is the measurement/D73 launch environment contract:
reconcile the full launcher’s Remotion-enabled environment with the validated
host path and retain a complete prior-vs-current environment receipt. No Agent
product edit is justified by this read-only evidence.
