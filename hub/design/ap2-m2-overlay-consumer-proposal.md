# M2 literal overlay consumer proposal

Status: proposal only; no App/shared source was changed.

Base: `tl/ap2-m2-overlay-strict-types-repair` at `6e592c1b1`.

## Bounded contract

This packet qualifies exactly one producer family:

- parent-owned, visual-output, effect overlay creation from
  `ElementsLibraryPanel`, with a literal element reference
  `{id, kind: "effect", revision}` and no `packId`;
- whole-row removal of that same literal overlay from the selected clip
  inspector/delete callback;
- existing `track.create` + `clip.add` for a missing visual output track,
  although the current panel path normally targets an existing selected clip
  track;
- one reserved clip ID per create gesture, one native command group, and the
  existing session/outbox retry identity.

It does not qualify selected project-pack overlays, animation placement,
transitions, fades, entrance/exit, parameter editing, media-backed rows,
occurrence-owned rows, or element detachment. Those remain on their existing
valid producers or visible refusal paths. No legacy writer is deleted by this
proposal.

The source is the approved `elementOverlayCapture.ts` helper at 423 lines. It
must be used unchanged. It preserves the complete row, params, opaque fields,
sibling order, parent clip mirrors, and native dependency guards. The native
row values come from the existing pure factory in
`runtime/element-adapter.ts`: `uniqueElementClipId`, `clipDuration`, and
`visualTrackId`; the panel must not reconstruct fixture-only rows.

## Existing caller and authority boundary

Today `ElementsLibraryPanel.tsx:50-110` calls
`editorContext.elementOperationAdapter.execute()` for both
`timeline.apply_element` and `timeline.apply_transition`. The current
`element-adapter.ts` path does one legacy whole-document CAS save. The current
panel test reaches that actual caller through `harness.execute`; it is not a
mock-only helper test.

The proposed route is selected before any native capture:

1. Find the exact published catalog entry by `id`, `kind`, and `revision`.
   A missing entry, draft, hidden/archived entry, or legacy entry refuses
   visibly without changing the draft.
2. Only an effect with no `packId` enters this qualified route. The row's
   `elementRef` deliberately omits `packId`; the exact admitted catalog
   identity is still checked before capture.
3. A selected `packId` stays on the existing producer. It is not blanket
   denied, and it is not silently converted to a literal row.
4. If the native overlay port is not mounted, the literal operation refuses
   visibly. There is no fallback after capture and no direct Runtime POST.

The callback passes the raw `TimelineData` and the original selected scope to
the session. It does not use the ACK or a refreshed display projection as the
capture basis.

## Row-local source hunks

The exact row-local proposal is in
`ap2-m2-overlay-consumer-proposal.patch`. It contains three applicable
hunks:

1. Extract/export the existing adapter's row/placement/duration/track factory
   and reuse it from the panel. The existing adapter's own mutation path calls
   the same factory, so this is not a second placement policy.
2. Replace only the literal effect branch in `ElementsLibraryPanel` with the
   overlay callback. Transition and selected-pack branches retain their
   current adapter path.
3. Wrap the existing selected-clip delete callback in `PropertiesPanelBody`
   for a literal generated effect row (`clipType === elementRef.id`, effect
   kind, no pack owner, parent scope). On native refusal it reports the error
   and does not call `handleDeleteClip`; all other clips retain the existing
   delete producer. This is whole-row delete, not element-ref clearing.

The create callback must build the row once:

```ts
const elementRef = { id: element.id, kind: 'effect' as const, revision: element.revision };
const row = buildElementOverlayRow(current.resolvedConfig, elementRef, selectedClip.id);
const captured = elementOverlay.capture({ current, operation: { kind: 'create', row } });
const prepared = elementOverlay.finish(captured);
elementOverlay.submit(prepared);
```

The delete callback passes only the stable raw selector:

```ts
const captured = elementOverlay.capture({
  current,
  operation: { kind: 'delete', select: `parent/clip:${selectedClip.id}` },
});
const prepared = elementOverlay.finish(captured);
elementOverlay.submit(prepared);
```

The session reserves the command batch's IDs once. The callback never calls
`crypto.randomUUID()` and never derives a new suffix on retry.

## Shared-port proposal (four files maximum)

The separate shared proposal/signatures are in
`ap2-m2-overlay-shared-port-proposal.md`. It touches exactly these existing
seams, after the approved literal `elementGesture.ts` port lands:

1. `src/tools/video-editor/commands/elementGesture.ts` — add the overlay
   operation/basis/port types beside the existing literal element port;
2. `src/tools/video-editor/commands/commitSession.ts` — implement the
   overlay port with `captureElementOverlay` /
   `captureElementOverlayDelete`, `finishElementOverlay`, and the existing
   `prepared` map plus `enqueue`;
3. `src/tools/video-editor/hooks/useTimelineCommandSession.ts` — apply the
   existing legacy-clean barrier to capture, finish, and submit, and expose
   the callback through `TimelineCommandSessionSurface`;
4. `src/tools/video-editor/hooks/useTimelineState.ts` — expose the callback
   on the already-existing `chrome.commandSession` surface consumed by the
   panel. No new store slice, DTO, serializer, or Provider automatic-host
   construction is introduced.

The shared port accepts one operation union and one prepared submission shape;
it is not a generic arbitrary-command submit API:

```ts
export type ElementOverlayOperation =
  | { kind: 'create'; row: Record<string, JSON>; track?: Record<string, JSON> }
  | { kind: 'delete'; select: string };

export type ElementOverlayCaptureBasis = {
  readonly operation: ElementOverlayOperation;
  readonly bundle: AuthoredBundle;
  readonly commands: readonly EditCommand[];
  readonly localGeneration: number;
  readonly localBasis: OutboxBasis;
  readonly previewVersion: number;
};

export interface ElementOverlayCapturePort {
  capture(input: { current: TimelineData; operation: ElementOverlayOperation }): ElementOverlayCaptureBasis;
  finish(basis: ElementOverlayCaptureBasis): {
    commands: EditCommand[];
    bundle: AuthoredBundle;
    preview: TimelinePatch;
  };
  submit(input: {
    commands: readonly EditCommand[];
    preview: TimelinePatch;
  }): void;
}
```

`capture` records `before` and the local outbox predecessor. `finish` executes
the frozen helper basis against its original bundle and stores the exact
`commands + before + after + preview` in the existing prepared map.
`submit` accepts only the exact prepared command group, generation, and
preview, then calls the existing `enqueue`. A retry resends the stored body
and key. No capture runs after an acknowledgement, and no Runtime route is
called by the panel.

For the preview, using the captured `current.configVersion`, `track.create` maps to one `track.add`, `clip.add` maps to
one `clip.add`, and `clip.delete` maps to one `clip.remove`, all at the
current preview version. Preview is local-only and is not a second writer.

## Admission and refusal details

- Literal: catalog entry must be exact, published, non-legacy, effect kind;
  element row has no `packId`; native helper is allowed.
- Selected pack: existing adapter remains the producer until the authenticated
  Agent `realm_id`/`schema_source`/`schema_inputs` tuple is forwarded. No
  local schema cache or caller-side admission is added.
- Missing/non-output/inactive track, occupied reserved ID, unsupported media,
  unsupported timing/relations, nested ownership, or unsafe delete dependency:
  native visible refusal with original draft/basis preserved.
- Delete is only whole overlay-row deletion. `clip.set-element` is never used
  to emulate element detach.

## Verification plan and current evidence

Current-root evidence:

- `vitest ... elementOverlayCapture.test.ts ... ElementsLibraryPanel.test.tsx`
  — **7 files, 247 tests passed**.
- ESLint on the helper, focused helper test, panel, and panel test — **passed**.
- `tsc -p tsconfig.app.json --noEmit --pretty false` — **exit 2** from the
  known unrelated `elementCapture.ts` error and Composition integration
  errors; no `elementOverlayCapture.ts` or `ElementsLibraryPanel` error.
- Actual current-root TypeScript-produced native probe against read-only Agent
  310 and `/home/user/work/venv-app2-native` — **add/delete validate and
  execute accepted; command, record, bundle, inverse, replay, and round-trip
  exact**.

The following consumer gates are intentionally open and must be run after the
shared seam and row hunks are applied in a private candidate:

- mounted `ElementsLibraryPanel` effect apply reaches the callback with the
  original raw basis;
- selected-pack apply still reaches the original adapter producer;
- a literal overlay create has zero legacy adapter/route calls;
- a literal overlay delete has zero legacy calls and preserves unrelated rows;
- exact retry sends the same grouped body and idempotency key;
- Runtime acceptance -> reload -> guarded undo for create and delete;
- browser gate and live socket journey.

No broad matrix, full suite, browser, localhost, or live-socket suite was run.
