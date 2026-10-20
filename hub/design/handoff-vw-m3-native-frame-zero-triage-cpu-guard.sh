#!/bin/sh
set -eu
orch=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
for marker in "$orch/QUIET.md" "$orch/managers/viewing/QUIET.md"; do
  if test -f "$marker"; then
    date -u +%FT%TZ > "$orch/workers/vw-m3-native-frame-zero-triage/QUIET_ACK"
    cat "$marker"
    exit 75
  fi
done
exec "$@"
