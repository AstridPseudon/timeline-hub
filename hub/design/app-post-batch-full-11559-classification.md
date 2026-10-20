# App post-batch full 11559 classification

**Disposition: historical-compatible safety qualification only.** The central run completed on the retained App source `1be0efdde` / tree `21cf7c3b` with **1,460 passed files, 4 failed files; 18,436 passed tests, 6 failed, 3 expected failures** in 1,157.71s. It is not green because the six failures are the exact M1 10022 baseline set.

The exact failed-node comparison is:

- M1 full 10022 → current 11559: **added 0, missing 0**.
- Corrected 3410 baseline → current 11559: **added 0, missing 1**; the sole missing node is the original `useAssetManagement.assetDrop.test.ts` optional-placement JSON-safe prepared-media positive. That original asset-drop failure is therefore gone.

The four failed files contain the six retained baseline nodes: two SDK example-governance nodes, two gateway-CORS nodes, hosted-auth loading, and absent-bridge proposal error-code. There are no collection failures, worker-start/unrun-file indicators, or new expected-failure markers. The run prechecks report no placeholder smoke tests, exactly 3 authorized expected-failure markers, and 0 forbidden markers. The default dot reporter does not emit per-file positive lines; the 1,460 passed + 4 failed accounting is the available file-level proof.

The current source adds three test fixtures, accounting for the corrected-baseline file count change **1,461 → 1,464**: `src/tools/video-editor/commands/runner.test.ts`, `src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx`, and `src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx`. None is a failed node; no per-file positive count is inferred beyond the full-run accounting.

The test snapshot tree `21cf7c3b47ec1fc5e6f3b65525342b8ac2899712` equals both `/home/user/work/wt/app-m2-post-batch-current-full-source` and current `/home/user/work/app` integration HEAD `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff`. The actual leased environment was Agent `4a75f68f`, Runtime `4bb1d0f7`, standard physical dependency directory `/tmp/app-m2-coherent-deps8/node_modules`, Composition `0.0.8` with the recorded 77 archive members, and the existing leases remain KEEP unchanged. The result artifact’s external Agent/Runtime/Composition hashes are snapshot metadata, not the actual environment tuple.

Central command recorded by the test service:

```sh
env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source npm test -- --maxWorkers=2
```

No local test, full retry, build, browser, TypeScript check, install, or product change was made for this classification. M2 writer work remains OPEN; the manager may resume only gated small merges. This report does not qualify the current all-product tuple or public-12 release.
