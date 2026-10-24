## Report

Implemented the minimum faithful fix in:

- `tests/e2e/local/three-products.p2-popup.spec.ts`
- `tests/e2e/local/support/p2-popup-oracle.test.mjs`

The retained failure’s seven extras were all `POST /api/runtime/v1/projects/<project>/timelines/<timeline>/inspect` read requests, with 200 responses; observed durations ranged roughly 20–5,335 ms. Source inspection confirms these are Runtime canonical-head inspection/coalesced polling reads, not writes. The expected commit remained the sole film mutation; media import remained separately excluded.

The classifier now accepts only the exact inspect POST (direct or mounted prefix, no query/hash). Exact negatives reject old-save, unknown-write, extra-commit, wrong-method, and query variants. Existing exact commit equality and POST/commit-route predicates remain intact. Canonical, identity, reload, undo, waits, and timeouts were untouched.

Source blobs:

- Popup: `33763eb5435aa6e357a2ff3489a53e23b9487b00`
- Control: `a1b4852b92efb3f0a6ee3e233bb3758833375730`

Tests passed:

- Dedicated Node control: 3/3
- App TypeScript noEmit
- Node TypeScript noEmit
- Scoped ESLint
- Node syntax check
- `git diff --check`

Central E2E attempt reported “No test files found” because the targeted Vitest suite excludes Playwright E2E specs. No unchanged ADD retry or full suite was run.

Protected six-file SHA-256 map: only the permitted popup spec changed; the other five remained byte-identical.

Commit message and `DONE` marker were created.