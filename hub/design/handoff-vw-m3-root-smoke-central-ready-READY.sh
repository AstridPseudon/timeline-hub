#!/usr/bin/env bash
set -euo pipefail
orch=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
own=$orch/workers/vw-m3-root-smoke-central-ready
if test -e "$orch/QUIET.md" || test -e "$orch/managers/viewing/QUIET.md"; then
    date -u +%FT%TZ > "$own/PAUSED_ACK"
    echo 'QUIET active; controller paused before CPU/browser work.' >&2
    exit 75
fi
exec 9>/tmp/timeline-viewing-browser.lock
flock -x 9
exec /home/user/work/venv-agent/bin/python \
    "$orch/design/handoff-vw-m3-root-smoke-central-ready-controller.py" run
