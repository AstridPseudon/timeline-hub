## Done

Implemented the narrow D09 Scene-only caller join:

- Root-backed public Scene queries with exact source/clip/frame validation.
- Managed `filmstrip_bundle.zip` consumption via `scene-answers.json`.
- Existing managed receipt provenance bound to capture identity and timeline.
- Missing/stale results remain advisory `UNAVAILABLE`.
- Added focused executor and SDK tests.

Tests:

- `PYTHONPATH="$PWD" python -m pytest -q tests/packs/rendering/test_scene_only_executor.py tests/sdk/test_scene_caller_preservation.py tests/packs/rendering/test_scene_answers.py` — **43 passed**
- `ASTRID_TEST_NODE_MODULES=/home/user/work/app/node_modules PYTHONPATH="$PWD" python -m pytest -q tests/packs/rendering/test_capture_scene_labels.py tests/packs/rendering/test_scene_host.py` — **35 passed**
- `git diff --check` — passed
- No full suite run.

Commit message written to the requested path; empty `DONE` marker created.