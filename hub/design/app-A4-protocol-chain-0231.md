## Report

Implemented A4 migration:

- Added `localSaveSession.chainProtocol.test.ts` with all six retained declarations.
- Removed only those declarations from `commitSession.test.ts`.
- No production/helper changes.

Validation:

- Node 20 Vitest: 6 files, 131 tests passed.
- TypeScript `--noEmit --incremental false`: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.

Decision: missing-manifest recovery uses the current authoring validator’s refusal without preserving the obsolete error wording; no test-only predicate was added.

No blockers. Commit message and `DONE` marker created.