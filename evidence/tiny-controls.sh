#!/usr/bin/env bash
set -Eeuo pipefail
ROOT=/home/user/work/wt/agt-F-D141l-controller-binding-prep-0718/evidence
LAUNCHER=/home/user/work/agent/tools/p4-d73-pinned-launch.sh
mkdir -m 700 -p "$ROOT/control-logs"
OUT=$(mktemp -d "$ROOT/control-logs/tiny-XXXXXXXX")
run_case() {
  local name=$1 expected_exit=$2 expected_calls=$3 rc calls
  local out=$OUT/$name
  mkdir -m 700 "$out"
  : > "$out/stub.count"
  if env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
    PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
    P4_D73_EVIDENCE="$out" P4_D73_REQUEST_ID="agent-core-full-$name" P4_STUB_COUNT="$out/stub.count" \
    "$LAUNCHER" "$ROOT/$name.manifest" dry -- "$ROOT/positive-stub.sh" > "$out/raw.stdout" 2> "$out/raw.stderr"; then rc=0; else rc=$?; fi
  calls=$(wc -l < "$out/stub.count")
  printf 'case=%s exit=%s calls=%s expected_exit=%s expected_calls=%s\n' "$name" "$rc" "$calls" "$expected_exit" "$expected_calls" | tee "$out/result.txt"
  if [ "$rc" -ne "$expected_exit" ] || [ "$calls" -ne "$expected_calls" ]; then
    cat "$out/raw.stdout" "$out/raw.stderr" >&2
    return 1
  fi
}
run_case positive 17 1
run_case poison 1 0
