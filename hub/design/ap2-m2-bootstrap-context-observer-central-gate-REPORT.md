# AP2-M2 bootstrap context-observer central qualification

## Result

**NOT QUALIFIED — the corrected fixture observer still missed the real browser
Runtime requests.** The one authorized central run selected and executed only
the bootstrap test. It failed at the fixture assertion that reads the
Playwright-collected request list, while the Playwright trace proves that the
browser sent both required Runtime POSTs. This is not evidence that production
failed to create a timeline.

No production App source changed. The committed candidate is
`1913f00af62b25943f258d2fd1362af3c73636d7` (tree
`7c8e930ee73f8a8804da11ff19f7edc23928decb`), whose only delta from the
configured-provider base is the intended test-fixture change from
`page.on('request')` to `context.on('request')`.

## Harness repair and selection proof

I created one disposable worker-owned wrapper and one uniquely named central
suite entry. The wrapper preserved the normal014 private source/authority
guards and exact tuple:

- Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`
- Runtime `202074110717146fc7f08af2306a8dd7f695b0b1`
- immutable producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`
- schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- locked Composition 13

Before `npm run build:hosted`, the central wrapper ran Playwright `--list`
with the exact path `tests/e2e/local/three-products.spec.ts` and the
unanchored unique substring `bootstrap actual consumer`. The service log
proved:

```text
three-products.spec.ts:1141:1 › M2 real gate 5 bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo
Total: 1 test in 1 file
```

The disposable wrapper and suite registration were removed after the run.

## One central run

Exact request:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-context-observer-central-gate \
  ap2-m2-bootstrap-context-observer-central-gate)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-bootstrap-context-observer-central-gate-ap2-m2-bootstrap-context-observer-central-gate-1020204553-434
```

Result: **FAIL, exit 1, 103 seconds**. Exactly one test ran. Hosted build and
the pre-build one-test collection proof passed. The first causal fixture
failure was `tests/e2e/local/three-products.spec.ts:1180`:

```text
production bootstrap must create the timeline through Runtime /v1
Received: undefined
```

No rerun, fallback journey, neighboring Gate 5 run, local browser/socket run,
or full suite was performed.

## Actual origin and transport proof

The central trace at
`/tmp/timeline-normal014-app.cPq73K/browser-output/three-products-M2-real-gat-9f316-ry-restart-and-guarded-undo/trace.zip`
contains these browser network entries in `0-trace.network`:

- `20:47:44.855Z`: `POST http://127.0.0.1:17340/api/runtime/v1/projects/e97619998da54d0199c7c4c9fe80fa93/timelines`, HTTP `201`.
- `20:47:44.936Z`: `POST http://127.0.0.1:17340/api/runtime/v1/projects/e97619998da54d0199c7c4c9fe80fa93/timelines/4aab3ff3-0cf0-5219-bda9-70c2af630d26/commit`, HTTP `200`.

Both entries have Chromium `User-Agent`, `Sec-Fetch-Mode: cors`,
`Sec-Fetch-Dest: empty`, and `Origin: https://astrid.test:37117`; they are
browser-originated cross-origin requests to the Runtime door, not Node-side
`harness.runtimeJson` calls. The trace therefore proves the product POST and
native commit happened. The failed `context.on` list is an observation gap,
not a missing product request.

The next fixture repair must capture the request at a boundary that records
the Runtime-door method/path/body (the existing `DirectHarness.audit()` is a
useful server-side path/origin signal but does not carry the commit body), or
add an equivalent test-only transport capture. Merely switching `page.on` to
`context.on` is insufficient in this hosted/browser transport. Do not claim a
product-side missing POST from this result.

## Verification and boundaries

- `git diff --check` — passed.
- Central `--list` — exactly one bootstrap test, before hosted build — passed.
- Central hosted build — passed.
- Central browser execution — one test, failed at the observer assertion.
- No App production source, Runtime authority, provider, schema, DTO,
  dependency, pin, public adoption, or product guard changed.
