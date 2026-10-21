# App M2 trace: fresh producer clip birth and ownership carrier

## Result

No live callers changed. No App product files were edited.

The carrier is not missing from Main's producer. Main does not put `managedBy` on
the initial `clip.add`, but the existing transcript producer builds complete
host-generated metadata before it emits the later update. The narrow integration
regression is earlier: integration routes this mixed producer batch into generic
native capture, which refuses the rich update before the existing compiler and
publication path can run.

## Main producer and normal runner

The real Main object is `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
`ea4eabb8eb469df63fd1d515f84982d85b2f14cc`. The transcript extension is unchanged
between that object and the integration worktree for this trace.

In `src/tools/video-editor/dev/transcript-lane/extension.ts`:

- Lines 404-420 call `createHostGeneratedObjectMeta` with the invocation's
  `extensionId`, the real `TRANSCRIPT_CAPTION_CONTRIBUTION_ID`, source schema and
  item, source revision, output value, generator version, fingerprints, and
  conflict policy.
- Lines 423-433 emit the intentionally minimal `clip.add`: track, start time,
  and `clipType: 'text'`. It has no `managedBy` and should not be treated as a
  complete row by itself.
- Lines 435-449 emit the ordered `clip.update`: track, start, `hold`, text
  geometry, label, and `app: { __generated__: generatedMeta }`.
- Lines 754-774 are the normal extension runner: snapshot, build, validate, and
  `ctx.creative.timeline.apply(patch)`.

This is a complete generated-metadata carrier, not an implicit owner claim. The
host helper's one contract is visible in
`src/sdk/video/timeline/sourceMap.ts:133-180,251-285`: `GeneratedObjectMeta`
contains `extensionId` and `contributionId`, while its provenance contains the
schema, source item, source fingerprint/revision, generator version, output
fingerprint, and conflict policy.

There is no `app.managedBy` in this producer's patch. That distinction matters:
`src/tools/video-editor/lib/timeline-reader.ts:129-153` derives the separate
`managed/managedBy` summary only from explicit `managedBy`, a known extension
namespace, or `source_uuid`; `:167-184` extracts `app.__generated__` separately,
and `:647-655,906-935` carries both fields into the reader summary. Therefore an
initial add without `managedBy` is not evidence that the later generated carrier
is absent, and this trace does not silently adopt an owner.

## Add, update, compiler, and persisted row

The existing compiler makes the later update the rest of the birth row:

- `src/tools/video-editor/lib/timeline-patch.ts:1137-1142` creates only the
  structural clip from `clip.add`; `:1165-1173` records minimal meta.
- `:1284-1288` shallow-merges the later update into that clip. The meta sync at
  `:1291-1314` permits `hold`, text/geometry, label, and `app`, so the generated
  metadata is retained for row serialization.
- `:1936-1978` rebuilds rows, merges compiler meta, attaches app/track data, and
  builds the next `TimelineData`. Thus the update's hold and host metadata are
  present in the complete clip row before publication.

The existing positive witnesses are real extension behavior, not invented owners:

- `src/tools/video-editor/dev/scene-phase-markers/extension.ts:605-612,614-655`
  documents and builds the normal `clip.add` then `clip.update{hold,label}` shape;
  its normal runner applies it at `:768-795`.
- `src/tools/video-editor/lib/timeline-patch.test.ts:5590-5613` proves that
  `clip.add + clip.update` persists label and hold in both the clip and row meta;
  `:5615-5638` proves source timing and opaque `app` data survive compilation.
- `src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx:1017-1043`
  uses the real transcript builder and verifies the host provenance fields and
  generated text. The stale generated-output fixture at `:1065-1090` also uses
  the real extension/contribution IDs.

After `commitData`, the existing publication path is:

1. `src/tools/video-editor/hooks/useTimelineCommit.ts:408-410` emits
   `scheduleSave` for the compiled data.
2. `src/tools/video-editor/hooks/useTimelinePersistence.ts:623-680` turns the
   scheduled authored config into a provider save attempt; `:1017-1135` queues,
   debounces, and invokes it.
3. `src/integrations/runtime/dataProvider.ts:1014-1027` enters
   `saveTimelineAtHead`; `:1072-1098` puts the compiled clips/config into the
   `parentComposition`; `:1131-1144` publishes it; `:1166-1184` accepts the
   persisted head and updates canonical state. The persisted row is therefore
   the `parent_composition.config.clips` / top-level `clips` payload, with the
   later update's `hold` and `app.__generated__` already attached.

## Integration-only regression and App-owned seam

Manager decision: the carrier trace is evidence for completing the native migration. Mixed-batch refusal must stay atomic; the recommendation below does not authorize restoring or expanding snapshot publication. Keep the original fresh-caption positive OPEN until the whole native recipe is qualified.

Main's `src/tools/video-editor/hooks/useTimelineOps.ts:250-279` goes directly
through validate, `compileTimelinePatch`, and `commitData`.

Integration added the generic route at
`src/tools/video-editor/hooks/useTimelineOps.ts:267-275`: any patch whose
`classifyGenericPatch` result is not `unsupported` is sent to the generic port
before the compiler. The transcript patch is classified as `mixed` because its
structural `clip.add` is accepted by
`src/tools/video-editor/commands/genericPatchCapture.ts:117-162`, while its rich
`clip.update` (hold + text + geometry + label + app metadata) is not one of the
supported shapes at `:129-149`.

`captureGenericPatch` then refuses the batch at
`src/tools/video-editor/commands/genericPatchCapture.ts:517-545`, specifically
`:526-536`, before owner resolution and before any authored write. Consequently
the compiler never gets the chance to merge the hold/host fields and the
publication path never receives this producer's row.

The narrow HOME/App-owned seam is the dispatch/classification boundary in
`useTimelineOps.ts`, not Runtime and not the shared persisted-row schema. The
existing producer patch family must remain on the legacy compiler/save route
until its whole batch has an explicit native command contract. Any future change
should be scoped to this unported producer family and preserve the generic
port's atomic refusal for genuinely mixed ordinary patches; it must not infer or
silently assign an owner.

## Mapping 0433 correction

The empty-owner semantic defect belongs to Agent's provider. Runtime independently
reviewed that behavior; this App trace does not add or propose a second Runtime
writer. The App finding here is only the producer-batch dispatch regression and
the existing `app.__generated__` carrier boundary.

## Verification and limits

Targeted App tests passed:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/timeline-reader.planner-contract.test.ts

Test Files  6 passed (6)
Tests       490 passed (490)
```

No browser, full, live-socket, or product integration suite was run, as required.
No source/pin/schema activation, DTO/store, or duplicate empty-owner audit was
performed.
