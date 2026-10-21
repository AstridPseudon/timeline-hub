# vw-m3-d09-dense-carrier-review-1236

## Verdict

REQUEST CHANGES — actual changed-hunk counterexample.

## Scope

Reviewed author branch `tl/vw-m3-d09-dense-state-carrier-1232` at
`e1bc96362`, against its `tl/integration` parent `c9ac7c7b0`. The reviewed
source changed only the existing `RemotionFrameProvider` capture path, the
filmstrip caller, the motion `public_scene` carrier, and its source-carry
regression. The separate `builtin.py`/aggregate consumer patch at
`handoff-vw-m3-d09-dense-state-carrier-1232.patch` remains unapplied and was
not treated as integrated product.

## Changed-hunk counterexample

In `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:924-943`,
the new `scene_frames` path unions semantic frames with card frames and passes
the union directly to `self.worker.capture(requested, ...)`. The existing
capture worker produces a PNG for every frame in that list. The new regression
asserts the worker request `(0, 24, 29)`; its fixture backend writes one image
for each requested frame, so frame 29 is an additional rendered PNG even
though it is semantic-only and not a card. The later copy/cache loops omit
that PNG from the output/cache, but they do not prevent the extra pixel render.

This violates the brief’s explicit requirement that dense semantic Scene rows
use the existing `host_frames_at` query within the retained Root lifetime
without extra pixel rendering. The source-query/refusal behavior is not enough
to approve this hunk while it couples semantic density to image capture.

## What checked out

- `CaptureSceneLabels.observe` still calls the existing `host_frames_at` once,
  and `retain` keeps exact source/frame/basis/address checks.
- `build_context` remains fail-closed for missing or stale/forged rows and
  keeps one evidence mode.
- No DTO, source factory, authority/store, new public field, package, or pin
  activation was introduced.

## Tests

All commands ran against a cleaned temporary archive of the author branch;
nothing was applied to `tl/integration`.

- `git diff --check tl/vw-m3-d09-dense-state-carrier-1232^ tl/vw-m3-d09-dense-state-carrier-1232` — passed.
- `PYTHONPATH="$review_tmp:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m py_compile astrid/packs/rendering/actions/timeline_visualize/composed_frame.py astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py astrid/packs/rendering/actions/timeline_visualize/motion/sheet.py tests/packs/rendering/test_scene_source_carry.py` — passed.
- `PYTHONPATH="$review_tmp:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py -k 'transport and (actual_source_join_queries_historical_scene_and_overlay or motion_scene_rows_join_exact_missing_frames_once or mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames or failed_capture_or_copy_exposes_no_scene_and_removes_partial_files or final_props_must_match_the_same_frozen_source_before_query or materialized_and_retained_sources_cannot_be_substituted)'` — 14 passed, 47 deselected.
- `PYTHONPATH="$review_tmp:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py -k 'transport and (actual_source_join_queries_historical_scene_and_overlay or canonical_basis_uses_whole_partial_canvas_and_rational_rate or motion_scene_rows_join_exact_missing_frames_once)'` — 7 passed, 54 deselected.
- `ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion PYTHONPATH="$review_tmp:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_presenter_selected_cut_aggregate.py -k 'public_mouth_facts or public_fact_failures or mixed_public_mouth_facts or actual_selected_cut_aggregate or selection_window_boundaries or strict_two_percent_boundary'` — 13 passed, 12 deselected.
- `PYTHONPATH="$review_tmp:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_timeline_visualize_motion_views.py -k 'motion_view_writes_two_pages_findings_and_timing'` — 1 passed, 32 deselected.
- A first accidental all-parameter source-carry run included native cases and hit 14 setup errors because the temporary archive had no native peer modules; it was not counted as evidence and was replaced by the required transport-only runs.

## Required next step

Split semantic Scene-row observation from pixel capture: keep the existing
card image request list passed to the renderer, and use an existing retained
host/root observation seam for semantic frames so no semantic-only PNGs are
rendered or cached. Re-run the focused positive/negative source-carry checks
and assert the renderer receives card frames only while the callback receives
the exact card-plus-semantic frame list.
