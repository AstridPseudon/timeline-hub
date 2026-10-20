# D09 explicit Scene Root-lifetime consumer

## Result

Added the private `scene_answers._prepared_host_frames_at(...)` adapter. It
accepts the caller's already-retained timeline/assets paths and invocation
paths, acquires the existing Remotion lock, enters the integrated
`_prepared_remotion_root` context with the exact requested frame sequence, and
calls the existing `host_frames_at` query while the prepared Root props,
  materialized assets, staged effects, and other invocation resources remain
  live. The canonical profile/basis comes from those prepared Root props.
  Frame-mode preserves the existing scene-query behavior and skips video PCM
  work. No renderer is launched, no capture is certified, and missing preparation is
reported as `SceneQueryUnavailable` rather than an empty/GAP answer.

The adapter is private and does not create a source factory, DTO, fallback
registry/theme, or second evaluator. Save/check/provider paths were not
changed. The current SDK `Checkout.check()` has no exact retained render-input
caller or Root-preparation arguments, so no SDK caller was invented; a caller
must supply that existing source seam before this private adapter can replace
the SDK's current diagnostic path. No deletion or physical parity claim is
made.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_scene_answers.py -k 'prepared_host_query or invalid_runtime_context'`
  — **3 passed, 29 deselected**.
- `/home/user/work/venv-agent/bin/ruff check astrid/core/timeline/scene_answers.py tests/packs/rendering/test_scene_answers.py`
  — **All checks passed**.
- `git diff --check` — **passed**.
- The requested scene-answer and host-neighbor run was attempted, but setup
  stopped before product tests: pinned Node `v20.19.4` is unavailable (only
  v22.22.0 is installed), and the worktree has no renderer peer graph. Result:
  **3 passed, 44 setup errors**; the errors are environment setup failures.
- No browser, renderer, socket, install, full suite, central test request, or
  shared dependency/cache write was run.

## Next step

Agent owner should connect the private adapter from a caller that already owns
the exact retained source/materialized paths and render extent. Until that
source contract exists, keep the SDK's current explicit diagnostic behavior
and save-core separation unchanged.
