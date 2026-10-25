# F/D134 independent host14 review

## Verdict

`PASS_SOURCE_ASSESSMENT`; `FAIL_FINAL_PROOF`. The retained 18455 log supports one
finite current boundary for all 14 REG14 IDs, but the final proof remains failed:
the actual XML, raw runner receipt, and complete disk witness are unavailable.
There is no ship, custody, release, or retirement credit.

## Finite actual diagnosis

The exact 18455 launcher recipe exports `PYTHONNOUSERSITE=1` and, through the
pinned D73 launcher, `ASTRID_REMOTION_PROJECT_DIR` for the pinned profile. The
unchanged source copies the environment into `_host_render_environment`, reaches
`_prepare_render_validation` from `ensure_pack_host`, and takes the Remotion
validation path because the project directory is present. The unchanged
`_registry_context` calls `probe_context`; its `_UNSUPPORTED_PYTHON_STARTUP`
set contains `PYTHONNOUSERSITE`, and `probe_context` raises
`RemotionValidationError` at line 236.

The retained actual log contains all 14 exact REG14 IDs. Every one is `FAILED`
with the same exception and the same stack boundary:

`host_bootstrap.py:1651 -> host_bootstrap.py:836 -> remotion_runtime.py:445 -> probe_context:236`

The full traceback also consistently passes through the Remotion preparation
helpers at lines 1095, 902, 922, and 831. The 14 `registry_settle` and 14
`launch_transaction` diagnostics are consistent with rejection before the
mocked host `popen`/Runtime child path. The separate first host-bootstrap extra
node has the same retained exception boundary but remains UNKNOWN and is not
folded into REG14.

This proves the current measurement environment cause at the pre-launch
boundary. It does not prove a product regression: the relevant host-bootstrap,
Remotion-runtime, and exact test blobs are byte-identical between current Agent
`a4e016b6` and bounded candidate `96df3f5b`.

The retained preflight also reports the expected Agent, Runtime protocol,
client, schema, and shared-schema origins with no contrary live root. That is a
tuple control only: the Runtime child is not reached at this boundary.

## Baseline limitation

The authentic bounded 1345 packet is 14/14 PASS with `PYTHONNOUSERSITE=1`, but
its complete shell environment is absent. Its retained source behavior shows
that missing `ASTRID_REMOTION_PROJECT_DIR` returns before strict validation;
the current launcher definitely supplies that variable. Therefore the current
environment cause is proved, while the exact raw 1345-vs-current environment
difference remains unproved. The independent pristine 26621 14/14 PASS is
retained evidence only and does not close current REG14.

## Classification bounds

The independent 1937 packet recomputes exactly 370 unique bad IDs:

- 344 `OURS_NEW_FILE` (absent at named `08e6b905`),
- 14 exact prior REG14 IDs (all current `FAILED`),
- 12 `UNKNOWN` (one separate first host-bootstrap node plus 11 others).

The equation is `190 failed + 180 errors = 370`, and the partition is
`344 + 14 + 12 = 370`. Status matches against baseline/upstream are not causal
proof. `core_open_n=UNKNOWN`, `reg_open_n=UNKNOWN`, `reg14_closed=false`, and
retirement remains zero.

## Minimal next scope

The next owner is the D73/full-measurement environment contract: reconcile the
Remotion-enabled full launcher with the validated bounded host path and retain a
complete prior-vs-current environment receipt. No Agent product edit is
justified by this evidence. A future result may not use the bounded PASS to
invent the missing environment or to relabel the current full run as PASS.
