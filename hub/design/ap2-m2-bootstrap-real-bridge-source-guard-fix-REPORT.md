# AP2-M2 bootstrap real bridge source-guard repair

## Result

Fixed only the held test-local project-create response source guard on top of
`tl/ap2-m2-bootstrap-create-response-predicate-source` (`fca9317a0`). The
production creator, API, schema, provider, transport, pins, and product
behavior are unchanged.

## Change

- Added the existing `DirectHarness` bridge carrier as `doorBase` with
  `/api/runtime` changed only to the sibling `/api/astrid` path; it uses the
  configured door origin/port and does not guess a port.
- Bound the context response predicate to that required bridge base and exact
  `/api/astrid/v1/projects` origin/path, with no query/hash, strict POST, HTTP
  201, and exact trimmed submitted name.
- Added a test-local response reader requiring the matched response's
  `data.project_id`, exact trimmed `data.name`, and `receipt.receipt_id`
  before the existing exact realm/project/timeline/readback/URL/lifecycle
  guards run.
- Extended the existing context control with one bridge-positive case and
  refusals for a wrong origin, the old `/api/runtime` lookalike, GET, wrong
  status/name, malformed request JSON, and a malformed `data`/`receipt`
  envelope. The context listener remains created before the click.

Changed paths only:

```text
tests/e2e/local/support/harness.ts
tests/e2e/local/support/timeline-scope.ts
tests/e2e/local/support/timeline-scope.test.ts
tests/e2e/local/three-products.spec.ts
```

Exact post-change SHA-256 hashes:

```text
9d37e73bd9b5fad18d93527ec9e7e1a9ff034d5b7f997472d64eb2fb214b5666  tests/e2e/local/support/timeline-scope.ts
e7506092720060b1982e3b1233061a822fdcc3a760969840cb8efb0eb3be92d6  tests/e2e/local/support/timeline-scope.test.ts
db4888ac5ceb12a1818f1a79efb7a2f41d56ba7b1c73b6cbfcf4bb2f0494500c  tests/e2e/local/support/harness.ts
825b6940aff8f759256b2c55227776b71c3471eb66e4b4f36fb25fc956aaeee8  tests/e2e/local/three-products.spec.ts
```

No external wrapper or wrapper hash was changed; no wrapper exists in this
worktree. These hashes are recorded only after the scoped source proof.

## Checks

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS.
- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.spec.ts` — PASS.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit` — PASS.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts` — PASS; 12 tests listed, exactly one bootstrap consumer test.
- `git diff --check` — PASS.
- Shell syntax check (`bash -n` over the scoped check body) — PASS.

Not run, as required: the actual bootstrap browser journey, localhost/live
sockets, Runtime Door, `request-test`, or any full suite. Real post-change
browser qualification remains unverified pending custody approval.

## Handoff

The harness should commit the worktree using the accompanying commit message.
The next step is narrow custody review of the configured bridge source guard;
only after approval may the existing authorized real bootstrap gate be run.
