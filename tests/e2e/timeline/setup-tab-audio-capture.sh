#!/usr/bin/env bash
set -Eeuo pipefail

# Manager-only future entry point. It is deliberately inert unless the final
# SHA grant and an explicit run request are supplied. The primary backend is
# getDisplayMedia tab capture; private PulseAudio is a fallback only.
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
CONTROLLER="$ROOT/tests/e2e/timeline/tab-audio-capture.controller.mjs"
LOCK_PATH=${TAB_AUDIO_LOCK_PATH:-/tmp/timeline-viewing-browser.lock}
export TAB_AUDIO_LOCK_PATH="$LOCK_PATH"
: "${TAB_AUDIO_PREFLIGHT_PATH:?manager must supply a unique preflight path}"
: "${TAB_AUDIO_RUN_MARKER:?manager must supply a unique one-shot marker path}"

exec 9>"$LOCK_PATH"
flock -n 9 || { echo 'central browser flock is already held' >&2; exit 75; }
export VIEWING_BROWSER_FLOCK_HELD=1

cleanup() {
  status=$?
  if [[ ${TAB_AUDIO_PREFLIGHT_DONE:-0} == 1 ]]; then
    postflight_status=0
    node "$CONTROLLER" --postflight || postflight_status=$?
    if [[ $status == 0 && $postflight_status != 0 ]]; then
      status=$postflight_status
    fi
  fi
  exit "$status"
}
trap cleanup EXIT

node "$CONTROLLER" --preflight
export TAB_AUDIO_PREFLIGHT_DONE=1

if [[ ${TAB_AUDIO_RUN:-0} != 1 ]]; then
  echo 'READY only: set TAB_AUDIO_RUN=1 after manager final-SHA grant review.'
  exit 0
fi

node "$CONTROLLER" --claim
PLAYWRIGHT_TIMELINE_DEVICES=1 \
  npm exec -- playwright test --config "$ROOT/tests/e2e/timeline/tab-audio-capture.config.ts" \
  --project=native-codec-chrome155-tab-audio
