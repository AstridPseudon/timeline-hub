#!/usr/bin/env bash
set -euo pipefail

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
OWN="$ORCH/workers/vw-m3-mouth697-physical-controller-prep"
if test -f "$ORCH/managers/viewing/QUIET.md"; then
  date -u +%FT%TZ > "$OWN/PAUSED_ACK"
  exit 75
fi
test -f "$OWN/REVIEW.md"
: "${ASTRID_CHECKOUT:?manager must select the clean ee71010a0 Agent source}"
: "${VIEWING_CROP_REVISION:?manager must select the reviewed full Agent SHA}"
: "${VIEWING_CROP_ARTIFACT:?manager must select immutable public12 77-file artifact}"
test "$(cat "$OWN/READY_GRANTED")" = "$VIEWING_CROP_REVISION"
exec flock -x /tmp/timeline-viewing-browser.lock \
  env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 VIEWING_CROP_CENTRAL=1 \
  VIEWING_BROWSER_FLOCK_HELD=1 \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/google/chrome/chrome \
  python3 "$ORCH/design/handoff-vw-m3-mouth697-physical-controller-prep-run-central.py"
