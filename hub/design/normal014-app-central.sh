#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$HERE/normal014-source-common.sh"

mode=${1:-preflight}
app_root=${2:-$(pwd)}
normal014_start_run timeline-normal014-app
normal014_use_private_tmp

case "$mode" in
  preflight|run) ;;
  *) echo "usage: $0 preflight|run [app-root]" >&2; exit 2;;
esac

test -f "$app_root/package.json"
prepare_sources "$run_root/sources"
agent="$run_root/sources/agent-6ef"
runtime="$run_root/sources/runtime-95"
producer="$run_root/sources/producer-95"
verify_locked_graph
prepare_private_python "$run_root"
verify_python_imports_and_collection "$NORMAL014_PYTHON" "$agent" "$runtime"

# Make a private App candidate.  The checked-in App worktree is not edited.
overlay="$run_root/app"
mkdir -p "$overlay"
cp -a "$app_root"/. "$overlay"/
rm -rf "$overlay/node_modules"
source_node_modules=$(realpath "$LOCKED_GRAPH/node_modules")
test "$source_node_modules" = "$LOCKED_GRAPH/node_modules"
private_node_modules="$run_root/private-node-modules"
prepare_private_node_graph "$source_node_modules" "$private_node_modules"
test -x "$private_node_modules/.bin/vite"
test "$(realpath "$private_node_modules")" = "$private_node_modules"
ln -s "$private_node_modules" "$overlay/node_modules"

OVERLAY="$overlay" APP_BASE_RUNTIME_SHA="$APP_BASE_RUNTIME_SHA" RUNTIME_SHA="$RUNTIME_SHA" node --input-type=module - <<'JS'
import { readFileSync, writeFileSync } from 'node:fs';
const file = `${process.env.OVERLAY}/runtime.lock.json`;
const lock = JSON.parse(readFileSync(file, 'utf8'));
if (lock.source_commit !== process.env.APP_BASE_RUNTIME_SHA) throw new Error(`unexpected App base lock: ${lock.source_commit}`);
lock.source_commit = process.env.RUNTIME_SHA;
writeFileSync(file, `${JSON.stringify(lock, null, 2)}\n`);
JS

cd "$overlay"
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$runtime"
node scripts/vendor-lock.mjs check runtime.lock.json --producer "$runtime"
node scripts/vendor-lock.mjs check runtime.lock.json
AGENT="$agent" verify_artifacts "$runtime" "$producer"
test "$(node -e 'console.log(require("./runtime.lock.json").source_commit)')" = "$RUNTIME_SHA"
test "$(sha256sum src/integrations/runtime/generated-contract-metadata.ts | cut -d' ' -f1)" = "$APP_METADATA_SHA"
test "$(sha256sum src/integrations/runtime/generated.ts | cut -d' ' -f1)" = "$APP_GENERATED_SHA"
test "$(sha256sum src/integrations/runtime/timeline-commit-types.ts | cut -d' ' -f1)" = "$APP_TYPES_SHA"
test "$(sha256sum vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json | cut -d' ' -f1)" = "$APP_SCHEMA_SHA"

mkdir -p "$run_root/npm-cache" "$run_root/pw-cache" "$run_root/browser-output" "$run_root/vite-cache"
export ASTRID_CHECKOUT="$agent"
export ASTRID_PYTHON="$NORMAL014_PYTHON"
export ASTRID_RUNTIME_CHECKOUT="$runtime"
export ASTRID_RUNTIME_PYTHON="$NORMAL014_PYTHON"
export TIMELINE_BUNDLE_AGENT_HEAD="$AGENT_SHA"
export TIMELINE_BUNDLE_RUNTIME_HEAD="$RUNTIME_SHA"
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
export PWTEST_CACHE_DIR="$run_root/pw-cache"
export PLAYWRIGHT_OUTPUT_DIR="$run_root/browser-output"
export npm_config_cache="$run_root/npm-cache"
export VITE_CACHE_DIR="$run_root/vite-cache"
export TMPDIR="$run_root/tmp"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1

# Exercise the same hosted build that Playwright's global setup invokes, before
# any browser work.  The output is in the disposable overlay and Vite's
# node_modules/.vite cache is private because the graph above is private.
cd "$overlay"
npm run build:hosted
test -f "$overlay/dist/index.html"
test "$(realpath "$overlay/dist")" = "$overlay/dist"
test -f "$private_node_modules/.bin/vite"
echo "normal014 App PRE-browser: private npm/Vite caches and hosted build output verified"

if [ "$mode" = preflight ]; then
  mkdir -p "$run_root/vitest-cache" "$run_root/tmp"
  printf '%s\n' "const path = require('node:path');" "global.__dirname = path.resolve(process.cwd(), 'config/testing');" > "$run_root/vitest-runner.cjs"
  TMPDIR="$run_root/tmp" VITE_CACHE_DIR="$run_root/vitest-cache" \
    node --require "$run_root/vitest-runner.cjs" node_modules/vitest/vitest.mjs list \
      --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
      --maxWorkers=1 --no-file-parallelism \
      src/integrations/runtime/client.test.ts \
      src/integrations/runtime/clientSharedSession.test.ts \
      src/integrations/runtime/recordedResponses.test.ts \
      src/integrations/runtime/timelineCommit.test.ts \
      src/integrations/runtime/dataProvider.test.ts \
      src/integrations/runtime/vendorLock.test.ts >/dev/null
  chromium=$(realpath /opt/pw-browsers/chromium)
  test -x "$chromium"
  "$chromium" --version >/dev/null
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR="$run_root/tmp" \
    node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
      --grep 'M2 real gate 5' --list >/dev/null
  echo "normal014 App preflight: private vendor-lock, provider collection, Chromium, Playwright collection, and tuple/artifact bytes verified"
  exit 0
fi

if flock -w 600 /home/user/work/.app-m1-browser.lock \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
  --grep 'M2 real gate 5'; then
  normal014_exit_status=0
else
  normal014_exit_status=$?
fi
exit "$normal014_exit_status"
