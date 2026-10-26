# PLAN v2: a shot is one isolated layer at its occurrence slot

Plan only. Supersedes PLAN.md (v1 stays). Paths: App = labs/app-gallery-bar (VE = src/tools/video-editor), Astrid = live-door/Astrid, Runtime = live-door/Runtime. Land on the three mains, never the live checkouts. Drift (from v1, unchanged): low rebase risk; Astrid pins timeline-composition v0.0.6 (remotion/package.json:18).

## 0. What changed vs v1
- Runtime no longer learns the stacking rule (v1 S3 dropped). Export renders ASTRID's projection (invocation.py:1310 -> managed_timeline.py:903/967 -> invocation.py:1424); Runtime render_config is admission-only (store.py:2047, 2312-2326). So S0(a) is settled, not a spike.
- Two copies of the ordering rule only: App TS + Astrid Py, tied by one shared fixture.
- ONE release (App + Astrid + split fix + dialog fix + fixture) instead of S1/S2/S3 staged landings. No preview/export disagreement window.
- New root-cause fix: Astrid restructure stops hoisting visual crossers to film level (decision 4). Loose clips stop being created.
- Migration is three classes (was: lift-only). Chapter sprites are class (b), not "lifted".
- Occurrence opacity/transform: refused, not composed (decision 6). Per-child overwrite deleted.
- Shot dialog edits the shot's own timeline (decision 5).
- Add flows must not hide new work (decision 9).
- Export isolation is a follow-up, not part of the release.

## 1. Semantics

A shot occurrence is one compositing layer at the stack position of its occurrence's parent row. Inside it, its own tracks keep their own order. The finished shot composites into the parent as one image with alpha.

| Case | Result |
|---|---|
| Loose clip on a row above the shot's row | over the whole shot |
| Loose clip on a row below the shot's row | under the whole shot |
| Loose clip on the SAME row as the occurrence | the shot draws over it while active (rule). Add flows avoid creating this case (section 3.5) |
| Inner order | the shot's own track order, unchanged |
| Empty area of a shot | transparent; parent shows through |
| Inner blend / opacity / effect-layer | affect only inner content (release: App preview groups; export: S4 follow-up. Film uses none) |
| Occurrence opacity / transform | non-empty values REFUSED with a plain technical message (all 7 film placements are `{}`) |
| Audio | not layered; additive; occurrence gain/mute per clip as today |
| Visual clip crossing a shot boundary (restructure) | cut at the boundary into each covered shot on the same inner track; uncuttable types go to `<row>-over` and are reported by name |
| One level deep | already enforced (VE/data/shotCompositionProjection.ts:137-153, Runtime test_shot_composition_runtime.py:621) |

## 2. Representation (decided, not re-opened)
Group-tagged flat tracks. Per occurrence, each inner VISUAL track becomes `"<occ>~<track>"` with `app.group = { id: <occ>, sourceTrack: <track> }`, spliced contiguously at the occurrence row's index, group directly above that parent row. Child clips use the namespaced track id. Inner audio tracks keep merging by id. The group info is under `track.app.group` because a top-level track key is dropped by the App save sanitiser (timeline-domain.ts:212, 2482-2505). No schema or digest change (tracks.items has a free `app` object, timeline-config.schema.json:72-75).
Id spellings to keep apart: group track ids use `~`; the existing parent-projection CLIP ids are `${occurrenceId}:${clipId}` (shotCompositionProjection.ts:327-328, H-c). Do not conflate.

## 3. THE RELEASE (one landing, three mains, one deploy)

Contents land together; the hosted astrid.haus App deploy and the live Astrid update go out together. Sandbox/local test only before that.

### 3.1 Shared fixture (S, Haiku)
`conformance/fixtures/shot-layering-v1.json` in Runtime (fixture home; both App and Astrid already read shared Runtime fixtures, e.g. visualSeamSharedCases.test.ts:56 via ASTRID_RUNTIME_CHECKOUT). Cases: film (picture shot + loose `type` clip below), loose above, same-row, shot-only suffix tracks (old append-at-bottom bug), two shots on one row, occurrence missing its row (fallback: top of stack + warning; smoke timeline "Opening" has no `picture`). Expected: flat track order with namespaced ids, `app.group`, per-clip track. Fixture bytes change -> update contract/artifacts.json digest only for NEW file; existing visual-seam-cases-v1.json untouched.

### 3.2 Astrid (M, Sonnet)
- shot_composition_projection.py: replace `_track_merge` (:241-269) with `_group_tracks`; `_project_clip` (:291-366) writes the namespaced track. DELETE `_track_merge`, neighbour insertion, and the per-child opacity/transform overwrite (:165-166). `_apply_placement_transform` (:153-178) becomes a refuse-if-nonempty guard (plain message, names the occurrence).
- Restructure split fix (decision 4), timeline_restructure.py:
  - `plan()` branch :413-421: audio and music keep the hoist (:415-420). For a VISUAL clip, drop the crossing test; for every chapter j from k to the last starting before the clip end emit a piece into `chapters[j].clips`: start `max(s, wall_j)`, end `min(e, wall_j+1)`, `at = start - wall_j`, same `track`, stable id `_stable_id(id, j)`. `split()` (:476-550) already derives used tracks and asset registries from chapter.clips, so no further change there.
  - Piece builder is a per-type cutter (H-a findings, section 6): faithful types cut; others go to `<row>-over` (a parent row inserted above the shot row; reported by name in `describe()` :650 with a reason key).
  - Reuse `_set_length` (doc.py:56-64) for hold/from/to. NOT `Cut.split`/`_split_cut` (edits.py:165): that is the narrative-cut picture op, it does not shift params or keyframes and does not fit chapter pieces.
  - `differences()` (:608-631): the comparison is already ownership-blind (both sides projected flat, :559-606), but one flat clip vs N pieces fails counts/JSON. Edit: before comparing, re-join contiguous same-source pieces (ids derived from `_stable_id`, same track, `end == next.start`, `from` continuous, params equal after un-rebasing) on the restructured side; `-over` parents compare as they are. Check the inert tolerance (:624-627) while there.
- Tests pinning hoisting to REPLACE (tests/sdk/test_timeline_restructure.py): :163-177 (`cross` in parent.clips), :549-562 (`wide` on film), :249-262 (cross -> non-empty differences, keep intent via real mismatch), :180-183 (`differences(flat, split(flat)) == []` must still hold: this is the new acceptance), :211-224 and :272-291 review only. ADD: visual crosser across 2 and 3 chapters; cut piece round-trip equals flat render input; uncuttable type -> `-over` + reported; audio crosser still hoisted.
- Tests for the projection: replace anything pinning `_track_merge` order (grep `shot_composition_projection` in tests/) with the fixture test.
- Astrid does NOT touch the Remotion package in the release. The 0.0.6 composition paints per track in order (TimelineComposition.tsx:266), so contiguous namespaced tracks already fix clip-0 on the old exporter; group opacity/blend isolation is the S4 follow-up.

### 3.3 App (M-L, Sonnet; Haiku for test churn)
- VE/data/shotCompositionProjection.ts: `tracksFor` (:271-316) -> `groupTracks`; `projectClip` (:318-433, track at :359) namespaces track; per-child `timeline.effects` (:512-515) stay. Delete the placement overwrite equivalent; refuse non-empty occurrence opacity/transform with the same message. Add `occurrenceClips(composition, base)` for seams/summaries.
- Preview: VE/compositions/TimelineRenderer.tsx loop (:1598, :1664-1701): partition visual tracks by `app.group.id` via pure `partitionTrackGroups(tracks)` in VE/lib/; each group an `AbsoluteFill` with `isolation:isolate` and its own accumulate loop, so effect-layers wrap only inner tracks. Reuses the idea of `ShotClipSequence` isolation, not its code.
- Seams: visualSeamContract.ts:340-357 and :517/:523, portableVisualSeamIntent.ts: lane per (track, occurrence); the continuity check maps `app.group.sourceTrack` only where needed so cross-shot adjacency on `plate` is still found. Runtime already groups lanes by (track, occurrence) (visual_seam.py:420-424), so no Runtime change here.
- Shot dialog (decision 5), src/tools/travel-between-images/components/shotTimelineDataProvider.ts (note: NOT under video-editor): load via `loadCanonicalTimeline` (:191-234) must stop calling `projectCanonicalComposition` for the one occurrence (:201-206) and instead read `occurrence.revision.internal_timeline_revision.timeline` (shotCompositionEditor.ts:429, 594) with bare ids; save (`createCanonicalTimeline` :135-156, `saveTimeline` :236, call :277-282) writes bare timeline through `updateCanonicalShotTimeline` (shotCompositionEditor.ts:465). DELETE: the clip-id prefix strip (:136, :144); keep the `canonical`/`canonicalTiming` filter (:139) only if it still sees projection artifacts, else delete too; `remapIndependentInternalTimeline` (shotCompositionEditor.ts:148-160, call :309) prefixes on write: verify its guard (:305-309, not read by H-c) and delete if shot-local revisions then store bare ids. Persistence is CAS on the composition graph (provider :340); no dedicated shot endpoint. Tests: add shotTimelineDataProvider round-trip test (none exists); adjust ShotTimelinePreview.test.ts (~:265-361), shotCompositionEditor.test.ts, timeline-shot-summaries.test.ts:22 (still asserts the parent `:` prefix).
- Add flows (decision 9, H-b): rule helper `rowAboveShotsAt(config, t0, t1)` returns the target row (creating one if needed); apply in: `commands/media.ts:129-205` (add-media: no overlap check today), `lib/panel-clip-drag.ts:146-158` + `timeline-patch.ts:1099-1165` (clip.add: no occupancy check, also covers agent patches), `lib/external-drop-utils.ts:87-97, 280-400` (bottom-zone drop appends a row BELOW all rows, which is under any shot: change to the above-shot row when a shot covers t), `lib/shot-group-pack-commands.ts:152-226` (copy on the same row stacks over existing shots: check occupancy). Text overlay `hooks/clip-editing/useClipTextOverlay.ts:74-88` already goes to the top visual row or creates a new top row; keep, add the shot check in `handleAddTextAt` (:30-33). Gallery add-to-timeline (VideoEditorProvider.tsx:~598-625, timeline-asset-plans.ts:268-300) lands at timelineEnd, past all shots: safe, add a test only. Same-row loose clip vs shot stays defined by the rule. Duplicate clip (lib/duplicate-clip.ts) ripples, safe. NOT TRACED by H-b: pinned bottom-row AI generate/extend/effect handlers: first task of this sub-step.
- DELETE in the release: `tracksFor`, data/shotTrackOrder.fixture.json. Stage 5 deletions wait (section 5).
- Tests replaced: shotCompositionProjection.test.ts:61 (flat merge order) -> shared fixture; :288 (shared ids) -> namespaced; :414 (same-lane cap) stays (lane = parent track); canonicalCompositionState.test.ts:41,:60 unchanged in intent; seam suites keep expectations via sourceTrack. New: TimelineRenderer.groups.test.tsx (isolation style, inner effect scope, inner blend stays inside), partitionTrackGroups fixture test, add-flow tests (one per flow listed). App vitest on Node 20 (tools/node-v20.19.4-darwin-arm64/bin), one heavy job at a time. No *.test.ts under astrid/packs/*/rendering/elements/**.

### 3.4 Runtime (S, Sonnet)
- timeline_inspection.py:490-520: replace `expand_shot_clips` as the `render_timing` source. `render_timing` feeds only the inspection response (:513, :672, context :779), so the swap is safe. Non-expanding source (H-d): for each child with speed 1 and source_offset 0 (existing guard :495-496): `raw_at = occ.start + child.at`; `raw_end = raw_at + hold`; clip to `[occ.start, occ.start + occ.duration]`; drop if empty; if `from` exists add `(vis_at - raw_at)` and set `to = from + hold`; track defaults to the occurrence track. The record equals what `_timing_record` already makes, so `_timing_record` / `_render_timing_context` unchanged. Fix the FALSE parity comment at :491 ("same shot clipping producer as managed rendering"): managed rendering never calls it. Remove the fabricated `clipType:'shot'` parent (:499-506) only if the inspection path still works without it; check :652 precedence.
- `expand_shot_clips` (managed_render_snapshot.py:28-220, `__all__` :220): after the swap the only remaining callers are tests (test_direct_render_admission.py:12, 486-604; test_asset_identity.py:7, 36). Delete function and re-point those tests at the shared fixture in the deletions stage unless trivial now. The whole-tree grep for external consumers timed out in H-d: re-run once before deletion.
- visual_seam.py:337-346 is NOT reordered. Fixture lives in conformance/.

### 3.5 Acceptance (owner's film)
Sandbox COPY of timeline "almost-ready-no-first-second-v2" (project 811a657af5fe43e4b2b48a670de1f3e8), after restructure/migration logic runs on the copy:
1. Preview at 24.5 s: shot 02 footage (plate) visible, clip-0 hidden (hidden from 23.867 s to 28.867 s; owner calls its current visibility the bug).
2. Export of the sandbox copy at 23.0, 23.9, 24.5, 26.0, 28.7, 28.85 s agrees with preview (clip-0 not visible). RENDERING NEEDS OWNER OK ("no render" rule): ask in the go-ahead for the migration step.
3. Shared fixture green in App, Astrid (and Runtime conformance load).
4. `timelines restructure` on a film with visual crossers no longer refuses (differences group-aware).
5. Opening the shot dialog and saving a trivial change writes NO `~` ids and NO `app.group` into the shot's own timeline.

## 4. Follow-ups, in order

### F1. Export isolation S4 (M, Sonnet)
Astrid wrapper `GroupedTimelineComposition` in remotion/src (Root.tsx:2-8 default id): split visual tracks into runs (ungrouped / one group); bottom run keeps theme bg, upper runs transparent via a DEFAULT_THEME copy; audio only to the first run; `isolation:isolate` on group runs. Test: node test on partition with the shared fixture; synthetic 3 s sandbox timeline with a group blend (the film has no blends/effects) vs preview. Effect-layer renders null in 0.0.6 (TimelineComposition.tsx:61-63): not fixed here (offer). Fallback: v0.0.7 package release (rights unverified; `gh` missing, AstridPseudon push failed 16 Oct).

### F2. Migration (M, Sonnet; dry-run script, runs on COPIES first, owner go before real timelines)
Rule per loose visual clip overlapping a shot, comparing against that shot's content at that time TODAY:
(a) above ALL of the shot's content -> lift to `<row>-over` above the shot row (look kept).
(b) sandwiched -> cut into the shot(s) on the same inner track (same cutter as 3.2; look kept exactly).
(c) below all of it -> stays, becomes hidden, listed for the owner.
Owner exception: film clip-0 stays where it is (class (a) by look, left alone on purpose).
Counts (h7-realm-analysis, 18 timelines, 9 with shots, 4 with loose-vs-shot overlap):
| Timeline | Loose visual | Overlap pairs | Outcome |
|---|---|---|---|
| film almost-ready-no-first-second-v2 (7 shots) | 2 | 2 (clip-0 only) | clip-0 stays, hidden 23.867-28.867 s; clip-1 (196.567 s) no overlap |
| 01M4GGKMHZ3J8V402C8CWSCE95 chapters (8 shots) | 5 | 10 | 4 sprites class (b); c17-05 class (c) |
| 01M53A4F6WYGNQAD3XHS6MKNY0 chapters (04/05 fixed) (8 shots) | 5 | 10 | same as above |
| Render smoke 01M4G8W9VERXYSNEQC3J6HK987 (1 shot "Opening", no `picture` row; 4 loose text) | 4 | 2 | shot fallback slot; classify when run |
| 5 other shot timelines (01M4GFCX 8 shots, one-shot-original, v9-vision-trial, 01M4GBH85, r3s-import-trial) | 0 | 0 | nothing to do |
Chapters sprites: am-sprite-09/10/11 and c29-06 MYSTERY on `sprite` (idx 4), 85.667-93.3 s. Today they sit under shot 05's `type` clips and over plate (shot 06: under chrome c30-03/04 at 92.8-93.3 s), so sandwiched = class (b): cut at 90.8 s (and the 5/6 wall) into shots 05 and 06's inner `sprite` track. The am-sprite cutter must rebase keyframes (section 6); if it cannot, those clips fall to `-over`, which changes the look (they would cover type) and is reported. c17-05 (plate, 57.967-58.167 s) is below the type/fx children and ties plate children: class (c). Smoke "Opening" still needs the missing-row fallback.
Verification on copies: before/after stills at film 23.9, 24.5, 26, 28.7, 28.85 s and chapters 58.1, 85.7, 87, 89.5, 91, 92.9 s (render needs owner OK); class (a)/(b) match today, clip-0 and class (c) differ by intent. Rollback = restore previous revision (service.py:2580).

### F3. UI deltas (S, S, M; Sonnet)
1. Dialog breadcrumb: AstridTimelineEditor.tsx:615-650 sr-only title -> "Parent timeline > Shot <name>" + Back; reuses `handleOpenCanonicalOccurrence` (:309-314).
2. Row select in inspector: ShotOccurrenceInspectorSection (PropertiesPanel.tsx:167-186) writes `placement.track` via the parent publish path (dataProvider.ts:743-900); guard with `assertParentLanePlacement` (shotCompositionEditor.ts:212-237). Moving a shot below a loose clip changes the look: fine, it is the point.
3. Block drag across rows/time: wire `moveCanonicalOccurrence` (:563) to TimelineCanvas block drag (positionedShotGroups :751-792). Trim stays out (offer).

### F4. Deletions stage (M; Haiku grunt + Sonnet review)
- Astrid: core/timeline/expand_shots.py + its tests (only tests call it); onscreen/visualize adjusted (read config tracks: onscreen.py:248, timeline_visualize/model.py:524: namespaced ids appear to agents; map via `app.group.sourceTrack`).
- App: `ShotClipSequence` (TimelineRenderer.tsx:212-276, :1415-1416, child cache :139-187), TimelineRenderer.shots.test.tsx (476 lines), `hasNestedShots` (TimelineEditorCore.tsx:575, Body:549), ClipAction.tsx:601, the `userId === null` lane switch (canonicalCompositionState.ts:36-39, 8 call sites in H2 §1), exportGuard.ts:1050, managedRuntimeClipTypes.ts:9.
- Runtime: `expand_shot_clips` and its test callers (3.4).
- NOT deleted: vendored @banodoco/timeline-composition 0.0.2 (theme-api and registry.generated imported by 7+ files); only its dead TimelineComposition/VisualClip/AudioTrack copies, after checking scripts/astrid-landing/public-source.patch:287.
- The two timeline_restructure neighbour inserts (:218-242 `flatten.add_track`, :451-469 `_layer_order`) stay: storage conversions, needed until UNSPLIT-CHAPTERS.

## 5. Sizes and executors
Fixture S Haiku. Astrid projection + restructure split fix + differences M-L Sonnet. App projection/preview/seams/dialog/add-flows L Sonnet (Haiku test churn). Runtime S Sonnet. Release acceptance: Haiku runs fixtures, main thread judges stills. F1 M Sonnet. F2 M Sonnet (dry-run first). F3 S+S+M Sonnet. F4 M Haiku + Sonnet review. Order inside the release: fixture -> Astrid + App projections in parallel -> split fix -> dialog -> add flows -> Runtime -> acceptance on sandbox -> joint deploy.

## 6. Clip cutting: findings that shape the split fix (H-a)
- The SDK's `Cut.split`/`_split_cut` (model.py:797-806, edits.py:165) is the narrative-cut operation: it copies only the picture, advances top-level `from` (edits.py:189-190), touches no `params`, and does not shift timed words (`_filter_words` never called; `_split_audio` doc.py:~99-111 is the right pattern). It is not the primitive to reuse.
- Faithful by cutting with `_set_length`-style math: video/media (top-level from/to; renderer reads them, core/rendering/service.py:1198-1204, speed-aware), image/hold-only stills with no animation (clip-0 is this: a hold image), text and non-picture layers (local time continues).
- Not faithful as is: am-footage (in-point is `params.in`, component.tsx:240; `trimBefore`; zoom uses `frame/total`, :236) -> needs params.in advance plus zoom reparameterisation; treat as uncuttable unless a per-type cutter is written. am-sprite: keyframes are HELD POSES at clip-local frames (am-sprite component.tsx:53-70), so a cutter can be exact: piece 2 gets keyframes with `frame -= offsetFrames`, plus a frame-0 keyframe holding the active pose at the cut, earlier keyframes dropped. Other keyframed am-* (catalog.ts:1820, 4606 "clip-local"): uncuttable unless they declare a cutter.
- Design consequence: a small registry `CUTTERS[clipType]` (media, still, text, am-sprite) in Astrid; anything absent goes to `<row>-over` and is reported by name. The cutters live with the types; "which types cut" is data, not scattered branches. Unverified: the wrapper making element `useCurrentFrame()` clip-local (H-a did not find it); first task of the cutter work is to confirm it with a 2-clip sandbox render.
- Pre-existing, unfixed: windowed renders restart non-media animation at the window start (service.py:1188, 1198-1204). Offer.

## 7. Constraints
App vitest on Node 20 (tools/node-v20.19.4-darwin-arm64/bin), one heavy test job at a time. No *.test.ts under astrid/packs/*/rendering/elements/**. Land on the three mains. Hosted editor on astrid.haus bundles its own App build: it needs a hosted deploy; the local :2222 live door needs its own update (owner go). No renders, saves or timeline writes without owner OK. Rule copies: App TS + Astrid Py tied by the shared fixture (Runtime has no copy).

## 8. Offers (one line each)
- three.js convention: ThreeTimelineComposition.tsx:343-387 uses the opposite z order; align or retire.
- ffmpeg backend ignores tracks (command.py:82-88): refuse multi-track films with a clear message.
- Effect-layer renders null in export (0.0.6, TimelineComposition.tsx:61-63): no effects exported today.
- TimelineEditorCoreBody duplication (978 vs 1017 lines).
- `pinnedShotGroups` writer (documentPlacement.ts:70-99) and its allowlists.
- Chapter-split copies / UNSPLIT-CHAPTERS and the two restructure neighbour inserts.
- Canvas shot trim (`trimCanonicalOccurrence` :583 stays extent-only).
- Windowed-render animation restart (service.py:1188).

## 9. Remaining owner questions
1. OK to render stills on sandbox copies (acceptance and migration)?
2. am-footage and other keyframed am-*: ship with them going to `-over` + reported (default), or write cutters now?
3. Go for migration on the real chapters timelines after the copy check?
4. Package release rights on banodoco/timeline-composition (only matters if the wrapper proves ugly).
5. Namespaced `~` track ids visible in agent tools: acceptable (mapped via sourceTrack in tools)?

## Uncertainty
Unverified: wrapper making element frames clip-local; pinned-row AI button handlers; remapIndependentInternalTimeline guard (shotCompositionEditor.ts:305-309); external consumers of expand_shot_clips (grep timed out); 0.0.6 root background (F1); whether a hold image's absence of `from` makes every still trivially cuttable (true by `_set_length`, doc.py:56-64).
