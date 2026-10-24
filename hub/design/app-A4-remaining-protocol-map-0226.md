# A4 report — remaining protocol migration map

Read-only inventory at `5ad7907e8676553133f9a77cc6e9a541f1364c42`. No source or tests changed.

`commitSession.test.ts` contains 42 declarations:

- 37 remaining session-backed declarations.
- Excluded: two owner-recovery cases (0226), the seven-fault dependent recovery matrix (Sol0224), and lifecycle coverage already migrated in `b7261d56fd`.
- Two closure tests at [commitSession.test.ts:247](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/commands/commitSession.test.ts:247) and `:260` do not instantiate the retired session; move them to a loader/provider suite separately.
- No direct `runner.ts` import remains in this file.

## Packet 1 — Parent local-save protocol and resolution

Estimated files: [localSaveSession.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/commands/localSaveSession.test.ts), [localSaveSessionEnvironment.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/commands/__tests__/localSaveSessionEnvironment.ts), possibly [timelineLocalSaveHandoff.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts).

Current API: `createLocalSaveSession`; use `append()` for already-authored semantic commands, `appendDocument()` for `doc.patch`, then `flush()`, `recover(ownerId)`, `dispose()`. Production seam is `useTimelinePersistence` → `TimelineLocalSaveHandoff.capture/flush` → `localSaveSession/outbox`.

Cases:

- “keeps an unknown free transform conservative…”
- “retains a corrupt original display closure…”
- “captures dependent A5/B7…”
- “keeps a drag capture original…”
- “advances publication identity…”
- “queues B authored after uncertain A…” (`accepted`, `conflict`)
- “retains an unsaved B preview…”
- “recovers legacy work only with a matching original document…” (`true`, `false`)
- “recovers B on its original display closure…”
- “retains typed `$fault` on recovery…” (`conflict`, `refused`, `validation`, `authorization` × pending/non-pending)
- “keeps newer observed C…”
- “distinguishes busy/unavailable/conflict…”
- “keeps the preview visible and sends nothing…”
- “undo sends the explicit accepted publication…”
- “keeps the unknown-ACK barrier…”
- “authors a new explicit label intent…”
- “retains dependent B and unsupported operations…”
- “disables Keep for a rejected parent-label prefix…”
- “preserves the original rejected request…” (`deleted target`, `ambiguous owner`, `wrong scope`, `wrong revision`, `read failure`, `storage failure`)
- “fences keep/latest when dispose races…”

Retain exact request body/key, predecessor links, accepted-prefix adoption, refusal/error status, retained outbox bytes, no-send assertions, canonical rollback, and guarded undo. Undo must use `TimelineLocalSaveHandoff.undo/redo`; `LocalSaveSession` has no `undo()` API.

Targeted command:

```bash
npx vitest run src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts
```

## Packet 2 — Track-label behavior through document patches

Estimated files: [localSaveSession.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/commands/localSaveSession.test.ts), [timelineLocalSaveHandoff.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts), and the existing track-management persistence tests.

Current production path: `useTimelinePersistence` captures the actual editor document through `TimelineLocalSaveHandoff`; use `appendDocument()`/`doc.patch`, not a replacement `trackLabelPort`.

Cases:

- “keeps original presence… for value, empty and clear edits”
- “keeps queued move → label guards…”
- “keeps typing capture original…”
- “refuses an observed external label mutation…”
- “surfaces an unobserved external label change…”
- “allows disjoint remote editing…” (`move`, `label`)
- “drains a label-only edit on close…”
- “keeps a pending label request unchanged…”
- “refuses synthetic or ambiguous track ownership…”
- “refuses a mismatched … display basis…” (`project`, `timeline`, `publication`, `synthetic`)
- “refuses mixed previews atomically…”
- “refuses a typing capture invalidated…”

Retain absent vs present/null/empty semantics, only-label mutation, disjoint remote preservation, stale-capture refusal, pending request/key identity, no outbox append on invalid input, and full refusal chains. Translate obsolete `track.set`/preview-port assertions to the actual `doc.patch` changes emitted by A2; do not invent a LocalSave track-label alias.

Targeted command:

```bash
npx vitest run src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/commands/localSaveSession.test.ts
```

## Packet 3 — Native ingress seams and current A2 routing

Estimated files: [shotTimelineDataProvider.a3.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts), [bootstrapInitialization.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/integrations/runtime/bootstrapInitialization.test.ts), [timelineLocalSaveHandoff.test.ts](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts), plus existing capture tests.

Cases:

- “fences parent-media preparation…”
- “queues one literal overlay command…”
- “queues one native parent intent…”
- “captures one occurrence ADD batch…”
- “routes a persisted native bootstrap owner…”

Concrete seam decisions:

- Parent media add maps to `TimelineGestureReadBasis: 'prepared-media'` and `TimelineLocalSaveHandoff`; swap preparation has no equivalent LocalSave API and must not gain an invented one.
- Literal overlay has no current production caller found; retain its capture-unit coverage or establish the A2 document-save seam before migrating.
- Direct `occurrenceAddMediaPort` is not a production API. The real A2 path is `sharedPopupMediaCommands()` producing `occurrence.fork` plus `occurrence.add-media/swap-media` in [shotTimelineDataProvider.ts:739](/home/user/work/wt/app-A4-remaining-protocol-map-0226/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:739).
- Bootstrap has a real native seam: `RuntimeDataProvider.recoverNativeBootstrapTimeline()` → `recoverBootstrapInitialization()`. Keep it out of LocalSave migration and move its session-wrapper assertion to `bootstrapInitialization.test.ts`.

Retain exact media identity, stale/unverified refusals, durable request/key reuse, bootstrap owner reuse, and no recapture. Do not add LocalSave “bootstrap”, “occurrence”, or “elementOverlay” ports.

Targeted command:

```bash
npx vitest run src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/occurrenceMediaCapture.test.ts src/tools/video-editor/commands/elementOverlayCapture.test.ts
```

Tests were not run because this was an inventory-only task. The next safe dispatch is Packet 1; Packet 3 should follow only after A2 confirms the literal-overlay and parent-media-swap seams.