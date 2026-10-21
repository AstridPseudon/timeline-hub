# D09 presenter curve last-caller diagnosis

Result: **no product patch; the private fallback is live and must remain.**

The normal curve layer is `layers/builtin.py:278-289`, where
`render_curves()` calls `model.props_at()` for every non-audio, non-sequence
element. `model.props_at()` (`motion/model.py:627-636`) first calls
`own_motion()`, which is the admitted element-owned `motionAt` carrier. For
`am-presenter`, the component source is
`astrid_motion/rendering/elements/effects/am-presenter/motion.ts:132-141` and
its `motionAt()` returns the component-owned `mouth` scalar using the local
`MOUTH_LEVEL` codebook (`motion.ts:127-129`).

When Node/esbuild is unavailable, `ElementMaths.at()` returns `None` and records
the unavailability; `props_at()` then deliberately uses
`PROPS["am-presenter"]`, whose `_presenter_props()` at
`motion/model.py:600-603` calls `mouth_state()`. That fallback is reachable,
not dead code, and preserves the no-Node behavior. The existing named test
`test_without_node_the_mirror_answers_and_says_so` asserts this path.

Public13 also exposes the exact component-owned value through the existing
query carrier: `am-presenter/scene.ts:23-28` publishes `diagnostics.motion:
motionAt(...)`; `remotion/scene-query.mjs:9-36` returns the prepared scene
rows; and the existing Agent sheet handoff retains source-bound fresh/cache
rows at `motion/sheet.py:155-188`. This is an exact source/delegate, not a
Python clock/hash replacement. However, the current normal `render_curves()`
path does not consume those rows; its established fallback is the only path
available when the component motion evaluator cannot run. Replacing
`_presenter_props()` with a public query would therefore require a separate
public curve handoff and would remove the required no-Node fallback. No such
rewiring, geometry change, render-policy change, or public proof was performed.

The independent `render_lipsync()` fallback at `builtin.py:470-474` remains a
second live `mouth_state()` caller for unqualified/stale/missing public facts;
this task did not alter that pixel/statistical path.

## Evidence

Targeted non-integration controls:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short -m 'not integration' tests/packs/rendering/test_timeline_visualize_motion_views.py tests/packs/rendering/test_timeline_visualize_motion.py tests/packs/rendering/test_timeline_visualize_motion_discovery.py
39 passed, 2 skipped, 1 deselected in 10.18s
```

The same targeted files without excluding integration reached 39 passed, 2
skipped, 1 failed. The sole failure was the expected environment prerequisite:
`test_transform_at_adapter_preserves_clip_time_and_canvas_units` could not
find the pinned Node v20.19.4 and found only Node v22.22.0. No source failure
was inferred from that result.

`git diff --check` passed. Product tree is unchanged; no full, browser,
socket, normal render, physical, or public13 proof was run.
