#!/usr/bin/env bash
set -Eeuo pipefail

# Central-only entry point. Without TAB_AUDIO_RUN=1 this performs no browser,
# daemon, socket, or capture work and only asks the two controllers for their
# offline readiness records.
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
export TAB_AUDIO_APP_ROOT="$ROOT"
NODE=${TAB_AUDIO_NODE_EXECUTABLE:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node}
BASE_CONTROLLER="$ROOT/tests/e2e/timeline/tab-audio-capture.controller.mjs"
PRIVATE_CONTROLLER="$ROOT/tests/e2e/timeline/private-pulse-stereo.controller.mjs"
CONFIG="$ROOT/tests/e2e/timeline/private-pulse-stereo.config.ts"
: "${PRIVATE_PULSE_STATE_ROOT:?owned per-run state root required}"
STATE="$PRIVATE_PULSE_STATE_ROOT"

[[ -x "$NODE" ]] || { echo "Missing admitted Node: $NODE" >&2; exit 2; }
[[ "$("$NODE" --version)" == v20.19.4 ]] || { echo 'Admitted Node must be v20.19.4' >&2; exit 2; }
export TAB_AUDIO_RUN_MODE=stereo PATH="$(dirname "$NODE"):$PATH" NODE_PATH=''
export XDG_CACHE_HOME="$STATE/cache" XDG_CONFIG_HOME="$STATE/config" PWTEST_CACHE_DIR="$STATE/playwright-transform"
mkdir -p "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$PWTEST_CACHE_DIR"

if [[ ${TAB_AUDIO_RUN:-0} != 1 ]]; then
  TAB_AUDIO_RUN=0 "$NODE" "$PRIVATE_CONTROLLER" --prepare
  echo 'Offline preflight only; no private daemon, browser, socket, network, or capture was started.'
  exit 0
fi

: "${TAB_AUDIO_PREFLIGHT_PATH:?fresh preflight path required}"
: "${TAB_AUDIO_RUN_MARKER:?fresh one-shot marker required}"
: "${TAB_AUDIO_GRANT_PATH:?fresh exact-source grant required}"
: "${PLAYWRIGHT_OUTPUT_DIR:?fresh output directory required}"
: "${TAB_AUDIO_LOCK_PATH:?shared browser lock required}"

TASK_TMPDIR=$(mktemp -d /tmp/timeline-private-pulse-capture-XXXXXX)
chmod 700 "$TASK_TMPDIR"
export TMPDIR="$TASK_TMPDIR" TMP="$TASK_TMPDIR" TEMP="$TASK_TMPDIR"
cleanup() {
  local status=$? postflight=0
  if [[ ${TAB_AUDIO_PREFLIGHT_DONE:-0} == 1 ]]; then
    "$NODE" "$BASE_CONTROLLER" --postflight || postflight=$?
  fi
  if [[ -n "${TASK_TMPDIR:-}" ]]; then
    [[ "$TASK_TMPDIR" == /tmp/timeline-private-pulse-capture-* && -d "$TASK_TMPDIR" && "$(realpath -- "$TASK_TMPDIR")" == "$TASK_TMPDIR" ]] || {
      echo "refusing to remove non-owned task temp: $TASK_TMPDIR" >&2
      postflight=1
    }
    if [[ $postflight == 0 ]]; then rm -rf -- "$TASK_TMPDIR"; fi
  fi
  if [[ $status == 0 && $postflight != 0 ]]; then status=$postflight; fi
  exit "$status"
}
trap cleanup EXIT

exec 9>"$TAB_AUDIO_LOCK_PATH"
flock -n 9 || { echo 'shared browser flock is already held' >&2; exit 75; }
export VIEWING_BROWSER_FLOCK_HELD=1 TAB_AUDIO_LOCK_FD=9

TAB_AUDIO_RUN=0 "$NODE" "$PRIVATE_CONTROLLER" --prepare
"$NODE" "$BASE_CONTROLLER" --preflight
export TAB_AUDIO_PREFLIGHT_DONE=1
"$NODE" "$BASE_CONTROLLER" --claim
PLAYWRIGHT_TIMELINE_DEVICES=1 "$NODE" "$ROOT/node_modules/playwright/cli.js" test \
  --config "$CONFIG" --project=private-pulse-stereo-chrome155 --workers=1
