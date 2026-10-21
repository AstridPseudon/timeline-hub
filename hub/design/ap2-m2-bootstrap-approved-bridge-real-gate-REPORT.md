# AP2-M2 bootstrap approved bridge real gate

## Result

Ported the approved bridge source-guard repair onto current `hub/tl/integration`
with exactly four test-local files changed. The current selected-credential
helper was retained; no stale full harness/spec was copied.

The one authorized central bootstrap gate was run once with `--no-cache` and
is **NOT QUALIFIED**. The bridge observer and strict project scope checks were
reached, but the existing bootstrap history assertion failed:

```text
expected bootstrapHistory.items length: 1
received: 2
failure: tests/e2e/local/three-products.spec.ts:1496
```

The two retained history entries were a bootstrap
`parent_composition.publish` entry followed by the recorded `timeline.commit`
entry. This worker did not weaken or rewrite that assertion and did not retry
the unchanged gate.

## Source/custody proof

Changed paths only:

```text
tests/e2e/local/support/harness.ts
tests/e2e/local/support/timeline-scope.ts
tests/e2e/local/support/timeline-scope.test.ts
tests/e2e/local/three-products.spec.ts
```

Effective SHA-256 values after the scoped port:

```text
a4f478dd30b4725e76b9784b74c34fc555ccc8c190003b8651a0a4ff2f15d254  tests/e2e/local/support/harness.ts
9d37e73bd9b5fad18d93527ec9e7e1a9ff034d5b7f997472d64eb2fb214b5666  tests/e2e/local/support/timeline-scope.ts
e7506092720060b1982e3b1233061a822fdcc3a760969840cb8efb0eb3be92d6  tests/e2e/local/support/timeline-scope.test.ts
825b6940aff8f759256b2c55227776b71c3471eb66e4b4f36fb25fc956aaeee8  tests/e2e/local/three-products.spec.ts
```

`bridgeBase` is derived from the configured `doorBase`; it does not guess an
origin or port. The context listener is installed before the click. The
predicate requires the configured bridge origin, exact `/api/astrid/v1/projects`
path, no query/hash, POST, 201, and trimmed submitted name. The response
reader requires string `data.project_id`, exact trimmed `data.name`, and a
string `receipt.receipt_id`. Existing strict URL/realm/project/timeline,
readback, outbox, lifecycle, retry/restart, inverse, opaque-data, and
zero-legacy assertions remain unchanged.

Central preflight retained the qualified tuple: Agent `3c4f…`, Runtime
`202074110717`, producer `a0dca169…`, artifact `f021…`, shared schema
`6ba7b51e…`, and the locked Composition 13 graph. It verified 75 artifacts and
the private dependency graph before the hosted build. No Main01495bd adoption,
pin, provider, schema, fallback, or product change was made.

## Checks

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS, 1 test.
- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.spec.ts` — PASS.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit` — PASS.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep 'bootstrap actual consumer' --list` — PASS, exactly 1 test in 1 file.
- `sh -n` over the existing bootstrap wrapper and committed-service runner — PASS.
- `git diff --check` — PASS.
- Central gate: `request-test ap2-m2-bootstrap-approved-bridge-real-gate ap2-m2-bootstrap-observed-request-match-fix --no-cache` followed by `wait-test` — FAIL, exit 1, 86s. Result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-approved-bridge-real-gate-ap2-m2-bootstrap-observed-request-match-fix-1021001554-14046/`.

The central log retains the sanitized failure summary and source tuple. The
wrapper removed its temporary browser output after the failure; no second run
was made to preserve an unchanged failure.

## Blocker and next step

Blocked on the existing two-entry bootstrap history behavior versus the
preserved one-entry assertion. The orchestrator should determine whether the
qualified Runtime/Agent tuple needs a source-level correction or whether the
history contract is intentionally different. Do not claim the bootstrap gate,
publisher cut, or public adoption until a separately approved correction is
qualified.
