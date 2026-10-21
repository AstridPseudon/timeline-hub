# App2 parent viewport: executable MAIN handoff

Status: SOURCE CLOSED; MAIN PREFLIGHT AND ACTUAL NOT RUN. This packet is not
READY until the unresolved prerequisites below are closed by the manager.

## Exact source role

The harness-committed App source is:

```text
parent_role_sha=6707a30f14bf3a5ee19cb9e481b7dbd95b77522a
parent_role_tree=6ff32d797f0e774b8574274a3494ce8755fa160c
source_file=tests/e2e/local/three-products.spec.ts
source_blob=e612c18cac2a651e855e75388498762f034dc63a
pointer_ancestor=44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0
donor_commit=9018c733c429f3ad176bebf26c6351fce0414da1
donor_spec_blob=e612c18cac2a651e855e75388498762f034dc63a
```

The source is the original parent mounted ADD journey plus the 0952 fixture
geometry correction. It retains pointer `22.5`, centered left edge `20`,
target row V1, both real File/DataTransfer drops, strict full 404 body,
native `clip.add-media`, exact retry, restart/recovery, undo, raw/opaque/
order/source/epoch/ACK/hold, and zero-legacy assertions. No live caller changed.

Frozen R4 provenance is unchanged:

```text
agent       11caf1d9de291d76f491cf69f7942606b7471d7a
runtime     31c7ac3a00f7a205f507bf5bd4d4625628d429bd
app         8f0c2484463e9b666d184a744d52e252984e551a
composition c82eb7c459d0a41263954bf007071a6a0e8e0a6a
```

## Main custody and current environment facts

Do not use moving `/home/user/work/app` as `APP_ROOT`. Request the exact
detached source through the existing mechanism, then use the returned path:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout   app 6707a30f14bf3a5ee19cb9e481b7dbd95b77522a   "freeze parent viewport source for one MAIN preflight"
```

The manager must set `APP_ROOT` to that clean detached checkout, preserve its
`KEEP` marker, and never substitute a synthetic commit or moving branch.
`/home/user/work/app/node_modules` is dependency-only, read-only material; it
is not the source root.

HOME's current concrete Main packets identify these tool paths:

```text
NODE=/opt/node20/bin/node                 # must report v20.19.4
NODE_SHA256=43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
AGENT_PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
CHROMIUM_SHA256=85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95
CHROMIUM_VERSION=Chromium 141.0.7390.37
GRAPH_ROOT=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned
GRAPH=${GRAPH_ROOT}/node_modules
```

The graph must have its existing READY/LEASE controls, be a real symlink-free
directory, and contain the exact public13 package set with Playwright 1.60.0.
The existing source runner requires the graph's exact source archive separately;
the manager must supply its existing absolute path as
`NORMAL014_LOCKED_GRAPH_ARCHIVE`, with SHA-256
`895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
No archive path is guessed here.

Other immutable final95 inputs remain Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, Runtime/producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, manifest count 76,
manifest `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
and Composition 0.0.13 archive
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
with 77 regular members.

## Absolute executable artifacts

The shared helper remains byte-identical and read-only:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
sha256=96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
```

The following worker-owned absolute artifacts are data-bound copies. Their
only changes are source identity/path bindings; approved runner guards,
retention, failure packets, and cleanup remain intact:

```text
bound helper     /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-source-common.bound.sh
                 sha256=2b3b67bfd29e76d66f05e7c473eff80b6bd9f9609b4dcba4bf2d4cd2dcac59b1
bound App runner /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-app-central.bound.sh
                 sha256=803fedad9aa2159ce2046fbdbe841b9ed7309d4bd63edae9cf359988964ab0c4
bound source    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-parent-media-central.bound.sh
                 sha256=9873e8dc50ae9b4dbce84b3a03a74f2eda1d92bf077842e59782f49611573a35
driver          /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-run-parent-manual-drop-evidence.sh
                 sha256=a91bef93c84b1ae8cc2dcfaf9afcc29ce46f1878214fe2b9f8c67968843abe65
gate            /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-final-keeper-gate.sh
                 sha256=1370f563689546b09e3a50aea66c341b939163e20390e445bb8a82fb3b31c81a
```

The shared helper is not mutated. The bound helper requires
`NORMAL014_LOCKED_GRAPH` and `NORMAL014_LOCKED_GRAPH_ARCHIVE` explicitly,
and the gate creates all disposable source/list/TMP roots under a short
`/tmp/tl-pv-*` parent. The long absolute design/evidence path is never a
socket root.

## Executable aggregate preflight

Run this once on the exact detached `APP_ROOT`, before any actual. It must
fail closed if any prerequisite is absent; do not replace unresolved values
with local Node 22, a guessed graph archive, a moving source, or a new
wrapper.

```sh
set -eu
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
APP_ROOT=${APP_ROOT:?set APP_ROOT to the request-checkout result}
NODE=/opt/node20/bin/node
AGENT_PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
GRAPH_ROOT=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned
GRAPH="$GRAPH_ROOT/node_modules"
ARCHIVE=${NORMAL014_LOCKED_GRAPH_ARCHIVE:?set the exact existing public13 graph archive}
RUN_SHORT=tl-pv-${RANDOM:-1116}
RUN_ROOT_PARENT=/tmp/$RUN_SHORT
TMPDIR="$RUN_ROOT_PARENT/tmp"
XDG_RUNTIME_DIR="$RUN_ROOT_PARENT/xdg"
EVIDENCE_ROOT="$ORCH/workers/ap2-m2-parent-viewport-durable-main-finalize-1116/evidence/$RUN_SHORT"
GATE="$ORCH/design/ap2-m2-parent-viewport-durable-main-finalize-1116-final-keeper-gate.sh"
DRIVER="$ORCH/design/ap2-m2-parent-viewport-durable-main-finalize-1116-run-parent-manual-drop-evidence.sh"
mkdir -p "$RUN_ROOT_PARENT/home" "$TMPDIR" "$XDG_RUNTIME_DIR" "$EVIDENCE_ROOT"
chmod 700 "$RUN_ROOT_PARENT" "$RUN_ROOT_PARENT/home" "$TMPDIR" "$XDG_RUNTIME_DIR" "$EVIDENCE_ROOT"
test "${#TMPDIR}" -lt 100
test "${#XDG_RUNTIME_DIR}" -lt 100
test "$(realpath "$APP_ROOT")" != /home/user/work/app
test "$(git -C "$APP_ROOT" rev-parse HEAD)" = 6707a30f14bf3a5ee19cb9e481b7dbd95b77522a
test "$(git -C "$APP_ROOT" rev-parse 'HEAD^{tree}')" = 6ff32d797f0e774b8574274a3494ce8755fa160c
test -z "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)"
test -f "$APP_ROOT/KEEP"
test "$(realpath "$APP_ROOT/node_modules")" = /home/user/work/app/node_modules
test -x "$NODE"
test "$(sha256sum "$NODE" | cut -d' ' -f1)" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
test "$("$NODE" --version)" = v20.19.4
test -x "$AGENT_PYTHON" && test -x "$RUNTIME_PYTHON"
test -d "$GRAPH" && test "$(realpath "$GRAPH")" = "$GRAPH"
test -f "$GRAPH_ROOT/READY" && test -f "$GRAPH_ROOT/LEASE"
test -f "$ARCHIVE"
test "$(sha256sum "$ARCHIVE" | cut -d' ' -f1)" = 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
test -z "$(find -P "$GRAPH" -type l -print -quit)"
test "$("$NODE" -p "require('$GRAPH/@banodoco/timeline-composition/package.json').version")" = 0.0.13
test "$("$NODE" -p "require('$GRAPH/@playwright/test/package.json').version")" = 1.60.0
test "$(sha256sum "$APP_ROOT/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | cut -d' ' -f1)" = 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
test "$(tar -tzf "$APP_ROOT/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | awk '!/\/$/ {n++} END {print n+0}')" = 77
test "$(sha256sum "$GATE" | cut -d' ' -f1)" = 1370f563689546b09e3a50aea66c341b939163e20390e445bb8a82fb3b31c81a
test "$(sha256sum "$DRIVER" | cut -d' ' -f1)" = a91bef93c84b1ae8cc2dcfaf9afcc29ce46f1878214fe2b9f8c67968843abe65
sh -n "$GATE" "$DRIVER"   "$ORCH/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-source-common.bound.sh"   "$ORCH/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-app-central.bound.sh"   "$ORCH/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-parent-media-central.bound.sh"
test "$(realpath "$NODE")" = /opt/node20/bin/node
test "$(realpath /opt/pw-browsers/chromium-1194/chrome-linux/chrome)" = /opt/pw-browsers/chromium-1194/chrome-linux/chrome
flock -n /home/user/work/.app-m1-browser.lock -c :
test "$(df -Pk /tmp | awk 'NR==2 {print $4}')" -ge 10485760
test "$(df -Pk /home/user/work | awk 'NR==2 {print $4}')" -ge 10485760
(
  cd "$APP_ROOT"
  env -i HOME="$RUN_ROOT_PARENT/home" LANG=C.UTF-8   PATH=/opt/node20/bin:/usr/bin:/bin   NODE="$NODE" TMPDIR="$TMPDIR" XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"   NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent   NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE="$AGENT_PYTHON"   NORMAL014_LOCKED_GRAPH="$GRAPH_ROOT" NORMAL014_LOCKED_GRAPH_ARCHIVE="$ARCHIVE"   APP_ROOT="$APP_ROOT" NORMAL014_RECORD_ROOT="$EVIDENCE_ROOT"   NORMAL014_RUN_ROOT_PARENT="$RUN_ROOT_PARENT"   ASTRID_PYTHON="$AGENT_PYTHON" ASTRID_RUNTIME_PYTHON="$RUNTIME_PYTHON"   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome   sh "$DRIVER" probe
  env -i HOME="$RUN_ROOT_PARENT/home" LANG=C.UTF-8   PATH=/opt/node20/bin:/usr/bin:/bin   TMPDIR="$TMPDIR" XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"   NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent   NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE="$AGENT_PYTHON"   NORMAL014_LOCKED_GRAPH="$GRAPH_ROOT" NORMAL014_LOCKED_GRAPH_ARCHIVE="$ARCHIVE"   APP_ROOT="$APP_ROOT" NORMAL014_RECORD_ROOT="$EVIDENCE_ROOT"   NORMAL014_RUN_ROOT_PARENT="$RUN_ROOT_PARENT"   ASTRID_PYTHON="$AGENT_PYTHON" ASTRID_RUNTIME_PYTHON="$RUNTIME_PYTHON"   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome   sh "$GATE" preflight
)
```

This aggregate verifies source/tree/cleanliness/KEEP, dependency resolution,
graph/READY/LEASE/archive/77-member Composition facts, exact Node 20.19.4
and Chromium identity, frozen lock inputs (through the existing source
runner), argv/config/list-1, lock availability, forbidden inherited
environment (the `env -i` child), physical short roots, and evidence-first
failure retention. The `probe` also exercises zero-test refusal and
evidence-before-cleanup. It does not start a browser, Runtime socket, service,
build, install, or actual journey.

## One later actual (manager-authorized only)

Only after the aggregate preflight exits 0, run exactly once with the same
fresh `APP_ROOT`, `ARCHIVE`, `RUN_ROOT_PARENT`, and evidence directory:

```sh
(
  cd "$APP_ROOT"
  env -i HOME="$RUN_ROOT_PARENT/home" LANG=C.UTF-8   PATH=/opt/node20/bin:/usr/bin:/bin   TMPDIR="$TMPDIR" XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"   NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent   NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE="$AGENT_PYTHON"   NORMAL014_LOCKED_GRAPH="$GRAPH_ROOT" NORMAL014_LOCKED_GRAPH_ARCHIVE="$ARCHIVE"   APP_ROOT="$APP_ROOT" NORMAL014_RECORD_ROOT="$EVIDENCE_ROOT"   NORMAL014_RUN_ROOT_PARENT="$RUN_ROOT_PARENT"   ASTRID_PYTHON="$AGENT_PYTHON" ASTRID_RUNTIME_PYTHON="$RUNTIME_PYTHON"   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome   sh "$GATE" run
)
```

This is the sole browser/build/socket/service execution. Preserve the failure
packet if it fails; do not retry or relabel a partial body as qualification.
The gate's existing driver retains source identity, exact retry/restart/undo
and zero-legacy evidence, and copies bounded trace/error context before
trap-cleaning disposable roots.

## Unresolved prerequisites

All must be resolved together before any `run` command:

1. This worker cannot bind `APP_ROOT` to the manager's exact detached
   request-checkout, so source custody is not yet executable here.
2. This worker does not have the HOME-owned exact Node 20.19.4 binary,
   Agent/Runtime venvs, or private graph; local Node 22 is not an allowed
   substitute. The exact `/opt/node20/bin/node` version/hash must be checked
   by MAIN.
3. The current HOME packet identifies the private graph root and its READY/
   LEASE, but does not publish the graph archive path. MAIN must provide that
   existing path and verify the fixed `895c...` hash; no worker-local graph
   artifact may be used.
4. The detached source's read-only dependency attachment and the shared
   node_modules before/after manifest must pass. No shared dependency/cache
   writes are allowed.
5. The real mounted 404/ADD/retry/restart/undo/zero-legacy behavior remains
   unverified because this task intentionally ran no actual.

Until all five close, this packet is **NOT READY**, not a product
qualification result.
