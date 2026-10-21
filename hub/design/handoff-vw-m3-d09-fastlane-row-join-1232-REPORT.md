# D09 fast-lane source-row join

Branch: `tl/vw-m3-d09-fastlane-row-join-1232`  
Base: `tl/vw-m3-d09-label-existing-row-carry-1226` (`d9c863aa7`)

## Change

- Added an optional existing frame-provider join to `fast_lane._labelled_tiles`.
- For a supplied provider, the fast lane accepts only a frame in
  `fresh_scene_frames`, obtains the existing `CaptureSceneLabels` carrier via
  `scene_for_frame`, and formats its source/frame-bound `_frame_facts` through
  the existing `overlay_labels_frame(..., scene=..., source_identity=...)`
  path.
- Missing, stale, forged, or malformed carrier rows are advisory-unavailable
  for that display copy: the fast lane leaves it unlabelled and never falls
  back to PNG metadata or private visibility math.
- The existing no-carrier config-only positive remains unchanged for callers
  that do not have a scene callback. This preserves the original legacy
  overlay assertions; the source-backed path is the one that retires the
  private visibility query.
- Added focused fresh-row, forged-source, and stale-frame tests. No changes
  were made to the parent carrier files.

## Evidence

```text
PYTHONPATH=/home/user/work/wt/vw-m3-d09-fastlane-row-join-1232:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_fast_lane_words.py \
  tests/packs/rendering/test_labels_overlay.py \
  tests/packs/rendering/test_timeline_visualize_labels.py \
  tests/sdk/test_timeline_checkout.py
131 passed, 4 warnings in 29.35s

PYTHONPATH=/home/user/work/wt/vw-m3-d09-fastlane-row-join-1232:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m ruff check \
  astrid/packs/rendering/actions/timeline_visualize/fast_lane.py \
  tests/packs/rendering/test_fast_lane_words.py
All checks passed!

git diff --check
pass
```

The first test attempt without the Runtime worktree on `PYTHONPATH` failed at
collection because `runtime_protocol` is supplied by Runtime; it did not
modify the worktree. No full, native/browser, live-socket, install, or shared
dependency suite was run.

## Decision / limitation

The current `prepare_pair` implementation does not itself expose a frame
provider after the managed render; no new source authority, DTO, store, or
provider was invented. The fast lane consumes providers only when an existing
caller carries them in `pair["frame_providers"]`; otherwise its pre-existing
no-carrier positive path remains in force. Connecting the actual successful
fresh callback to `prepare_pair` requires an upstream caller seam outside this
worker's allowed files.

Changed files are limited to:

- `astrid/packs/rendering/actions/timeline_visualize/fast_lane.py`
- `tests/packs/rendering/test_fast_lane_words.py`
