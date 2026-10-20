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

## Requester continuation seam

App-owned source investigation, `app-m2-auto-requester-bindings-design`; design
only. Source aliases below are exact commits, not requested dependency pins:
App **P** `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff`; staged D13 **D**
`c195d1ee19464692712857d65648e91a9b93bee3`
(`tl/app-m2-render-continuation-outbox-stage`); Agent **A**
`7261b4ad5827466b2e17f1a30bf35d2fd05e0700`; Runtime **R**
`1f3e64d0c5f681d056dc0154748dbef5714cd6fa`. App paths are relative to
`/home/user/work/wt/app-m2-auto-requester-bindings-design`, Agent paths to
`/home/user/work/agent`, Runtime paths to `/home/user/work/runtime`.
The original policy findings above remain unchanged.

**Actual ingress and existing durable facts.**

| Source | Observed path / consequence |
| --- | --- |
| P: `src/tools/image-generation/hooks/useImageGenSubmit.ts::useImageGenSubmit` → `src/shared/lib/taskCreation/imageGeneration.ts::createImageGenerationTasks` | Image submission composes a producer-owned admission at `/generation/compose`, then calls `createTask`. Travel uses `src/tools/travel-between-images/components/ShotEditor/services/generateVideoService.ts::generateVideo` → `src/shared/lib/taskCreation/travelGeneration.ts::createTravelGenerationTask` → the same boundary. These carry generation/shot lineage, not an approved canonical timeline placement. |
| P: `src/shared/lib/taskCreation/createTask.ts::createTask`, `src/integrations/astrid/taskRoutes.ts::AstridLocalTaskRoutes.admit` | Despite stale comments mentioning `/projects/:slug/tasks`, the actual POST is `/v1/tasks`. `createTask` validates capability/input authority, allocates a UUID **idempotency key**, retries twice with that in-memory key, and returns task IDs/status. It does not allocate a task ID or persist the request/key/run locator. `admit` normalizes the closed envelope before serialization and projects away the mutation receipt. A reload/new call allocates a different key. Recovery must replay the already prepared bytes/key, without repeating fresh-admission validation/composition. |
| R: `runtime_protocol/service.py::RuntimeService.create_task`; `runtime_protocol/store.py::RuntimeStore.create_task` | Runtime allocates `run_id` and `task_id` with `new_id()` inside admission, records `task.create` identity/receipt atomically, and compares persisted admission identity on replay. The requester must store the admission reservation **before knowing either ID**, then persist returned IDs. Expired/missing replay evidence is a visible refusal, never permission to allocate a new key automatically. |
| A: `astrid/sdk/invocation.py::invoke`, `_kernel_invoke`, `_generation_publish_effect`; `astrid/sdk/remote.py::RemoteTasks.create/prepare_admission/dispatch_admission`; `astrid/sdk/workspace_client.py::WorkspaceClient.prepare_task_admission/dispatch_task_admission` | SDK/agent generation requests already use ordinary Runtime admission, with producer-declared generation selectors and settlement effects. `invoke(recovery_path=..., resume=True)` reuses `astrid/sdk/recovery.py::AdmissionReceipt.freeze/locate/recover_task`: frozen prepared arguments before send, then exact task/run locator, authenticated realm and one local lock. This existing SDK recovery is not an App owner or automatic-placement grant. No current Python author of `placement_intent`/`timeline_placement` was found. A standalone agent remains its own requester; App must not adopt its tasks by scanning a project. |
| P: `src/tools/video-editor/hooks/useAgentSession.ts::useSendAgentMessage` | Agent chat captures project/timeline context and retries the captured message in memory; `agentStore.prompt` and view-lifetime fencing do not persist an automatic-placement task continuation. Chat context, gallery add links and `shotId` cannot supply missing auto-approval/owner/raw references. |
| P: `src/tools/video-editor/hooks/useTimelineCommandSession.ts::useTimelineCommandSession`; `commands/commitSession.ts::createTimelineCommandSession`; `commands/commitOutbox.ts::createCommitOutbox` (the latter two under `src/tools/video-editor/`) | The real command owner uses authenticated `getRecoverableIdentity()` plus the canonical document's project/timeline and head pair. IndexedDB `astrid.command-outbox` / `owners`, browser exclusive lock and claim generation already retain original captures, reserved commit bytes/key and ACK. Recovery currently lists only owners with `intents` or `pending`; a task-only or accepted-only continuation would be invisible. |
| P: `src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.ts::createTaskEventPoller/readyRuntimeTaskEvents`; adjacent `useRuntimeTasks.ts::pollRuntimeTasks` | Events are wakeups; the cursor/pending IDs and QueryClient task cache are in memory. Startup establishes a feed cursor then reads the full list; visibility/reconnect/list refresh repairs display state. `src/shared/realtime/RealtimeConnection.ts::RealtimeConnection` also keeps snapshot maps in memory. Neither path persists requester authority or resumes an edit. Reopen must reread **saved task IDs**, independently of a historical event being delivered again. |

**Exact completion discovery, without a new provenance carrier.** At R,
`RuntimeService.settle_attempt` checks task/attempt/lease/fence/epoch;
`RuntimeStore._settle_attempt` atomically persists result, managed associations,
generation publication and `task.completed`. `_apply_settlement_effect` returns
exact IDs in `result.generation_publish_v1.publications[*].variants[*]`, or
`result.generation_variant` for create/append effects. Decode that normal task
result from `AstridRuntimeClient.getTask(savedTaskId)`; select the output using
the **original admitted** group/selector/variant key/output port/ordinal, never
array-first or current primary. Multi-output approval must specify which outputs
may be placed; absent/ambiguous publication remains pending/refused.

Use `AstridRuntimeClient.listManagedOutputs(savedTaskId)` (all pages) to match
the exact task, settled attempt, publication IDs/object and declared output.
The existing `getProjectMediaSelection(projectId, {association_id, object_id,
version})` uses the association's **lifecycle version**, not task version
(P: `src/integrations/runtime/client.ts` and `timeline-commit-types.ts`). R:
`runtime_protocol/timeline_commit_port.py::MediaReads.selection`,
`_output_selection_binding`, `_selected_project_media`, `selected` already
resolve the five-field selection and recheck settled attempt, provenance and
registered variant under commit authority. The catalog pin includes this managed
binding; retain it for the normal Agent media capture and acceptance recheck.
Do not create an App hash, synthetic attempt fence or render-proposal DTO.
P's `src/integrations/astrid/runtimeReadModels.ts::runtimeOutputs` maps output
`digest` into `media_id`; `bridgeTaskOutputs.ts::readBridgeTaskOutputs` then calls
that `_variant_id`. That display projection is **not a canonical variant ID**.

**Smallest reuse: extend the existing owner record, not another queue.** D's
`commitOutbox.ts::append/dispatch/reserveRenderAdmission/recordRenderTask` proves
the local storage pattern: finite detached JSON, exact method/path/body/key,
immutable locator, lock/generation fencing, and an ACK transaction that preserves
a continuation independently of rolling `accepted`. D is storage-only and starts
from an accepted command; its render-specific methods cannot represent an initial
generation request. Add only the corresponding pre-admission continuation state
to the same `owners` record/transactions, without a dummy command/ACK or a new
database, journal, coordinator, server task dependency or automatic-trigger API.
The following are conceptual local states, **not new wire names or API methods**:

| Transition | Durable requirement before advancing |
| --- | --- |
| Explicit request → reserved admission | Under the requesting owner, persist authenticated realm/actor, canonical project/timeline, original revision/publication and authoring closure, explicit canonical media owner, raw anchor/lane and fallback references (including explicitly absent alternatives), approved policy/output selection and auto-approval. Freeze the producer's prepared admission bytes/key before task POST. If the user starts over unsaved edits, finish the ordinary save/ACK first or preserve their existing dependent basis; never pretend preview is an accepted head. Refuse before admission if bindings, approval or storage are unavailable. |
| Reserved → admitted/waiting | Dispatch the saved normal task request; atomically attach the validated original task/run locator to its reservation. Unknown outcome keeps the reservation. Do not store credentials or worker lease authority. |
| Waiting → captured/queued | Reread the saved task and exact output binding. With the original approved closure/references, invoke the Agent-owned deterministic automatic capture required above, reserving birth IDs once. Atomically append its original guarded command batch into the **same** owner's ordinary command queue and link that intent ID to the continuation. Crash before this transaction leaves nothing queued; crash after it resumes that intent, never recaptures it. Captured commands, pin and IDs become durable before commit dispatch. |
| Queued → accepted | `dispatch` reserves the ordinary `/v1/.../commit` request/key. Its ACK transaction must also retain the continuation→intent→accepted result linkage before pruning flight/intent. A later B/C acceptance cannot erase it. Duplicate notifications see queued/pending/accepted linkage, rather than enqueue another birth. Undo does not re-arm the continuation. |
| Recovery / refusal | Extend existing owner discovery/filtering to include unfinished task continuations and retained accepted linkage, under the saved realm/actor/project/timeline. Reuse explicit owner recovery and the same browser lock; do not attach work to whichever editor is active. A finite resume pass when the authenticated requester reconnects, and the existing task read wakeups, suffice. Storage failure prevents posting; authorization/scope change, cancelled/failed task, missing output or stale capture leaves visible retained work. Only the server may rebase original recorded intent. |

The existing session has only clip-move ingress at P; the batch ingress/capture,
atomic linkage and continuation discovery above are **required implementation**,
not capabilities supplied by D. Render proposal custody explains one related
authority seam; it does not authorize reusing `producer.guard`, admitted-target
fields or render artifact names for ordinary generated-media placement. Any
additional task guard beyond normal selected-media authority must be supplied
by the Agent/Runtime owners; App invents no wire field/opname here.

**Acceptance obligations and scope block.** These are future acceptance cases;
this source investigation ran no behavior tests.

| Case | Required outcome |
| --- | --- |
| Original success | Explicitly approved local-door request completes; the exact completed variant is added once through the requesting outbox with the original anchor/fallback/lane and image/video semantics above. Canonical reload and guarded undo/redo succeed; zero edge/snapshot timeline writes. No approval means output completion only. |
| Editor closed / App closed | Durable task continuation survives editor unmount and page close; generation can settle while no App is running. Reopen with the same authenticated identity recovers the saved owner/task and commits once without opening the original editor first. **No requesting client running means no placement at completion time.** This differs from the former edge behavior; immediate placement while all requesters are closed cannot be promised within local-door/client-only authority. Manager must route that timing gap; no edge writer is revived. |
| Reload / reconnect / other timeline active | Resume task-only and accepted-only owners; reread exact task even if the event cursor/cache vanished or task pane never mounted. Preserve original target when head advanced to C; server rebase or visible conflict, never capture against C or retarget to the current editor. A competing tab cannot claim the same owner. |
| Lost task-admission ACK | Reopen after task POST but before locator persistence: resend original prepared bytes/key, recover the same task/run, then attach locator. Changed bytes/key input or expired replay window refuses visibly. No new generation task is silently admitted. |
| Lost commit ACK / duplicate completion | Reopen after accepted commit but before ACK persistence: replay exact pending commit/key; recover original accepted result and record linkage atomically. Duplicate completion before capture, during append/flight and after ACK (also after newer C/undo) never allocates another birth or a second accepted placement. Rollback of append/linkage or ACK leaves the preceding recoverable state intact. |
| Wrong origin / attempt / scope | A stale/superseded attempt or changed managed binding refuses through normal Runtime authority; completed accepted replay follows normal receipt rules. Different actor/realm/project, unapproved output and absent canonical owner bindings never become permission to commit. |

**Local door versus Supabase origin:** P's
`supabase/functions/create-task/index.ts` is a 410 tombstone, although unused
resolver `resolvers/shared/lineage.ts::applyLineageFields` still copies old intent
shapes. `supabase/functions/complete_task/generation.ts::createGenerationFromTask`
can create legacy Supabase generations/variants; `handler.ts::handleCompleteTask`
does not persist its `completionAsset` as a Runtime association/requester link,
and its HTTP success body has URLs/follow-up status, not a canonical variant pin.
A Supabase task UUID, URL or `source_task_id` is not a Runtime task/run/managed
output identity. No existing verified cross-origin mapping or approved requester
continuation was found. P's `imageGeneration.ts::assertComposeAvailable` and
`src/shared/components/RuntimeConnection/copy.ts::composeDisabledReason` also
disable image composition when `runtimeOrigin() !== ''`; same-origin local
generation is a distinct supported ingress from a hosted page using the door.
`src/app/runtime/runtimeAuthority.ts::resolveRuntimeAuthority` selects authority
explicitly, not from ID shape.

Consequently this design can restore only requests originating with an explicit
authorized local-door requester and durable bindings. Old hosted/Supabase-only
tasks with no reachable authorized door, canonical owner and imported managed
variant are an **authorized-scope block**, not an App adapter omission fixable
with polling. The manager must obtain a scoped migration/import/requester decision
for those tasks; the plan's deferred hosted relay and deleted edge timeline
writer remain out of scope. Keep the existing placement writer pending the
original capture dependencies and real requester/recovery qualification.
