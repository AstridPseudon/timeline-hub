#!/bin/bash
set -euo pipefail
cd /home/user/work/wt/vw-m3-scene-carry-public12-proof
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=
export PYTHONPATH=$PWD
export ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
export ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
export ASTRID_TEST_COMPOSITION_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-carry-public12-proof/pytest-source tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_capture_scene_labels.py
