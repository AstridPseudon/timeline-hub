#!/usr/bin/env bash
set -Eeuo pipefail

# F D141l plain pristine comparator. It uses the same environment and
# collection settings as command-cut.sh, but never invokes the D73 launcher.
readonly EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-proof-return-0515/evidence
readonly RUN_ROOT=$EVIDENCE_ROOT/private/measurement-runs/pristine-agent-core-full
readonly SOURCE_MANIFEST=$EVIDENCE_ROOT/source-manifest.json
readonly COMMAND_PATH=$EVIDENCE_ROOT/command-pristine.sh
readonly AGENT_CHECKOUT=/home/user/work/wt/agt-pin-64197afa
readonly RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-fa9cd546
readonly PYTHON=/home/user/work/venv-agent/bin/python
readonly NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
readonly PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
readonly SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
readonly DISK_USAGE_ROOT=/home/user
readonly SOURCE_ADMISSION_BYTES=4714564096
readonly CONTINUOUS_STOP_BYTES=4000000000
readonly REQUEST_ID=agent-core-full
readonly ADMISSION_RECEIPT=$1
readonly CONTROLLER_BRIEF=$2
APP_RECEIPT=$3
[ -n "$APP_RECEIPT" ] || APP_RECEIPT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D141s-postREG-source-home-0545.json
readonly APP_RECEIPT

readonly STATUS_FILE=$RUN_ROOT/status.txt
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
readonly CUSTODY_BEFORE_FILE=$RUN_ROOT/custody-before.txt
readonly CUSTODY_AFTER_FILE=$RUN_ROOT/custody-after.txt
readonly INTERPRETER_FILE=$RUN_ROOT/interpreter.txt
readonly CALLER_ARGV_FILE=$RUN_ROOT/callerargv.txt
readonly SERVICE_FILE=$RUN_ROOT/service.txt
readonly MONITOR_STOP=$RUN_ROOT/monitor-stop

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
  local message=$1 exit_code=78
  [ "$#" -ge 2 ] && exit_code=$2
  [[ $exit_code =~ ^[1-9][0-9]*$ ]] || exit_code=78
  printf 'REFUSED: %s\n' "$message" >&2
  exit "$exit_code"
}

guard_repo() {
  local label=$1 path=$2 expected_sha=$3 expected_tree=$4
  local actual_sha=UNREADABLE actual_tree=UNREADABLE state=UNREADABLE path_state=non-exact rc=0
  if [ "$(realpath "$path" 2>/dev/null || :)" = "$path" ] && [ -d "$path" ]; then path_state=exact; else rc=78; fi
  actual_sha=$(git -C "$path" rev-parse HEAD 2>/dev/null) || { actual_sha=UNREADABLE; rc=78; }
  actual_tree=$(git -C "$path" rev-parse 'HEAD^{tree}' 2>/dev/null) || { actual_tree=UNREADABLE; rc=78; }
  state=$(git -C "$path" status --porcelain --untracked-files=all 2>/dev/null) || { state=UNREADABLE; rc=78; }
  [ "$state" = '' ] && state=clean || state=dirty
  printf '%s\tsha=%s\ttree=%s\tstatus=%s\tpath=%s\n' "$label" "$actual_sha" "$actual_tree" "$state" "$path_state"
  [ "$actual_sha" = "$expected_sha" ] || rc=78
  [ "$actual_tree" = "$expected_tree" ] || rc=78
  [ "$state" = clean ] || rc=78
  [ "$path_state" = exact ] || rc=78
  return "$rc"
}

guard_app_receipt() {
  "$PYTHON" -P - "$APP_RECEIPT" <<'PY_APP'
import json
import sys
from pathlib import Path
try:
    data = json.loads(Path(sys.argv[1]).read_bytes())
    app = data["app"]
    if len(app["head"]) != 40 or len(app["tree"]) != 40:
        raise ValueError("App head/tree is not concrete")
    if not app["clean"] or not app["normal_ref_equal"]:
        raise ValueError("App receipt is not clean normal owner evidence")
    if data["agent"]["head"] != "8585ed9c0404d0187b2ce70242d25114a32747c2":
        raise ValueError("App receipt Agent binding mismatch")
    if data["composition"]["head"] != "635f4de06fda22a85fc2e4cfc764d0153a4c9f40":
        raise ValueError("App receipt Composition binding mismatch")
except (OSError, UnicodeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
    print(f"REFUSED: App owner receipt: {exc}", file=sys.stderr)
    raise SystemExit(78)
print(f"app_head={app['head']} app_tree={app['tree']} parents={' '.join(app['parents'])}")
PY_APP
}

capture_sources() {
  local rc=0
  guard_repo agent "$AGENT_CHECKOUT" 64197afa297f86f1e738238d5e80aff6d33e303a 6c0488b3efdfa47479b0ad1b7bd20608383be26e || rc=$?
  guard_repo runtime "$RUNTIME_CHECKOUT" fa9cd5464a8b37b02f971de375e56be846cd69e2 124e10dbcd54fb90219e783ec11aa34f8c91590c || rc=$?
  guard_app_receipt || rc=$?
  return "$rc"
}

write_witness() {
  local path=$1 contents=$2 rc
  if [ "$output_owned" -eq 1 ]; then
    if printf '%s\n' "$contents" > "$path"; then chmod 600 "$path" 2>/dev/null || :; return 0; else rc=$?; fi
  else rc=98; fi
  [ "$evidence_rc" -ne 0 ] || evidence_rc=$rc
  printf 'EVIDENCE_UNWRITABLE path=%s exit=%s\n%s\n' "$path" "$rc" "$contents" >&2 || :
  return "$rc"
}

available_bytes() {
  "$PYTHON" -P - "$DISK_USAGE_ROOT" <<'PY_DISK'
import shutil
import sys
print(shutil.disk_usage(sys.argv[1]).free)
PY_DISK
}

record_disk() {
  local phase=$1 available
  available=$(available_bytes) || { printf 'phase=%s\tstatus=UNREADABLE\tutc=%s\n' "$phase" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE"; return 97; }
  printf 'phase=%s\tavailable_bytes=%s\tutc=%s\n' "$phase" "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE" || return 98
  printf '%s\n' "$available"
}

admitted_dispatch() {
  "$PYTHON" -P - "$ADMISSION_RECEIPT" "$CONTROLLER_BRIEF" "$SOURCE_MANIFEST" "$SOURCE_MANIFEST" "$COMMAND_PATH" "$APP_RECEIPT" "$SOURCE_ADMISSION_BYTES" <<'PY_ADMIT'
import hashlib
import json
import sys
from pathlib import Path
receipt, brief, manifest, source_manifest, command, app_receipt = map(Path, sys.argv[1:7])
floor = int(sys.argv[7])
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
try:
    record = json.loads(receipt.read_bytes())
    request = record["request"]
    witness = record["manager_dispatch_witness"]
    if record["route"] != "request-test" or record["authenticated"] is not True:
        raise ValueError("receipt is not an authenticated request-test receipt")
    if record["status"] != "ADMITTED" or request["request_id"] != "agent-core-full":
        raise ValueError("receipt is not the admitted agent-core-full request")
    if request["command"] != str(command):
        raise ValueError("request command binding mismatch")
    if request["manifest_sha256"] != digest(manifest) or request["source_manifest_sha256"] != digest(source_manifest):
        raise ValueError("manifest/source-manifest binding mismatch")
    if request["brief_sha256"] != digest(brief) or request["app_receipt_sha256"] != digest(app_receipt):
        raise ValueError("brief/App binding mismatch")
    if witness["comparison"] != "PASS" or type(witness["free_bytes"]) is not int or witness["free_bytes"] < floor:
        raise ValueError("D89d dispatch floor was not met")
    if witness["required_bytes"] != floor:
        raise ValueError("receipt required floor is not D89d floor")
except (OSError, UnicodeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
    print(f"REFUSED: authenticated controller receipt: {exc}", file=sys.stderr)
    raise SystemExit(78)
print(f"request_id={request['request_id']} service_id={record['service_id']} dispatch_utc={witness['utc']} admitted_bytes={witness['free_bytes']} floor_bytes={floor}")
PY_ADMIT
}

body_alive() { [ -n "$body_pid" ] && { kill -0 "$body_pid" 2>/dev/null || kill -0 -- "-$body_pid" 2>/dev/null; }; }

stop_body() {
  local rc=0
  if body_alive; then
    kill -TERM -- "-$body_pid" 2>/dev/null || kill -TERM "$body_pid" 2>/dev/null || rc=125
    sleep 1 || rc=$?
    kill -KILL -- "-$body_pid" 2>/dev/null || kill -KILL "$body_pid" 2>/dev/null || :
  fi
  return "$rc"
}

custody() {
  local out=$1
  : > "$out" || return 98
  for path in "$RUN_ROOT" "$RUN_ROOT/KEEP" "$RAW_STDOUT" "$RAW_STDERR" "$RUNNER_LOG" "$JUNIT_XML" "$DISK_TRACE_FILE" "$SOURCE_BEFORE_FILE" "$SOURCE_AFTER_FILE" "$STATUS_FILE"; do
    realpath "$path" >> "$out" || return 98
    stat -c 'mode=%a inode=%i owner=%u:%g path=%n' "$path" >> "$out" || return 98
    sha256sum "$path" >> "$out" || return 98
  done
}

check_custody() {
  [ -s "$CUSTODY_BEFORE_FILE" ] && [ -s "$CUSTODY_AFTER_FILE" ] || return 98
  diff -u <(grep -Ev '^[0-9a-f]{64}  ' "$CUSTODY_BEFORE_FILE") <(grep -Ev '^[0-9a-f]{64}  ' "$CUSTODY_AFTER_FILE") >/dev/null || return 98
  [ -f "$RAW_STDOUT" ] && [ -f "$RAW_STDERR" ] && [ -f "$RUNNER_LOG" ] && [ -f "$JUNIT_XML" ] || return 98
  return 0
}

monitor_disk() {
  while [ ! -e "$MONITOR_STOP" ]; do
    local available
    available=$(available_bytes) || { stop_body; return 97; }
    if [ "$available" -lt "$CONTINUOUS_STOP_BYTES" ]; then
      printf 'phase=monitor\tstatus=STOP_FLOOR_REACHED\tavailable_bytes=%s\tutc=%s\n' "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE"
      stop_body; return 124
    fi
    printf 'phase=monitor\tavailable_bytes=%s\tutc=%s\n' "$available" "$(date -u +%FT%TZ)" >> "$DISK_TRACE_FILE" || { stop_body; return 98; }
    sleep 5 || { stop_body; return 97; }
  done
  return 0
}

finish() {
  local rc=$1 after_rc=0 after_sources= after_status=clean cleanup_rc=0 status_rc=0 source_before=
  trap - EXIT INT TERM
  set +e
  body_alive && { stop_body; cleanup_rc=$?; }
  [ "$body_started" -eq 1 ] && [ "$body_rc" = pending ] && { wait "$body_pid"; body_rc=$?; }
  [ -n "$monitor_pid" ] && [ "$monitor_rc" = pending ] && { : > "$MONITOR_STOP"; wait "$monitor_pid"; monitor_rc=$?; }
  if [ "$before_attempted" -eq 0 ]; then source_before=$(capture_sources); before_rc=$?; fi
  after_sources=$(capture_sources); after_rc=$?; [ "$after_rc" -eq 0 ] || after_status=failed
  write_witness "$SOURCE_BEFORE_FILE" "$source_before"; write_witness "$SOURCE_AFTER_FILE" "$after_sources"; write_witness "$SOURCE_AFTER_ERRORS" "after_exit=$after_rc"
  write_witness "$RUNNER_EXIT_FILE" "runner_exit=$body_rc"; write_witness "$MONITOR_EXIT_FILE" "monitor_exit=$monitor_rc"
  if [ "$body_started" -eq 1 ]; then
    { printf '%s\n' '--- raw stdout ---'; cat "$RAW_STDOUT"; printf '%s\n' '--- raw stderr ---'; cat "$RAW_STDERR"; } > "$RUNNER_LOG" || evidence_rc=98
    [ -s "$JUNIT_XML" ] || evidence_rc=98
  fi
  if [ "$body_started" -eq 1 ] && [ "$rc" -eq 0 ]; then
    [ "$body_rc" -eq 0 ] || rc=$body_rc
    [ "$monitor_rc" -eq 0 ] || rc=$monitor_rc
  fi
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
  [ "$status_rc" -eq 0 ] || rc=$status_rc
  [ "$output_owned" -eq 1 ] && custody "$CUSTODY_AFTER" || evidence_rc=98
  [ "$output_owned" -eq 1 ] && check_custody || evidence_rc=98
  [ "$rc" -ne 0 ] || [ "$evidence_rc" -eq 0 ] || rc=$evidence_rc
  exit "$rc"
}

readonly ROOTS=(
  tests/editing_conformance
  tests/sdk
  tests/timeline
  tests/core/timeline
  tests/core/test_timeline_element_publication.py
  tests/core/rendering/test_timeline_visualize_cli_grammar.py
  tests/packs/timeline
  tests/packs/rendering/test_live_scene_composition.py
  tests/packs/rendering/test_render_export_task_adapter.py
  tests/packs/rendering/test_timeline_filmstrip_cards.py
  tests/packs/rendering/test_timeline_filmstrip_execution.py
  tests/packs/video_editing/test_runtime_publication_chain.py
  tests/stage1/test_cold_launch_autobootstrap.py
  tests/test_installer_schema.py
  tests/test_installer_sources.py
  tests/test_timeline_clip_replacement.py
  tests/v10/timelines_create.py
)

trap 'finish "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

[ "$#" -ge 2 ] || die 'expected authenticated admission receipt and controller brief'
[ ! -e "$RUN_ROOT" ] || die 'run root already exists; refusing stale custody'
if source_before=$(capture_sources); then before_rc=0; else before_rc=$?; fi
before_attempted=1
mkdir -m 700 -p "$RUN_ROOT"
output_owned=1
exec 9>"$RUN_ROOT/heavy.lock"
flock -n 9 || die 'another Agent-core-full body is active'
: > "$RAW_STDOUT"; : > "$RAW_STDERR"; : > "$RUNNER_LOG"; : > "$JUNIT_XML"; : > "$DISK_TRACE_FILE"
printf KEEP > "$RUN_ROOT/KEEP"
chmod 444 "$RUN_ROOT/KEEP"; chmod 600 "$RAW_STDOUT" "$RAW_STDERR" "$RUNNER_LOG" "$JUNIT_XML" "$DISK_TRACE_FILE"
write_witness "$SOURCE_BEFORE_FILE" "$source_before"
write_witness "$RUNNER_EXIT_FILE" runner_exit=not-started
write_witness "$MONITOR_EXIT_FILE" monitor_exit=not-started
[ "$before_rc" -eq 0 ] || die 'frozen pristine source admission failed'
write_witness "$STATUS_FILE" state=PRECHECK
python_realpath=$(realpath "$PYTHON") || die 'interpreter cannot be resolved'
python_version=$("$PYTHON" --version 2>&1) || die 'interpreter version probe failed'
node_version=$("$NODE" --version) || die 'Node cannot be resolved'
[ "$python_realpath" = /usr/bin/python3.13 ] || die "interpreter realpath mismatch: $python_realpath"
[ "$python_version" = 'Python 3.13.16' ] || die "interpreter version mismatch: $python_version"
[ "$node_version" = v20.19.4 ] || die "Node version mismatch: $node_version"
write_witness "$INTERPRETER_FILE" "requested=$PYTHON
resolved=$python_realpath
version=$python_version
node=$NODE
node_version=$node_version
profile=$PROFILE
schema=$SCHEMA
runtime_source_root=$RUNTIME_CHECKOUT"
controller_witness=$(admitted_dispatch) || die 'controller admission is not an authenticated exact receipt binding'
source_available=$(record_disk source_admission) || die 'source-admission disk measurement failed'
[ "$source_available" -ge "$CONTINUOUS_STOP_BYTES" ] || die 'source disk stop floor reached'
write_witness "$SERVICE_FILE" "route=existing request-test/test-run
request_id=$REQUEST_ID
controller_dispatch=$controller_witness
controller_admission_receipt=$ADMISSION_RECEIPT
controller_manager_brief=$CONTROLLER_BRIEF
app_owner_receipt=$APP_RECEIPT
source_manifest=$SOURCE_MANIFEST
body=one heavy pristine Agent-core-full comparator
admission_floor_bytes=$SOURCE_ADMISSION_BYTES
continuous_stop_bytes=$CONTINUOUS_STOP_BYTES"
write_witness "$CALLER_ARGV_FILE" "env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=$AGENT_CHECKOUT:$RUNTIME_CHECKOUT PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin VIRTUAL_ENV=/home/user/work/venv-agent ASTRID_RUNTIME_CHECKOUT=$RUNTIME_CHECKOUT ASTRID_RUNTIME_SOURCE_ROOT=$RUNTIME_CHECKOUT $PYTHON -P -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=$JUNIT_XML tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_publication.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/packs/timeline tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py"
before_body_available=$(record_disk before_body) || die 'before-body disk trace failed'
[ "$before_body_available" -ge "$CONTINUOUS_STOP_BYTES" ] || die 'before-body disk stop floor reached'
custody "$CUSTODY_BEFORE_FILE" || die 'before custody failed'
monitor_disk & monitor_pid=$!
cd "$AGENT_CHECKOUT"
exec 7> "$RAW_STDOUT" 8> "$RAW_STDERR"
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin VIRTUAL_ENV=/home/user/work/venv-agent ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" "$PYTHON" -P -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$JUNIT_XML" "${ROOTS[@]}" >&7 2>&8 &
body_pid=$!
body_started=1
body_rc=pending
monitor_rc=pending
if wait "$body_pid"; then body_rc=0; else body_rc=$?; fi
after_body_available=$(record_disk after_body) || exit 97
[ "$after_body_available" -ge "$CONTINUOUS_STOP_BYTES" ] || exit 124
: > "$MONITOR_STOP"
if wait "$monitor_pid"; then monitor_rc=0; else monitor_rc=$?; fi
[ "$monitor_rc" -eq 0 ] || exit "$monitor_rc"
[ "$body_rc" -eq 0 ] || exit "$body_rc"
exit 0

