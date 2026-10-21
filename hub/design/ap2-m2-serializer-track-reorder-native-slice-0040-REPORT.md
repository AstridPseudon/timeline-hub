# App M2 track-reorder serializer producer slice

## Disposition

**Held: no current pinned native recipe exists for track collection reorder.**
The App row-local producer remains the existing `config` mutation in
`useTimelineTrackManagement`; no source deletion, serializer bypass, or new
operation was added.

The smallest candidate slice is the media-only row reorder path
(`handleMoveTrack(activeId, overId)` without `lanes`). It changes only the
ordered `config.tracks` collection. The mixed media/data-lane path also changes
`config.app.timelineDataLanePlacement` and must remain on the guarded legacy
path until a native contract covers both authored collections atomically.

## Executable mismatch

The current App behavior is positive and already tested:

```ts
const before = {
  tracks: [
    { id: 'V1', kind: 'visual', label: 'V1', opaque: { keep: null } },
    { id: 'V2', kind: 'visual', label: 'V2', opaque: { keep: false } },
    { id: 'A1', kind: 'audio', label: 'A1', opaque: { keep: 0 } },
  ],
  // clips, registry, root extension fields, and all track objects are retained
};
const after = { ...before, tracks: [before.tracks[1], before.tracks[0], before.tracks[2]] };
```

`handleMoveTrack('track-V1', 'track-V2')` emits `type: 'config'` with that
exact permutation, preserving the clip collection and each raw track object.
`serializeForDisk` followed by `buildTimelineData` preserves the permutation;
this is the existing positive at
`src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts:149-161`.

The smallest apparent generic patch is not equivalent:

```ts
{
  version: 1,
  operations: [{ op: 'track.update', target: 'V1', payload: { order: 1 } }],
}
```

`classifyGenericPatch` refuses this shape because the current `track.update`
adapter accepts only a label merge. A new `track.reorder`/`timeline.reorder`
operation is not in the current App patch vocabulary, and current Agent's
operation registry exposes `track.create` and `track.set` but no track-order
operation. Therefore there is no qualified capture, command, inverse, or
preview projection to use here. Reusing `track.set` would either discard the
permutation or encode collection order as an unsupported scalar field.

## Exact Agent request

Agent should qualify one current native command for **parent authored track
collection reorder**, without changing any track payload:

- Capture the complete, unique, same-owner track identity permutation and the
  original complete permutation as a guard; reject missing, extra, duplicate,
  cross-owner, stale, and A→B→A-changed order states before any write.
- Record the synthetic authored collection property as a direct write (the
  existing R4 reference calls this `track_order`; its frozen operation is prior
  art only, not an adoption request).
- Apply only the order of existing raw track entries. Preserve exact track
  membership, object payloads, opaque siblings, root/config siblings, clip
  membership, and all absence/null/false/0 values.
- Return the normal `EditCommand` record with exact reads/selections/order,
  guarded inverse/redo and deterministic replay. The command must be previewable
  from the same captured basis, so preview and save produce the same permutation.
- Publish the operation/schema/registry entry and focused Agent tests for fresh
  capture, serialized reload, guarded undo/redo, stale order refusal, ABA
  refusal, and preservation of opaque siblings before App adopts it.

The App follow-up can then be a row-local capture/builder around the existing
`handleMoveTrack` media-only branch. It must be integrated through the
HOME-owned session/Provider/door/outbox seam by the App owner; this worker did
not edit those shared files. The lane-placement branch needs a separate
qualified native representation or an explicit refusal that retains its draft.

## Current live callers and exports

No exports or source files changed in this worker.

Relevant existing exports and their production callers, confirmed by `rg`:

- `useTimelineTrackManagement` is consumed by
  `src/tools/video-editor/hooks/useTimelineState.ts:74,352,437,1009,1289`,
  which supplies the editor operations, and by
  `src/tools/video-editor/contexts/VideoEditorProvider.tsx:802`.
- `handleMoveTrack` is passed/called by
  `src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx:363,391,907,922`
  and
  `src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx:355,382,878,893`.
- `moveTrackWithinKind` is also used by
  `src/tools/video-editor/hooks/useTimelineCommandsService.ts:28,1025`.
- The resulting `type: 'config'` mutation is consumed by the live serializer
  save branch in `src/tools/video-editor/hooks/useTimelineCommit.ts:536-553`
  and the pure preview twin in
  `src/tools/video-editor/lib/timeline-mutation-engine.ts:208-222`.

The existing `serializeResolvedTimelineEdit` and its mutation variants remain
live and were not deleted.

## Verification

Direct targeted Vitest run (no browser, socket, localhost, Runtime, or full
suite):

```sh
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
```

Result: **2 files, 46 tests passed, exit 0**.

Additional source checks:

- `src/sdk/video/timeline/patch.ts` has no reorder operation family; its track
  families are `track.add`, `track.update`, and `track.remove`.
- Current Agent `astrid/sdk/timeline/commands.py` has `track.create` and
  `track.set`, with no `timeline.reorder`, `track.reorder`, or track-order
  command. The frozen R4 branch does contain `timeline.reorder`, but it is not
  a current pinned cohort and was not ported.
- `git diff --check`: pass; worktree source is unchanged.

No full or central test service run was requested or performed.
