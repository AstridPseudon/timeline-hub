Implemented A4 migration.

- Added `localSaveSession.trackLabelProtocol.test.ts` with all six original scenarios using `doc.patch`/outbox flow.
- Removed only those six declarations from `commitSession.test.ts`.
- Preserved guards, reload identity, canonical/raw/sibling/closure assertions, conflict handling, and old-route rejection.

Tests:

- ESLint: passed.
- TypeScript (`npx tsc --noEmit --incremental false`): passed.
- Targeted Vitest: 6 files, 214 tests passed.

No full/browser suites run.

Note: `TimelineLocalSaveHandoff.capture` lacks an explicit track-label clear token and treats omission as a partial view. The clear case therefore uses the same underlying `documentPatchIntent`/outbox path directly; recommended follow-up is adding explicit clear support to the handoff API.