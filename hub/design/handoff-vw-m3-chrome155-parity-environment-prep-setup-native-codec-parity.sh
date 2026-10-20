#!/usr/bin/env bash
set -euo pipefail
orch=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
own="$orch/workers/vw-m3-chrome155-parity-environment-prep"
node=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

if test -f "$own/REVIEW.md"; then cat "$own/REVIEW.md"; fi
if test -f "$orch/managers/viewing/QUIET.md"; then
    cat "$orch/managers/viewing/QUIET.md"
    date -u +%FT%TZ > "$own/PAUSED_ACK"
    echo 'Manager QUIET marker is active; no render.' >&2
    exit 75
fi
test -f "$own/READY_GRANTED__vw-m3-chrome155-native-parity"
test -n "${VIEWING_BROWSER_FLOCK_HELD:-}"
# A self-conflicting second open proves that the outer central flock owns the lock.
if flock -n /tmp/timeline-viewing-browser.lock true; then
    echo 'Central browser flock is not held; no render.' >&2
    exit 1
fi
test "${VIEWING_SOURCE_IDENTITY:-}" = leased-b70-9f9-installed8-diagnostic
export ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source
test "$(cat "$orch/workers/vw-m3-runtime-source-lease2/exit")" = 0
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2
export TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition
( set -o noclobber; date -u +%FT%TZ > "$own/RUN_STARTED__vw-m3-chrome155-native-parity" )
output=$(mktemp -d /tmp/viewing-native-codec-parity-XXXXXX)
printf '%s\n' "$output" > "$own/playwright-output-path"
# Keep this exec foreground: central test-run removes its source snapshot only after
# this controller completes Playwright AND finally/postflight. No background launch.
# Reuse the qualified live-host parent and readonly Remotion runtime. No installs.
exec env -i HOME=/root LANG=C.UTF-8 \
    PATH="$(dirname "$node"):/home/user/work/venv-agent/bin:/usr/bin:/bin" \
    VIEWING_BROWSER_FLOCK_HELD="$VIEWING_BROWSER_FLOCK_HELD" \
    ASTRID_CHECKOUT="$ASTRID_CHECKOUT" \
    ASTRID_RUNTIME_CHECKOUT="$ASTRID_RUNTIME_CHECKOUT" \
    TIMELINE_COMPOSITION_CHECKOUT="$TIMELINE_COMPOSITION_CHECKOUT" \
    ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
    ASTRID_PACK_HOST_PYTHON=/home/user/work/venv-agent/bin/python \
    ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
    ASTRID_NODE_EXECUTABLE="$node" \
    ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion \
    ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
    ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
    PLAYWRIGHT_OUTPUT_DIR="$output" \
    "$node" --import tsx "$own/run-native-codec-parity.mjs"
