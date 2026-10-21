#!/usr/bin/env bash
set -Eeuo pipefail

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
BASE_RUNTIME=$ORCH/bin/make-runtime
BASE_CHILD=$ORCH/bin/make-child-venv
ORIGINAL=$ORCH/design/vw-m4-runtime-child-existing-env-carrier-1156.patch
SUCCESSOR=$ORCH/design/vw-m4-runtime-child-existing-env-carrier-1156-successor.patch
ROOT=$(mktemp -d /tmp/vw-m4-runtime1156-exact-carrier-fix-1210.XXXXXX)
printf 'fixture root: %s\n' "$ROOT"

cleanup() {
  find "$ROOT" -depth -delete
}
trap cleanup EXIT

mkdir -p "$ROOT/old/bin" "$ROOT/successor/bin" "$ROOT/orch/tests/provision" "$ROOT/agent" "$ROOT/work/runtimes" "$ROOT/bin"
cp "$BASE_RUNTIME" "$ROOT/old/bin/make-runtime"
cp "$BASE_CHILD" "$ROOT/old/bin/make-child-venv"
cp "$BASE_RUNTIME" "$ROOT/successor/bin/make-runtime"
cp "$BASE_CHILD" "$ROOT/successor/bin/make-child-venv"
patch --silent -p1 -d "$ROOT/old" < "$ORIGINAL"
patch --silent -p1 -d "$ROOT/successor" < "$SUCCESSOR"

for suite in old successor; do
  sed -i \
    -e "s#O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch; A=/home/user/work/agent; W=/home/user/work#O=$ROOT/orch; A=$ROOT/agent; W=$ROOT/work#" \
    -e 's#D=/home/user/work/runtimes/\$N#D=$W/runtimes/$N#' \
    -e "s#NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin#NODE=$ROOT/bin#" \
    "$ROOT/$suite/bin/make-runtime" "$ROOT/$suite/bin/make-child-venv"
done

printf '%s\n' '#!/bin/sh' \
  'if [ "$1" = "-C" ]; then shift 2; fi' \
  'case "$1" in' \
  '  cat-file) printf "called\n" > "'"$ROOT"'/git-cat-file-called"; exit 0 ;;' \
  '  fetch) exit 0 ;;' \
  '  archive) printf "called\n" > "'"$ROOT"'/git-archive-called"; exit 1 ;;' \
  'esac' \
  'exit 97' > "$ROOT/bin/git"
chmod +x "$ROOT/bin/git"
printf '%s\n' '#!/bin/sh' \
  'printf "called\n" > "'"$ROOT"'/python-venv-called"' \
  'exit 1' > "$ROOT/bin/python3.13"
chmod +x "$ROOT/bin/python3.13"
export PATH="$ROOT/bin:$PATH"

flat=$ROOT/work/runtimes/agent-remotion-0012
nested=$ROOT/work/runtimes/agent-remotion-0012/remotion
child_flat=$ROOT/work/runtimes/agent-remotion-child-runtime
child_nested=$ROOT/work/runtimes/agent-remotion-child-runtime/remotion
status=
output=

reset_markers() {
  : > "$ROOT/git-archive-called"
  : > "$ROOT/git-cat-file-called"
  : > "$ROOT/python-venv-called"
}

run_capture() {
  set +e
  output=$("$@" 2>&1)
  status=$?
  set -e
  printf '%s\n' "COMMAND: $*"
  printf '%s\n' "STATUS: $status"
  printf '%s\n' "$output"
}

run_trace() {
  set +e
  output=$(BASH_XTRACEFD=2 bash -x "$@" 2>&1)
  status=$?
  set -e
  printf '%s\n' "COMMAND: BASH_XTRACEFD=2 bash -x $*"
  printf '%s\n' "STATUS: $status"
  printf '%s\n' "$output"
}

assert_contains() {
  printf '%s\n' "$output" | grep -Fq -- "$1"
}

assert_not_marked() {
  [ ! -s "$ROOT/$1" ]
}

write_runtime_inputs() {
  printf 'ASTRID_REMOTION_PROJECT_DIR=%s\n' "$1" > "$ROOT/orch/tests/agent-remotion-0012.env"
  printf '%s\n' "$2" > "$ROOT/orch/tests/suites.conf"
}

run_runtime_case() {
  name=$1
  suite_line=$2
  write_runtime_inputs "$flat" "$suite_line"
  reset_markers
  run_capture "$ROOT/old/bin/make-runtime" "agent-remotion-$name" synthetic-agent
  [ "$status" = 1 ]
  [ -s "$ROOT/git-archive-called" ]
  printf 'PASS 1156 red runtime case reached archive: %s\n' "$name"
  reset_markers
  run_capture "$ROOT/successor/bin/make-runtime" "agent-remotion-$name-successor" synthetic-agent
  [ "$status" = 2 ]
  assert_contains 'REFUSED:'
  assert_not_marked git-archive-called
  [ ! -e "$ROOT/work/runtimes/agent-remotion-$name-successor.partial" ]
  printf 'PASS successor refuses runtime case before allocation: %s\n' "$name"
}

run_runtime_case runtime-missing-carrier \
  "agent remotion-0012-nodes env venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
run_runtime_case runtime-foreign-carrier \
  "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=/tmp/foreign-runtime venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
run_runtime_case runtime-broken-carrier \
  "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=relative/runtime venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
run_runtime_case runtime-duplicate-carrier \
  "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=$flat ASTRID_REMOTION_PROJECT_DIR=$nested venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"

for value in "$flat" "$nested"; do
  write_runtime_inputs "$value" "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=$value venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
  reset_markers
  run_trace "$ROOT/successor/bin/make-runtime" "agent-remotion-positive-$(basename "$value")" synthetic-agent
  [ "$status" = 1 ]
  assert_contains "LEGACY_PROJECT=$value"
  assert_contains "SUITE_PROJECT=$value"
  [ -s "$ROOT/git-archive-called" ]
  printf 'PASS successor retains runtime carrier: %s\n' "$value"
done

write_child_inputs() {
  printf 'ASTRID_REMOTION_PROJECT_DIR=%s\n' "$1" > "$ROOT/orch/tests/agent-remotion-child-runtime.env"
  printf '%s\n' "$2" > "$ROOT/orch/tests/suites.conf"
}

run_child_case() {
  name=$1
  suite_line=$2
  write_child_inputs "$child_flat" "$suite_line"
  reset_markers
  run_capture "$ROOT/old/bin/make-child-venv" "venv-agent-child-$name-old" synthetic-agent remotion-0012-nodes agent-remotion-child-runtime
  [ "$status" = 1 ]
  [ -s "$ROOT/python-venv-called" ]
  printf 'PASS 1156 red child case reached venv allocation: %s\n' "$name"
  reset_markers
  run_capture "$ROOT/successor/bin/make-child-venv" "venv-agent-child-$name-successor" synthetic-agent remotion-0012-nodes agent-remotion-child-runtime
  [ "$status" = 2 ]
  assert_contains 'must contain exactly one'
  assert_not_marked python-venv-called
  printf 'PASS successor refuses child case before allocation: %s\n' "$name"
}

run_child_case child-duplicate-carrier \
  "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=$child_flat ASTRID_REMOTION_PROJECT_DIR=$child_nested venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
run_child_case child-duplicate-selector \
  "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=$child_flat venv-agent-child-s2 venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"

for value in "$child_flat" "$child_nested"; do
  write_child_inputs "$value" "agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=$value venv-agent-child-s2 /home/user/work/venv-agent-child-s2/bin/python"
  reset_markers
  run_trace "$ROOT/successor/bin/make-child-venv" "venv-agent-child-positive-$(basename "$value")" synthetic-agent remotion-0012-nodes agent-remotion-child-runtime
  [ "$status" = 1 ]
  assert_contains "CHILD_LINE="
  assert_contains "ASTRID_REMOTION_PROJECT_DIR=$value"
  assert_contains "venv-agent-child-positive-$(basename "$value")"
  [ -s "$ROOT/python-venv-called" ]
  printf 'PASS successor retains child carrier and selector: %s\n' "$value"
done

printf '%s\n' 'PASS actual 1156 red and successor green changed-hunk probes'
