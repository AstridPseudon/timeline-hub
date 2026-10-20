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

[[ "$(id -u)" == 0 ]] || { echo 'private Pulse capture requires the original root launcher UID' >&2; exit 2; }
command -v runuser >/dev/null || { echo 'runuser is required for the private Pulse daemon' >&2; exit 2; }
command -v setsid >/dev/null || { echo 'setsid is required for the private Pulse daemon process group' >&2; exit 2; }
PULSE_USER_RECORD=$(getent passwd 65534 || true)
IFS=: read -r PULSE_USER _ PULSE_UID PULSE_GID _ _ _ <<< "$PULSE_USER_RECORD"
[[ "$PULSE_USER" == nobody && "$PULSE_UID" == 65534 && "$PULSE_GID" == 65534 ]] \
  || { echo 'existing nobody UID/GID 65534 is required for private Pulse' >&2; exit 2; }
PULSE_USER=$(getent passwd 65534 | cut -d: -f1)
[[ "$(id -u -- "$PULSE_USER")" == 65534 && "$(id -g -- "$PULSE_USER")" == 65534 ]] \
  || { echo 'getent nobody identity did not resolve to UID/GID 65534' >&2; exit 2; }

TASK_TMPDIR=$(mktemp -d /tmp/timeline-private-pulse-capture-XXXXXX)
chmod 700 "$TASK_TMPDIR"
for child_dir in home cache config playwright-transform playwright-output xdg-runtime; do
  install -d -m 700 "$TASK_TMPDIR/$child_dir"
done
CHILD_OUTPUT_DIR="$TASK_TMPDIR/playwright-output"
export TMPDIR="$TASK_TMPDIR" TMP="$TASK_TMPDIR" TEMP="$TASK_TMPDIR"

# These are separate direct /tmp allocations because the root-owned task
# directory is intentionally 0700: nobody must not need to traverse it. Only
# these newly-created daemon directories are handed to the existing nobody
# account; source, graph, grants, controller, Node, Chrome, and ffmpeg remain
# in the original root process.
PULSE_RUNTIME_DIR=$(mktemp -d /tmp/timeline-private-pulse-runtime-XXXXXX)
PULSE_HOME_DIR=$(mktemp -d /tmp/timeline-private-pulse-home-XXXXXX)
PULSE_COOKIE_DIR=$(mktemp -d /tmp/timeline-private-pulse-cookie-XXXXXX)
chmod 700 "$PULSE_RUNTIME_DIR" "$PULSE_HOME_DIR" "$PULSE_COOKIE_DIR"
PULSE_COOKIE="$PULSE_COOKIE_DIR/cookie"
PULSE_SOCKET="$PULSE_RUNTIME_DIR/native"
PULSE_DAEMON_LOG="$TASK_TMPDIR/pulse-daemon.log"
PULSE_DAEMON_PID=''

assert_owned_private_dir() {
  local path="$1"
  [[ -d "$path" && ! -L "$path" && "$(realpath -- "$path")" == "$path" \
    && "$(stat -c '%u %a' -- "$path")" == "$(id -u) 700" ]] \
    || { echo "private Pulse path is not a fresh root-owned 0700 directory: $path" >&2; exit 2; }
}
for pulse_path in "$PULSE_RUNTIME_DIR" "$PULSE_HOME_DIR" "$PULSE_COOKIE_DIR"; do
  assert_owned_private_dir "$pulse_path"
done
[[ "$(stat -c '%u %a' -- "$TASK_TMPDIR")" == "$(id -u) 700" ]] \
  || { echo 'private Pulse task temp is not a fresh root-owned 0700 directory' >&2; exit 2; }
chown "$PULSE_UID:$PULSE_GID" "$PULSE_RUNTIME_DIR" "$PULSE_HOME_DIR" "$PULSE_COOKIE_DIR"

start_private_pulse() {
  setsid runuser --user "$PULSE_USER" -- env -i \
    "HOME=$PULSE_HOME_DIR" \
    PATH=/usr/bin:/bin \
    "XDG_RUNTIME_DIR=$PULSE_RUNTIME_DIR" \
    "XDG_CONFIG_HOME=$PULSE_HOME_DIR/config" \
    "PULSE_RUNTIME_PATH=$PULSE_RUNTIME_DIR" \
    "PULSE_STATE_PATH=$PULSE_HOME_DIR/state" \
    "PULSE_COOKIE=$PULSE_COOKIE" \
    pulseaudio -n --daemonize=no --use-pid-file=no --exit-idle-time=-1 --log-target=stderr \
      "--load=module-native-protocol-unix socket=$PULSE_SOCKET auth-cookie=$PULSE_COOKIE auth-cookie-enabled=1" \
      '--load=module-null-sink sink_name=player rate=48000 channels=2 format=float32le channel_map=front-left,front-right' \
    >"$PULSE_DAEMON_LOG" 2>&1 &
  PULSE_DAEMON_PID=$!
}

stop_private_pulse() {
  [[ -n "$PULSE_DAEMON_PID" ]] || return 0
  kill -TERM -- "-$PULSE_DAEMON_PID" 2>/dev/null || kill -TERM "$PULSE_DAEMON_PID" 2>/dev/null || true
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    kill -0 -- "-$PULSE_DAEMON_PID" 2>/dev/null || break
    sleep 0.1
  done
  if kill -0 -- "-$PULSE_DAEMON_PID" 2>/dev/null; then
    kill -KILL -- "-$PULSE_DAEMON_PID" 2>/dev/null || kill -KILL "$PULSE_DAEMON_PID" 2>/dev/null || true
  fi
  wait "$PULSE_DAEMON_PID" 2>/dev/null || true
  PULSE_DAEMON_PID=''
}

remove_private_pulse_dir() {
  local path="$1"
  case "$path" in
    /tmp/timeline-private-pulse-runtime-*|/tmp/timeline-private-pulse-home-*|/tmp/timeline-private-pulse-cookie-*) ;;
    *) echo "refusing to remove unexpected private Pulse path: $path" >&2; return 1 ;;
  esac
  [[ -d "$path" && ! -L "$path" && "$(realpath -- "$path")" == "$path" ]] \
    || { echo "refusing to remove non-owned private Pulse path: $path" >&2; return 1; }
  rm -rf -- "$path"
}

cleanup() {
  local status=$? postflight=0
  stop_private_pulse
  if [[ ${TAB_AUDIO_PREFLIGHT_DONE:-0} == 1 ]]; then
    "$NODE" "$BASE_CONTROLLER" --postflight || postflight=$?
  fi
  for pulse_path in "$PULSE_RUNTIME_DIR" "$PULSE_HOME_DIR" "$PULSE_COOKIE_DIR"; do
    remove_private_pulse_dir "$pulse_path" || postflight=1
  done
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

[[ -r "$ROOT/node_modules/playwright/cli.js" && -r "$ROOT/tests/e2e/timeline/private-pulse-stereo.probe.ts" ]] \
  || { echo 'Original launcher UID cannot read the exact frozen graph/source' >&2; exit 2; }

start_private_pulse

run_probe() {
  local -a command=(env
    -u PULSE_SERVER -u PULSE_COOKIE -u PULSE_SINK -u PULSE_SOURCE
    -u PULSE_RUNTIME_PATH -u PULSE_STATE_PATH -u PULSE_CLIENTCONFIG -u PULSE_CONFIG -u PULSE_LATENCY_MSEC
    "HOME=$TASK_TMPDIR/home"
    "TMPDIR=$TASK_TMPDIR" "TMP=$TASK_TMPDIR" "TEMP=$TASK_TMPDIR"
    "XDG_RUNTIME_DIR=$TASK_TMPDIR/xdg-runtime"
    "XDG_CACHE_HOME=$TASK_TMPDIR/cache" "XDG_CONFIG_HOME=$TASK_TMPDIR/config"
    "PWTEST_CACHE_DIR=$TASK_TMPDIR/playwright-transform"
    "PLAYWRIGHT_OUTPUT_DIR=$CHILD_OUTPUT_DIR"
    "PULSE_SERVER=unix:$PULSE_SOCKET" "PULSE_COOKIE=$PULSE_COOKIE" "PULSE_SINK=player"
    "TAB_AUDIO_RUN_MODE=stereo" NODE_PATH=''
    PATH="$(dirname "$NODE"):/usr/bin:/bin"
    PLAYWRIGHT_TIMELINE_DEVICES=1
    "$NODE" "$ROOT/node_modules/playwright/cli.js" test
    --config "$CONFIG" --project=private-pulse-stereo-chrome155 --workers=1)
  "${command[@]}"
}

probe_status=0
run_probe || probe_status=$?
mkdir -p "$PLAYWRIGHT_OUTPUT_DIR"
cp -a "$CHILD_OUTPUT_DIR/." "$PLAYWRIGHT_OUTPUT_DIR/"
exit "$probe_status"
