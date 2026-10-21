# App2 M2 bootstrap bridge-base source review

## Disposition

APPROVE the exact App commit `dfdbef10f9d8ccf1a630f000cd076023918ead8a`
and tree `33674ef4bbaa4b043baed77492621095cccc28f7` for the closed source
profile and for one source-only next gate. No concrete code fix is required.
This approves source custody and the offline observer contract only. The
normal014 live bootstrap result `4657` remains false/unqualified.

## Reviewed change

The commit changes exactly one file and adds exactly two lines:

`tests/e2e/local/support/harness.ts:424-425`

```ts
get bridgeBase() { return this.doorBase.replace(/\/api\/runtime$/, '/api/astrid'); }
```

There are no product/runtime source changes, route additions, origin overrides,
credential changes, custody changes, or assertion removals in this commit.

## Origin and process-source review

The getter uses the existing configured door origin and only changes the
existing service path. The chain is consistent end to end:

- `scripts/hosted-build-origin.mjs:1-8` resolves the door origin from
  `ASTRID_APP_DIRECT_DOOR_PORT`, defaulting to `http://127.0.0.1:17340`.
- `scripts/build-hosted.mjs:4` puts that same origin into `VITE_RUNTIME_ORIGIN`.
- `src/integrations/runtime/connection.ts:83-90` derives
  `runtimeApiBase()` as `/api/runtime` and `astridBase()` as `/api/astrid` on
  the configured origin.
- `DirectHarness.doorBase` uses the same configured door port and
  `/api/runtime`; `bridgeBase` therefore resolves to the configured door's
  `/api/astrid` sibling.
- `src/integrations/astrid/projectRoutes.ts:53-72` sends the normal project
  create as `POST /v1/projects` through `AstridBridgeTransport`, with the
  existing name, slug, metadata, and idempotency key.
- `src/shared/hooks/projects/useProjectCRUD.ts:140-154` uses that existing
  project-create path, then calls the existing timeline bootstrap. Timeline
  initialization remains the separate RuntimeDataProvider path, not the
  bridge observer path.

The browser App origin is intentionally different (`https://astrid.test` in
the direct journey). The getter does not derive from or equate that browser
origin with the Runtime/bridge origin. The normal014 runner builds with the
same `ASTRID_APP_DIRECT_DOOR_PORT`-derived hosted origin and runs the existing
three-products suite; it does not introduce a second route or origin.

The observer remains strict. `timeline-scope.ts` requires the configured
bridge origin, exact `/api/astrid/v1/projects` path with no query/hash,
`POST`, status `201`, matching trimmed submitted name, and a valid
`data.project_id`, exact `data.name`, and string `receipt.receipt_id`. The
existing project/timeline scope, readback, history, retry/restart, inverse,
opaque-data, and zero-legacy assertions remain in the staged source.

## Preservation and conversion accounting

The native source preservation mapping is exact against HOME `ed194ce2f`:

- `src/integrations/runtime/createDefaultTimeline.ts` is byte-identical.
- `src/integrations/runtime/createDefaultTimeline.test.ts` is byte-identical:
  12 native tests and 61 `expect` calls remain.
- `runtime.lock.json` is byte-identical and retains the approved 0.2.14
  final95 bytes: producer version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
  Runtime source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, metadata hash
  `4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044`,
  generated-client hash
  `c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d`, and
  timeline-type hash
  `f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564`.

Relative to approved baseline-conversion commit `541f07f57`, the carried
final95 conversion is 12 files, 668 additions, and 157 deletions. That work
is inherited before this review commit; the review commit itself is only one
file and two added lines. In the native test file, the current source retains
12 tests and 61 expectations versus 12 tests and 33 expectations at `541f07f57`.
The extra expectations are explicit final95 native transport/receipt/history
checks, not assertion loss.

Relative to HOME `ed194ce2f`, the relevant carried observer/test additions are
the timeline-scope helper (`+91` lines), its test conversion (`+67/-1` lines),
the bootstrap journey conversion (`+83/-10` lines), and this harness getter
(`+2` lines). The bootstrap journey remains at 34 tests and increases from
577 to 588 `expect` calls; the scope unit test increases from 2 to 3 tests.
The 12 native tests/61 expectations and approved pin remain unchanged. No
unknown assertion drop was found. The only diff introduced by this review
commit is the getter itself.

## Offline verification

All passed:

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — 1 passed.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/three-products.spec.ts` — passed.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit` — passed.
- `ASTRID_APP_DIRECT_DOOR_PORT=18456 node --import tsx --input-type=module -e "..."` — positive configured-door getter and negative browser-origin probe passed.
- `git diff --check` — passed.
- Exact preservation checks with `git diff --quiet` for the native source, 12-test/61-assertion file, and lock file against HOME and the review parent — passed.

Not run by instruction: browser, localhost, live socket, Runtime service,
normal014 gate, full suite, or any bootstrap rerun. The prior `4657` run's
timeout is therefore not reclassified by this review.

## Next step

Use this exact commit/tree for the source-only next gate review, then have the
orchestrator decide whether to authorize one fresh normal014 bootstrap run.
Keep `4657` unqualified until that live run reaches and passes the preserved
strict create-response and native bootstrap assertions.
