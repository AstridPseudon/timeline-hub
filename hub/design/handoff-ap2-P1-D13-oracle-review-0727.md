# Handoff: ap2-P1 D13 oracle review — 2026-10-23

## Separate verdicts

- **One-field oracle: PASS.** `tl/ap2-P1-D13-oracle-and-reply-0722` at
  `1f30782236cc2e2a4be580c94e77e4ea2282f6c4` changes exactly one original
  expectation: line 375 `merge: 'atomic'` → `merge: 'fields'`. D13 requires
  App gesture saves to declare authentic consulted reads and use fields merge.
  No assertion, guard, fixture byte, wait, ID, retry, rollback, undo, or
  old-traffic behavior was weakened.
- **Integrated source identity: PASS.** App `890b9561666c3619f69335dd747b15e042b3a9a3`
  has exact tree `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`; the paired-head
  source/test/parity blobs are respectively
  `e7c12ca04da5bd064b1aef604afe5aac4992f755`,
  `ac37fb2f41c8f94e5fffbb92ac2c3a2c9d6906be`, and
  `018e44e3b0b5d2a44363aac2095b0e7a20e6b6c1`, matching reviewed 05f and fresh
  port 507. Normal vendor lock returned `ok`; exact819acf archive SHA is
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- **Original behavior: FAIL/unresolved separately.** The second case still
  dereferences `data.canonical_document` at line 479. The actual retained run
  saw it missing, but retained no public status/body. This is an unresolved
  Runtime/Agent public reply-path error; do not optional-chain, rewrite the
  success assertion, or claim source execution readiness/H3 GO.

## Authentic source boundary

`timelineLocalSaveHandoff.ts:197-254` reads the original verified selected
clip, output/fallback timing fields, referenced asset, and split collection
membership/order plus pinned-shot-group state, then emits those reads with
`merge: 'fields'`. `localSaveSession.ts:153-178` preserves the persisted
patch/step/read data and joins the full-v2 request: API version, scope, exact
base pair, commands, label, steps/patch, reads, merge, `dry_run: false`, source,
and idempotency key. `client.ts` and `dataProvider.ts` preserve accepted/merged
canonical/head/digest/receipt and the generated command effects, bindings,
dependencies, history, undo_steps, conflict, and invalid shapes.

## Checks and limits

Passed:

- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p1-chain.spec.ts` — exactly 2 tests;
- `node node_modules/typescript/bin/tsc --noEmit`;
- `node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0`;
- `git diff --check`;
- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json`.

Reused the independent 0705 PASS153/static evidence and checked the existing
private exact graph read-only (0.0.14, 80 files, no root generated files).
No product/test/ops/schema/generated/pin/lock changes were made by this
review, and diagnostics-0727 was not edited or duplicated. No browser,
HTTP/body, socket, service, build, full suite, or original P1 execution was
run. Next action is one manager-owned original two-case execution retaining
response status/body for the missing-canonical diagnosis.
