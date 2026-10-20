#!/usr/bin/env bash
set -Eeuo pipefail

# Manager-only future entry point. It is deliberately inert unless the final
# SHA grant and an explicit run request are supplied. The primary backend is
# getDisplayMedia tab capture; private PulseAudio is a fallback only.
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
CONTROLLER="$ROOT/tests/e2e/timeline/tab-audio-capture.controller.mjs"
NODE=${TAB_AUDIO_NODE_EXECUTABLE:-/tmp/vw-m3-agent-gate-node20.19.4/bin/node}
[[ -x "$NODE" ]] || { echo "Pinned Node executable is missing: $NODE" >&2; exit 2; }
[[ "$("$NODE" --version)" == v20.19.4 ]] || { echo "Pinned Node must be v20.19.4" >&2; exit 2; }
export PATH="$(dirname "$NODE"):$PATH"
LOCK_PATH=${TAB_AUDIO_LOCK_PATH:-/tmp/timeline-viewing-browser.lock}
export TAB_AUDIO_LOCK_PATH="$LOCK_PATH"
export TAB_AUDIO_LOCK_FD=9

exec 9>"$LOCK_PATH"
flock -n 9 || { echo 'central browser flock is already held' >&2; exit 75; }
export VIEWING_BROWSER_FLOCK_HELD=1

cleanup() {
  status=$?
  if [[ ${TAB_AUDIO_PREFLIGHT_DONE:-0} == 1 ]]; then
    postflight_status=0
    "$NODE" "$CONTROLLER" --postflight || postflight_status=$?
    if [[ $status == 0 && $postflight_status != 0 ]]; then
      status=$postflight_status
    fi
  fi
  exit "$status"
}
trap cleanup EXIT

if [[ ${TAB_AUDIO_RUN:-0} != 1 ]]; then
  "$NODE" "$CONTROLLER" --prepare
  echo 'Offline preflight only. Manager must review this exact fingerprint before a fresh grant.'
  exit 0
fi

: "${TAB_AUDIO_PREFLIGHT_PATH:?manager must supply a unique preflight path}"
: "${TAB_AUDIO_RUN_MARKER:?manager must supply a unique one-shot marker path}"
: "${TAB_AUDIO_GRANT_PATH:?manager must supply a new exact-source grant}"
: "${PLAYWRIGHT_OUTPUT_DIR:?manager must supply a new output directory}"
"$NODE" "$CONTROLLER" --preflight
export TAB_AUDIO_PREFLIGHT_DONE=1

"$NODE" "$CONTROLLER" --claim
PLAYWRIGHT_TIMELINE_DEVICES=1 \
  "$NODE" "$ROOT/node_modules/playwright/cli.js" test --config "$ROOT/tests/e2e/timeline/tab-audio-capture.config.ts" \
  --project=native-codec-chrome155-tab-audio
