# vw-m3-d09-semantic-query-fix-review-1242

## Verdict

APPROVE — the source fix removes semantic-only frames from the PNG capture
request while retaining the prepared Root semantic query and existing guards.

## Scope

Reviewed source branch `tl/vw-m3-d09-semantic-query-only-fix-1242` at
`ef7f39af3`, based on `tl/vw-m3-d09-dense-state-carrier-1232` at
`e1bc96362`. The final patch changes only:

- `composed_frame.py`: separates `pixel_frames` from the ephemeral
  `scene_query_frames`; retention validates only produced pixel files while
  retaining all queried semantic rows.
- `root_preparation.py` and Remotion `run.py`: carry the private semantic
  frame set to the existing prepared Root callback without changing the
  renderer's image frame set.
- `test_scene_source_carry.py`: asserts the renderer receives `(0, 24)`, the
  callback observes `(0, 24, 29)`, and one retained source serves both rows.

The original sparse pixel/cache path remains intact. Semantic-only frames do
not enter PNG output or cache writes. `CaptureSceneLabels.observe` still
queries `host_frames_at` from the current prepared Root props with the exact
source, frame set, basis, and clip mapping. Existing one-mode handling,
wrong-source/basis refusal, and no-mint-on-cache-hit controls remain. No
public DTO/result field, new authority/store/source factory, type/pin, or
consumer patch was introduced.

## Tests

All commands ran against a private archive of `ef7f39af3`; no integration
worktree was modified.

- `PYTHONPATH=/tmp/semantic-query-review-2UwsWW:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py -k 'transport and (motion_scene_rows_join_exact_missing_frames_once or actual_source_join_queries_historical_scene_and_overlay)'` — **6 passed, 55 deselected**.
- `PYTHONPATH=/tmp/semantic-query-review-2UwsWW:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py -k 'wrong_canonical_basis_cannot_query or final_props_must_match_the_same_frozen_source_before_query'` — **5 passed, 56 deselected**.
- `PYTHONPATH=/tmp/semantic-query-review-2UwsWW:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_cache_payload.py -k 'new_provider_reuses_rows_without_query_or_private_visibility or default_provider_keeps_png_only_cache_reusable_across_owners or failed_batch_never_mints_cache_payload'` — **7 passed, 31 deselected**.
- `git diff --check tl/vw-m3-d09-dense-state-carrier-1232 tl/vw-m3-d09-semantic-query-only-fix-1242` — passed.

The source worker additionally reported its focused source-carry lane as
14 passed/47 deselected, motion lane as 1 passed/32 deselected, `py_compile`
passed, and no full/browser/native/physical/install/shared-dependency suite
was run. This review did not run a full suite.

## Decisions, blockers, next steps

No review decision or source change was needed. No blocker found. The
orchestrator can merge the source branch through the normal queue and run
broader qualification there.
