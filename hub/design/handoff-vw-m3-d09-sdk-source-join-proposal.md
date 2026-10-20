# D09 source join: exact owner seam, no invented API

Base Agent d8749a9ce. Production source migration is blocked; no changes to check.py,
onscreen.py, scene_answers.py, renderer, publish.py or transaction.py are proposed as
an executable patch. The test-only prerequisite patch is separate.

The executable prototype is /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-sdk-source-join-prototype.py.
It starts with real open_authoring_bundle -> Checkout edit -> actual check/resolve ->
preview_authoring_candidate(checkout.document()) -> prepare_filmstrip(authoring_preview)
-> Timeline.dump -> actual run._execute_remotion_locked final staging callback ->
run._canonical_profile -> scene_answers.host_frames_at. Runtime document/admission and
renderer toolchain/port selection are doubled. A callback exception stops before any
render. It does not manufacture Root props, registry or source maps. Its 24 frames are
COVERED/EMPTY at 200x100/24; the existing map joins the opaque compiled ID to c08.field,
source_clip_id opaque:source:field and occurrence_id opaque:occ:A.

The next unchanged explicit Checkout.check() fails at check.py:106 when private
onscreen.coverage is forbidden, even though its exact candidate has a positive public
answer. There is no current check argument or retained prepared Root carrier through
which those rows can reach _on_screen/_sprite_problems. Supplying a monkeypatched span
would only repeat the formatter tests and is deliberately not called a source join.

Requested owner handoff, in this order:

1. Agent owns the invocation separation: check.py:534/569 calls the viewer, but
   publish.py:37 and transaction.py:147/169 call the SAME check(). Choose and implement
   the explicit-check boundary and its existing callers before private coverage is
   removed. Saving must never evaluate the scene or launch Node. Keep existing
   structural validity and existing diagnostic positives; do not make a new flag up
   inside the Viewing worker. The supplied save guards are the ready prerequisite.
2. Rendering owner owns reusing the final-Root preparation lifetime currently inside
   run.py::_execute_remotion_locked, from AssetMaterializer/resolved_registry and
   _resolved_theme_for_render through _stage_effect_assets_for_timeline and final
   on_scene_props. Its existing callback is inside render execution, after toolchain
   validation/registry regeneration/port selection; it is not a scene-only preparation
   entry. Extract/reuse this existing preparation with the exact frozen candidate and
   compiled map/profile, rather than call render and deliberately throw as production
   control flow. Reuse the existing projector, profile and source validation; no source
   factory, DTO, new field, source store, certificate or colon-ID parsing. This requires
   the owner's renderer grant; current worker may not edit that path.
3. Preserve CaptureSceneLabels' successful-fresh-PNG semantics. It cannot be used as
   storage for explicit check rows: frame() is unavailable until retain() receives a
   complete successful fresh capture. Do not synthesize PNGs to make checks work.
4. Package owner still needs existing crop/outer entrance-exit geometry answers before
   claiming the complete old positive set. c35/bdd's direct tests pass, but public12
   reports unknown-animation-geometry for these wrappers. AM component support alone
   cannot override that package decision. This is additional existing missing proof,
   not permission to downgrade a positive to UNKNOWN or refusal.

Once those owner boundaries exist, rerun the unchanged red positive through the actual
explicit check. Then migrate _on_screen and sprite bounds using the existing compiled
source/occurrence map, retaining addressed OFFCANVAS/run-in/MIXED-SCALE/DAMAGED-ART,
EMPTY/deliberate hold/CONTENT/GAP/DIP and unavailable advisory behavior. Until then keep
all current private callers and their tests. No reflow, labels/cache, mouth, timing,
pixel, save or public-package contract edits in this worker. No physical parity or
production admission/current API claim is made.
