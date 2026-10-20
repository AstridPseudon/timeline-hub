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

[[ -d "$STATE" && ! -L "$STATE" && "$(realpath -- "$STATE")" == "$STATE" ]] \
  || { echo 'PRIVATE_PULSE_STATE_ROOT must be an existing real per-run directory' >&2; exit 2; }

RUN_AS_USER="${TAB_AUDIO_RUN_AS_USER:-}"
if [[ "$(id -u)" == 0 ]]; then
  : "${RUN_AS_USER:?root launcher requires an area-lead-admitted existing non-root identity in TAB_AUDIO_RUN_AS_USER}"
  command -v runuser >/dev/null || { echo 'runuser is required for the root-to-user-mode handoff' >&2; exit 2; }
  RUN_UID=$(id -u -- "$RUN_AS_USER")
  RUN_GID=$(id -g -- "$RUN_AS_USER")
  [[ "$RUN_UID" != 0 ]] || { echo 'TAB_AUDIO_RUN_AS_USER must resolve to a non-root identity' >&2; exit 2; }
else
  RUN_UID=$(id -u)
  RUN_GID=$(id -g)
  if [[ -n "$RUN_AS_USER" && "$(id -u -- "$RUN_AS_USER")" != "$RUN_UID" ]]; then
    echo 'TAB_AUDIO_RUN_AS_USER must name the invoking non-root identity' >&2
    exit 2
  fi
  RUN_AS_USER=$(id -un)
fi

TASK_TMPDIR=$(mktemp -d /tmp/timeline-private-pulse-capture-XXXXXX)
chmod 700 "$TASK_TMPDIR"
if [[ "$(id -u)" == 0 ]]; then
  chown "$RUN_UID:$RUN_GID" "$TASK_TMPDIR"
fi
for child_dir in home cache config playwright-transform playwright-output xdg-runtime; do
  if [[ "$(id -u)" == 0 ]]; then
    install -d -o "$RUN_UID" -g "$RUN_GID" -m 700 "$TASK_TMPDIR/$child_dir"
  else
    install -d -m 700 "$TASK_TMPDIR/$child_dir"
  fi
done
CHILD_OUTPUT_DIR="$TASK_TMPDIR/playwright-output"
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

assert_child_access() {
  if [[ "$(id -u)" == 0 ]]; then
    runuser --user "$RUN_AS_USER" -- test -r "$ROOT/node_modules/playwright/cli.js" \
      && runuser --user "$RUN_AS_USER" -- test -r "$ROOT/tests/e2e/timeline/private-pulse-stereo.probe.ts"
  else
    [[ -r "$ROOT/node_modules/playwright/cli.js" && -r "$ROOT/tests/e2e/timeline/private-pulse-stereo.probe.ts" ]]
  fi
}
assert_child_access || { echo 'Admitted identity cannot read the exact frozen graph/source' >&2; exit 2; }

run_probe_as_user() {
  local -a command=(env
    "HOME=$TASK_TMPDIR/home"
    "TMPDIR=$TASK_TMPDIR" "TMP=$TASK_TMPDIR" "TEMP=$TASK_TMPDIR"
    "XDG_RUNTIME_DIR=$TASK_TMPDIR/xdg-runtime"
    "XDG_CACHE_HOME=$TASK_TMPDIR/cache" "XDG_CONFIG_HOME=$TASK_TMPDIR/config"
    "PWTEST_CACHE_DIR=$TASK_TMPDIR/playwright-transform"
    "PLAYWRIGHT_OUTPUT_DIR=$CHILD_OUTPUT_DIR"
    "TAB_AUDIO_RUN_MODE=stereo" NODE_PATH=''
    PATH="$(dirname "$NODE"):/usr/bin:/bin"
    PLAYWRIGHT_TIMELINE_DEVICES=1
    "$NODE" "$ROOT/node_modules/playwright/cli.js" test
    --config "$CONFIG" --project=private-pulse-stereo-chrome155 --workers=1)
  if [[ "$(id -u)" == 0 ]]; then
    runuser --user "$RUN_AS_USER" -- "${command[@]}"
  else
    "${command[@]}"
  fi
}

probe_status=0
run_probe_as_user || probe_status=$?
mkdir -p "$PLAYWRIGHT_OUTPUT_DIR"
cp -a "$CHILD_OUTPUT_DIR/." "$PLAYWRIGHT_OUTPUT_DIR/"
exit "$probe_status"
