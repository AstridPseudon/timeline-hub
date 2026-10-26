# PLAN: a shot is one isolated layer at its occurrence slot

Draft for the main thread to judge. Plan only. Paths: App = labs/app-gallery-bar (VE = src/tools/video-editor), Astrid = live-door/Astrid, Runtime = live-door/Runtime. Land on the three mains, not the live checkouts. Drift checked: App `git diff origin/main -- VE` is empty; Astrid origin/main did NOT touch shot_composition_projection.py, timeline_restructure.py, expand_shots.py or remotion/src, and still pins timeline-composition v0.0.6 (remotion/package.json:18); managed_timeline.py changed by 9 lines only (asset metadata shape). Runtime is level with origin. Rebase risk is low.

## 1. Semantics

A shot occurrence is one compositing layer. It sits at the stack position of its occurrence's parent track (`occurrence.track`); inside it, its own tracks keep their own order and are drawn only against each other. The finished shot then composites into the parent as one flattened image with alpha. Where nothing inside draws, it is transparent. Blend modes and effect layers of inner tracks see only inner content. A loose clip on a parent row below the shot's row draws under the whole shot; above, over it. One level deep (already enforced: VE/data/shotCompositionProjection.ts:137-153, Runtime test_shot_composition_runtime.py:621).

| Case | Result |
|---|---|
| Loose clip on a row above the shot's row | over the whole shot |
| Loose clip on a row below the shot's row | under the whole shot (clip-0 on `type`, shot on `picture`) |
| Loose clip on the SAME row as the occurrence | under the shot while the shot is active (decision, flag to owner) |
| Inner order | shot's own track order, unchanged |
| Empty area of a shot | transparent, parent shows through |
| Inner blend/opacity/scale on a track | affect only inner content (isolated group) |
| Inner effect-layer | wraps only inner tracks below it |
| Occurrence opacity / transform | one group-level opacity/transform that composes with children (replaces today's per-child overwrite, shot_composition_projection.py:165-166) |
| Audio | not layered; additive mix; occurrence gain/mute stay per clip as today |

## 2. Representation: group-tagged flat tracks (chosen)

Render/projected config stays a flat `tracks` + `clips` list. Per occurrence, each INNER VISUAL track becomes a track with id `"<occurrenceId>~<trackId>"`, carrying `app: { group: { id: <occurrenceId>, sourceTrack: <trackId>, opacity?, transform? } }`, spliced contiguously at the occurrence track's index (group sits immediately above that parent row). Child clips get `track` = the namespaced id. Inner audio tracks keep merging into parent audio tracks by id (order is irrelevant for audio). Definition of a namespaced track = parent's definition of the same id (keeps today's look), child fields fill gaps.

Why this, with code evidence:
1. **No schema release.** `tracks.items` is `additionalProperties:false` (Runtime contract/schemas/timeline-config.schema.json:82) but has a free `app` object (:72-75), and the App already hangs `app.canonical` on clips. So no @banodoco/timeline-schema bump, no contract/artifacts.json digest change, no pin changes in 3 repos. A first-class `group` field can follow later as an optional promotion.
2. **Degrades correctly.** Stage 1 (contiguous namespaced slot) already fixes clip-0 on the OLD exporter (0.0.6) because it paints per-track in order (TimelineComposition.tsx:266). A nested clip would simply vanish on an unpatched renderer (no `shot` handling in 0.0.6; clipType is a free string, schema :160, but nothing draws it).
3. **Consumers keep working.** Seam contract, data lanes, summaries and the transcript all read flat `config.clips` (helper report: visualSeamContract.ts:340-357,523; useDataLanes.ts:94-97; timeline-shot-summaries.ts:57-100; useTimelineState.ts:1127-1156 only reads the registry). Nested would force two trees.
4. **Cheaper preview.** No nested `<TimelineRenderer>` subtree per shot (own AudioAnalysisProvider, async child cache, premount), only a wrapper `AbsoluteFill` per group.

Why not nested (clip + inline child config): needs a new clip shape in the shared schema, a package release for export, a second consumer path, and a new runtime child loader on the canonical lane (H3 option A "medium-large"). And I do not use `ShotClipSequence` (TimelineRenderer.tsx:212-276) as the seed: it is opaque black (:1727), loads children through `loadReferencedTimeline` (legacy doc ids), and TimelineRenderer.shots.test.tsx pins only that loader's cache/host/premount behaviour, not any visual rule. Only its idea (isolate the sub-tree) is reused. Weakness of my choice: namespaced ids change what agents/tools see as track ids (onscreen.py:248, timeline_visualize/model.py:524 read config tracks) and the seam lane key must map back via `app.group.sourceTrack`. Stage 0 checks the tool side.

Export isolation WITHOUT a package release: Astrid-owned wrapper in remotion/src (`GroupedTimelineComposition`, registered in Root.tsx:2-8 as the default id) splits the visual track list into runs (ungrouped run / one group), renders each run via the pinned `TimelineComposition` with only that run's visual tracks, bottom run first; group runs get `isolation:isolate`, group opacity/transform. Audio tracks go only to the first run. Unknowns: nested TimelineComposition root paints `theme.visual.color.bg ?? 'black'` (0.0.2 vendor L263; unchecked in 0.0.6), so the wrapper must pass a transparent bg; and its Remotion `Sequence`/audio duplication. If the wrapper proves ugly, fall back to releasing v0.0.7 of banodoco/timeline-composition. Release ability is UNVERIFIED: `gh` is not installed on this Mac, the unauthenticated API shows a public repo with tags v0.0.2..v0.0.6 and no releases, and memory says AstridPseudon could not push on 16 Oct. Treat release as blocked until the owner confirms; the wrapper is the default.

## 3. Stages (each landable alone; film keeps working)

**S0 Verification spikes (S, Haiku, read-only, before S1).**
(a) Who feeds the export: Astrid `managed_timeline.py:962-973` re-projects from pinned revisions, while Runtime `visual_seam.normalize_closure(materialize=True)` also builds `render_config` (store.py:1933). Trace which one the executor really renders; if only Astrid's, Runtime's materialized tracks need only keep seams honest. (b) Do agent tools (`timelines show`, onscreen, visualize) read the projected tracks or the SDK model? (c) 0.0.6 root background and what `theme` prop does (remotion/node_modules/@banodoco/timeline-composition). (d) Runtime `occurrence.track` missing from parent tracks (smoke timeline "Opening" has no `picture`): choose fallback = top of stack plus a warning.

**S1 Shared fixture + Astrid projection + stack order in export (M, Sonnet).**
- New `conformance/fixtures/shot-layering-v1.json` in Runtime (parent tracks, occurrences, child tracks, loose clips; expected flat track order incl. namespaced ids, group tags, per-clip track). Include the film case (picture shot, loose `type` clip) and a shot-only-suffix case (the old append-at-bottom bug).
- Astrid `shot_composition_projection.py`: replace `_track_merge` (:241-269) with `_group_tracks`; `_project_clip` (:291-366) writes the namespaced track; `_apply_placement_transform` (:153-178) writes group props to `app.group`, no per-child overwrite. Astrid pytest reads the shared fixture.
- DELETE: `_track_merge`, neighbour-insertion logic in the projection.
- Tests: tests that pin `_track_merge` order (find with grep `shot_composition_projection` in tests/) replaced by the fixture test.
- Acceptance: render a SANDBOX copy of the film, stills at 23.0, 23.9, 24.5, 26.0, 28.7, 28.85 s: clip-0 not visible, plate footage visible (old exporter, no isolation yet).

**S2 App projection + preview groups (M-L, Sonnet).**
- `VE/data/shotCompositionProjection.ts`: `tracksFor` (:271-316) -> `groupTracks`; `projectClip` (:318-433, track at :359) namespaces track; `timeline.effects` appended per child (:512-515) stay per child. Add helper `occurrenceClips(composition, base)` (seams/summaries need `{occurrenceId, shotId, trackId, atMs, clips}`; summaries already group by `clipIdentities`, lib/timeline-shot-summaries.ts:21-38,63-68).
- `VE/data/visualSeamContract.ts:340-357,523` and `portableVisualSeamIntent.ts`: lane key = `clip.app.group.sourceTrack ?? clip.track`, so cross-shot adjacency on `plate` is still found. Both lanes must equal Runtime's lane keys (fixture visual-seam-cases-v1.json).
- `VE/compositions/TimelineRenderer.tsx`: at the loop (:1598, :1664-1701) partition visual tracks into runs by `app.group.id`; render each group as an `AbsoluteFill` with `isolation:'isolate'`, group opacity/transform, and its OWN accumulate loop so effect-layers wrap only inner tracks (fixes the leak H3 §2-3). Extract the partition as a pure function `partitionTrackGroups(tracks)` in `VE/lib/` and export the same case table to the shared fixture.
- DELETE: `tracksFor`; `data/shotTrackOrder.fixture.json`.
- Replace tests: `shotCompositionProjection.test.ts:61` (flat merge order) -> shared fixture; `:288` (shared ids parent/child) -> namespaced; `:414` (same-lane cap) stays (lane = parent track); `canonicalCompositionState.test.ts:41,:60` unchanged in intent; `lib/timeline-shot-summaries.test.ts:13` and the seam suites keep expectations via sourceTrack. New: `TimelineRenderer.groups.test.tsx` (isolation style, inner effect scope, inner blend stays inside, group opacity composes). Run on Node 20, one heavy job at a time.
- Acceptance: preview of the sandbox film at the S1 times matches the S1 export stills (pixel diff under threshold; browser screenshot at 24s as in scratchpad/tl-23s/browser).

**S3 Runtime materialization + seam (M, Sonnet).**
- `runtime_protocol/visual_seam.py`: :313 (`child_tracks` merge), :337-341 (append at END of tracks), :343-346 -> namespaced group tracks at the occurrence slot; :420-440 lane key from sourceTrack; `docs/visual-seam-policy.md:21-22` rewrite the flattening rule.
- Fixtures: shot-layering-v1 consumed by tests/ (new `test_shot_layering_cases.py`); visual-seam-cases-v1.json stays green (App `visualSeamSharedCases.test.ts:56` via ASTRID_RUNTIME_CHECKOUT). Update contract/artifacts.json fixture digests (fixture bytes change).
- DELETE: `managed_render_snapshot.expand_shot_clips` (:28-220), and the fabricated `clipType:'shot'` parent in timeline_inspection.py:499-506, :652 precedence made to agree (child def parent-first).
- Schema/envelope (shot-composition.json) unchanged. Seam fixture order: S3 lands before/with S2 so App and Runtime lane keys agree.

**S4 Export isolation (M, Sonnet).** The Astrid wrapper (section 2): remotion/src/GroupedTimelineComposition.tsx, Root.tsx registration, run.py:116 composition id untouched. Tests: a node test on the partition function using the same shared fixture; a sandbox render of a synthetic 3 s timeline with a group blend + opacity (the film has none, see §4) compared with the preview. Effect-layer is `null` in 0.0.6 (TimelineComposition.tsx:61-63), so effects are not exported at all today, shot or not; the wrapper does not fix that (offer).

**S5 Delete the old lanes (M, Haiku grunt work + Sonnet review).**
- Astrid: `core/timeline/expand_shots.py` + its tests (only tests call it). Python `onscreen`/visualize adjusted if S0(b) says so.
- App: `ShotClipSequence` (TimelineRenderer.tsx:212-276, :1415-1416, shot child cache :139-187), `TimelineRenderer.shots.test.tsx` (476 lines), `hasNestedShots` (TimelineEditorCore.tsx:575, Body:549), `ClipAction.tsx:601`, the `userId === null` lane switch (canonicalCompositionState.ts:36-39 and 8 call sites listed in H2 §1; make the composition lane depend on document content only), `exportGuard.ts:1050`, `managedRuntimeClipTypes.ts:9`.
- NOT deleted (correction to the hypothesis): the vendored `@banodoco/timeline-composition` 0.0.2. The App imports `theme-api` and `registry.generated` from it in at least 7 files (TimelineRenderer.tsx:35, installed-themes.ts:4, astrid-element-host.ts:2, sequences/*). Only its dead TimelineComposition.tsx/VisualClip/AudioTrack copies (vendor/.../src) can go, after checking scripts/astrid-landing/public-source.patch:287.
- Also corrected: of the four neighbour-merge copies, S1 and S2 kill the two projections (App `tracksFor`, Astrid `_track_merge`); the two in timeline_restructure.py (:218-242 `flatten.add_track`, :451-469 `_layer_order`) are STORAGE conversions between chapter shots and one flat shot, still needed until the UNSPLIT-CHAPTERS decision. They stay (offer).

**S6 Timeline UI (S then M, Sonnet).** Settled: the canvas already shows one block per shot on the occurrence row, so no hiding of children.
1. S: shot dialog breadcrumb. AstridTimelineEditor.tsx:615-650 sr-only title -> visible "Parent timeline > Shot <name>" with a Back control (closes dialog); reuses `handleOpenCanonicalOccurrence` (:309-314).
2. S: change a shot's row via the inspector. `ShotOccurrenceInspectorSection` (PropertiesPanel.tsx:167-186) shows track read-only; make it a select writing `placement.track` through the existing parent publish path (`saveTimelineInOrder` dataProvider.ts:743-900 publishes occurrences; `occurrence.track` has no writer today, shotCompositionEditor.ts:170-173 only reads). Guard with `assertParentLanePlacement` (:212-237) for same-lane overlap.
3. M: drag the block between rows and along time: wire `moveCanonicalOccurrence` (shotCompositionEditor.ts:563) to a label/block drag in TimelineCanvas (positionedShotGroups :751-792). `trimCanonicalOccurrence` (:583) forbids anything but the content extent; leave trim out until the owner wants trimming (offer).
4. Show a hint in the block label when a loose clip is under the shot at that time (optional, offer).

Hosted editor on astrid.haus bundles its own App build: S2/S6 reach it only on a hosted deploy; the local :2222 live door needs its own update (owner go).

## 4. Effects in use (helper evidence)
Film: no `effect-layer` clips, no non-normal blend modes (only blendMode "normal"), no track opacity, no shot `transform` (all seven placements `transform: {}`), no child opacity != 1 (two opacity-0 snap-plate clips exist only in other realm bundles). So the effect/blend leak is NOT live on the film; the clip-0 order is the only live symptom. The isolation work (S2 renderer part, S4) is correctness for other timelines and should be tested on a synthetic sandbox timeline, not the film.

## 5. Migration (default; owner flagged clip-0 only)

H7: no single shot slot preserves all looks (film wants shot above `type`; chapters want sprites above shot). Default rule, run by a one-off script (Astrid `sdk`/scripts, dry-run first):
- A loose visual clip is LIFTED when it overlaps a shot occurrence's active window, sits on a row BELOW the shot's row, and draws over at least one of that shot's children today (its row index is above the child's track). Lifted clips move to a new track `<row>-over` inserted above the shot's row, one new track per source row, keeping their relative order; times, params, assets unchanged. Their look is therefore kept.
- Exceptions: clips the owner flagged as the bug stay below. Film: clip-0 (type, 23.867-28.867 s) STAYS (becomes hidden under shot 02/04, the owner's intent). clip-1 (196.567 s, at the timeline end) stays.
- Film result: no row changes; clip-0 hidden for its 5 s overlap. Chapters timelines (01M4GGKMHZ3J8V402C8CWSCE95, 01M53A4F6WYGNQAD3XHS6MKNY0): 5 loose clips hidden under nested: am-sprite-09/10/11 and c29-06 MYSTERY (sprite row, 85.667-93.3 s) get lifted to `sprite-over`; c17-05 (plate, loose, 57.967-58.167 s) is a plate/plate tie, default NOT lifted (owner question). Other 9 shot timelines: zero or no overlap; smoke-test timeline "Opening" (track `picture` absent) needs the S0(d) fallback.
- Safety: all migration runs on COPIES (new timeline ids) first; never write to the owner's timelines without the owner's go. Verification: before/after stills on the copies at film 23.9, 24.5, 26, 28.7, 28.85 s and chapters 58.1, 85.7, 87, 89.5, 91, 92.9 s: lifted clips must match "today"; clip-0 differs by intent. Rendering stills is the owner's call per the "no render" rule: ask in the same go-ahead.
- Shape of the stored data: lifted clips and new tracks are ordinary parent data; rollback = restore the previous revision (service.py:2580 restore keeps the exact payload).

## 6. Order and sizes
S0 S (Haiku) -> S1 M (Sonnet) -> S3 M (Sonnet, ahead of or with S2) -> S2 M-L (Sonnet, Haiku for test churn) -> S4 M (Sonnet) -> migration script M (Sonnet, dry-run) -> S5 M (Haiku, Sonnet review) -> S6 S+S, then M.
S1 and S4 are the only stages touching the exporter; S1 gives the visible fix in export alone. No stage needs the package repo.

## 7. Constraints honoured
App vitest on tools/node-v20.19.4-darwin-arm64/bin, one heavy job at a time. No `*.test.ts` under astrid/packs/*/rendering/elements/**. Each rule with an editor copy and a Runtime copy changes both plus shared cases (here three copies: App TS, Astrid Python, Runtime Python; one shared fixture in Runtime conformance/). Targets are the three mains; no live-door checkouts touched.

## 8. Open questions for the owner
1. A loose clip on the SAME row as a shot occurrence: shot over it (my default)?
2. c17-05 (0.2 s plate-on-plate): lift above the shot, or leave under?
3. Occurrence opacity/transform: composes at group level (default); no timeline uses it today.
4. Package release rights on banodoco/timeline-composition (unknown; `gh` missing): else the Astrid wrapper path.
5. Namespaced inner track ids appear in agent tools unless S0(b) finds a clean mapping: acceptable?
6. Frame stills on sandbox copies for the migration check: ok to render?

## 9. Out of scope (offers)
- three.js convention (ThreeTimelineComposition.tsx:343-387 opposite z): align or retire.
- ffmpeg backend (ignores tracks, command.py:82-88): refuse multi-track films with a clear message.
- TimelineEditorCoreBody duplication (978 vs 1017 lines).
- `pinnedShotGroups` writer (documentPlacement.ts:70-99 and friends) and its allowlists.
- Chapter-split copies and `timeline_restructure` neighbour inserts (UNSPLIT / SHOTS-ONE-COPY).
- Effect layers unsupported in the export (`effect-layer` -> null in 0.0.6).
- Shot trim from the canvas.

## Uncertainty summary
Unverified by me: which projection the executor consumes (S0a); 0.0.6 root background; same-track tie order for clip-0 vs c17-39 (moot after the change, shot wins); whether seam lane keys by `sourceTrack` reproduce today's seam reports (shared fixture will tell); package write access.
