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
  printf 'REFUSED: %s\n' "$*" >&2
  exit 78
}

mkdir -p "$RUN_ROOT"
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

: > "$RAW_STDOUT"
: > "$RAW_STDERR"
: > "$PYTEST_LOG"
: > "$BODY_EXIT_FILE"
: > "$MONITOR_EXIT_FILE"
: > "$DISK_FILE"
printf 'body_exit=not-started\n' > "$BODY_EXIT_FILE"
printf 'monitor_exit=not-started\n' > "$MONITOR_EXIT_FILE"
printf 'state=PRECHECK\nstarted_utc=%s\n' "$(date -u +%FT%TZ)" > "$STATUS_FILE"

body_started=0
body_pid=
monitor_pid=

guard_repo() {
  local label=$1 path=$2 expected_sha=$3 expected_tree=$4
  local actual_sha actual_tree status clean_status
  if actual_sha=$(git -C "$path" rev-parse HEAD 2>/dev/null); then :; else
    printf '%s\tsha=UNREADABLE\ttree=UNREADABLE\tstatus=UNREADABLE\n' "$label"
    return 78
  fi
  if actual_tree=$(git -C "$path" rev-parse 'HEAD^{tree}' 2>/dev/null); then :; else
    printf '%s\tsha=%s\ttree=UNREADABLE\tstatus=UNREADABLE\n' "$label" "$actual_sha"
    return 78
  fi
  if status=$(git -C "$path" status --porcelain --untracked-files=all 2>/dev/null); then :; else
    printf '%s\tsha=%s\ttree=%s\tstatus=UNREADABLE\n' "$label" "$actual_sha" "$actual_tree"
    return 78
  fi
  clean_status=clean
  [ -z "$status" ] || clean_status=dirty
  printf '%s\t%s\t%s\t%s\n' "$label" "$actual_sha" "$actual_tree" "$clean_status"
  [ "$actual_sha" = "$expected_sha" ] || return 78
  [ "$actual_tree" = "$expected_tree" ] || return 78
  [ "$clean_status" = clean ] || return 78
}

capture_sources() {
  guard_repo agent "$AGENT_CHECKOUT" \
    8b6ed2116fd1803d24b2be5bc08bd9490407fe4a \
    0a3691a49b63fd7b0c22fb3478e9cf1947f266ed || return $?
  guard_repo runtime "$RUNTIME_CHECKOUT" \
    fa9cd5464a8b37b02f971de375e56be846cd69e2 \
    124e10dbcd54fb90219e783ec11aa34f8c91590c || return $?
  guard_repo app "$APP_CHECKOUT" \
    7ca61bb3280beca21d98a854af266a382f7ce5df \
    974de7cd08900872eeb0bd6f6004d44323e01fab || return $?
  guard_repo composition "$COMPOSITION_CHECKOUT" \
    67b8aa3d0d6831d3e3504a340ff583c3da253707 \
    62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120 || return $?
}

finish() {
  local rc=$1 after_rc=0 log_rc=0 after_status=clean

  if capture_sources > "$SOURCE_AFTER_FILE" 2> "$SOURCE_AFTER_ERRORS"; then :; else
    after_rc=$?
    after_status=failed
  fi
  if [ "$body_started" -eq 1 ]; then
    if {
      printf '%s\n' '--- raw stdout ---'
      cat "$RAW_STDOUT"
      printf '%s\n' '--- raw stderr ---'
      cat "$RAW_STDERR"
    } > "$PYTEST_LOG"; then :; else
      log_rc=$?
    fi
  fi
  [ "$rc" -ne 0 ] || [ "$after_rc" -eq 0 ] || rc=$after_rc
  [ "$rc" -ne 0 ] || [ "$log_rc" -eq 0 ] || rc=$log_rc
  if [ "$rc" -eq 0 ]; then
    printf 'state=PASS\nexit=%s\nbody_started=%s\nbody_exit=%s\nmonitor_exit=%s\nsource_after=%s\nfinished_utc=%s\n' \
      "$rc" "$body_started" "${body_rc:-not-started}" "${monitor_rc:-not-started}" "$after_status" "$(date -u +%FT%TZ)" > "$STATUS_FILE"
  else
    printf 'state=FAIL\nexit=%s\nbody_started=%s\nbody_exit=%s\nmonitor_exit=%s\nsource_after=%s\nfinished_utc=%s\n' \
      "$rc" "$body_started" "${body_rc:-not-started}" "${monitor_rc:-not-started}" "$after_status" "$(date -u +%FT%TZ)" > "$STATUS_FILE"
  fi
  trap - EXIT
  exit "$rc"
}

trap 'finish "$?"' EXIT

for path in "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$APP_CHECKOUT" "$COMPOSITION_CHECKOUT"; do
  test -d "$path" || die "missing frozen checkout: $path"
  test "$(realpath "$path")" = "$path" || die "checkout path is not exact: $path"
done

if capture_sources > "$SOURCE_BEFORE_FILE"; then :; else
  die "frozen source admission failed"
fi

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
  || die "source-admission disk measurement is unreadable"
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

exec 9>"$RUN_ROOT/heavy.lock"
flock -n 9 || die "another D141b heavy body is active"

body_available=$(record_disk body_dispatch) \
  || die "body-dispatch disk measurement is unreadable"
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
  while kill -0 "$body_pid" 2>/dev/null; do
    local available monitor_measure_rc
    if available=$(record_disk monitor); then :; else
      monitor_measure_rc=$?
      printf 'monitor_failure=unreadable\tavailable_bytes=unknown\tutc=%s\n' "$(date -u +%FT%TZ)" >> "$DISK_FILE" \
        || return 125
      if kill -0 "$body_pid" 2>/dev/null; then
        kill -TERM "$body_pid" 2>/dev/null || return 125
      fi
      return "$monitor_measure_rc"
    fi
    if [ "$available" -lt "$STOP_BYTES" ]; then
      printf 'STOP_FLOOR_REACHED available_bytes=%s stop_bytes=%s\n' "$available" "$STOP_BYTES" >> "$DISK_FILE" \
        || return 125
      if kill -0 "$body_pid" 2>/dev/null; then
        kill -TERM "$body_pid" 2>/dev/null || return 125
      fi
      return 124
    fi
    sleep 5
  done
}

env -i \
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
  > "$RAW_STDOUT" 2> "$RAW_STDERR" &
body_pid=$!
body_started=1
monitor_disk &
monitor_pid=$!
set +e
wait "$body_pid"
body_rc=$?
printf 'body_exit=%s\n' "$body_rc" > "$BODY_EXIT_FILE"
wait "$monitor_pid"
monitor_rc=$?
printf 'monitor_exit=%s\n' "$monitor_rc" > "$MONITOR_EXIT_FILE"
set -e

if [ "$monitor_rc" -ne 0 ]; then
  exit "$monitor_rc"
fi
if [ "$body_rc" -ne 0 ]; then
  exit "$body_rc"
fi
exit 0
