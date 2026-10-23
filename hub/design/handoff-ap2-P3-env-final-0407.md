# P3 environment final handoff

Status: **READY for the App resolver owner; Gate 5 remains unqualified.**

The existing `ap2-P3-gate5-h6-0348` suite row was updated to use the durable graph at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`

The exact original Gate 5 selector is retained once. The graph uses the existing `prepareNodeModulesOverlay` helper, the locked Composition archive `0.0.14`, 73,451 bytes, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. Its 80 regular files match the archive byte-for-byte. Normal dependencies remain shared-install links; `vite` and `rollup` are helper-owned physical copies. No package-root generated-module links, package-root `typescript`, source fallback links, repack, pin, upgrade, or shared `node_modules` mutation was used.

Node imports passed through the archive exports and resolved to `dist/index.js`, `dist/effects.generated.js`, `dist/animations.generated.js`, and `dist/transitions.generated.js`. The selector collected exactly one test without starting a browser or service.

Source preflight is exact and clean:

- App `206d5f30c22b68975d94942430278a581140a0a`
- Agent `/home/user/work/agent` `f894c3c9dda25ab03527eeb7f52da5da31d627c1`
- Runtime `/home/user/work/wt/rt-pin-34eac004` `34eac0041b0891e9011966b39bcbd26053fde5bc`
- Both bundle SHA environment values matched those actual heads.
- Runtime lookup found `/home/user/work/wt/rt-pin-34eac004/.venv/bin/python`, resolving to `/usr/bin/python3.12`; both explicit interpreter variables use `/home/user/work/venv-app2-native/bin/python` and resolve to the same interpreter.

The exact-graph Vite diagnostic reproduced the current App source failure: the string package-root alias intercepts the official `effects.generated`, `animations.generated`, and `transitions.generated` subpaths and yields `noResolved` root paths. The archive’s official exports point to `dist/*.js`. App owns the minimal resolver correction. This handoff does not qualify the browser/body journey.

See the worker [report](../workers/ap2-P3-env-final-0407/report.md) and durable [graph manifest](../workers/ap2-P3-env-final-0407/record/graph-manifest.json).
