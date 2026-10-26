# H5 - Astrid render pipeline and layering (read-only)

Repo: /Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/Astrid
State: detached HEAD at 8b6ed2116fd1803d24b2be5bc08bd9490407fe4a. Local origin/main ref is 64197afa297f86f1e738238d5e80aff6d33e303a.
HEAD is an ancestor of that ref, 43 commits behind (`rev-list --count HEAD...origin/main` = 0 / 43). I did not fetch (dry-run printed nothing), so the remote may be further ahead.
Paths below are relative to the repo root.

## 1. Render pipeline: shots -> frames

### Flatten / expand functions (there is no single one; there are five plus two track-merge copies)

| Function | file:line | Who calls it | Role |
|---|---|---|---|
| `expand_shot_clips` | astrid/core/timeline/expand_shots.py:37 | tests only (tests/test_storyboard_repair_p4_p5.py:11,91,130). Docstring says "retained only for explicit offline migration and repair" (:6-8). No production caller in Astrid. | Legacy `clipType == "shot"` expansion, sub-clips offset by `parent.at + sub.at` (:224), clamped to parent window (:226-257). |
| `project_runtime_parent_composition` | astrid/core/timeline/shot_composition_projection.py:454 | Production render: astrid/packs/rendering/actions/render/managed_timeline.py:962-973. Also astrid/sdk/authoring_render_preview.py:71,163, and astrid/sdk/timeline_restructure.py:562-577 (`renderer_input`). | Canonical path. Consumes Runtime-pinned occurrences + shot revisions + internal timeline revisions. |
| `project_shot_composition` | shot_composition_projection.py:369 | astrid/core/timeline/snapshot.py:281, astrid/packs/rendering/actions/timeline_storyboard/run.py:286. Alias `project_canonical_shot_composition` (:678). | Graph-input variant of the same projection. |
| `_track_merge` | shot_composition_projection.py:241-269 | Both projections (:397, :574). | Merges shot tracks into parent `config.tracks`. |
| `_project_clip` | shot_composition_projection.py:291-366 | Called per child clip from the projection (:633). | Offsets child `at` by occurrence start (:308), clips to occurrence window (:310-313), namespaces id `occurrence_id:clip_id` (:329-331). |
| `flatten` | astrid/sdk/timeline_restructure.py:295 | astrid/sdk/timeline/checkout.py:39-41, :325-327; astrid/sdk/timeline/publish.py:97-99. | Editor working copy only: collapses a chapter film (one shot per chapter) into ONE flat shot. Not used on render. |
| `_flat_side` (with nested `add_track`) | timeline_restructure.py:198 (add_track :218-242) | flatten (:299). | Concatenates chapter clips with `at += start` (:276), keeps shot track order via neighbour insertion (:224-241). |
| `split` / `plan` | timeline_restructure.py:476 / :377 | publish.py:234-237 | Inverse of flatten. Film-level clips = music or clips crossing a chapter wall (:419-421). Stores complete track order on the film (:492-494). |
| `_layer_order` | timeline_restructure.py:451-469 | plan() at :432 only, result becomes `planned.tracks` -> `config["tracks"]` (:494). | Third copy of the same neighbour-insertion algorithm. |
| `renderer_input` | timeline_restructure.py:559-600 | `assert_equivalent` (:614), split guard (:660). | Equivalence check only; it is not the render. |
| `visual_tracks_paint_order` | astrid/core/timeline/duration.py:292-309 | timeline_visualize/model.py:524-525 | Paint order helper (docstring :295-299: first config visual track is topmost). |
| on-screen model `_build` | astrid/core/timeline/onscreen.py:248-292 | onscreen model (z 0 = top, :40) | Sorts by config `track_index` then reverse position (:271). Own ordering on the flat config. |

Track-merge copies (three near-identical neighbour-insertion algorithms):
- timeline_restructure.py:218-242 (add_track, flatten)
- timeline_restructure.py:451-469 (_layer_order, plan)
- shot_composition_projection.py:241-269 (_track_merge, render)

### Pipeline (render path)
1. Runtime holds a parent revision (`payload.config.clips`, `payload.config.tracks`, `payload.occurrences`), plus pinned shot revisions and internal timeline revisions.
2. managed_timeline.py:962-973 calls `project_runtime_parent_composition`.
3. Per occurrence (projection:538-648): `_track_merge` into parent tracks (:574); each internal clip is projected through `_project_clip` (:628-648) and appended to `config["clips"]` (:648). Parent clips are placed first (:499-504).
4. Output = one flat timeline (`config.clips`, `config.tracks`) with ids namespaced per occurrence. This is what the backend receives.
5. Backend selected by `selector` (default `rendering.remotion`): render/run.py:422, :614; core/rendering/service.py:202. The timeline is handed to the renderer as a flat timeline; there is no `clipType: shot` left in it (legacy expansion is not on this path).

### Note on the legacy path
expand_shots.py:258-264 keeps each sub-clip's own `track` (only fills it from the shot clip when `track` is None, :258-259), and tags `shot_id`/`shot_occurrence_id`. The shot clip's track is therefore never a layer.

## 2. Track ordering inside expansion (answer to Q2)

Runtime projection (`_track_merge`, shot_composition_projection.py:241-269):
- Shared track ids are NOT re-ordered: if `track_id in by_id` (:250) nothing happens. The parent order wins for every shared id. So a shot whose tracks all exist in the parent contributes NO order at all. Its inner order is ignored.
- Shot-only tracks are inserted next to their nearest preceding shared neighbour (:261-262), else before the nearest following shared neighbour (:266).
- A shot-only suffix (no following shared track) is appended at `len(tracks)` (:257-260). In a 2D render that is the BOTTOM-most visual track (2D paints index 0 last; see section 3), not the top. The comment says "after the film's complete track list, including unrelated film-only layers such as music" (:258-259).
- Tracks are not namespaced, so two occurrences of one shot with the same inner track id share the same track slot.

Occurrence track:
- The runtime occurrence has no track field. `_project_clip` never reads the occurrence track. Child clips keep their authored `track` (`_timeline_clip` requires it, :125-126). The occurrence affects `at`, window clipping, speed, gain, and a placement transform (`_apply_placement_transform`, :153-178, applied at :328).
- Legacy expand_shots: the occurrence (shot clip) track is used only when a child has no track (expand_shots.py:258-259). It never affects order.
- Answer: the occurrence track does not affect order in either path.

Placement transform note: `_apply_placement_transform` copies occurrence `transform.x/y/width/height/crop*/opacity` onto each child with `clip[key] = value` (shot_composition_projection.py:165-166). That REPLACES child values, it does not compose them. Each child gets it individually, not as a group.

## 3. Backends and layering rules

### 2D Remotion (default; 0.0.6)
- Installed package: remotion/node_modules/@banodoco/timeline-composition (package.json version 0.0.6). Remotion pins it in remotion/package.json (dependency is the v0.0.6 tarball URL).
- Source is NOT vendored in Astrid; it is the installed npm tarball at remotion/node_modules/@banodoco/timeline-composition/typescript/src/. (The App vendors 0.0.2, per CONTEXT.)
- Visual track order: TimelineComposition.tsx:266 `[...getVisualTracks(timeline)].reverse()`, then map at :313-316. Index 0 is painted LAST = top. (lib/tracks.ts:9-14 keeps config order.)
- Each track is an AbsoluteFill with its own `opacity` and `mixBlendMode` (TimelineComposition.tsx:230-239). Blend and opacity are per track, not per group.
- Clips within a track: `sortClipsByAt` (:30-32), rendered in that order (:215-228), transitions between adjacent clips (:219-224).
- `effect-layer` clips return null (:61-63). They are not drawn here.
- No `shot` handling anywhere in the composition (only a type field, types.ts:60). Shots are expected to be flat by then.
- Root registration: remotion/src/Root.tsx:2-8 (imports TimelineComposition). Lazy three.js review variant at :91-99.
- Default composition id: remotion/run.py:116 (`DEFAULT_COMPOSITION_ID = "TimelineComposition"`).

### three.js (`ThreeTimelineComposition`)
- Opposite convention in code (remotion/src/ThreeTimelineComposition.tsx):
  - Comment at :33-38 says "later track = on top", and says the 2D convention is the reverse.
  - Code at :385-387: `paintIndex = visualTracks.length - 1 - trackIndex`; `mesh.position.set(0, 0, -paintIndex)`; `mesh.renderOrder = trackIndex`. Index 0 gets the most negative z (farthest), and a higher index draws later. So later config track is on top, the opposite of 2D (TimelineComposition.tsx:266, which puts index 0 on top).
  - Only text planes are built from timeline clips in this function (`buildTextPlanes`, :335-391, skips non-text at :348-350).
- Backend (rendering.threejs): astrid/packs/rendering/rendering/renderers/threejs/run.py.
  - Clip types: `_SUPPORTED_CLIP_TYPES = {"text","media", live-scene}` (:95). Support reasons (:145-170) reject unknown types; audio is refused (:186).
  - Declared `clip_types: [text, media, haus.astrid.liveScene]`, `features.media_textures: false`, `effects: false`, `transitions: false` (threejs/renderer.yaml).
- When used: only when `selector == "rendering.threejs"`. In this checkout there is no automatic selection. Found only in the renderer's own files, the Remotion files, and a test (Runtime/tests reference `rendering.remotion` only). The render action's `--selector` help lists it (astrid/packs/rendering/actions/render/run.py:541-543). It is not the default.
- Git: ThreeTimelineComposition.tsx last changed 18 Oct (caa98c20b).

### FFmpeg (rendering.ffmpeg)
- Entry: astrid/packs/rendering/rendering/renderers/ffmpeg/command.py. Media groups (`_media_clip_groups` :68-95): visual `media` clips, split into "base" (no hold, sorted by `at`) and "overlays" (with hold, sorted by `at`). Tracks are used only for the kind filter, not z order.
- Single-track rule: astrid/packs/rendering/rendering/renderers/ffmpeg/support.py:511-514: `rendering.ffmpeg requires exactly one visual track carrying media clips`. With overlays, only ONE overlay is composited (command.py:299-300, `overlay_clips[0]`).
- Static overlay mode needs exactly two visual tracks, with the held image on the top track (support.py:483-499).
- Also: text overlays (rasterized PNG).
- When used: `selector == "rendering.ffmpeg"`. Default for video_editing orchestration (astrid/packs/video_editing/shared/runtime_orchestration.py:435). Not the default for `render`.
- Conclusion: it cannot render a multi-track film like this one.

### ffmpeg layer compositor (exists, not used by this film in this checkout)
- astrid/packs/rendering/rendering/finalizers/compositor/run.py:2-14: merges N z-layer segments bottom-to-top.
- Host side: astrid/core/rendering/service.py:1063-1104 materializes `LayerRef` slices (track allowlist + alpha stamp). Contract: astrid/core/rendering/contracts.py:1293-1340 (`LayerRef`: z, tracks, blend "normal" only, opacity). Plan validation at contracts.py:1495-1509.
- I found no planner in this checkout that emits `LayerRef`. Search: `LayerRef(` and `layer=` produce no producer under astrid/ outside contracts/service/compositor.

### Which backend renders this film (answer to Q3)
- Default selector is `rendering.remotion` (render/run.py:422, :614; service.py:202), which is the 2D TimelineComposition.
- I could not confirm the selector used for the film's actual renders. The scratchpad data (tl-23s) has no render record. The runtime or App side that picks the selector was not checked here.
- The three.js renderer rejects audio and only supports text/media in the composition (threejs/run.py:186, :167). The ffmpeg renderer would refuse this film (support.py:511-514).

## 4. Agent-facing tools (flat model)

- Checkout flattens chapter films into one working shot (sdk/timeline/checkout.py:39-41, :325-327). Agents edit the flat shot. Chapter rows are then the shots (timeline_restructure.py:477-478 docstring).
- `timelines show`: cli_show.py:206-214 `--clips` requires `--shot N`. `--shot` filters rows by shot id (cli_show.py:241; cli.py:1066). Cut table is one row list, not a tree.
- `onscreen.py` `_build` (:248-292) and `duration.py` `visual_tracks_paint_order` (:292-309) are both flat track-index ordering over config tracks/clips.
- Review captions: remotion/src/ReviewOverlay.tsx:5, :47-53 shows the shot whose `[at, at+hold)` window contains the time. Time-based, not layer-based.
- Adding a clip (`add`): sdk/timeline/edits.py:48-50 (signature). Shot chosen by time: `sid = self._shot_at(start)` (edits.py:69). `_shot_at` raises if outside every shot (lookup.py:415-421). The track must exist in that shot's OWN internal tracks, else the call fails (edits.py:73-74; `set_track` does the same, model.py:663-664). Clip `at` stored relative to shot start (model.py:735).
- Film-level (parent) clips exist in the SDK (`PARENT_SHOT = ""`, _common.py:85; `_parent_clips` lookup.py:363-366), but `add()` never writes to them. They are created by `split` for music or wall-crossing clips (timeline_restructure.py:419-421, :491).
- So today: an agent places a clip inside a shot by giving a time inside that shot, and the track must be in that shot's own list. A main-timeline clip is only created via restructure (or by editing parent clips directly, which I did not check).

## 5. "Shot = nested layer": would expanding into the occurrence slot be enough? (OPINION, labelled)

Opinion: for stacking order alone, yes. For true nesting, no.

Basis:
- Stacking order in 2D is one flat list of tracks, each its own AbsoluteFill (TimelineComposition.tsx:230-239, :266). If `_track_merge` (shot_composition_projection.py:241-269) inserted each occurrence's inner tracks as namespaced ids (e.g. `occ:type`, `occ:plate`) at the occurrence's track slot, the inner order would be kept exactly (the list is already in z order), and a loose main clip on a lower track would still draw under the whole shot. The current code cannot do this because shared ids are skipped (:250), so the shot's order is dropped whenever ids match. Namespacing also removes the id-collision case.
- Needed changes beyond expansion: the parent's track list must place the occurrence slot, track ids must be namespaced per occurrence, `_project_clip` (:331) already namespaces clip ids but not track ids, and all consumers (onscreen.py:248, visualize model.py:524, the editor projection) must read the same order.

Why it is not true nesting:
- Shot-level opacity, blend, transform, or an effect-layer (`effect-layer` returns null in 2D, TimelineComposition.tsx:61-63, so today such a layer cannot wrap anything) need a GROUP container. The 2D composition has only per-track opacity and blend (:230-239). Pushing a shot's opacity onto each namespaced track multiplies per track, which is not the same as a group opacity when tracks overlap.
- The per-clip transform overwrite (shot_composition_projection.py:165-166) would also need to become a group transform to keep one shot-level placement.
- Transitions across shot boundaries would need the group, not the flat list.

Suggested minimal shape (opinion): a group clip type rendered as one AbsoluteFill that holds its own track list, added to 2D only. Flat expansion covers the owner's stated rule (shot as one layer in main layering, inner order kept) without that group.

## Key evidence file list
- astrid/core/timeline/expand_shots.py:37-271
- astrid/core/timeline/shot_composition_projection.py:153-178, 241-269, 291-366, 454-675
- astrid/packs/rendering/actions/render/managed_timeline.py:962-973
- astrid/sdk/timeline_restructure.py:198-295, 377-494, 559-620
- astrid/sdk/timeline/checkout.py:39-41, 325-327; astrid/sdk/timeline/publish.py:97-99, 234-237
- astrid/sdk/timeline/edits.py:48-74; lookup.py:333-366, 415-421; model.py:663-664, 735
- astrid/core/timeline/onscreen.py:248-292; duration.py:292-309
- astrid/packs/rendering/rendering/renderers/ffmpeg/command.py:68-95, 296-300; support.py:483-514
- astrid/packs/rendering/rendering/renderers/threejs/run.py:95, 145-186
- astrid/packs/rendering/actions/render/run.py:422, 541-543, 614
- astrid/core/rendering/service.py:202, 1063-1104; contracts.py:1293-1340
- remotion/src/ThreeTimelineComposition.tsx:33-38, 335-391
- remotion/src/Root.tsx:2-8, 91-99; remotion/src/ReviewOverlay.tsx:5, 47-53
- remotion/node_modules/@banodoco/timeline-composition/typescript/src/TimelineComposition.tsx:30-32, 61-63, 215-239, 266, 313-316; lib/tracks.ts:9-14
