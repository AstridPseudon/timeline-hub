#!/bin/sh
set -eu

. "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh"

mode=${1:-preflight}
app_root=${2:-$(pwd)}
case "$mode" in
  preflight|run) ;;
  *) echo "usage: $0 preflight|run [app-root]" >&2; exit 2 ;;
esac

run_root=${NORMAL014_RUN_ROOT:-$(mktemp -d /tmp/timeline-normal014-app.XXXXXX)}
cleanup=1
if [ "${NORMAL014_KEEP_TEMP:-0}" = 1 ]; then cleanup=0; fi
cleanup_run() {
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$cleanup" = 1 ]; then rm -rf "$run_root"; fi
  exit "$status"
}
trap cleanup_run EXIT
trap 'exit 130' INT
trap 'exit 143' HUP TERM

test -f "$app_root/package.json"
prepare_sources "$run_root/sources"
agent="$run_root/sources/agent-3c4"
runtime="$run_root/sources/runtime-202"
producer="$run_root/sources/producer-a0"
verify_locked_graph
prepare_private_python "$run_root"
verify_python_imports_and_collection "$NORMAL014_PYTHON" "$agent" "$runtime"

qualified_ref=f487c0ca9a7b916bf842dd7a2cb3fa442ebeda3e
qualified_tree=6444fffcaa606bfe83101ccb561c47fbd0d10ce4
qualified_repo=${QUALIFIED_APP_REPO:-/home/user/banodoco/reigh-app}
if ! git -C "$qualified_repo" cat-file -e "$qualified_ref^{commit}" 2>/dev/null; then
  qualified_repo=$app_root
fi
test "$(git -C "$qualified_repo" show -s --format=%T "$qualified_ref")" = "$qualified_tree"

overlay="$run_root/app"
mkdir -p "$overlay"
cp -a "$app_root"/. "$overlay"/

qualified_paths="$run_root/qualified-paths.txt"
effective_paths="$run_root/effective-paths.txt"
printf '%s\n' \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/integrations/runtime/bootstrapInitialization.ts \
  src/integrations/runtime/client.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts \
  src/integrations/runtime/createDefaultTimeline.ts \
  src/integrations/runtime/dataProvider.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/commitOutbox.ts \
  src/tools/video-editor/commands/fixtures/bootstrap_parity.py \
  src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json \
  tests/e2e/local/support/app.ts \
  tests/e2e/local/support/timeline-scope.test.ts \
  tests/e2e/local/support/timeline-scope.ts \
  tests/e2e/local/three-products.spec.ts > "$qualified_paths"
git -C "$qualified_repo" diff-tree --no-commit-id --name-only -r "$qualified_ref^" "$qualified_ref" | sort > "$effective_paths"
cmp "$qualified_paths" "$effective_paths"

# The reviewed production delta must be present in the requested candidate.
# Never overlay the frozen donor test over the project-selection correction.
while IFS= read -r relative; do
  case "$relative" in
    tests/e2e/local/three-products.spec.ts|tests/e2e/local/support/timeline-scope.ts|tests/e2e/local/support/timeline-scope.test.ts) continue ;;
  esac
  git -C "$qualified_repo" show "$qualified_ref:$relative" > "$run_root/qualified-blob"
  cmp "$overlay/$relative" "$run_root/qualified-blob"
done < "$qualified_paths"

test "$(sha256sum "$overlay/tests/e2e/local/three-products.spec.ts" | cut -d' ' -f1)" = fda4df2030ff09d8c6606611c84f5ed761ca4cf7836190903348c579d95a08f6
test "$(sha256sum "$overlay/tests/e2e/local/support/timeline-scope.ts" | cut -d' ' -f1)" = a2965d220628de15bb169baff96dd1db020248d3df727ea6e2d83640b17346ab
test "$(sha256sum "$overlay/tests/e2e/local/support/timeline-scope.test.ts" | cut -d' ' -f1)" = 71e73fd4fc59ae5079144518d1aa0d0be5fa1818e3b9c9e7c529b037527175ee

test_file=tests/e2e/local/three-products.spec.ts
effective_test_sha=$(sha256sum "$overlay/$test_file" | cut -d' ' -f1)
echo "bootstrap source identity: donor_ref=$qualified_ref donor_tree=$qualified_tree repaired_test_sha=$effective_test_sha"

rm -rf "$overlay/node_modules"
source_node_modules=$(realpath "$LOCKED_GRAPH/node_modules")
test "$source_node_modules" = "$LOCKED_GRAPH/node_modules"
private_node_modules="$run_root/private-node-modules"
prepare_private_node_graph "$source_node_modules" "$private_node_modules"
test -x "$private_node_modules/.bin/vite"
test "$(realpath "$private_node_modules")" = "$private_node_modules"
ln -s "$private_node_modules" "$overlay/node_modules"

OVERLAY="$overlay" RUNTIME_SHA="$RUNTIME_SHA" node --input-type=module - <<'JS'
import { readFileSync, writeFileSync } from 'node:fs';
const file = `${process.env.OVERLAY}/runtime.lock.json`;
const lock = JSON.parse(readFileSync(file, 'utf8'));
if (lock.source_commit !== '2c4ac180c2220bdad966bc01e95ad230e99ce26a') throw new Error(`unexpected App base lock: ${lock.source_commit}`);
lock.source_commit = process.env.RUNTIME_SHA;
writeFileSync(file, `${JSON.stringify(lock, null, 2)}\n`);
JS

cd "$overlay"
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$runtime"
node scripts/vendor-lock.mjs check runtime.lock.json --producer "$runtime"
node scripts/vendor-lock.mjs check runtime.lock.json
AGENT="$agent" verify_artifacts "$runtime" "$producer"
test "$(node -e 'console.log(require("./runtime.lock.json").source_commit)')" = "$RUNTIME_SHA"
test "$(sha256sum src/integrations/runtime/generated-contract-metadata.ts | cut -d' ' -f1)" = 9b3b8723a8d86a78d57bf83f43eb82914d1d0cd81ae89ebdf993b1560ddc57dd
test "$(sha256sum src/integrations/runtime/generated.ts | cut -d' ' -f1)" = c422ce38279e6df9eb93c5b53993d57e68339b0807d34ed69d85b2408ed98be2
test "$(sha256sum src/integrations/runtime/timeline-commit-types.ts | cut -d' ' -f1)" = f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
test "$(sha256sum vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json | cut -d' ' -f1)" = f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1

mkdir -p "$run_root/npm-cache" "$run_root/pw-cache" "$run_root/browser-output" "$run_root/tmp" "$run_root/vite-cache" "$run_root/vitest-cache"
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

BOOTSTRAP_SUBSTRING='M2 real gate 5 bootstrap actual consumer'
BOOTSTRAP_PATH='tests/e2e/local/three-products.spec.ts'
printf '%s\n' "const path = require('node:path');" "global.__dirname = path.resolve(process.cwd(), 'config/testing');" > "$run_root/vitest-runner.cjs"
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR="$run_root/tmp" \
  node --require "$run_root/vitest-runner.cjs" node_modules/playwright/cli.js test \
    --config playwright.three-products.config.ts --grep "$BOOTSTRAP_SUBSTRING" --list \
    "$BOOTSTRAP_PATH" > "$run_root/bootstrap-list.txt"
selected=$(grep -F "$BOOTSTRAP_SUBSTRING" "$run_root/bootstrap-list.txt" | wc -l | tr -d ' ')
test "$selected" = 1
grep -F "Total: 1 test in 1 file" "$run_root/bootstrap-list.txt"
echo "bootstrap selector proof: path=$BOOTSTRAP_PATH grep=$BOOTSTRAP_SUBSTRING selected=$selected test_sha=$effective_test_sha"

cd "$overlay"
npm run build:hosted
test -f "$overlay/dist/index.html"
test "$(realpath "$overlay/dist")" = "$overlay/dist"
echo "normal014 App PRE-browser: qualified source identity, exact selector, private caches, and hosted build verified"

if [ "$mode" = preflight ]; then
  chromium=$(realpath /opt/pw-browsers/chromium)
  test -x "$chromium"
  "$chromium" --version >/dev/null
  exit 0
fi

evidence_dir=${BOOTSTRAP_EVIDENCE_DIR:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-project-scope-causal-repair/scope-evidence}
mkdir -p "$evidence_dir"
test "$(realpath "$evidence_dir")" = "$evidence_dir"
set +e
flock -w 600 /home/user/work/.app-m1-browser.lock \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
  --grep "$BOOTSTRAP_SUBSTRING" "$BOOTSTRAP_PATH"
status=$?
set -e
# Preserve only the allowlisted, sanitized normal-API scope snapshots.
find "$run_root/browser-output" -name bootstrap-scope.json -type f -exec cp '{}' "$evidence_dir/" \;
exit "$status"
