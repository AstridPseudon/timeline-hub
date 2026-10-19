> Owner update 2026-10-19 ~23:11Z: PURGE every Supabase canonical writer in ai-timeline-agent, timeline-import, complete_task append+registry upsert and shared astridAppendService; delete retired write tests/docs, keep completion/billing/media preparation/relational metadata and make retained edge tests import/pass. Four isolated workers active; not integrated yet. This supersedes the earlier owner-HOLD and conversion-vs-retirement uncertainty below.

# App M2 durable writer map

Status: **HELD — docs-only groundwork, 2026-10-19.** This map is audited against
App `tl/integration` at `9d0a383a1` (including the M1 restore-proof merge). It
replaces the stale M0 inventory; it does not authorize a product or schema
change. The target remains one `/v1` Runtime commit door from [PLAN](../PLAN.md).

Useful design evidence is retained in [edit-recipe.md](edit-recipe.md),
[m2-move-draft.md](m2-move-draft.md), [app-contract-consumption.md](app-contract-consumption.md),
[app-m1-coordination.md](app-m1-coordination.md), and
[commit-contract.md](commit-contract.md). PLAN wins if any wording here differs.

## Proven M1 boundary

The following is proven for the narrow same-track absolute `clip.move` slice;
it is not a claim that all App writers have migrated:

* `useClipDrag` / `useTimelineCommandsService.moveClip` capture through
  `commands/{semanticGestures,clipMoveCapture,authoringBundle}.ts` and the
  `useTimelineCommandSession` port.
* `commands/commitSession.ts` seals the original reads, selections, bindings,
  writes, immutable media/source pins and created IDs; `commands/commitOutbox.ts`
  persists the exact request/body/key and unsent suffix. The provider sends
  `POST /v1/projects/{project}/timelines/{timeline}/commit` through
  `RuntimeDataProvider.commitTimeline`, not a snapshot publication.
* Accepted undo emits the Agent-defined `timeline.inverse` command with the
  accepted publication ID. It is guarded server-side; local inverse state is
  not accepted history.

Evidence on the integrated source: `tests/e2e/local/three-products.spec.ts`
(`M1 real gesture...` and `M1 real dependency conflict...`) passed 2/2 in the
central `app-m1-journey-python-basis-e2e-m1-gesture-1019210718-13326` run;
`tests/e2e/timeline/command-outbox.spec.ts` passed 1/1 in
`app-m1-outbox-browser-full-e2e-timeline-1019191816-103`; and
`tests/integration/runtimeRestore.test.ts` passed 1/1 in
`app-m1-restore-proof-handshake-restore-integration-1019223958-23422`.
The five-case M1 closure also passed centrally on its final tuple. These prove
move/inverse/outbox/restart mechanics. They do **not** close Gate 6.

The following remain **OPEN** until their own producer emits an Agent command
through `commitTimeline`, or the producer is deleted: ordinary editor snapshot
save, add/update/trim/split/delete/track edits, asset/registry writes, popup
add/swap, duplicate/group writes, placement, element/standalone adapters,
visual seam/transcript/project-data writes, and all Supabase producers.

## Reachable writer census

Paths below are current App paths, not filenames inferred from the M0 search.

| Reachable surface | Current call chain and durable effect | Status and removal boundary |
|---|---|---|
| **Editor snapshot funnel** | `hooks/useTimelineCommit.ts` → `hooks/useTimelinePersistence.ts:399-403` → `DataProvider.saveTimelineAtHead`; `integrations/runtime/dataProvider.ts:891-1008` calls `publishParentComposition` at `/v1/.../composition-revisions`. The numeric `saveTimeline` branch is still at `useTimelinePersistence.ts:403`. | **OPEN except M1 move.** Keep command-session preview/outbox separate from snapshot recovery. Delete numeric selection and the snapshot save branch only after every editor producer below has command coverage and zero-traffic tests. |
| **Editor producers** | `hooks/useTimelineCommandsService.ts:442-1083`, `hooks/useTimelineOps.ts`, `commands/{runner,media}.ts`, `hooks/useTimelineState.ts:929-995`, `hooks/useTimelineTrackManagement.ts`, `hooks/useExternalDrop.ts`, `lib/{keyboard-delete,shot-group-commands}.ts`. These build local rows/config/registry and still feed the snapshot funnel. | **OPEN.** M1 `moveClip` is the only command-backed gesture. Add/update/delete/trim/split/track and prepared-media operations wait for Agent-published schemas and capture rules; never serialize local `TimelineCommand`, `TimelinePatch`, `add-media`, or `swap` names as wire opnames. |
| **Popup add/swap** | `travel-between-images/components/shotTimelineDataProvider.ts:435-590` implements `saveTimeline`; it calls `enqueueCanonicalShotPublish` and `shotCompositionAdapter.publish`, which reaches `publishParentComposition`. Recovery is persisted through `saveTimelineDraftIfOwner` at `:516-537`. | **OPEN.** Remove this `saveTimeline` compatibility publisher only after add and swap each have independent command-door tests; refusal must make no snapshot/legacy call. |
| **Canonical duplicate/group** | `components/AstridTimelineEditor.tsx:390-445` directly calls `runtime.shots.shotComposition.publish` for canonical duplication. The fallback `lib/shot-group-pack-commands.ts:379-418` / `:444-477` calls `mutateTimelineDocument`; `shared/lib/placement/placementService.ts:78-147` saves through `saveTimelineAtHead`. | **OPEN.** Duplicate must become a command/proposal or be deleted. The M2 group migration and occurrence moves below are the only approved route for legacy-group behavior; no direct graph publication or whole-parent replacement survives. |
| **Shared placement** | `shared/lib/placement/placementService.ts:119-239` loads, mutates and CAS-saves the document. Callers include `placeGeneration`, `unplaceGeneration`, `batchUpdatePlacementFrames`, and `lib/shot-group-pack-commands.ts:410,469`. | **OPEN.** Convert canonical placement/unplacement/frame edits to Agent commands with server rebase, or delete the writer. Its bounded client CAS loop is not semantic migration proof. |
| **Supabase append service and callers** | `_shared/astridAppendService.ts:119-163` posts `config-replaced` / `create-with-config`. `ai-timeline-agent/db.ts:716-729` exposes `saveTimelineConfigVersioned`; callers are `ai-timeline-agent/tools/registry.ts:810,840,961,1039`, `complete_task/handler.ts:105`, `complete_task/placement.ts:235`, and `timeline-import/handler.ts:249,302`. | **OPEN.** These server-side producers must propose Agent commands and reach the same Runtime commit path, or be deleted. An edge function that cannot reach the door is a blocker to escalate with evidence, never permission for a second writer. |
| **Other durable adapters** | `hooks/useTimeline.ts:31-50`, `runtime/element-adapter.ts:66-105`, `useTimelineState.persistVisualSeamConfig`, persisted transcript/project-data paths, and asset registration through `useTimelineCommit.patchRegistry` / `useAssetOperations.ts`. | **OPEN.** Convert each bounded producer or remove its provider save branch. Relational `shot_generations.timeline_frame` and `metadata.end_frame` remain outside canonical M2 scope and cannot count as command coverage. |

Local preview, IndexedDB recovery drafts and test providers are not accepted
writers. `createDefaultTimeline.ts:41-71` is explicit setup/bootstrap only.
`restoreHistory` remains the guarded `timeline.restore` adapter; it is not a
replacement for ordinary command undo.

## Current priority override — orchestrator AUDIT2216Z, received 22:50Z

M1 now additionally requires command move → ordinary legacy edit → save → reload,
with either success or a visible refusal plus durable, recoverable local work.
app-m1-mixed-edit-safety owns that real browser proof/minimal safety fix; no
Runtime compatibility writer. M2 PRIORITY #1 is every remaining writer converted
to EditCommands, then deletion of the legacy publisher; the same mixed journey
must then end in successful accepted reload and guarded undo. This supersedes
calling group moves the first App implementation item. The group dependency
sequence below remains valid within that slice, not the current global priority.

Current Next5: (1) ordinary editor track/clip producers, beginning the mixed
track-rename case, on official Agent operations/capture; (2) popup add/swap with
immutable media/occurrence pins; (3) placement plus Supabase writer disposition/
conversion; (4) remaining adapters/registry/transcript/data producers and delete
the last snapshot publisher once all callers pass; (5) canonical group migration/
occurrence/retrack/new-track/free-multi sequence and its three original positives.
Accepted-history and conflict UI/clone branches proceed independently; M2 merges
still wait for the recorded M1 gate. Missing command schemas are Agent handoff
dependencies, never permission to invent local wire names.

## Group dependency sequence and popup slice details

Each slice is small enough to branch independently where its Agent artifact
dependency is available. “Remove” means remove the named old writer after the
slice’s accepted-reload and negative zero-traffic tests pass; until then it is
visibly **OPEN**.

| Order | Slice, current App seam, and Agent dependency | Binding/immutability requirements; App exit and writer removal |
|---|---|---|
| **1** | **Lossless legacy-group migration plus read view.** App seams: `hooks/usePinnedShotGroups.ts`, `data/shotCompositionProjection.ts`, `components/AstridTimelineEditor.tsx:370-380`, and compatibility observations in `hooks/useClipDrag.test.tsx`. Agent must publish the migration command/capture/recorder and shot/occurrence root-create semantics described in `m2-move-draft.md`; its proposed `timeline.migrate-groups` name is not an App-installed schema. | Capture all original group membership/order, opaque metadata, source/media/transcript pins and exact legacy-to-canonical bindings. Allocate shot/occurrence IDs once before outbox sealing. Do not infer ownership from display IDs, tuples or load-time conversion. Derive the read view from accepted canonical occurrence/child state plus migration provenance. This slice removes no durable writer and does **not** close Gate 6; it unblocks occurrence editing. It may run independently of the later free-set slice. |
| **2** | **Existing-lane occurrence move and atomic child retrack.** App seams: `hooks/{useClipDrag,useClipDrag.helpers,useTimelineCommandsService}.ts`, `commands/{semanticGestures,clipMoveCapture,authoringBundle}.ts`, `data/shotCompositionProjection.ts`, and `hooks/useShotGroups.ts`. Agent must publish occurrence-root resolution, occurrence member/order selections, exact source-shot mapping, blocker queries and occurrence placement writes; `occurrence.move` in the draft is provisional until the Agent artifact lands. | Pointerdown capture binds `occurrence:O`, source shot/revision and every owned child in authored order; read exact source windows, speed/hold/duration, lane predicates, consumed registry/media pins and immutable occurrence closure. Move must update occurrence placement **and every owned raw child track** atomically, preserving sibling occurrences/shared shots and opaque data. Keep the three current `it.fails` assertions unchanged. When accepted reload/undo passes, remove the legacy pinned-group drag mutation/snapshot path for this slice; do not remove general snapshot saving. |
| **3** | **New-track occurrence move composed with `track.create`.** App seams are the same drag/session files plus `hooks/useTimelineTrackManagement.ts:349-617` and `commands/commitSession.ts`. Agent’s existing `track.create` is settled; the new occurrence child-lane creation and staged inverse must be published before App wiring. | Capture the parent lane ID once, reserve it, and use that same ID for the occurrence child lane; no replay allocation. Submit create + move as one group/undo unit. Read and bind exact media/source/occurrence membership and destination-lane occupancy; inverse must reverse consumers before deleting the created lane and redo the same IDs. The second existing `it.fails` test remains until this succeeds. Remove only the new-track legacy group/whole-config mutation path; the rest stays OPEN. |
| **4** | **Independent free multi-clip move.** App seams: `lib/multi-drag-utils.ts`, `lib/clip-drag-planner.ts`, `hooks/useClipDrag.ts`, `hooks/useTimelineTrackManagement.ts`, and the public command service. Agent must publish the explicit multi-member command/capture/query schema (the draft’s `clip.move-set` is provisional). | Bind a nonempty ordered set of exact parent or occurrence clip refs, one anchor, original lane membership/order, all source/media selections and collision/extent predicates. Apply one quantized delta, preserve relative offsets/source windows/opaque fields, and refuse mixed owners, shared ownership, blockers or missing immutable pins as one transaction. The third `it.fails` test remains until accepted reload/inverse/redo passes. This slice does not edit group provenance or remove popup/placement writers. |
| **5** | **Popup add/swap command conversion.** App seam: `travel-between-images/components/shotTimelineDataProvider.ts:321-590`; tests: `ShotTimelinePreview.test.ts`, popup provider tests, and the command-session/outbox tests. Agent must publish exact add and replacement/clear operations; local `add-media` and `swap` are not wire names. Runtime must provide the immutable media-selection read and accepted canonical closure needed by the command. | Add captures the exact occurrence owner, canonical head pair, source/media selection, asset identity, duration/type and all created IDs. Swap captures the exact occurrence/clip identity, old membership/source pin and replacement media selection; it must not select by display ID or refresh guards after authoring. Test add and swap separately, including missing occurrence/media pins, mixed batches, lost ACK and exact retry. On proof, remove popup `saveTimeline`, `shotCompositionAdapter.publish`, and its whole-graph fallback; retain draft recovery as command outbox recovery. |

Placement and Supabase work is a parallel **OPEN** conversion lane, not a
hidden sixth writer closure: it can proceed independently once Agent publishes
the relevant command/capture contract, but no Next-5 success authorizes their
snapshot/config append paths to remain.

## Supabase producer transport boundary (2026-10-19 audit)

Audited App worker base `fa1f7965e`; details, exact tests and the socket-free
executable probe are in
[the boundary report](../workers/app-m2-edge-producer-boundary/report.md).
**No current producer uses the normal local commit door. This is not evidence
that ordinary App editing requires a cloud relay.** Current App chat uses
`hooks/useAgentSession.ts:313,709` (local ACP), and task creation uses
`shared/lib/taskCreation/createTask.ts:324-346` (capability admission).
Production App call-site searches found no invocation of `ai-timeline-agent`,
`complete_task`, or `timeline-import`; edge entrypoints and their internal
writer calls still exist. External CLI/worker use and deployed configuration
were not checked. The census above remains an inventory of writers to remove,
not proof that these three endpoints have ordinary App callers.

`_shared/astridAppendService.ts:7-8,48-87,119-163` reads only the two
`ASTRID_APP_APPEND_SERVICE_*` variables and posts a whole config to
`config-replaced` / `create-with-config` with an internal bearer. It has no
local discovery, product-credential binding, project-scoped commit request,
base head pair, or idempotency key. The real normal client is
`integrations/runtime/generated.ts:174-176` plus
`dataProvider.ts:678-694`; local proxy/discovery supplies its product credential
(`config/vite/runtimeProxy.ts:8-25`, `scripts/runtime-discovery-proxy.mjs:46-81`).
Changing the append URL cannot convert either route/body into a commit.
A hosted edge function's loopback would address that host, not the user's
local Runtime (topology inference, not an attempted connection); a same-host
deployment is not intrinsically impossible, but no supported wiring appears
in the audited source. No environment values or secrets were inspected.

Smallest permitted follow-up: qualify and delete unused legacy canonical-write
entrypoints/wrappers, or return proposed edits to an **identified existing local
caller** for Agent capture → existing outbox → normal commit. The edge agent
already returns proposals (`index.ts:107-117`, `tools/registry.ts:512-536`), but
they are numeric-version `TimelinePatch` envelopes, not canonical EditCommands;
`importEdgeProposals` has no production caller. Completion returns URLs and
follow-up warnings (`complete_task/handler.ts:570-592`); import returns only
version/created status (`timeline-import/types.ts`). Neither has a local
proposal consumer. Do not invent one silently. Agent must publish the relevant
operation/capture and lossless-import semantics; Runtime/Agent must identify
any retained completion/import caller and immutable media/result handoff.
Delete `createTimelineViaService`, `appendTimelineConfigViaService`, and
`saveTimelineConfigVersioned` only after their remaining consumers are retired
or converted; preserve artifact storage, billing and relational placement.
Next worker: **app-m2-edge-writer-retirement**, after manager disposition of
external consumers. This audit converts no writer and leaves Gate 6 OPEN.

## Backend reachability and negative matrix

The App-only Supabase targets
`/v1/timelines/{t}/config-replaced` and `/v1/timelines/create-with-config` are
not Runtime routes. Delete their callers; do not add Runtime aliases. Direct
authenticated negative tests must use the Runtime-owned rejection matrix in
`commit-contract.md` and assert unchanged head pair, history/publication and
authored bytes. The relevant mapping is:

| Legacy reachable surface | Runtime disposition and required App proof |
|---|---|
| External `publishParentComposition` / authored `config-replaced` / snapshot overwrite | Reject, including first publication; only constrained `createTimeline` bootstrap and private commit transaction may publish. App gesture spy must show zero calls. |
| `updateTimeline`, `replaceTimelineClip`, `replaceParentCompositionMedia`, archive/recover timeline | Reject; use commands. Direct authenticated request returns the matrix error and leaves head/history/bytes unchanged. |
| Direct shot, shot-item, occurrence-like, reference, association/primary/link and text-binding routes | Reject, including unused resources and same-value writes; use command captures with exact occurrence/media/source bindings. |
| Render/task admission or settlement carrying canonical timeline/shot/reference effects | Reject canonical mutation at admission and settlement. Commit first, then use the existing revision-pinned render/task APIs. |
| `restoreProjectParentCompositionRevision` | Keep only behind guarded `timeline.restore` with the observed head pair and revision/content digest; old revision-only calls are negative cases. |
| `createTimeline` / ordinary Documents / media preparation | Keep narrow atomic empty bootstrap, ordinary noncanonical Documents and immutable media preparation. None may replace authored canonical state or act as a fallback writer. |

For each migrated App producer, add a direct spy/traffic assertion that
`saveTimeline`, `saveTimelineAtHead`, gesture `publishParentComposition`,
`config-replaced`, and any legacy Astrid save route are not called. Keep the
Runtime direct-negative matrix separate so a zero client-traffic test cannot
pretend to prove server reachability. Placement relational writes remain a
separate projection candidate and do not satisfy Gate 6.

## Concrete next-worker checks

* App command/session slices: targeted Vitest for the touched files plus
  `src/tools/video-editor/hooks/useClipDrag.test.tsx`; keep all three original
  `it.fails` tests until their canonical migration/occurrence-retrack/new-track/
  free-multi requirements pass. Add zero-legacy spies at the producer seam.
* Popup: targeted `src/tools/travel-between-images/components/ShotTimelinePreview.test.ts`
  and `ShotTimelinePreview.integration.test.tsx` tests for add and swap independently, then the
  command outbox/restart test; no snapshot fallback is an accepted substitute.
* Placement/Supabase: targeted placement and function tests must assert command
  proposal/commit calls and no `saveTimelineConfigVersioned` or append-service
  call. If the edge runtime cannot reach `/v1/.../commit`, record the exact
  transport failure and stop at the blocker.
* Agent owns unpublished operation schemas, capture queries, recorder effects,
  immutable media/occurrence binding rules and conformance tests; App must pin
  the published artifact rather than guess an opname. Runtime owns the route,
  generated DTO/artifact refresh and direct-negative rejection tests.

No full or socket suite was run for this docs-only map. Gate 6 proof remains
open, and no first group slice is represented as closing it.
