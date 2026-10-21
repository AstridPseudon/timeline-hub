# app-m2-popup-file-birth-existing-serializer-proposal-r81

## Result

Produced one unapplied File-import occurrence-birth mapping and one bounded
peer request to App2. No App product or test source was changed. The mapping
reuses the existing `rowsToConfig` conversion and the existing
`buildAssetDropEdit` planner, with the explicit canonical occurrence and
original Runtime five-field selection retained.

The source trace is currently **fail-closed**: Main's serializer does not
preserve the Agent raw-row contract. Image rows retain `clipType: 'hold'`
instead of `image`/`media`; video rows retain `from/to/speed` but omit the
required positive `hold`. No field was invented and no App2 activation was
proposed.

## Exact source evidence

- Main conversion: `src/tools/video-editor/lib/timeline-data.ts:272-414`.
- Existing prepared-media caller of that conversion:
  `src/tools/video-editor/commands/media.ts:521-558`.
- Existing planner: `src/tools/video-editor/lib/timeline-asset-plans.ts:321-427`.
- File-import selection capture and forwarding:
  `src/integrations/runtime/dataProvider.ts:1640-1711` and
  `src/tools/video-editor/hooks/useAssetManagement.ts:210-261,411-530`.
- Explicit occurrence selection and popup local coordinates:
  `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:83-125,519-530`.
- Agent raw-row validator and capture signature:
  `src/tools/video-editor/commands/occurrenceMediaCapture.ts:211-250,312-355`.
- Agent approved video birth shape:
  `/home/user/work/agent/docs/design/m2-auto-placement.md:25-26`.

## Verification

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=2 src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts
```

Result: **2 files passed, 25 tests passed** (4.27s). These are existing
serializer/planner witnesses; they do not qualify the unimplemented occurrence
branch. No actual, browser, full suite, install, build, graph, or live-socket
run was performed.

## Blocker / next step

App2 needs reciprocal agreement on the fail-closed boundary and an existing
Main-owned source that supplies an already Agent-compatible newborn raw row.
The existing `handleAssetDrop(assetKey, trackId, time, forceNewTrack,
insertAtTop, preparedAsset, removeClipId)` callback is the smallest available
handoff: `preparedAsset` retains the original selection and its track/time
arguments retain drop context, but it returns no raw child row. The exact
missing input is therefore an already Agent-compatible row. The smallest
required semantic repair is exactly `clipType: 'image'` for image births and
`hold = to - from` for video births; this worker did not apply it.

