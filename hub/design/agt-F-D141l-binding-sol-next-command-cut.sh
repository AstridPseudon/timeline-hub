#!/usr/bin/env bash
set -Eeuo pipefail

# Operational recipe only. The controller binding is consumed when supplied;
# this preparation never submits or installs a row.
configure() {
  MODE=cut
  EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-sol-next/evidence
  CHECKER=$EVIDENCE_ROOT/check-source.py
  BINDING_SOURCE=$EVIDENCE_ROOT/binding-source.py
  COMMAND_PATH=$EVIDENCE_ROOT/command-cut.sh
  MANIFEST=$EVIDENCE_ROOT/positive.manifest
  SOURCE_MANIFEST=$EVIDENCE_ROOT/source-manifest.json
  AGENT_CHECKOUT=/home/user/work/agent
  RUNTIME_CHECKOUT=/home/user/work/runtime
  PYTHON=/home/user/work/venv-agent/bin/python
  NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
  PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
  SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
  SOURCE_ADMISSION_BYTES=4714564096
  CONTINUOUS_STOP_BYTES=4000000000
  REQUEST_ID=
  RUN_ROOT=$EVIDENCE_ROOT/privatecontrol-logs/run-cut
  PAIR_LOCK=$EVIDENCE_ROOT/privatecontrol-logs/pair-heavy.lock
  ROOTS=(
    tests/editing_conformance
    tests/sdk
    tests/timeline
    tests/core/timeline
    tests/core/test_timeline_element_orphan_cleanup.py
    tests/core/test_timeline_element_publication.py
    tests/core/test_timeline_element_publication_runtime.py
    tests/core/rendering/test_timeline_visualize_cli_grammar.py
    tests/core/rendering/test_local_schema.py
    tests/packs/timeline
    tests/packs/rendering/test_composition_package.py
    tests/packs/rendering/test_live_scene_composition.py
    tests/packs/rendering/test_render_export_task_adapter.py
    tests/packs/rendering/test_timeline_filmstrip_cards.py
    tests/packs/rendering/test_timeline_filmstrip_execution.py
    tests/packs/video_editing/test_runtime_publication_chain.py
    tests/stage1/test_cold_launch_autobootstrap.py
    tests/test_installer_schema.py
    tests/test_installer_sources.py
    tests/test_installer_bootstrap_schema.py
    tests/test_timeline_clip_replacement.py
    tests/v10/test_timelines_create.py
  )
  body_pid= monitor_pid= source_before=
  body_started=0 body_rc=not-started monitor_rc=not-started
  before_rc=0 evidence_rc=0 output_owned=0
  setup_paths
}

setup_paths() {
  LAUNCHER_EVIDENCE=$RUN_ROOT/launcher-evidence
  RAW_STDOUT=$RUN_ROOT/raw-stdout.log
  RAW_STDERR=$RUN_ROOT/raw-stderr.log
  RUNNER_LOG=$RUN_ROOT/runner.log
  JUNIT_XML=$RUN_ROOT/agent-core-full.xml
  DISK_TRACE_FILE=$RUN_ROOT/disk-trace.txt
  SOURCE_BEFORE_FILE=$RUN_ROOT/source-before.txt
  SOURCE_AFTER_FILE=$RUN_ROOT/source-after.txt
  STATUS_FILE=$RUN_ROOT/status.txt
  MONITOR_STOP=$RUN_ROOT/monitor-stop
}

die() { printf 'REFUSED: %s\n' "$1" >&2; exit "${2:-78}"; }

write_witness() {
  if [ "$output_owned" -eq 1 ] && printf '%s\n' "$2" > "$1" && chmod 600 "$1"; then
    return 0
  fi
  evidence_rc=98
  printf 'EVIDENCE_UNWRITABLE path=%s\n' "$1" >&2
  return 98
}

capture_sources() { "$PYTHON" -P "$CHECKER" sources "$MODE"; }

admitted_dispatch() {
  "$PYTHON" -P "$BINDING_SOURCE" dispatch-readiness
}

native_service_identity() {
  "$PYTHON" -P "$BINDING_SOURCE" identity "${D66_OUTPUT_DIR:-}" \
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests "$SOURCE_MANIFEST"
}

interpreter() {
  [ "$(realpath "$PYTHON")" = /usr/bin/python3.13 ] || return 78
  [ "$("$PYTHON" --version)" = 'Python 3.13.16' ] || return 78
  [ "$("$NODE" --version)" = v20.19.4 ] || return 78
  printf 'python=%s\nresolved=%s\nversion=%s\nnode=%s\nprofile=%s\nschema=%s\nruntime_source_root=%s\n' \
    "$PYTHON" "$(realpath "$PYTHON")" "$("$PYTHON" --version)" "$NODE" "$PROFILE" "$SCHEMA" "$RUNTIME_CHECKOUT"
}

build_argv() {
  PYTEST_ARGV=(-m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 "--junitxml=$JUNIT_XML" "${ROOTS[@]}")
  BODY_ENV=(env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
    "PYTHONPATH=$AGENT_CHECKOUT:$RUNTIME_CHECKOUT"
    PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin
    VIRTUAL_ENV=/home/user/work/venv-agent "ASTRID_RUNTIME_CHECKOUT=$RUNTIME_CHECKOUT"
    "ASTRID_RUNTIME_SOURCE_ROOT=$RUNTIME_CHECKOUT" "ASTRID_REMOTION_PROJECT_DIR=$PROFILE"
    "ASTRID_NODE_EXECUTABLE=$NODE" "ASTRID_TEST_NODE_MODULES=$PROFILE/node_modules")
  if [ "$MODE" = cut ]; then
    BODY_ARGV=("${BODY_ENV[@]}" "P4_D73_MANIFEST=$MANIFEST" "P4_D73_EVIDENCE=$LAUNCHER_EVIDENCE"
      "P4_D73_REQUEST_ID=$REQUEST_ID" /bin/bash --noprofile --norc -c 'exec "$@"' _
      "$AGENT_CHECKOUT/tools/p4-d73-pinned-launch.sh" "$MANIFEST" run -- "${PYTEST_ARGV[@]}")
  else
    # The production launcher unsets this before both its preflight and body.
    BODY_ARGV=("${BODY_ENV[@]}" /bin/bash --noprofile --norc -c 'unset PYTHONNOUSERSITE; exec "$@"' _
      "$PYTHON" -P "${PYTEST_ARGV[@]}")
  fi
}

available_bytes() {
  "$PYTHON" -P -c 'import os; s=os.statvfs("/home/user"); print(s.f_bavail*s.f_frsize)'
}

record_disk() (
  local available
  # Monitor and foreground samples share one append stream. Measure and stamp
  # under that file's lock so append order also remains timestamp order.
  exec 6>>"$DISK_TRACE_FILE" || return 98
  flock -x 6 || return 98
  available=$(available_bytes) || return 97
  [[ $available =~ ^[0-9]+$ ]] || return 97
  printf 'phase=%s\tavailable_bytes=%s\tutc=%s\n' "$1" "$available" "$(date -u +%FT%T.%NZ)" >&6 || return 98
  [ "$available" -ge "$CONTINUOUS_STOP_BYTES" ] || return 124
)

body_alive() {
  [ -n "$body_pid" ] && { kill -0 -- "-$body_pid" 2>/dev/null || kill -0 "$body_pid" 2>/dev/null; }
}

group_running() {
  [ -n "$body_pid" ] || return 1
  ps -eo pgid=,stat= | awk -v group="$body_pid" '$1 == group && $2 !~ /^Z/ { found=1 } END { exit !found }'
}

stop_body() {
  if body_alive; then
    kill -TERM -- "-$body_pid" 2>/dev/null || kill -TERM "$body_pid" 2>/dev/null || ! body_alive || return 125
    sleep 1
    if body_alive; then
      kill -KILL -- "-$body_pid" 2>/dev/null || kill -KILL "$body_pid" 2>/dev/null || ! body_alive || return 125
    fi
  fi
}

monitor_disk() {
  local rc
  while [ ! -e "$MONITOR_STOP" ]; do
    if record_disk monitor; then :; else
      rc=$?
      stop_body || return 125
      return "$rc"
    fi
    sleep 5 || { rc=$?; stop_body; return "$rc"; }
  done
}

custody_before() {
  "$PYTHON" -P "$CHECKER" custody-before "$RUN_ROOT" "$COMMAND_PATH" "$MANIFEST" "$SOURCE_MANIFEST" "$CHECKER"
}

custody_after() { "$PYTHON" -P "$CHECKER" custody-after "$RUN_ROOT" "$body_started"; }

finish() {
  local rc=$1 after_sources after_rc=0 cleanup_rc=0
  trap - EXIT INT TERM HUP
  set +e
  stop_body || cleanup_rc=$?
  if [ "$body_rc" = pending ]; then wait "$body_pid"; body_rc=$?; fi
  if group_running; then
    for ((i=0; i<20; i++)); do group_running || break; sleep 0.1; done
    group_running && cleanup_rc=125
  fi
  if [ "$monitor_rc" = pending ]; then
    : > "$MONITOR_STOP" || evidence_rc=98
    wait "$monitor_pid"; monitor_rc=$?
  fi
  if [ "$output_owned" -ne 1 ]; then exit "$rc"; fi
  after_sources=$(capture_sources); after_rc=$?
  write_witness "$SOURCE_AFTER_FILE" "$after_sources" || evidence_rc=98
  record_disk after_body || { cleanup_rc=$?; [ "$cleanup_rc" -ne 98 ] || evidence_rc=98; }
  write_witness "$RUN_ROOT/runner-exit.txt" "runner_exit=$body_rc" || evidence_rc=98
  write_witness "$RUN_ROOT/monitor-exit.txt" "monitor_exit=$monitor_rc" || evidence_rc=98
  { printf '%s\n' '--- raw stdout ---'; cat "$RAW_STDOUT"; printf '%s\n' '--- raw stderr ---'; cat "$RAW_STDERR"; } > "$RUNNER_LOG" || evidence_rc=98
  if [ -e "$RUN_ROOT/custody-before.json" ]; then
    custody_after || evidence_rc=98
  elif [ "$body_started" -eq 1 ]; then
    evidence_rc=98
  fi
  [ "$monitor_rc" != 98 ] || evidence_rc=98
  # Compute the terminal state only after every evidence/custody operation.
  if [ "$monitor_rc" != not-started ] && [ "$monitor_rc" -ne 0 ]; then rc=$monitor_rc; fi
  [ "$rc" -ne 0 ] || [ "$body_rc" = not-started ] || rc=$body_rc
  [ "$rc" -ne 0 ] || rc=$before_rc
  [ "$rc" -ne 0 ] || rc=$after_rc
  [ "$rc" -ne 0 ] || rc=$cleanup_rc
  [ "$evidence_rc" -eq 0 ] || rc=$evidence_rc
  local state=REFUSED
  if [ "$body_started" -eq 1 ]; then state=FAIL; [ "$rc" -ne 0 ] || state=PASS; fi
  write_witness "$RUN_ROOT/.terminal-status" "state=$state
exit=$rc
body_started=$body_started
runner_exit=$body_rc
monitor_exit=$monitor_rc
source_before_exit=$before_rc
source_after_exit=$after_rc
cleanup_exit=$cleanup_rc
evidence_exit=$evidence_rc" || { printf 'TERMINAL_STATUS_UNWRITABLE exit=98\n' >&2; exit 98; }
  chmod 400 "$RUN_ROOT/.terminal-status" && mv -T "$RUN_ROOT/.terminal-status" "$STATUS_FILE" || { printf 'TERMINAL_STATUS_PUBLISH_FAILED exit=98\n' >&2; exit 98; }
  exit "$rc"
}

run() {
  trap 'finish "$?"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  trap 'exit 129' HUP
  umask 077
  mkdir -m 700 -p "$(dirname "$RUN_ROOT")"
  mkdir -m 700 "$RUN_ROOT" || die 'run root exists or cannot be owned; retained unchanged'
  output_owned=1
  for p in "$RAW_STDOUT" "$RAW_STDERR" "$RUNNER_LOG" "$JUNIT_XML" "$DISK_TRACE_FILE"; do : > "$p"; chmod 600 "$p"; done
  printf KEEP > "$RUN_ROOT/KEEP"
  chmod 444 "$RUN_ROOT/KEEP"
  exec 9>"$PAIR_LOCK"
  flock -n 9 || die 'one heavy pair member is already active'
  if source_before=$(capture_sources); then before_rc=0; else before_rc=$?; fi
  write_witness "$SOURCE_BEFORE_FILE" "$source_before"
  [ "$before_rc" -eq 0 ] || die 'exact clean source guard failed'
  interpreter > "$RUN_ROOT/interpreter.txt" || die 'interpreter/runtime identity failed'
  REQUEST_ID=$(native_service_identity) || die 'native service identity unavailable'
  build_argv
  printf '%q ' "${BODY_ARGV[@]}" > "$RUN_ROOT/callerargv.txt"
  printf '\n' >> "$RUN_ROOT/callerargv.txt"
  admitted_dispatch > "$RUN_ROOT/service.txt" || die 'current pair lacks a genuine normal controller binding'
  # Dispatch admission is checked once in its original witness, never here again.
  record_disk source_admission || exit "$?"
  custody_before || exit 98
  record_disk before_body || exit "$?"
  cd "$AGENT_CHECKOUT"
  # setsid owns the complete body group, including xdist workers.
  exec 7>"$RAW_STDOUT" 8>"$RAW_STDERR"
  ( trap - EXIT INT TERM HUP; exec setsid --wait "${BODY_ARGV[@]}" ) >&7 2>&8 &
  body_pid=$!
  body_started=1 body_rc=pending monitor_rc=pending
  monitor_disk & monitor_pid=$!
  if wait "$body_pid"; then body_rc=0; else body_rc=$?; fi
  record_disk after_wait || exit "$?"
  : > "$MONITOR_STOP"
  if wait "$monitor_pid"; then monitor_rc=0; else monitor_rc=$?; fi
  [ "$monitor_rc" -eq 0 ] || exit "$monitor_rc"
  exit "$body_rc"
}

main() { configure "$@"; run; }
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi

