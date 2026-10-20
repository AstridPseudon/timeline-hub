#!/bin/bash
set -eu
cd /home/user/work/wt/vw-m3-pcm-native-window-resume-r1
exec env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_REMOTION_PROJECT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-native-window-resume-r1/audio-project PATH="/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short "$@"
