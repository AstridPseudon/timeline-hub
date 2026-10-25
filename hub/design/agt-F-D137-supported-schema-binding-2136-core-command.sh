#!/usr/bin/env bash
set -euo pipefail
umask 077
E=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D137-supported-schema-binding-2136/evidence
T=$TMPDIR
AGENT=/home/user/work/wt/agt-pin-a4e016b6
RUNTIME=/home/user/work/wt/rt-pin-5e9ad1c6
CHILD=/home/user/work/bench-store/entries/child-3e16336b6a5a2d8293a95a99c3665cbafbefb234b4b421fab53e17edde29af30
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
LAUNCHER=$AGENT/tools/p4-d73-pinned-launch.sh
STUB=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence/positive-stub.sh
PRIVATE=$T/d137-schema-binding-controls
mkdir -p "$PRIVATE/positive" "$PRIVATE/poison"
run_one() {
  local label=$1 manifest=$2
  local evidence=$PRIVATE/$label
  local counter=$evidence/counter
  : > "$counter"
  set +e
  env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
    PATH="$NODE:/usr/local/bin:/usr/bin:/bin" \
    PYTHONPATH="$AGENT:$RUNTIME" \
    ASTRID_RUNTIME_CHECKOUT="$RUNTIME" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME" \
    ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA" \
    ASTRID_HOST_EXECUTION_PROFILE=installed ASTRID_REMOTION_PROJECT_DIR="$PROFILE" \
    ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules" \
    P4_D73_MANIFEST="$manifest" P4_D73_EVIDENCE="$evidence" \
    P4_D73_REQUEST_ID="d137-schema-binding-$label" P4_STUB_COUNT="$counter" \
    "$LAUNCHER" "$manifest" dry -- "$STUB" > "$PRIVATE/$label.stdout" 2> "$PRIVATE/$label.stderr"
  rc=$?
  set -e
  printf '%s\n' "$rc" > "$PRIVATE/$label.exit"
  printf '%s\n' "$label rc=$rc counter_bytes=$(wc -c < "$counter") counter_lines=$(wc -l < "$counter")"
}
run_one positive "$E/positive.manifest"
run_one poison "$E/poison.manifest"
sha256sum "$PRIVATE"/positive.stdout "$PRIVATE"/positive.stderr "$PRIVATE"/poison.stdout "$PRIVATE"/poison.stderr "$PRIVATE"/positive.exit "$PRIVATE"/poison.exit "$PRIVATE"/positive/counter "$PRIVATE"/poison/counter
stat -c '%n mode=%a bytes=%s' "$PRIVATE"/positive.stdout "$PRIVATE"/positive.stderr "$PRIVATE"/poison.stdout "$PRIVATE"/poison.stderr "$PRIVATE"/positive.exit "$PRIVATE"/poison.exit "$PRIVATE"/positive/counter "$PRIVATE"/poison/counter
