# vw-m3-d09a-complete-state-map-fix-1304

## Result

Implemented the smallest fix for review1256's real dense semantic consumer
failure. `render_lipsync` now separates the sparse pixel-card clock from the
complete source-bound semantic clock carried by the approved query-only
producer. Public semantic validation uses all admitted `public_scene` rows;
pixel crop/statistics continue to use only the sparse `ctx.frames` rows.

The state lookup is guarded for incomplete public maps, preserving the existing
private fallback for missing, mixed, stale, forged, invalid, or unavailable
public evidence. The private fallback is not called in the new complete dense
positive regression. `model.mouth_state` is intentionally retained because the
existing refusal/fallback controls and `render_curves` normal caller still rely
on it; no retirement claim is made for that helper.

## Exact ledger

| File | Change | Evidence |
| --- | --- | --- |
| `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py` | Split `pixel_series` from `semantic_series`; consume complete `public_scene`; preserve guarded fallback and sparse pixel statistic | 62 direct tests; dense test tripwires private state |
| `tests/packs/rendering/test_presenter_selected_cut_aggregate.py` | Added registered Scene dense rows `0..29` with sparse pixel cards `(0,24,29)`; generalized test-only provider/path setup | New regression passes; base-1250 run had `KeyError: 1` |
| `astrid/.../motion/model.py` | Unchanged; private helper remains only where refusal/fallback behavior still requires it | `git diff` clean for model |
| Approved producer files | Unchanged | byte/equality check clean |

## Evidence

Targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
tests/packs/rendering/test_timeline_visualize_motion_views.py --tb=short
```

Result: **62 passed in 16.93s**.

`git diff --check`, changed-file `py_compile`, and producer equality checks all
passed. No full/browser/socket/install/shared-dependency suite was run.

## Decision / limits

The requested live public positive is preserved and now works with sparse pixel
cards plus dense semantic rows. Geometry/raw-mouth compatibility and pixel ROI
remain deferred as directed. Private state deletion is not safe in this unit:
the existing missing/invalid/public-unavailable paths still have normal callers
and retained positive fallback assertions. No new advisory-unavailable shape,
public API, field, store, source factory, package, or timing math was added.
