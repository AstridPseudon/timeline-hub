# Automatic placement: KEEP pending native semantics

App worker `app-m2-automatic-placement-native-gap-r1`, App base `b8064ecf1`.
Source audit only; no activation, writer retirement, release or Runtime qualification.
PLAN M2 and the persistent-ID reservation decision remain authoritative.

## Actual trigger and lost behavior

Before D03 (`git show ade7b5ff9^:supabase/functions/complete_task/handler.ts`),
successful `createGenerationFromTask` immediately ran placement **inside completion**:

1. A valid `params.placement_intent` took precedence. `extractPlacementIntent`
   and `executePlacement` in the deleted `complete_task/placement.ts` found the
   live anchor by clip ID, used its end and `preferred_track_id`, or used
   `fallback_at`/`fallback_track_id` when the anchor was absent. Missing preferred
   track with a live anchor refused; it did not select the fallback. The exact
   completed generation/variant came from `completionAsset`, not gallery primary.
2. Otherwise `applyCompletedGenerationTimelinePlacement` in the old handler used
   `params.timeline_placement.target_track` and `insertion_time` literally.
   `source_clip_id` and `intent` were logged, not resolved into a replacement:
   even `intent: "replace"` called add. Preserve this observed behavior unless
   the owner explicitly changes it.
3. Both registered an asset, called `addMediaClip`, and saved the config. A
   placement failure degraded follow-up; generation completion/billing continued.
   The old independent registry upsert could precede a failed config save; that
   partial-write defect must not be copied into the atomic command path.

Current `complete_task/handler.ts:246-252` records
`automatic_timeline_placement_retired` for either intent and performs no placement.
`create-task/resolvers/shared/lineage.ts` still transports both old intent shapes.
An `rg` of current `src` finds no author of those snake-case fields.
`shared/hooks/useRealtimeInvalidation.ts:95-150` reacts to completion by invalidating
queries, without proposing or committing edits. There is no App completion-to-command
trigger to reconnect by merely replacing `placementService` I/O. Restoring the
deleted edge writer is expressly excluded.

## Exact policies that must stay distinct

| Surface | Existing success semantics / source |
|---|---|
| Completion image | `addMediaClip` → `commands/media.ts:125-204`: five-second image hold, image opacity/manual-layout defaults. Original placement fixture: anchor at 8, hold 2.5 → new image at 10.5; absent anchor → 22.25. Exact completed variant is retained. |
| Completion video | Same builder: `from:0`, `to:asset.duration ?? 5`, `speed:1`, volume/opacity defaults. The deleted completion registry entry supplied no duration, so its normal video insertion used five seconds. This differs from using a newly verified full video duration. |
| Shared shot image **and video** | `documentPlacement.ts:223-266`: `clipType:media`, four-second hold, regardless of media duration. Registry metadata is merged/refreshed; no video source window is authored. |
| Auto lane | `ensureShotGroup`: existing shot group lane, else first existing group's lane, else first authored track, else `V1`. It neither creates a lane nor filters that first track by kind. These are legacy group policies, not canonical occurrence ownership. |
| Shared auto position | Undefined frame appends after the selected group's greatest `round(at*fps) + max(1, round(hold*fps)) - 1`, then one frame. Empty group starts at zero. Other shots on the same lane do not affect that extent. Numeric fps only; invalid/missing fps falls back to 30. |
| Shared pool | Null frame registers media and group pool membership, with no clip. `keepAsPooled:true` removes the clip and preserves membership when managed media exists. |
| Shared shift/batch | Explicit frame clamps/rounds, then increments only while a **start frame** is occupied in that shot. It permits interval overlap. Batch applies sequentially; pooled members promote; missing rows are omitted by the primitive (the outer batch adapter checks completeness). |
| Re-place / replacement | Legacy deterministic remove/recreate is not an admissible native implementation. Same unchanged media → existing `placement.move`; replacement → fresh reserved identity. Never reuse a retired ID. |

Original positive tests and inputs remain unchanged. Four added ordinary tests in
`shared/lib/placement/__tests__/documentPlacement.test.ts` pin shared-lane extent,
lane inheritance, video four-second hold, and start-frame-only shifting. These
prove legacy semantics, not native migration.

## Published captures, checked against source

Agent `hub/timeline/agent/tl/agt-m2-stack-sync-2` =
`2431ae1fcdb6c9baf568043d3c0dad7c602b0e49`:

* `native_placement_commands.py`: `placement.move` moves an existing raw clip at
  explicit global seconds. `placement.create` creates an **image only** in an
  exclusive occurrence at explicit numeric `on` and `hold`. `placement.unplace`
  removes that expression and keeps the binding. No automatic policy, pool,
  collision shift, registry refresh or lane creation is supplied.
* `native_occurrence_media_commands.py`: explicit `occurrence.add-media` can
  already insert image/video rows with a five-field verified selection. Video
  needs `from/to/hold/speed` and a sufficient verified duration. This is a usable
  explicit-video primitive, not the missing automatic selection/placement policy.
  Its occurrence/source-window/track/extent constraints still apply.
* Both birth paths require `{asset,generation_id,variant_id,object_id,catalog_digest}`.
  URL/MIME/`resolveGenerationAsset` output is not this pin. The ordinary Runtime
  `getProjectMediaSelection` and verified-media read are the existing authority.

App staged move capture at `tl/app-m2-placement-native-parity-r1` =
`9a7aee7bf95177f9c5e7b003acd3f581d3dd5c11` has `capturePlacement` /
`finishPlacement`, exact Agent golden/record parity, and explicit owner/raw IDs.
Its session has no placement port. The staged popup source at
`tl/app-m2-popup-exact-vector-confirm-r1` = `01eee706421b34a84037ca45339af522644cf5da`
has `occurrenceMediaPort` in the ordinary session, original-basis capture,
verified pins, whole-closure preview and outbox handling. Reuse that seam for
explicit occurrence media; do not copy a second queue or snapshot publisher.
Neither staged source supplies a generated-completion observer or automatic policy.
This worker's base session supports clip move only.

Runtime audited at `1f3e64d0c5f681d056dc0154748dbef5714cd6fa`:
`contract/schemas/edit-command.json` contains `placement.move` and
`occurrence.add-media`, but no `placement.create` / `placement.unplace`.
Agent's stack-sync-2 `commit.py:771-774` already requests `selected_media` for
create. Runtime's existing `timeline_commit_port.py:266-273` already verifies
declared selections through `MediaReads`; no new port or endpoint is needed.
This is source evidence of an unpublished/mismatched contract, not an
acceptance result. Broad App `EditCommand.op:string` typing does not authorize it.

## Smallest App integration recipe and exact dependencies

1. The requesting App surface must persist its explicit auto-approval and
   canonical project/timeline/head pair, owner/raw anchor/raw lane and fallback
   refs with its task continuation. Old display IDs, `shotId`, default timeline
   selection and completed gallery primary cannot supply that authority. Existing
   old payloads alone cannot unambiguously identify an occurrence or exact media pin.
2. On completion/reconnect, the requesting client resolves the completed **variant**
   through the existing immutable media-selection read, reserves new IDs once,
   and captures against its original command-session bundle. Completion discovery
   and the durable continuation must survive an App restart or closed editor;
   query invalidation is not that continuation. Duplicate completion notifications
   resume the same outbox work, never allocate another identity after acceptance.
   Task/attempt guards must come from the Agent/Runtime authority, not an App-invented
   ledger or wire field. No autonomous extension trigger framework is needed.
3. **Agent dependency:** publish the smallest deterministic capture for the
   existing completion anchor-after / absent-anchor fallback choice and shared
   append/lane/start-frame-shift policies, recording the anchor timing, absence,
   lane membership/order, extent and collision selections it consumes. Define the
   canonical pool membership representation and guarded promotion/unplace-to-pool;
   legacy pinned groups first need their recorded migration. Reuse the existing
   media birth/move/removal machinery and explicit video source-window recipe;
   add parent-media coverage for the old parent-owned completion cases. Do not
   compute an unguarded numeric `on` in App and call that automatic intent.
   Image/video holds must retain the distinct policies above. No new opname,
   query schema, guards or DTO is specified by this handoff.
4. **Runtime dependency:** publish the official Agent schema/provider/client pair
   for the selected recipe (include create/unplace only if those operations are
   consumed), reuse the existing selected-media port, and retain the immutable
   inputs needed for reload/inverse. Then qualify the real
   create/unplace and video cases, reservation refusal and task/attempt fencing.
5. **App adapter:** reuse the staged ordinary session and occurrence media seam.
   For an already explicit, exclusively owned image, use create with `hold:4`
   for shared placement or the exact five-second completion row via media ADD.
   For already explicit video use the published occurrence-media row after
   source-window validation. Existing unchanged media re-placement uses move;
   replacement uses a fresh identity. Original reads, pin, IDs, commands and
   request/key go into the existing outbox before sending `commitTimeline`.
   Preview is local; accepted reload and `timeline.inverse` determine success.
   No partial adapter is activated here because the current completion callers
   lack those explicit bindings and the automatic capture is absent.
6. Manager qualifies real current reload/undo/redo, lost ACK and restart/exact
   retry, concurrent edits, duplicate completion, and zero legacy traffic for
   each policy before removing the corresponding shared snapshot writer.

`workers/app-m2-automatic-placement-native-gap-r1/notes/automatic-placement-native.RED.patch`
contains executable ordinary positive tests for the existing shared-service
requests, success/readback and required zero-snapshot native boundary. They fail
on the real current service's snapshot writes; no expected-failure/skip marker or
fake accepted native sender is supplied. These are a red migration obligation,
not a replacement for the completion trigger or Runtime acceptance journey.
The original deleted completion placement test is also retained verbatim in
notes as historical input evidence; its removed edge imports are not runnable
current App evidence. No edge source is restored.

Targeted evidence and reproduction commands are in the worker's `notes/report.md`.
KEEP the existing general placement writer. Automatic placement restoration is
blocked on the contracts and explicit caller bindings above.
