#!/bin/sh
set -eu

APP_ROOT=${1:?usage: $0 APP_ROOT}
case "$APP_ROOT" in
  /*) ;;
  *) echo 'APP_ROOT must be absolute' >&2; exit 2 ;;
esac
test -f "$APP_ROOT/package.json"
test -z "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)"

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
LOCKED_GRAPH="$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph"
LOCKED_GRAPH_ARCHIVE="$ORCH/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar"
AGENT_REPO=/home/user/peteromallet/astrid-agent
RUNTIME_REPO=/home/user/banodoco/banodoco-workspace-runtime
AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55
AGENT_TREE=236c3e57e0265c52b81ba8085de3193026176bff
RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a
RUNTIME_TREE=7ab412cc4bcbe517efcfa806e092336390312e18
GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
COMPOSITION_TARBALL_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
PYTHON=/home/user/work/venv-app2-native/bin/python
TEST_TITLE='local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo'

test -d "$LOCKED_GRAPH/node_modules"
test -f "$LOCKED_GRAPH_ARCHIVE"
test -x "$PYTHON"
test "$(sha256sum "$LOCKED_GRAPH_ARCHIVE" | cut -d' ' -f1)" = "$GRAPH_ARCHIVE_SHA"
test "$(node -p "require('$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | sha256sum | cut -d' ' -f1)" = "$COMPOSITION_TARBALL_SHA"
test "$(git -C "$AGENT_REPO" rev-parse "$AGENT_SHA^{commit}")" = "$AGENT_SHA"
test "$(git -C "$AGENT_REPO" rev-parse "$AGENT_SHA^{tree}")" = "$AGENT_TREE"
test "$(git -C "$RUNTIME_REPO" rev-parse "$RUNTIME_SHA^{commit}")" = "$RUNTIME_SHA"
test "$(git -C "$RUNTIME_REPO" rev-parse "$RUNTIME_SHA^{tree}")" = "$RUNTIME_TREE"

RUN_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/ap2-m2-selected-p1.XXXXXX")
TRACE_DEST="$ORCH/workers/ap2-m2-selected-draft-p1-review-gate/central-trace"
RUN_LOG="$RUN_ROOT/driver.stderr"
# The frozen Agent asks the neutral Runtime to start an already-selected workspace.
# Create that workspace through Runtime's own command in this per-run realm; do
# not synthesize catalog/history state or let the fixture fall back to a shared
# user workspace.
RUNTIME_DATA_ROOT="$RUN_ROOT/runtime-data"
RUNTIME_REALM_ROOT="$RUN_ROOT/runtime-realm"
RUNTIME_REALM_ID="selected-p1-$$"
RUNTIME_DOOR_PORT=$((18000 + $$ % 1000))
SOURCE_MANIFEST="$RUN_ROOT/source-manifest.json"
exec 3>&2
cleanup() {
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$status" -ne 0 ]; then
    rm -rf "$TRACE_DEST"
    if [ -d "$RUN_ROOT/browser-output" ]; then
      cp -a "$RUN_ROOT/browser-output" "$TRACE_DEST"
    else
      mkdir -p "$TRACE_DEST"
    fi
    if [ -f "$RUN_LOG" ]; then
      cp "$RUN_LOG" "$TRACE_DEST/driver.stderr"
      cat "$RUN_LOG" >&3
    fi
    echo "selected central trace retained at $TRACE_DEST" >&3
  fi
  rm -rf "$RUN_ROOT"
  exec 2>&3 3>&-
  exit "$status"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$RUN_ROOT/sources" "$RUN_ROOT/tmp" \
  "$RUN_ROOT/npm-cache" "$RUN_ROOT/pw-cache" "$RUN_ROOT/browser-output" "$RUN_ROOT/vite-cache" \
  "$RUNTIME_DATA_ROOT"
exec 2>"$RUN_LOG"

git clone --quiet --shared --no-checkout "$AGENT_REPO" "$RUN_ROOT/sources/agent"
git -C "$RUN_ROOT/sources/agent" checkout --quiet --detach "$AGENT_SHA"
test "$(git -C "$RUN_ROOT/sources/agent" rev-parse HEAD)" = "$AGENT_SHA"
test "$(git -C "$RUN_ROOT/sources/agent" show -s --format=%T HEAD)" = "$AGENT_TREE"
test -z "$(git -C "$RUN_ROOT/sources/agent" status --porcelain=v1 --untracked-files=all)"

git clone --quiet --shared --no-checkout "$RUNTIME_REPO" "$RUN_ROOT/sources/runtime"
git -C "$RUN_ROOT/sources/runtime" checkout --quiet --detach "$RUNTIME_SHA"
test "$(git -C "$RUN_ROOT/sources/runtime" rev-parse HEAD)" = "$RUNTIME_SHA"
test "$(git -C "$RUN_ROOT/sources/runtime" show -s --format=%T HEAD)" = "$RUNTIME_TREE"
test -z "$(git -C "$RUN_ROOT/sources/runtime" status --porcelain=v1 --untracked-files=all)"

# Use the exact pinned Agent/Runtime checkouts and Python launcher the fixture
# exports below. Runtime owns creation, identity, and readiness of this realm.
printf '%s\n' \
  '{' \
  '  "profile": "astrid",' \
  "  \"runtime_checkout\": \"$RUN_ROOT/sources/runtime\"," \
  "  \"source_checkout\": \"$RUN_ROOT/sources/agent\"," \
  "  \"runtime_environment\": \"$(dirname "$(dirname "$PYTHON")")\"" \
  '}' > "$SOURCE_MANIFEST"
export ASTRID_RUNTIME_DATA_ROOT="$RUNTIME_DATA_ROOT"
export ASTRID_RUNTIME_SOURCE_MANIFEST="$SOURCE_MANIFEST"
export ASTRID_RUNTIME_DOOR_PORT="$RUNTIME_DOOR_PORT"
unset ASTRID_RUNTIME_LAUNCHER
export PYTHONPATH="$RUN_ROOT/sources/runtime:$RUN_ROOT/sources/runtime/packages/python:$RUN_ROOT/sources/agent${PYTHONPATH:+:$PYTHONPATH}"

"$PYTHON" -m astrid_runtime workspace create \
  --profile astrid \
  --data-root "$RUNTIME_DATA_ROOT" \
  --realm-root "$RUNTIME_REALM_ROOT" \
  --realm-id "$RUNTIME_REALM_ID" \
  --display-name "selected DEV private workspace" \
  --source-manifest "$SOURCE_MANIFEST" \
  --json > "$RUN_ROOT/workspace-create.json"

"$PYTHON" -m astrid_runtime workspace inspect \
  --data-root "$RUNTIME_DATA_ROOT" \
  --realm-root "$RUNTIME_REALM_ROOT" \
  --expected-realm-id "$RUNTIME_REALM_ID" \
  --json > "$RUN_ROOT/workspace-inspect.json"
"$PYTHON" - "$RUN_ROOT/workspace-inspect.json" "$RUNTIME_REALM_ID" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
assert payload["ok"] is True
assert payload["state"] == "configured"
assert payload["realm_id"] == sys.argv[2]
assert payload["inspection"]["checks"]["realm_identity"]["ok"] is True
PY

if [ "${SELECTED_WORKSPACE_PREFLIGHT_ONLY:-0}" = 1 ]; then
  echo "selected DEV private workspace preflight: ready"
  exit 0
fi

# Reuse the reviewed private graph builder; it symlinks package contents read-only
# and creates only private bin links. Vite/Playwright caches stay below RUN_ROOT.
. "$ORCH/design/normal014-source-common.sh"
prepare_private_node_graph "$LOCKED_GRAPH/node_modules" "$RUN_ROOT/private-node-modules"
test "$(realpath "$RUN_ROOT/private-node-modules")" = "$RUN_ROOT/private-node-modules"

APP_OVERLAY="$RUN_ROOT/app"
mkdir -p "$APP_OVERLAY"
cp -a "$APP_ROOT"/. "$APP_OVERLAY"/
rm -f "$APP_OVERLAY/node_modules"
ln -s "$RUN_ROOT/private-node-modules" "$APP_OVERLAY/node_modules"
test "$(realpath "$APP_OVERLAY/node_modules")" = "$RUN_ROOT/private-node-modules"

export ASTRID_CHECKOUT="$RUN_ROOT/sources/agent"
export ASTRID_PYTHON="$PYTHON"
export ASTRID_RUNTIME_CHECKOUT="$RUN_ROOT/sources/runtime"
export ASTRID_RUNTIME_PYTHON="$PYTHON"
export TIMELINE_BUNDLE_AGENT_HEAD="$AGENT_SHA"
export TIMELINE_BUNDLE_RUNTIME_HEAD="$RUNTIME_SHA"
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
export PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
export PWTEST_CACHE_DIR="$RUN_ROOT/pw-cache"
export PLAYWRIGHT_OUTPUT_DIR="$RUN_ROOT/browser-output"
export npm_config_cache="$RUN_ROOT/npm-cache"
export VITE_CACHE_DIR="$RUN_ROOT/vite-cache"
export TMPDIR="$RUN_ROOT/tmp"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
export NODE_OPTIONS=--max-old-space-size=4096
unset ASTRID_PUBLIC_CHECKOUT ASTRID_APP_DIRECT_DIST

cd "$APP_OVERLAY"
# Collection is deliberately before the hosted build and must select one test.
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list
npm run build:hosted
test -f dist/index.html
flock -w 600 /home/user/work/.app-m1-browser.lock \
  npm run test:e2e:three-products -- --grep "$TEST_TITLE"
