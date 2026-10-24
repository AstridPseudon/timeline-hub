## A4 census report

- Actual HEAD: `22efcda3da4005f8663c078439ff0edbfade69be`
- Tree: `3387c860ec236c8631d64e5f979588bd6071e33a`
- Worktree clean; zero source/test/generated edits.

### Current caller map

Keep:

- `commands/runner.ts`, `types.ts`, `media.ts`: live prepared-media preview path via `useTimelineState.ts`, `useTimelineHistory.ts`, and `media.ts`.
- `commands/autoCapture.ts`, `editorImagePlacement.ts`: live automatic-placement path via `clientLocalAdapter.ts`.
- `commands/bootstrapCapture.ts`: live `bootstrapInitialization.ts` dependency.
- `commands/clipMovePrimitives.ts`, `authoringBundle.ts`, `commitOutbox.ts`, `localSaveSession.ts`, `timelineLocalSaveHandoff.ts`: current v2/local-save machinery.
- `useTimelineSave.ts:85-225` → `localSaveSession` → `DataProvider.commitTimeline` → generated Runtime client.
- Current v2 request/reply fields, idempotency key, canonical adoption, accepted/merged/rebased/conflict/invalid handling remain in this path.

Dormant retirement candidates:

- `commands/commitSession.ts` (1435 lines): no runtime constructor callers; imported by legacy tests and as the stale `OccurrenceAddMediaCapturePort` type in five production files.
- `commands/genericPatchCapture.ts` (696 lines): only legacy session/member tests and `ordinaryScalarMember.ts`.
- Legacy capture family: `clipMoveCapture`, `clipParamsCapture`, `clipScalarCapture`, `clipTrimCapture`, `elementCapture`, `elementOverlayCapture`, `nativePlacementCapture`, `occurrenceDuplicateCapture`, `occurrenceMediaCapture`, `parentClipAddCapture`, `parentClipSwapCapture`, `sessionPlacement`, `shotSetCapture`, and `trackLabelCapture`.
- `parentAfterAnchorCapture.ts` and `trackReorderCapture.ts` have no production callers. Current UI uses `media.ts`/`duplicate-clip.ts` and `useTimelineTrackManagement.ts`; these are not equivalent to the raw hold/ripple or explicit track-order command semantics.

Required test migration/preservation:

- `commitSession*.test.ts`, `shotSetSession.test.ts`, `genericPatchCapture.test.ts`, `ordinary*Member.test.ts`, and capture-specific suites must retain assertions while moving supported cases to mounted v2/local-save boundaries.
- Do not replace raw-positive after-anchor cases with raw negatives; current mounted path does not cover missing/null hold, subminimum duration, incoming transition, or equivalent raw ripple semantics.
- Candidate legacy goldens include `recipe_m1_move.json`, `recipe_m2_app_clip_scalar_fields.json`, `recipe_m2_app_occurrence_duplicate.json`, `recipe_m2_app_track_label.json`, `recipe_m2_clip_trim*.json`, `ordinary_real_batch.json`, and their legacy parity scripts. Keep active bootstrap, prepared-image producer, `authoringBundle.json`, and P1 corpus fixtures until their consumers migrate.

D31 keep:

- Keep `transcriptAssociateCapture.ts` and its unchanged 397-line/40-assertion test.
- Keep required current helpers: `project-transcript-host.ts`, `reconcileTranscriptReferences.ts`, and `importTranscriptHandoff.ts`.
- No new parity/approval gate was added. Existing reports correctly record remaining config-mirror/collision/shared-row gaps.

### Existing acceptance commands

Qualified targeted forms are:

```bash
node --import <dirname-preload> node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/commands/trackReorderCapture.test.ts
```

```bash
node --import <dirname-preload> node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx \
  src/tools/video-editor/lib/project-transcript-host.test.ts \
  src/tools/video-editor/data/typed/importTranscriptHandoff.test.ts \
  src/tools/video-editor/commands/transcriptAssociateCapture.test.ts
```

Prior bounded evidence: occurrence-port review `118/118` plus A3 guard `25/25`; mounted track `29` tests; mounted positive `53`; transcript `52`, reconciliation `56`; all reported TypeScript, ESLint, and diff checks passed. This worker ran no suite because it made no source changes.

The earlier `1900/1906` work removed only unused occurrence ports while retaining the executor; it must not be labeled as whole-A4 deletion. Retirement remains gated on independently qualified original P1 `118792` actual `2/2 PASS`.

Required commit message and `DONE` marker were written.