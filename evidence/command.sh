#!/usr/bin/env bash
set -Eeuo pipefail

# F/D141b: plain PRISTINE COMPARATOR.  This is an operational recipe only;
# the source worker does not invoke pytest, collection, imports, or the body.

readonly AGENT_CHECKOUT=/home/user/work/wt/agt-pin-8b6ed211
readonly RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-fa9cd546
readonly APP_CHECKOUT=/home/user/work/wt/app-pin-7ca61bb3
readonly COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-67b8aa3d
readonly PYTHON=/home/user/work/venv-agent/bin/python
readonly EXPECTED_PYTHON_REALPATH=/usr/bin/python3.13
readonly EXPECTED_PYTHON_VERSION='Python 3.13.16'
readonly RUN_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-plain-command-2358/run-pristine-comparator
readonly GATE_ROOT=$RUN_ROOT/gates
readonly SOURCE_FLOOR_BYTES=4600000000
readonly START_BYTES=4700000000
readonly STOP_BYTES=4000000000

die() {
  local rc=${2:-78}
  printf 'REFUSED: %s\n' "$1" >&2 || :
  exit "$rc"
}

readonly STATUS_FILE=$RUN_ROOT/status.txt
readonly COMMAND_FILE=$RUN_ROOT/command.txt
readonly INTERPRETER_FILE=$RUN_ROOT/interpreter.txt
readonly SOURCE_BEFORE_FILE=$RUN_ROOT/source-before.txt
readonly SOURCE_AFTER_FILE=$RUN_ROOT/source-after.txt
readonly SOURCE_AFTER_ERRORS=$RUN_ROOT/source-after-errors.txt
readonly DISK_FILE=$RUN_ROOT/disk.txt
readonly RAW_STDOUT=$RUN_ROOT/raw-stdout.log
readonly RAW_STDERR=$RUN_ROOT/raw-stderr.log
readonly PYTEST_LOG=$RUN_ROOT/pytest.log
readonly JUNIT_XML=$RUN_ROOT/pristine-comparator.xml
readonly BODY_EXIT_FILE=$RUN_ROOT/body-exit.txt
readonly MONITOR_EXIT_FILE=$RUN_ROOT/monitor-exit.txt

body_started=0
body_pid=
monitor_pid=
body_rc=not-started
monitor_rc=not-started
before_sources=
before_rc=0
before_attempted=0
evidence_rc=0
output_owned=0

guard_repo() {
  local label=$1 path=$2 expected_sha=$3 expected_tree=$4
  local actual_sha=UNREADABLE actual_tree=UNREADABLE status clean_status=UNREADABLE
  local resolved path_status=non-exact rc=0
  if resolved=$(realpath "$path" 2>/dev/null) && [ "$resolved" = "$path" ] && [ -d "$path" ]; then
    path_status=exact
  else
    rc=78
  fi
  actual_sha=$(git -C "$path" rev-parse HEAD 2>/dev/null) || { actual_sha=UNREADABLE; rc=78; }
  actual_tree=$(git -C "$path" rev-parse 'HEAD^{tree}' 2>/dev/null) || { actual_tree=UNREADABLE; rc=78; }
  if status=$(git -C "$path" status --porcelain --untracked-files=all 2>/dev/null); then :; else
    rc=78
    status=UNREADABLE
  fi
  if [ "$status" != UNREADABLE ]; then
    clean_status=clean
    [ -z "$status" ] || clean_status=dirty
  fi
  printf '%s\tsha=%s\ttree=%s\tstatus=%s\tpath=%s\n' \
    "$label" "$actual_sha" "$actual_tree" "$clean_status" "$path_status" || return $?
  [ "$actual_sha" = "$expected_sha" ] || rc=78
  [ "$actual_tree" = "$expected_tree" ] || rc=78
  [ "$clean_status" = clean ] || rc=78
  return "$rc"
}

capture_sources() {
  local rc=0
  guard_repo agent "$AGENT_CHECKOUT" \
    8b6ed2116fd1803d24b2be5bc08bd9490407fe4a \
    0a3691a49b63fd7b0c22fb3478e9cf1947f266ed || rc=$?
  guard_repo runtime "$RUNTIME_CHECKOUT" \
    fa9cd5464a8b37b02f971de375e56be846cd69e2 \
    124e10dbcd54fb90219e783ec11aa34f8c91590c || rc=$?
  guard_repo app "$APP_CHECKOUT" \
    7ca61bb3280beca21d98a854af266a382f7ce5df \
    974de7cd08900872eeb0bd6f6004d44323e01fab || rc=$?
  guard_repo composition "$COMPOSITION_CHECKOUT" \
    67b8aa3d0d6831d3e3504a340ff583c3da253707 \
    62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120 || rc=$?
  return "$rc"
}

# A failed durable write is also printed to service stderr. It cannot become
# PASS merely because a later write succeeds (including inside the EXIT trap).
write_witness() {
  local path=$1 contents=$2 write_rc
  if [ "$output_owned" -eq 1 ]; then
    if printf '%s\n' "$contents" > "$path"; then return 0; else write_rc=$?; fi
  else
    write_rc=98
  fi
  [ "$evidence_rc" -ne 0 ] || evidence_rc=$write_rc
  printf 'EVIDENCE_UNWRITABLE path=%s exit=%s\n%s\n' "$path" "$write_rc" "$contents" >&2 || :
  return "$write_rc"
}

body_alive() {
  [ -n "$body_pid" ] && { kill -0 "$body_pid" 2>/dev/null || kill -0 -- "-$body_pid" 2>/dev/null; }
}

stop_body() {
  local stop_rc=0
  if body_alive; then
    # setsid owns this group. The direct-PID fallback covers the brief window
    # before setsid has established it; no unrelated process group is targeted.
    if kill -0 -- "-$body_pid" 2>/dev/null; then
      kill -TERM -- "-$body_pid" 2>/dev/null || ! body_alive || stop_rc=125
    else
      kill -TERM "$body_pid" 2>/dev/null || ! body_alive || stop_rc=125
    fi
    sleep 1 || stop_rc=$?
    if kill -0 -- "-$body_pid" 2>/dev/null; then
      kill -KILL -- "-$body_pid" 2>/dev/null || ! body_alive || stop_rc=125
    fi
    if kill -0 "$body_pid" 2>/dev/null; then
      kill -KILL "$body_pid" 2>/dev/null || ! body_alive || stop_rc=125
    fi
  fi
  return "$stop_rc"
}

finish() {
  local rc=$1 after_rc=0 after_sources after_errors= after_status=clean state=NOTRUN cleanup_rc=0 log_rc
  trap - EXIT INT TERM
  set +e

  # Stop/reap our own processes before any fallible terminal evidence I/O.
  if body_alive; then
    stop_body || cleanup_rc=$?
  fi
  if [ "$body_started" -eq 1 ] && [ "$body_rc" = pending ]; then
    if wait "$body_pid"; then body_rc=0; else body_rc=$?; fi
  fi
  if [ -n "$monitor_pid" ] && [ "$monitor_rc" = pending ]; then
    kill -TERM "$monitor_pid" 2>/dev/null || :
    if wait "$monitor_pid"; then monitor_rc=0; else monitor_rc=$?; fi
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
    printf 'BODY_NOT_QUIESCENT pid=%s group=%s\n' "$body_pid" "$body_pid" >&2 || :
  fi
  write_witness "$SOURCE_BEFORE_FILE" "$before_sources" || :
  write_witness "$SOURCE_AFTER_FILE" "$after_sources" || :
  write_witness "$SOURCE_AFTER_ERRORS" "$after_errors" || :
  write_witness "$BODY_EXIT_FILE" "body_exit=$body_rc" || :
  write_witness "$MONITOR_EXIT_FILE" "monitor_exit=$monitor_rc" || :
  if [ "$body_started" -eq 1 ]; then
    if {
      printf '%s\n' '--- raw stdout ---' && cat "$RAW_STDOUT" &&
      printf '%s\n' '--- raw stderr ---' && cat "$RAW_STDERR"
    } > "$PYTEST_LOG"; then :; else
      log_rc=$?
      [ "$evidence_rc" -ne 0 ] || evidence_rc=$log_rc
      printf 'EVIDENCE_UNWRITABLE path=%s\n' "$PYTEST_LOG" >&2 || :
    fi
    if [ ! -s "$JUNIT_XML" ]; then
      [ "$evidence_rc" -ne 0 ] || evidence_rc=98
      printf 'EVIDENCE_MISSING path=%s\n' "$JUNIT_XML" >&2 || :
    fi
  fi
  if [ "$body_started" -eq 1 ] && [ "$rc" -eq 0 ]; then
    if [[ "$monitor_rc" =~ ^[0-9]+$ ]] && [[ "$body_rc" =~ ^[0-9]+$ ]]; then
      [ "$monitor_rc" -eq 0 ] || rc=$monitor_rc
      [ "$rc" -ne 0 ] || [ "$body_rc" -eq 0 ] || rc=$body_rc
    else
      rc=125
    fi
  fi
  [ "$body_started" -ne 0 ] || [ "$rc" -ne 0 ] || rc=78
  [ "$rc" -ne 0 ] || [ "$before_rc" -eq 0 ] || rc=$before_rc
  [ "$rc" -ne 0 ] || [ "$after_rc" -eq 0 ] || rc=$after_rc
  [ "$rc" -ne 0 ] || [ "$cleanup_rc" -eq 0 ] || rc=$cleanup_rc
  [ "$rc" -ne 0 ] || [ "$evidence_rc" -eq 0 ] || rc=$evidence_rc
  if [ "$body_started" -eq 1 ] && [ -s "$JUNIT_XML" ]; then
    state=FAIL
    [ "$rc" -ne 0 ] || state=PASS
  fi
  local terminal_status
  printf -v terminal_status 'state=%s\nexit=%s\nbody_started=%s\nbody_exit=%s\nmonitor_exit=%s\nsource_before_exit=%s\nsource_after=%s\nevidence_exit=%s\nfinished_utc=%s' \
    "$state" "$rc" "$body_started" "$body_rc" "$monitor_rc" "$before_rc" "$after_status" "$evidence_rc" "$(date -u +%FT%TZ)"
  if write_witness "$STATUS_FILE" "$terminal_status"; then :; else
    [ "$rc" -ne 0 ] || rc=$evidence_rc
    printf 'TERMINAL state=%s exit=%s durable_status=UNWRITABLE\n' \
      "$([ "$body_started" -eq 0 ] && printf NOTRUN || printf FAIL)" "$rc" >&2 || :
  fi
  exit "$rc"
}

# Nothing fallible above this point: custody and terminal handling precede
# source probes, mkdir and every witness initialization.
trap 'finish "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if before_sources=$(capture_sources); then before_rc=0; else before_rc=$?; fi
before_attempted=1

mkdir -p "$RUN_ROOT"
exec 9>"$RUN_ROOT/heavy.lock"
flock -n 9 || die "another D141b heavy body is active"
output_owned=1
write_witness "$SOURCE_BEFORE_FILE" "$before_sources"
: > "$RAW_STDOUT"
: > "$RAW_STDERR"
: > "$PYTEST_LOG"
: > "$JUNIT_XML"
: > "$DISK_FILE"
write_witness "$BODY_EXIT_FILE" 'body_exit=not-started'
write_witness "$MONITOR_EXIT_FILE" 'monitor_exit=not-started'
write_witness "$STATUS_FILE" "state=PRECHECK
started_utc=$(date -u +%FT%TZ)"
[ "$before_rc" -eq 0 ] || die "frozen source admission failed"

python_realpath=$(realpath "$PYTHON") || die "interpreter cannot be resolved: $PYTHON"
test "$python_realpath" = "$EXPECTED_PYTHON_REALPATH" \
  || die "interpreter realpath mismatch: $python_realpath"
python_version=$("$PYTHON" --version 2>&1) || die "interpreter version probe failed"
test "$python_version" = "$EXPECTED_PYTHON_VERSION" \
  || die "interpreter version mismatch: $python_version"
printf 'requested=%s\nresolved=%s\nversion=%s\n' \
  "$PYTHON" "$python_realpath" "$python_version" > "$INTERPRETER_FILE"

available_bytes() {
  df -B1 --output=avail /home/user \
    | awk '$1 ~ /^[0-9]+$/ { if (++n == 1) value=$1 } END { if (n != 1) exit 1; print value }'
}

record_disk() {
  local phase=$1 available
  if available=$(available_bytes); then :; else
    printf 'phase=%s\tstatus=UNREADABLE\tutc=%s\n' "$phase" "$(date -u +%FT%TZ)" >> "$DISK_FILE" \
      || return 98
    return 97
  fi
  printf 'phase=%s\tavailable_bytes=%s\tutc=%s\n' "$phase" "$available" "$(date -u +%FT%TZ)" >> "$DISK_FILE" \
    || return 98
  printf '%s\n' "$available"
}

source_available=$(record_disk source_admission) \
  || die "source-admission disk measurement or witness failed" "$?"
test "$source_available" -ge "$SOURCE_FLOOR_BYTES" \
  || die "source disk floor not met: $source_available < $SOURCE_FLOOR_BYTES"

# These markers are installed by the manager only after the independent review
# and final U2 freeze.  Missing or non-PASS markers refuse the body.
test -f "$GATE_ROOT/U2_FINAL_FREEZE_PASS" || die "U2 final-freeze gate is absent"
test "$(tr -d '[:space:]' < "$GATE_ROOT/U2_FINAL_FREEZE_PASS")" = PASS \
  || die "U2 final-freeze gate is not PASS"
test -f "$GATE_ROOT/INDEPENDENT_COMMAND_PASS" || die "independent-command gate is absent"
test "$(tr -d '[:space:]' < "$GATE_ROOT/INDEPENDENT_COMMAND_PASS")" = PASS \
  || die "independent-command gate is not PASS"

body_available=$(record_disk body_dispatch) \
  || die "body-dispatch disk measurement or witness failed" "$?"
test "$body_available" -ge "$START_BYTES" \
  || die "body dispatch disk floor not met: $body_available < $START_BYTES"

cat > "$COMMAND_FILE" <<EOF
label=PRISTINE COMPARATOR
source_agent=$AGENT_CHECKOUT
source_agent_sha=8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
source_agent_tree=0a3691a49b63fd7b0c22fb3478e9cf1947f266ed
source_runtime=$RUNTIME_CHECKOUT
source_runtime_sha=fa9cd5464a8b37b02f971de375e56be846cd69e2
source_runtime_tree=124e10dbcd54fb90219e783ec11aa34f8c91590c
python=$PYTHON
python_realpath=$python_realpath
python_version=$python_version
cwd=$AGENT_CHECKOUT
environment=HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=$AGENT_CHECKOUT:$RUNTIME_CHECKOUT ASTRID_RUNTIME_CHECKOUT=$RUNTIME_CHECKOUT
pytest=$PYTHON -P -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=$JUNIT_XML
roots=17 upstream-present roots; no deselection, skip, xfail, or launcher
source_floor_bytes=$SOURCE_FLOOR_BYTES
body_dispatch_bytes=$START_BYTES
continuous_stop_bytes=$STOP_BYTES
raw_stdout=$RAW_STDOUT
raw_stderr=$RAW_STDERR
pytest_log=$PYTEST_LOG
junit_xml=$JUNIT_XML
body_exit=$BODY_EXIT_FILE
monitor_exit=$MONITOR_EXIT_FILE
EOF

cd "$AGENT_CHECKOUT"
export PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"

body_pid=
monitor_pid=
monitor_disk() {
  while body_alive; do
    local available monitor_measure_rc
    # On read failure, stop first: even the failure witness may be unwritable.
    if available=$(available_bytes); then :; else
      stop_body || return $?
      printf 'monitor_failure=unreadable\tavailable_bytes=unknown\tutc=%s\n' "$(date -u +%FT%TZ)" >> "$DISK_FILE" \
        || return 98
      return 97
    fi
    if [ "$available" -lt "$STOP_BYTES" ]; then
      stop_body || return $?
      printf 'STOP_FLOOR_REACHED available_bytes=%s stop_bytes=%s\n' "$available" "$STOP_BYTES" >> "$DISK_FILE" \
        || return 98
      return 124
    fi
    if printf 'phase=monitor\tavailable_bytes=%s\tutc=%s\n' "$available" "$(date -u +%FT%TZ)" >> "$DISK_FILE"; then :; else
      monitor_measure_rc=$?
      stop_body || return $?
      return "$monitor_measure_rc"
    fi
    sleep 5 || { monitor_measure_rc=$?; stop_body || return $?; return "$monitor_measure_rc"; }
  done
}

# Open raw streams in the parent: a redirection failure is still admission
# NOTRUN, before a body PID is announced.
exec 7>"$RAW_STDOUT" 8>"$RAW_STDERR"
set +m
setsid --wait env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" \
  "$PYTHON" -P -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml="$JUNIT_XML" \
  tests/editing_conformance \
  tests/sdk \
  tests/timeline \
  tests/core/timeline \
  tests/core/test_timeline_element_publication.py \
  tests/core/rendering/test_timeline_visualize_cli_grammar.py \
  tests/packs/timeline \
  tests/packs/rendering/test_live_scene_composition.py \
  tests/packs/rendering/test_render_export_task_adapter.py \
  tests/packs/rendering/test_timeline_filmstrip_cards.py \
  tests/packs/rendering/test_timeline_filmstrip_execution.py \
  tests/packs/video_editing/test_runtime_publication_chain.py \
  tests/stage1/test_cold_launch_autobootstrap.py \
  tests/test_installer_schema.py \
  tests/test_installer_sources.py \
  tests/test_timeline_clip_replacement.py \
  tests/v10/test_timelines_create.py \
  >&7 2>&8 &
body_pid=$!
body_started=1
body_rc=pending
monitor_rc=pending
monitor_disk &
monitor_pid=$!
if wait "$body_pid"; then body_rc=0; else body_rc=$?; fi
if wait "$monitor_pid"; then monitor_rc=0; else monitor_rc=$?; fi
# finish writes and checks both exit witnesses, without replacing these exits.

if [ "$monitor_rc" -ne 0 ]; then
  exit "$monitor_rc"
fi
if [ "$body_rc" -ne 0 ]; then
  exit "$body_rc"
fi
exit 0
