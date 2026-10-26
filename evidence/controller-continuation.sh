#!/usr/bin/env bash
set -Eeuo pipefail

# The existing controller calls this only after request-test/test-run has
# produced a genuine receipt, request, service row and owner brief. It does
# not submit, install, poll, or admit anything itself.
ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-controller-binding-prep-0718/evidence
PYTHON=/home/user/work/venv-agent/bin/python
BINDING_SOURCE=$ROOT/binding-source.py

die() { printf 'REFUSED: %s\n' "$1" >&2; exit "${2:-78}"; }

usage() {
  cat >&2 <<'EOF'
usage:
  controller-continuation.sh check
  controller-continuation.sh materialize BINDING.json OUTPUT_DIR

OUTPUT_DIR is a private controller-owned evidence directory. Nothing is
installed into tests/suites.conf and no request-test/test-run action is made.
EOF
  exit 78
}

check() {
  [ ! -e "$ROOT/controller-binding.json" ] || die 'a future binding was pre-created in source preparation'
  printf '%s\n' 'status=WAITING_FOR_GENUINE_CONTROLLER_BINDING' \
    'request_test=not_called' 'test_run=not_called' 'rows=not_installed' \
    'heavy=not_started' 'floor_bytes=4714564096'
}

materialize() {
  local binding=$1 output=$2
  [ -f "$binding" ] || die 'controller binding file is missing'
  [ "$output" != "$ROOT" ] || die 'output must not replace source preparation'
  [ ! -e "$output" ] || die 'output directory already exists; retained unchanged'
  mkdir -m 700 "$output"
  local cut pristine
  cut=$("$PYTHON" -P "$BINDING_SOURCE" consume "$binding" cut \
    "$ROOT/command-cut.sh" "$ROOT/positive.manifest" "$ROOT/source-manifest.json") \
    || die 'cut binding did not pass the production consumer'
  pristine=$("$PYTHON" -P "$BINDING_SOURCE" consume "$binding" pristine \
    "$ROOT/command-pristine.sh" "$ROOT/positive.manifest" "$ROOT/source-manifest.json") \
    || die 'pristine binding did not pass the production consumer'
  local receipt brief
  receipt=$("$PYTHON" -P - "$binding" <<'PY'
import json
import sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["receipt"]["path"])
PY
)
  brief=$("$PYTHON" -P - "$binding" <<'PY'
import json
import sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["brief"]["path"])
PY
)
  printf 'agent agent-core-full /bin/bash %s %s %s\n' \
    "$ROOT/command-cut.sh" "$receipt" "$brief" > "$output/rows.txt"
  printf 'agent d141b-pristine-comparator-2358 /bin/bash %s %s %s\n' \
    "$ROOT/command-pristine.sh" "$receipt" "$brief" >> "$output/rows.txt"
  "$PYTHON" -P - "$output" "$binding" "$cut" "$pristine" <<'PY'
import json
import pathlib
import sys

out, binding, cut, pristine = map(pathlib.Path, sys.argv[1:])
data = json.loads(binding.read_text(encoding="utf-8"))
payload = {
    "status": "MATERIALIZED_NOT_INSTALLED",
    "cut": json.loads(cut),
    "pristine": json.loads(pristine),
    "rows": str(out / "rows.txt"),
    "request_id": data["request_id"],
    "service_id": data["service_id"],
}
(out / "readiness.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
  printf 'status=MATERIALIZED_NOT_INSTALLED output=%s\n' "$output"
}

case "${1:-}" in
  check) [ "$#" -eq 1 ] || usage; check ;;
  materialize) [ "$#" -eq 3 ] || usage; materialize "$2" "$3" ;;
  *) usage ;;
esac
