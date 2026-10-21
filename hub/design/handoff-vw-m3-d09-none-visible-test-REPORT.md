# REPORT

## Result

The live compatibility projection is already present and needed no production
change: `CaptureSceneLabels.labels()` calls
`overlays.labels.labels_for_scene()`, which skips only `layer["visible"] is
False`. Unknown rows remain visible/unknown. This is consumed by the filmstrip
frame-address path and contact/label overlays.

Added a public13 direct-host regression in
`tests/packs/rendering/test_scene_host.py` with one registered absent element
and one unsupported custom control. The test checks both the raw diagnostic
rows and the adapter projection, plus the existing audio-only GAP behavior.

## Exact current live callers

- `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:112-116`:
  `CaptureSceneLabels.labels()` -> `labels_for_scene()`.
- `astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py:26-28`:
  frame-index `addresses` consumes `capture.labels()`.
- `astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py:54-60`:
  contact tiles route through `overlay_labels_frame(..., capture=...)`.
- `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py:107-114`:
  `overlay_labels_frame()` consumes `capture.labels()` for public Scene rows.

The private `onscreen.visible_at()` path remains separate and is not used by
this retained public Scene label projection.

## Evidence

Passed:

- Public13 host lane: `17 passed in 10.44s`.
- Adjacent capture/label lanes: `28 passed in 6.16s`.
- Ruff on touched file: `All checks passed!`.
- `git diff --check`: passed.

A combined Ruff invocation including untouched
`tests/packs/rendering/test_labels_overlay.py` reports its existing `I001`
import-order issue; that file was not changed. No full, browser, live-render,
physical, install, or shared-dependency run was performed.

## Decisions / limits

No adapter implementation was added because the existing adapter already has
the settled conservative behavior. No unknown custom element is filtered, and
raw diagnostics remain in the public Scene answer. The test uses a private
pytest extraction directory and read-only shared renderer dependencies.
