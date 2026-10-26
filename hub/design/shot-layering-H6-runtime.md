# H6-runtime: how the Runtime stores and interprets shots

Repo: ~/Developer/astrid-video/astrid-local/live-door/Runtime (read-only)
HEAD: fa9cd5464a8b37b02f971de375e56be846cd69e2 ("Use expected render storage and a one GiB reserve"), detached.
origin/main: fa9cd54 (after fetch, 0 behind / 0 ahead). Not behind.

## 1. Schema: shots, occurrences, child timelines

Two shot representations exist in the Runtime. Only the canonical one is live for render.

Canonical (live):
- Parent composition revision: runtime_protocol/canonical_schema.py:348 `parent_composition_revisions` (payload_json, content_digest).
  Occurrences are a separate table: canonical_schema.py:369 `composition_revision_occurrences`, with `track TEXT NOT NULL` (l.380),
  plus shot_id / shot_revision_id / placement / duration_ms / speed / transform / gain / muted / provenance.
- Shot = `project_shots` (canonical_schema.py:208), `shot_revisions` (l.338) with `internal_timeline_revision_id` (l.340) -> child timeline.
- Child timeline = `internal_timeline_revisions` (canonical_schema.py:329): payload is a full TimelineConfig (clips + tracks).
- Heads: `parent_composition_heads` (l.362), `shot_revision_heads` (l.354).
- Publication envelope: contract/schemas/shot-composition.json
  - required: project_id, timeline_id, expected_head, parent_composition (l.9-10)
  - ParentComposition = {config (TimelineConfig), registry, clips, occurrences[]} (l.~50-60)
  - Occurrence required: occurrence_id, shot_id, shot_revision_id, placement, duration_ms, track (l.55)
  - ShotRevisionInput carries internal_timeline_revision_id (l.74, 78); ShotPayload (l.118), "Immutable link to the child timeline revision")
  - InternalTimelineRevisionInput payload = TimelineConfig (pinned sha f52b8202...).
- TimelineConfig itself is owned by @banodoco/timeline-schema: contract/schemas/timeline-config.schema.json
  (tracks at l.13 with id/kind visual|audio/label/role; clips at l.7; TimelineClip has `track` l.154).
- contract/schemas/timeline.json and timeline-revision.json are the minimal product-neutral timeline: their Shot is only
  {shot_id, start_ms, duration_ms, reference_ids}. They do not carry layer or child-timeline data; they are not the composition model.

Legacy (retired at render):
- A `clipType: "shot"` clip on a parent track with params {shot_id, timeline_document_id} (managed_render_snapshot.py:28+,
  the `clipType != "shot"` branch and params check ~l.94-110). Render admission now rejects it: store.py ~1905-1915
  raises ConflictError "legacy clipType 'shot' render admission is retired" and points to publishParentComposition.

Representable as-is? Yes, for the data model. "Shot = sub-timeline at a track position" fits the existing shapes:
the occurrence already has a parent `track`, and its child is an immutable TimelineConfig with its own tracks and clips.
No schema change is needed to store it. What the schema does not express is how the child is composited. Nothing in the
TimelineConfig or the envelope says "this clip is a group that renders as one layer". Nesting would need a new
render-side construct, and any change to TimelineConfig (new clip type or group field) lands in @banodoco/timeline-schema,
which is pinned by sha in shot-composition.json and timeline-config.schema.json. That is a cross-repo bump.

Contract pins: contract/artifacts.json:12 (fixture digest) and :51-52 (schema digests). Changing a schema or fixture
requires a manifest update (sha256 pins).

## 2. Code that flattens or reasons about layer order

Flattening (the same flattening, two places):
- runtime_protocol/visual_seam.py normalize_closure (l.162-401):
  - l.169 parent `tracks` map; l.175 `picture_lanes` = continuity tracks, else the parent occurrence tracks.
  - l.313 `child_tracks = {**body.tracks, **parent tracks}`. Comment at l.312: "Flattening keeps the parent's definition when
    lane IDs collide." Parent wins on id collision.
  - l.343-346: each child clip is added with `track = c.get("track", o["track"])` (raw child track id, no occurrence
    namespace), `inherited_track=o["track"]`, and `track_definitions=child_tracks`.
  - l.337-341 (materialize): child tracks not already known are appended to render_config["tracks"], i.e. to the END of
    the parent track list, not next to the occurrence's parent track.
  - l.271-274: rendered clips are emitted flat into render_config["clips"].
  - l.326 occurrence span keeps `track: o["track"]` (parent lane), so seam checks treat the occurrence as a parent-lane entity.
- runtime_protocol/managed_render_snapshot.py expand_shot_clips (l.28-220): legacy flattener. l.196-197: a child with no
  track inherits the shot clip's track, otherwise keeps its own track id. Output is a flat clip list.
- runtime_protocol/timeline_inspection.py:504: inspection calls expand_shot_clips to cross-check legacy projection.
- runtime_protocol/timeline_inspection.py:652: `internal_tracks = {**parent_tracks, **child_tracks}` (child wins for inspection,
  parent wins for render; comment at l.649-651 says so explicitly).

Layer-order reasoning:
- There is no z-order / stacking concept in the Runtime. grep for z-order, layer order, reverse, draw order found nothing
  relevant to visual layering. Ordering of tracks is not read anywhere in the seam logic. Lanes are compared by id and time,
  not by index. Order only exists as the array order that goes to the renderer (store.py:1933-1935 hands render_config over).
- visual_seam.py:420-440 groups overlap/gap checks by (track, path[:4]) for children and (track, "parent") for occurrences.
  Children of different occurrences on the same track id are checked separately, so no cross-shot false overlap there.
  Parent occurrence lanes are checked against each other by track id, which is where shot-vs-loose-clip layering would be
  checked, and it is not modelled.
- docs/visual-seam-policy.md:21-22 says "parent-first track definitions as render materialization, for nested clips too."
  That is the explicit flattening rule.

Render admission (store.py ~1862-1945):
- l.1881 admit_closure(..., materialize=True) builds seam_metadata; l.1933-1934 uses render_config / render_registry as source.
- l.1918 `_project_output_timeline` (store.py:1718) projects `role: "source"` tracks away. It does not touch order.
- Legacy clipType "shot" in config.clips is refused (store.py ~1905-1915).

Composition revision restore: service.py:2580 restore_project_parent_composition_revision re-publishes the exact historical
payload as a new head. It verifies digest (l.2593-2598) and does not interpret tracks. service.py:3133 publish_parent_composition:
occurrence track is required (service.py:3046-3048: `track` must be a non-empty string). It checks presence only, not
existence in parent tracks. store.py:6098-6112 checks expected occurrence rows against stored values, including track.

shot_dependencies.py (155 lines): dependency/invalidation analysis. No track or order logic.
timeline_view.py:127-128: text view groups lanes by (occurrence, track), a display only.

## 3. Shared fixtures (App and Runtime)

- conformance/fixtures/visual-seam-cases-v1.json: App test src/tools/video-editor/data/visualSeamSharedCases.test.ts:58
  reads it via ASTRID_RUNTIME_CHECKOUT. Also portableVisualSeamIntent.test.ts.
  Runtime tests: tests/test_visual_seam_shared_cases.py, tests/test_visual_seam_admission.py.
  Shot/track content: only one occurrence case ("overlapping overlays inside an occurrence", occurrence on track "picture",
  children on "picture" and "overlay"). It asserts seam warnings, not layer order. Lanes like "plate" are declared as
  pictureTracks (case "declared custom picture track ...").
  Canonicalized in commit 6ce4f02 (Oct 24). Any change to seam rules must change both sides.
- conformance/fixtures/shot-composition-compatibility.json: authorities, composition_shapes, shot_payload_shapes,
  invalid_shot_payloads. This is the one that carries parent occurrences and shot payloads. Shapes include occurrence
  `track`. Needs a sync check if the envelope changes. Tests: tests/test_shot_composition_contract.py.
- conformance/fixtures/canonical-timeline-parity.json: canonical_occurrences (name, occurrence_id, start_ms, duration_ms),
  legacy_shells, parent_effects. Parity between canonical and legacy shells. No track order asserted.
- conformance/fixtures/asset-identity.json: asset identity cases only. No shots or tracks. Not affected by shot nesting.
- conformance/fixtures/visual-boundary-v1.json: boundary vectors. Not inspected in depth; check before any seam change.

## 4. Who renders

The Runtime does not render. It builds the snapshot and hands it to an executor. The renderer is behind the executor.
- The Runtime builds the composition: store.py:1881-1935 (canonical parent + closure -> render_config/registry).
  The legacy path at managed_render_snapshot.py:28 flattened shots in the Runtime too, but is refused now.
- Work is queued under capability "rendering.render": store.py:2308-2310, 2475-2478 (render toolchain digest).
- Execution: local_worker_composition.py:349-351 spawns `astrid.core.execution.generic_host run ... --executor-id astrid-pack-host`
  with the pack root. That is Astrid's pack host, a separate process. local_worker_composition.py:493-495 also spawns
  runtime_protocol.local_execution_supervisor.
- The renderer that consumes config.clips and tracks is Astrid's (remotion / TimelineComposition, per CONTEXT). The Runtime
  does not contain a renderer. Its only hook is the handed-off render_config. Its tracks/clips order is what the renderer sees.

Where the composition the renderer receives is built: store.py ~1935 `_project_output_timeline(source_config, ...)`, fed by
visual_seam.py:337-346 for canonical occurrences. So the flattened composition is built in the Runtime, in visual_seam.py
normalize_closure with materialize=True.

## Blast radius on the Runtime side of nested shot layers

Must change (flattening and ordering are both in these spots):
1. visual_seam.py:313 (child track merge), :337-341 (child tracks appended at END of parent tracks), :343-346 (raw child track ids
   as lane ids). A nested model needs a child group node at the occurrence's parent track position, and child lanes keyed
   by (occurrence, track), not a shared id.
2. visual_seam.py:420-440 seam grouping/overlap. Lanes become (occurrence, track) for children. Overlap across the parent
   occurrence lane stays as is.
3. store.py:1933 render_config projection. It must carry the nesting into the output the renderer gets. Either a group clip
   (needs a TimelineConfig change in @banodoco/timeline-schema) or a pre-composited child per occurrence (no schema change,
   but needs a child render step in the executor).
4. managed_render_snapshot.py (legacy flattener): only if the legacy path must keep working. It is refused at render, so it is
   mostly dead. Still reached from timeline_inspection.py:504.
5. timeline_inspection.py:652 track catalog precedence and :649 comment. Inspection and render disagree today (child wins vs parent
   wins). Nested layers would make them agree on "child inside its track".
6. docs/visual-seam-policy.md:21-22, the flattening rule, and contract/schemas shot-composition.json (no change required for storage).

Probably unchanged: publish/restore/checkout validation (service.py:3046, store.py:6098, service.py:2580). They only require a
track string and verify digests, so they accept a nested model as long as occurrence.track stays a parent track id.

Shared fixtures that must move with any seam or render change: visual-seam-cases-v1.json (App + Runtime),
shot-composition-compatibility.json (Runtime; check App vendor copy), plus contract/artifacts.json digests.
asset-identity.json and canonical-timeline-parity.json are not layer-sensitive.

Opinion (labelled): the lowest-blast option is to keep the schema and the occurrence `track` as they are, and make the Runtime
expand each occurrence into child clips on namespaced lanes inserted at the parent track's index in render_config.tracks.
That avoids a TimelineConfig change and keeps the executor unchanged. It still changes visual_seam.py and store.py render
projection, and the seam fixture set.
