# M2 parent final frozen code custody review 0236

## Verdict

APPROVE the exact committed source and helper packet. No source correction is
needed.

Final App source:

- commit: `da6d910f7ab3dfc71142ece7f632d43341238882`
- tree: `6809757f93ca5e166b24b8bc0160ca09005e984a`
- parent: `7e85d89120227f336a2e8dbf8e0ea44d98311da0`
- subject: `test(app): assert exact parent media refusal`

The committed source was read with `git show` from the final commit after the
source worktree had been removed. The final diff changes only:

- `tests/e2e/local/three-products.spec.ts`: the wrong verified-selection
  response is exactly HTTP `404`, code `not_found`, and message
  `selected media is not a managed project generation/variant/object`.
- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`: the existing
  driver now binds the final source through the closed helper and keeps the
  existing ancestry anchor `7e85d89120227f336a2e8dbf8e0ea44d98311da0`.

The original parent ADD body is retained: valid media import `201`, selected
five-field media identity, verified selection `200`, native `clip.add-media`,
lost-ACK exact retry, dependent edit retention, reload, Runtime restart,
recovery, guarded undo, opaque-data preservation, and `wire.legacy` empty
assertions. `git diff --check da6d910f^ da6d910f` passed and showed no removed
assertions in this test body. Bootstrap remains the unchanged selector
`dfdbef10f9d8ccf1a630f000cd076023918ead8a` / tree
`33674ef4bbaa4b043baed77492621095cccc28f7`.

## Closed custody

The final95 parent selector in `normal014-source-common.sh` is exactly:

```text
APP_ROOT_SHA=da6d910f7ab3dfc71142ece7f632d43341238882
APP_ROOT_TREE=6809757f93ca5e166b24b8bc0160ca09005e984a
```

The existing closed guards remain in force: final source ancestry, exact tree,
clean state, four App pin bytes, Agent and Runtime trees, artifact/manifest and
schema equality, imports and collection, locked public13 graph, and producer
HEAD. Frozen producer identities observed directly:

- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime and producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.

Helper SHA-256 values approved:

```text
normal014-source-common.sh        3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014
normal014-parent-media-central.sh 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
normal014-app-central.sh          8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e
```

Live callers are the existing `normal014-parent-media-central.sh`,
`normal014-app-central.sh`, and the committed
`run-parent-manual-drop-evidence.sh` driver. The suite registration remains
the existing `normal014-integration-parent-media-accepted` command in
`scratchpad/orch/tests/suites.conf`.

## Evidence run

All commands were source-only; no browser, socket, full suite, or actual gate
was run.

- Exact existing command, against a private checkout of the final commit:
  `NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 NORMAL014_RUN_ROOT="$ROOT/run" bash /tmp/.../design/normal014-parent-media-central.sh preflight "$ROOT/app"`
  — PASS. It verified 76 artifacts, manifest
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, schema
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, the
  native parent replacement collection, and cleaned its run root.
- Identity negatives — PASS/refused: wrong source selector, wrong current
  integration tree, missing Git provenance, dirty final source, and tampered
  `runtime.lock.json` pin.
- `sh -n` for both final committed driver bytes and all three normal014 helper
  scripts — PASS.
- Final source ancestry check and `git diff --check` — PASS.

The earlier stale review cause is confirmed: it inspected provisional source
while the helper still expected tree `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`.
That is now closed by the committed `da6d910f` / `6809757f` selector.

## Next step

The packet is ready for the separately authorized existing parent mounted ADD
gate. This review does not qualify that browser/Runtime gate or authorize a
writer deletion.
