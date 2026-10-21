# vw-m3-d09-selected-mouth-production-prerequisite-0605

## Result

Completed the missing production caller hunk for the already-qualified
source-bound selected-mouth adapter. `render_lipsync` now skips the private
`model.mouth_box` lookup only when `_public_mouth_facts` has accepted the exact
selected frame series. It consumes the existing public ROI and retains the
private crop fallback for default, partial, raw-invalid, mixed, missing, stale,
or forged facts.

The existing path is now complete end to end:

`final Root callback -> CaptureSceneLabels -> motion.sheet.build_context ->
layers.builtin.render_lipsync`.

The existing compiled-ID/address map and exact four-frame aggregate remain the
source of the public rows. No new carrier, evaluator, authority, DTO, cache,
geometry, threshold, denominator, retry, or package change was made. The
private `mouth_state`/`mouth_box` fallbacks remain live.

## Changes

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`: use
  `box = None if public else model.mouth_box(presenter, 0)` before the existing
  public crop/fallback selection.
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py`: the
  normalized selected positive now fails if the private crop helper is called,
  while preserving the exact `3 of 3` aggregate assertion.

## Tests

All commands were run from this worktree with the read-only Runtime checkout
on `PYTHONPATH`; no shared dependency was written.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts='' -p no:cacheprovider tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_scene_capability.py` — **40 passed in 12.59s**.
- Same environment, `tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_scene_cache_payload.py` — **97 passed in 15.97s**.
- `python -m py_compile` on the two changed Python files — passed.
- `python -m ruff check --no-cache` on the two changed Python files — passed.
- `node --check tests/packs/rendering/presenter_selected_cut_query.mjs` — passed.
- `git diff --check` — passed.

The first pytest attempt without `/home/user/work/runtime` on `PYTHONPATH`
failed during collection with `ModuleNotFoundError: runtime_protocol`; it was
an environment setup issue, corrected without changing the source or shared
Runtime checkout.

## Decisions and limits

- Applied the previously reviewed one-line caller fix (`b153dd2f8`) because it
  was not an ancestor of the current Agent integration; no duplicate adapter
  or aggregate was added.
- Default/partial/raw-invalid inputs remain unqualified by design. Their
  existing private state/crop behavior and no-crop default behavior remain.
- No full suite, browser/localhost/live-socket run, physical replay, public14
  adoption, private fallback deletion, package change, or pin change was run or
  claimed.

Live caller changed: `builtin.render_lipsync` only. No other caller changed.
