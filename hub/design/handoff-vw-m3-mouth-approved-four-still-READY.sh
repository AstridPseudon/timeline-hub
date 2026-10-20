#!/usr/bin/env bash
# READY, not executed by the worker. Manager grants a specific committed SHA.
# Set ASTRID_CHECKOUT and VIEWING_CROP_REVISION; write that SHA to READY_GRANTED.
set -euo pipefail
own=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-approved-four-still
orch=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
if test -f "$own/REVIEW.md"; then cat "$own/REVIEW.md"; fi
if test -f "$orch/managers/viewing/QUIET.md"; then
    date -u +%FT%TZ > "$own/PAUSED_ACK"
    exit 75
fi
: "${ASTRID_CHECKOUT:?select the approved committed Agent worktree}"
: "${VIEWING_CROP_REVISION:?select its full approved SHA}"
test "$(cat "$own/READY_GRANTED")" = "$VIEWING_CROP_REVISION"
exec flock -x /tmp/timeline-viewing-browser.lock \
    env VIEWING_BROWSER_FLOCK_HELD=1 PYTHONDONTWRITEBYTECODE=1 \
    /home/user/work/venv-agent/bin/python "$own/run-central.py"
