# App writer → published-command gaps

Current against App `c8566f12` and the reviewed, not-final Bundle2 tuple:
Agent `d4743e2984cef0908fa0b6bef166aa801f2bde8f` / schema
`472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`, Runtime
`d691ddadb4ef3f5881a25fa893b4fb812211f102` / client `0.2.3`. These are
read-only review inputs; no App release, paired pin, or M2 integration is
claimed. The old recovery worker left no usable tracked or shared-doc changes.

“Open” means the behavior still reaches the snapshot/document publisher (or a
legacy adapter), even where local preview or a command-shaped helper exists.
Deletion is safe only after the listed producer has accepted-reload, retry,
inverse/undo, and zero-legacy-traffic proof. No operation name is proposed
below unless it already appears in the reviewed tuple.

| Existing producer and durable effect | Current caller / test node | Published-command coverage | Smallest Agent dependency; deletion boundary |
|---|---|---|---|
| **Empty timeline bootstrap** supplies Main/additional-timeline defaults and repairs an existing headless shell. | `src/integrations/runtime/createDefaultTimeline.ts:41-115`; `createDefaultTimeline.test.ts:19-241` (fresh, additional, repair, stable retry, metadata CAS/concurrent Main). | **Open; legal create is necessary but insufficient.** Frozen `createTimeline(project, timeline, key, name?)` creates an accepted empty head, without App output or tracks. `track.create` covers full V1/A1 rows; no published root/output command or public headless repair exists in the audited tuple. | Runtime owns constrained existing-shell bootstrap admission and Door POST fix; Agent owns a published guarded initialization/config capture for missing authored fields. See the source audit below. Keep the publisher and original positive behavior tests until the complete replacement is qualified; no partial retirement or default-filled config stamped accepted. |
| **Visual seam acknowledgement** updates authored `config.app.visualSeamContract`; `useTimelineState` rebuilds the document and flushes the snapshot save. | `src/tools/video-editor/hooks/useRenderState.ts:973-982`; `src/tools/video-editor/hooks/useTimelineState.ts:654-680`; `useRenderState.test.tsx` — “disables seam acknowledgement when the timeline changes after the failed render”. | **Open.** Render admission/read validation exists, but the acknowledgement is not an EditCommand. | A reviewed root/config-field capture that records the original seam contract and writes only that field (or an existing Agent capture if it exactly covers it). Remove this save branch only after the acknowledgement journey proves durable command commit and refusal preserves the draft. |
| **Transcript artifact and source association.** Transcript content is stored as a Runtime project document; selecting/promoting it changes the timeline source association/projection. | `data/typed/projectTranscript.ts:83-119`; `lib/project-transcript-host.ts:500-575,756-857`; `hooks/useTimelineState.ts:1136-1150`; `data/typed/importTranscriptHandoff.test.ts` — “never presents a timeline-only write as a durable project import”. | **Split boundary.** Direct transcript document create/update is producer-artifact storage and should remain. The authored association/reference carried through timeline data is **open** through the snapshot funnel. | Agent capture/schema for the source document identity/version and authored association/reference, preserving the existing document repository and its conflict draft. Do not delete document writes; delete only the timeline snapshot association path after command coverage and reload/undo proof. |
| **Extension project data** (`project-data.write/delete`) is applied to the local timeline bundle and then persisted with the authored document. | `src/tools/video-editor/lib/timeline-patch.ts:463-607`; producer example `lib/compiler-canary.ts:152-214`; `lib/timeline-patch.test.ts` project-data validation cases. | **Open for canonical timeline data.** These are local patch names, not published wire commands in Bundle2. | Agent’s smallest namespaced-data capture/schema with exact key/value read/write/clear guards. Do not invent a wire opname. Keep noncanonical extension/catalog data on its existing artifact/catalog path; remove snapshot fallback only for data proven command-backed. |
| **Asset/registry registration** patches the canonical timeline registry; upload/media preparation itself settles bytes and metadata outside the timeline. | `hooks/useAssetOperations.ts:61-71,94-172`; `hooks/useTimelineCommandsService.ts:952-988`; `integrations/runtime/dataProvider.ts:1147-1160`; `hooks/useAssetOperations.test.tsx`, `runtime/element-adapter.test.ts` registry/save assertions. | **Open.** `patchRegistry` is durable only because the snapshot save owner eventually publishes it. Bundle2 `clip.add` is NONMEDIA ONLY and creates no registry binding; create-or-require registry birth exists inside occurrence.add-media/swap-media only, not a generic standalone registry writer. | Use the published add/media capture with immutable media selection and created-ID/registry guards; Agent must cover any standalone registration that is not an add. Keep catalog/media preparation and generation metadata writes. Delete `registerAsset`’s snapshot route only after all callers have command coverage and zero direct publisher traffic. |
| **Generic clip property updates** (opacity, effects, position and related shallow patches) mutate a resolved clip and flush the snapshot publisher. | `hooks/useTimelineCommandsService.ts:604-655` (`updateClip`); property producers in `components/PropertiesPanel/ClipTransitionSection.tsx:131-147,242-317` and the effects/position panels; `components/PropertiesPanel/ClipPanel.sequence.test.tsx` and `ClipPanel.transition.test.tsx`. | **Open.** Bundle2 `clip.set` values are hold-only; its clear set includes asset/transition/hold, not opacity/effects/position. | Agent must publish the smallest closed capture/schema extension for these authored fields, with original leaf reads and explicit clear semantics. App must not serialize `TimelinePatch` or infer film semantics. Delete generic `updateClip` snapshot persistence only after each field family has accepted reload/undo and zero-traffic proof. |
| **Transition clear (`None`)** removes the incoming transition field. | `components/PropertiesPanel/ClipTransitionSection.tsx:131-147,264-274`; `ClipPanel.transition.test.tsx` — “calls onChange with undefined transition when None is selected”; `tests/e2e/local/three-products.spec.ts` `setTransitionToNone` / clear assertion. | **Agent-covered, App-unwired.** Bundle2 `clip.set` explicitly supports `clear: ["transition"]`; this is not transition SET. | Wire the existing exact `clip.set` capture on the original raw clip. Keep the current UI meaning (ABSENT, never empty/null). Delete the old transition snapshot path only after accepted reload/undo and the existing zero-legacy journey pass. |
| **Transition SET** (choose a transition, duration/params) updates the incoming transition and successor-facing playback effect. | `components/PropertiesPanel/ClipTransitionSection.tsx:137-147,242-317`; `components/ElementsLibraryPanel.tsx:70-84` sends `timeline.apply_transition`; `runtime/element-adapter.test.ts:188-250,341-359`; `ClipPanel.transition.test.tsx` selector/duration nodes. | **Uncovered.** Bundle2 intentionally excludes transition SET; `timeline.apply_transition` still routes through the legacy element adapter/snapshot save. | Agent-owned transition-SET capture/schema, including the exact existing transition identity/registry and adjacent-clip reads required by the current behavior. Do not alias `crossfade`/`cross-fade` or choose incoming/outgoing semantics here. No deletion until this replacement is qualified. |
| **Hold after move** updates source-duration/derived `for` leaves after a clip move. | `hooks/useTimelineCommandsService.ts:658-705,744-779`; `hooks/useClipDrag.ts`; `tests/e2e/local/three-products.spec.ts` move cases; existing App scalar/drag tests. | **Contract successor exists, App wiring open.** The reviewed hold-after-move successor keeps the `clip.set` shape and original guards, but is not an official paired release. | Consume the reviewed successor only after Agent/Runtime re-freeze; capture hold on the moved local result without refreshing guards, preserving the compound move→hold order. Delete the old successor/hold snapshot mutation only after compound accepted reload, retry and inverse proof. |
| **Duplicate/group and ordinary import placement** mutates canonical clips/groups/registry. | `components/AstridTimelineEditor.tsx:390-445`; `lib/shot-group-pack-commands.ts:379-477`; `hooks/useExternalDrop.ts`; `commands/media.ts` (`buildAssetDropEdit`, duplicate/add); `data/shotCompositionEditor.ts:617-665`; `AstridTimelineEditor.document-shots.test.tsx`, `lib/timeline-domain.shot-groups.test.ts`. | **Open and split.** Ordinary NONMEDIA parent insertion has reviewed `clip.add`; it explicitly refuses media/image/video/audio and all asset selectors even null. Parent media insertion needs an Agent-owned native contract; occurrence media has reviewed `occurrence.add-media`/`occurrence.swap-media`. Canonical group/occurrence duplication still publishes/mutates whole documents and has no Bundle2 replacement. Catalog/generation duplication is not timeline publication. | Wire nonmedia parent add to exact clip.add capture. Parent media/import insertion requires its missing published capture; do not alias it to nonmedia clip.add or occurrence add. Agent must separately publish the group/occurrence duplicate contract before touching group writers. Delete `mutateTimelineDocument`/direct shot publication only per producer after its replacement’s reload/undo/zero-traffic proof; retain catalog/media duplication. |
| **Shared placement** places/unplaces generations and changes canonical frame placement. | `shared/lib/placement/placementService.ts:119-147,172-239`; callers `placeGeneration`, `unplaceGeneration`, `batchUpdatePlacementFrames`, and `lib/shot-group-pack-commands.ts:410,469`; placement tests and `runtime/dataProvider.test.ts` CAS checks. | **Open.** Bundle2 contains reviewed `placement.move` capture, but App still uses a bounded whole-document CAS/reapply cycle. | Wire `placement.move` capture through the normal command session with exact owner/media/placement reads. Agent must cover any unplace/batch shape not equivalent to that published capture. Keep relational `shot_generations.timeline_frame` and `metadata.end_frame` out of M2; delete the CAS writer only after command rebase/reload/undo and zero-traffic proof. |
| **Popup occurrence add/swap** publishes the canonical shot graph and keeps a recovery draft. | `travel-between-images/components/shotTimelineDataProvider.ts:435-590`; `ShotTimelinePreview.test.ts`, `ShotTimelinePreview.integration.test.tsx`; popup helper coverage in the current worker branch. | **Captured, not accepted.** d474 has `occurrence.add-media` and `occurrence.swap-media`; popup positive acceptance remains held on the normal Runtime asset-schema boundary. | Use exact five-field immutable media selection, occurrence/raw-child identity, create-or-require registry policy, and the reviewed Runtime verified-media read only after its official 0.2.6 tuple is published and paired. Delete `saveTimeline`/`shotCompositionAdapter.publish` only after independent add and swap accepted-reload/undo/retry/zero-legacy tests. |

## Keep outside canonical writer deletion

Keep Runtime media/object preparation and immutable catalog records; generation
duplication, gallery/catalog metadata, billing/task completion, and other
relational placement projections are not authored timeline state. Keep UI
preferences/session state and local IndexedDB recovery drafts. They must not be
counted as published-command coverage, and they must not be converted into
invented timeline opnames. The Supabase canonical append/registry purge is reviewed on held App d5000e35c, not yet integrated; do not restore it or count D03 as DELETED.

## Concrete next five writer results

1. **Clip scalar/property slice:** App wires transition clear and hold-after-move
   to the reviewed `clip.set` capture; Agent publishes the smallest SET capture
   for opacity/effects/position only if current behavior needs it. Preserve the
   existing transition-None assertion and distinguish it from SET.
2. **Popup add:** wire occurrence add against an official paired media read,
   proving immutable selection, created registry identity, reload/undo, exact
   retry, and zero snapshot traffic.
3. **Popup swap:** prove the same independently for old/new media pins and
   explicit raw-child identity; no media-swap-as-clear behavior.
4. **Placement:** replace the service’s whole-document CAS mutation with the
   reviewed placement capture where its semantics match, while retaining
   relational projections and proving rebase/reload/undo.
5. **Remaining document writers:** convert registry-backed ordinary add/import,
   visual seam acknowledgement, and authored transcript/project-data
   association one producer at a time; then delete the snapshot publisher only
   when every caller has a published command and zero-traffic coverage. Group
   duplication remains held for its separate Agent contract.

No tests, typecheck, build, browser, server, install, or full suite was run for
this source-only recovery. The active post-opaque App full remains the single
central run; M2/M3 integration remains held until PLAN records M1.

Manager source correction02:54: exactAgent027 _clip_commands.py:clip_add rejects media types and every assetselector evennull. Therefore ordinaryparentmedia/import and genericregistryregistration are STILL MISSING contracts; earlier wording suggesting clip.add covers them was wrong. Nonmediaadd sourceport assigned separately; popupregistrybirth stays occurrence-owned.

## Empty bootstrap seam — source audit, 2026-10-20

This row alone uses App `823d078daa27081dabc360037de1aaaa2bb1a408`
(worker base `tl/app-m2-bundle2-client-pin`), frozen Agent
`027bd16d96010544331c953c0e1014e161786e71` and Runtime
`4c145dc62192f0e942e3ee3922a11488aefe9b41` / client `0.2.3`.
Agent/Runtime anchors below are in the retained read-only worktrees
`/home/user/work/wt/app-m2-bundle2-{agent,runtime}-source`; paths are relative
to the named repo. This does not update the other rows' historical tuple.
The next `0.2.6` cohort/Door fix is staging, not qualified here.

**Answer: no complete source-backed migration recipe exists yet.** Legal create
is initial *empty* publication, not an arbitrary document/first-media bootstrap.
The missing behavior is not solved by the known Door routing fix.

| Field/behavior | Existing legal contract and exact difference |
|---|---|
| Empty accepted identity | Runtime `runtime_protocol/service.py:1887-1930` records `timeline.create`, then calls `TimelineCommitStore.bootstrap` inside the same durable transaction **when a provider is registered**. Exact-key replay precedes collision checks and returns the original resource/receipt, including original head pair, even after later edits. Without a provider it can create a headless shell; App must require verified history, not infer readiness. |
| Canonical empty bytes | Runtime `runtime_protocol/timeline_commit_baseline.py:417-440`: payload is exactly `{config:{clips:[],tracks:[]},registry:{},clips:[],occurrences:[]}`, with empty dependency lists. The bootstrap install check compares against these exact bytes. Runtime `timeline_commit_store.py:804-841` owns the private publication/history transaction; no App-authored candidate is accepted by create. |
| App output | App `src/tools/video-editor/lib/defaults.ts:25-44` requires `{resolution:'1280x720',fps:30,file:'output.mp4',background:null,background_scale:null}`. **All five are absent** from legal creation. Explicit null must stay distinct from absence. Theme/theme_overrides/generation_defaults remain absent. Agent `astrid/sdk/timeline/commands.py:30-52,74-82` lists the published operations and validates their closed schemas: no output/config/root setter. Compiler capability is not a public command: `astrid/core/timeline/authoring_bundle.py:1030` copies authored parent fields; it does not supply these defaults. |
| Full tracks/order | App `defaults.ts:4-23` requires V1 then A1, each with `label`, `scale:1`, `fit:'contain'`, `opacity:1`, `blendMode:'normal'`, plus `id`/`kind`. Agent `astrid/core/timeline/schema/edit-command.schema.json:1189-1214` and App generated `timeline-commit-types.ts:33,93` accept full `args.row` JSON with extra properties. Agent `capture.py:224-250`, `_recording.py:126-153`, `_command_state.py:170-184,383-399` record absent identity, collection selection and full-row creation, then append in command order. No stripped-down track DTO or metadata-only follow-up is needed. |
| Parent metadata/registry | Current publisher includes name-derived slug, payload `name` and `registry:{assets:{}}` (`createDefaultTimeline.ts:48-64`); legal payload omits both names and has `registry:{}`. Create's `name` sets the timeline row (`service.py:1906`), not payload name/slug. `_timeline_resource` obtains slug only from a document (`service.py:1349-1368`). Exact authored preservation therefore also needs these fields addressed in the Agent-owned initialization contract; the closed registry has no generic root/registry edit. Do not silently treat `{}` as byte-equivalent to `{assets:{}}` or resource name as payload metadata. |
| Headless shell | Current App repairs the *same* ID (`createDefaultTimeline.ts:104-108`). Create rejects any existing ID after replay (`service.py:1903-1904`), including a shell created under another key or without a provider. Private `bootstrap` can install an empty head on a member shell, but has no public repair entry. Startup only installs verified **existing publications** (`service.py:2587-2597`); `list_timeline_commits` calls `_ensure_timeline_commit_baseline`, which calls `head` and refuses missing history (`service.py:2690-2729`, `timeline_commit_store.py:170-179`). A read does not repair it. |

The Agent projector `astrid/core/timeline/shot_composition_projection.py:499-509`
copies the canonical config and normalizes projected assets; it does not add
output or V1/A1. App `dataProvider.ts:822-835` calls `withDefaultTimelineOutput`
for display, which cannot prove canonical persistence; an empty tracks array
also stays empty (`defaults.ts:96-98`). `loadTimelineCommandBasis:778-819`
requires verified history/head/manifest and exact immutable reads. Preserve that
admission; never turn locally filled defaults or a legacy document into its
accepted canonical document.

**Exact covered portion, not a runnable complete replacement:** the generated
call is `WorkspaceClient.createTimeline(projectId, timelineId, key, name)`
(`src/integrations/runtime/generated.ts:145`). `AstridRuntimeClient` currently
has no create wrapper; add a thin `withMutation` delegate when implementing,
matching `client.ts:576-586`, to retain session/instance fencing. The Runtime
HTTP handler exists (`runtime_protocol/server.py:488-497`), but the frozen Door
allows GET only at `/v1/projects/:/timelines` (`runtime_protocol/door.py:157`).
Consume its reviewed POST fix in the next official pair; do not alter frozen
`4c145` or bypass the Door.

After legal creation/repair supplies a verified basis, the official track
capture sequence is (Agent reference code, **not executed**):

```python
a = capture_track_create(bundle, 'parent', full_V1_row)
after_a = execute(bundle, [a]).bundle
b = capture_track_create(after_a, 'parent', full_A1_row)
# [a, b] is one ordered atomic commit/inverse unit over the original bundle.
```

Port that capture exactly for App; preserve its original selections, reads,
created refs `parent/track:V1` / `parent/track:A1` and row JSON. Do not capture B
against the pre-A collection. The complete one-time initialization must also
include the **not-yet-published** guarded output/metadata/empty-registry edits,
so do not ship a track-only replacement. Agent owns the smallest closed
capture/schema and inverse/rebase semantics; no guessed operation name here.

Reuse `commands/commitSession.ts:146-164,206-240` and
`commands/commitOutbox.ts:253-305`: one persisted initialization intent with
the commands and verified base pair, exact POST body/key reserved before send,
ACK saved atomically, and dependent first edits held behind it. The existing
outbox accepts **commit routes only** (`:266-267`); creation stays the existing
stable-key mutation, not a new outbox route/coordinator. Fresh Main retains
`stableUuid('astrid-first-timeline:'+projectId)` and
`astrid-first-timeline-${projectId}`; additional creation retains its captured
ID/name/key (`VideoEditorPage.tsx:1086-1106`, helper `:79-88`). Retry the same
request; a create replay's old head is not the current edit base—reload the
verified basis. Recover an existing scoped outbox before creating new init
work. A crash between create and init must resume only a proven pristine
bootstrap, using existing history/outbox facts; recorded later edits or undo
must never trigger defaults again. No new marker/wire field is proposed.

**Smallest missing seams / next workers:** Runtime must expose constrained
same-ID headless repair through existing creation/admission machinery, with
scope/admission/idempotency checks and atomic bootstrap/history. It must prove
the shell has no authored content, dependencies or conflicting publication;
never call the private bootstrap blindly over a headless document. Preserve
already headed timelines and exact original create retries. This requires a
Runtime-owned semantic change; the existing public read is insufficient.
Agent must publish guarded initialization writes for the missing authored
fields above, preserving opaque fields, explicit null/absence and safe inverse.
Do not broaden Runtime's exact-empty check into arbitrary initial snapshots.
Recommend these bounded owner workers first, then an App
`createDefaultTimeline` replacement worker consuming the official pair and
capture goldens, reusing the current session/outbox and retiring this publisher
only with the complete behavior qualified.

## Placement candidate review — 2026-10-20

Reviewed App `c8566f12` against Agent candidate **`a6c2db3d14c14da3be61c7e28b615c0e4202e619`**
(`hub/timeline/agent/tl/agt-m2-placement-create-unplace-b`, frozen027 base).
**Keep placement OPEN.** Fresh explicit image creation and plain removal have
native captures; this is not a qualified replacement for the service. The
candidate's advertised same-ID remove/create composition fails provider admission.
Canonical contract/schema and product/tests are unchanged by this review.

App paths below are relative to the App repo; Agent paths to the candidate.

| Actual producer / behavior | Proposed supported mapping and remaining boundary |
|---|---|
| `shared/hooks/shots/addImageToShotHelpers.ts:31-47` forwards `shot_id`, generation, project and optional frame. `useShotGenerationMutations.ts:66-115,344-369` wraps add/pool/auto-position. Reference upload `referenceDomainService.ts:252` and backfill `useGenerationBackfillMigration.ts:119` also call place with no frame. | None supplies an occurrence owner or raw child ID. Resolve ownership from the original accepted canonical bundle, never from `shotId` spelling or first occurrence. Parent/shared shapes remain uncovered. The projection exposes occurrence/raw-child identities (`data/shotCompositionProjection.ts:336-354,498-502`); the service currently picks a default timeline (`placementService.ts:112-118,149-154`). Migration/resolution must precede command capture. |
| Fresh, explicit, noncolliding image placement | Candidate `capture_placement_create` accepts `occurrence:O`, a never-reserved raw clip ID, five-field pin, absolute global seconds and literal `hold:4`. Owner must be exclusive, active/translation-only, with matching rational fps, no source window, existing active visual lane/registry and interval within occurrence. See `native_placement_commands.py:81-103,137-145` and `native_occurrence_media_commands.py:15-62`. Convert an already explicit frame using the pinned fps; capture before preview and persist IDs/pins through retry. No auto/collision policy is supplied. |
| Media selection / image and video | `placementService.ts:173-190` consumes R13 `resolveGenerationAsset`; resolver `:84-97,103-138,259-273` picks primary-or-first variant and supports video/audio as well as image. It returns URLs/registry metadata, not a catalog digest or authoritative verified media. Use existing `getProjectMediaSelection` (`integrations/runtime/client.ts:632`, types `:65-78`) for `{asset,generation_id,variant_id,object_id,catalog_digest}` and the owner-approved immutable-media capture seam; never fabricate verification from URLs/MIME or refresh selection at ACK. Candidate create is image-only. Its exact create-or-require registry binding is not the legacy registry refresh/merge. Video creation remains uncovered. |
| `undefined` append, `null` pool, collision shift, pooled promotion/batch | `documentPlacement.ts:197-218,223-266,307-330` implements these distinct positive behaviors. Create accepts only numeric global `on`; it neither selects last occupancy/next-free-frame nor records pool membership. Do not precompute these policies in App without Agent-recorded reads/intent. No mapping yet. |
| Re-place same `(shot,generation)` | Legacy `documentPlacement.ts:233-237` removes/recreates deterministic `clip-sg-<shot>-<generation>` (`:45-48`). Candidate ordinary `unplace` + `create` with that same reserved ID is **not supported** (admission evidence below). Existing `placement.move` is a possible narrow mapping only for an already placed, unchanged-media clip with explicit time and no collision shift; registry refresh/pooling/replacement is not covered by move. |
| Plain unplace / `keepAsPooled` | `capture_placement_unplace` removes one raw child and keeps the registry, guarding membership/whole row/binding/declared relations (`native_placement_commands.py:106-123,148-154`). Only removal without pooling matches. Actual hook caller `useShotGenerationMutations.ts:151-169` always requests `keepAsPooled:true`, then optional frame shifts; that full user action remains uncovered. Unplace accepts `clipType:media/image`; it does not itself establish video-create support. |

**Reservation and undo blockers, executed through Agent's real
`RuntimeCommitService.commit` with its existing detached `MediaRealm` port:**

* After accepted create, pure `execute([unplace,create(same ID)])` succeeds;
  provider commit rejects both that batch and a separate post-unplace create
  with **409 `identity_collision`**, ref `occurrence:occ-a/clip:placed`.
  `commit.py:523-618` scans accepted boundaries/created records monotonically;
  `:773` calls it before `port.accept`. This agrees with `edit-recipe.md:43` /
  `m2-move-draft.md:299-306`: ordinary retired-ID reuse is forbidden, trusted
  inverse/redo can restore identity. Keep that rule; correct the candidate's
  same-ID re-place claim. Prefer existing move for the narrow matching case.
* Create → unplace → undo(unplace) restores the exact post-create document;
  undo(create) then rejects **409 `intervening_write`** on that child root.
  `commit.py:713-722` / `inverse.py:144-201` treats removal and its inverse as
  overlapping publications. Single-step undo/redo passes, but ordinary LIFO
  stack use is blocked. Agent/history owner must reconcile this concrete
  sequence with lossless undo while preserving concurrent/other-author ABA
  refusals; App must not bypass guards or silently drop the undo step.

**Evidence/next qualification:** unchanged App placement/caller tests **40 PASS**,
media resolver **5 PASS**; candidate placement conformance **35 PASS**. Diagnostic
script and exact failures: `workers/app-m2-placement-contract-review/notes/placement-provider-probe.{py,json}`.
This is detached provider evidence, **not real Runtime acceptance** (candidate
tests fake ABI exceptions/metadata and use an in-memory port). Local Runtime
`4bb1d0f7` has no `placement.create` in its packaged command schema; no matching
official pair was run. Runtime owner recipe: release the candidate schema/pair
normally; ingest real image generation/variant and bootstrap the golden's
occurrence closure; get the public five-field selection; commit captured create
and reload; submit same-ID unplace/create in one batch and separately, proving
reservation rejection with unchanged head/history; then create → unplace →
undo(unplace) → undo(create), asserting the original authored state as the
required positive outcome (currently blocked). Repeat restart/exact retry and
other-author ABA/dependency controls. No digest override, new port/DTO/op or
legacy publisher fallback. Keep all existing positive auto/pool/collision/
re-place/keepAsPooled/batch tests unchanged until their real replacement passes;
if temporarily removed, retain their positive assertions with the mandated
expected-failure marker. No tests were changed here.

Retain all seven `createDefaultTimeline.test.ts` positives: existing head reuse,
atomic fresh creation, same-ID headless repair, reassigned Main, metadata CAS,
additional timeline and identical lost-ACK retry. Their publisher-specific
transport assertions must move to the legal calls while keeping every success
assertion; never replace repair/defaults with refusal expectations. Extend them
to assert exact accepted output/nulls/tracks/order/slug/name/registry on reload,
create→init crash boundaries, init lost ACK/restart, inverse/redo and no second
initialization after edits/undo, concurrent init and identity collision, provider
unavailable, and zero legacy publication traffic. Keep page empty-project and
retry behavior (`VideoEditorPage.test.tsx:1405,1432`) and local project creation
(`shared/hooks/projects/__tests__/useProjectCRUD.local-workspace.test.tsx`).
Retain Runtime `test_timeline_commit_port.py::test_create_has_real_atomic_empty_bootstrap`,
`::test_created_timeline_provenance_and_exact_retry_survive_restart`,
`::test_bootstrap_failure_rolls_back_creation_and_both_receipts` and
`test_timeline_commit_read_basis.py::test_bootstrap_manifest_is_the_exact_empty_read_basis`;
add actual Door/repair/nonempty-refusal/no-write cases. Retain Agent
`test_recipe_m1_commands.py::test_track_create_inverse_redo_exact_opaque_row_and_identity_collision`
and `::test_structural_group_uses_generic_creation_and_restores_order`; add exact
App-default fixture/capture/undo/rebase cases. Run the real App journey and
socket tests centrally after the active-full restriction lifts.

No tests, code execution, typecheck, build, install, browser, socket or test
service request was run for this audit (full `10022` active). Product/test
sources are unchanged; this is a source-backed gap report, not coverage or
retirement evidence. Project `metadata.default_timeline_id` remains the existing
noncanonical CAS write (`createDefaultTimeline.ts:117-133`), preserving chat and
concurrent Main reassignment; it is not an EditCommand.
