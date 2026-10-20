# App M2: native `track.create` ingress map

Status: design/source audit only. No product code is changed by this worker.

The native capture, session staging, and metadata-preservation work is present at
`d73783d10`, `1e91a4c14`, and `5a648a425`, composed at `74c21c62`. Those changes
prove the command shape and durable-session seam; they do not make every App
track-birth gesture a native `track.create`.

## Decision

The smallest complete consumer cut is the two explicit footer actions,
`+ Video` and `+ Audio`. They are the only bounded UI journey whose semantic
edit is currently just “append one parent-owned track row.” The cut should pass
the complete authored row through the existing `trackCreatePort` and normal
session/outbox path, with the row id allocated once and reused for retry.

The facade, `TimelineOps`, context-menu extension route, bottom-track clip
gestures, media drops, and group/retrack paths stay outside this cut. They either
accept insertion/order or combine track birth with another edit. They must not be
made to look native by issuing independent `track.create` requests. Compound
create-plus-move/add work belongs to the next worker and must remain one grouped
operation with guarded inverse ordering.

This document does not add a wire operation, guard table, id mapping, or
compatibility writer. The current M2 merges remain open; no candidate is retired
until the integrated Runtime has demonstrated reload, undo, retry, and zero
legacy traffic.

## Native contract and proven subset

`src/tools/video-editor/commands/trackCreateCapture.ts` captures a native
`track.create` with exactly one argument, `row`. The native assertions require:

- schema version 1, op `track.create`, command version `1`, `select: "parent"`,
  and an empty intent;
- a complete JSON row with a non-empty id and kind, and no `/` or `::` in the id;
- the authored raw parent `config.tracks` collection as the basis;
- a selection guard over the existing raw parent track refs, retaining their
  exact membership, order, and boundaries;
- an absent guard and direct authorship for `parent/track:<new-id>`;
- the full supplied row written to the raw parent collection and recorded as a
  created track.

Capture executes and then checks the supplied claims. Finish replays the frozen
basis and the same authored row; it does not recapture after acknowledgement.
The session rejects a duplicate id in either displayed `config.tracks` or
`resolvedConfig.tracks`, preserves the prepared preview, and enqueues the exact
native command. These are the useful retry and lost-ACK properties, not evidence
that all callers are migrated.

The native subset is therefore:

1. one new parent-owned track;
2. one stable, complete raw row;
3. append semantics (there is no insertion index or reorder claim);
4. one command/session intent with the normal outbox lifecycle.

It does not include child or occurrence-owned tracks, a move, media placement,
group retrack, an insertion position, or an atomic batch. A sequence of separate
submits is not an atomic create-plus-consumer edit and is not an acceptable
substitute.

## Authored source versus derived UI

The capture basis is the raw parent revision payload produced by
`authoringBundleFromDocument`. `config.tracks`, raw clips, opaque fields, nulls,
unknown siblings, and parent metadata are authored facts. The native golden
fixture intentionally retains those facts.

`resolvedConfig`, `rows`, `meta`, `clipOrder`, `dataLanes`, `output`, asset
registries, source items, transcript references, and the accepted/local head
pair are projections or session facts. `assembleTimelineData` rebuilds them for
preview; they are not alternative authorship for the native command. The
track-create preview retains these projection facts while adding the complete
row to both config and resolved preview views. It must not replace the raw row
with the smaller display row.

There are two related selection details worth keeping explicit:

- explicit Add Track currently constructs a display/default row through
  `editor-utils.addTrack`; the native consumer must turn that into the complete
  authored row once, before capture, and keep the allocated id stable;
- a moving shot/group is occurrence-owned work. `pinnedShotGroups` is a
  migration-only legacy view; the canonical ownership is the occurrence and its
  child tracks. It cannot be represented by a parent-only create command.

## Exact ingress map

| Caller | Current behavior and source | Native `track.create` decision |
| --- | --- | --- |
| Timeline footer `+ Video` / `+ Audio` | `TimelineCanvas.tsx` invokes `onAddTrack`; `TimelineEditorCoreBody.tsx` passes the read-only-guarded `handleAddTrack`; `useTimelineTrackManagement.ts` calls `addTrack(resolvedConfig, kind)` and `applyEdit({type: 'config'})`. | **Smallest consumer cut.** Replace only this final mutation handoff with the existing track-create port. Preserve explicit Add Track’s output-role/default row semantics. |
| Public `TimelineCommands.addTrack({kind, index?})` | `useTimelineCommandsService.ts` computes a new resolved config and applies a config snapshot. The optional `index` is meaningful behavior. | **Not in the cut.** Native create has append-only semantics. The facade needs a separately designed ordering/compound migration; do not silently drop `index`. |
| `TimelineOps` `track.add` | `useTimelineOps.ts` validates/compiles the patch, then sends all non-label operations through `commitData(..., {save: true, semantic: true})`. | **Legacy/unsupported.** `track.add` is a patch vocabulary, not proof of native `track.create`. Do not add a compatibility writer at this seam. |
| Context-menu route | SDK context-menu contributions can dispatch timeline commands/ops, but App has no separate built-in track-create callback in the audited sources. A contribution reaching the facade or `TimelineOps` inherits that caller’s legacy behavior. | **Not a separate native caller.** It becomes native only when its concrete command is migrated; do not claim context-menu coverage from the existence of the menu contribution API. |
| Clip bottom-drop / new-track drag | `useClipDrag.helpers.ts` explicitly refuses `dropPosition.isNewTrack` / `plan.needsNewTrack` for native `clip.move`; `useTimelineTrackManagement.ts` has legacy create-and-move helpers. | **Unsupported by create alone.** Requires one grouped create-plus-move command. Keep the refusal and legacy path unchanged in this worker. |
| Free clip `createTrackAndMoveClip` | Allocates a new V/A id, creates a row, and moves a clip in one local legacy `applyEdit`; it can preserve the source track role. | **Compound next worker.** It is not safe as two independent submits. |
| Group drag / group retrack | `translateGroupMembers` changes multiple rows, clip order, metadata, and `pinnedShotGroupsOverride`; original new-track positives remain in `useClipDrag.test.tsx`. | **Unsupported.** Canonical occurrence ownership and child-track updates must be atomic. |
| External text/effect/file drop | `external-drop-utils.ts` calls `createTrackForDrop` when no compatible track exists, then performs placement or metadata work. | **Unsupported compound path.** Track birth is subordinate to text/effect/media placement. |
| Generation/shot/media drop | `planAssetDropTarget` allocates a track in a prepared derived config; `useAssetManagement.ts` then applies media placement (`add-media` / `place-prepared-media` or rows). | **Unsupported compound path.** Do not serialize those local media command names as Runtime wire operations. |
| Audio detach fallback | `editor-utils.ts` can call `addTrack(..., 'audio')` while detaching audio if no audio track exists. | **Unsupported compound path.** The birth is part of detach/audio placement, not an independent append. |
| Track reorder/remove/label/popover edits | Track management has separate legacy mutations; label has its own native port. | **Out of scope.** They are not track birth and must not be folded into this map. |

The “exact live” distinction matters: `handleAddTrack` is wired from the visible
footer, while `createTrackAndMoveClip` and the external-drop helpers are exposed
legacy ingress capabilities even where the current drag controller refuses the
new-track case. They are mapped so future migration does not mistake a helper or
test fixture for a completed native consumer.

## Smallest UI wiring and real-journey handoff

The next implementation should keep the existing footer chain and change only
the edit handoff:

1. Read the current raw/session bundle and resolved display state at the gesture
   boundary. Build the full authored row using the explicit Add Track defaults;
   allocate its id once. Do not derive a new id on retry or from a later
   `resolvedConfig` snapshot.
2. Call the existing `trackCreatePort.capture`/`finish`/`submit` seam with that
   row. The preview should use the complete row and preserve data lanes,
   metadata/transcript/source facts, root opaque data, registry/asset map, and
   accepted head/local edit projection as already covered by the native preview
   tests.
3. Keep selection on the newly created track after the local preview. The
   explicit Add Track journey has output-role semantics; do not borrow the
   source-role behavior used by a clip move.
4. Do not change `createTrackAndMoveClip`, external drops, group drag, or the
   current `clip.move` new-track refusal in this cut.

The real journey handoff for integration is:

`+ Video` or `+ Audio` click → App command request through the normal `/v1`
Runtime door → local preview with the complete row → lost-ACK exact retry and
restart/recovery → accepted reload showing the raw row and preserved opaque
facts → guarded undo. The trace must show no legacy `saveTimeline`/snapshot
`commitData` traffic for this exact gesture. It must also prove Runtime reload,
undo, retry, and zero legacy traffic after the candidate is actually integrated;
this source audit cannot provide that gate evidence.

For create-plus-move/add, the later grouped design must use consumer-first
inverse ordering, LIFO/dependency-safe rollback, and one guarded batch. It must
not submit N independent creates and consumers and call that atomic.

## Original positives and source-audit evidence

The native positive coverage remains in:

- `commands/trackCreateCapture.test.ts`: exact golden command/after-bundle,
  frozen replay, full row/null/opaque preservation, parent selection guards,
  and refusal cases;
- `commands/trackCreateGesture.test.ts`: exact submit/preview shape and
  preservation of data lanes, source items, transcript refs, root opaque config,
  registry, asset map, and accepted/local head facts;
- `commands/commitSession.trackCreate.test.ts`: lost-ACK/reload/recovery,
  retry identity/body, fresh dependent keys, and server parent tracks;
- `hooks/useClipDrag.test.tsx`: the three original group/new-track positives,
  unchanged as `it.fails` until the required grouped implementation exists:
  free multi-clip drag to a new bottom track, pinned group across tracks, and
  pinned group onto a new track.

This worker ran the bounded existing tests only:

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 \
  src/tools/video-editor/commands/trackCreateCapture.test.ts \
  src/tools/video-editor/commands/trackCreateGesture.test.ts \
  src/tools/video-editor/commands/commitSession.trackCreate.test.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts
```

Result: PASS, 5 files, 93 tests, Vitest 4.1.5, 9.70s. This is regression
evidence for the existing seams and caller behavior, not a claim that the
footer is already wired to native capture or that Runtime integration has
passed.

