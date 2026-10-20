# App post-shot full 21209 classification

**Disposition: historical-compatible safety qualification only.** The central run completed against App `18becfbede00038830b97e63345445eeef54fa42` / tree `44d514b44c864ff9dbb3b99aba2b0a41891af83f` with **18,461 passed, 3 failed, and 3 authorized expected failures** across **18,467 tests**. File accounting was **1,462 passed and 2 failed across all 1,464 files**. Vitest duration was **1,180.36s**; the service wall duration was **1,185s**.

The active failed-node set is exactly the expected current three-node set:

- `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx` — gateway poster CORS attribute
- `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx` — gateway video CORS attribute
- `src/shared/contexts/__tests__/AuthContext.gated.test.tsx` — hosted auth loading state

Compared with the accepted historical six-node 11559 result, **added 0, missing 3**: the two SDK example-governance nodes and the ACP absent-bridge proposal node are gone. The remaining three are expected because the active source delta does not modify the gateway or hosted-auth implementation/tests, while the ACP fixture now supplies the `/events` response and the transcript example now imports and uses `PanelFrameAnchor` and `PanelPreviewService`. There are **0 new regressions** after complete execution.

The run had **3 authorized expected-failure markers and 0 forbidden markers**, no placeholder smoke tests, no collection failures, no unhandled errors, and no worker-failure or unrun-file indicators. The terminal accounting covers all 1,464 files (`1,462 + 2`) and all 18,467 tests (`18,461 + 3 + 3`).

The exact central command was:

```sh
env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source \
NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
npm test -- --configLoader=runner --no-cache --maxWorkers=2
```

Actual environment evidence is Agent `4a75f68f32049a69fd86135c645fa64c51175c14`, Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`, physical dependencies `/tmp/app-m2-coherent-deps8/node_modules`, and Composition `0.0.8` with the recorded 77 archive members (SHA-256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`). The active log proves the deps8 path and `--no-cache` runner; the `ext` file's generic Agent/Runtime/Composition HEADs are not used as the actual product tuple.

The result snapshot tree is `44d514b44c864ff9dbb3b99aba2b0a41891af83f`, equal to the active source checkout and this clean classifier checkout. No source, dependency, cache, browser, build, TypeScript, or test files were changed by this classification. The active result artifacts are `request`, `snap`, `ext`, `log.txt`, `summary`, and `exit`; `summary`/terminal log are authoritative and `exit` is `1` because the retained three failures remain.

This result preserves the historical six-node 11559 result; it does not relabel that run and does not qualify the all-product tuple or public-12 release. M2 writer work remains open.
