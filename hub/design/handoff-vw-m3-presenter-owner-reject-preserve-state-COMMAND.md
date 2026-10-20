cd /home/user/work/wt/vw-m3-presenter-owner-reject-preserve-state

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
--basetemp=/tmp/vw-m3-presenter-owner-reject-focused3
# 17 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/astrid_motion/test_astrid_motion_pack.py \
tests/packs/rendering/test_remotion_element_generation.py \
tests/packs/rendering/test_timeline_visualize_motion_views.py \
--basetemp=/tmp/vw-m3-presenter-owner-reject-neighbors
# 38 passed, 2 skipped

/opt/node22/bin/node --check tests/packs/rendering/presenter_scene_capability.mjs
/opt/node22/bin/node --check tests/packs/rendering/presenter_crop_geometry.mjs
# both passed

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py
# All checks passed

git diff --check
# passed

