# D09 caller map

## Migrated

- `filmstrip_cards.build_filmstrip_pack` passes the existing
  `RemotionFrameProvider` into `motion.sheet.build_context` for motion views.
- `motion.sheet.build_context` collects only `_frame_facts` from
  `scene_for_frame`; the map is private `LayerContext.shared["public_scene"]`.
- `layers.builtin.render_lipsync` validates source identity, exact frame rows,
  declared basis/FPS, projected address ownership, public component state, and
  one component-zero compatibility mouth row before using its ROI.

## Retained fallback

- Cache-only and mixed frames have no retained public facts and continue using
  `motion.model.mouth_box` for pixel statistics.
- Unsupported, stale, malformed, or incomplete public rows fail closed to the
  same private path; no blanket refusal or uncertified public crop is emitted.
- Existing public label overlays and `CaptureSceneLabels.frame/labels` remain
  unchanged apart from the private fact adapter.

## Not touched

SDK, checks, save/core-provider paths, `_timing_evaluators`, public DTO/model
surfaces, private mouth helpers, comparator/thresholds, and source admission.

