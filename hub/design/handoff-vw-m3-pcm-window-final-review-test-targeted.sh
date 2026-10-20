#!/bin/bash
set -eu
TASK_WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-window-final-review
cd "$TASK_WORKER/candidate"
exec env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK_WORKER/candidate" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_REMOTION_PROJECT_DIR="$TASK_WORKER/audio-project" PATH="/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short "$@"
