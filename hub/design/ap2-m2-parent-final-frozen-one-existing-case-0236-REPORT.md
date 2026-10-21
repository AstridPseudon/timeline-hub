# M2 parent final frozen existing ADD case 0236

## Result

The exact final source/helper packet was approved, and one central `--no-cache`
submission was made against the frozen author0230 source. The mounted ADD case
did not execute. The run failed before a test case with:

```text
Error: No tests found
normal014 Playwright child exit: 1
```

The source-bound Playwright listing immediately before the build showed the
intended existing case:

```text
three-products.spec.ts:1440:1 › M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
Total: 1 test in 1 file
```

The central result was `exit=1` after 65 seconds. It produced no case
summary, no first request packet, and no mounted ADD result. Therefore there is
no evidence for valid ADD, lost ACK, restart/recovery, exact retry, reload,
undo, opaque-data preservation, or `wire.legacy === []`. No writer retirement
or deletion is qualified.

## Exact source and approval

The central target was the frozen author0230 branch
`ap2-m2-parent-exact-negative-source-finish-0230`:

- commit `da6d910f7ab3dfc71142ece7f632d43341238882`
- tree `6809757f93ca5e166b24b8bc0160ca09005e984a`
- parent `7e85d89120227f336a2e8dbf8e0ea44d98311da0`

The independent custody review approved this exact source and helper packet.
It verified the exact HTTP `404`, `not_found` code, pinned refusal message, and
retention of the original ADD/recovery/retry/reload/undo/opaque/zero-legacy
assertions. Approved helper hashes were:

```text
normal014-source-common.sh        3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014
normal014-parent-media-central.sh 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
normal014-app-central.sh          8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e
```

The source-only preflight and identity negatives passed before submission:
exact ancestry/tree/clean state, four App pins, Agent `6efc8150`, Runtime and
producer `95bd3c5f`, artifacts/schema/imports, public13 graph, and producer
HEAD. The bootstrap selector remained unchanged at
`dfdbef10f9d8ccf1a630f000cd076023918ead8a` / tree
`33674ef4bbaa4b043baed77492621095cccc28f7`.

## Commands and results

- `sh -n` on the three normal014 helpers and committed driver — PASS (custody
  review).
- Source-only exact-parent preflight — PASS (custody review).
- Source identity negatives for wrong selector/tree, missing provenance, dirty
  source, and wrong runtime pin — PASS/refused (custody review).
- `request-test ap2-m2-parent-exact-negative-source-finish-0230 ap2-m2-parent-final-frozen-existing-add-0236 --no-cache` — submitted exactly once.
- `wait-test ... 10` — completed with central result `exit=1`; hosted build
  completed, then the Playwright child reported `No tests found`.

The one named suite was registered as a direct command from the frozen source:

```text
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

No wrapper, local browser, local full suite, install, retry, or HTTP swap
replay was used. The existing driver was the actual command from the approved
source. The failure evidence is retained by the central run under its result
directory, including the runner log and result summary.

## Live callers

The existing prepared-ADD chain remains live:

`handleFileDrop` / `dispatchTimelineDrop` → `useExternalDrop.ts` and
`external-drop-utils.ts` → `useAssetManagement.ts` (`commands.addClip`) →
`useTimelineState.ts` / `parentMediaCommands` →
`useTimelineCommandsService.ts` → `commitSession.ts` and
`useTimelineCommandSession.ts` outbox/commit plumbing.

The source packet's helper callers remain
`normal014-parent-media-central.sh`, `normal014-app-central.sh`, and the
committed `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`.

## Decision and next step

I registered the direct source-bound suite because the older retained-evidence
suite points at a stale wrapper/source identity. The central run's pre-case
`No tests found` result is the first and only mounted-run evidence. Do not
retry in this task; diagnose the source driver's case-selection mismatch in a
new review/task, then obtain a fresh custody approval before another mounted
run. Keep all legacy writers and callers unchanged until the full original
ADD/recovery/undo/zero-legacy body passes.
