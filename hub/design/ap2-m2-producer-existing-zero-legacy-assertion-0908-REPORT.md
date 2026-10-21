# AP2 M2 producer existing zero-legacy assertion — 0908

## Result

Added the missing zero-legacy-traffic guard to the original producer case:

- `tests/e2e/local/producer-ownership-current-pin.spec.ts`
  - Starts the existing `observeProducerCommits` observer before producer
    gestures.
  - Asserts `legacyTraffic.legacy` is empty in the existing scene `finally`
    (so the visible refusal/early return cannot bypass the check).
  - Checks again in the undo `finally`, then disposes the whole-test observer.
  - Preserves the marker count `2`, source IDs, protected foreign/user rows and
    order, refusal and `no-accepted-ownership-proof` annotation, exact command
    selector/value/clear assertions, lost-ACK exact body/key retry, reload,
    authored readback, and undo assertions.
- `tests/e2e/local/support/producer-ownership-current-pin.ts`
  - Extends the existing producer observer with the established mounted-test
    film-save boundary:
    `/(?:composition-revisions|revisions|restore|restore-history)(?:\/[^/]+)?$/`
    on paths, with `POST`, `PUT`, `PATCH`, and `DELETE` mutation verbs.
  - Normal setup reads and document/catalog operations are not recorded as
    legacy film saves.

No production code, fixtures, source pins, shared `support/app.ts`, or guards
were changed. The detector is row-local because the established pattern is not
exported by the HOME-owned shared support; no generic framework was added.

## Exact source/tree/spec hashes

- Base/current committed HEAD: `4d6ff2176c6a19fc8b5831662beb8e6d7d0e5de6`
- Base/current committed tree: `16d17331db3c0b4949844872851c9c868dfe7312`
- Current spec Git blob: `9f8b4682238ad57df3ba03db33ddfc66a90cc880`
- Current spec SHA-256: `6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6`
- Current helper Git blob: `86c099627710dfd4f61a93b304142107f032f284`
- Current helper SHA-256: `df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949`

The tree hash is the committed base tree; the two changed files are uncommitted
worker changes and therefore represented by their current blob/SHA-256 hashes.
Diff: 2 files, 21 insertions, 2 deletions.

## Verification

Passed:

```text
node --input-type=module <<'EOF'
const legacyWrites = /\/(?:composition-revisions|revisions|restore|restore-history)(?:\/[^/]+)?$/;
const cases = [
  ['POST', '/api/runtime/v1/projects/p/timelines/t/composition-revisions', true],
  ['PUT', '/api/runtime/v1/projects/p/timelines/t/revisions/r', true],
  ['PATCH', '/api/runtime/v1/projects/p/timelines/t/restore/r', true],
  ['DELETE', '/api/runtime/v1/projects/p/timelines/t/restore-history/r', true],
  ['GET', '/api/runtime/v1/projects/p/timelines/t/composition-revisions', false],
  ['POST', '/api/runtime/v1/projects/p/timelines/t/commit', false],
  ['POST', '/api/runtime/v1/projects/p/documents', false],
  ['POST', '/api/runtime/v1/projects/p/catalog', false],
];
for (const [method, pathname, expected] of cases) {
  const observed = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && legacyWrites.test(pathname);
  if (observed !== expected) throw new Error(`${method} ${pathname}: expected ${expected}, got ${observed}`);
}
console.log(`legacy detector proof: ${cases.length} cases passed`);
EOF
legacy detector proof: 8 cases passed
git diff --check
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts
```

The detector proof covered all four mutation verbs on the four established
legacy suffixes, plus GET/read, native `/commit`, document, and catalog
exclusions.

Attempted, not run to completion:

```text
node_modules/.bin/playwright test \
  tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

It failed during config loading because the isolated-port allocator could not
allocate `PLAYWRIGHT_PORT` after 80 attempts. No browser, build, daemon,
localhost/service, live socket, actual, full, install, or broad matrix run was
performed.

## Historical-run caveat

The old `19080` run failed before producer gestures at the obsolete
`transcript-lane-chip` selector and did not contain this zero-legacy assertion.
It is not evidence for a zero-legacy result. The independent 0903 review also
correctly recorded that the original producer case had no separate
zero-legacy assertion; this change closes that specific gap only.

## Next step

Run the existing central producer actual/list gate after integration. This
worker does not claim accepted producer behavior or a live zero-legacy result.
