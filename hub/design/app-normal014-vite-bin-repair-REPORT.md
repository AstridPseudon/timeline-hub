# App normal014 Vite bin repair

## Change

Updated `normal014-source-common.sh` and `normal014-app-central.sh` in this
private harness only. Each run now builds a private `node_modules` graph whose
package directories point read-only at the locked graph, while `.bin` is
created in the run root from installed package `bin` declarations. The locked
graph and its archive are never written. The App runner now runs the actual
`npm run build:hosted` before Playwright, with disposable npm/Vite cache and
build-output paths.

Exact source guards remain: Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`,
Runtime `202074110717146fc7f08af2306a8dd7f695b0b1`, producer
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, artifact manifest 75 entries
`ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`, shared
schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
and the existing locked graph/archive and Composition hashes.

## Checks

- `sh -n .../normal014-source-common.sh .../normal014-app-central.sh .../normal014-parent-media-central.sh` — PASS.
- Private bin check against the locked graph — PASS: `vite 5.4.21`, `tsc 5.9.3`, Playwright `1.60.0`; source archive hash and read-only permissions unchanged.
- Exact-checkout local private `npm run build:hosted` — PASS: 5,569 modules transformed and hosted origin emitted in disposable `dist`.
- Full App preflight wrapper was not claimable locally because the sandbox could not resolve the package index for its disposable Python venv (`Could not find a version that satisfies jsonschema>=4.18`); the central runner had the required Python setup.

## Central result

Requested exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app normal014-integration-e2e-gate5
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-normal014-integration-e2e-gate5-1020174558-6901
```

Result `app-normal014-integration-e2e-gate5-1020174558-6901`, App tree
`48c40d05662e837c5d2acd802725d65a8816a03d`, duration 204s: **1 failed**.
The PRE-browser build passed (`vite` resolved; build completed in 1m18s), and
the journey logged the exact Agent/Runtime tuple and matching wire/schema
digests. The one failure was
`tests/e2e/local/three-products.spec.ts:1017` (`M2 real gate 5`): after the
hosted page mounted, `openCommandTimeline` timed out after 90s waiting for the
durable command owner (`ready: false`). This is classified as a remaining
App journey/product block after environment repair, not a Vite/bin failure.

Parent PASS1 was not rerun. No package install, shared dependency/cache write,
pin/release/activation, source mutation, browser run locally, or test
weakening was performed.
