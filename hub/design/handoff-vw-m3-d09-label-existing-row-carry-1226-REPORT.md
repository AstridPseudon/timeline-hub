# D09 existing bound row carry — handoff

Branch: `tl/vw-m3-d09-label-existing-row-carry-1226`.

The existing `_frame_facts` carrier now includes its source identity. The label overlay validates the carried answer, basis, canvas, address map, frame, and source before formatting it through `labels_for_scene`; the filmstrip frame-address join uses this path for fresh and validated cache-backed rows. Cache validation and MISS/fresh-callback behavior are unchanged.

The focused regression uses a validated cache-shaped `CaptureSceneLabels` carrier, proves ordering/opacity/geometry without the private visibility evaluator, and rejects stale frame and forged source facts. Existing overlay/cache/source-carry assertions remain green.

Evidence: 96 focused tests passed, 19 native cases deselected; Ruff and `git diff --check` passed. Native/browser/full/live-socket/install suites were not run per the worker brief. The no-carrier direct/legacy fallback remains because its existing positive assertions have no source-row carrier; the smallest missing joins are `_filmstrip_cache.py:20-22`, `fast_lane.py:742`, and `layers/builtin.py:604` (occupied by another worker).

