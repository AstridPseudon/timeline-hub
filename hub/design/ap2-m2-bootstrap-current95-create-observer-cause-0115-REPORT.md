# CURRENT95 bootstrap create-observer causal repair

## Result

The first-causal failure was in the App test harness observer, not the
production project flow. The test called `harness.bridgeBase`, but
`DirectHarness` had no `bridgeBase` getter. JavaScript therefore passed
`undefined` to `isCreatedProjectResponse`; its strict URL parser failed
closed for every response, so `waitForCreatedProjectResponse` timed out at
`tests/e2e/local/support/timeline-scope.ts:100`.

The smallest correction adds the existing configured-door mapping:

```ts
get bridgeBase() { return this.doorBase.replace(/\/api\/runtime$/, '/api/astrid'); }
```

No production App source, API, DTO, store, provider, harness architecture,
Runtime source, Agent source, pin, or bootstrap activation was changed.

## Source and causal evidence

The reviewed tuple is App `ea7ee414acad6299f7d3906eb57cf9ef74a4c4b5`,
Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, and Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. The approved history conversion
`541f07f5754fd0ebc6b16767d692baba736bbdb3` and native14 source/pin remain
unchanged.

The production implementation is already the intended existing route:

- `useProjectCRUD.addNewProject` trims the submitted name and calls
  `AstridLocalClient.projects.create`.
- `AstridLocalProjectRoutes.create` sends `POST /v1/projects` through the
  existing `AstridBridgeTransport`, with JSON
  `{ name, slug, metadata }` and the existing idempotency key.
- `astridBase()` is the configured origin plus `/api/astrid`, so the exact
  browser URL is
  `<configured door origin>/api/astrid/v1/projects`.
- The existing response contract requires HTTP 201 and an envelope containing
  `data.project_id`, `data.name`, and `receipt.receipt_id`. The caller
  uses `data.project_id` to run the existing native timeline bootstrap.
- Native timeline creation then uses the separate configured Runtime route
  `/api/runtime/v1/projects/<project>/timelines`; the existing strict project,
  timeline, readback, retry/restart, history, and undo assertions remain in
  place.

The retained CURRENT95 gate result
`normal014-integration-e2e-gate5-1021011023-4657` contains one neighboring
mounted test pass and a bootstrap timeout while waiting for the matching
project-create response. Its retained sanitized scope file contains only
`beforeCreate`; it has no captured project POST URL, response status/body,
name, project scope, or receipt. I do not invent those missing current95
values and do not call the Runtime service pass qualified.

The earlier approved bridge gate advanced past the same observer to the
two-entry bootstrap history assertion, which is evidence that the real bridge
observer path is viable when supplied the configured bridge base. That older
result is not current95 qualification and is not substituted for the failed
4657 run.

## Changed exports and live callers

- Added `DirectHarness.bridgeBase` in
  `tests/e2e/local/support/harness.ts`.
- Existing callers are
  `tests/e2e/local/three-products.spec.ts:1660` and `:1664`.
- The observer helper's strict configured-origin, exact
  `/api/astrid/v1/projects`, POST, 201, submitted-name, parsed-envelope,
  project/timeline scope, readback, retry/restart, history, and undo checks
  were not weakened or filtered.

## Verification

Passed:

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts`
  — 1 test passed; existing positive and negative route/name/status/malformed
  response cases remain covered.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/three-products.spec.ts`.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit`.
- `git diff --check`.
- Offline getter probe — resolved
  `http://127.0.0.1:17340/api/astrid`.

Not run: browser, localhost/socket, Runtime service, `request-test), full
suite, old26437, first-neighbor, or bootstrap reruns.

## Next step

Review this two-line test-harness correction, then authorize one fresh
CURRENT95 bootstrap gate if desired. Keep the 4657 service result
FALSE/unqualified until that gate passes; no HOME product seam is needed
because the existing project flow is present and the failure was observer
wiring.

