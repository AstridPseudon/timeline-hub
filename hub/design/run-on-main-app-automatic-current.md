# Run on main: App automatic placement, current source

Status: **APPROVE — ONE main execution after every preflight check passes.** This packet clears the r55 command
custody HOLD. It does not authorize an actual in this worker.

## Authority and exact source

The source is the immutable App checkout at App commit
1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf, tree
8e242d1497841f391b6152ecd8d204143fa03b52. It must be reachable from
refs/remotes/hub/timeline/app/tl/integration; check ancestry, never require
that moving ref’s tip to equal App1490. The other immutable inputs are:

| input | exact pin |
|---|---|
| Agent | 6efc81500a0e0688c2bb41e736503f0fc3e04abb / tree 2ed2b8a12b5b3391ca221ba6ff05390f71a73556 |
| Runtime | 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / tree d3a290b407fa61e6ab2d476f50c068073f70df00 |
| runner | scripts/testing/auto-real-proxy-main95.mjs, SHA-256 7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f |
| App Composition | 0.0.13, SHA-256 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, 77 safe regular archive members |
| Agent Composition | 0.0.12, SHA-256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3, 77 safe regular archive members |
| Runtime artifacts | 76; contract/artifacts.json SHA-256 a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d; producer sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac |

Use the existing test and config only:

- tests/e2e/local/auto-real-proxy.spec.ts, title real operation proxy
  automatic image placement survives reconnect, lost ACK retry, reload and
  guarded undo;
- playwright.auto-real-proxy.config.ts (one worker, no retries, retained
  failure trace).

## Main-owned prerequisites and pure gate

Main may create its own isolated dependency copy. Shared installs and venvs are
read-only; do not install into or replace /home/user/work/app/node_modules.
Use a short private root so the harness’s existing credential file and socket
paths remain below 100 characters:

~~~bash
set -Eeuo pipefail
MAIN=/tmp/tl-a1490
SOURCE_REPO=/home/user/work/app
APP=$MAIN/source/app-1490
AGENT=$MAIN/source/agent-6efc8150
RUNTIME=$MAIN/source/runtime-95bd3c5f
GRAPH=$MAIN/graph/public13
PRIVATE=$MAIN/private
EVIDENCE=$MAIN/evidence/automatic-current
NODE=$MAIN/node-v20.19.4-linux-x64/bin/node
XDG_RUNTIME_DIR=$MAIN/run/x
TMP_PARENT=$MAIN/run/t
APP_SHA=1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf
APP_TREE=8e242d1497841f391b6152ecd8d204143fa03b52
AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
RUNNER_SHA=sha256:7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f

# Resolve the immutable source; do not move the hub ref.
git -C "$SOURCE_REPO" cat-file -e "$APP_SHA^{commit}"
git -C "$SOURCE_REPO" merge-base --is-ancestor "$APP_SHA" \
  refs/remotes/hub/timeline/app/tl/integration
test "$(git -C "$SOURCE_REPO" rev-parse "$APP_SHA^{tree}")" = "$APP_TREE"
# Create APP as a clean detached checkout of APP_SHA before continuing.

mkdir -p "$PRIVATE" "$MAIN/home" "$TMP_PARENT" "$XDG_RUNTIME_DIR" \
  "$MAIN/cache/npm" "$MAIN/cache/pw" "$MAIN/cache/vite" "$MAIN/cache/xdg" \
  "$EVIDENCE/preflight" "$EVIDENCE/recorded"
chmod 700 "$PRIVATE" "$MAIN/home" "$MAIN/run" "$TMP_PARENT" "$XDG_RUNTIME_DIR" \
  "$MAIN/cache" "$EVIDENCE" "$EVIDENCE/preflight" "$EVIDENCE/recorded"
test ! -L "$TMP_PARENT" && test ! -L "$XDG_RUNTIME_DIR"
test "$(stat -c '%a' "$TMP_PARENT")" = 700
test "$(stat -c '%a' "$XDG_RUNTIME_DIR")" = 700

test "$("$NODE" --version)" = v20.19.4
test "$(git -C "$APP" rev-parse HEAD)" = "$APP_SHA"
test "$(git -C "$APP" rev-parse HEAD^{tree})" = "$APP_TREE"
test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
git -C "$APP" merge-base --is-ancestor \
  02ac224cd3c0d376f08b6129f58ded624f3e400d "$APP_SHA"
git -C "$APP" merge-base --is-ancestor \
  da5d6d564af58ad06f126188c25e9a47f4e45be4 "$APP_SHA"

# APP initially points at the private public13 graph. The runner temporarily
# replaces this link with its own private overlay and restores it in finally.
test -L "$APP/node_modules"
test "$(realpath "$APP/node_modules")" = "$(realpath "$GRAPH/node_modules")"
test -d "$GRAPH/node_modules/.vite" && test ! -L "$GRAPH/node_modules/.vite"
test -d "$GRAPH/node_modules/.vite-temp" && test ! -L "$GRAPH/node_modules/.vite-temp"
test -z "$(find -P "$GRAPH/node_modules" -type l -print -quit)"
"$NODE" - "$GRAPH/node_modules" <<'NODE'
const fs = require('node:fs');
const path = require('node:path');
const root = process.argv[2];
const expected = {
  '@banodoco/timeline-composition': '0.0.13', react: '18.3.1', 'react-dom': '18.3.1',
  remotion: '4.0.509', '@remotion/player': '4.0.509', '@remotion/three': '4.0.509',
  playwright: '1.60.0', '@playwright/test': '1.60.0',
};
for (const [name, version] of Object.entries(expected)) {
  const value = JSON.parse(fs.readFileSync(path.join(root, name, 'package.json')));
  if (value.version !== version) throw new Error(name + ': ' + value.version + ' !== ' + version);
}
NODE
test "$(sha256sum "$RUNTIME/contract/artifacts.json" | awk '{print $1}')" = \
  a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
test "$(sha256sum "$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | awk '{print $1}')" = \
  9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
test "$(tar -tzf "$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | awk '!/\/$/ {n++} END {print n+0}')" = 77
test "$(sha256sum "$APP/scripts/testing/auto-real-proxy-main95.mjs" | awk '{print $1}')" = \
  7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f

# These are the effective env-i inputs for the startup check, --list check,
# and runner. No NODE_OPTIONS, NODE_PATH, LD_*, or PYTHONHOME is inherited.
COMMON_ENV=(
  HOME="$MAIN/home" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin"
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
  ASTRID_APP_DIRECT_DOOR_PORT=17340 XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"
  TMPDIR="$TMP_PARENT" npm_config_cache="$MAIN/cache/npm" npm_config_offline=true
  PWTEST_CACHE_DIR="$MAIN/cache/pw" VITE_CACHE_DIR="$MAIN/cache/vite"
  XDG_CACHE_HOME="$MAIN/cache/xdg" TSX_DISABLE_CACHE=1
  TIMELINE_BUNDLE_AGENT_HEAD="$AGENT_SHA" TIMELINE_BUNDLE_RUNTIME_HEAD="$RUNTIME_SHA"
  TIMELINE_AUTO_REAL_PROXY_APP_SHA="$APP_SHA" TIMELINE_AUTO_REAL_PROXY_APP_TREE="$APP_TREE"
  TIMELINE_AUTO_REAL_PROXY_AGENT_SHA="$AGENT_SHA" TIMELINE_AUTO_REAL_PROXY_AGENT_TREE="$AGENT_TREE"
  TIMELINE_AUTO_REAL_PROXY_RUNTIME_SHA="$RUNTIME_SHA" TIMELINE_AUTO_REAL_PROXY_RUNTIME_TREE="$RUNTIME_TREE"
  TIMELINE_AUTO_REAL_PROXY_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME"
  TIMELINE_AUTO_REAL_PROXY_DEPENDENCY_ROOT="$GRAPH/node_modules"
  TIMELINE_AUTO_REAL_PROXY_PRIVATE_ROOT="$PRIVATE"
  TIMELINE_AUTO_REAL_PROXY_RUNNER_SHA256="$RUNNER_SHA"
)
env -i "${COMMON_ENV[@]}" "$NODE" -e '
  for (const key of Object.keys(process.env))
    if (/^(NODE_OPTIONS|NODE_PATH|LD_|PYTHONHOME$)/.test(key)) throw new Error(key);
  for (const value of process.argv.slice(1)) if (value.length >= 100) throw new Error(value);
' "$TMP_PARENT" "$XDG_RUNTIME_DIR" \
  "$PRIVATE/real-proxy-9999999999/tmpdir/astrid-direct-XXXXXX/product-credential.json" \
  "$XDG_RUNTIME_DIR/timeline.sock"

cd "$APP"
env -i "${COMMON_ENV[@]}" \
  TIMELINE_AUTO_REAL_PROXY_RUN=1 TIMELINE_AUTO_REAL_PROXY_STARTUP_ONLY=1 \
  TIMELINE_AUTO_REAL_PROXY_RECORD_DIR="$EVIDENCE/preflight" \
  "$NODE" scripts/testing/auto-real-proxy-main95.mjs \
  > "$EVIDENCE/preflight.log" 2>&1
grep -Fq '"mode":"startup-only"' "$EVIDENCE/preflight.log"
env -i "${COMMON_ENV[@]}" npm exec -- playwright --version | grep -Fxq 'Version 1.60.0'

SHARED_REAL=$(realpath /home/user/work/app/node_modules)
test "$SHARED_REAL" != "$(realpath "$GRAPH/node_modules")"
find -P "$SHARED_REAL" -type f -exec sha256sum {} + | LC_ALL=C sort > "$EVIDENCE/shared-node-modules.before"
find -P "$GRAPH/node_modules" -type f -exec sha256sum {} + | LC_ALL=C sort > "$EVIDENCE/private-graph.before"

# The one executable list check is before the actual and must find exactly one
# collected test. It is not the actual; it has no browser, task, or Runtime.
env -i "${COMMON_ENV[@]}" npm exec -- playwright test \
  --config playwright.auto-real-proxy.config.ts \
  tests/e2e/local/auto-real-proxy.spec.ts --list \
  > "$EVIDENCE/list.txt" 2>&1
"$NODE" - "$EVIDENCE/list.txt" <<'NODE'
const fs = require('node:fs');
const text = fs.readFileSync(process.argv[2], 'utf8');
const title = 'real operation proxy automatic image placement survives reconnect, lost ACK retry, reload and guarded undo';
if (text.split('auto-real-proxy.spec.ts').length - 1 !== 1) throw new Error('test file count is not 1');
if (text.split(title).length - 1 !== 1) throw new Error('test title count is not 1');
if (!text.includes('Total: 1 test in 1 file')) throw new Error('list total is not 1 test in 1 file');
NODE

# The sole actual. Do not replace this with direct Playwright: the existing
# runner creates the private Vite/Rollup overlay, adds private caches and
# record paths, supplies bundle heads, checks sources/graph/browser/credentials,
# and restores/postflights in finally.
set +e
env -i "${COMMON_ENV[@]}" \
  TIMELINE_AUTO_REAL_PROXY_RUN=1 \
  TIMELINE_AUTO_REAL_PROXY_RECORD_DIR="$EVIDENCE/recorded" \
  "$NODE" scripts/testing/auto-real-proxy-main95.mjs \
  > "$EVIDENCE/runner.log" 2>&1
STATUS=$?
set -e
test "$STATUS" = 0

# Exact runner-spawned child argv (from runRealProxyGate):
# npm exec -- playwright test --config playwright.auto-real-proxy.config.ts
# The config’s testMatch selects auto-real-proxy.spec.ts; no second actual,
# --grep, retry, selector, timeout, browser, install, or build is permitted.

# Postflight is required even when the runner exits zero.
test "$(git -C "$APP" rev-parse HEAD)" = "$APP_SHA"
test "$(git -C "$APP" rev-parse HEAD^{tree})" = "$APP_TREE"
test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
test "$(realpath "$APP/node_modules")" = "$(realpath "$GRAPH/node_modules")"
test "$(sha256sum "$APP/scripts/testing/auto-real-proxy-main95.mjs" | awk '{print $1}')" = \
  7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f
test -s "$EVIDENCE/recorded/runner-result.json"
test -s "$EVIDENCE/recorded/auto-http-failures.json"
test "$(find -P "$GRAPH/node_modules" -type l -print -quit)" = ''
find -P "$SHARED_REAL" -type f -exec sha256sum {} + | LC_ALL=C sort > "$EVIDENCE/shared-node-modules.after"
find -P "$GRAPH/node_modules" -type f -exec sha256sum {} + | LC_ALL=C sort > "$EVIDENCE/private-graph.after"
cmp -s "$EVIDENCE/shared-node-modules.before" "$EVIDENCE/shared-node-modules.after"
cmp -s "$EVIDENCE/private-graph.before" "$EVIDENCE/private-graph.after"
~~~

The runner’s actual privateEnvironment carries bundle heads, TSX_DISABLE_CACHE,
private npm/Playwright/Vite caches, PLAYWRIGHT_OUTPUT_DIR, and the durable
record directory into the spawned npm child. Its prepareNodeModulesOverlay
copies Vite/Rollup privately, links the remaining graph read-only, and restores
the original App symlink. The harness creates the existing
product-credential.json as mode 0600 and passes its path through the established
discovery/config flow; do not create or print a replacement credential.

The mandatory actual result is the existing case collected once and passing:
one passed, zero failed, no relevant retained non-2xx responses, no invalidating
page/console/request-failure diagnostics, and zero legacy writer POSTs. ACP
traffic/noise is diagnostic-only; there is no invented ACP zero-response rule.
On failure, preserve EVIDENCE and report the first sanitized entry in
recorded/auto-http-failures.json plus the runner log. The runner’s record and
source/graph postflight checks remain authoritative.

## r55 disposition and real prerequisites

All eight r55 command findings are resolved here: executable source/HEAD/tree
and ancestry checks; private graph/package/archive/manifest checks; Node and
Chromium variables in every phase; process-local forbidden-env check; physical
short TMPDIR/XDG runtime path checks; executable one-test list; runner-owned
overlay/cache/record/source postflight; and no direct actual bypass. Main still
must supply Node v20.19.4, Chromium
/opt/pw-browsers/chromium-1194/chrome-linux/chrome version 141.0.7390.37,
the pinned Agent/Runtime checkouts and read-only venvs, a verified private
public13 graph, and free door port 17340. No browser/build/install/graph/actual
was run while preparing this packet; the source was preserved exactly.
