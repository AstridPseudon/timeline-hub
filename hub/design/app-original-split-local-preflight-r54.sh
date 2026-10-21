#!/usr/bin/env bash
set -Eeuo pipefail

# Pure preflight for the existing current013 parent-split runner.  This file
# deliberately creates no directories, starts no service, and never sets the
# runner's execution switch.  The caller supplies already-materialized,
# manager-owned paths.

die() { printf 'BLOCKED: %s\n' "$*" >&2; exit 2; }
need() { [[ -n "${!1:-}" ]] || die "$1 is required"; }
physical_dir() {
  local name=$1 value=${!1}
  [[ -d "$value" && ! -L "$value" ]] || die "$name must be an existing physical directory: $value"
}
physical_file() {
  local name=$1 value=${!1}
  [[ -f "$value" && ! -L "$value" ]] || die "$name must be an existing physical file: $value"
}
mode700() { [[ "$(stat -c '%a' "$1")" == 700 ]] || die "expected mode 0700: $1"; }
sha256() { sha256sum "$1" | awk '{print $1}'; }
git_at() { git -C "$1" "$@"; }

need MAIN
need APP
need AGENT
need AGENT_VENDOR
need RUNTIME
need GRAPH
need PRIVATE
need READY
need LEASE
need EVIDENCE
need NODE
need CHROME
need TMP
need SOCKET
need SHORT
need CREDENTIAL
need PORT

APP_SHA=${APP_SHA:-92c30b570cf8105dc021a64874c258e6c950b841}
APP_TREE=${APP_TREE:-c34d65b66481fd0015279451b175c53b7b5e8f4f}
AGENT_SHA=${AGENT_SHA:-6efc81500a0e0688c2bb41e736503f0fc3e04abb}
AGENT_TREE=${AGENT_TREE:-2ed2b8a12b5b3391ca221ba6ff05390f71a73556}
AGENT_VENDOR_SHA=${AGENT_VENDOR_SHA:-091aa23ec83ea05ffd3b0115a640230d51c8c429}
AGENT_VENDOR_TREE=${AGENT_VENDOR_TREE:-e3ae90fe482ba6cad6c3f94069127faf76ebceb6}
RUNTIME_SHA=${RUNTIME_SHA:-95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c}
RUNTIME_TREE=${RUNTIME_TREE:-d3a290b407fa61e6ab2d476f50c068073f70df00}
RUNTIME_VERSION=${RUNTIME_VERSION:-sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac}
ARCHIVE_SHA=${ARCHIVE_SHA:-9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738}
MIN_DISK_BYTES=${MIN_DISK_BYTES:-5000000000}

for d in "$MAIN" "$APP" "$AGENT" "$AGENT_VENDOR" "$RUNTIME" "$GRAPH" "$GRAPH/node_modules" "$PRIVATE" "$EVIDENCE" "$TMP" "$SOCKET" "$SHORT"; do
  [[ -d "$d" && ! -L "$d" ]] || die "missing or symlinked directory: $d"
done
for d in "$PRIVATE" "$EVIDENCE" "$TMP" "$SOCKET" "$SHORT"; do mode700 "$d"; done
[[ ${#TMP} -lt 100 && ${#SOCKET} -lt 100 ]] || die 'temporary directory or socket path is 100 characters or longer'
[[ -x "$NODE" ]] || die "Node is not executable: $NODE"
[[ "$($NODE --version)" == v20.19.4 ]] || die 'Node must be v20.19.4'
[[ -x "$CHROME" ]] || die "Chromium is not executable: $CHROME"
physical_file CREDENTIAL
[[ "$(stat -c '%a' "$CREDENTIAL")" == 600 ]] || die 'Runtime product credential must be mode 0600'

available=$(df -B1 --output=avail "$MAIN" | tail -n 1 | tr -d '[:space:]')
[[ "$available" =~ ^[0-9]+$ && "$available" -ge "$MIN_DISK_BYTES" ]] || die "disk floor failed at $MAIN: ${available:-unknown} < $MIN_DISK_BYTES"

for root in "$APP" "$AGENT" "$AGENT_VENDOR" "$RUNTIME"; do
  [[ -z "$(git_at "$root" status --porcelain --untracked-files=normal)" ]] || die "dirty source checkout: $root"
done
[[ "$(git_at "$APP" rev-parse HEAD)" == "$APP_SHA" ]] || die 'App source HEAD is not the exact r51 source'
[[ "$(git_at "$APP" rev-parse HEAD^{tree})" == "$APP_TREE" ]] || die 'App source tree is not the exact r51 tree'
[[ "$(git_at "$AGENT" rev-parse HEAD)" == "$AGENT_SHA" && "$(git_at "$AGENT" rev-parse HEAD^{tree})" == "$AGENT_TREE" ]] || die 'Agent 6ef source mismatch'
[[ "$(git_at "$AGENT_VENDOR" rev-parse HEAD)" == "$AGENT_VENDOR_SHA" && "$(git_at "$AGENT_VENDOR" rev-parse HEAD^{tree})" == "$AGENT_VENDOR_TREE" ]] || die 'Agent vendor 091 source mismatch'
[[ "$(git_at "$RUNTIME" rev-parse HEAD)" == "$RUNTIME_SHA" && "$(git_at "$RUNTIME" rev-parse HEAD^{tree})" == "$RUNTIME_TREE" ]] || die 'Runtime 95bd source mismatch'

[[ "$(sha256 "$APP/tests/e2e/local/parent-split-command.spec.ts")" == 48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574 ]] || die 'original split spec bytes changed'
[[ "$(sha256 "$APP/playwright.parent-split.config.ts")" == 7eb1bff0269a554f1b9bfd5d750c622cec07b3472827f68290874fc4b690bad4 ]] || die 'parent-split config bytes changed'
[[ "$(sha256 "$APP/scripts/testing/current013-parent-split.mjs")" == 93c0a21a35ca9a6d254aa12ad7150994ff870e1f7eeac4ecf78172d4a05c86b7 ]] || die 'existing split runner bytes changed'
[[ "$(sha256 "$APP/scripts/testing/current013-parent-split.test.mjs")" == 0cd2e7cbbef272e5ac8d8f6ea5e515498fa6dc78c4815c6658a835937b046449 ]] || die 'split runner control bytes changed'

ARCHIVE="$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz"
physical_file ARCHIVE
[[ "$(sha256 "$ARCHIVE")" == "$ARCHIVE_SHA" ]] || die 'Composition public13 archive digest mismatch'
mapfile -t archive_files < <(tar -tzf "$ARCHIVE" | awk '!/\/$/{print}')
[[ ${#archive_files[@]} -eq 77 ]] || die 'Composition archive does not contain exactly 77 regular files'
declare -A seen=()
for member in "${archive_files[@]}"; do
  [[ "$member" == package/* && "$member" != *'/../'* && "$member" != ../* ]] || die "unsafe archive member: $member"
  [[ -z "${seen[$member]:-}" ]] || die "duplicate archive member: $member"
  seen[$member]=1
done

GRAPH_NODE_MODULES=$(realpath "$GRAPH/node_modules")
SHARED_NODE_MODULES=$(realpath /home/user/work/app/node_modules)
[[ "$(realpath "$APP/node_modules")" == "$GRAPH_NODE_MODULES" ]] || die 'App node_modules is not the selected private13 overlay'
[[ "$GRAPH_NODE_MODULES" != "$SHARED_NODE_MODULES" ]] || die 'private13 graph resolves to shared App node_modules'
while IFS= read -r link; do die "private13 graph contains symlink: $link"; done < <(find "$GRAPH_NODE_MODULES" -type l -print)

"$NODE" - "$GRAPH_NODE_MODULES" <<'NODE'
const path = require('node:path');
const root = process.argv[2];
const expected = {
  '@banodoco/timeline-composition': '0.0.13', react: '18.3.1', 'react-dom': '18.3.1',
  remotion: '4.0.509', '@remotion/player': '4.0.509', three: '0.185.1',
  playwright: '1.60.0', '@playwright/test': '1.60.0',
};
for (const [name, version] of Object.entries(expected)) {
  const actual = require(path.join(root, name, 'package.json')).version;
  if (actual !== version) throw new Error(`${name}=${actual}; expected ${version}`);
}
NODE

[[ "$($NODE -p "require('$RUNTIME/contract/artifacts.json').producer")" == astrid-runtime ]] || die 'Runtime manifest producer mismatch'
[[ "$($NODE -p "require('$RUNTIME/contract/artifacts.json').version")" == "$RUNTIME_VERSION" ]] || die 'Runtime manifest digest mismatch'
[[ "$($NODE -p "Object.keys(require('$RUNTIME/contract/artifacts.json').artifacts).length")" == 76 ]] || die 'Runtime manifest is not all76'

physical_file READY
physical_file LEASE
grep -Eq 'status[=:](READY|ACTIVE)|READY' "$READY" || die 'private13 READY marker is not ready'
grep -Eq "graph[=:].*${GRAPH_NODE_MODULES}|node_modules[=:].*${GRAPH_NODE_MODULES}" "$LEASE" || die 'private13 lease does not bind the selected graph'
grep -Eq "${ARCHIVE_SHA}" "$READY" "$LEASE" || die 'private13 READY/LEASE does not bind the public13 archive'
! grep -Eq '(^|[=:])(RELEASED|EXPIRED)($|[[:space:]])' "$READY" "$LEASE" || die 'private13 lease is released or expired'

"$NODE" - "$CREDENTIAL" <<'NODE'
const fs = require('node:fs');
const file = process.argv[2];
const value = JSON.parse(fs.readFileSync(file, 'utf8'));
const forbidden = new Set(['owner', 'astrid-pack-host', 'admin', 'worker']);
if (value.version !== 1 || value.scope !== 'astrid' || typeof value.actor_id !== 'string' || !value.actor_id.trim() || forbidden.has(value.actor_id.trim()) || typeof value.token !== 'string' || !value.token.trim()) throw new Error('credential is not a valid App Runtime product credential');
NODE

for key in ASTRID_PACK_HOST_PYTHON ASTRID_PACK_HOST_HELPER_CHECKOUT; do
  [[ -z "${!key:-}" ]] || die "$key must be unset for the local split lane"
done
command -v ss >/dev/null || die 'ss is required for native port observation'
[[ -z "$(ss -Hln "sport = :$PORT" 2>/dev/null)" ]] || die "native port $PORT is already listening"

export ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_PYTHON=${ASTRID_PYTHON:-/home/user/work/venv-agent/bin/python}
export ASTRID_RUNTIME_PYTHON=${ASTRID_RUNTIME_PYTHON:-/home/user/work/venv-runtime/bin/python}
export TIMELINE_CURRENT013_APP_SHA="$APP_SHA" TIMELINE_CURRENT013_APP_TREE="$APP_TREE"
export TIMELINE_CURRENT013_AGENT_SHA="$AGENT_SHA" TIMELINE_CURRENT013_RUNTIME_SHA="$RUNTIME_SHA"
export TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME"
export PRIVATE13_NODE_MODULES="$GRAPH_NODE_MODULES" TIMELINE_CURRENT013_PRIVATE13_READY="$READY" TIMELINE_CURRENT013_PRIVATE13_LEASE="$LEASE"
export TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" TIMELINE_CURRENT013_CONFIG_PATH="$APP/playwright.parent-split.config.ts"
export PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" WORKSPACE_RUNTIME_TOKEN_FILE="$CREDENTIAL"

for executable in "$ASTRID_PYTHON" "$ASTRID_RUNTIME_PYTHON"; do [[ -x "$executable" ]] || die "Python executable is not available: $executable"; done

cd "$APP"
SOURCE_SNAPSHOT=$(env -i HOME="$MAIN/h" LANG=C.UTF-8 PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  ASTRID_CHECKOUT="$ASTRID_CHECKOUT" ASTRID_RUNTIME_CHECKOUT="$ASTRID_RUNTIME_CHECKOUT" \
  ASTRID_PYTHON="$ASTRID_PYTHON" ASTRID_RUNTIME_PYTHON="$ASTRID_RUNTIME_PYTHON" \
  TIMELINE_CURRENT013_APP_SHA="$APP_SHA" TIMELINE_CURRENT013_APP_TREE="$APP_TREE" \
  TIMELINE_CURRENT013_AGENT_SHA="$AGENT_SHA" TIMELINE_CURRENT013_RUNTIME_SHA="$RUNTIME_SHA" \
  TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" \
  PRIVATE13_NODE_MODULES="$GRAPH_NODE_MODULES" TIMELINE_CURRENT013_PRIVATE13_READY="$READY" TIMELINE_CURRENT013_PRIVATE13_LEASE="$LEASE" \
  TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" TIMELINE_CURRENT013_CONFIG_PATH="$APP/playwright.parent-split.config.ts" \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" WORKSPACE_RUNTIME_TOKEN_FILE="$CREDENTIAL" \
  "$NODE" --input-type=module -e 'import { readCurrent013ParentSplitInputs, checkCurrent013ParentSplitSources } from "./scripts/testing/current013-parent-split.mjs"; const input = readCurrent013ParentSplitInputs(process.env, process.cwd()); console.log(JSON.stringify(checkCurrent013ParentSplitSources(input)));')

CACHE_ID=$(env -i HOME="$MAIN/h" LANG=C.UTF-8 PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  "$NODE" --input-type=module -e 'import { parentSplitCacheIdentity } from "./scripts/testing/current013-parent-split.mjs"; console.log(parentSplitCacheIdentity({ appSha: process.argv[1], appTree: process.argv[2], agentSha: process.argv[3], runtimeSha: process.argv[4] }));' \
  "$APP_SHA" "$APP_TREE" "$AGENT_SHA" "$RUNTIME_SHA")
[[ -n "$CACHE_ID" ]] || die 'existing split runner cache identity is empty'

LIST_ENV=(
  HOME="$MAIN/h" LANG=C.UTF-8 PATH="$(dirname "$NODE"):/usr/bin:/bin"
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" ASTRID_PYTHON="$ASTRID_PYTHON" ASTRID_RUNTIME_PYTHON="$ASTRID_RUNTIME_PYTHON"
  TIMELINE_BUNDLE_AGENT_HEAD="$AGENT_SHA" TIMELINE_BUNDLE_RUNTIME_HEAD="$RUNTIME_SHA"
  PRIVATE13_NODE_MODULES="$GRAPH_NODE_MODULES" PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" WORKSPACE_RUNTIME_TOKEN_FILE="$CREDENTIAL"
)
set +e
LIST_OUTPUT=$(env -i "${LIST_ENV[@]}" npm run test:e2e:three-products -- --config playwright.parent-split.config.ts --list 2>&1)
LIST_STATUS=$?
set -e
[[ "$LIST_STATUS" -eq 0 ]] || die "existing split list1 failed with exit $LIST_STATUS: $LIST_OUTPUT"
[[ $(grep -oF 'M2 native parent split preserves raw closure through lost ACK, restart, retry and Runtime inverse' <<<"$LIST_OUTPUT" | wc -l) -eq 1 ]] || die 'list1 did not select the original split title exactly once'
[[ $(grep -oF 'parent-split-command.spec.ts' <<<"$LIST_OUTPUT" | wc -l) -eq 1 ]] || die 'list1 did not select the original split file exactly once'
grep -Eq 'Total:[[:space:]]*1 test in 1 file' <<<"$LIST_OUTPUT" || die 'list1 is not exactly one test in one file'

SOURCE_POSTFLIGHT=$(env -i HOME="$MAIN/h" LANG=C.UTF-8 PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  ASTRID_CHECKOUT="$ASTRID_CHECKOUT" ASTRID_RUNTIME_CHECKOUT="$ASTRID_RUNTIME_CHECKOUT" ASTRID_PYTHON="$ASTRID_PYTHON" ASTRID_RUNTIME_PYTHON="$ASTRID_RUNTIME_PYTHON" \
  TIMELINE_CURRENT013_APP_SHA="$APP_SHA" TIMELINE_CURRENT013_APP_TREE="$APP_TREE" TIMELINE_CURRENT013_AGENT_SHA="$AGENT_SHA" TIMELINE_CURRENT013_RUNTIME_SHA="$RUNTIME_SHA" \
  TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" PRIVATE13_NODE_MODULES="$GRAPH_NODE_MODULES" \
  TIMELINE_CURRENT013_PRIVATE13_READY="$READY" TIMELINE_CURRENT013_PRIVATE13_LEASE="$LEASE" TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" TIMELINE_CURRENT013_CONFIG_PATH="$APP/playwright.parent-split.config.ts" \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" WORKSPACE_RUNTIME_TOKEN_FILE="$CREDENTIAL" \
  "$NODE" --input-type=module -e 'import { readCurrent013ParentSplitInputs, checkCurrent013ParentSplitSources } from "./scripts/testing/current013-parent-split.mjs"; const input = readCurrent013ParentSplitInputs(process.env, process.cwd()); console.log(JSON.stringify(checkCurrent013ParentSplitSources(input)));')
[[ "$SOURCE_POSTFLIGHT" == "$SOURCE_SNAPSHOT" ]] || die 'source postflight changed during pure preflight'
[[ "$(realpath "$APP/node_modules")" == "$GRAPH_NODE_MODULES" && "$(realpath "$GRAPH/node_modules")" == "$GRAPH_NODE_MODULES" ]] || die 'overlay postflight changed'

printf '%s\n' 'READY preflight: original split actual remains unexecuted.'
printf 'source=%s tree=%s agent=%s runtime=%s archive=%s cache=%s\n' "$APP_SHA" "$APP_TREE" "$AGENT_SHA" "$RUNTIME_SHA" "$ARCHIVE_SHA" "$CACHE_ID"
printf 'list=exactly 1 test in 1 file; native-port=%s clear; pack-host-env=unset; overlay-postflight=stable\n' "$PORT"
printf '%s\n' 'Later actual (do not run until Trim is terminal and wrapper negative proof is accepted):'
printf 'TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_CACHE_ID=%q node scripts/testing/current013-parent-split.mjs\n' "$CACHE_ID"
