# PASS — ap2-P1-diagnostic-port-review-0607

Reviewed current App port `f98a5060e9a836245eaaaebb3b124da671e93dc8` against exact base `cffa91c93e80717cec1a4e740fae67140394eb88`.

## Exact identity and scope

- Target parent is the exact base.
- Base-to-target diff: exactly one file, `tests/e2e/local/three-products.p1-chain.spec.ts`.
- Donor: commit `cc05d7de25d4842964d3a4e5d5ff792f53294e0e`; donor file blob `4f0e7a97e67051ccd5c587f7e9ea6c3ae70f9cf2`.
- Target file blob and working-tree blob both equal `4f0e7a97e67051ccd5c587f7e9ea6c3ae70f9cf2`; SHA-256 is `956aaf219aae927d23a4f13e0ce8b0e358fe235508454fe70b0c6ad6ed84eb8c`.
- Both original P1 test bodies are byte-for-byte unchanged from the donor parent, including goto/connected/track/90-second idle-owner wait/catch-rethrow and the accepted/merged/refused, lost-ACK/restart, new-ID, guard, raw, opaque, order, rollback, history, and inverse assertions.
- Diagnostic capture is restricted to the donor-reviewed structural allowlist: bounded records, counts/booleans, fixed enums, and templated routes. No arbitrary data, auth, keys, product/support/fixture/schema/generated/client-pin/lock/suite/launcher changes, or report ancestry was imported.

## Commands and results

1. `env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144 npm run test:e2e:three-products -- --list tests/e2e/local/three-products.p1-chain.spec.ts` — PASS; exact 2 tests in 1 file.
2. `env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144 npm exec tsc -- --noEmit` — PASS.
3. `env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144 npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS.
4. `git diff --check cffa91c93e80717cec1a4e740fae67140394eb88..HEAD && git diff --check` — PASS.
5. Scope/hash assertions — PASS: one path only; exact donor blob and clean worktree hash.

## Limitation / next step

No browser/runtime E2E was launched: the existing original two-case service on port 19451 was instructed to remain untouched, with no suite/hash/input change and no duplicate body. This handoff is source/static PASS only and gives no integrated behavior or H3 credit. On PASS, manager action is limited to `git log currentintegration..worker` showing the worker's own commit, followed by the remote App merge.

