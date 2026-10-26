# A shot is one layer at its row

Plan, 26 Oct 2026. Plan only: nothing here has been changed, rendered or saved.

Short version. Today a shot's clips are poured onto the main tracks and stacked by those tracks, so the row a shot sits on does nothing. A loose image on the Type row therefore draws over the shot's footage, although the shot sits on the top row. The fix is to treat a shot as one layer at its row, with its own clips stacked inside it. We do this in one release across the App, Astrid and Runtime, then migrate the existing timelines.

Names used below. App is the editor (repo `labs/app-gallery-bar`; `VE` means `src/tools/video-editor`). Astrid is the agent and renderer (`live-door/Astrid`). Runtime is the service that stores timelines (`live-door/Runtime`). Paths are inside those repos.

---

## 1. The problem in plain words

### 1.1 What you see

Open the film "almost-ready-no-first-second-v2". At about 23.8 s a still image (the otter and the crate tree) appears and stays until about 28.9 s. The editor shows that image as a small block on the Type row. Shot 02, "The Vision", sits on the top Picture row and covers 9.1 s to 28.7 s. A shot on the top row should draw over anything on a lower row. It does not.

![The editor at 24 s: the Picture row shows the shot, the Type row holds one small image block, and the preview shows the image.](evidence/24s-editor.png)

Browser proof. Same film, preview at 24.5 s:

![Preview at 24.5 s: the otter and crate tree.](evidence/preview-245.png)

Then we hid that one image clip and looked again:

![Preview at 24.5 s with the image hidden: shot 02's footage (the ASTRID machine) was underneath the whole time.](evidence/preview-245-img-hidden.png)

So the shot's footage is playing. The loose image is drawn on top of it. The image is a single hold clip, `clip-0`, on track `type`, 23.867 s to 28.867 s, with opacity 1 (raw data in [H7](sources/H7-migration.md)).

### 1.2 The wider problem

The 23.8 s image is one symptom. The cause is that the editor shows one thing and draws another, and the code keeps several copies of the conversion between the two. Section 2 covers it in full.

---

## 2. Why it happens: the whole problem

### 2.1 The timeline shows a layer; preview and export draw a flattened pile

In the timeline, a shot is one block on its occurrence row. Its children are not on the main rows. The shot's row is Picture, the top one.

Preview and export do something else. They take each child clip of the shot and put it on the main track with the same id (`plate`, `fx`, `type`, and so on), then stack everything by main track order. The shot's own row has no effect on stacking.
- App preview/export lane: `VE/data/shotCompositionProjection.ts:271-316` (track list), `:318-433` (each clip; the track at `:359`), `:440-590` (whole projection; parent shot clips dropped at `:532`).
- Astrid export: `astrid/core/timeline/shot_composition_projection.py:241-269` (track merge), `:291-366` (clip). Its output is one flat list of tracks and clips (`config.clips`, `config.tracks`) with clip ids namespaced per occurrence ([H5](sources/H5-astrid-render.md) section 2).
- The renderers paint tracks in array order, first track on top: App `VE/compositions/TimelineRenderer.tsx:1598` and loop `:1664-1701`; Astrid's Remotion package `@banodoco/timeline-composition` 0.0.6, `TimelineComposition.tsx:266`.

In the film, the shot's `plate` clips land on the main `plate` row (low). The loose image sits on `type` (higher). Higher row wins, so the image covers the footage. Nothing in the picture consults the shot's row. Full trace and the ordering table: [H8](sources/H8-smells.md) sections 1 and 3.

Where a shot has its own tracks that the parent lacks, the projection splices them next to a neighbour, and if nothing below them is shared it appends them at the BOTTOM of the stack. That is the "titles hidden under plate" bug of 17 Oct (section 2.6).

### 2.2 How the loose image got there

The film is stored as chapters, and each chapter is a real shot. That came from the 16 Oct chapter split: `timelines restructure` splits one flat working copy into one shot per chapter (commit `a0949881e`).

The split puts every clip inside the chapter it starts in. A clip that crosses a chapter boundary is not cut. It is moved up to the film level as a loose clip: `astrid/sdk/timeline_restructure.py:413-427` (the test for "crosses the wall" at `:413-421`; the loose clip is appended to the film list at `:422-427`). Music is hoisted the same way.

`clip-0` starts at 23.867 s inside shot 02 and ends at 28.867 s, past the wall at 28.667 s. So it became a loose clip. Chapter 05's sprites (85.667-93.3 s) cross the 90.8 s wall the same way.

Agents never see the problem. They edit a flat working copy: checkout flattens a chapter film into one shot (`astrid/sdk/timeline/checkout.py:39-41, :325-327`; `timeline_restructure.py:295`). In that copy `clip-0` is one clip on `type` over the plate, so the on-screen model and checks show the image on top (`astrid/core/timeline/onscreen.py:248-292`, `duration.py:292-309`). The flat copy and the stored shots disagree about what the film looks like, and the check reads the flat one.

### 2.3 A second bug waiting: effects and blends leak out of shots

Because inner tracks share the main tracks' ids, a shot's inner effect layer on `fx` wraps every main track below `fx`, not just the shot's own tracks. A blend mode on an inner track blends against the main tracks drawn before it. (`VE/compositions/TimelineRenderer.tsx:1664-1701`, `EffectLayerSequence.tsx:19-72`; analysis in [H3](sources/H3-preview-render.md) sections 2-3.)

This is not live on the film: it has no effect-layer clips, no blend mode other than normal, no track opacity, no shot transform (all seven placements are `{}`). It is a correctness bug for other timelines and for later work.

### 2.4 Two drawing paths in the editor, chosen by a sentinel

The editor has two ways to draw a shot. The canonical path flattens it (section 2.1). The legacy path, `ShotClipSequence` (`VE/compositions/TimelineRenderer.tsx:212-276`, dispatched at `:1415-1416`), draws a real nested renderer for a clip of type `shot`. It is a sub-timeline, which is close to the model we want, but it is only reachable for old data.

The editor picks the path with `userId === null`: `VE/data/canonicalCompositionState.ts:36-39` and at least seven more call sites (for example `useRenderState.ts:568-574`, `CompactPreview.tsx:28-34`, `hooks/useTimelineState.ts:1136`; list in [H8](sources/H8-smells.md) section 6). The same `null` also means "signed out" (`AuthContext.tsx:55,87`) and "Runtime mode". The dev extension harness already flips to the legacy path through a fake user id. This is a hidden mode: `userId` here is an editor prop, not the signed-in user. Every real page passes `null` (`pages/VideoEditorPage.tsx:149,168`), so the flattening path always runs and the nested path survives only in dev harness pages.

### 2.5 Copies of the same logic

- Projection and ordering: App TypeScript (`shotCompositionProjection.ts`), Astrid Python (`shot_composition_projection.py`, 686 lines), and Runtime Python (`runtime_protocol/visual_seam.py:312-346`). Runtime never reaches frames: its `render_config` is for admission only (`store.py:2047, 2312-2326`). Export renders Astrid's projection (`invocation.py:1310` to `managed_timeline.py:903/967` to `invocation.py:1424`).
- Four merge-by-neighbour track splicers with the same append-at-bottom edge: App `tracksFor` (`shotCompositionProjection.ts:271-315`), Astrid `_track_merge` (`shot_composition_projection.py:241-270`), and the two in `timeline_restructure.py` (`flatten.add_track` `:212-245`, `_layer_order` `:451-470`). They agree except that the App skips tracks with role "source" and the Astrid copy does not.
- Dead flatteners: Astrid `core/timeline/expand_shots.py` (271 lines, only tests call it) and Runtime `managed_render_snapshot.expand_shot_clips` (`:28-220`), kept alive only because `timeline_inspection.py:499-506` fabricates a `shot` clip to feed it. Its comment at `:491` says it uses "the same shot clipping producer as managed rendering"; managed rendering does not call it.
- Unused vendored composition in the App: `vendor/timeline-composition` 0.0.2. No App source imports its `TimelineComposition`; the App draws with its own `TimelineRenderer.tsx` (1771 lines). The vendor package is still imported for `theme-api` and `registry.generated`, so it cannot simply be removed.
- Preview renderer vs export package: two code bases that happen to share a track order convention. The export package returns nothing for `effect-layer` (`TimelineComposition.tsx:61-63`: effect layers are not exported at all). The three.js backend uses the opposite order (`remotion/src/ThreeTimelineComposition.tsx:343-387`; its own live-scene stack at `:451` uses the usual order). The ffmpeg backend ignores tracks (`packs/rendering/.../ffmpeg/command.py:78-88`).
- Also a chapter-split copy problem: the split copies film-wide track definitions into every chapter shot (`timeline_restructure.py:19-22`).

### 2.6 History: the same class of bug three times

1. 16 Oct, chapter split. Chapters stored as shots, one flat copy to edit. Crossing clips hoisted to loose clips (`a0949881e`, `e0b9bd94d`). This is the origin of `clip-0`.
2. 17 Oct, titles under plate. Shot-only title tracks were appended at the bottom of the stack, under the footage. A shot-only track ordering commit followed (`e75d793e7`, diff not reviewed here); all four splicer copies still carry the bottom-append rule today. Today's image over shot 02 is the same class: the stored shot and the drawn picture disagree.
3. 22 Oct, RT3-05 drift. A copied asset's fields were lost in one copy of film-wide data, so flatten refused the film with `conflicting asset key 'RT3-05'`. Fixed the same day (`2f92ff099`, `cb98e249b`), but the class (several copies of one fact) remains.

Source for the dates and quotes: [H1](sources/H1-prior-art.md).

### 2.7 Root cause in four sentences

Shots are stored as sub-timelines but drawn as clips poured onto shared main tracks, so the shot's row has no say in the stack. Every consumer that needs the picture (App preview, Astrid export, the flat working copy, the restructure round trip) carries its own conversion between the two forms, and the conversions disagree. The chapter split then creates loose clips by hoisting anything that crosses a boundary, which the flattened drawing places above the shot. Until a shot is drawn as one layer, this keeps coming back.

---

## 3. The decided model

Your words: a shot is a sub-timeline. Its clips sit on its own tracks, and the shot as a whole sits as one layer at the row its occurrence is on. It respects the main layering and the layering inside it. Like a nested sequence in Premiere.

| Case | Result |
|---|---|
| Loose clip on a row above the shot's row | over the whole shot |
| Loose clip on a row below the shot's row | under the whole shot |
| Loose clip on the same row as the shot | the shot draws over it while the shot is active. The editor avoids creating this case |
| Order inside the shot | the shot's own track order, unchanged |
| Empty area of a shot | transparent; the parent shows through |
| Inner blend, opacity, effect layer | affect only the shot's inner content |
| Shot opacity or transform | refused with a plain message (all seven placements on the film are empty) |
| Audio | not layered; mixes additively; gain and mute stay per clip |
| Visual clip crossing a shot boundary during a split | cut at the boundary into each shot it covers, on the same inner track |
| Nesting | one level deep, as today |

Representation. The saved timeline keeps a flat list of tracks and clips. Each inner visual track of a shot becomes a track named `<occurrence>~<track>`, with `app.group = { id, sourceTrack }`, placed directly above the shot's row. The group information lives under `track.app.group` because a new top-level track field would be dropped by the App's save sanitiser (`VE/lib/timeline-domain.ts:212, 2482-2505`). This needs no schema change and no package release. Inner audio tracks still merge by id.

---

## 4. Recommendation: one release

Everything below lands together on the three mains, and the hosted astrid.haus editor deploy and the live Astrid update go out together. That way preview and export never disagree. Nothing is released until you say so.

### 4.1 Shared fixture
A new file `conformance/fixtures/shot-layering-v1.json` in Runtime. Cases: the film (shot on picture, loose clip on type), loose above, same row, shot-only suffix tracks (the old bottom-append bug), two shots on one row, a shot whose row is missing (falls back to the top of the stack with a warning). Expected output: flat track order, group tags, each clip's track. App and Astrid tests both read it. Runtime does not learn the rule.

### 4.2 Astrid
- Replace `_track_merge` with a group builder; clips take the namespaced track (`shot_composition_projection.py:241-269, 291-366`). Delete `_track_merge`, the neighbour insertion, and the per-child opacity and transform overwrite (`:165-166`). Non-empty shot opacity or transform now refuses with a named message.
- Fix the split (`timeline_restructure.py:413-427`). Visual clips that cross a boundary are cut at each boundary, staying on the same inner track, with a new stable id per piece. Audio and music keep today's hoisting. Pieces are built per clip type by a small cutter list:
  - cut faithfully: video and other media (source offset advances with speed), still images (clip-0 is one), text;
  - cut faithfully with extra work: `am-sprite`, whose keyframes are held poses at clip-local frames, so the second piece shifts them and gets a starting pose;
  - not cut: `am-footage` (its in-point is in `params.in` and its zoom restarts) and other keyframed `am-*` clips. These go to a new `<row>-over` row above the shot row and are reported by name.
  The existing `Cut.split` (`astrid/sdk/timeline/edits.py:165`) is not reused; it only handles the picture layer and shifts no params or keyframes. The cutter reuses the length math in `astrid/sdk/timeline/doc.py:56-64`.
- Make `differences()` (`timeline_restructure.py:608-631`) group-aware, so `timelines restructure` compares the flat copy to the cut result and does not refuse every film. It re-joins contiguous pieces of one clip before comparing.
- Tests: replace those that pin hoisting (`tests/sdk/test_timeline_restructure.py:163-177, 549-562, 249-262`; keep `:180-183` as the new acceptance); add tests for crossers over two and three chapters, a round trip against the flat render input, an uncuttable type going to `-over`, and audio still hoisting. Replace projection-order tests with the fixture.
- Not in this release: the Remotion package (it already paints per track in order, so contiguous inner tracks fix the film in export).

### 4.3 App
- Projection: `tracksFor` becomes a group builder; `projectClip` writes the namespaced track; shot opacity and transform refuse. Delete `tracksFor` and `data/shotTrackOrder.fixture.json`.
- Preview: split visual tracks into groups with a small pure function (`partitionTrackGroups`). Each group is drawn in its own isolated container with its own stacking loop, so effect layers wrap only the shot's own tracks and blends stay inside.
- Seams: a clip's lane is its (track, occurrence) as the Runtime already does; the continuity check maps `app.group.sourceTrack` only where needed (`VE/data/visualSeamContract.ts:340-357, 517, 523`; `portableVisualSeamIntent.ts`).
- Shot dialog: it must read and save the shot's own timeline, never the parent projection, so `occ~` ids and `app.group` cannot be written into a shot. Today it loads through `projectCanonicalComposition` (`src/tools/travel-between-images/components/shotTimelineDataProvider.ts:191-234`) and strips prefixes on save (`:135-156`, calling `updateCanonicalShotTimeline`, `VE/data/shotCompositionEditor.ts:465`). New: read `occurrence.revision.internal_timeline_revision.timeline` and save it back. Delete the prefix stripping (`:136, :144`), and `remapIndependentInternalTimeline` (`shotCompositionEditor.ts:148-160`) once shot-local revisions store bare ids (its guard at `:305-309` still needs to be read).
- Add flows. Any flow that creates a visual clip at a time a shot covers must target a row above that shot's row, creating one if needed. The flows without such a check today: add-media (`VE/commands/media.ts:129-205`), `clip.add` (panel drag and agent patches, `lib/panel-clip-drag.ts:146-158`, `lib/timeline-patch.ts:1099-1165`), file drops into the bottom zone, which appends a row below everything (`lib/external-drop-utils.ts:87-97, 280-400`), and shot-group duplicate (`lib/shot-group-pack-commands.ts:152-226`). Text overlay already goes to the top row or makes a new one (`hooks/clip-editing/useClipTextOverlay.ts:74-88`) and gets a shot check in `handleAddTextAt`. Gallery add lands at the timeline end, past every shot. The pinned bottom-row AI buttons were not traced; that is the first task here.
- Tests: replace `shotCompositionProjection.test.ts` order cases (`:61`, `:288`) with the fixture; keep the same-lane cap (`:414`); new tests for group drawing, group partition, each add flow, and a dialog round trip (none exists today). App tests run on Node 20 (`tools/node-v20.19.4-darwin-arm64/bin`), one heavy job at a time. No test files under `astrid/packs/*/rendering/elements/**`.

### 4.4 Runtime
- `runtime_protocol/timeline_inspection.py:490-520`: replace `expand_shot_clips` as the source of `render_timing`. It feeds only the inspection response. The new source is the occurrence's start and duration plus the child clip times, clipped to the occurrence (children with speed 1 and offset 0, as today). Fix the false comment at `:491`.
- Runtime does not reorder tracks (`visual_seam.py:337-346` is left alone). `expand_shot_clips` loses its last production caller; its tests move to the fixture and it is deleted in the deletions step (section 5.4).

### 4.5 Acceptance on the film
On a sandbox copy of the film, never the real one:
1. Preview at 24.5 s shows shot 02's footage; `clip-0` is hidden (from 23.867 s to 28.867 s).
2. Export of the sandbox copy at 23.0, 23.9, 24.5, 26.0, 28.7, 28.85 s agrees with preview. Rendering needs your OK.
3. The shared fixture passes in the App and in Astrid, and Runtime loads it.
4. `timelines restructure` accepts a film with visual crossers.
5. Opening and saving a shot dialog writes no `~` ids and no `app.group` into the shot.

Sizes. Fixture small; Astrid medium-large; App large; Runtime small. Intricate pieces (projection, split fix, preview groups, dialog) by Sonnet; grunt work and test churn by Haiku.

---

## 5. Follow-ups, in order

### 5.1 Export isolation
Preview isolates a shot; the 0.0.6 export package does not, so a blend or effect inside a shot could still reach other tracks in export. Add an Astrid wrapper composition (`remotion/src`) that renders each group as its own run: bottom run keeps the theme background, upper runs are transparent, audio goes to one run. The film has no blends or effects, so test it on a synthetic timeline. Fallback: a v0.0.7 package release, which needs release rights (`gh` is not installed here; unverified).

### 5.2 Migration
Run per loose visual clip that overlaps a shot, on copies first. Compare with what the shot shows at that time today:
- (a) above all of the shot's content: lift it to a new `<row>-over` above the shot row. The look is kept.
- (b) between the shot's layers: cut it into the shot or shots on the same inner track (the same cutter as the split fix). The look is kept exactly.
- (c) below all of it: it stays, becomes hidden, and is listed for you.
Exception you flagged: the film's `clip-0` stays where it is, hidden under shot 02 from 23.867 s.

Counts from the realm scan (18 timelines; 9 have shots; 4 have a loose clip overlapping a shot; [H7](sources/H7-migration.md)):

| Timeline | Loose visual clips | Overlap pairs | Outcome |
|---|---|---|---|
| Film, almost-ready-no-first-second-v2 (7 shots) | 2 | 2 (`clip-0` only) | `clip-0` stays, hidden 23.867-28.867 s. `clip-1` (196.567 s) has no overlap |
| Chapters 01M4GGKMHZ3J8V402C8CWSCE95 (8 shots) | 5 | 10 | 4 sprites class (b); `c17-05` class (c) |
| Chapters 01M53A4F6WYGNQAD3XHS6MKNY0, "(04/05 fixed)" (8 shots) | 5 | 10 | same as above |
| Render smoke 01M4G8W9VERXYSNEQC3J6HK987 (1 shot "Opening", no `picture` row; 4 loose text clips) | 4 | 2 | falls back to the top of the stack; classify when run |
| Five other shot timelines (8-shot 01M4GFCX, one-shot-original, v9-vision-trial, 01M4GBH85, r3s-import-trial) | 0 | 0 | nothing to do |

The chapters sprites (`am-sprite-09/10/11` and `c29-06` MYSTERY, on `sprite`, 85.667-93.3 s) sit today under shot 05's `type` clips and over its `plate`; in shot 06 they sit under its `chrome` clips at 92.8-93.3 s. That is "between the layers", class (b): cut at 90.8 s into the inner `sprite` tracks of shots 05 and 06. If the sprite cutter cannot be made exact, those clips would fall back to `-over` and cover the type clips, which changes the look; they would then be reported. `c17-05` (a 0.2 s plate clip at 57.967-58.167 s) is below the type and fx clips and ties with the plate clips: class (c).

Checks on copies: stills at film 23.9, 24.5, 26, 28.7, 28.85 s and chapters 58.1, 85.7, 87, 89.5, 91, 92.9 s. Class (a) and (b) must match today; `clip-0` and class (c) differ on purpose. Rollback: restore the previous revision (`service.py:2580`). Nothing touches your real timelines without your go.

### 5.3 UI changes
1. Shot dialog breadcrumb: "Parent timeline > Shot name" with a Back control (`AstridTimelineEditor.tsx:615-650`, `handleOpenCanonicalOccurrence` `:309-314`).
2. Row select in the inspector for a shot's row (`PropertiesPanel.tsx:167-186`), saved through the parent publish path with the overlap guard `assertParentLanePlacement` (`shotCompositionEditor.ts:212-237`).
3. Drag a shot block between rows and along time (`moveCanonicalOccurrence` `:563`; positioned groups in `TimelineCanvas` `:751-792`). Trim stays out.

### 5.4 Deletions
- Astrid: `core/timeline/expand_shots.py` and its tests. Agent tools (`onscreen.py:248`, `timeline_visualize/model.py:524`) read config tracks; they show the source track name through `app.group.sourceTrack` (for example "shot 02 · type"), never the internal `~` id.
- App: `ShotClipSequence` and its child cache (`TimelineRenderer.tsx:212-276, :1415-1416, :139-187`), `TimelineRenderer.shots.test.tsx` (476 lines), `hasNestedShots` (`TimelineEditorCore.tsx:575`, `...Body.tsx:549`), `ClipAction.tsx:601`, the `userId === null` lane switch (`canonicalCompositionState.ts:36-39` and its call sites; the lane then depends on the document only), `exportGuard.ts:1050`, `managedRuntimeClipTypes.ts:9`.
- Runtime: `expand_shot_clips` and the tests that call it. Re-run the whole-repo search for other callers first (the helper's search timed out).
- Not deleted: the vendored composition package (still imported for `theme-api` and `registry.generated`); only its dead `TimelineComposition`, `VisualClip`, `AudioTrack` copies can go, after checking `scripts/astrid-landing/public-source.patch:287`.
- Stays: the two `timeline_restructure.py` neighbour splicers (`:218-242`, `:451-469`). They convert between chapter shots and one flat shot and are needed until the unsplit-chapters decision.

---

## 6. What happens to your film and the chapters timelines

The film (7 shots, all on `picture`, 539 shot clips): the only loose clips are `clip-0` and `clip-1`. After the release, `clip-0` is hidden under shot 02 and shot 04 from 23.867 s to 28.867 s and the footage shows, as you wanted. Nothing else changes. Inner order inside every shot is already a subset of the parent's order, so it is unchanged.

The two chapters timelines: with the release alone, shots draw over everything on lower rows, so the four sprites would be hidden under shots 05 and 06 and `c17-05` would be hidden under the shot's plate. The migration (class (b) for the sprites) keeps them visible by cutting them into the shots at the right layer. Run on copies first, checked with the stills above.

The smoke timeline "Opening" has no `picture` row, so its shot gets the top-of-stack fallback.

---

## 7. Decisions taken and why

- Flat tracks tagged with a group, not a nested clip. A nested clip needs a new clip shape in the shared schema, a package release for export, a second consumer path and a new child loader (H3 option A, medium-large). Flat tracks need no schema change, keep the seam checks, data lanes, summaries and transcript on one flat list, and make cheaper previews. The internal `~` track ids stay internal: agent tools and the editor show the source track name.
- Clip types that can't be cut faithfully yet (`am-footage` and other keyframed `am-*` clips) go to a `<row>-over` row above the shot and are reported by name; cutters for them can follow if that ever matters. `am-sprite` gets a cutter now because the chapters sprites need it.
- Two copies of the ordering rule, not three. Runtime never reaches frames, so it does not learn the rule; the Runtime copy that v1 proposed was dropped.
- One release, not staged landings. Staged landings leave preview and export disagreeing for a while, which is the failure we are fixing.
- Fix where loose clips come from. Migration alone would let the next split re-create them.
- Refuse shot opacity and transform instead of building a group transform rule in two renderers. All seven placements are empty.
- The dialog edits the shot's own timeline. Reading the parent projection is how prefixed ids could leak back into a shot.
- Add flows target a row above covered shots. Otherwise new work silently hides under a shot.
- Export isolation comes after the release. The film uses no blends or effects, and the 0.0.6 package already orders tracks correctly.
- Rejected: reuse of `ShotClipSequence` as the base (opaque black background, loads children through the legacy loader, tests only pin that loader), and a low "plate" slot for shots (keeps the film's look but not the chapters', where sprites sit above the plate; H7).

---

## 8. Questions for you

1. Go to build the release (App, Astrid, Runtime, fixture)?
2. OK to render stills on sandbox copies (the acceptance check and the migration check)?
3. After the copy check, go to migrate the real chapters timelines?

Not yet verified: that element frames are clip-local in the renderer (a 2-clip sandbox render settles it); the pinned-row AI buttons; the guard in `remapIndependentInternalTimeline`; callers of `expand_shot_clips` outside Runtime.

---

## 9. Offers

- three.js backend: it stacks tracks in the opposite order; align or retire it.
- ffmpeg backend: it ignores tracks; refuse multi-track films with a clear message.
- Effect layers are not exported at all today (the export package draws nothing for them).
- `TimelineEditorCoreBody` and `TimelineEditorCore` are two near-copies (978 vs 1017 lines).
- The `pinnedShotGroups` writer on the Shots page (`documentPlacement.ts:70-99`) and its allowlists.
- Chapter-split copies and the two neighbour splicers in `timeline_restructure.py` (unsplit-chapters).
- Canvas shot trim (`trimCanonicalOccurrence` `:583` is extent-only).
- Windowed renders restart non-media animation at the window start (`core/rendering/service.py:1188`).

---

## 10. Sources

Research reports (read-only, 26 Oct), copied into `sources/`:
- [H1 prior art](sources/H1-prior-art.md): intent of shots over time, flatten decisions, constraints.
- [H2 editor data](sources/H2-editor-data.md): projection, lanes, `userId` switch.
- [H3 preview and render](sources/H3-preview-render.md): nested vs flat, effect and blend scope.
- [H4 timeline UI](sources/H4-timeline-ui.md): rows, shot blocks, inspector, drag.
- [H5 Astrid render](sources/H5-astrid-render.md): export path, flatteners, agent tools.
- [H6 Runtime](sources/H6-runtime.md): seam, flattening, admission.
- [H7 migration](sources/H7-migration.md): what changes per timeline, with the per-timeline scan results.
- [H8 smells](sources/H8-smells.md): copies, dead code, hidden modes.
- [Plan v1](sources/PLAN-v1.md) and [Plan v2](sources/PLAN-v2.md): earlier drafts of this plan (v2 is the engineering version with the helper findings).
Evidence images are in `evidence/`.
