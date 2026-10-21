# App2 popup occurrence ADD caller seam (D01 / Gate 6)

Status: **UNAPPLIED proposal**. This document is a handoff for App2; it does
not activate a caller, add a writer, or qualify ADD/SWAP.

Source reviewed: `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf`.
The dormant assembly is from `9990054a502d23ab41c2f874ded3f9607c63b675`
(`origin/codex/handover-timeline-r4-20261019-candidate-app` ancestry in the
reviewed worktree).

## Current shared seam

The shared seam already exists and is mounted. No additional popup prop chain
is needed for it:

- `src/tools/video-editor/commands/commitSession.ts` owns
  `OccurrenceAddMediaCapturePort` and its `capture`, `finish`, and `submit`
  methods. Capture freezes the explicit owner, raw row, five-field media
  selection, local generation, and outbox basis/head. Finish revalidates the
  clean head/generation and creates the existing `occurrence.add-media`
  command. Submit enqueues that command in the existing outbox.
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts` forwards that
  port through the existing readiness fence.
- `src/tools/video-editor/hooks/useTimelineState.ts` forwards it as
  `editorOps.occurrenceAddMedia`.
- `src/tools/video-editor/hooks/useTimelineState.types.ts` carries the port in
  `TimelineEditorOpsContextValue`.
- `src/tools/video-editor/contexts/VideoEditorProvider.test.tsx` already has
  the cheap mounted check for the port and its readiness methods. Do not add a
  duplicate r61 test.

The nested popup Provider created by
`src/tools/travel-between-images/components/ShotTimelinePreview.tsx` therefore
owns the port internally. `AstridTimelineEditor -> LocalTimelineShotBrowser ->
ShotEditorView -> ShotTimelinePreview` does not need an `occurrenceAddMedia`
prop merely to mount it.

The missing caller seam is lower in the shared service assembly:

- `src/tools/video-editor/hooks/useTimelineState.ts:962` calls
  `services.useAssetManagement(...)` without the port.
- `src/tools/video-editor/hooks/useTimelineState.ts:995` supplies only the
  resulting `handleAssetDrop` to `useExternalDrop`.
- `src/tools/video-editor/hooks/useAssetManagement.ts:67` has no occurrence
  port in `UseAssetManagementArgs`.
- `src/tools/video-editor/hooks/useExternalDrop.ts:453` likewise has no
  occurrence port. `src/tools/video-editor/runtime/timelineHostServiceHooks.ts`
  types the installed/public service through that argument shape.

Those are the only missing props/context identified. They are intentionally
not changed in this handoff because the product caller belongs to App2’s
row-local files.

## Exact unapplied proposal

App2 should apply the smallest paired signature change:

```ts
// App2-owned useAssetManagement.ts
export interface UseAssetManagementArgs {
  // existing fields...
  occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
}

// shared useTimelineState.ts, only when the installed App2 hook accepts it
const assetManagement = services.useAssetManagement({
  // existing fields...
  commands: parentMediaCommands,
  occurrenceAddMediaPort: save.commands.occurrenceAddMediaPort,
});
```

The optional field is a carrier, not a fallback. App2’s occurrence branch
should use a narrow helper with this contract (the helper remains unapplied in
this branch):

```ts
async function submitPreparedOccurrenceMedia(input: {
  ownerRef: `occurrence:${string}`;
  row: Record<string, JSON>;
  preparedAsset: TimelineProvisionedAsset;
  current: TimelineData;
  occurrenceAddMediaPort: OccurrenceAddMediaCapturePort;
  getProjectVerifiedMedia: (selection: MediaSelection) => Promise<VerifiedMedia>;
}): Promise<boolean>;
```

Required order and semantics:

1. Require the explicit `ownerRef`, the explicit raw child `row`, and
   `preparedAsset.mediaSelection`. The selection must be the existing five
   fields (`asset`, `generation_id`, `variant_id`, `object_id`,
   `catalog_digest`); do not look up “latest” media or infer an owner.
2. Call `capture({ ownerRef, row, media: preparedAsset.mediaSelection,
   current })`.
3. Await the already-scoped verified-media read with the exact selection.
4. Call `finish(basis, verifiedMedia)` and then `submit({ command, preview })`.
   `submit` is synchronous and uses the existing outbox; do not add a POST,
   writer, store, or local snapshot.
5. Return `true` only after submit succeeds. The existing drop boundary must
   `await` this promise before reporting success or seeking the drop position.

If capture, the verified read, finish, or submit refuses, preserve the draft,
surface the refusal, return `false`, and do not call the old placement writer
for that same explicit native attempt. There is no local snapshot fallback.
Before the native branch is selected because the port is absent, App2 may
retain the existing non-native route; after explicit native selection, refusal
must not silently fall through to it.

The raw row must come from the approved occurrence newborn/birth carrier. Do
not fabricate a legal row from display geometry or `removeClipId`: preserve
the row’s explicit `id`, `track`, `clipType`, `asset`, `at`, and `hold`, plus
the existing video `from`/`to`/`speed` fields when present. In particular,
`buildAssetDropEdit` currently produces ordinary visual-drop rows, while the
Agent occurrence validator requires the approved occurrence shape; App2 must
use the reviewed carrier rather than invent a normalizer or duplicate writer.

`removeClipId` and `uploading-*` are transient cleanup identities only. If a
file path creates a placeholder, remove it in `finally` only while
`isTransientUploadPlaceholder(current, placeholderId)` is true. Never use that
placeholder ID as the canonical occurrence row ID, and never delete a
persisted row on a refusal. The file input still clears its value after the
chooser callback as it does today.

## Every popup manual File/gallery entry point

The later App2 caller review must account for all of these paths. Each is a
candidate only when it resolves to one explicit occurrence and one approved
raw row; otherwise it remains on its existing path or refuses visibly.

| Entry point | Current path | Proposed caller treatment |
| --- | --- | --- |
| Popup **Add Images** chooser at `src/tools/travel-between-images/components/Timeline/TimelineContainer/components/TimelineBottomControls.tsx:99-108` | `onFileDrop(files)` -> timeline file-drop handler -> `useExternalDrop.onTimelineDrop` -> `external-drop-utils.handleFileDrop` -> image/video upload -> `prepareGenerationForDrop` -> `handleAssetDrop(..., preparedAsset, skeletonId)` | Await one native occurrence submission per approved media item. Clean only the transient skeleton in `finally`; no fallback after native refusal. Generic non-image/video files have no five-field media selection and are not occurrence ADD. |
| Desktop File drag/drop on the popup timeline | `useExternalDrop.ts:612-655` -> `dispatchTimelineDrop` -> `handleFileDrop` (`external-drop-utils.ts:300-573`) | Same contract as the chooser. Multiple files retain existing awaited/partial-drop semantics only if every native item has an explicit carrier; never mix a refused native item with a legacy writer. |
| Gallery single-generation drag | `external-drop-utils.ts:690-776` -> `handleSingleGenerationDrop` -> `handleAssetDrop(..., preparedAsset)` | Pass the explicit selection and occurrence row to the helper; await its boolean. A missing/invalid selection is a refusal, not an inferred read. |
| Gallery multi-generation drag | `external-drop-utils.ts:575-687` -> `handleMultiGenerationDrop` -> repeated prepared drops | Each item needs its own explicit owner/row/media basis. Preserve existing ordering and await each item; if the batch cannot map one-to-one, refuse before canonical mutation rather than inventing ownership. |
| Gallery `asset-key` drag | `useExternalDrop.ts:442-450` -> `external-drop-utils.ts:778-814` -> `handleAssetDrop` | A bare asset key has no five-field selection, so it cannot enter occurrence ADD without an already-carried explicit media selection and row. Do not query or infer one. |
| Gallery shot/group drag | `useExternalDrop.ts:138-262` | Final-video and image-group drops currently create ordinary rows and pin shot groups. Leave this distinct multi-row route unchanged unless App2 supplies an explicit one-occurrence carrier; do not collapse a group into one occurrence ADD. |

Guidance-video and audio pickers (`GuidanceVideoControls` and
`AddAudioButton`) are separate product paths, not visual occurrence ADD entry
points. Parent/list-level file drops outside the nested popup are also outside
this seam. Text/effect drops in `useExternalDrop.ts:107-113` are not media and
must remain unchanged.

## Acceptance boundaries

- This proposal does not activate a caller or claim ADD proof. The kept
  `15911` trace reached the real drop but recorded zero POSTs and timed out;
  it had no verified read/POST and no occurrence-branch diagnostic.
- Do not run a browser for this handoff. Do not cut a shared writer, activate a
  local snapshot fallback, or touch SWAP. SWAP accepted closure remains
  **UNKNOWN / unqualified**.
- The only new shared handoff is the optional carrier above. No new authority,
  store, DTO, owner inference, latest-media query, or legacy writer is
  permitted.
- The existing mounted Provider/readiness test is sufficient for this seam;
  App2’s follow-up should add caller tests for capture -> verified read ->
  finish -> submit ordering, refusal/no-fallback, and placeholder cleanup.
