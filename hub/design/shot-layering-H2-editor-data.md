# H2 — App editor shot DATA layer (read-only)

Repo: `/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/app-gallery-bar` (branch feat/gallery-bar). Editor root `src/tools/video-editor` (abbrev. `VE/`). All paths below are under the App repo unless noted.

## 1. The two lanes: `userId` and `resolveCanonicalComposition`

### What `userId` is
- `userId` is an editor-runtime prop, NOT a Supabase user in the editor. `VE/contexts/VideoEditorProvider.tsx:851,885` takes it as `string | null`.
- The only production mount that feeds the editor is `src/tools/video-editor/pages/VideoEditorPage.tsx`:
  - `useVideoEditorProviderSelection` hard-codes `userId: null` (`pages/VideoEditorPage.tsx:149`), and `useEditorTourSelection` also does (`:168`).
  - `VideoEditorProvider` is mounted with `userId={providerSelection.userId}` (`:865`), and its data provider is `RuntimeDataProvider` (`integrations/runtime/dataProvider.ts`), constructed with only `projectId` and `onRuntimeError` (`pages/VideoEditorPage.tsx:~121`).
- The Supabase/`AuthContext` user is not what the editor receives. `shared/contexts/AuthContext.tsx:85-87` returns `userId: LOCAL_USER_ID` (`'local-user'`, `shared/auth/bridgeSession.ts:25`) when gated, or the probed userId otherwise. The editor never reads `useAuth().userId` for this prop.
- Other mounts: `tools/travel-between-images/components/ShotTimelinePreview.tsx:632` passes `userId={null}`. `BrowserVideoEditorProvider.tsx:69,116` defaults to `null`. Non-null values appear only in `pages/ExtensionHarnessPage.tsx:445,581,664` (`'harness-user'`, `'extension-harness-user'`) and `pages/VideoEditorProcessesHarnessPage.tsx:647` (`'process-harness-user'`). The `examples/CustomTwoPaneVideoEditorExample.tsx:145` mount takes whatever is passed in.

### Which lane each environment takes
- Local dev (:5193 / :2222, against local Runtime) and hosted astrid.haus: the same code path. Both run `VideoEditorPage` -> `RuntimeDataProvider` with `userId = null`.
- With `userId === null`, `isDocumentShotMode` is true (`components/AstridTimelineEditor.tsx:116`). `isCanonicalEditor = isDocumentShotMode && Boolean(runtime.shots?.shotComposition)` (`:126`). `RuntimeDataProvider` always defines `shotComposition` (`integrations/runtime/dataProvider.ts:132`), so the canonical editor is ON in both environments.
- Inside the resolver (`data/canonicalCompositionState.ts:36-38`): `canonicalLane = userId === null && hasShotComposition && (hasShotClips || Boolean(composition))`.
  - For a Runtime timeline with a loaded canonical head, `composition` is non-null (even with zero occurrences), so the canonical lane is taken for every userId-null session.
  - If the head fails to load and the parent has `clipType:'shot'` clips, the result is `source:'canonical', status:'error'`. It does NOT fall back to legacy (`:48-55`, test `canonicalCompositionState.test.ts:75` "fails closed").
- Legacy lane is reached only when: (a) `userId !== null` (harness and example pages only), or (b) `shotComposition` is absent (a DataProvider without the port, e.g. in-memory/tour/public-editor providers), or (c) `composition` is null and there are no shot clips (`canonicalCompositionState.test.ts:28`).
- Verdict (judgment): no real astrid.haus or :2222 user path takes the legacy lane. `userId !== null` is harness-only. Legacy `clipType:'shot'` rendering (`ShotClipSequence`) is reachable only in case (b)/(c), which the app's own providers do not produce for user timelines. Treat it as migration residue unless a non-Runtime provider is used with real projects.

### Every caller of `resolveCanonicalComposition`
- `components/CompactPreview.tsx:29`
- `components/PreviewPanel/useVideoEditorPreviewComposition.ts:13`
- `hooks/useRenderState.ts:569`
- Definition: `data/canonicalCompositionState.ts:18`; test `data/canonicalCompositionState.test.ts`.

### Every `isDocumentShotMode` / `userId === null` / `!== null` branch for shots
- `components/AstridTimelineEditor.tsx`: `:116` (def), `:126` (isCanonicalEditor), `:296` (usePinnedShotGroupViews gate), `:441,:466` (`shots: undefined` when document mode), `:549` (dropped-legacy banner), `:586-604` (shot-group menu handlers undefined in document mode; `:598` existingShots=[]; `:599` create-from-selection uses document handler; `:600-605` navigate/generate disabled).
- `components/TimelineEditor/TimelineEditorCore*.tsx` and `ShotGroup*`: legacy `clipType==='shot'` scans (`TimelineEditorCore.tsx:348,575`, `TimelineEditorCoreBody.tsx:340,549`, `AstridTimelineEditor.tsx:298`).
- `components/PreviewPanel/useVideoEditorPreviewComposition.ts:10,18` and `components/CompactPreview.tsx:33-34`: composition only when `userId === null`.
- `hooks/useRenderState.ts:573-574,679`: `canonicalLane` gates the export guard's shot scan.
- `hooks/useFinalVideoAvailable.ts:309`: `canonicalComposition` only when `userId === null`.
- `lib/timeline-shot-summaries.ts:15`: `playedShotComposition` returns null unless `userId === null`. Callers: `useDataLanes.ts:93`, `hooks/useTimelineState.ts:1136`, `components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx:66`, `contexts/VideoEditorProvider.tsx:396`, `lib/timeline-reader.ts:1046` (summarizeShotPlacements).
- `contexts/editorRuntimeAssembly.tsx:804` (playedAssetRegistry).
- `exportGuard.ts:1050`: `clip.clipType === 'shot'` (managed-shot guard).
- `data/shotComposition.architecture.test.ts:13-18` forbids `clipType === 'shot'` and `pinnedShotGroups` in 5 product modules (adapter, useAstridShotsHost, localTimelineShotModel, LocalTimelineShotBrowser, ShotEditorView).

## 2. Storage shape

### Wire contract (`data/shotComposition.ts`)
- `ShotCompositionContract` (`:13-20`): `schema_version:1`, `project`, `primary_timeline` (head revision + content digest), `shot_revisions[]`, `occurrences[]`, `cases`.
- Occurrence required fields (`validateShotComposition`, `:191-206`): `occurrence_id`, `parent_document_id`, `shot_id`, `revision_id`, `ordinal`, `at_ms`, `duration_ms`, `stable_deep_link`, `output_identity` (must equal `project/.../occurrence/<id>/output/final-video`).
- Optional occurrence fields read by the adapter (`data/shotCompositionAdapter.ts:216-246`): `track` (-> `trackId`), `source_offset`, `speed`, `gain`, `muted`, `transform`, `text_bindings`. `placement.start_ms` and `placement.track` are read by the editor (`shotCompositionEditor.ts:170-173`) and the Runtime dataProvider (`:1480-1493`). Track default is `'video'`.
- Shot revision (`:109-176`): `shot_id`, `revision_id`, `content_digest`, `internal_timeline_revision{revision_id, content_digest, timeline:{tracks[], clips[]}}`, `timing.duration_ms`, optional `audio`, `name`, `assets[]` (asset_id, object_id, media_id, role, type, media_kind, media_type, digest, scope), `generation_inputs[]`, `provenance`, `dependencies[]` (must resolve), `runtime_playback_assets` (used by projection, `shotCompositionProjection.ts:240`).
- Forbidden: `clipType==='shot'` inside revision timelines (`:128`) and `pinnedShotGroups` (`:96`), both marked migration-only.

### Adapter (`data/shotCompositionAdapter.ts`)
- `prepareContract` (`:191-259`) flattens each occurrence with its revision object (`CanonicalShotOccurrence`, `:112-131`), sorted by `ordinal`.
- `publish` (`:319-350`): validates, runs `projectCanonicalComposition(submitted)` plus `assertVisualSeamAdmission` (`:332-333`), then calls the port. CAS is `expectedHeadRevisionId`.

### Runtime reads (`integrations/runtime/dataProvider.ts`)
- `loadRuntimeShotComposition` (`:454`) and `loadRuntimeShotCompositionAtHead` (`:587`) resolve each occurrence's `shot_revision_id ?? revision_id` into immutable child revisions.
- Parent write path `saveTimelineInOrder` (`:743-900`) publishes `parent_composition` with `internal_timeline_revisions: []` and `shot_revisions: []` (`:833-852`). The editor changes only the parent config and registry; Runtime resolves child authority from occurrences.
- Parent `config.clips` is the parent's own clips only. `reconcileParentClips` (`:1517-1570`) writes config.clips, merged over canonical clips by id.

### Child timeline and track list
- Each child is an independent `internal_timeline_revision.timeline` with its own `tracks[]` and `clips[]`. Storage is independent per revision.
- Child clip `track` ids are NOT prefixed. Child tracks are merged into the parent by id: `tracksFor` skips any child track whose id already exists in the parent (`shotCompositionProjection.ts:286-287`). So shot children reuse parent track ids by design, and two shots with track `plate` share one lane.
- Child clip ids ARE prefixed `${occurrenceId}:${clipId}` (`projection.ts:327-328`).
- Assets: each revision carries its own `assets[]`. The projection merges them into one registry. Colliding asset ids across shots get `canonical:<occ>:<asset>` aliases (`projection.ts:259-267`).

## 3. Projection and the reverse path

### `projectCanonicalComposition` (`data/shotCompositionProjection.ts:440-588`), step by step
1. Base config: use the given base, or rebuild from `parent_composition` (`:448-464`). Track roles are read from authored tracks (`:465-467`).
2. `projectOutputTimelineConfig(base)` removes Source tracks (`:468-470`).
3. `outputOccurrences` drops occurrences whose parent lane role is `source` (`:474-476`).
4. `assertDependencies` (`:477`, `:118-135`).
5. For each occurrence (`:482-528`): `outputTimeline(child)` -> `timelineContentExtentMs`, then `timelineOccurrenceEffectiveDurationMs` caps the duration at the next same-lane occurrence's `at_ms` (lane = `trackId`, defaulting to `'video'`) (`shotCompositionTiming.ts:99-143`).
6. For each child clip: `projectClip` (`:318-433`):
   - id = `${occurrenceId}:${clipId}` (`:328`)
   - `at = occurrence.atMs + clipAt` (`:379`); clip `at` may be transport `at_ms` or editor-form `at` seconds (`:335-337`)
   - `track = clip.track ?? occurrence.trackId ?? 'video'` (`:359`). The occurrence track is only a fallback. The shot is NOT a layer.
   - trim, speed, hold/duration and gain are computed (`:338-357`)
   - `app.canonical` = identity; `app.canonicalTiming` = offsets and duration (`:403-415`)
   - optional clamp to occurrence duration (`:419-430`)
   - timeline-level `effects` are appended to each child clip (`:512-515`)
7. Parent clips: `outputBaseConfig.clips` minus `clipType==='shot'` (`:532`). Parent clips come first in the array, then child clips (`:540`).
8. Asset registry and aliases: `assetRegistryFor` (`:168-269`), then each projected clip gets `assetEntry` (`:540-546`).
9. Tracks: `tracksFor` (`:271-316`) starts from the parent track list. For each child track not already present, it inserts after the nearest preceding shared track in the child's order, or before the next shared track. Otherwise it appends (`:296-307`). Skips `source` role. Falls back to a `video` track if empty.
10. Seam report via `analyzeVisualSeams` (`:568-581`), with `mode:'enforced'`.

Result: one flat `ResolvedTimelineConfig` (tracks plus clips) plus identity maps. `clipIdentities` maps child clip id to occurrence. There is no nested structure.

### How preview and render differ from the timeline canvas
- The projected config feeds preview (`resolveCanonicalComposition` in CompactPreview, PreviewPanel, useRenderState) and the data lanes and reader summaries (`playedTimelineClips`, `summarizeShotPlacements`).
- The timeline canvas does NOT use the projection. `hooks/useTimelineState` and the rows come from `lib/timeline-data.ts` `assembleTimelineData` -> `configToRows(canonicalConfig)` (`:464-493`). In canonical mode `canonicalConfig` is the parent's `config` (from `integrations/runtime/dataProvider.ts:1117-1140`). Child clips are therefore NOT rows on the canvas. Shots show as group overlays from `hooks/useShotGroups.ts:178-330` and `ShotGroupOverlay`. This contradicts the CONTEXT note that "children are drawn on their own shared rows". I verified this from the code path; I did not run the UI.

### Reverse path (write-back)
- Parent canvas edits (move, trim, add, delete of parent clips, including the loose clip) go through `saveTimelineAtHead` -> `saveTimelineInOrder` (`integrations/runtime/dataProvider.ts:713-900`). That writes `config.clips` through `reconcileParentClips` (`:1517-1570`). Child clips never appear in the parent save payload, so this path cannot write a child change.
- Shot-occurrence geometry: `moveCanonicalOccurrence` (`data/shotCompositionEditor.ts:563`, sets `at_ms`) and `trimCanonicalOccurrence` (`:583`, sets `duration_ms`) have NO production callers. Only `data/shotCompositionEditor.test.ts` uses them. `duplicateIndependentShot` is called from `components/AstridTimelineEditor.tsx:321`. So in canonical mode the App UI cannot move or trim an occurrence through these functions. `occurrence.track` is never written by the editor (`shotCompositionEditor.ts` has no writer; only `parentLaneKey` reads it, `:170-173`).
- Child content edits happen in the shot-local popup, which is a nested `VideoEditorProvider` with `userId={null}` (`components/AstridTimelineEditor.tsx:626-660`; `tools/travel-between-images/components/ShotTimelinePreview.tsx:626-632`).
  - It loads a projection of one occurrence with an empty base (`tools/travel-between-images/components/shotTimelineDataProvider.ts:~400-410`), with `clampToOccurrenceDuration:false`.
  - Save: `createCanonicalTimeline` strips `${occurrenceId}:` from clip ids, drops `canonical`/`canonicalTiming` from `app`, and writes the clips plus `tracks: config.tracks` (`shotTimelineDataProvider.ts:135-156`).
  - Publish: `updateCanonicalShotTimeline` (`data/shotCompositionEditor.ts:465-533`) -> `updateCanonicalShotRevision` (new immutable child revision for that occurrence only, `:239`). It also sets `occurrenceDurationMs` from content extent, and serializes via `enqueueCanonicalShotPublish` (`:16`). Pause-gap remapping is done only when declared pauses exist (`:478-530`).
- Consequence for a projected child clip dragged on a shared row: no such row exists on the canvas (see above). Child clips are edited only in the popup. Loose parent clips are saved as parent clips.
- Consequence for a loose clip dragged into a shot's time range on a shared track: the save path has no shot awareness. `assertParentLanePlacement` (`shotCompositionEditor.ts:212-237`) checks only occurrence-vs-occurrence overlap on the same lane. The loose clip stays a parent clip on its own track. In preview, `TimelineRenderer` draws per track id (`compositions/TimelineRenderer.tsx:1598-1600`), so the loose clip paints in track order over or under the child on the same track, not over or under the shot as a whole. This is the reason for the clip-0 bug in the film (CONTEXT).
- Consequence for dragging a shot to another track: there is no path in the App that changes `occurrence.track` (see above). Its lane identity is fixed by the Runtime wire. The lane still matters, because it defines same-lane blocking (`timelineOccurrenceHardDurationMs`, `shotCompositionTiming.ts:118-132`).

## 4. Blast radius: modules that depend on children living on parent tracks

Track-id reads (count: 94 files in `lib hooks components compositions data runtime data-kinds effects` contain `.track` or `trackId`). The ones that matter most for nested semantics:
- Projection and track merge: `data/shotCompositionProjection.ts:271-316` (tracksFor), `:359` (clip track), `:532-552` (parent+child clip list).
- Seam contract: `data/visualSeamContract.ts` groups spans by `clip.track` (`:220` path, `:351`, `:393`, `:399-419`, `:457-472`, `:505-506`, `:517-520`). Pause gaps are keyed by `gap.track` (`:457-472`). Owner id uses `app.canonical` (`:209-222`). `data/portableVisualSeamIntent.ts:29,47,58,62,92-94` keys seams by track and `app.canonicalTiming`. Changing to nested would change span grouping, the continuity set and the "same track seen twice" frame test.
- Row layout: `lib/timeline-row-layout.ts:66-76` builds one row per track id in array order. Canonical canvas rows come from parent tracks only (`lib/timeline-data.ts`).
- Shot groups and selection: `hooks/useShotGroups.ts:129-330` (`projectCanonicalShotRows`, lanes by `occurrence.trackId`), `components/TimelineEditor/ShotGroupOverlay.tsx`, `components/TimelineEditor/TimelineCanvas.tsx:789-833`, `hooks/useClipResize.ts`, `hooks/useDragCoordinator.ts`, `lib/clip-drag-planner.ts`, `lib/multi-drag-utils.ts`, `hooks/useSelectedMediaClips.ts`.
- Snapping and drop: `lib/drop-position.ts`, `lib/external-drop-utils.ts`, `hooks/useExternalDrop.ts`, `lib/auto-scroll.ts`.
- Transcript and data lanes: `data-kinds/useDataLanes.ts:93-95` (playedTimelineClips), `hooks/useTimelineState.ts:925-937` (canonicalShotTrackIds, shotTracksSettling), `data/typed/projectTranscript.ts` and `assembleDataLanes.ts`.
- Effects: `data/shotCompositionProjection.ts:512-515` (timeline.effects appended to every child clip), `effects/transitions.ts`, `lib/renderRouter.ts`, `runtime/renderPlanner.ts`.
- Inspector: `components/PropertiesPanel/ClipPanelBody.tsx`, `PropertiesPanel.tsx`, `TimelineOutlinePanel.tsx`, `lib/clip-inspector.ts`.
- Render and preview: `compositions/TimelineRenderer.tsx:1598-1600` (per-track stacking), `:1415-1416` (legacy ShotClipSequence), `:1670-1701` (accumulate), `hooks/useRenderState.ts`, `hooks/useFinalVideoAvailable.ts`.
- Reader and agent tools: `lib/timeline-reader.ts:1046`, `lib/timeline-shot-summaries.ts:57-95` (summaries use `clip.track`), `runtime/agentToolInvocationService.ts`.
- Remote renderers (outside App, from CONTEXT): Astrid `timeline_restructure.py` merges shot tracks by neighbour, `expand_shots.py:258`; `@banodoco/timeline-composition` reverse convention; three.js backend opposite convention.

## 5. Tests that pin the current flattening

Projection and track order:
- `data/shotCompositionProjection.test.ts`:
  - `:61` "merges shot-only lanes around shared picture layers" — pins `projection.config.tracks` order equal to `shotTrackOrder.fixture.json` `expected_order` plus `video`, `audio`, and that child track properties are preserved. This is the direct pin of flattened track merging.
  - `:188` "projects occurrence timing ... without legacy group or shot clips" — timing and speed mapping.
  - `:247` "filters child Source lanes before extent, asset selection and track merging".
  - `:288` "classifies parent Source ownership ... even when a child reuses the ID" — pins shared track IDs between parent and child.
  - `:313,:324,:348,:362` — asset aliasing and per-occurrence keys.
  - `:393` "clips an overlong child to the occurrence"; `:414` "caps content-derived occurrence duration at the next same-lane cut" — same-lane = parent track.
  - `:484` editor-form seconds and trim.
  - `:738,:748` missing dependency and unsupported nesting (`unsupported_nesting` rejects child `shot_id`/`clipType:'shot'`, so nested child shots are explicitly disallowed today).
  - `:764` managed output matching.
- `data/shotTrackOrder.fixture.json`: film tracks `picture,sprite,plate,vo,music` plus shot tracks `chrome,type,fx,sprite,plate,vo,sfx`, with `expected_order` `picture,chrome,type,fx,sprite,plate,vo,music,sfx`. This fixture encodes the interleaved flat order and is the main pin to change.
- `data/shotComposition.fixture.json` is used by `shotComposition.test.ts`, `shotCompositionAdapter.test.ts`, `shotCompositionEditor.test.ts`.

Downstream of projection:
- `data/canonicalCompositionState.test.ts`: `:15` waits for graph (no legacy shells); `:28` ordinary timelines stay legacy (userId null, no shot clips, composition null); `:41` preview and export share projection; `:60` prepared graph wins without shot shells; `:75` fails closed.
- `lib/timeline-shot-summaries.test.ts`: `:13` placements in timeline order with the clips they play (groups by `clip.id` prefix); `:30` reader snapshots; `:41` child-shot draft first and only for local canonical editors; `:49` media identity of assets only inside shots.
- `data/canonicalShotViewModel.test.ts`, `data/visualSeamContract.test.ts`, `data/visualSeamAcceptance.test.ts`, `data/visualSeamSharedCases.test.ts`, `data/visualSeamPerformance.test.ts`, `data/portableVisualSeamIntent.test.ts` — seam grouping by track and `app.canonical`.
- `data/shotComposition.architecture.test.ts`: `:13` no `clipType==='shot'` and no `pinnedShotGroups` in 5 product modules; `:21` shared adapter and port; `:30` normal host canonical-only.
- `data/shotCompositionEditor.test.ts`: `moveCanonicalOccurrence` and `trimCanonicalOccurrence` tests (no UI callers), plus revision and duplicate behaviour.
- `hooks/useRenderState.test.tsx`, `hooks/useFinalVideoAvailable.test.ts`, `lib/renderRouter.test.tsx`, `components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx`, `data-kinds/useDataLanes.test.tsx`, `adapters/app/useAstridShotsHost.test.tsx`.
- `components/AstridTimelineEditor.document-shots.test.tsx`: `:185` holds just-published graph; `:194` targets active timeline and leaves relational shot actions dormant; `:246` canonical shot overlay without reloading.

Legacy nested (ShotClipSequence) pins:
- `compositions/TimelineRenderer.shots.test.tsx` (476 lines, `clipType:'shot'` at `:131,:146,:387`): nested `TimelineRenderer` host resolution through two nesting levels (`:211,:231,:243,:254`), mount dedupe and premount (`:292-377`), invalidation (`:421`), failed-load fallback (`:460`). This is the ONLY test that already exercises nested child semantics, and it is the legacy lane. It is the closest existing model for "shot as a sub-timeline layer".

Travel-between-images tests that use the canonical shot path (not flattening pins, but they depend on the projection): `tools/travel-between-images/components/ShotTimelinePreview.test.ts`, `ShotTimelinePreview.integration.test.tsx`, `pages/LocalTimelineShotBrowser.test.tsx`, `pages/ShotEditorView.test.tsx`, `pages/localTimelineShotModel.test.ts`. Also `src/integrations/runtime/shotCompositionRuntime.test.ts` and `dataProvider.test.ts` / `dataProvider.parity.test.ts`.

## Findings in brief
1. In the shipped app both :2222 and astrid.haus take the canonical lane (userId null + RuntimeDataProvider). Nothing in the App mounts a real user with userId !== null. Legacy `clipType:'shot'` rendering is residue for non-Runtime providers and harnesses.
2. A shot child is a separate immutable revision with its own tracks and clips. Child track ids are not namespaced; they are merged into parent tracks by id (`tracksFor`). Child clip ids are prefixed.
3. The canvas does not draw child clips. Preview, render and reader use the flattened projection. The occurrence track is only a fallback for clips and the same-lane blocking key.
4. Child edits only happen in the shot-local popup, which writes a new child revision. Loose parent-clip edits never touch shots. `moveCanonicalOccurrence` and `trimCanonicalOccurrence` have no UI callers. Occurrence track cannot be changed by the App.
5. Blast radius: projection, seam contract (grouping by track id), occurrence lanes (`useShotGroups`), data lanes and transcript, reader summaries, TimelineRenderer per-track stacking, and the Astrid-side renderers.
6. Pins to change: `shotCompositionProjection.test.ts:61` (+ `shotTrackOrder.fixture.json`), `:288`, `:414`; `canonicalCompositionState.test.ts:41,:60`; `timeline-shot-summaries.test.ts:13`; seam tests; `TimelineRenderer.shots.test.tsx` already encodes nested semantics for the legacy lane.

Not verified: whether any production parent timeline still carries `clipType:'shot'` shells (the film has none; the Runtime rejects them only inside revisions); and the live canvas behaviour (no UI run, code read only).
