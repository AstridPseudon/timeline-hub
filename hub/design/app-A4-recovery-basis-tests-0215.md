## Report

Implemented on base `8f92a51e3a`:

- Removed the seven-fault case from `commitSession.test.ts`.
- Added `localSaveSession.recoveryBasis.test.ts` using real `createLocalSaveSession`, IndexedDB outbox, document-patch intents, A-ACK/B-retry setup, exact retention and refusal assertions.
- No production/helper or out-of-scope files changed.
- Commit message written; `BLOCKED` marker created. No `DONE` marker.

Validation:

- Existing targeted suites: **90 passed** across 4 files.
- New recovery matrix: **7 failed** because current `localSaveSession` resolves recovery instead of refusing malformed dependent `displayBasis`.
- Root/App/Node TypeScript: **PASS**.
- Scoped ESLint (`--max-warnings 0`): **PASS**.
- `git diff --check`: **PASS**.
- Census: title appears once in the new file; all seven faults preserved.

Blocker: `localSaveSession.ts:224-237` validates only the accepted prefix and skips the dependent intent’s stored display basis, then reprojects/retries B. Production/helper edits were explicitly out of scope, so the required matrix remains failing without weakening expectations.

No full, browser, backend, live-service, or central suites were run.