#!/usr/bin/env bash
set -Eeuo pipefail

# F/D141i: one Agent-core-full measurement command. This packet publishes the
# corrected recipe and dry controls only; it does not invoke this command.
readonly EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-command-return-0238/evidence
readonly RUN_ROOT=$EVIDENCE_ROOT/private/measurement-runs/agent-core-full
readonly LAUNCHER_EVIDENCE=$RUN_ROOT/launcher-evidence
readonly MANIFEST=$EVIDENCE_ROOT/positive.manifest
readonly AGENT_CHECKOUT=/home/user/work/wt/agt-pin-28e56cac
readonly RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-6a011d58
readonly APP_CHECKOUT=/home/user/work/wt/app-pin-867cb273
readonly COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-635f4de0
readonly PYTHON=/home/user/work/venv-agent/bin/python
readonly NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
readonly PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
readonly SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
readonly DISK_USAGE_ROOT=/home/user
readonly SOURCE_ADMISSION_BYTES=4700000000
readonly CONTINUOUS_STOP_BYTES=4000000000
readonly REQUEST_ID=agent-core-full

readonly STATUS_FILE=$RUN_ROOT/status.txt
readonly CALLER_ARGV_FILE=$RUN_ROOT/callerargv.txt
readonly SERVICE_FILE=$RUN_ROOT/service.txt
readonly INTERPRETER_FILE=$RUN_ROOT/interpreter.txt
readonly SOURCE_BEFORE_FILE=$RUN_ROOT/source-before.txt
readonly SOURCE_AFTER_FILE=$RUN_ROOT/source-after.txt
readonly SOURCE_AFTER_ERRORS=$RUN_ROOT/source-after-errors.txt
readonly DISK_TRACE_FILE=$RUN_ROOT/disk-trace.txt
readonly RAW_STDOUT=$RUN_ROOT/raw-stdout.log
readonly RAW_STDERR=$RUN_ROOT/raw-stderr.log
readonly RUNNER_LOG=$RUN_ROOT/runner.log
readonly JUNIT_XML=$RUN_ROOT/agent-core-full.xml
readonly RUNNER_EXIT_FILE=$RUN_ROOT/runner-exit.txt
readonly MONITOR_EXIT_FILE=$RUN_ROOT/monitor-exit.txt

body_pid=
monitor_pid=
body_started=0
body_rc=not-started
monitor_rc=not-started
before_rc=0
before_attempted=0
output_owned=0
evidence_rc=0

die() {
  local message=$1 exit_code=${2:-78}
  [[ "$exit_code" =~ ^[1-9][0-9]*$ ]] || exit_code=78
  printf 'REFUSED: %s\n' "$message" >&2
  exit "$exit_code"
}

guard_repo() {
  local label=$1 path=$2 expected_sha=$3 expected_tree=$4
  local actual_sha=UNREADABLE actual_tree=UNREADABLE state=UNREADABLE path_state=non-exact rc=0
  if [ "$(realpath "$path" 2>/dev/null || :)" = "$path" ] && [ -d "$path" ]; then
    path_state=exact
  else
    rc=78
  fi
  actual_sha=$(git -C "$path" rev-parse HEAD 2>/dev/null) || { actual_sha=UNREADABLE; rc=78; }
  actual_tree=$(git -C "$path" rev-parse 'HEAD^{tree}' 2>/dev/null) || { actual_tree=UNREADABLE; rc=78; }
  state=$(git -C "$path" status --porcelain --untracked-files=all 2>/dev/null) || {
    state=UNREADABLE
    rc=78
  }
  if [ "$state" = '' ]; then state=clean; else state=dirty; fi
  printf '%s\tsha=%s\ttree=%s\tstatus=%s\tpath=%s\n' \
    "$label" "$actual_sha" "$actual_tree" "$state" "$path_state"
  [ "$actual_sha" = "$expected_sha" ] || rc=78
  [ "$actual_tree" = "$expected_tree" ] || rc=78
  [ "$state" = clean ] || rc=78
  [ "$path_state" = exact ] || rc=78
  return "$rc"
}

capture_sources() {
  local rc=0
  guard_repo agent "$AGENT_CHECKOUT" \
    28e56cacb42d3da85b02e5b3543895b44f3d0f70 \
    2ebe2ddf5a61f013953ab1e21d51ebaab746e58a || rc=$?
  guard_repo runtime "$RUNTIME_CHECKOUT" \
    6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d \
    ac5b862744bece65b2e30565db1777bacd60da28 || rc=$?
  guard_repo app "$APP_CHECKOUT" \
    867cb2737af1b46dc608c7cd37c349e920fe9422 \
    2b44a46ca51d880c6a00da4c19aa8629b55eb7dd || rc=$?
  guard_repo composition "$COMPOSITION_CHECKOUT" \
    635f4de06fda22a85fc2e4cfc764d0153a4c9f40 \
    5ab5191a296980a0a6bcd1178ab6902d6478a148 || rc=$?
  return "$rc"
}

write_witness() {
  local path=$1 contents=$2 rc
  if [ "$output_owned" -eq 1 ]; then
    if printf '%s\n' "$contents" > "$path"; then return 0; else rc=$?; fi
  else
    rc=98
  fi
  [ "$evidence_rc" -ne 0 ] || evidence_rc=$rc
  printf 'EVIDENCE_UNWRITABLE path=%s exit=%s\n%s\n' "$path" "$rc" "$contents" >&2 || :
  return "$rc"
}

available_bytes() {
  "$PYTHON" -P - "$DISK_USAGE_ROOT" <<'PY'
import shutil
import sys

print(shutil.disk_usage(sys.argv[1]).free)
PY
}

record_disk() {
  local phase=$1 available
  if available=$(available_bytes); then
    printf 'phase=%s\tavailable_bytes=%s\tutc=%s\n' \
      "$phase" "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE" || return 98
    printf '%s\n' "$available"
  else
    printf 'phase=%s\tstatus=UNREADABLE\tutc=%s\n' \
      "$phase" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE" || return 98
    return 97
  fi
}

body_alive() {
  [ -n "$body_pid" ] &&
    { kill -0 "$body_pid" 2>/dev/null || kill -0 -- "-$body_pid" 2>/dev/null; }
}

stop_body() {
  local rc=0
  if body_alive; then
    if kill -0 -- "-$body_pid" 2>/dev/null; then
      kill -TERM -- "-$body_pid" 2>/dev/null || ! body_alive || rc=125
    else
      kill -TERM "$body_pid" 2>/dev/null || ! body_alive || rc=125
    fi
    sleep 1 || rc=$?
    if kill -0 -- "-$body_pid" 2>/dev/null; then
      kill -KILL -- "-$body_pid" 2>/dev/null || ! body_alive || rc=125
    fi
    if kill -0 "$body_pid" 2>/dev/null; then
      kill -KILL "$body_pid" 2>/dev/null || ! body_alive || rc=125
    fi
  fi
  return "$rc"
}

finish() {
  local rc=$1 after_rc=0 after_sources= after_errors= after_status=clean cleanup_rc=0 status_rc=0
  trap - EXIT INT TERM
  set +e
  if body_alive; then stop_body; cleanup_rc=$?; fi
  if [ "$body_started" -eq 1 ] && [ "$body_rc" = pending ]; then
    wait "$body_pid"; body_rc=$?
  fi
  if [ -n "$monitor_pid" ] && [ "$monitor_rc" = pending ]; then
    kill -TERM "$monitor_pid" 2>/dev/null
    wait "$monitor_pid"; monitor_rc=$?
  fi
  if [ "$before_attempted" -eq 0 ]; then
    if before_sources=$(capture_sources); then before_rc=0; else before_rc=$?; fi
  fi
  if after_sources=$(capture_sources); then :; else
    after_rc=$?
    after_errors="source-after guard exit=$after_rc"
    after_status=failed
  fi
  if body_alive; then
    cleanup_rc=125
    after_status=body-not-quiescent
  fi
  write_witness "$SOURCE_BEFORE_FILE" "$before_sources"
  write_witness "$SOURCE_AFTER_FILE" "$after_sources"
  write_witness "$SOURCE_AFTER_ERRORS" "$after_errors"
  write_witness "$RUNNER_EXIT_FILE" "runner_exit=$body_rc"
  write_witness "$MONITOR_EXIT_FILE" "monitor_exit=$monitor_rc"
  if [ "$body_started" -eq 1 ]; then
    if [ -f "$RAW_STDOUT" ] && [ -f "$RAW_STDERR" ]; then
      { printf '%s\n' '--- raw stdout ---'; cat "$RAW_STDOUT"
        printf '%s\n' '--- raw stderr ---'; cat "$RAW_STDERR"; } > "$RUNNER_LOG"
      runner_log_rc=$?
      [ "$runner_log_rc" -eq 0 ] || { [ "$evidence_rc" -ne 0 ] || evidence_rc=$runner_log_rc; }
    fi
    if [ ! -s "$JUNIT_XML" ]; then
      [ "$evidence_rc" -ne 0 ] || evidence_rc=98
    fi
  fi
  if [ "$body_started" -eq 1 ] && [ "$rc" -eq 0 ]; then
    [[ "$body_rc" =~ ^[0-9]+$ ]] && [ "$body_rc" -eq 0 ] || rc="$body_rc"
    [[ "$monitor_rc" =~ ^[0-9]+$ ]] && [ "$monitor_rc" -eq 0 ] || rc="$monitor_rc"
  fi
  [ "$body_started" -ne 0 ] || [ "$rc" -ne 0 ] || rc=78
  [ "$rc" -ne 0 ] || [ "$before_rc" -eq 0 ] || rc=$before_rc
  [ "$rc" -ne 0 ] || [ "$after_rc" -eq 0 ] || rc=$after_rc
  [ "$rc" -ne 0 ] || [ "$cleanup_rc" -eq 0 ] || rc=$cleanup_rc
  [ "$rc" -ne 0 ] || [ "$evidence_rc" -eq 0 ] || rc=$evidence_rc
  local state=NOTRUN
  [ "$body_started" -eq 1 ] && state=FAIL
  [ "$body_started" -eq 0 ] && [ "$rc" -ne 0 ] && state=REFUSED
  [ "$body_started" -eq 1 ] && [ -s "$JUNIT_XML" ] && [ "$rc" -eq 0 ] && state=PASS
  write_witness "$STATUS_FILE" "state=$state
exit=$rc
body_started=$body_started
runner_exit=$body_rc
monitor_exit=$monitor_rc
source_before_exit=$before_rc
source_after=$after_status
evidence_exit=$evidence_rc
finished_utc=$(date -u +%FT%TZ)"
  status_rc=$?
  [ "$status_rc" -eq 0 ] || [ "$rc" -ne 0 ] || rc=$status_rc
  exit "$rc"
}

trap 'finish "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if before_sources=$(capture_sources); then before_rc=0; else before_rc=$?; fi
before_attempted=1
mkdir -p "$RUN_ROOT" "$LAUNCHER_EVIDENCE"
output_owned=1
exec 9>"$RUN_ROOT/heavy.lock"
flock -n 9 || die 'another Agent-core-full heavy body is active'
: > "$RAW_STDOUT"
: > "$RAW_STDERR"
: > "$DISK_TRACE_FILE"
: > "$JUNIT_XML"
: > "$CALLER_ARGV_FILE"
: > "$SERVICE_FILE"
printf '%s\n' 'KEEP' > "$RUN_ROOT/KEEP"
write_witness "$SOURCE_BEFORE_FILE" "$before_sources"
write_witness "$RUNNER_EXIT_FILE" 'runner_exit=not-started'
write_witness "$MONITOR_EXIT_FILE" 'monitor_exit=not-started'
write_witness "$STATUS_FILE" "state=PRECHECK
started_utc=$(date -u +%FT%TZ)"
[ "$before_rc" -eq 0 ] || die 'frozen source admission failed'

python_realpath=$(realpath "$PYTHON") || die 'interpreter cannot be resolved'
python_version=$($PYTHON --version 2>&1) || die 'interpreter version probe failed'
test "$python_realpath" = /usr/bin/python3.13 || die "interpreter realpath mismatch: $python_realpath"
test "$python_version" = 'Python 3.13.16' || die "interpreter version mismatch: $python_version"
write_witness "$INTERPRETER_FILE" "requested=$PYTHON
resolved=$python_realpath
version=$python_version"

source_available=$(record_disk source_admission) || die 'source-admission disk measurement failed'
test "$source_available" -ge "$SOURCE_ADMISSION_BYTES" ||
  die "controller admission disk floor not met: $source_available < $SOURCE_ADMISSION_BYTES"

write_witness "$SERVICE_FILE" "service=agent-core-full
repo=agent
source=$AGENT_CHECKOUT
runtime=$RUNTIME_CHECKOUT
launcher=$AGENT_CHECKOUT/tools/p4-d73-pinned-launch.sh
manifest=$MANIFEST
request_id=$REQUEST_ID
evidence=$LAUNCHER_EVIDENCE
body=one heavy Agent-core-full request
disk_admission_bytes=$SOURCE_ADMISSION_BYTES
disk_stop_bytes=$CONTINUOUS_STOP_BYTES"
write_witness "$CALLER_ARGV_FILE" "env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=$AGENT_CHECKOUT:$RUNTIME_CHECKOUT PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin VIRTUAL_ENV=/home/user/work/venv-agent ASTRID_RUNTIME_CHECKOUT=$RUNTIME_CHECKOUT ASTRID_RUNTIME_SOURCE_ROOT=$RUNTIME_CHECKOUT P4_D73_MANIFEST=$MANIFEST P4_D73_EVIDENCE=$LAUNCHER_EVIDENCE P4_D73_REQUEST_ID=$REQUEST_ID /bin/bash --noprofile --norc -c exec tools/p4-d73-pinned-launch.sh MANIFEST run -- -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=$JUNIT_XML tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py"

monitor_disk() {
  while body_alive; do
    local available
    if available=$(available_bytes); then :; else
      stop_body
      printf 'phase=monitor\tstatus=UNREADABLE\tutc=%s\n' "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE"
      return 97
    fi
    if [ "$available" -lt "$CONTINUOUS_STOP_BYTES" ]; then
      stop_body
      printf 'phase=monitor\tstatus=STOP_FLOOR_REACHED\tavailable_bytes=%s\tutc=%s\n' \
        "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE"
      return 124
    fi
    printf 'phase=monitor\tavailable_bytes=%s\tutc=%s\n' \
      "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE" || {
      stop_body
      return 98
    }
    sleep 5 || { stop_body; return 97; }
  done
}

record_disk before_body >/dev/null || die 'before-body disk trace failed'
cd "$AGENT_CHECKOUT"
export PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"
exec 7>"$RAW_STDOUT" 8>"$RAW_STDERR"
setsid --wait env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$MANIFEST" P4_D73_EVIDENCE="$LAUNCHER_EVIDENCE" P4_D73_REQUEST_ID="$REQUEST_ID" \
  /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' \
  "$AGENT_CHECKOUT" "$MANIFEST" "$JUNIT_XML" >&7 2>&8 &
body_pid=$!
body_started=1
body_rc=pending
monitor_rc=pending
monitor_disk &
monitor_pid=$!
if wait "$body_pid"; then body_rc=0; else body_rc=$?; fi
if wait "$monitor_pid"; then monitor_rc=0; else monitor_rc=$?; fi
after_body_rc=0
if record_disk after_body >/dev/null; then :; else after_body_rc=$?; fi
[ "$after_body_rc" -eq 0 ] || exit "$after_body_rc"
[ "$monitor_rc" -eq 0 ] || exit "$monitor_rc"
[ "$body_rc" -eq 0 ] || exit "$body_rc"
exit 0
