## Result

Separated semantic public presenter motion from the deferred private pixel ROI path.

- `render_lipsync` now admits the existing exact source/clip/frame-bound `diagnostics.motion.mouth` rows with the existing `allow_default_motion=True` policy.
- Explicit-null and raw-invalid `params.mouth` values still fail that public qualification and use private fallback.
- Pixel checking always uses the existing private `model.mouth_box(presenter, 0)` conversion and unchanged strict `> 2%` comparison/statistics. The public crop adapter was removed.
- Updated the one direct consumer test with a private `mouth_state` tripwire and a private-crop call assertion. Existing aggregate, denominator, strict-boundary, stale, and forged controls remain unchanged.
- No new public field/type/release/pin was added; D09a remains pending until the live `mouth_state` duplication can be retired.

## Tests

- `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --tb=short tests/packs/rendering/test_presenter_selected_cut_aggregate.py` — **28 passed**.
- `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --tb=short tests/packs/rendering/test_timeline_visualize_motion_views.py tests/packs/rendering/test_presenter_crop_equivalence.py` — **9 passed, 33 deselected**.
- `git diff --check` — passed.
- An initial aggregate invocation without the shared Runtime/Composition environment failed during setup before collection; no source failure. It was rerun with the existing read-only shared paths above and passed.
- No full, browser, physical, install, or central suite was run.

## Review / next step

The patch is intentionally limited to `builtin.py` and its direct aggregate test. An independent changed-hunk review is still required before merge.

