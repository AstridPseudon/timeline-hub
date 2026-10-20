#!/bin/bash
set -euo pipefail
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-carry-final-review/candidate
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PWD
export ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
export ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-carry-final-review/pytest-source tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_capture_scene_labels.py
# Exit 0: 79 passed in 16.97s. Includes every native-host parameter, pinned public10.
unset ASTRID_NODE_EXECUTABLE ASTRID_TEST_NODE_MODULES
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-carry-final-review/pytest-neighbors tests/packs/rendering/test_composed_frame_capture.py tests/packs/rendering/test_remotion_capture_scene_props.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py tests/sdk/test_timeline_filmstrip.py tests/packs/rendering/test_timeline_filmstrip_cards.py -k 'not test_pack_'
# Exit 0: 125 passed, 3 deselected in 5.92s. The three pack cases generate rendering fixtures.
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-carry-final-review/pytest-executor tests/packs/rendering/test_timeline_filmstrip_execution.py::test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source tests/packs/rendering/test_timeline_filmstrip_execution.py::test_bundle_publication_keeps_previous_complete_bundle_on_archive_failure tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_preserves_session_primary_through_all_capture_cleanup_layers tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_successful_capture_does_not_swallow_close_failure
# Exit 0: 7 passed in 1.13s.
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_capture_scene_labels.py astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py
# Exit 0: All checks passed.
git -C /home/user/work/wt/vw-m3-scene-carry-final-review diff --check 56409ab287007ed44eede6fd634096421c824951 28d4e515da6c8c8c9180c7cd0076eec0f510989c
# Exit 0.
