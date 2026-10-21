# vw-m3-d09a complete semantic frame map review

## Verdict

**APPROVE the 1304 correction; no private `mouth_state` retirement.**

The exact completed source is Git commit `6741dda8629e1401f383a9371ca299d2c4f0c647`
(`fix(rendering): consume complete public semantic clock`), parent
`e83aa8253`. Its two-file diff is the requested minimal scope:

- `builtin.py`: separates the sparse PNG `pixel_series` from the complete
  admitted `public_scene` semantic clock, guards sparse-frame lookup, and
  keeps pixel crop/statistics on the original sparse series.
- The selected-cut test adds the registered sparse-card/dense-semantic
  regression.

The supplied flatpatch is malformed at line 57 (the second hunk has an
incomplete `@@` header), so I validated the exact Git commit rather than
repairing review input. The commit tree is the authoritative source.

## Semantic-map review

The new semantic series is taken from the existing `public_scene` result,
not from PNG-card keys. Admission remains source/clip/basis-bound through the
unchanged `_public_mouth_facts` checks: fresh/cache evidence mode, complete
frame coverage, basis dimensions and fps, answer frame/dimensions, source
addresses, expected presenter clip address, unique presenter layer,
content-frame-zero/ROI rules where applicable, and the existing
`closed|half|open` codebook.

`sheet.build_context` publishes `public_scene` only from the existing
fresh/cache provider result when the requested set is complete and uses one
evidence mode. Mixed, missing, stale, forged, invalid, or unavailable public
facts still clear/refuse the public map and use the established private
fallback. No new advisory result, UNKNOWN rule, source, provider, field,
timing math, or public API was added. Known source rows are not silently
omitted or blanket-converted to UNKNOWN.

The original behavior remains intact:

- public semantic rows replace the old positive one-to-one when admitted;
- absent admitted rows/refused public batches use `model.mouth_state`;
- qualified public ROI uses the existing public crop;
- unqualified ROI uses the existing `model.mouth_box` fallback;
- PNG crop/statistics retain the sparse selected frames, strict `> 0.02`
  threshold, and original pair denominator.

## Private-helper retirement

Retirement is **not safe or authorized**. The 1304 diff does not modify
`motion/model.py`. Production still contains:

- `builtin.py:502`: `render_lipsync` falls back to
  `model.mouth_state` for frames without admitted public state;
- `model.py:603`: `_presenter_props` calls `mouth_state` when
  `props_at` has no public override, preserving the independent
  `render_curves`/ordinary presenter path.

This fails the required zero-normal-callers condition. The named active
assertions are present and passing: public lipsync positive, dense semantic
positive, public curve positive, default public curve positive, missing-row
fallback, mixed/partial/default/invalid/stale/forged refusal controls, the
selected-cut aggregate, strict threshold, and the retained private codebook
test. They prove the public replacement and fallback boundary; they do not
justify deleting the helper.

## Evidence

Exact targeted run against the committed 1304 tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TREE:/home/user/work/runtime" \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
tests/packs/rendering/test_timeline_visualize_motion_views.py --tb=short
```

Result: **62 passed in 17.18s**.

Focused regression/positive/refusal run: **14 passed in 5.90s**, including
`test_sparse_pixels_use_dense_public_semantic_clock`, public fresh/cache
lipsync, public/default curve, missing/mixed/partial/invalid/stale/forged
fallbacks, selected-cut aggregate, and strict 2% boundary.

Additional static evidence:

- `git diff --check 6741dda86^ 6741dda86`: passed.
- `model.py`, `sheet.py`, and `composed_frame.py` are unchanged by 1304.
- No full suite, browser/native/live-socket run, install, or shared-dependency
  write was performed.

## Recommended next step

Merge the bounded 1304 correction if the orchestrator accepts the review.
Keep `mouth_state` until every normal fallback caller has a named equivalent
source-bound public assertion and is removed in a separate, explicitly
qualified change.

