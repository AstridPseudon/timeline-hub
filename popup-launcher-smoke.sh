#!/usr/bin/env bash
set -Eeuo pipefail

die() {
  echo "[popup-launcher-smoke] $*" >&2
  exit 1
}

ORCH=${ORCH:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
SUITE=e2e-popup-post-selection-one-diagnostic-r13-source979ac-tree266109-agent8130-runtime2c4-public13-9412-all75-all77-chrome141-e2e-integration
WRAPPER="$ORCH/workers/app-m2-popup-post-selection-one-diagnostic-capture-r12/run-popup-post-selection-diagnostic-r12.sh"
ACTUAL_SUITE_FILE=${ACTUAL_SUITE_FILE:-$ORCH/tests/suites.conf}
CORRECTED_ROW=${CORRECTED_ROW:-"$PWD/suite-row.corrected.txt"}

[[ -f "$WRAPPER" ]] || die "wrapper is missing: $WRAPPER"
WRAPPER_SHA=354b674ef6aebef594fdf6ae002f7b82423a808b45d69bda00e2062c0ab5c50d
BAD_WRAPPER_SHA=354b674ef6aebef594fdf6ae002f7b82423a808b45d69bda00e2062c0ab5c50d3
[[ "$(sha256sum "$WRAPPER" | awk '{print $1}')" == "$WRAPPER_SHA" ]] || die 'wrapper bytes changed'
bash -n "$WRAPPER"

actual_row=$(awk -v suite="$SUITE" '$1 == "app" && $2 == suite {print; count++} END {if (count != 1) exit 2}' "$ACTUAL_SUITE_FILE") || die 'registered row is not unique'
corrected_row=$(sed -n '1p' "$CORRECTED_ROW")
bad_tail="node $WRAPPER"
good_tail="bash $WRAPPER"
bad_hash="TIMELINE_POPUP_DIAGNOSTIC_WRAPPER_SHA256=sha256:$BAD_WRAPPER_SHA"
good_hash="TIMELINE_POPUP_DIAGNOSTIC_WRAPPER_SHA256=sha256:$WRAPPER_SHA"
[[ "$actual_row" == *"$bad_tail" ]] || die 'registered row does not show the diagnosed node launcher'
[[ "$actual_row" == *"$bad_hash"* ]] || die 'registered row does not show the diagnosed wrapper hash'
normalized_row=${actual_row/"$bad_hash"/"$good_hash"}
normalized_row=${normalized_row/"$bad_tail"/"$good_tail"}
[[ "$corrected_row" == "$normalized_row" ]] || die 'corrected row changes more than wrapper hash and node to bash'
printf '%s\n' 'registered wrapper hash: refused (one extra hex digit)' 

tmp=$(mktemp -d /tmp/popup-launcher-smoke-r14.XXXXXX)
cleanup() {
  find "$tmp" -depth -delete 2>/dev/null || true
}
trap cleanup EXIT

expect_refusal() {
  local label=$1 expected=$2 launcher=$3
  local output status
  set +e
  output=$(env -i PATH="$PATH" "$launcher" "$WRAPPER" 2>&1)
  status=$?
  set -e
  [[ $status -ne 0 ]] || die "$label unexpectedly succeeded"
  grep -Fq "$expected" <<<"$output" || die "$label did not report $expected"
  printf '%s: refused (exit %s)\n' "$label" "$status"
}

expect_refusal missing-env 'missing TIMELINE_POPUP_DIAGNOSTIC_RUN_ROOT' bash
expect_refusal wrong-node 'Unexpected identifier' node

run_guard_case() {
  local label=$1 expected=$2
  local run_root=/tmp/pls14 original_sha=2f908f1421d6c5bc2cb3cca333556342808e3a8d
  local public_sha=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
  local runtime_sha=2c4ac180c2220bdad966bc01e95ad230e99ce26a
  case "$label" in
    path) run_root=/var/pls14 ;;
    hash) original_sha=0000000000000000000000000000000000000000 ;;
    source) public_sha=0000000000000000000000000000000000000000000000000000000000000000 ;;
    pins) runtime_sha=0000000000000000000000000000000000000000 ;;
    *) die "unknown guard case: $label" ;;
  esac

  local output status
  set +e
  output=$(env -i \
    PATH="$PATH" \
    TIMELINE_POPUP_DIAGNOSTIC_RUN_ROOT="$run_root" \
    TIMELINE_POPUP_DIAGNOSTIC_WRAPPER_SHA256=sha256:$WRAPPER_SHA \
    PRIVATE13_NODE_MODULES=/tmp/pls14/node_modules \
    TIMELINE_CURRENT013_PRIVATE13_NODE_MODULES=/tmp/pls14/node_modules \
    TIMELINE_CURRENT013_PRIVATE13_READY=/tmp/pls14/READY \
    TIMELINE_CURRENT013_SHARED_NODE_MODULES=/tmp/pls14/shared \
    ASTRID_CHECKOUT=/tmp/pls14/agent \
    ASTRID_RUNTIME_CHECKOUT=/tmp/pls14/runtime \
    TIMELINE_POPUP_ORIGINAL_APP_SHA="$original_sha" \
    TIMELINE_POPUP_ORIGINAL_APP_TREE=a93260712001a402fe0998b4a16a539d5687611d \
    TIMELINE_POPUP_CANDIDATE_APP_TREE=2661095121e26acd10160d921c191403671373a5 \
    TIMELINE_CURRENT013_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55 \
    TIMELINE_CURRENT013_AGENT_TREE=236c3e57e0265c52b81ba8085de3193026176bff \
    TIMELINE_CURRENT013_RUNTIME_SHA="$runtime_sha" \
    TIMELINE_CURRENT013_RUNTIME_TREE=7ab412cc4bcbe517efcfa806e092336390312e18 \
    TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55 \
    TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
    TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256="$public_sha" \
    ASTRID_APP_DIRECT_DOOR_PORT=28461 \
    VITE_RUNTIME_ORIGIN=http://127.0.0.1:28461 \
    PLAYWRIGHT_CHROMIUM_EXECUTABLE=/tmp/pls14/chrome \
    TMPDIR=/tmp/pls14/t \
    TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/pls14/s \
    PWTEST_CACHE_DIR=/tmp/pls14/p \
    XDG_CACHE_HOME=/tmp/pls14/x \
    VITE_CACHE_DIR=/tmp/pls14/v \
    PLAYWRIGHT_OUTPUT_DIR=/tmp/pls14/o \
    TIMELINE_CURRENT013_RUN_DIR=/tmp/pls14/r \
    HOME=/tmp/pls14/h \
    bash "$WRAPPER" 2>&1)
  status=$?
  set -e
  [[ $status -ne 0 ]] || die "$label unexpectedly succeeded"
  grep -Fq "$expected" <<<"$output" || die "$label did not report $expected"
  printf '%s: refused (exit %s)\n' "$label" "$status"
}

run_guard_case path 'invalid run scope'
run_guard_case hash 'original App SHA mismatch'
run_guard_case source 'Composition source hash is not public13/9412'
run_guard_case pins 'Runtime SHA is not the frozen 2c4 source'

echo 'launcher argv/env comparison: only wrapper hash and node -> bash differ'
echo 'no browser, build, install, or central service invoked'
