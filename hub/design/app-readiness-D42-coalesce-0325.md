## Done

Implemented same-head bootstrap basis-read coalescing in `useTimelineSave.ts`.

- Reuses only an unresolved read with identical provider, scope, head, mounted source identity, and edit sequence.
- Settled/rejected reads retire; changed head/publication/scope/source/provider starts a fresh read.
- Preserved cancellation, generation, authority, stale-head, refusal, IndexedDB, and wait semantics.
- Copied diagnostic packet from donor `7502a2c57f`.
- Added coverage for coalescing, rejection retry, publication changes, source mismatch, and diagnostic correlation.

## Tests

- `useTimelineSave.test.tsx`: 91 passed
- Diagnostic/provider tests: 90 passed
- Root/app/node TypeScript checks: passed
- Scoped ESLint: passed
- `git diff --check`: passed

No full suite, browser, service, or Gate run was performed. The historical P2 cancellation trigger remains UNKNOWN.

Commit message and `DONE` marker created. Independent Luna review is still required.