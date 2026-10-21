# AP2 M2 parent current proof source custody review 0358

## Verdict

**HOLD. Do not approve or run the mounted ADD proof.** The required frozen
stage0356 source packet is absent, and the actual HOME source does not satisfy
the required integrated 84ec skeleton handoff or the preserved original ADD
assertions.

## Blocking evidence

- The stage0356 worker has no report, commit message, DONE, or BLOCKED marker.
  Its worktree is unchanged at App `976e08c6c8fffd4ebb4e61e8fc1523685a330f87`,
  tree `196cb0c8c630bd21b851ce8a9d1d0e056edd9a2f`; no frozen source argument
  or harness-final SHA/tree was supplied.
- 84ec exists as
  `84ec385a463fd4907628e68e87aabbe717202a96` (tree
  `a9f1d73b0182c639a5e9403dbe61f878f8e19c16`) but is not an ancestor of the
  HOME integration ref checked during review. `git diff 84ec HOME` shows the
  four skeleton files differ. HOME `976e` retains the pre-fix behavior:
  `useAssetManagement` forwards `removeClipId` without the approved
  `isTransientUploadPlaceholder` safety predicate, and `external-drop-utils`
  unconditionally removes the local skeleton after placement.
- HOME `976e` also changes the original author0230 mounted negative from the
  required exact 404 body to `expect([404, 409]).toContain(...)`. This fails the
  explicit requirement to preserve the original 404/`not_found` assertion.
- While reviewing, HOME advanced to `1557c312b999ddc0a21c1728acbc64052ef6491f`,
  tree `cf94daef960fe1426f6f50e4000b00c0fc42867e`, which includes
  `5c53ed21f` native-bootstrap activation. That violates this task's
  nativebootstrap-dormant boundary and cannot be used as the proof source.

The durable 0323 driver is a separate approved artifact with SHA-256
`40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f`; its
closed source tuple is author0230 App `da6d910f7ab3dfc71142ece7f632d43341238882`,
tree `6809757f93ca5e166b24b8bc0160ca09005e984a`, Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`,
Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, and published014
graph/archive controls. Those guards are not valid for the un-frozen current
HOME source, and the current HOME driver still advertises stale tree
`78f3784287d78fc92677ebe5eb710d162b0f50ae` plus old Agent/Runtime metadata.

## Checks run

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — PASS.
- `NORMAL014_RECORD_DIR=<private> sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — PASS; zero-test child was refused and the evidence-first cleanup probe passed.
- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list` — PASS; exactly one case, `three-products.spec.ts:1440`.
- Existing source-only preflight against the actual current argument (`976e`/tree
  `196cb0...`) — REFUSED before source preparation by the closed parent source
  identity guard. No hosted build, browser, socket, actual gate, full suite,
  or nativebootstrap run occurred.

The prior 0323 record remains the evidence for the old frozen source's
wrong-source/pin/provenance and selector controls. It does not approve this
new current source. No source SHA/tree/driver/suite tuple is approved by this
review.

## Required next step

HOME must first merge/finalize the reviewed 84ec skeleton handoff onto a
nativebootstrap-dormant source, restore the exact original 404 body assertion,
and produce a clean frozen source argument with guards bound to that argument's
actual SHA/tree. Then a fresh independent custody review can rerun the
source-only preflight, negative controls, and exact `--list` check before any
actual authorization.
