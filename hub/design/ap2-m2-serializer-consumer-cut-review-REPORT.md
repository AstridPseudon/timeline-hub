# App M2 resolved-edit serializer consumer cut review

## Result

No source deletion is safe on the current `hub/tl/integration` tree. The row is
cut-ready only after the remaining `resolved-config`/whole-resolved-config
producers are converted to qualified native command producers. I left the App
tree unchanged; deleting `serializeResolvedTimelineEdit`, its imports, or the
mutation variants now would remove live behavior and/or unsupported-family
draft preservation.

Reviewed tree: `480db7febe624fe4658a75cbdb66ed5de84c2c61` (same SHA as
`hub/tl/integration`). The latest HOME status is App `42fc57460`; it explicitly
keeps D01 resolved-edit serializer open and lists the remaining writer cuts.
The existing source handoff was based on the older current-root tree; this
review rechecked the current integration tree, including the later raw-basis
serializer changes.

## Exact live serializer consumers

`serializeResolvedTimelineEdit` has exactly three non-test production callsites:

1. `src/tools/video-editor/commands/runner.ts:3,244-255`, in the
   `applyTimelineCommandEffect` `resolved-config` arm. The live producer is
   `src/tools/video-editor/commands/media.ts:244-291`,
   `buildSwapMediaCommandEffect`, whose swap descriptor still builds a complete
   resolved document and returns `type: 'resolved-config'`. Existing native
   `occurrence.swap-media`/verified-media machinery is the intended family, but
   there is not yet a qualified App capture/session bridge carrying the exact
   raw occurrence ownership, old media selection, new media selection, and
   guards. This is the popup/parent media add/swap blocker, not dead code.

2. `src/tools/video-editor/hooks/useTimelineCommit.ts:22,536-553`, the final
   `applyEdit` `type: 'config'` branch. It is the shared save owner: it calls
   the serializer, rebuilds with `buildDataFromCurrentRegistry`, and schedules
   the legacy snapshot save. Current live emissions include:
   - `useTimelineCommandsService.ts:742,864,910,990,1034,1130` for generic
     clip update, trim, split, track creation, track reorder, and managed-clip
     detach;
   - `useClipEditing.ts:99-114`, used by clip positioning, splitting, and audio
     management;
   - `useTimelineTrackManagement.ts:621-648,904,941,956,964,994,1072` for
     group/clip movement, track edits, row reorder, track removal, and unused
     track cleanup;
   - `browser/hooks.tsx:209-214,290-295` for public config replacement and
     sequence-draft replacement; and
   - `ShaderInspector.tsx:289-301` for clip and postprocess shader metadata.
   These are still open producer families. Native Agent operations exist for
   several narrow shapes (`clip.set`, `clip.set-params`, `clip.trim`,
   `clip.split`, `track.create`, `track.set`, `clip.add`, `clip.delete`), but
   the App capture/session adapters and exact authored guards are not qualified
   for this entire set. Mixed config edits, shader roots, track removal/reorder,
   and sequence/whole-timeline transforms cannot be silently narrowed.

3. `src/tools/video-editor/lib/timeline-mutation-engine.ts:3,208-222`, the
   pure preview/validation twin. `useTimelineCommandsService.ts` routes its
   `applyValidatedMutation` config producers through this branch before the
   shared save owner. Removing this call without making preview consume the
   same native command projection would leave preview and commit semantically
   different. It is a live preview consumer, not a dead helper.

The mutation type declarations remain live at
`commands/types.ts:58-75` and `useTimelineCommit.ts:93-124`; the
`resolved-config` arm is still emitted by media swap and the `config` arm is
still emitted by the families above. The current native move/track-label,
prepared-media, selected-param, duplicate, and parent-media work does not make
these serializer consumers dead.

## Serializer-local helper audit

No serializer-local deletion is proven safe:

- `serializeForDisk`, `serializeClipForDisk`, `serializeTrackForDisk`, and
  `validateSerializedConfig` remain used by production code and/or the shared
  domain validation path.
- `serializeProjectedTimelineConfig` remains live in
  `travel-between-images/components/shotTimelineDataProvider.ts:562` and
  `useTimelineSave.draftConfig.ts:30`; it must not be confused with the
  legacy resolved-edit writer.
- `projectedClipCounterparts` and `verifiedRetainedRawClipIds` are used by
  that projection path and by `serializeProjectedTimelineConfig` itself.
- `cloneTimelineExtras` is shared by `timeline-domain.ts`, `timeline-data.ts`,
  `shotCompositionProjection.ts`, and the resolved serializer. It is not
  legacy-only.

The direct `serializeResolvedTimelineEdit` behavior tests at
`serialize.test.ts:942-1056` preserve authored registry/opaque roots,
null/false/0/order/proto values, raw-cap restoration, and refusal when the
verified raw basis is missing. They remain required positives/refusal behavior;
none maps one-to-one to a qualified replacement yet.

## Merge/ownership review

- `8c0e1f799` is the duplicate deletion merge. Its graph-writer deletion is
  unrelated to the serializer; the three direct serializer callsites remain.
- `7d42fcd3a` is the owner/stale `TimelineOps` merge. It adds native command
  session coverage but does not replace the generic config mutation branch.
- `5a7144b55` is the selected-param shared prerequisite. It qualifies the
  selected-param carrier only; it does not authorize deleting the generic
  resolved serializer or changing App-owned session/door/outbox seams here.
- PLAN keep/cut requires the old App fallback writers to reach zero, but also
  requires each consumer to emit a command first. This row owns review/cut
  preparation; it does not own native adoption or shared session plumbing.

## Cut-ready sequence and blockers

1. Qualify one producer family at a time with an Agent-native command, exact
   raw/base/revision inputs, local preview equal to the command projection,
   Runtime `/v1` acceptance, reload, guarded undo, lost-ack exact retry, and
   draft preservation on unsupported shapes.
2. Route both `timeline-mutation-engine` preview and `useTimelineCommit` save
   through that same native projection. Keep generic opaque/null/order/proto
   and unsupported-family refusal coverage.
3. Prove zero old snapshot traffic for that representative gesture, including
   popup add/swap where applicable.
4. Only after all producers are converted: remove the `resolved-config` and
   resolved `config` mutation variants, the three imports/calls, and finally
   `serializeResolvedTimelineEdit`. Do not delete `serializeForDisk` or the
   raw-basis projection helpers as part of this cut.

Blocking prerequisites are the App capture/session adapters and independent
acceptance for the open producer families above, plus the central Gate 5/6
checks. No new DTO/API/provider/framework is needed or proposed.

## Tests

Ran the bounded requested Vitest lane with the shared `node_modules` treated as
read-only and no cache written there:

```sh
TMPDIR=/tmp/ap2-m2-serializer-consumer-cut-review-vitest-cache \
  npx vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/commands/runner.test.ts \
  src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts
```

Result: **3 files, 63 tests passed, exit 0**. No full, browser, socket, or
live-runtime suite was run. No source tests were retired or weakened.

