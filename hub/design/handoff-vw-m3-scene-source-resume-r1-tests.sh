#!/bin/bash
set -euo pipefail
cd /home/user/work/wt/vw-m3-scene-source-resume-r1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PWD
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_scene_source_carry.py -k 'not native'
# 40 passed, 19 deselected in 5.41s. Native-host parameters deliberately not run.
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_composed_frame_capture.py tests/packs/rendering/test_remotion_capture_scene_props.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_capture_closure_source.py
# 108 passed, 9 xfailed in 116.96s. All nine xfails pre-exist in unchanged tests.
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_timeline_filmstrip_execution.py::test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source tests/packs/rendering/test_timeline_filmstrip_execution.py::test_bundle_publication_keeps_previous_complete_bundle_on_archive_failure tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_preserves_session_primary_through_all_capture_cleanup_layers tests/packs/rendering/test_timeline_filmstrip_execution.py::test_filmstrip_successful_capture_does_not_swallow_close_failure tests/packs/rendering/test_capture_scene_labels.py::test_stale_root_inputs_refuse_before_query tests/packs/rendering/test_capture_scene_labels.py::test_missing_or_guessed_projected_identity_refuses tests/packs/rendering/test_capture_scene_labels.py::test_only_actual_sorted_unique_capture_frames_are_accepted tests/packs/rendering/test_capture_scene_labels.py::test_cache_only_has_no_observation_to_retain
# 18 passed in 1.22s.
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_timeline_filmstrip_cards.py -k 'not test_pack_'
# 35 passed, 3 deselected in 1.65s. The three deselected tests render ffmpeg fixtures.
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_capture_scene_labels.py astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py
# All checks passed.
git diff --check
# Exit 0.
