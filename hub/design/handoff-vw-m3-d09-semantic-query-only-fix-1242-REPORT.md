# vw-m3-d09-semantic-query-only-fix-1242

## Result

Implemented on branch `tl/vw-m3-d09-semantic-query-only-fix-1242`, based on
`tl/vw-m3-d09-dense-state-carrier-1232`.

The capture path now keeps sparse pixel misses as the renderer request. A
private ephemeral scene-frame argument carries the pixel-plus-semantic frame
set to the existing prepared Root callback, where `host_frames_at` observes
all required semantic rows. Retention validates only the produced pixel
frames, while the retained in-memory scene source covers semantic-only rows.
Cache reads/writes and the public `requested_frames` result remain card/pixel
only; existing source, basis, wrong-source, and one-mode guards remain.

The compact regression proves one callback/capture, pixel request `(0, 24)`,
query rows `(0, 24, 29)`, and one retained scene source for both pixel and
semantic rows. No `builtin.py` or consumer patch was applied.

## Tests

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py -k 'transport and (actual_source_join_queries_historical_scene_and_overlay or motion_scene_rows_join_exact_missing_frames_once or mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames or failed_capture_or_copy_exposes_no_scene_and_removes_partial_files or final_props_must_match_the_same_frozen_source_before_query or materialized_and_retained_sources_cannot_be_substituted)'` — **14 passed, 47 deselected**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_timeline_visualize_motion_views.py -k 'motion_view_writes_two_pages_findings_and_timing'` — **1 passed, 32 deselected**.
- `python -m py_compile` on the three changed implementation modules and the focused source-carry test — **passed**.
- `git diff --check` — **passed**.

No full, browser, native, physical, install, or shared-dependency suite was run.

## Decisions / blockers

The named handoff report was found at
`scratchpad/orch/design/handoff-vw-m3-d09-dense-carrier-review-1236-REPORT.md`
rather than the brief's `scratchpad/luna/reports/` path; its settled
REQUEST CHANGES finding was followed. No blocking issue remains.

Recommended next step: review and merge this worker branch, then run the
manager's broader qualification outside this worker sandbox.
