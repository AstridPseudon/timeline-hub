# App2 popup occurrence ADD caller — bounded UNAPPLIED proposal

Status: **UNAPPLIED / stopped at missing raw birth carrier**.

This proposal is limited to the App2-owned caller files:

- `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/hooks/useExternalDrop.ts`
- `src/tools/video-editor/lib/external-drop-utils.ts`
- their direct caller tests

It consumes the already integrated `OccurrenceAddMediaCapturePort` from
`9990054a502d23ab41c2f874ded3f9607c63b675` (merged as `5ff11809e`). It does
not edit or activate session, Provider, state, or writer code.

## Intended caller contract

The caller must add a narrow async helper equivalent to:

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

The helper must require the explicit owner, raw child row, and original
five-field selection; call `capture`, await the exact verified-media read,
call `finish`, then synchronous `submit`, and return `true` only after submit.
Any refusal returns `false`, preserves the draft, and does not call the
ordinary placement route for that explicit native attempt.

For file drops, placeholder removal belongs in `finally` and is allowed only
while `isTransientUploadPlaceholder(current, placeholderId)` is true. A
persisted row must never be removed. `removeClipId` and `uploading-*` remain
cleanup identities only.

The video birth row must retain the approved carrier's explicit `id`, `track`,
`clipType`, `asset`, `at`, and `hold`; when present, preserve `from`, `to`, and
`speed`. The caller must not synthesize an occurrence row from display
geometry, `removeClipId`, latest media, or owner inference.

## HOME seam request

The smallest optional port carrier is the handoff's existing field, passed at
the HOME-owned `useTimelineState.ts:962` call site:

```ts
import type { OccurrenceAddMediaCapturePort } from
  '@/tools/video-editor/commands/commitSession.ts';

export interface UseAssetManagementArgs {
  // existing fields...
  occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
}

services.useAssetManagement({
  // existing fields...
  occurrenceAddMediaPort: save.commands.occurrenceAddMediaPort,
});
```

This is only a carrier and not a fallback. Before App2 can apply the caller,
HOME must also identify and expose the already-approved occurrence newborn /
birth result containing the explicit `ownerRef` and detached raw child `row`.
No new row builder, normalizer, owner inference, store, DTO, or writer is
requested. The current tree has no such result at any allowed caller seam;
the existing row-building code at
`src/tools/video-editor/hooks/useTimelineCommandsService.ts:520-563` is the
HOME-owned **parent** carrier and cannot be reused as occurrence ownership.

## Entry-point coverage after the carrier lands

The caller patch must cover Add Images chooser, desktop file drag/drop,
gallery single-generation drag, gallery multi-generation drag, bare
`asset-key` drag, and shot/group drag. The first four require one explicit
occurrence/carrier per native item and await each result. Bare `asset-key`
and shot/group drops remain unsupported for occurrence ADD unless they carry
the same explicit data; they must refuse or retain their existing distinct
route without inference. Guidance-video, audio-picker, parent/list-level
drops, text, and effect drops remain outside this visual occurrence seam.

## Direct tests required with a real carrier

- capture → verified read → finish → submit ordering, including no success
  before the await;
- capture/read/finish/submit refusal returns `false` and never invokes the
  ordinary writer for that native attempt;
- `finally` removes only a still-transient placeholder and leaves persisted
  rows intact;
- external-drop boundary awaits the boolean before reporting success or
  seeking; multi-item ordering/refusal is preserved.

No product patch is applied until the raw carrier is supplied and these tests
can use the real explicit owner/row rather than a fabricated fixture.
