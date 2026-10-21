# D09 fast-lane source-binding review

## Verdict

**APPROVE.** No actual changed-hunk counterexample found in the completed
author source.

## Scope reviewed

Reviewed commit `de7ab77f1` on
`tl/vw-m3-d09-fastlane-row-join-1232`, against Agent `tl/integration`,
limited to the new hunks in:

- `astrid/packs/rendering/actions/timeline_visualize/fast_lane.py`
- `tests/packs/rendering/test_fast_lane_words.py`

The fast-lane provider path requires a fresh frame membership row, obtains
the existing `_frame_facts` carrier, and routes it through the existing
source/frame/clip/basis validation and overlay formatter. Missing, stale,
forged, or unavailable rows leave that display copy unlabelled; the code does
not derive visibility from PNG/config data on that path. The legacy no-carrier
path and the original pixel/timing/crop behavior are unchanged in these hunks.
No DTO, source factory, authority/store, new public field, package, or pin
activation was added by the reviewed commit.

## Independent evidence

Ran against an exact temporary `git archive` of the author branch (not
applied to this review worktree):

```text
PYTHONPATH=<author-archive>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_fast_lane_words.py \
  -k 'labelled_tiles_use_fresh_source_bound_rows_and_reject_forged_rows or verify_says_what_each_side_shows_and_the_exact_pixels or verify_with_zoom_crops_both_sides_at_full_resolution'
3 passed, 6 deselected

PYTHONPATH=<author-archive>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m ruff check \
  astrid/packs/rendering/actions/timeline_visualize/fast_lane.py \
  tests/packs/rendering/test_fast_lane_words.py
All checks passed!

git diff --check tl/integration..tl/vw-m3-d09-fastlane-row-join-1232 -- \
  astrid/packs/rendering/actions/timeline_visualize/fast_lane.py \
  tests/packs/rendering/test_fast_lane_words.py
pass
```

The author additionally reported 131 focused tests passed with 4 warnings,
Ruff passed, and `git diff --check` passed. No full, native/browser,
live-socket, install, or physical suite was run.

## Limitation / next step

`verify()` forwards `pair["frame_providers"]`, but the current `prepare_pair`
does not populate that key. Therefore this review approves the source-only
consumer seam and its refusal behavior, not end-to-end production activation.
An upstream caller must pass the existing successful fresh callback provider
before the new source-bound path can be claimed as active.
