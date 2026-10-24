## Report

- Added `localSaveSession.trackLabelRefusal.test.ts` with six migrated A4 label-refusal declarations using real IndexedDB/local `doc.patch` handoff behavior.
- Removed only those six declarations from `commitSession.test.ts`.
- Preserved guarded patch values, outbox chaining, pending request/key identity, raw opaque/sibling data, and no-send assertions.
- Wrote commit message and `DONE` marker.

Tests:

- Targeted Vitest: 6 files, 124 passed.
- `tsc` root/App/Node: all passed.
- Scoped ESLint with `--max-warnings 0`: passed.
- Environment reported Node v22.22.0; Node 20 was unavailable.

No production or helper files changed.