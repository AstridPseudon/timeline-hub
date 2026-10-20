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
STATE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix
export XDG_CACHE_HOME="$STATE/cache" XDG_CONFIG_HOME="$STATE/config"
export PWTEST_CACHE_DIR="$STATE/playwright-transform"
export NODE_PATH=''
mkdir -p "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$PWTEST_CACHE_DIR"
TASK_TMPDIR=''
TASK_TMPDIR_ID=''

cleanup_task_tmpdir() {
  local path=$1
  [[ -n "$path" ]] || return 0
  [[ -e "$path" ]] || return 0
  if [[ -L "$path" || ! -d "$path" || "$(dirname -- "$path")" != /tmp \
    || "$(basename -- "$path")" != timeline-tab-audio-* \
    || "$(realpath -- "$path")" != "$path" \
    || "$(stat -c '%d:%i' -- "$path")" != "$TASK_TMPDIR_ID" ]]; then
    echo "refusing to remove non-owned Chrome task temp: $path" >&2
    return 1
  fi
  rm -rf -- "$path"
}

unset TAB_AUDIO_TASK_TMPDIR
TASK_TMPDIR=$(mktemp -d /tmp/timeline-tab-audio-XXXXXX)
TASK_TMPDIR_ID=$(stat -c '%d:%i' -- "$TASK_TMPDIR")
export TAB_AUDIO_TASK_TMPDIR="$TASK_TMPDIR" TMPDIR="$TASK_TMPDIR" TMP="$TASK_TMPDIR" TEMP="$TASK_TMPDIR"

cleanup() {
  status=$?
  if [[ ${TAB_AUDIO_PREFLIGHT_DONE:-0} == 1 ]]; then
    postflight_status=0
    "$NODE" "$CONTROLLER" --postflight || postflight_status=$?
    if [[ $status == 0 && $postflight_status != 0 ]]; then
      status=$postflight_status
    fi
  fi
  task_temp_status=0
  cleanup_task_tmpdir "$TASK_TMPDIR" || task_temp_status=$?
  if [[ $status == 0 && $task_temp_status != 0 ]]; then
    status=$task_temp_status
  fi
  exit "$status"
}
trap cleanup EXIT

LOCK_PATH=${TAB_AUDIO_LOCK_PATH:-/tmp/timeline-viewing-browser.lock}
export TAB_AUDIO_LOCK_PATH="$LOCK_PATH"
export TAB_AUDIO_LOCK_FD=9

exec 9>"$LOCK_PATH"
flock -n 9 || { echo 'central browser flock is already held' >&2; exit 75; }
export VIEWING_BROWSER_FLOCK_HELD=1

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
