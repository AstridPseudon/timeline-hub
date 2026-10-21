#!/bin/sh
set -eu

# The existing public13 runner owns the graph attachment, source checkouts,
# caches, short TMPDIR, build, and cleanup. This file only forwards its final
# ordinary child command to the already-approved producer selector.
if test "${PRODUCER_PUBLIC13_NPM_FORWARDER:-0}" = 1; then
  case "${PRODUCER_PUBLIC13_RUN_MODE:-}" in
    list|run) ;;
    *) echo 'PRODUCER_PUBLIC13_RUN_MODE must be list or run' >&2; exit 2 ;;
  esac
  if test "${1:-}" = run && test "${2:-}" = build:hosted; then
    exec "$PRODUCER_PUBLIC13_REAL_NPM" "$@"
  fi
  if test "${1:-}" = run \
    && test "${2:-}" = test:e2e:three-products \
    && test "${3:-}" = -- \
    && test "${4:-}" = --grep \
    && test "${5:-}" = 'M2 ordinary extension batch' \
    && test "$#" = 5; then
    LIST_LOG=${PRODUCER_PUBLIC13_LIST_LOG:?missing list log}
    set +e
    if test "$PRODUCER_PUBLIC13_RUN_MODE" = list; then
      "$PRODUCER_PUBLIC13_APP_ROOT/node_modules/.bin/playwright" test \
        --config playwright.producer-ownership-current-pin.config.ts \
        tests/e2e/local/producer-ownership-current-pin.spec.ts --list \
        >"$LIST_LOG" 2>&1
    else
      "$PRODUCER_PUBLIC13_APP_ROOT/node_modules/.bin/playwright" test \
        --config playwright.producer-ownership-current-pin.config.ts \
        tests/e2e/local/producer-ownership-current-pin.spec.ts \
        >"$LIST_LOG" 2>&1
    fi
    status=$?
    set -e
    cat "$LIST_LOG"
    if test "$PRODUCER_PUBLIC13_RUN_MODE" = list; then
      test "$status" = 0 || exit "$status"
      ! grep -Eiq 'No tests found|No test files found|collected 0 items|Total: 0 test' "$LIST_LOG"
      grep -Fq 'Total: 1 test in 1 file' "$LIST_LOG"
      exit 0
    fi
    passed_count=$(grep -Ec '^[[:space:]]*1[[:space:]]+passed([[:space:]]|$)' "$LIST_LOG" || true)
    failed_count=$(grep -Ec '^[[:space:]]*1[[:space:]]+failed([[:space:]]|$)' "$LIST_LOG" || true)
    if test "$passed_count" = 1 && test "$failed_count" = 0; then
      test "$status" = 0 || { echo 'producer actual test reported pass with nonzero child status' >&2; exit 1; }
    elif test "$passed_count" = 0 && test "$failed_count" = 1; then
      test "$status" -ne 0 || { echo 'producer actual test reported failure with zero child status' >&2; exit 1; }
    else
      echo 'producer actual test did not report exactly one passed or failed test' >&2
      exit 1
    fi
    exit "$status"
  fi
  echo "unexpected npm child command: $*" >&2
  exit 2
fi

APP_ROOT=${1:?usage: $0 APP_ROOT list|run|preflight}
test "$#" = 2 || { echo "usage: $0 APP_ROOT list|run|preflight" >&2; exit 2; }
RUN_MODE=$2
case "$RUN_MODE" in
  list|run|preflight) ;;
  *) echo 'mode must be list or run' >&2; exit 2 ;;
esac
case "$APP_ROOT" in
  /*) ;;
  *) echo 'APP_ROOT must be absolute' >&2; exit 2 ;;
esac

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
PUBLIC13_RUNNER="$ORCH/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh"
LOCKED_GRAPH="$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph"
LOCKED_GRAPH_ARCHIVE="$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar"
AGENT_REPO=/home/user/peteromallet/astrid-agent
RUNTIME_REPO=/home/user/banodoco/banodoco-workspace-runtime
AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55
AGENT_TREE=236c3e57e0265c52b81ba8085de3193026176bff
RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a
RUNTIME_TREE=7ab412cc4bcbe517efcfa806e092336390312e18
APP_SHA=4ef89267f00d193273441ff6dbb955f30d27d708
APP_TREE=8c7393050ded32854503dfb7719a102b5dec94eb
APP_SOURCE_SHA=00bbc22d63b4abe7275cfe9ad5f3762157d7394f
APP_SOURCE_TREE=f41a45c01293b0248a27c490bb9e8aa02be33ecd
APP_SOURCE_PARENT_SHA=70dec48e88ea036bf160539b58b68bb64c38f3b3
BODY_SHA=36dd91257fd13dcad0d58b48c790caa5063b4c8c
BODY_TREE=d908845dbc8e5ebf96698d08621557e904f20c52
GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
COMPOSITION_TARBALL_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
COMPOSITION_PACKAGE_SHA=7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61
COMPOSITION_EVALUATION_SHA=e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155
SPEC_SHA=d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
HELPER_SHA=50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
CONFIG_SHA=5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
RUNNER_SHA=be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b
PRODUCER_SHA=sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56

PREFLIGHT_FAILURES=''
PREFLIGHT_CHECKS=0

record_failure() {
  label=$1
  if test -n "$PREFLIGHT_FAILURES"; then
    PREFLIGHT_FAILURES="$PREFLIGHT_FAILURES
"
  fi
  PREFLIGHT_FAILURES="${PREFLIGHT_FAILURES}- ${label}"
}

check() {
  label=$1
  shift
  PREFLIGHT_CHECKS=$((PREFLIGHT_CHECKS + 1))
  if "$@" >/dev/null 2>&1; then
    return 0
  fi
  record_failure "$label"
}

verify_ref() {
  repo=$1
  commit=$2
  tree=$3
  test -d "$repo/.git" \
    && test "$(git -C "$repo" rev-parse --verify "$commit^{commit}" 2>/dev/null)" = "$commit" \
    && test "$(git -C "$repo" show -s --format=%T "$commit^{commit}" 2>/dev/null)" = "$tree" \
    && test -z "$(git -C "$repo" status --porcelain=v1 --untracked-files=all)"
}
verify_app_ref() {
  repo=$1
  commit=$2
  tree=$3
  test "$(git -C "$repo" rev-parse --verify "$commit^{commit}" 2>/dev/null)" = "$commit" \
    && test "$(git -C "$repo" show -s --format=%T "$commit^{commit}" 2>/dev/null)" = "$tree" \
    && test -z "$(git -C "$repo" status --porcelain=v1 --untracked-files=all)"
}

check_app_root() { test -d "$APP_ROOT" && test -f "$APP_ROOT/package.json"; }
check_app_clean() { test -z "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)"; }
check_agent_source() { verify_ref "$AGENT_REPO" "$AGENT_SHA" "$AGENT_TREE"; }
check_runtime_source() { verify_ref "$RUNTIME_REPO" "$RUNTIME_SHA" "$RUNTIME_TREE"; }
check_app_baseline() { verify_app_ref "$APP_ROOT" "$APP_SHA" "$APP_TREE"; }
check_body() { verify_app_ref "$APP_ROOT" "$BODY_SHA" "$BODY_TREE"; }
check_source_ancestry() {
  test "$(git -C "$APP_ROOT" rev-parse --verify "$APP_SOURCE_SHA^{commit}" 2>/dev/null)" = "$APP_SOURCE_SHA" \
    && test "$(git -C "$APP_ROOT" show -s --format=%T "$APP_SOURCE_SHA^{commit}" 2>/dev/null)" = "$APP_SOURCE_TREE" \
    && test "$(git -C "$APP_ROOT" show -s --format=%P "$APP_SOURCE_SHA^{commit}" 2>/dev/null)" = "$APP_SOURCE_PARENT_SHA" \
    && test "$(git -C "$APP_ROOT" show -s --format=%P "$APP_SOURCE_PARENT_SHA^{commit}" 2>/dev/null)" = "$APP_SHA"
}
check_approved_delta() {
  APP_HEAD=$(git -C "$APP_ROOT" rev-parse HEAD)
  if test "$APP_HEAD" = "$APP_SOURCE_SHA"; then
    :
  else
    test "$(git -C "$APP_ROOT" rev-parse HEAD^1 2>/dev/null)" = "$APP_SOURCE_SHA" || return 1
  fi
  CHANGED=$(git -C "$APP_ROOT" diff --name-only "$APP_SHA" "$APP_HEAD" -- . | grep -v '^scripts/testing/run-producer-public13-list\.sh$' || true)
  test -z "$CHANGED"
}
check_body_source_hashes() {
  test "$(sha256sum "$APP_ROOT/tests/e2e/local/producer-ownership-current-pin.spec.ts" | cut -d' ' -f1)" = "$SPEC_SHA" \
    && test "$(sha256sum "$APP_ROOT/tests/e2e/local/support/producer-ownership-current-pin.ts" | cut -d' ' -f1)" = "$HELPER_SHA" \
    && test "$(sha256sum "$APP_ROOT/playwright.producer-ownership-current-pin.config.ts" | cut -d' ' -f1)" = "$CONFIG_SHA"
}
check_runner() { test "$(sha256sum "$PUBLIC13_RUNNER" | cut -d' ' -f1)" = "$RUNNER_SHA"; }
check_graph() {
  test -d "$LOCKED_GRAPH/node_modules" \
    && test "$(realpath "$LOCKED_GRAPH/node_modules")" = "$LOCKED_GRAPH/node_modules" \
    && test "$(sha256sum "$LOCKED_GRAPH_ARCHIVE" | cut -d' ' -f1)" = "$GRAPH_ARCHIVE_SHA" \
    && test "$(node -p "require('$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13 \
    && test "$(sha256sum "$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json" | cut -d' ' -f1)" = "$COMPOSITION_PACKAGE_SHA" \
    && test "$(sha256sum "$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/dist/evaluation.js" | cut -d' ' -f1)" = "$COMPOSITION_EVALUATION_SHA" \
    && test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | sha256sum | cut -d' ' -f1)" = "$COMPOSITION_TARBALL_SHA" \
    && test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | tar -tzf - | sed '/\/$/d' | wc -l)" = 77
}
check_cohort() {
  test "$(git -C "$RUNTIME_REPO" show "$RUNTIME_SHA:contract/artifacts.json" | EXPECTED_PRODUCER="$PRODUCER_SHA" node --input-type=commonjs -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{let x=JSON.parse(s);if(x.version!==process.env.EXPECTED_PRODUCER)process.exit(1);process.stdout.write(String(Object.keys(x.artifacts).length))})')" = 75
}
check_disk() {
  available_kib=$(df -Pk "$APP_ROOT" | awk 'NR == 2 { print $4 }')
  test "$available_kib" -ge 10485760
}
check_isolation() {
  test -L "$APP_ROOT/node_modules" \
    && test -n "$(readlink "$APP_ROOT/node_modules")" \
    && test -d "$LOCKED_GRAPH/node_modules" \
    && test "$(realpath "$LOCKED_GRAPH/node_modules")" = "$LOCKED_GRAPH/node_modules"
}
check_forwarded_argv() {
  if test "$RUN_MODE" != list && test "$RUN_MODE" != run && test "$RUN_MODE" != preflight; then
    return 1
  fi
  test -f "$APP_ROOT/package.json" \
    && test -f "$APP_ROOT/playwright.producer-ownership-current-pin.config.ts" \
    && test -f "$APP_ROOT/tests/e2e/local/producer-ownership-current-pin.spec.ts"
}

check app-root check_app_root
check app-clean check_app_clean
check app-baseline check_app_baseline
check approved-body check_body
check source-ancestry check_source_ancestry
check approved-delta check_approved_delta
check body-helper-config-hashes check_body_source_hashes
check existing-runner check_runner
check graph check_graph
check cohort check_cohort
check disk-space check_disk
check isolation check_isolation
check argv-and-test-path check_forwarded_argv

if test "$PREFLIGHT_CHECKS" = 0; then
  record_failure 'no preflight checks executed'
fi
if test -n "$PREFLIGHT_FAILURES"; then
  printf '%s\n%s\n' 'producer preflight FAIL' "$PREFLIGHT_FAILURES" >&2
  exit 1
fi

LIST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/tl-ap2-producer-existing-XXXXXX")
trap 'find -P "$LIST_ROOT" -depth -delete 2>/dev/null || true' EXIT HUP INT TERM
mkdir -p "$LIST_ROOT/bin"
REAL_NPM=$(command -v npm)
SCRIPT_PATH=$(realpath "$0")
ln -s "$SCRIPT_PATH" "$LIST_ROOT/bin/npm"
LIST_LOG="$LIST_ROOT/producer-list.log"
export PRODUCER_PUBLIC13_NPM_FORWARDER=1
export PRODUCER_PUBLIC13_REAL_NPM=$REAL_NPM
export PRODUCER_PUBLIC13_APP_ROOT=$APP_ROOT
export PRODUCER_PUBLIC13_LIST_LOG=$LIST_LOG
export PRODUCER_PUBLIC13_RUN_MODE=$RUN_MODE
export PATH="$LIST_ROOT/bin:$PATH"

if test "$RUN_MODE" = preflight; then
  export PUBLIC13_PREFLIGHT_ONLY=1
else
  unset PUBLIC13_PREFLIGHT_ONLY
fi

exec sh "$PUBLIC13_RUNNER" "$APP_ROOT" ordinary
