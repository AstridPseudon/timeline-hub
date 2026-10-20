#!/bin/bash
set -euo pipefail
cd /home/user/work/wt/vw-m3-scene-current-owner-unit
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PWD
export TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-current-owner-unit/tmp
mkdir -p "$TMPDIR"
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_scene_source_carry.py -k 'not native'
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_composed_frame_capture.py tests/packs/rendering/test_remotion_capture_scene_props.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_capture_closure_source.py
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_timeline_filmstrip_execution.py::test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source tests/packs/rendering/test_timeline_filmstrip_execution.py::test_bundle_publication_keeps_previous_complete_bundle_on_archive_failure tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_preserves_session_primary_through_all_capture_cleanup_layers tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_successful_capture_does_not_swallow_close_failure tests/packs/rendering/test_capture_scene_labels.py::test_stale_root_inputs_refuse_before_query tests/packs/rendering/test_capture_scene_labels.py::test_missing_or_guessed_projected_identity_refuses tests/packs/rendering/test_capture_scene_labels.py::test_only_actual_sorted_unique_capture_frames_are_accepted tests/packs/rendering/test_capture_scene_labels.py::test_cache_only_has_no_observation_to_retain
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_timeline_filmstrip_cards.py -k 'not test_pack_'
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_capture_scene_labels.py astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py
git diff --check
