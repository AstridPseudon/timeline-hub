## Report

Implemented D73 exact-submit handling in:

- `scripts/testing/d66-plain-stack.mjs`
- `scripts/testing/d66-plain-stack.test.mjs`

The harness now:

- Captures full SHA/tree pins for App, Agent, Runtime, and Composition once at submit.
- Requests detached exact checkouts and validates genuine receipts.
- Uses only pinned sources during launch; moving normal homes no longer invalidate runs.
- Preserves P1/P2/P3 and exact-one-element collection routes/private logs.
- Adds stale, missing, tampered, wrong-checkout, App/Composition, and zero-gesture negative coverage.

Submit candidate:

```bash
D66_SUBMIT_TARGET=app-P-D73-exact-submit-1709 \
D66_SUBMIT_SUITE=d66-p3-exact-submit \
node scripts/testing/d66-plain-stack.mjs p3 --submit
```

This requests all four checkouts, waits for validated receipts, then prints the service recipe and the subsequent `bin/request-test` command. No browser, original journey, or service was run.

Tests passed:

- Node20 focused tests: 8/8
- Collection: P1=2, P2=8, P3=1, element=1
- Node20 `--check`
- TypeScript `tsconfig.node.json`
- Scoped ESLint
- `git diff --check`
- Six protected spec hashes unchanged

No blockers. Existing running request 26907 was not interrupted or repeated. Commit message and `DONE` marker are ready.