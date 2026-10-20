# App refresh full 20880 classification

**Disposition: historical-compatible safety qualification only; no new refresh regression.** The one authorized central run completed against App source commit `667498cc49b4ec2b1ccd3a515eb87311c5126c93`, tree `74d6c8033b1e006e8dbd4accc361b4e1288093e`, with **18,496 passed, 2 failed, and 3 authorized expected failures** across **18,501 tests**. File accounting was **1,468 passed and 1 failed across 1,469 files**. Vitest duration was `1191.40s`; service duration was `1196s`; exit was `1`.

The active failed-node set is exactly the pre-refresh CORS subset:

- `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx` — gateway poster CORS attribute (`crossorigin` expected `anonymous`, received `null`).
- `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx` — gateway video CORS attribute (`crossorigin` expected `anonymous`, received `null`).

Compared with pre-refresh full 21209 (**18,461 passed, 3 failed, 3 expected; 1,464 files**), the refresh has **0 new failed nodes, 2 retained failed nodes, and 1 prior failed node no longer failing**. The removed failure is the old `src/shared/contexts/__tests__/AuthContext.gated.test.tsx` loading assertion: main commit `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` intentionally changed it to the deterministic two-reading/fake-timer expectation. Do not revive the abandoned boot patch or relabel this as a product regression.

Collection is fully accounted for: `1464 -> 1469` collected files and `18467 -> 18501` total tests. The source-tree test inventory is `1468 -> 1473` candidates, with the same four default exclusions (three checkout-lane files plus `astridSceneComposition.test.tsx`). The net `+5` is exactly 10 new test paths minus 5 removed source paths (one rename is neutral):

- Added: `RuntimeDocumentNormalizationGate.test.tsx`, `localAgents.test.ts`, `GlobalHeader/CreateProjectModal.test.tsx`, `RuntimeConnection/RuntimeConnectorRecoveryBanner.test.tsx` (rename destination), `SettingsModal.test.tsx`, `AstridTravelRoute.test.tsx`, `ClipInspectorActions.test.tsx`, `useClipTextOverlay.test.ts`, `clip-inspector.test.ts`, `timeline-asset-plans.test.ts`.
- Removed: `localModeUrl.test.ts`, `AstridAcpSessionControls.test.tsx`, `WorkspaceConnectionRecovery.hosted.test.tsx`, `useAstridBridgeDiscovery.test.tsx`, and the rename source `WorkspaceConnectionRecovery.test.tsx`.

There were no collection errors, unrun-file indicators, skipped/deselected indicators, unhandled-error indicators, or new expected-failure markers. The prechecks passed: `No placeholder smoke tests found`, **3 authorized expected-failure markers**, **0 forbidden markers**. The three existing expected failures remain the authorized `useClipDrag.test.tsx` cases at lines 774, 1120, and 1230; no marker changes occurred.

Causality is source-proven. `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx` and `src/shared/components/media/HoverScrubVideo.tsx` are byte-identical between baseline tree `44d514b44c864ff9dbb3b99aba2b0a41891af83f` and refresh tree `74d6c8033b1e006e8dbd4accc361b4e1288093e`; route the two retained failures to the existing shared-media CORS follow-up with the original assertions unchanged. `AuthContext.gated.test.tsx` is intentionally changed by main’s two-reading test commit, and its old failure is not a valid follow-up.

The exact central command was:

```sh
env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source \
NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
npm test -- --configLoader=runner --no-cache --maxWorkers=2
```

The explicit historical source/environment paths were verified: Agent `4a75f68f32049a69fd86135c645fa64c51175c14` (clean), Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` (clean), physical dependencies `/tmp/app-m2-coherent-deps8/node_modules`, and Composition `0.0.8` archive SHA-256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa` with 77 archive members and 77 installed files. The run log proves the deps8 path and cache-free runner. Generic moving `ext` metadata was not used for qualification.

No product, test, expectation, dependency, cache, build, browser, TypeScript, or source-environment files were changed by this classifier. This result does not qualify the current-product tuple, public-12 release, browser/e2e, renderer parity, or writer retirement. Recommended next step: route only the two retained CORS failures to the shared-media owner, preserving the original assertions; retain main’s AuthContext behavior.
