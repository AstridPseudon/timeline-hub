# A2/P1 paired-head handoff

The App normal read now obtains `head_revision_id` and `head_publication_id` from the authenticated public timeline GET, after canonical inspection. It requires the GET response to identify the requested project/timeline and its revision to exactly equal the inspected revision. A mismatch retries once with a fresh inspection, then refuses before the immutable revision read; no latest-publication/old-revision pairing is possible. Actual legacy `null` publication values are preserved. The matched pair is returned to the normal `LoadedTimeline` basis and remains pinned for later Runtime CAS.

Changed files are limited to `src/integrations/runtime/dataProvider.ts`, `src/integrations/runtime/dataProvider.test.ts`, and `src/integrations/runtime/dataProvider.parity.test.ts`. Existing tests received local public-head transport adapters because `runtimeFixture` intentionally rejects the retired mutable timeline GET; the fixture itself is unchanged.

Evidence: private exact graph targeted Vitest **152/152 pass** across the two provider suites plus `useTimelineSave.test.tsx` and `timelineLocalSaveHandoff.test.ts`; `npm exec tsc -- --noEmit`, scoped ESLint, and `git diff --check` pass. Composition archive hash remains `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. No full/browser/service/live-socket run was performed.

Review seam: inspect the bounded pairing loop and the test adapters, then merge only this App worker's own commit after review. Runtime, generated/client/schema, Undo/history, fixtures, pins, and locks were not modified.
