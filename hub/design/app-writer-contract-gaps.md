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
| **Visual seam acknowledgement** updates authored `config.app.visualSeamContract`; `useTimelineState` rebuilds the document and flushes the snapshot save. | `src/tools/video-editor/hooks/useRenderState.ts:973-982`; `src/tools/video-editor/hooks/useTimelineState.ts:654-680`; `useRenderState.test.tsx` — “disables seam acknowledgement when the timeline changes after the failed render”. | **Open.** Render admission/read validation exists, but the acknowledgement is not an EditCommand. | A reviewed root/config-field capture that records the original seam contract and writes only that field (or an existing Agent capture if it exactly covers it). Remove this save branch only after the acknowledgement journey proves durable command commit and refusal preserves the draft. |
| **Transcript artifact and source association.** Transcript content is stored as a Runtime project document; selecting/promoting it changes the timeline source association/projection. | `data/typed/projectTranscript.ts:83-119`; `lib/project-transcript-host.ts:500-575,756-857`; `hooks/useTimelineState.ts:1136-1150`; `data/typed/importTranscriptHandoff.test.ts` — “never presents a timeline-only write as a durable project import”. | **Split boundary.** Direct transcript document create/update is producer-artifact storage and should remain. The authored association/reference carried through timeline data is **open** through the snapshot funnel. | Agent capture/schema for the source document identity/version and authored association/reference, preserving the existing document repository and its conflict draft. Do not delete document writes; delete only the timeline snapshot association path after command coverage and reload/undo proof. |
| **Extension project data** (`project-data.write/delete`) is applied to the local timeline bundle and then persisted with the authored document. | `src/tools/video-editor/lib/timeline-patch.ts:463-607`; producer example `lib/compiler-canary.ts:152-214`; `lib/timeline-patch.test.ts` project-data validation cases. | **Open for canonical timeline data.** These are local patch names, not published wire commands in Bundle2. | Agent’s smallest namespaced-data capture/schema with exact key/value read/write/clear guards. Do not invent a wire opname. Keep noncanonical extension/catalog data on its existing artifact/catalog path; remove snapshot fallback only for data proven command-backed. |
| **Asset/registry registration** patches the canonical timeline registry; upload/media preparation itself settles bytes and metadata outside the timeline. | `hooks/useAssetOperations.ts:61-71,94-172`; `hooks/useTimelineCommandsService.ts:952-988`; `integrations/runtime/dataProvider.ts:1147-1160`; `hooks/useAssetOperations.test.tsx`, `runtime/element-adapter.test.ts` registry/save assertions. | **Open.** `patchRegistry` is durable only because the snapshot save owner eventually publishes it. Bundle2 has registry birth inside reviewed `clip.add`/`occurrence.add-media`, not a generic standalone registry writer. | Use the published add/media capture with immutable media selection and created-ID/registry guards; Agent must cover any standalone registration that is not an add. Keep catalog/media preparation and generation metadata writes. Delete `registerAsset`’s snapshot route only after all callers have command coverage and zero direct publisher traffic. |
| **Generic clip property updates** (opacity, effects, position and related shallow patches) mutate a resolved clip and flush the snapshot publisher. | `hooks/useTimelineCommandsService.ts:604-655` (`updateClip`); property producers in `components/PropertiesPanel/ClipTransitionSection.tsx:131-147,242-317` and the effects/position panels; `components/PropertiesPanel/ClipPanel.sequence.test.tsx` and `ClipPanel.transition.test.tsx`. | **Open.** Bundle2 `clip.set` values are hold-only; its clear set includes asset/transition/hold, not opacity/effects/position. | Agent must publish the smallest closed capture/schema extension for these authored fields, with original leaf reads and explicit clear semantics. App must not serialize `TimelinePatch` or infer film semantics. Delete generic `updateClip` snapshot persistence only after each field family has accepted reload/undo and zero-traffic proof. |
| **Transition clear (`None`)** removes the incoming transition field. | `components/PropertiesPanel/ClipTransitionSection.tsx:131-147,264-274`; `ClipPanel.transition.test.tsx` — “calls onChange with undefined transition when None is selected”; `tests/e2e/local/three-products.spec.ts` `setTransitionToNone` / clear assertion. | **Agent-covered, App-unwired.** Bundle2 `clip.set` explicitly supports `clear: ["transition"]`; this is not transition SET. | Wire the existing exact `clip.set` capture on the original raw clip. Keep the current UI meaning (ABSENT, never empty/null). Delete the old transition snapshot path only after accepted reload/undo and the existing zero-legacy journey pass. |
| **Transition SET** (choose a transition, duration/params) updates the incoming transition and successor-facing playback effect. | `components/PropertiesPanel/ClipTransitionSection.tsx:137-147,242-317`; `components/ElementsLibraryPanel.tsx:70-84` sends `timeline.apply_transition`; `runtime/element-adapter.test.ts:188-250,341-359`; `ClipPanel.transition.test.tsx` selector/duration nodes. | **Uncovered.** Bundle2 intentionally excludes transition SET; `timeline.apply_transition` still routes through the legacy element adapter/snapshot save. | Agent-owned transition-SET capture/schema, including the exact existing transition identity/registry and adjacent-clip reads required by the current behavior. Do not alias `crossfade`/`cross-fade` or choose incoming/outgoing semantics here. No deletion until this replacement is qualified. |
| **Hold after move** updates source-duration/derived `for` leaves after a clip move. | `hooks/useTimelineCommandsService.ts:658-705,744-779`; `hooks/useClipDrag.ts`; `tests/e2e/local/three-products.spec.ts` move cases; existing App scalar/drag tests. | **Contract successor exists, App wiring open.** The reviewed hold-after-move successor keeps the `clip.set` shape and original guards, but is not an official paired release. | Consume the reviewed successor only after Agent/Runtime re-freeze; capture hold on the moved local result without refreshing guards, preserving the compound move→hold order. Delete the old successor/hold snapshot mutation only after compound accepted reload, retry and inverse proof. |
| **Duplicate/group and ordinary import placement** mutates canonical clips/groups/registry. | `components/AstridTimelineEditor.tsx:390-445`; `lib/shot-group-pack-commands.ts:379-477`; `hooks/useExternalDrop.ts`; `commands/media.ts` (`buildAssetDropEdit`, duplicate/add); `data/shotCompositionEditor.ts:617-665`; `AstridTimelineEditor.document-shots.test.tsx`, `lib/timeline-domain.shot-groups.test.ts`. | **Open and split.** Ordinary media insertion has reviewed `clip.add`; occurrence media has reviewed `occurrence.add-media`/`occurrence.swap-media`. Canonical group/occurrence duplication still publishes/mutates whole documents and has no Bundle2 replacement. Catalog/generation duplication is not timeline publication. | Wire ordinary import/add to the exact add capture and immutable media pins. Agent must separately publish the group/occurrence duplicate contract before touching group writers. Delete `mutateTimelineDocument`/direct shot publication only per producer after its replacement’s reload/undo/zero-traffic proof; retain catalog/media duplication. |
| **Shared placement** places/unplaces generations and changes canonical frame placement. | `shared/lib/placement/placementService.ts:119-147,172-239`; callers `placeGeneration`, `unplaceGeneration`, `batchUpdatePlacementFrames`, and `lib/shot-group-pack-commands.ts:410,469`; placement tests and `runtime/dataProvider.test.ts` CAS checks. | **Open.** Bundle2 contains reviewed `placement.move` capture, but App still uses a bounded whole-document CAS/reapply cycle. | Wire `placement.move` capture through the normal command session with exact owner/media/placement reads. Agent must cover any unplace/batch shape not equivalent to that published capture. Keep relational `shot_generations.timeline_frame` and `metadata.end_frame` out of M2; delete the CAS writer only after command rebase/reload/undo and zero-traffic proof. |
| **Popup occurrence add/swap** publishes the canonical shot graph and keeps a recovery draft. | `travel-between-images/components/shotTimelineDataProvider.ts:435-590`; `ShotTimelinePreview.test.ts`, `ShotTimelinePreview.integration.test.tsx`; popup helper coverage in the current worker branch. | **Captured, not accepted.** d474 has `occurrence.add-media` and `occurrence.swap-media`; popup positive acceptance remains held on the normal Runtime asset-schema boundary. | Use exact five-field immutable media selection, occurrence/raw-child identity, create-or-require registry policy, and the reviewed Runtime verified-media read only after its official 0.2.6 tuple is published and paired. Delete `saveTimeline`/`shotCompositionAdapter.publish` only after independent add and swap accepted-reload/undo/retry/zero-legacy tests. |

## Keep outside canonical writer deletion

Keep Runtime media/object preparation and immutable catalog records; generation
duplication, gallery/catalog metadata, billing/task completion, and other
relational placement projections are not authored timeline state. Keep UI
preferences/session state and local IndexedDB recovery drafts. They must not be
counted as published-command coverage, and they must not be converted into
invented timeline opnames. The retired Supabase canonical append/registry lane
is already closed; do not restore it.

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
