#!/bin/sh
# The preflight intentionally keeps going so all prerequisite failures are
# reported together; each check is responsible for returning nonzero.

# Owned final95 selected runner.  The default mode is CHEAP/offline preflight;
# set SELECTED_FINAL95_MODE=run only for the later central actual invocation.
# The shared normal014 helper is sourced read-only for its private graph/source
# functions.  This runner never edits that helper or the old selected driver.

APP_ROOT=${1:?usage: $0 APP_ROOT}
case "$APP_ROOT" in
  /*) ;;
  *) echo 'APP_ROOT must be absolute' >&2; exit 2 ;;
esac
test -f "$APP_ROOT/package.json"
# The central service may present a captured tree under a synthetic commit.
# A separate keeper remains the exact protected source registration.  The
# keeper is required only by the actual path, while cheap preflight retains
# the historical one-root invocation.
APP_KEEPER_ROOT=${APP_KEEPER_ROOT:-/home/user/work/wt/app-pin-0cc2583a}
if [ "${SELECTED_FINAL95_MODE:-preflight}" = run ]; then
  case "$APP_KEEPER_ROOT" in
    /*) ;;
    *) echo 'APP_KEEPER_ROOT must be an absolute protected keeper in run mode' >&2; exit 2 ;;
  esac
fi

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
KEEPER_LEASE="$ORCH/design/ap2-m2-selected-clean-keeper-main-port-1120-KEEP"
OWNED_RECORD="$ORCH/design"
OLD_DRIVER="$ORCH/design/ap2-m2-selected-clean-keeper-main-port-1120-selected-p1-driver.sh"
SOURCE_COMMON="$ORCH/design/ap2-m2-selected-clean-keeper-main-port-1120-source-common.sh"
PARENT_MEDIA="$ORCH/design/ap2-m2-selected-clean-keeper-main-port-1120-parent-media-central.sh"
LOCKED_GRAPH=${LOCKED_GRAPH:-"$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph"}
LOCKED_GRAPH_ARCHIVE=${LOCKED_GRAPH_ARCHIVE:-"$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar"}
AGENT_REPO=/home/user/peteromallet/astrid-agent
RUNTIME_REPO=/home/user/banodoco/banodoco-workspace-runtime

# Current selected normal-DEV source, not the old013 driver source and not a
# new source authority.
APP_SOURCE_SHA=0cc2583aaf07e89190b9344b5ac82849d6279586
APP_SOURCE_TREE=320e74a93676c781e83885b86ec237b4a1465d80
APP_BASE_SHA=32b74fdea165816226b6f0727a16817a6a1a79c3
APP_BASE_TREE=a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65
SELECTED_SPEC_SHA=2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
HARNESS_SHA=bdd9b30b025c87097a99e5e67117ee01612f50b4f5a7c11f8f8dbe1ddb13f64a
VITE_CONFIG_SHA=5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
PROXY_SHA=93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0

# Exact final95 cohort/environment from the qualified normal014 controls.
AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
PRODUCER_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
PRODUCER_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
MANIFEST_SHA=a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
MANIFEST_COUNT=76
SCHEMA_SHA=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
WIRE_SHA=sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
APP_LOCK_SHA=770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
APP_METADATA_SHA=4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
APP_GENERATED_SHA=c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
APP_TYPES_SHA=f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
APP_SCHEMA_SHA=f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
COMPOSITION_TARBALL_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
PYTHON=/home/user/work/venv-app2-native/bin/python
TEST_TITLE='local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo'
TEST_SPEC='tests/e2e/local/three-products.selected-param-dev.spec.ts'

artifact_version_from_runtime95() {
  RUNTIME_REPO="$RUNTIME_REPO" RUNTIME_SHA="$RUNTIME_SHA" python3 - <<'PY'
import json
import os
import subprocess

repo = os.environ['RUNTIME_REPO']
revision = os.environ['RUNTIME_SHA']
manifest_bytes = subprocess.check_output(
    ['git', '-C', repo, 'show', f'{revision}:contract/artifacts.json']
)
manifest = json.loads(manifest_bytes)
if manifest.get('producer') != 'astrid-runtime':
    raise SystemExit('unexpected Runtime artifact producer')
version = manifest.get('version')
if not isinstance(version, str) or not version.startswith('sha256:'):
    raise SystemExit('Runtime artifact manifest has no valid version')
print(version)
PY
}

ARTIFACT_SHA=$(artifact_version_from_runtime95)

RUN_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/ap2-m2-selected-final95-owned.XXXXXX")
FAILURES="$RUN_ROOT/failures"
CHECK_OUTPUT="$RUN_ROOT/check-output"
mkdir -p "$CHECK_OUTPUT"
: > "$FAILURES"
CHILD_LOG="$RUN_ROOT/selected-child.log"
DURABLE_ROOT=${SELECTED_FINAL95_DURABLE_ROOT:-$ORCH/workers/ap2-m2-selected-failure-retention-owned-0903/artifacts/retained-evidence}
child_started=0
body_started=0
mkdir -p "$RUN_ROOT/browser-output"
: > "$CHILD_LOG"
check_number=0
ACTUAL_NODE_OPTIONS=--max-old-space-size=4096
ACTUAL_TRACE_FILE=${SELECTED_FINAL95_TRACE_FILE:-$RUN_ROOT/actual-preflight.trace}
: > "$ACTUAL_TRACE_FILE"
# Control inherited Node resolution before any helper or graph check can spawn
# Node.  The actual overlay switches NODE_PATH to its private graph below.
export NODE_OPTIONS="$ACTUAL_NODE_OPTIONS" NODE_PATH="$LOCKED_GRAPH/node_modules"

copy_bounded() {
  source=$1
  destination=$2
  limit_bytes=$3
  test -f "$source" || return 1
  size=$(wc -c <"$source") || return 1
  test "$size" -le "$limit_bytes" || return 1
  cp -p -- "$source" "$destination" || return 1
}

write_failure_identity() {
  durable_root=$1
  run_root=$2
  status=$3
  phase=$4
  output_dir=$5
  runner_path=$(realpath "$0" 2>/dev/null || printf '%s' "$0")
  {
    printf '%s\n' 'selected final95 failure evidence v1'
    printf 'runner=%s\n' "$runner_path"
    printf 'runner_sha256=%s\n' "$(sha256sum "$0" | cut -d' ' -f1)"
    printf 'phase=%s\n' "$phase"
    printf 'child_status=%s\n' "$status"
    printf 'child_started=%s\n' "$child_started"
    printf 'body_started=%s\n' "$body_started"
    printf 'source_app_root=%s\n' "$(realpath "$APP_ROOT")"
    printf 'app_head=%s\n' "$APP_SOURCE_SHA"
    printf 'app_tree=%s\n' "$APP_SOURCE_TREE"
    printf 'app_base=%s\n' "$APP_BASE_SHA"
    printf 'app_base_tree=%s\n' "$APP_BASE_TREE"
    printf 'selected_spec_sha256=%s\n' "$SELECTED_SPEC_SHA"
    printf 'harness_sha256=%s\n' "$HARNESS_SHA"
    printf 'vite_config_sha256=%s\n' "$VITE_CONFIG_SHA"
    printf 'discovery_proxy_sha256=%s\n' "$PROXY_SHA"
    printf 'agent_head=%s\n' "$AGENT_SHA"
    printf 'agent_tree=%s\n' "$AGENT_TREE"
    printf 'runtime_head=%s\n' "$RUNTIME_SHA"
    printf 'runtime_tree=%s\n' "$RUNTIME_TREE"
    printf 'producer_head=%s\n' "$PRODUCER_SHA"
    printf 'producer_tree=%s\n' "$PRODUCER_TREE"
    printf 'runtime_artifact=%s\n' "$ARTIFACT_SHA"
    printf 'runtime_manifest_sha256=%s\n' "$MANIFEST_SHA"
    printf 'runtime_schema_sha256=%s\n' "$SCHEMA_SHA"
    printf 'composition_archive_sha256=%s\n' "$COMPOSITION_TARBALL_SHA"
    printf 'node=%s\n' "$(node --version 2>/dev/null || printf unavailable)"
    printf 'npm=%s\n' "$(npm --version 2>/dev/null || printf unavailable)"
    printf 'playwright=%s\n' "$(node -p "require('$LOCKED_GRAPH/node_modules/playwright/package.json').version" 2>/dev/null || printf unavailable)"
    printf 'vite=%s\n' "$(node -p "require('$LOCKED_GRAPH/node_modules/vite/package.json').version" 2>/dev/null || printf unavailable)"
    printf 'playwright_config=playwright.three-products.config.ts\n'
    printf 'playwright_output_dir=%s\n' "$output_dir"
    printf 'dom_present=%s\n' "${dom_present:-false}"
    printf 'error_context_present=%s\n' "${context_present:-false}"
    printf 'trace_present=%s\n' "${trace_present:-false}"
    printf 'dom_retained=%s\n' "${dom_retained:-false}"
    printf 'error_context_retained=%s\n' "${context_retained:-false}"
    printf 'trace_retained=%s\n' "${trace_retained:-false}"
    printf 'child_command=npm run test:e2e:three-products -- --grep %s\n' "$TEST_TITLE"
    printf 'run_root=%s\n' "$run_root"
  } >"$durable_root/identity.txt" || return 1
}

retain_failure_evidence() {
  run_root=$1
  durable_root=$2
  child_log=$3
  status=$4
  phase=PREBODY
  output_dir="$run_root/browser-output"
  test -d "$run_root"
  test "$(realpath "$run_root")" = "$run_root"
  case "$durable_root" in
    /*) ;;
    *) echo 'selected failure evidence root must be absolute' >&2; return 1 ;;
  esac
  durable_parent=$(realpath "$(dirname "$durable_root")")
  test ! -e "$durable_root" || { echo 'selected failure retention refused: durable evidence root already exists' >&2; return 1; }
  test "$durable_parent" != "$run_root"
  case "$durable_parent" in
    "$run_root"/*) echo 'selected failure evidence root must be outside RUN_ROOT' >&2; return 1 ;;
  esac
  mkdir "$durable_root" || return 1
  durable_root=$(realpath "$durable_root")
  test "$durable_root" != "$run_root"
  case "$durable_root" in
    "$run_root"/*) echo 'selected failure evidence root resolved inside RUN_ROOT' >&2; return 1 ;;
  esac
  chmod 700 "$durable_root" || return 1
  copy_bounded "$child_log" "$durable_root/child.log" 10485760 || return 1

  output_files=0
  if test -d "$output_dir"; then
    output_files=$(find -P "$output_dir" -type f -print | wc -l)
  fi
  trace=$(find -P "$output_dir" -type f -name trace.zip -print -quit 2>/dev/null || true)
  context=$(find -P "$output_dir" -type f -name error-context.md -print -quit 2>/dev/null || true)
  dom=$(find -P "$output_dir" -type f \( -name dom.html -o -name dom-snapshot.html -o -name '*.html' \) -print -quit 2>/dev/null || true)
  if test -n "$trace"; then trace_present=true; else trace_present=false; fi
  if test -n "$context"; then context_present=true; else context_present=false; fi
  if test -n "$dom"; then dom_present=true; else dom_present=false; fi
  trace_retained=false
  context_retained=false
  dom_retained=false
  if test "$output_files" -eq 0; then
    phase=PREBODY
  else
    phase=BODY
  fi
  if test -n "$trace" || test -n "$context" || test -n "$dom"; then
    mkdir "$durable_root/browser-output" || return 1
  fi
  if test -n "$dom"; then
    copy_bounded "$dom" "$durable_root/browser-output/dom.html" 5242880 || return 1
    dom_retained=true
  fi
  if test -n "$context"; then
    copy_bounded "$context" "$durable_root/browser-output/error-context.md" 1048576 || return 1
    context_retained=true
  fi
  if test -n "$trace"; then
    copy_bounded "$trace" "$durable_root/browser-output/trace.zip" 52428800 || return 1
    trace_retained=true
  fi
  write_failure_identity "$durable_root" "$run_root" "$status" "$phase" "$output_dir" || return 1
  if ! (
    cd "$durable_root"
    find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | while IFS= read -r path; do
      sha256sum -- "$path"
    done
  ) >"$durable_root/SHA256SUMS"; then
    return 1
  fi
  test -s "$durable_root/SHA256SUMS" || return 1
}

cleanup() {
  status=$?
  trap - EXIT HUP INT TERM
  retention_status=0
  if test "$status" -ne 0; then
    if retain_failure_evidence "$(realpath "$RUN_ROOT")" "$DURABLE_ROOT" "$CHILD_LOG" "$status"; then
      :
    else
      retention_status=$?
      printf 'selected failure retention FAILED status=%s run_root=%s\n' "$retention_status" "$RUN_ROOT" >&2
    fi
  fi
  rm -rf -- "$RUN_ROOT"
  if test "$retention_status" -ne 0; then
    exit 1
  fi
  exit "$status"
}
on_signal() {
  signal_status=$1
  trap - "$2"
  exit "$signal_status"
}
trap cleanup EXIT
trap 'on_signal 129 HUP' HUP
trap 'on_signal 130 INT' INT
trap 'on_signal 143 TERM' TERM

check() {
  label=$1
  shift
  check_number=$((check_number + 1))
  output="$CHECK_OUTPUT/$check_number"
  if "$@" >"$output" 2>&1; then
    echo "PASS  $label"
    return 0
  fi
  echo "FAIL  $label"
  sed -n '1,12p' "$output" | sed 's/^/      /'
  printf '%s\n' "$label" >> "$FAILURES"
  return 1
}

assert_equal() {
  test "${1-}" = "${2-}"
}

verify_app_source() {
  app_root=$(CDPATH= cd -- "$APP_ROOT" && pwd)
  test "$(realpath "$app_root")" = "$app_root"
  test "$(realpath "$(git -C "$app_root" rev-parse --show-toplevel)")" = "$app_root"
  test "$(git -C "$app_root" rev-parse HEAD)" = "$APP_SOURCE_SHA"
  test "$(git -C "$app_root" rev-parse 'HEAD^{tree}')" = "$APP_SOURCE_TREE"
  git -C "$app_root" merge-base --is-ancestor "$APP_BASE_SHA" HEAD
  test "$(git -C "$app_root" show -s --format=%T "$APP_BASE_SHA")" = "$APP_BASE_TREE"
  test -z "$(git -C "$app_root" status --porcelain=v1 --untracked-files=all)"
  test "$(sha256sum "$app_root/$TEST_SPEC" | cut -d' ' -f1)" = "$SELECTED_SPEC_SHA"
  test "$(sha256sum "$app_root/tests/e2e/local/support/harness.ts" | cut -d' ' -f1)" = "$HARNESS_SHA"
  test "$(sha256sum "$app_root/config/vite/vite.config.ts" | cut -d' ' -f1)" = "$VITE_CONFIG_SHA"
  test "$(sha256sum "$app_root/scripts/runtime-discovery-proxy.mjs" | cut -d' ' -f1)" = "$PROXY_SHA"
}

verify_service_app_source() {
  app_root=$(CDPATH= cd -- "$APP_ROOT" && pwd)
  test "$(realpath "$app_root")" = "$app_root"
  test "$(realpath "$(git -C "$app_root" rev-parse --show-toplevel)")" = "$app_root"
  test "$(git -C "$app_root" rev-parse 'HEAD^{tree}')" = "$APP_SOURCE_TREE"
  git -C "$app_root" merge-base --is-ancestor "$APP_BASE_SHA" HEAD
  test "$(git -C "$app_root" show -s --format=%T "$APP_BASE_SHA")" = "$APP_BASE_TREE"
  test -z "$(git -C "$app_root" status --porcelain=v1 --untracked-files=all)"
  test "$(sha256sum "$app_root/$TEST_SPEC" | cut -d' ' -f1)" = "$SELECTED_SPEC_SHA"
  test "$(sha256sum "$app_root/tests/e2e/local/support/harness.ts" | cut -d' ' -f1)" = "$HARNESS_SHA"
  test "$(sha256sum "$app_root/config/vite/vite.config.ts" | cut -d' ' -f1)" = "$VITE_CONFIG_SHA"
  test "$(sha256sum "$app_root/scripts/runtime-discovery-proxy.mjs" | cut -d' ' -f1)" = "$PROXY_SHA"
}

verify_protected_keeper() {
  keeper_root=$(CDPATH= cd -- "$APP_KEEPER_ROOT" && pwd)
  app_root=$(CDPATH= cd -- "$APP_ROOT" && pwd)
  test "$keeper_root" != "$app_root"
  test "$(realpath "$keeper_root")" = "$keeper_root"
  test "$(realpath "$(git -C "$keeper_root" rev-parse --show-toplevel)")" = "$keeper_root"
  test "$(git -C "$keeper_root" rev-parse HEAD)" = "$APP_SOURCE_SHA"
  test "$(git -C "$keeper_root" rev-parse 'HEAD^{tree}')" = "$APP_SOURCE_TREE"
  test -z "$(git -C "$keeper_root" status --porcelain=v1 --untracked-files=all)"
  test -f "$KEEPER_LEASE"
  test ! -L "$KEEPER_LEASE"
}

verify_keep_and_normal_link() {
  test -f "$KEEPER_LEASE"
  test ! -s "$KEEPER_LEASE"
  test -f "$APP_ROOT/runtime.lock.json"
  test "$(realpath "$APP_ROOT")" = "$APP_ROOT"
  test "$(git -C "$APP_ROOT" rev-parse --show-toplevel)" = "$APP_ROOT"
  test "$(sha256sum "$APP_ROOT/runtime.lock.json" | cut -d' ' -f1)" = "$APP_LOCK_SHA"
  test "$(cd "$APP_ROOT" && node -e 'console.log(JSON.parse(require("fs").readFileSync("runtime.lock.json", "utf8")).source_commit)' </dev/null)" = "$RUNTIME_SHA"
  test "$(sha256sum "$APP_ROOT/src/integrations/runtime/generated-contract-metadata.ts" | cut -d' ' -f1)" = "$APP_METADATA_SHA"
  test "$(sha256sum "$APP_ROOT/src/integrations/runtime/generated.ts" | cut -d' ' -f1)" = "$APP_GENERATED_SHA"
  test "$(sha256sum "$APP_ROOT/src/integrations/runtime/timeline-commit-types.ts" | cut -d' ' -f1)" = "$APP_TYPES_SHA"
  test "$(sha256sum "$APP_ROOT/vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json" | cut -d' ' -f1)" = "$APP_SCHEMA_SHA"
}

verify_source_refs() {
  test "$(git -C "$AGENT_REPO" rev-parse "$AGENT_SHA^{commit}")" = "$AGENT_SHA"
  test "$(git -C "$AGENT_REPO" rev-parse "$AGENT_SHA^{tree}")" = "$AGENT_TREE"
  test "$(git -C "$RUNTIME_REPO" rev-parse "$RUNTIME_SHA^{commit}")" = "$RUNTIME_SHA"
  test "$(git -C "$RUNTIME_REPO" rev-parse "$RUNTIME_SHA^{tree}")" = "$RUNTIME_TREE"
  test "$(git -C "$RUNTIME_REPO" rev-parse "$PRODUCER_SHA^{commit}")" = "$PRODUCER_SHA"
  test "$(git -C "$RUNTIME_REPO" rev-parse "$PRODUCER_SHA^{tree}")" = "$PRODUCER_TREE"
  git -C "$RUNTIME_REPO" merge-base --is-ancestor "$PRODUCER_SHA" "$RUNTIME_SHA"
  test -z "$(git -C "$AGENT_REPO" status --porcelain=v1 2>/dev/null)"
  test -z "$(git -C "$RUNTIME_REPO" status --porcelain=v1 2>/dev/null)"
}

verify_owned_artifacts() {
  AGENT_REPO="$AGENT_REPO" RUNTIME_REPO="$RUNTIME_REPO" AGENT_SHA="$AGENT_SHA" RUNTIME_SHA="$RUNTIME_SHA" \
    PRODUCER_SHA="$PRODUCER_SHA" EXPECTED_MANIFEST="$MANIFEST_SHA" EXPECTED_ARTIFACT="$ARTIFACT_SHA" \
    EXPECTED_SCHEMA="$SCHEMA_SHA" EXPECTED_COUNT="$MANIFEST_COUNT" python3 - <<'PY'
import hashlib, json, os, subprocess

agent = os.environ['AGENT_REPO']
runtime = os.environ['RUNTIME_REPO']
agent_sha = os.environ['AGENT_SHA']
runtime_sha = os.environ['RUNTIME_SHA']
producer_sha = os.environ['PRODUCER_SHA']

def show(repo, rev, path):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{rev}:{path}'])

def digest(data):
    return hashlib.sha256(data).hexdigest()

manifest_bytes = show(runtime, runtime_sha, 'contract/artifacts.json')
manifest = json.loads(manifest_bytes)
assert manifest['producer'] == 'astrid-runtime'
assert manifest['version'] == os.environ['EXPECTED_ARTIFACT']
assert len(manifest['artifacts']) == int(os.environ['EXPECTED_COUNT'])
assert digest(manifest_bytes) == os.environ['EXPECTED_MANIFEST']
for relative, expected in manifest['artifacts'].items():
    candidate = show(runtime, runtime_sha, relative)
    original = show(runtime, producer_sha, relative)
    assert candidate == original, relative
    assert f'sha256:{digest(candidate)}' == expected, relative

runtime_schema = show(runtime, runtime_sha, 'contract/schemas/edit-command.json')
agent_schema = show(agent, agent_sha, 'astrid/core/timeline/schema/edit-command.schema.json')
assert digest(runtime_schema) == os.environ['EXPECTED_SCHEMA']
assert agent_schema == runtime_schema
print(f"artifacts={len(manifest['artifacts'])} manifest={digest(manifest_bytes)} schema={digest(runtime_schema)}")
PY
}

verify_actual_artifact_version() {
  expected_artifact=$(artifact_version_from_runtime95) || return 1
  test "$ARTIFACT_SHA" = "$expected_artifact"
}

verify_planted_artifact_version_refusal() {
  saved_artifact=$ARTIFACT_SHA
  ARTIFACT_SHA=sha256:planted-wrong-artifact-version
  if verify_actual_artifact_version; then
    ARTIFACT_SHA=$saved_artifact
    return 1
  fi
  ARTIFACT_SHA=$saved_artifact
}

verify_owned_graph() {
  test -d "$LOCKED_GRAPH/node_modules"
  test -f "$LOCKED_GRAPH_ARCHIVE"
  test "$(realpath "$LOCKED_GRAPH/node_modules")" = "$LOCKED_GRAPH/node_modules"
  test "$(sha256sum "$LOCKED_GRAPH_ARCHIVE" | cut -d' ' -f1)" = "$GRAPH_ARCHIVE_SHA"
  test "$(node -p "require('$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
  test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | sha256sum | cut -d' ' -f1)" = "$COMPOSITION_TARBALL_SHA"
  test -z "$(find -P "$LOCKED_GRAPH" -type f -perm /022 -print -quit)"
  LOCKED_GRAPH="$LOCKED_GRAPH" node - <<'JS'
const { createRequire } = require('node:module');
const requireFromGraph = createRequire(`${process.env.LOCKED_GRAPH}/package.json`);
const composition = requireFromGraph('@banodoco/timeline-composition/package.json');
const vite = requireFromGraph('vite/package.json');
const vitest = requireFromGraph('vitest/package.json');
const playwright = requireFromGraph('playwright/package.json');
if (composition.version !== '0.0.13' || vite.version !== '5.4.21'
  || vitest.version !== '4.1.5' || playwright.version !== '1.60.0') process.exit(1);
JS
  test "$(node --version)" = v22.22.0
}

verify_scripts_and_scope() {
  test "$(sha256sum "$OLD_DRIVER" | cut -d' ' -f1)" = a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
  test "$(sha256sum "$SOURCE_COMMON" | cut -d' ' -f1)" = 96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
  test "$(sha256sum "$PARENT_MEDIA" | cut -d' ' -f1)" = 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
  sh -n "$OLD_DRIVER"
  sh -n "$SOURCE_COMMON"
  node --check "$APP_ROOT/scripts/runtime-discovery-proxy.mjs"
  grep -F 'ASTRID_RUNTIME_OPERATION_ORIGIN: this.devOrigin' "$APP_ROOT/tests/e2e/local/support/harness.ts" >/dev/null
  grep -F 'ASTRID_WORKSPACE_DISCOVERY: discoveryPath' "$APP_ROOT/tests/e2e/local/support/harness.ts" >/dev/null
  grep -F 'WORKSPACE_RUNTIME_TOKEN_FILE: this.credentialPath' "$APP_ROOT/tests/e2e/local/support/harness.ts" >/dev/null
  grep -F 'ASTRID_RUNTIME_CREDENTIAL: credentialFile' "$APP_ROOT/tests/e2e/local/support/harness.ts" >/dev/null
  grep -F "PRODUCT_SCOPES = ['handshake', 'projects:read', 'projects:write', 'tasks:read', 'tasks:write', 'objects:read', 'objects:write']" "$APP_ROOT/tests/e2e/local/support/harness.ts" >/dev/null
  grep -F 'allowedOrigin: process.env.ASTRID_RUNTIME_OPERATION_ORIGIN' "$APP_ROOT/scripts/runtime-discovery-proxy.mjs" >/dev/null
}

verify_selected_contract() {
  test "$(grep -cF "test('$TEST_TITLE'" "$APP_ROOT/$TEST_SPEC")" = 1
  for literal in \
    'const CEILING = { timeout: 90_000 };' \
    'expectConnected' \
    "scope: 'worker', timeout: 240_000" \
    'await harness.startSelectedParamDevServer();' \
    'page.goto(`${harness.devOrigin}/tools/video-editor`);' \
    'selected.p1DocumentPin' \
    'advanceSelectedParamAndRemoveSource' \
    "page.reload();" \
    'connectionreset' \
    'idempotency-key' \
    'timeline.inverse' \
    'expect(legacyPosts).toEqual([])'
  do
    grep -F "$literal" "$APP_ROOT/$TEST_SPEC" >/dev/null
  done
  test "$(grep -cF 'await page.reload();' "$APP_ROOT/$TEST_SPEC")" = 2
  test "$(grep -cF 'await expectConnected(page);' "$APP_ROOT/$TEST_SPEC")" = 3
}

verify_lock_disk_and_copy_controls() {
  test -x "$PYTHON"
  test -f /home/user/work/.app-m1-browser.lock || :
  flock -n /home/user/work/.app-m1-browser.lock -c ':'
  free_tmp=$(df -Pk /tmp | awk 'NR==2 {print $4}')
  free_work=$(df -Pk /home/user/work | awk 'NR==2 {print $4}')
  test "$free_tmp" -ge 10485760
  test "$free_work" -ge 10485760
  test "$(grep -cF 'cp -a "$APP_ROOT"/. "$APP_OVERLAY"/.' "$0" 2>/dev/null || true)" = 1
  test "$(grep -cF 'prepare_private_node_graph' "$0")" -ge 1
  test "$(grep -cF 'rm -f "$APP_OVERLAY/node_modules"' "$0")" -ge 1
}

expect_refusal() {
  expected=$1
  observed=$2
  if assert_equal "$expected" "$observed"; then
    return 1
  fi
  return 0
}

require_one_list() {
  test "${1-}" = '1 test in 1 file'
}

verify_planted_refusals() {
  expect_refusal final95 old013
  expect_refusal "$AGENT_TREE" 236c3e57e0265c52b81ba8085de3193026176bff
  expect_refusal "$APP_LOCK_SHA" a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
  expect_refusal "$LOCKED_GRAPH" /tmp/wrong-graph
  expect_refusal 'node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list' 'node node_modules/playwright/cli.js test --config wrong.config.ts --list'
  if require_one_list '0 tests'; then
    return 1
  fi
}

run_cheap_preflight() {
  echo "owned final95 selected CHEAP preflight: source=$APP_SOURCE_SHA tree=$APP_SOURCE_TREE"
  check 'final App source, ancestry, selected spec and clean checkout' verify_app_source || :
  check 'separate clean detached keeper and protected lease' verify_protected_keeper || :
  check 'KEEP marker and clean normal App/runtime link' verify_keep_and_normal_link || :
  check 'final95 source refs, trees, ancestry and clean source repos' verify_source_refs || :
  check 'final95 76-artifact manifest, producer bytes and schema6ba' verify_owned_artifacts || :
  check 'locked graph, Composition13/9412, Node/Vite/Vitest/Playwright resolution' verify_owned_graph || :
  check 'copied driver/helper hashes, syntax, DEV proxy/origin/credential scope' verify_scripts_and_scope || :
  check 'exact selected title/spec, budgets, argv-related assertions and reload count' verify_selected_contract || :
  check 'local lock, disk floor, private graph and single App-copy controls' verify_lock_disk_and_copy_controls || :
  check 'offline wrong role/tree/pin/path/argv/zero-test refusal probes' verify_planted_refusals || :
  check 'planted wrong artifact version is refused by the actual guard' verify_planted_artifact_version_refusal || :

  # This is the only preflight operation that enters the private App overlay.
  # It collects Playwright's one-test list and never starts Vite, Runtime, a
  # browser, a daemon, a socket listener, a build, or the actual test.
  NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
    NORMAL014_LOCKED_GRAPH="$LOCKED_GRAPH" NORMAL014_LOCKED_GRAPH_ARCHIVE="$LOCKED_GRAPH_ARCHIVE" \
    . "$SOURCE_COMMON"
  restore_owned_tuple
  prepare_private_node_graph "$LOCKED_GRAPH/node_modules" "$RUN_ROOT/private-node-modules" >"$CHECK_OUTPUT/private-graph" 2>&1 || {
    echo 'FAIL  private graph preparation and exact list1';
    sed -n '1,12p' "$CHECK_OUTPUT/private-graph" | sed 's/^/      /';
    printf '%s\n' 'private graph preparation and exact list1' >> "$FAILURES";
  }
  if test -d "$RUN_ROOT/private-node-modules"; then
    APP_OVERLAY="$RUN_ROOT/app"
    mkdir -p "$APP_OVERLAY"
    cp -a "$APP_ROOT"/. "$APP_OVERLAY"/
    rm -f "$APP_OVERLAY/node_modules"
    ln -s "$RUN_ROOT/private-node-modules" "$APP_OVERLAY/node_modules"
    check 'private App overlay and exact selected Playwright list1' verify_private_list || :
  fi

  if test -s "$FAILURES"; then
    echo
    echo 'CHEAP PREFLIGHT REFUSED; all prerequisite failures:'
    sed 's/^/  - /' "$FAILURES"
    return 1
  fi
  echo 'CHEAP PREFLIGHT PASS: all prerequisites and offline refusal probes passed'
}

verify_private_list() {
  test "$(realpath "$APP_OVERLAY/node_modules")" = "$RUN_ROOT/private-node-modules" || { echo 'actual list1: private node_modules link mismatch' >&2; return 1; }
  test "$(realpath "$RUN_ROOT/private-node-modules/@banodoco/timeline-composition")" = "$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition" || { echo 'actual list1: Composition link mismatch' >&2; return 1; }
  test "$(node -p "require('$APP_OVERLAY/node_modules/vite/package.json').version")" = 5.4.21 || { echo 'actual list1: Vite version mismatch' >&2; return 1; }
  test "$(node -p "require('$APP_OVERLAY/node_modules/playwright/package.json').version")" = 1.60.0 || { echo 'actual list1: Playwright version mismatch' >&2; return 1; }
  list_output="$RUN_ROOT/list1.txt"
  if ! (cd "$APP_OVERLAY" && NODE_PATH="$RUN_ROOT/private-node-modules" node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list) >"$list_output" 2>&1; then
    sed -n '1,80p' "$list_output" >&2
    return 1
  fi
  test "$(grep -cF "$TEST_TITLE" "$list_output")" = 1
  grep -F '1 test in 1 file' "$list_output" >/dev/null
  ! grep -Eq '0 tests|No tests found' "$list_output"
}

verify_actual_node_graph() {
  test "$(realpath "$APP_OVERLAY/node_modules")" = "$RUN_ROOT/private-node-modules"
  test "$(node -p "require('$APP_OVERLAY/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
  NODE_PATH="$RUN_ROOT/private-node-modules" NODE_OPTIONS="$ACTUAL_NODE_OPTIONS" \
    APP_OVERLAY="$APP_OVERLAY" LOCKED_GRAPH="$LOCKED_GRAPH" node --input-type=module - <<'JS'
import { createRequire } from 'node:module';
import { dirname } from 'node:path';
import { realpathSync } from 'node:fs';

const require = createRequire(`${process.env.APP_OVERLAY}/package.json`);
const expected = {
  vite: '5.4.21',
  vitest: '4.1.5',
  playwright: '1.60.0',
  composition: '0.0.13',
};
const resolved = {
  vite: require.resolve('vite/package.json'),
  vitest: require.resolve('vitest/package.json'),
  playwright: require.resolve('playwright/package.json'),
  composition: require.resolve('@banodoco/timeline-composition/package.json'),
};
for (const [name, version] of Object.entries(expected)) {
  const packagePath = resolved[name];
  const physicalPath = realpathSync(packagePath);
  const packageJson = (await import(`file://${physicalPath}`, { with: { type: 'json' } })).default;
  if (packageJson.version !== version) throw new Error(`${name} resolved ${packageJson.version}`);
  const graphPackagePath = realpathSync(`${process.env.LOCKED_GRAPH}/node_modules/${name === 'composition' ? '@banodoco/timeline-composition' : name}/package.json`);
  if (physicalPath !== graphPackagePath) {
    throw new Error(`${name} resolved outside the locked graph mapping: ${physicalPath}`);
  }
}
const compositionPackage = realpathSync(resolved.composition);
const composition = await import(`file://${dirname(compositionPackage)}/dist/evaluation.js`);
if (typeof composition.computeMediaTrim !== 'function') throw new Error('Composition ESM entry missing');
JS
}

trace_actual() {
  printf '%s\n' "$1" >> "$ACTUAL_TRACE_FILE"
}

restore_owned_tuple() {
  AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
  AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
  RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
  RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
  PRODUCER_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
  PRODUCER_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
  ARTIFACT_SHA=$(artifact_version_from_runtime95)
  MANIFEST_SHA=a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
  MANIFEST_COUNT=76
  SCHEMA_SHA=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
  LOCKED_GRAPH=${LOCKED_GRAPH:-"$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph"}
  LOCKED_GRAPH_ARCHIVE=${LOCKED_GRAPH_ARCHIVE:-"$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar"}
}

run_actual() {
  # The actual path is deliberately unreachable from the default invocation.
  # It retains the original selected argv/title/spec and the qualified parent
  # private-source/graph/copy controls for the central service.
  NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
    NORMAL014_LOCKED_GRAPH="$LOCKED_GRAPH" NORMAL014_LOCKED_GRAPH_ARCHIVE="$LOCKED_GRAPH_ARCHIVE" \
    . "$SOURCE_COMMON"
  restore_owned_tuple
  # Use the runner's already-created root.  Do not call normal014_start_run:
  # the shared helper's trap and root would otherwise replace this runner's
  # single custody/cleanup root.
  run_root=$RUN_ROOT
  normal014_use_private_tmp
  runtime_data_root="$run_root/runtime-data"
  runtime_realm_root="$run_root/runtime-realm"
  runtime_realm_id="selected-final95-$$"
  runtime_door_port=$((18000 + $$ % 1000))
  source_manifest="$run_root/source-manifest.json"
  mkdir -p "$run_root/sources" "$run_root/tmp" "$run_root/npm-cache" "$run_root/pw-cache" "$run_root/browser-output" "$run_root/vite-cache" "$runtime_data_root"
  prepare_sources "$run_root/sources"
  runtime="$run_root/sources/runtime-95"
  agent="$run_root/sources/agent-6ef"
  producer="$run_root/sources/producer-95"
  trace_actual source_refs
  verify_source_refs
  trace_actual artifacts
  verify_owned_artifacts
  trace_actual locked_graph
  verify_owned_graph
  prepare_private_python "$run_root"
  runtime_environment=$(CDPATH= cd -- "$(dirname -- "$(dirname -- "$NORMAL014_PYTHON")")" && pwd)
  printf '%s\n' '{' '  "profile": "astrid",' "  \"runtime_checkout\": \"$runtime\"," "  \"source_checkout\": \"$agent\"," "  \"runtime_environment\": \"$runtime_environment\"" '}' > "$source_manifest"
  export ASTRID_RUNTIME_DATA_ROOT="$runtime_data_root" ASTRID_RUNTIME_SOURCE_MANIFEST="$source_manifest" ASTRID_RUNTIME_DOOR_PORT="$runtime_door_port"
  unset ASTRID_RUNTIME_LAUNCHER
  export PYTHONPATH="$runtime:$runtime/packages/python:$agent${PYTHONPATH:+:$PYTHONPATH}"
  "$NORMAL014_PYTHON" -m astrid_runtime workspace create --profile astrid --data-root "$runtime_data_root" --realm-root "$runtime_realm_root" --realm-id "$runtime_realm_id" --display-name 'selected DEV private workspace' --source-manifest "$source_manifest" --json > "$run_root/workspace-create.json"
  "$NORMAL014_PYTHON" -m astrid_runtime workspace inspect --data-root "$runtime_data_root" --realm-root "$runtime_realm_root" --expected-realm-id "$runtime_realm_id" --json > "$run_root/workspace-inspect.json"
  APP_OVERLAY="$run_root/app"
  mkdir -p "$APP_OVERLAY"
  export ASTRID_CHECKOUT="$agent" ASTRID_PYTHON="$NORMAL014_PYTHON" ASTRID_RUNTIME_CHECKOUT="$runtime" ASTRID_RUNTIME_PYTHON="$NORMAL014_PYTHON"
  export TIMELINE_BUNDLE_AGENT_HEAD="$AGENT_SHA" TIMELINE_BUNDLE_RUNTIME_HEAD="$RUNTIME_SHA" PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
  export PWTEST_CACHE_DIR="$run_root/pw-cache" PLAYWRIGHT_OUTPUT_DIR="$run_root/browser-output" npm_config_cache="$run_root/npm-cache" VITE_CACHE_DIR="$run_root/vite-cache" TMPDIR="$run_root/tmp" PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 NODE_OPTIONS="$ACTUAL_NODE_OPTIONS" NODE_PATH="$run_root/private-node-modules"
  export SELECTED_FINAL95_RUN_ROOT="$run_root" SELECTED_FINAL95_TRACE_FILE="$ACTUAL_TRACE_FILE"
  unset ASTRID_PUBLIC_CHECKOUT ASTRID_APP_DIRECT_DIST
  trace_actual scripts_scope
  verify_scripts_and_scope
  trace_actual selected_contract
  verify_selected_contract
  # These are the final source/keeper checks on the actual input.  They stay
  # directly adjacent to the copy so a service cannot swap a tree after the
  # earlier setup checks and before the overlay is made.
  trace_actual service_source
  verify_service_app_source
  trace_actual protected_keeper
  verify_protected_keeper
  trace_actual keep_and_normal_link
  verify_keep_and_normal_link
  cp -a "$APP_ROOT"/. "$APP_OVERLAY"/.
  rm -f "$APP_OVERLAY/node_modules"
  prepare_private_node_graph "$LOCKED_GRAPH/node_modules" "$run_root/private-node-modules"
  ln -s "$run_root/private-node-modules" "$APP_OVERLAY/node_modules"
  cd "$APP_OVERLAY"
  trace_actual node_graph
  verify_actual_node_graph
  trace_actual list1
  verify_private_list
  trace_actual artifact_version
  verify_actual_artifact_version
  trace_actual launch
  if [ -n "${SELECTED_FINAL95_LAUNCH_STUB:-}" ]; then
    command -v "$SELECTED_FINAL95_LAUNCH_STUB" >/dev/null
    child_started=1
    body_started=1
    set +e
    "$SELECTED_FINAL95_LAUNCH_STUB" >"$CHILD_LOG" 2>&1
    child_status=$?
    set -e
    return "$child_status"
  fi
  child_started=1
  set +e
  npm run build:hosted >"$CHILD_LOG" 2>&1
  child_status=$?
  if test "$child_status" -eq 0; then
    test -f dist/index.html || child_status=$?
  fi
  if test "$child_status" -eq 0; then
    body_started=1
    flock -w 600 /home/user/work/.app-m1-browser.lock npm run test:e2e:three-products -- --grep "$TEST_TITLE" >>"$CHILD_LOG" 2>&1
    child_status=$?
  fi
  set -e
  return "$child_status"
}

MODE=${SELECTED_FINAL95_MODE:-preflight}
case "$MODE" in
  preflight) run_cheap_preflight ;;
  run) run_actual ;;
  *) echo "unsupported SELECTED_FINAL95_MODE: $MODE (expected preflight or run)" >&2; exit 2 ;;
esac
