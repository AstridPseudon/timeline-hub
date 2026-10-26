#!/usr/bin/env bash
set -Eeuo pipefail
ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-sol-next/evidence
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
BIN=$ORCH/bin
SUITES=$ORCH/tests/suites.conf
PYTHON=/home/user/work/venv-agent/bin/python
INSTALLER=/home/user/work/agent/tools/install_p4_launcher.py
FLOOR=4714564096
STOP=4000000000
SUITE=agent-core-full
ORIGINAL_ROW=
INSTALLED_ROW=
PHASE_TEST_EXIT=

read_row() {
  "$PYTHON" - "$SUITES" "$SUITE" <<'PY'
import sys
from pathlib import Path
rows = [x for x in Path(sys.argv[1]).read_text().splitlines() if x.split()[:2] == ["agent", sys.argv[2]]]
if len(rows) != 1:
    raise SystemExit("expected one existing native suite row; no registry provision in this packet")
print(rows[0])
PY
}

# Use the existing installer and its full-registry preimage, fsync and
# outside-row conservation. This lock covers installers, never the daemon.
replace_row() {
  local expected=$1 replacement=$2 output=$3 digest candidate
  # Check the owned row and hash the very same registry bytes. Reading the row
  # and then hashing a newer registry could bless an intervening same-row edit.
  digest=$("$PYTHON" - "$SUITES" "$SUITE" "$expected" <<'PYIMAGE'
import hashlib, sys
from pathlib import Path
raw = Path(sys.argv[1]).read_bytes()
rows = [line.decode() for line in raw.splitlines() if line.split()[:2] == [b"agent", sys.argv[2].encode()]]
if rows != [sys.argv[3]]:
    raise SystemExit("REFUSED: intervening suite edit retained")
print(hashlib.sha256(raw).hexdigest())
PYIMAGE
) || return 78
  candidate=$output/candidate-row.txt
  mkdir -m 700 "$output" || return 78
  printf '%s\n' "$replacement" > "$candidate" || return 78
  "$PYTHON" -P "$INSTALLER" "$candidate" "$SUITES" "$output" "$digest" "$SUITE" || return 78
}

restore_row() {
  local output=$1 current
  [ -n "$INSTALLED_ROW" ] || return 0
  current=$(read_row) || return 78
  [ "$current" = "$INSTALLED_ROW" ] || { printf 'REFUSED: intervening suite edit retained\n' >&2; return 78; }
  replace_row "$INSTALLED_ROW" "$ORIGINAL_ROW" "$output" || return 78
  INSTALLED_ROW=
}

queue_and_wait() {
  local output=$1 returned wait_rc
  returned=$("$BIN/request-test" integration:agent "$SUITE" --no-cache) || return 78
  SERVICE_DIR=$("$PYTHON" - "$returned" "$ORCH/tests" <<'PY'
from pathlib import Path
import re, sys
lines = sys.argv[1].splitlines()
if len(lines) != 1 or not lines[0].endswith('/'):
    raise SystemExit('request-test returned no unique result directory')
p = Path(lines[0])
if p.parent != Path(sys.argv[2]) or p.resolve(strict=True) != p or not re.fullmatch(r'agent-agent-core-full-\d+-\d+', p.name):
    raise SystemExit('request-test returned an unexpected service directory')
print(p)
PY
) || return 78
  printf '%s\n' "$SERVICE_DIR" > "$output/returned-result-dir.txt" || return 78
  # The queued dispatcher is the sole test-run owner. 124 means keep waiting
  # for this same ID; never submit or launch a replacement.
  while true; do
    if "$BIN/wait-test" "$SERVICE_DIR" 1 >> "$output/wait-test.stdout" 2>> "$output/wait-test.stderr"; then wait_rc=0; else wait_rc=$?; fi
    [ "$wait_rc" -eq 124 ] || break
    # A genuine terminal timeout also exits 124; don't poll it forever.
    if [ -f "$SERVICE_DIR/status" ] && ! [[ $(cat "$SERVICE_DIR/status") =~ ^(queued|running)$ ]]; then break; fi
  done
  WAIT_EXIT=$wait_rc
}

inspect_terminal() {
  "$PYTHON" -P "$ROOT/binding-source.py" inspect-result "$SERVICE_DIR" "$1" \
    "$ROOT/command-$1.sh" "$ROOT/positive.manifest" "$ROOT/source-manifest.json" \
    "$ROOT/privatecontrol-logs/run-$1"
}

dispatch_phase() {
  local mode=$1 output=$2 phase row current observed_exit
  phase=$output/$mode
  mkdir -m 700 "$phase" || return 78
  row="agent $SUITE /bin/bash $ROOT/command-$mode.sh"
  current=$(read_row) || return 78
  [ "$current" = "$ORIGINAL_ROW" ] || return 78
  replace_row "$ORIGINAL_ROW" "$row" "$phase/install" || return 78
  INSTALLED_ROW=$row
  queue_and_wait "$phase" || return 78
  # No controller-authored pre-body receipt. Read the daemon's actual outcome,
  # command output seal, snapshot, and launcher result without upgrading custody.
  inspect_terminal "$mode" > "$phase/observation.json" || return 78
  observed_exit=$("$PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1]))["test_exit"])' "$phase/observation.json") || return 78
  [ "$WAIT_EXIT" -eq "$observed_exit" ] || return 78
  PHASE_TEST_EXIT=$observed_exit
  restore_row "$phase/restore" || return 78
  # Success here means artifact checks completed. PHASE_TEST_EXIT remains the
  # actual test result, including a failed measurement.
}

dispatch_pair() {
  local output=$1 cut_exit pristine_exit
  PHASE_TEST_EXIT=
  dispatch_phase cut "$output" || return 78
  cut_exit=$PHASE_TEST_EXIT
  [[ "$cut_exit" =~ ^[0-9]+$ ]] || return 78
  PHASE_TEST_EXIT=
  dispatch_phase pristine "$output" || return 78
  pristine_exit=$PHASE_TEST_EXIT
  [[ "$pristine_exit" =~ ^[0-9]+$ ]] || return 78
  printf 'cut_test_exit=%s\npristine_test_exit=%s\ncustody=UNPROVEN_NATIVE_ATOMIC_SPAN\nqualification=BLOCKED_U2_003\n' \
    "$cut_exit" "$pristine_exit" > "$output/pair-outcomes.txt" || return 78
  [ "$cut_exit" -eq 0 ] || return "$cut_exit"
  return "$pristine_exit"
}

available() { "$PYTHON" -c 'import shutil; print(shutil.disk_usage("/home/user").free)'; }

dispatch() {
  # Known native custody gap: refuse before output, row, request, or floor work.
  # This is a missing supported mechanism, not a new approval gate.
  "$PYTHON" -P "$ROOT/binding-source.py" dispatch-readiness || return 78
  local output=$1 free
  [ "$#" -eq 1 ] && [[ "$output" = /* ]] && [ ! -e "$output" ] || return 78
  free=$(available) || return 78
  [[ "$free" =~ ^[0-9]+$ ]] && [ "$free" -ge "$FLOOR" ] || return 78
  mkdir -m 700 "$output" || return 78
  printf 'utc=%s\nfree_bytes=%s\nrequired_bytes=%s\n' "$(date -u +%FT%T.%NZ)" "$free" "$FLOOR" > "$output/dispatch-witness.txt" || return 78
  ORIGINAL_ROW=$(read_row) || return 78
  # Both serial members retain native heavy admission (4700000000); this is
  # the single controller floor witness, with no second preparation admission.
  dispatch_pair "$output"
}

main() {
  case "${1:-}" in
    check) printf 'status=BLOCKED_U2_003\nrequest_test=not_called\ntest_run=dispatcher_only\nrows=not_installed\ncontroller_floor=4714564096\nnative_both_members=heavy_4700000000\ncontinuous_stop=4000000000\n' ;;
    dispatch) dispatch "${@:2}" ;;
    *) printf 'usage: controller-continuation.sh check|dispatch OUTPUT_DIR\n' >&2; return 78 ;;
  esac
}
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi
