# D09a caller map

## Public seam qualified by this worker

- `tests/packs/rendering/presenter_selected_cut_query.mjs` prepares one
  registered presenter Root and queries the exact retained frame keys
  `[0, 3, 4, 5]` through Composition's ordinary `querySceneFrame` API.
- Its aggregate obtains `state` and `motion` from the registered presenter
  `source.mouthStateAt`, `source.presenterAt`, `source.motionAt`, and
  `source.MOUTH_LEVEL`; it does not copy Python clock, hash, geometry, or
  codebook logic.
- The Python test compares those public semantic states with the existing
  ordinary visualize caller's `model.mouth_state`, while preserving the
  existing PNG crop, comparator, threshold, selection, missing-image, and
  denominator assertions.

## Actual private callers retained

- `astrid/packs/rendering/actions/timeline_visualize/motion/model.py:451`
  `mouth_state` is called by `_presenter_props` and by
  `layers/builtin.py:389` (`render_lipsync`).
- `motion/model.py:528` `mouth_box` is called by
  `layers/builtin.py:429` for the pixel crop and by the existing direct
  motion tests.
- `motion/model.py:438` `hash_unit`, `MOUTH_CYCLE`, and `GAP_HOLD_S` remain
  private implementation used by the retained ordinary caller.

## Why production migration is not qualified

- `RemotionFrameProvider.scene_for_frame()` exposes `CaptureSceneLabels` only
  for a complete successful fresh PNG batch. Cache hits carry bytes only;
  `filmstrip_cards.py:1686` therefore retains the legacy fallback.
- `LayerContext` receives frames/cut/config but not final Root props, the
  source identity, or a retained component-zero presenter row. The live
  `render_lipsync` caller cannot safely issue a public query in its current
  lifetime.
- Existing `test_live_source_label_native.py` proves the separate retained
  saved/candidate source -> exact final Root lifetime and public frame query;
  this worker does not pretend the retained four-still fixture is a Runtime
  source certificate.
