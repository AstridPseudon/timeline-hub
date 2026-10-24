## Report

Implemented a private D66 host profile that stages and resolves the exact pinned Composition `0.0.14` artifact without modifying shared dependencies, product code, or tests.

Exact artifact verified:

- Archive: 73,451 bytes
- SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
- Package digest: `6bbab9766c13dd450c08f3975e8f690bb718e2ba73f6d929ebd13ee4acb767cf`
- `animations.generated.js` resolved successfully

Tests:

- `node --check scripts/testing/d66-plain-stack-profile.mjs` — passed
- `node --import tsx --test scripts/testing/d66-plain-stack.test.mjs` — 22 passed
- All four source preflights — passed
- All four normal diagnostics reached build, readiness, and the original body:
  - Parent move: failed existing request-body assertion
  - Popup swap: Runtime `validation_error/invalid_records`
  - Transition single: failed existing `Edit timeline` body assertion
  - Transition bulk: UI displayed `__none__` instead of `None`

No retries or duplicate body submissions were made. Predecessor setup IDs `27231/12965/7951/6678` retained. Protected source hashes remained unchanged.

Evidence is under the assigned worker evidence directory. Full suites were not run per instructions. No blockers; no independent GO/NO-GO verdict issued.