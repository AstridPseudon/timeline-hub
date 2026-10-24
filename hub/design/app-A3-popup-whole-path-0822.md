# A3 read-only assessment

- Confirmed defect: `ShotTimelinePreview.tsx:548-550` passes the resolved projection into `createShotTimelineInitialData`; `shotTimelineDataProvider.ts:124-155` copies projected clips containing derived `assetEntry` into authored `TimelineData.config`.
- `rowsToConfig` retains that raw projected clip (`timeline-data.ts:322-336, 430-434`).
- `applyPreparedMediaCommand` then fails strict config validation (`media.ts:849-891`; `timeline-domain.ts:2581-2595`), and `useTimelineCommandsService.ts:509-523` returns `mutation_failed` before `applyEdit`. A2 capture, outbox, and Runtime are not reached.

The correct existing boundary is `createCanonicalTimeline` (`shotTimelineDataProvider.ts:158-205, 453-463`). It strips only derived `assetEntry`, joins exact raw counterparts, and preserves authored raw fields and closure data. The safe repair should separate this authored projection from the resolved render projection; do not loosen validation, remove `assetEntry` from rendering, or globally strip unknown fields.

Preservation requirements: raw v2 closure, registry, opaque/extension fields, metadata, absent-vs-null presence, raw IDs, pins, revisions, and dependency manifests. Existing P1 authoring-boundary controls in `authoringBundle.ts`, `p1FeasibilityCorpus.test.ts`, `timeline-data.test.ts`, and `commitSession.test.ts` cover these cases.

Actual vs mocked:

- Actual mounted production path reaches local popup preparation and fails before `applyEdit`.
- A2/outbox and RuntimeDataProvider transport were not reached.
- Existing 0748/0814 controls and P1 transport are mocked/unit boundaries; no browser, backend, HTTP, or full suite was run.

Verification:

- `git diff --check` — PASS
- Worktree remains clean.
- No product or test files changed.
- Commit message written and `DONE` marker created.