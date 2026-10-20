# AP2-M2 prepared parent-media consumer: current shared proposal

This is the current-root shared wiring proposal for the private App consumer
candidate. It is deliberately limited to four production files; the actual
manual `addClip` consumer remains row-local in
`useTimelineCommandsService.ts`. The carrier prerequisite is the approved
App repair `42e47ae11` (original five-field selection attached only to the
qualified prepared path).

## Shared files and signatures

1. `src/tools/video-editor/commands/commitSession.ts`
   - Adds `ParentClipAddMediaCaptureBasis` with the copied authored bundle,
     raw row, original `MediaSelection`, local generation, predecessor/head.
   - Adds `ParentClipAddMediaCapturePort`:
     `capture({row, media, current})`, `finish(basis, verifiedMedia)`, and
     `submit({command, preview})`.
   - The port uses the existing `captureParentClipAddMedia` helper and the
     existing durable outbox `enqueue` path. Capture fences the displayed
     head, bundle, and raw clip identity before the verification await;
     finish rechecks those fences before preparing the one intent.

2. `src/tools/video-editor/hooks/useTimelineCommandSession.ts`
   - Exposes the existing session's `parentClipAddMediaPort` alongside the
     existing gesture ports.

3. `src/tools/video-editor/hooks/useTimelineState.types.ts`
   - Carries the optional `ParentClipAddMediaCapturePort` through the existing
     editor-ops context type.

4. `src/tools/video-editor/hooks/useTimelineState.ts`
   - Wires the session port into the existing editor-ops context.

## Consumer contract

The row-local consumer accepts only a prepared video with a supplied original
`MediaSelection`, an existing visual track, and a manual new-clip placement.
It derives the row with the existing prepared-media planner, captures the row
and selection, awaits the existing verified-media read, then finishes and
submits through the session port. It does not register assets, create tracks,
duplicate/group clips, handle popup/automatic/recovery paths, add a new API or
DTO, or mutate the draft directly.

Unqualified prepared callers retain their existing synchronous path until
their separate migrations.
