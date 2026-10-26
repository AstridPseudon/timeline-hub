#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-return-0735/evidence
ORCH=${D141L_ORCH:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
BIN=${D141L_BIN:-$ORCH/bin}
SUITES=${D141L_SUITES_CONF:-$ORCH/tests/suites.conf}
PYTHON=/home/user/work/venv-agent/bin/python
FLOOR=4714564096
STOP=4000000000
SUITE=agent-core-full
CONTROLLER=agt-F-D141l-binding-return-0735
DISPATCH_UTC=
DISPATCH_FREE=
ORIGINAL_ROW=

die() { printf 'REFUSED: %s\n' "$1" >&2; exit "${2:-78}"; }

check() {
  [ ! -e "$ROOT/controller-binding.json" ] || die 'a future binding exists in source preparation'
  printf '%s\n' \
    'status=SOURCE_READY' \
    'request_test=not_called' \
    'test_run=not_called' \
    'wait_test=not_called' \
    'rows=not_installed' \
    'heavy=not_started' \
    "dispatch_floor_bytes=$FLOOR" \
    "continuous_stop_bytes=$STOP"
}

available() {
  df -B1 --output=avail /home/user | awk '$1 ~ /^[0-9]+$/ { if (++n == 1) print $1 }'
}

read_row() {
  "$PYTHON" - "$SUITES" "$SUITE" <<'PY'
import sys
from pathlib import Path
path, suite = Path(sys.argv[1]), sys.argv[2]
rows = [line for line in path.read_text().splitlines() if line.split()[:2] == ["agent", suite]]
if len(rows) != 1:
    raise SystemExit("expected exactly one native suite row")
print(rows[0])
PY
}

cas_row() {
  "$PYTHON" - "$SUITES" "$SUITE" "$1" "$2" <<'PY'
import os
import sys
from pathlib import Path
path, suite, expected, replacement = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
text = path.read_text()
lines = text.splitlines(keepends=True)
indices = [i for i, line in enumerate(lines) if line.split()[:2] == ["agent", suite]]
if len(indices) != 1 or lines[indices[0]].rstrip("\n") != expected:
    raise SystemExit("suite row CAS refused: registration changed")
ending = "\n" if lines[indices[0]].endswith("\n") else ""
lines[indices[0]] = replacement + ending
tmp = path.with_name("." + path.name + ".d141l-cas")
tmp.write_text("".join(lines))
os.chmod(tmp, path.stat().st_mode & 0o777)
os.replace(tmp, path)
PY
}

sha() { sha256sum "$1" | awk '{print $1}'; }

restore_row() {
  set +e
  current=$(read_row 2>/dev/null || true)
  [ -n "${current:-}" ] && [ -n "${ORIGINAL_ROW:-}" ] && [ "$current" != "$ORIGINAL_ROW" ] && cas_row "$current" "$ORIGINAL_ROW" >/dev/null 2>&1
}

write_receipt() {
  "$PYTHON" - "$@" <<'PY'
import json
import os
import sys
from pathlib import Path
receipt, request, row, registry, brief, terminal, mode, service, command, manifest, source, dispatch_utc, free = sys.argv[1:]
def h(path): return __import__("hashlib").sha256(Path(path).read_bytes()).hexdigest()
data = {
    "path": receipt,
    "controller": os.environ["D141L_CONTROLLER"],
    "mode": mode,
    "suite": "agent-core-full",
    "service_id": service,
    "request_id": service,
    "request": {"path": request, "sha256": h(request)},
    "registered_row": {"path": row, "sha256": h(row), "registry_path": registry, "registry_sha256": h(registry)},
    "brief": {"path": brief, "sha256": h(brief)},
    "command": {"path": command, "sha256": h(command), "manifest": manifest, "manifest_sha256": h(manifest),
                "source_manifest": source, "source_manifest_sha256": h(source)},
    "terminal": {"path": terminal},
    "admission": {"comparison": "PASS", "free_bytes": int(free), "required_bytes": 4714564096, "utc": dispatch_utc},
}
Path(receipt).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
os.chmod(receipt, 0o400)
PY
}

write_binding() {
  "$PYTHON" - "$@" <<'PY'
import json
import os
import sys
from pathlib import Path
binding, receipt, brief, terminal, mode, service = sys.argv[1:]
def entry(path):
    p = Path(path)
    return {"path": str(p), "sha256": __import__("hashlib").sha256(p.read_bytes()).hexdigest()}
data = {"controller": os.environ["D141L_CONTROLLER"], "mode": mode, "request_id": service,
        "service_id": service, "receipt": entry(receipt), "brief": entry(brief),
        "terminal": entry(terminal)}
Path(binding).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
os.chmod(binding, 0o400)
PY
}

dispatch_phase() {
  local mode=$1 original=$2 output=$3
  local command="$ROOT/command-$mode.sh" phase="$output/$mode"
  local receipt="$phase/receipt.json" brief="$phase/brief.md"
  local row_file="$phase/registered-row.txt" terminal="$phase/terminal.json"
  mkdir -m 700 "$phase"
  local row="agent $SUITE /bin/bash $command $receipt $brief"
  cas_row "$original" "$row"
  local registered
  registered=$(read_row)
  [ "$registered" = "$row" ] || die "native row differs after CAS for $mode"
  printf '%s\n' "$registered" > "$row_file"
  chmod 400 "$row_file"
  local returned request_dir service request_path request_sha row_sha
  returned=$("$BIN/request-test" integration:agent "$SUITE" --no-cache)
  request_dir=$(printf '%s\n' "$returned" | "$PYTHON" -c 'import pathlib,sys; rows=[x.strip() for x in sys.stdin if x.strip()]; assert len(rows)==1 and rows[0].endswith("/"); print(rows[0])')
  request_dir=${request_dir%/}
  [ -d "$request_dir" ] || die "request-test did not return a result directory"
  service=$(basename "$request_dir")
  request_path="$request_dir/request"
  [ -f "$request_path" ] || die "request-test result lacks request bytes"
  request_sha=$(sha "$request_path")
  row_sha=$(sha "$row_file")
  printf 'controller=%s\nmode=%s\nutc=%s\nfree_bytes=%s\nrequired_bytes=%s\nservice_id=%s request_sha256=%s row_sha256=%s\n' \
    "$CONTROLLER" "$mode" "$DISPATCH_UTC" "$DISPATCH_FREE" "$FLOOR" "$service" "$request_sha" "$row_sha" > "$brief"
  chmod 400 "$brief"
  D141L_CONTROLLER="$CONTROLLER" write_receipt "$receipt" "$request_path" "$row_file" "$SUITES" "$brief" "$terminal" \
    "$mode" "$service" "$command" "$ROOT/positive.manifest" "$ROOT/source-manifest.json" "$DISPATCH_UTC" "$DISPATCH_FREE"
  "$PYTHON" -P "$ROOT/binding-source.py" admission "$receipt" "$brief" "$mode" "$command" "$ROOT/positive.manifest" "$ROOT/source-manifest.json" > "$phase/admission.json"
  chmod 400 "$phase/admission.json"
  [ "$(read_row)" = "$row" ] || die "native row changed before test-run for $mode"
  local run_rc wait_rc status exit_code
  set +e
  "$BIN/test-run" "$service" > "$phase/test-run.stdout" 2> "$phase/test-run.stderr"
  run_rc=$?
  "$BIN/wait-test" "$service" 100 > "$phase/wait-test.stdout" 2> "$phase/wait-test.stderr"
  wait_rc=$?
  set -e
  status=$(cat "$request_dir/status" 2>/dev/null || printf unknown)
  exit_code=$(cat "$request_dir/exit" 2>/dev/null || printf 1)
  "$PYTHON" - "$terminal" "$service" "$run_rc" "$wait_rc" "$status" "$exit_code" "$request_dir" <<'PY'
import json, os, sys
from pathlib import Path
out, service, run_rc, wait_rc, status, exit_code, result = sys.argv[1:]
data = {"service_id": service, "request_id": service, "status": status, "exit": int(exit_code),
        "test_run_exit": int(run_rc), "wait_test_exit": int(wait_rc),
        "result_dir": result, "summary": str(Path(result) / "summary"),
        "log": str(Path(result) / "log.txt")}
Path(out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
os.chmod(out, 0o400)
PY
  D141L_CONTROLLER="$CONTROLLER" write_binding "$phase/binding.json" "$receipt" "$brief" "$terminal" "$mode" "$service"
  printf 'agent-core-full mode=%s service_id=%s row=%s receipt=%s terminal=%s\n' "$mode" "$service" "$row_file" "$receipt" "$terminal" >> "$output/rows.txt"
  cas_row "$row" "$original"
  [ "$(read_row)" = "$original" ] || die "original row was not restored after $mode"
  [ "$wait_rc" -eq 0 ] || return "$wait_rc"
}

dispatch() {
  [ "$#" -eq 1 ] || die 'usage: controller-continuation.sh dispatch OUTPUT_DIR'
  local output=$1
  [ ! -e "$output" ] || die 'controller output directory already exists'
  mkdir -m 700 "$output"
  local free
  free=$(available)
  [[ "$free" =~ ^[0-9]+$ ]] || die 'controller dispatch disk availability unreadable'
  [ "$free" -ge "$FLOOR" ] || die "controller admission refused: $free < $FLOOR"
  printf 'controller=%s\nutc=%s\nfree_bytes=%s\nrequired_bytes=%s\n' "$CONTROLLER" "$(date -u +%FT%T.%NZ)" "$free" "$FLOOR" > "$output/dispatch-witness.txt"
  DISPATCH_UTC=$(date -u +%FT%T.%NZ)
  DISPATCH_FREE=$free
  chmod 400 "$output/dispatch-witness.txt"
  local original
  original=$(read_row)
  ORIGINAL_ROW=$original
  exec 9>"$ORCH/tests/.d141l-controller.lock"
  flock -n 9 || die 'another existing controller owns the one-heavy route'
  trap restore_row EXIT
  : > "$output/rows.txt"
  dispatch_phase cut "$original" "$output"
  dispatch_phase pristine "$original" "$output"
  "$PYTHON" - "$output" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
bindings = [json.loads(p.read_text()) for p in sorted(out.glob("*/binding.json"))]
if len(bindings) != 2 or len({x["service_id"] for x in bindings}) != 2:
    raise SystemExit("pair did not produce two distinct returned service IDs")
data = {"status": "QUALIFIED", "real_pair_started": True,
        "request_test": "called", "test_run": "called", "wait_test": "called",
        "service_ids": [x["service_id"] for x in bindings],
        "bindings": [str(p) for p in sorted(out.glob("*/binding.json"))]}
(out / "readiness.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
PY
  chmod 400 "$output/readiness.json"
  trap - EXIT
  printf 'status=QUALIFIED output=%s\n' "$output"
}

case "${1:-}" in
  check) [ "$#" -eq 1 ] || die 'usage: controller-continuation.sh check'; check ;;
  dispatch) dispatch "${@:2}" ;;
  *) die 'usage: controller-continuation.sh check|dispatch OUTPUT_DIR' ;;
esac
