# Legacy fade class/content summary

## What changed

- Updated the exact legacy node `tests/core/timeline/test_onscreen_more.py::test_a_one_sided_fade_is_a_dip_during_the_ramp_then_covered` to assert a test-only adjacent class/content projection: `[0, 15)` DIP, `[15, 60)` COVERED.
- Kept the detailed public spans assertion explicit: `[0, 1)` retains empty visible membership, `[1, 15)` retains `only`, and both retain findings; `[15, 60)` remains `only`/CONTENT.
- Added `test_class_content_projection_does_not_cross_a_hole`, proving the projection does not merge non-adjacent intervals.
- Did not change `astrid/sdk/timeline/check.py`, `scene_answers.spans_from_frames`, any public API/query protocol, authored data, incoming-crossfade coverage, or the independent fades golden.

## Evidence

From the assigned worktree, using the read-only shared native8 dependency graph and pinned Node executable:

```sh
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/core/timeline/test_onscreen_more.py::test_a_one_sided_fade_is_a_dip_during_the_ramp_then_covered \
tests/core/timeline/test_onscreen_more.py::test_class_content_projection_does_not_cross_a_hole \
tests/packs/rendering/test_host_scene.py::test_spans_from_frames_does_not_fill_unqueried_frames \
tests/packs/rendering/test_host_scene.py::test_spans_from_frames_merges_only_matching_adjacent_answers \
tests/sdk/test_timeline_checkout.py::test_default_check_reports_scene_unavailable_without_renderer_imports
```

Result: **5 passed in 4.08s**.

```sh
/home/user/work/venv-agent/bin/ruff check --isolated tests/core/timeline/test_onscreen_more.py
git diff --check
```

Result: Ruff passed; diff check passed.

## Decisions and limits

The approved summary-consumer projection is test-only and merges only when the prior interval ends at the next interval's start and class/content match. Detailed membership and findings remain part of the unchanged `Span` assertions/API. No product source or SDK consumer change was required. No full, browser, socket, install, or independent-fades golden run was performed.

## Next step

Record the replacement proof in the viewing deletion ledger when this worker is integrated; retain the separate independent-fades requirement until its approved renderer/equivalence work lands.
