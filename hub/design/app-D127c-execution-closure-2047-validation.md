# D127c validation

## Independent read-only verification

- `git rev-parse HEAD HEAD^{tree}` — PASS: `fd586440a626fc49a35a9dd0ac7e838d5fe55a4b` / `6d2744e271f016206854ab33f57b3cfc737ad54d`.
- `sha256sum tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — PASS: `59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`.
- `git status --short --branch`, `git diff --check`, and `git diff --quiet` — PASS: clean worktree and no diff.
- `git -C /home/user/banodoco/banodoco-workspace-runtime rev-parse fb4addba95ca4bae0482c93be94e5cae2770ca09^{tree}` plus read-only helper hash — PASS: tree `8d5683702f36034f27ee7f49737665d66dbc2b75`, helper `095c252b…`.
- Supported Node20 `--version` and binary hash — PASS: `v20.19.4`, SHA-256 `43d6cf63…`.
- Real dependency origins — PASS: `node_modules` resolves to `/home/user/work/app/node_modules`; TSX `4.21.0`, TSX CJS API SHA-256 `b396a280…`, esbuild `0.27.7`.
- Source scan for assertion mutation — PASS: only imports of `node:assert/strict`; no `assert.ok`/`assert.throws` reassignment, spy, or mock.

## Qualifying prior execution

The exact recorded command is in the permanent Sol packet `app-D127c-Node20-loader-sol-2033/evidence/commands-results.md`. It ran the exact Node20.19.4 binary with `--test --test-concurrency=1`, the three full intended names, TAP plus the custom event reporter, and the worker-owned `cjs-api-controls.cjs` entry. The entry used `tsx/cjs/api` `require(source, __filename)` against the original `.test.ts` after checking its exact hash and a genuine 5GB local floor.

Result: exit 0 in 1.38s, intended 3 PASS / 0 FAIL / 0 intended SKIP. The final stdout and event stream show the three exact named `test:pass` events. `check-events.py` exited 0 and independently required those exact names, no skip flag, no failures, exactly four nonmatching skip events, and matching entry/reporter hashes.

The whole-file result is intentionally not collapsed to zero skips: 7 registered tests, 3 pass, 0 fail, 4 ordinary name-filter skips. The four nonmatches are targeted-selection events, not weakened tests or credited successes.

## Non-credit evidence and exclusions

Outside service `app-D127c-Node20-loader-sol-2033-d127c-node20-cjs-controls-2033-1025204001-13179` exited 1 at its 5GB snapshot guard before loading original source. It has zero success credit and was not repeated. Review2013's prior Node20 zero-node/timeout evidence remains preserved. Node22 supplemental passes and Runtime `30318` are corroboration only, not substitutes for the qualifying Node20 execution. No live/bootstrap/socket/browser/profile/native/full/tour test was run, and no Runtime or source retest was needed.
