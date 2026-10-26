#!/usr/bin/env bash
set -Eeuo pipefail

# F/D141b: plain PRISTINE COMPARATOR.  This is an operational recipe only;
# the source worker does not invoke pytest, collection, imports, or the body.

readonly AGENT_CHECKOUT=/home/user/work/wt/agt-pin-8b6ed211
readonly RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-fa9cd546
readonly APP_CHECKOUT=/home/user/work/wt/app-pin-7ca61bb3
readonly COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-67b8aa3d
readonly PYTHON=/home/user/work/venv-agent/bin/python
readonly RUN_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-plain-command-2358/run-pristine-comparator
readonly GATE_ROOT=$RUN_ROOT/gates
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
readonly DISK_FILE=$RUN_ROOT/disk.txt
readonly PYTEST_LOG=$RUN_ROOT/pytest.log
readonly JUNIT_XML=$RUN_ROOT/pristine-comparator.xml

printf 'state=PRECHECK\nstarted_utc=%s\n' "$(date -u +%FT%TZ)" > "$STATUS_FILE"
trap 'rc=$?; if [ "$rc" -eq 0 ]; then printf "state=PASS\nfinished_utc=%s\n" "$(date -u +%FT%TZ)" > "$STATUS_FILE"; else printf "state=FAIL\nexit=%s\nfinished_utc=%s\n" "$rc" "$(date -u +%FT%TZ)" > "$STATUS_FILE"; fi' EXIT

for path in "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$APP_CHECKOUT" "$COMPOSITION_CHECKOUT"; do
  test -d "$path" || die "missing frozen checkout: $path"
  test "$(realpath "$path")" = "$path" || die "checkout path is not exact: $path"
done

guard_repo() {
  local label=$1 path=$2 expected_sha=$3 expected_tree=$4
  local actual_sha actual_tree status
  actual_sha=$(git -C "$path" rev-parse HEAD)
  actual_tree=$(git -C "$path" rev-parse 'HEAD^{tree}')
  test "$actual_sha" = "$expected_sha" || die "$label commit mismatch: $actual_sha"
  test "$actual_tree" = "$expected_tree" || die "$label tree mismatch: $actual_tree"
  status=$(git -C "$path" status --porcelain --untracked-files=all)
  test -z "$status" || die "$label checkout is dirty"
  printf '%s\t%s\t%s\tclean\n' "$label" "$actual_sha" "$actual_tree"
}

capture_sources() {
  guard_repo agent "$AGENT_CHECKOUT" \
    8b6ed2116fd1803d24b2be5bc08bd9490407fe4a \
    0a3691a49b63fd7b0c22fb3478e9cf1947f266ed
  guard_repo runtime "$RUNTIME_CHECKOUT" \
    fa9cd5464a8b37b02f971de375e56be846cd69e2 \
    124e10dbcd54fb90219e783ec11aa34f8c91590c
  guard_repo app "$APP_CHECKOUT" \
    7ca61bb3280beca21d98a854af266a382f7ce5df \
    974de7cd08900872eeb0bd6f6004d44323e01fab
  guard_repo composition "$COMPOSITION_CHECKOUT" \
    67b8aa3d0d6831d3e3504a340ff583c3da253707 \
    62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120
}

capture_sources > "$SOURCE_BEFORE_FILE"

printf 'requested=%s\nresolved=%s\n' "$PYTHON" "$(realpath "$PYTHON")" > "$INTERPRETER_FILE"
"$PYTHON" --version 2>&1 | tee -a "$INTERPRETER_FILE"

available_bytes() {
  df -B1 --output=avail /home/user \
    | awk '$1 ~ /^[0-9]+$/ { if (++n == 1) value=$1 } END { if (n != 1) exit 1; print value }'
}

record_disk() {
  local phase=$1 available
  available=$(available_bytes) || die "disk availability is unreadable"
  printf 'phase=%s\tavailable_bytes=%s\tutc=%s\n' "$phase" "$available" "$(date -u +%FT%TZ)" >> "$DISK_FILE"
  printf '%s\n' "$available"
}

available=$(record_disk start)
test "$available" -ge "$START_BYTES" || die "start disk floor not met: $available < $START_BYTES"

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

cat > "$COMMAND_FILE" <<EOF
label=PRISTINE COMPARATOR
source_agent=$AGENT_CHECKOUT
source_agent_sha=8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
source_agent_tree=0a3691a49b63fd7b0c22fb3478e9cf1947f266ed
source_runtime=$RUNTIME_CHECKOUT
source_runtime_sha=fa9cd5464a8b37b02f971de375e56be846cd69e2
source_runtime_tree=124e10dbcd54fb90219e783ec11aa34f8c91590c
python=$PYTHON
python_realpath=$(realpath "$PYTHON")
cwd=$AGENT_CHECKOUT
environment=HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=$AGENT_CHECKOUT:$RUNTIME_CHECKOUT ASTRID_RUNTIME_CHECKOUT=$RUNTIME_CHECKOUT
pytest=$PYTHON -P -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=$JUNIT_XML
roots=17 upstream-present roots; no deselection, skip, xfail, or launcher
EOF

cd "$AGENT_CHECKOUT"
export PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"

body_pid=
monitor_pid=
monitor_disk() {
  while kill -0 "$body_pid" 2>/dev/null; do
    local available
    available=$(record_disk monitor) || return 97
    if [ "$available" -lt "$STOP_BYTES" ]; then
      printf 'STOP_FLOOR_REACHED available_bytes=%s stop_bytes=%s\n' "$available" "$STOP_BYTES" >> "$DISK_FILE"
      kill -TERM "$body_pid" 2>/dev/null || true
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
  > "$PYTEST_LOG" 2>&1 &
body_pid=$!
monitor_disk &
monitor_pid=$!
set +e
wait "$body_pid"
body_rc=$?
wait "$monitor_pid"
monitor_rc=$?
set -e
if [ "$monitor_rc" -eq 124 ]; then
  body_rc=124
fi

capture_sources > "$SOURCE_AFTER_FILE"
test "$body_rc" -eq 0 || exit "$body_rc"
