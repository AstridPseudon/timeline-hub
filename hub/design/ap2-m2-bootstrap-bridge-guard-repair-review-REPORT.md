# AP2-M2 bootstrap bridge guard repair review

## Verdict

**APPROVE the exact test-local repair delta for one authorized live gate.**
This is source/custody approval only; it is not live browser qualification.

Reviewed `fca9317a0` + `29bbee362` (`tl/ap2-m2-bootstrap-real-bridge-source-guard-fix`)
against the common source point and `hub/tl/integration`.

## Source proof

- `DirectHarness.bridgeBase` is derived from the existing `doorBase`; it keeps
  the configured door host/port and substitutes only `/api/runtime` with its
  sibling `/api/astrid`. No origin or port is guessed independently.
- `waitForCreatedProjectResponse(...)` is constructed before the
  `Create Project` click.
- The predicate requires the configured bridge origin, exact
  `/api/astrid/v1/projects` path, no query/hash, `POST`, HTTP `201`, and the
  parsed request name equal to `submittedName.trim()`.
- `readCreatedProjectResponse(...)` refuses malformed/non-object envelopes and
  requires `data.project_id` to be a string, exact trimmed `data.name`, and a
  string `receipt.receipt_id` before the journey uses the project ID.
- Controls explicitly refuse wrong origin, same-origin `/api/runtime` lookalike,
  `GET`, wrong name/status, malformed request JSON, and a missing
  `data`/`receipt` envelope.
- The exact URL, realm/project/timeline equality, project readback, reservation
  and outbox scope, selected-timeline lookup, lifecycle ordering, retry,
  reload/restart, inverse, opaque-data, and zero-legacy assertions remain in
  place. No latest/list/status fallback was introduced.

## Scope and wrapper custody

The branch commit range changes exactly these four test-local files:

```text
tests/e2e/local/support/harness.ts
tests/e2e/local/support/timeline-scope.ts
tests/e2e/local/support/timeline-scope.test.ts
tests/e2e/local/three-products.spec.ts
```

No product/provider/schema/DTO/pin/dependency path changes are present. The
merge-tree check is clean. The candidate branch snapshot predates the current
base's selected-credential harness commit (`50797493e`), so the live wrapper
must apply only the repair delta onto current `hub/tl/integration`; it must not
copy the stale branch snapshot over current harness behavior.

Branch-file SHA-256 values:

```text
db4888ac5ceb12a1818f1a79efb7a2f41d56ba7b1c73b6cbfcf4bb2f0494500c  tests/e2e/local/support/harness.ts
9d37e73bd9b5fad18d93527ec9e7e1a9ff034d5b7f997472d64eb2fb214b5666  tests/e2e/local/support/timeline-scope.ts
e7506092720060b1982e3b1233061a822fdcc3a760969840cb8efb0eb3be92d6  tests/e2e/local/support/timeline-scope.test.ts
825b6940aff8f759256b2c55227776b71c3471eb66e4b4f36fb25fc956aaeee8  tests/e2e/local/three-products.spec.ts
```

For a wrapper based on current integration, the effective harness hash after
preserving current selected-credential code and adding only `bridgeBase` is
`a4f478dd30b4725e76b9784b74c34fc555ccc8c190003b8651a0a4ff2f15d254`; the
other three effective hashes are the values above. The wrapper should prove
the exact test path plus one unique bootstrap selection before the hosted
build, and run only that one live gate.

## Evidence

Already recorded on the candidate:

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — **PASS**.
- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.spec.ts` — **PASS**.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit` — **PASS**.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts` — **PASS**, 12 tests listed and exactly one bootstrap consumer test.
- `git diff --check` — **PASS**.
- Static review of the four-file range and focused refusal controls — **PASS**.

No browser, localhost/live-socket, `request-test`, or full suite was run for
this review, as required. The one authorized live gate remains unverified.
