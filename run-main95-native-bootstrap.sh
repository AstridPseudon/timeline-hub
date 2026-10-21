#!/usr/bin/env bash
set -Eeuo pipefail

die() { echo "[main95-bootstrap] $*" >&2; exit 2; }
required=(
  TIMELINE_MAIN95_BOOTSTRAP_RUN
  TIMELINE_MAIN95_APP_SHA
  TIMELINE_MAIN95_APP_TREE
  TIMELINE_MAIN95_AGENT_SHA
  TIMELINE_MAIN95_AGENT_TREE
  TIMELINE_MAIN95_RUNTIME_SHA
  TIMELINE_MAIN95_RUNTIME_TREE
  TIMELINE_MAIN95_RUNTIME_PRODUCER_CHECKOUT
  TIMELINE_MAIN95_PRIVATE13_NODE_MODULES
  TIMELINE_MAIN95_PRIVATE13_READY
  TIMELINE_MAIN95_PRIVATE13_LEASE
  TIMELINE_MAIN95_SHARED_NODE_MODULES
  TIMELINE_MAIN95_RUNNER_PATH
  TIMELINE_MAIN95_RUNNER_SHA256
  TIMELINE_MAIN95_WRAPPER_SHA256
  ASTRID_CHECKOUT
  ASTRID_RUNTIME_CHECKOUT
  ASTRID_PYTHON
  ASTRID_RUNTIME_PYTHON
  PLAYWRIGHT_CHROMIUM_EXECUTABLE
  PLAYWRIGHT_BROWSERS_PATH
  TMPDIR
  TIMELINE_MAIN95_SHORT_TMPDIR
  npm_config_cache
  PWTEST_CACHE_DIR
  XDG_CACHE_HOME
  VITE_CACHE_DIR
  PLAYWRIGHT_OUTPUT_DIR
  PLAYWRIGHT_PROFILE_DIR
  HOME
)
for name in "${required[@]}"; do
  [[ -n "${!name:-}" ]] || die "missing $name"
done
[[ "$TIMELINE_MAIN95_BOOTSTRAP_RUN" == 1 ]] || die 'TIMELINE_MAIN95_BOOTSTRAP_RUN must be 1'
[[ -z "${NODE_PATH:-}" ]] || die 'NODE_PATH must be unset'

app_root=$(git rev-parse --show-toplevel)
app_sha=$(git rev-parse HEAD)
app_tree=$(git rev-parse HEAD^{tree})
[[ "$app_tree" == "$TIMELINE_MAIN95_APP_TREE" ]] || die "App tree mismatch: $app_tree != $TIMELINE_MAIN95_APP_TREE"
# The central test service snapshots the exact source into a synthetic commit.  The
# snapshot HEAD may differ, but the pinned original must independently resolve to
# the same tree before the snapshot is admitted.
[[ "$(git rev-parse "$TIMELINE_MAIN95_APP_SHA^{tree}")" == "$TIMELINE_MAIN95_APP_TREE" ]] || die 'pinned App source commit/tree mismatch'
[[ -z "$(git status --porcelain --untracked-files=normal)" ]] || die 'App snapshot is dirty'

git_head() { git -C "$1" rev-parse HEAD; }
git_tree() { git -C "$1" rev-parse HEAD^{tree}; }
[[ "$(realpath "$ASTRID_CHECKOUT")" == /home/user/work/wt/agt-pin-6efc8150 ]] || die 'unexpected Agent checkout'
[[ "$(realpath "$ASTRID_RUNTIME_CHECKOUT")" == /home/user/work/wt/rt-pin-95bd3c5f ]] || die 'unexpected Runtime checkout'
[[ "$(realpath "$TIMELINE_MAIN95_RUNTIME_PRODUCER_CHECKOUT")" == /home/user/work/wt/rt-pin-95bd3c5f ]] || die 'unexpected Runtime producer checkout'
[[ "$(git_head "$ASTRID_CHECKOUT")" == "$TIMELINE_MAIN95_AGENT_SHA" ]] || die 'Agent HEAD mismatch'
[[ "$(git_tree "$ASTRID_CHECKOUT")" == "$TIMELINE_MAIN95_AGENT_TREE" ]] || die 'Agent tree mismatch'
[[ "$(git_head "$ASTRID_RUNTIME_CHECKOUT")" == "$TIMELINE_MAIN95_RUNTIME_SHA" ]] || die 'Runtime HEAD mismatch'
[[ "$(git_tree "$ASTRID_RUNTIME_CHECKOUT")" == "$TIMELINE_MAIN95_RUNTIME_TREE" ]] || die 'Runtime tree mismatch'
[[ -z "$(git -C "$ASTRID_CHECKOUT" status --porcelain --untracked-files=normal)" ]] || die 'Agent checkout is dirty'
[[ -z "$(git -C "$ASTRID_RUNTIME_CHECKOUT" status --porcelain --untracked-files=normal)" ]] || die 'Runtime checkout is dirty'

runner_path=$(realpath "$TIMELINE_MAIN95_RUNNER_PATH")
wrapper_path=$(realpath "$0")
[[ "sha256:$(sha256sum "$runner_path" | awk '{print $1}')" == "$TIMELINE_MAIN95_RUNNER_SHA256" ]] || die 'source runner hash mismatch'
[[ "sha256:$(sha256sum "$wrapper_path" | awk '{print $1}')" == "$TIMELINE_MAIN95_WRAPPER_SHA256" ]] || die 'central wrapper hash mismatch'
[[ -x "$ASTRID_PYTHON" && -x "$ASTRID_RUNTIME_PYTHON" ]] || die 'pinned Python entry point is not executable'
[[ -x "$PLAYWRIGHT_CHROMIUM_EXECUTABLE" ]] || die 'pinned Chromium executable is not executable'
[[ -d "$PLAYWRIGHT_BROWSERS_PATH" ]] || die 'pinned Playwright browser directory is missing'

private_modules=$(realpath "$TIMELINE_MAIN95_PRIVATE13_NODE_MODULES")
shared_modules=$(realpath "$TIMELINE_MAIN95_SHARED_NODE_MODULES")
[[ "$private_modules" == /home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules ]] || die 'unexpected normal private graph'
[[ "$private_modules" == "$TIMELINE_MAIN95_PRIVATE13_NODE_MODULES" ]] || die 'private graph is not a real directory'
[[ "$private_modules" != "$shared_modules" ]] || die 'private graph resolves to shared App modules'
[[ -d "$private_modules" && -d "$shared_modules" ]] || die 'dependency graph is missing'
[[ -f "$TIMELINE_MAIN95_PRIVATE13_READY" && -f "$TIMELINE_MAIN95_PRIVATE13_LEASE" ]] || die 'private graph READY/LEASE is missing'
grep -Fq -- "Graph root: \`$(dirname "$private_modules")\`" "$TIMELINE_MAIN95_PRIVATE13_READY" || die 'READY graph identity mismatch'
grep -Fq -- "graph_root=$(dirname "$private_modules")" "$TIMELINE_MAIN95_PRIVATE13_LEASE" || die 'LEASE graph identity mismatch'
grep -Fq -- 'composition_sha256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738' "$TIMELINE_MAIN95_PRIVATE13_LEASE" || die 'LEASE archive identity mismatch'
[[ -z "$(find -L "$private_modules" -type l -print -quit)" ]] || die 'private graph contains symlinks'
[[ -L "$app_root/node_modules" ]] || die 'central snapshot node_modules is not a symlink'
[[ "$(realpath "$app_root/node_modules")" == "$shared_modules" ]] || die 'central snapshot did not start on shared modules'

for dir in "$TMPDIR" "$TIMELINE_MAIN95_SHORT_TMPDIR" "$npm_config_cache" "$PWTEST_CACHE_DIR" "$XDG_CACHE_HOME" "$VITE_CACHE_DIR" "$PLAYWRIGHT_OUTPUT_DIR" "$PLAYWRIGHT_PROFILE_DIR" "$HOME"; do
  [[ "$dir" = /* ]] || die "cache path is not absolute: $dir"
  mkdir -p "$dir"
done

node --input-type=module <<'NODE'
import { createRequire } from 'node:module';
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';

const app = process.cwd();
const runtime = process.env.ASTRID_RUNTIME_CHECKOUT;
const privateModules = process.env.TIMELINE_MAIN95_PRIVATE13_NODE_MODULES;
const provenance = JSON.parse(readFileSync(path.join(app, 'vendor/astrid-browser/provenance.json'), 'utf8'));
const runtimeLock = JSON.parse(readFileSync(path.join(app, 'runtime.lock.json'), 'utf8'));
if (provenance.astrid_commit !== process.env.TIMELINE_MAIN95_AGENT_SHA || provenance.astrid_tree !== process.env.TIMELINE_MAIN95_AGENT_TREE) throw new Error('Agent provenance mismatch');
if (runtimeLock.source_commit !== process.env.TIMELINE_MAIN95_RUNTIME_SHA) throw new Error('Runtime lock mismatch');
const manifest = JSON.parse(readFileSync(path.join(runtime, 'contract/artifacts.json'), 'utf8'));
if (Object.keys(manifest.artifacts ?? {}).length !== 76) throw new Error('Runtime manifest is not all76');
const require = createRequire(path.join(privateModules, '__main95_probe__.cjs'));
for (const [name, expected] of Object.entries({
  '@playwright/test': '1.60.0',
  playwright: '1.60.0',
  vite: '5.4.21',
  react: '18.3.1',
  'react-dom': '18.3.1',
  remotion: '4.0.509',
  '@remotion/player': '4.0.509',
  '@banodoco/timeline-composition': '0.0.13',
})) {
  const packageJson = require.resolve(`${name}/package.json`);
  if (!realpathSync(packageJson).startsWith(`${realpathSync(privateModules)}/`)) throw new Error(`${name} resolved outside private graph`);
  const actual = JSON.parse(readFileSync(packageJson, 'utf8')).version;
  if (actual !== expected) throw new Error(`${name} is ${actual}, expected ${expected}`);
}
if (!existsSync(path.join(privateModules, '.bin/vite'))) throw new Error('private Vite binary is missing');
if (!realpathSync(path.join(privateModules, '.bin/vite')).startsWith(`${realpathSync(privateModules)}/`)) throw new Error('Vite binary resolves outside private graph');
console.log(`[main95-bootstrap] metadata and private Node/Vite imports passed: Agent ${provenance.astrid_commit}/${provenance.astrid_tree}, Runtime ${runtimeLock.source_commit}, Runtime artifacts 76`);
NODE

archive="$app_root/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz"
[[ "$(sha256sum "$archive" | awk '{print $1}')" == 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 ]] || die 'Composition archive hash mismatch'
[[ "$(tar -tzf "$archive" | awk '!/\/$/{n++} END {print n+0}')" == 77 ]] || die 'Composition archive is not all77'
source_snapshot() {
  sha256sum "$app_root/package.json" "$app_root/package-lock.json" "$archive"
}
source_before=$(source_snapshot)

restore_modules() {
  status=$?
  if [[ -L "$app_root/node_modules" && "$(realpath "$app_root/node_modules")" == "$private_modules" ]]; then
    rm "$app_root/node_modules"
    ln -s "$shared_modules" "$app_root/node_modules"
  else
    echo '[main95-bootstrap] App node_modules was not left on the private graph link for restore' >&2
    status=2
  fi
  exit "$status"
}
trap restore_modules EXIT
rm "$app_root/node_modules"
ln -s "$private_modules" "$app_root/node_modules"
[[ "$(realpath "$app_root/node_modules")" == "$private_modules" ]] || die 'private graph link was not installed'
export TIMELINE_APP_ROOT="$app_root"
export VITE_TIMELINE_COMPOSITION_ROOT="$private_modules/@banodoco/timeline-composition"
printf '[main95-bootstrap] preflight passed app=%s tree=%s Agent=%s Runtime=%s privateGraph=%s\n' \
  "$app_sha" "$app_tree" "$TIMELINE_MAIN95_AGENT_SHA" "$TIMELINE_MAIN95_RUNTIME_SHA" "$private_modules"
set +e
node "$runner_path"
status=$?
set -e
source_after=$(source_snapshot)
[[ "$source_after" == "$source_before" ]] || die 'App source identity changed during Main95 bootstrap'
exit "$status"
