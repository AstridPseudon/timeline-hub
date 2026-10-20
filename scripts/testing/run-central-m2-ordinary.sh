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
TARGET_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55
TARGET_AGENT_TREE=236c3e57e0265c52b81ba8085de3193026176bff
TARGET_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a
TARGET_RUNTIME_TREE=7ab412cc4bcbe517efcfa806e092336390312e18
EXPECTED_GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
EXPECTED_COMPOSITION_TARBALL_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
NATIVE_PYTHON=/home/user/work/venv-app2-native/bin/python
APP_LOCK="$APP_ROOT/runtime.lock.json"
APP_COMPOSITION="$APP_ROOT/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz"

test "$(printf %s "$TARGET_AGENT_SHA" | wc -c)" = 40
test "$(printf %s "$TARGET_RUNTIME_SHA" | wc -c)" = 40
test "$(git -C "$AGENT_REPO" rev-parse "$TARGET_AGENT_SHA^{commit}")" = "$TARGET_AGENT_SHA"
test "$(git -C "$AGENT_REPO" rev-parse "$TARGET_AGENT_SHA^{tree}")" = "$TARGET_AGENT_TREE"
test "$(git -C "$RUNTIME_REPO" rev-parse "$TARGET_RUNTIME_SHA^{commit}")" = "$TARGET_RUNTIME_SHA"
test "$(git -C "$RUNTIME_REPO" rev-parse "$TARGET_RUNTIME_SHA^{tree}")" = "$TARGET_RUNTIME_TREE"

test -d "$LOCKED_GRAPH/node_modules"
test -f "$LOCKED_GRAPH_ARCHIVE"
test -x "$NATIVE_PYTHON"
test "$(sha256sum "$LOCKED_GRAPH_ARCHIVE" | cut -d' ' -f1)" = "$EXPECTED_GRAPH_ARCHIVE_SHA"
test "$(node -p "require('$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | sha256sum | cut -d' ' -f1)" = "$EXPECTED_COMPOSITION_TARBALL_SHA"
test "$(realpath "$LOCKED_GRAPH/node_modules")" = "$LOCKED_GRAPH/node_modules"
test -f "$APP_LOCK"
test "$(node -p "require('$APP_LOCK').source_commit")" = "$TARGET_RUNTIME_SHA"
test "$(node -p "require('$APP_LOCK').producer_version")" = sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56
test -f "$APP_COMPOSITION"
test "$(sha256sum "$APP_COMPOSITION" | cut -d' ' -f1)" = "$EXPECTED_COMPOSITION_TARBALL_SHA"

RUN_ROOT="$APP_ROOT/.m2-ordinary-central-run"
case "$RUN_ROOT" in
  "$APP_ROOT"/*) ;;
  *) echo 'unsafe run root' >&2; exit 2 ;;
esac
test ! -e "$RUN_ROOT"
mkdir -p "$RUN_ROOT" "$RUN_ROOT/agent" "$RUN_ROOT/runtime" "$RUN_ROOT/node-modules" \
  "$RUN_ROOT/tmp" "$RUN_ROOT/npm-cache" "$RUN_ROOT/pw-cache" "$RUN_ROOT/browser-output" "$RUN_ROOT/vite-cache"

ORIGINAL_NODE_MODULES_TARGET=$(readlink "$APP_ROOT/node_modules" 2>/dev/null || true)
test -n "$ORIGINAL_NODE_MODULES_TARGET"
test "$(realpath "$APP_ROOT/node_modules")" = /home/user/work/app/node_modules

# Chromium derives its profile and Unix-domain socket paths from TMPDIR. Keep
# those paths short and private; the App/agent/runtime work roots intentionally
# remain in the worktree so this does not create a second App checkout.
TMP_BASE=${TMPDIR:-/tmp}
test -d "$TMP_BASE" && test -w "$TMP_BASE"
BROWSER_ROOT=$(mktemp -d "$TMP_BASE/tl-chromium-XXXXXX")
mkdir -p "$BROWSER_ROOT/tmp" "$BROWSER_ROOT/xdg-cache" "$BROWSER_ROOT/xdg-config"

cleanup() {
  if test -n "$ORIGINAL_NODE_MODULES_TARGET"; then
    rm -f "$APP_ROOT/node_modules"
    ln -s "$ORIGINAL_NODE_MODULES_TARGET" "$APP_ROOT/node_modules"
  fi
  if test -z "$(git -C "$APP_ROOT" ls-files -- 'dist/**')"; then
    rm -rf "$APP_ROOT/dist"
  fi
  if test -n "${BROWSER_ROOT:-}"; then
    rm -rf "$BROWSER_ROOT"
  fi
  rm -rf "$RUN_ROOT"
}
trap cleanup EXIT HUP INT TERM

git clone --quiet --shared --no-checkout "$AGENT_REPO" "$RUN_ROOT/agent"
git -C "$RUN_ROOT/agent" reset --hard --quiet "$TARGET_AGENT_SHA"
test "$(git -C "$RUN_ROOT/agent" rev-parse HEAD)" = "$TARGET_AGENT_SHA"
test "$(git -C "$RUN_ROOT/agent" rev-parse 'HEAD^{tree}')" = "$TARGET_AGENT_TREE"
test -z "$(git -C "$RUN_ROOT/agent" status --porcelain=v1 --untracked-files=all)"

git clone --quiet --shared --no-checkout "$RUNTIME_REPO" "$RUN_ROOT/runtime"
git -C "$RUN_ROOT/runtime" reset --hard --quiet "$TARGET_RUNTIME_SHA"
test "$(git -C "$RUN_ROOT/runtime" rev-parse HEAD)" = "$TARGET_RUNTIME_SHA"
test "$(git -C "$RUN_ROOT/runtime" rev-parse 'HEAD^{tree}')" = "$TARGET_RUNTIME_TREE"
test -z "$(git -C "$RUN_ROOT/runtime" status --porcelain=v1 --untracked-files=all)"

# Keep the public locked graph immutable while recreating package bins in one
# private per-run graph. Vite and Playwright then resolve their own binaries.
SOURCE_NODE_MODULES="$LOCKED_GRAPH/node_modules" PRIVATE_NODE_MODULES="$RUN_ROOT/node-modules" node --input-type=module - <<'JS'
import { lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, statSync, symlinkSync } from 'node:fs';
import path from 'node:path';

const source = realpathSync(process.env.SOURCE_NODE_MODULES);
const destination = path.resolve(process.env.PRIVATE_NODE_MODULES);
mkdirSync(destination, { recursive: true });
mkdirSync(path.join(destination, '.bin'));
const packages = [];
for (const entry of readdirSync(source, { withFileTypes: true })) {
  if (entry.name === '.bin') continue;
  const scope = entry.name.startsWith('@');
  const sourceScope = path.join(source, entry.name);
  const destinationScope = path.join(destination, entry.name);
  if (scope) mkdirSync(destinationScope);
  const entries = scope ? readdirSync(sourceScope, { withFileTypes: true }) : [entry];
  for (const packageEntry of entries) {
    if (packageEntry.name === '.bin') continue;
    const packageSource = scope ? path.join(sourceScope, packageEntry.name) : sourceScope;
    const packageDestination = scope ? path.join(destinationScope, packageEntry.name) : path.join(destination, entry.name);
    symlinkSync(packageSource, packageDestination, 'dir');
    packages.push([scope ? `${entry.name}/${packageEntry.name}` : entry.name, packageDestination]);
  }
}
let bins = 0;
for (const [name, packageDirectory] of packages) {
  let packageJson;
  try { packageJson = JSON.parse(readFileSync(path.join(packageDirectory, 'package.json'), 'utf8')); }
  catch (error) { if (error?.code === 'ENOENT') continue; throw error; }
  const declaration = packageJson.bin;
  if (!declaration) continue;
  const declared = typeof declaration === 'string'
    ? { [String(packageJson.name ?? name).split('/').pop()]: declaration }
    : declaration;
  for (const [command, target] of Object.entries(declared)) {
    if (!command || typeof target !== 'string' || !target) throw new Error(`invalid bin declaration in ${name}`);
    const resolvedTarget = path.resolve(packageDirectory, target);
    if (resolvedTarget !== path.resolve(packageDirectory) && !resolvedTarget.startsWith(`${path.resolve(packageDirectory)}${path.sep}`)) {
      throw new Error(`bin target escapes ${name}: ${target}`);
    }
    lstatSync(resolvedTarget);
    const link = path.join(destination, '.bin', command);
    if (lstatSync(link, { throwIfNoEntry: false })) continue;
    symlinkSync(path.relative(path.join(destination, '.bin'), resolvedTarget), link);
    bins += 1;
  }
}
console.log(`private node graph: packages=${packages.length} bins=${bins}`);
JS
test -x "$RUN_ROOT/node-modules/.bin/vite"
test -x "$RUN_ROOT/node-modules/.bin/playwright"

rm -f "$APP_ROOT/node_modules"
ln -s "$RUN_ROOT/node-modules" "$APP_ROOT/node_modules"
export ASTRID_CHECKOUT="$RUN_ROOT/agent"
export ASTRID_PYTHON="$NATIVE_PYTHON"
export ASTRID_RUNTIME_CHECKOUT="$RUN_ROOT/runtime"
export ASTRID_RUNTIME_PYTHON="$NATIVE_PYTHON"
export TIMELINE_BUNDLE_AGENT_HEAD="$TARGET_AGENT_SHA"
export TIMELINE_BUNDLE_RUNTIME_HEAD="$TARGET_RUNTIME_SHA"
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
export PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
export PWTEST_CACHE_DIR="$RUN_ROOT/pw-cache"
export PLAYWRIGHT_OUTPUT_DIR="$RUN_ROOT/browser-output"
export npm_config_cache="$RUN_ROOT/npm-cache"
export VITE_CACHE_DIR="$RUN_ROOT/vite-cache"
export TMPDIR="$BROWSER_ROOT/tmp"
export XDG_CACHE_HOME="$BROWSER_ROOT/xdg-cache"
export XDG_CONFIG_HOME="$BROWSER_ROOT/xdg-config"
export DEBUG=pw:browser
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
export NODE_OPTIONS=--max-old-space-size=4096
unset ASTRID_PUBLIC_CHECKOUT ASTRID_APP_DIRECT_DIST

flock -w 600 /home/user/work/.app-m1-browser.lock sh -c '
  cd "$1"
  node scripts/testing/chromium-launch-smoke.mjs
  npm run build:hosted
  test -f dist/index.html
  npm run test:e2e:three-products -- --grep "M2 ordinary extension batch"
' sh "$APP_ROOT"

