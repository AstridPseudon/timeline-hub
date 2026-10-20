# App M2 current registered parent-delete executor

Result: blocked on actual product failures. The required new literal source-specific central suite was registered and executed against the completed integrated-root candidate. No feature edits or test weakening were made.

## Central execution

- Suite: `e2e-parent-delete-treea3ea8023-agent8130-runtime2c4-e2e-integration`
- Central TestID: `app-m2-delete-current-registered-executor-e2e-parent-delete-treea3ea8023-agent8130-runtime2c4-e2e-integration-1020152405-7378`
- Command: `node scripts/testing/current013-parent-delete.mjs`
- Result: exit 1; `2 failed`; fresh hosted build passed in 1m36s; Playwright discovered exactly 2 tests and ran them with 1 worker.
- Browser: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, Chromium `141.0.7390.37`.
- Public browser/direct-dist inputs were unset (`ASTRID_PUBLIC_CHECKOUT`, `ASTRID_APP_DIRECT_DIST`).

Case results:

1. `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip` (`tests/e2e/local/clip-delete-command.spec.ts:171`), artifact ID `clip-delete-command-M2-cur-9193a-rse-restore-raw-opaque-clip`: failed at the first accepted commit receipt assertion. Expected `receipt.receipt_id` `eeb52a6f-6c82-4baf-8609-965fb94815be`, received request key `txn-37aea606741a40d287324637025fd4b9`.
2. `M2 current013 parent DELETE conflict: same-property Agent move wins while the original delete request is held and draft is retained` (`tests/e2e/local/clip-delete-command.spec.ts:352`), artifact ID `clip-delete-command-M2-cur-42d5f--held-and-draft-is-retained`: failed at retained outbox equality (`:392`). The received outbox included `{ kind: "conflict", message: "conflict: original authored guard changed" }`, while the test expected the original intents/pending request unchanged.

The central launcher completed its postflight source checks. Because the first actual product errors occurred, raw deletion/mirror/registry/opaque/closure preservation, reload/inverse, durable lost-ACK/restart/exact-retry, and zero-legacy-write qualification are not claimed.

## Source tuple and guards

- App: commit `b91aa0c16cc9817b8078fdfe11c7bfca95853a52`, tree `a3ea802324e3d269c474046fe71526e99fea5228`
- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime and producer peer: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Public Composition: archive `banodoco-timeline-composition-0.0.12.tgz`, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, exactly 77 regular files
- Runtime manifest: exactly 75 artifacts; Runtime lock, peer/source cleanliness, generated metadata, schema/component digests, and both source Composition archives passed.
- Cache identity: `parent-delete-treea3ea802324e3d269c474046fe71526e99fea5228-agent8130a401bf44a518d5a40ae274d398b8c560be55-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnera71c71b3613f34d4b382a73959bf798271c7d646c380c011f1725a217e399bc7-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`

## Local controls

- `node --experimental-vm-modules --test scripts/testing/current013-parent-delete.test.mjs scripts/testing/current013-integration.test.mjs` — 2 file subtests passed.
- Exact source preflight via `readCurrent013Inputs` + `checkCurrent013Sources` — passed, including full-SHA, source cleanliness, Runtime lock/producer peer, 75-artifact manifest, 77-file archive, metadata, and vendor-lock checks.
- Chromium version probe — `Chromium 141.0.7390.37`.

## Blocker and next step

The candidate cannot be qualified until the product/contract owner resolves the receipt identity mismatch in the success path and the retained-outbox conflict-state mismatch in the same-property 409 path. Re-run this exact central suite after that resolution; do not reuse the obsolete tree7b86/d874 suite.
