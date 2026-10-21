#!/usr/bin/env bash
set -Eeuo pipefail

# Preparation only.  This materializes private source/graph copies and stops
# before the existing qualifier, credential helper, list, or actual may run.

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
MAIN=${MAIN:-/home/user/work/tl-app-main-private-r70}
HUB_REPO=${HUB_REPO:-/home/user/work/app}
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
GRAPH_ARCHIVE=$ORCH/artifacts/app-public13-main-node-modules-r25.tgz
GRAPH_SHA=a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e
SHORT_TMP=${SHORT_TMP:-/tmp/tl-app-main-private-r70}
PORT=17340

APP1490=1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf
APP1490_TREE=8e242d1497841f391b6152ecd8d204143fa03b52
APP0CC=0cc2583aaf07e89190b9344b5ac82849d6279586
APP0CC_TREE=320e74a93676c781e83885b86ec237b4a1465d80
APP92C=92c30b570cf8105dc021a64874c258e6c950b841
APP92C_TREE=c34d65b66481fd0015279451b175c53b7b5e8f4f
AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
AGENT_VENDOR_SHA=091aa23ec83ea05ffd3b0115a640230d51c8c429
AGENT_VENDOR_TREE=e3ae90fe482ba6cad6c3f94069127faf76ebceb6
RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00

die() { printf 'materialize: %s\n' "$*" >&2; exit 1; }
need_file() { test -f "$1" || die "missing file: $1"; }
need_dir() { test -d "$1" || die "missing directory: $1"; }
mode700() { test "$(stat -c %a "$1")" = 700 || die "not mode 0700: $1"; }
clean_repo() { test -z "$(git -C "$1" status --porcelain)" || die "dirty keeper: $1"; }

test ! -e "$MAIN" || die "refusing to overwrite existing MAIN: $MAIN"
test ! -e "$SHORT_TMP" || die "refusing to overwrite existing short temp: $SHORT_TMP"
need_file "$NODE"
test "$("$NODE" --version)" = v20.19.4 || die "wrong Node at $NODE"
need_file "$GRAPH_ARCHIVE"
test "$(sha256sum "$GRAPH_ARCHIVE" | awk '{print $1}')" = "$GRAPH_SHA" || die "graph archive SHA mismatch"
need_dir "$HUB_REPO"

AGENT=${AGENT:-/home/user/work/wt/agt-pin-6efc8150}
AGENT_VENDOR=${AGENT_VENDOR:-/home/user/work/wt/agt-pin-091aa23e}
RUNTIME=${RUNTIME:-/home/user/work/wt/rt-pin-95bd3c5f}
APP1490_KEEPER=${APP1490_KEEPER:-/home/user/work/wt/app-pin-1490fbfe}
APP0CC_KEEPER=${APP0CC_KEEPER:-/home/user/work/wt/app-pin-0cc2583a}
APP92C_KEEPER=${APP92C_KEEPER:-/home/user/work/wt/app-pin-92c30b57}

for pair in \
  "$AGENT:$AGENT_SHA:$AGENT_TREE" \
  "$AGENT_VENDOR:$AGENT_VENDOR_SHA:$AGENT_VENDOR_TREE" \
  "$RUNTIME:$RUNTIME_SHA:$RUNTIME_TREE"; do
  IFS=: read -r repo sha tree <<< "$pair"
  need_dir "$repo"
  clean_repo "$repo"
  test "$(git -C "$repo" rev-parse HEAD)" = "$sha" || die "keeper commit mismatch: $repo"
  test "$(git -C "$repo" rev-parse HEAD^{tree})" = "$tree" || die "keeper tree mismatch: $repo"
done

# Read-only object and publication checks.  No fetch is permitted here.
for app_pair in \
  "$APP1490_KEEPER:$APP1490:$APP1490_TREE" \
  "$APP0CC_KEEPER:$APP0CC:$APP0CC_TREE" \
  "$APP92C_KEEPER:$APP92C:$APP92C_TREE"; do
  IFS=: read -r keeper sha tree <<< "$app_pair"
  need_dir "$keeper"
  clean_repo "$keeper"
  test "$(git -C "$keeper" rev-parse HEAD)" = "$sha" || die "App keeper commit mismatch: $keeper"
  test "$(git -C "$keeper" rev-parse HEAD^{tree})" = "$tree" || die "App keeper tree mismatch: $keeper"
  git -C "$HUB_REPO" cat-file -e "$sha^{commit}" || die "App object absent from hub repository: $sha"
  git -C "$HUB_REPO" merge-base --is-ancestor "$sha" refs/remotes/hub/timeline/app/tl/integration || die "App commit is not reachable from existing hub integration ref: $sha"
done

need_file /home/user/work/venv-agent/bin/python
need_file /home/user/work/venv-runtime/bin/python
test "$(stat -c %a /home/user/work/venv-agent/bin/python)" != 000 || die "unusable Agent venv"
test "$(stat -c %a /home/user/work/venv-runtime/bin/python)" != 000 || die "unusable Runtime venv"

mkdir -p "$MAIN" "$MAIN/cases" "$MAIN/evidence" "$MAIN/home" "$MAIN/run" "$MAIN/cache"
chmod 700 "$MAIN" "$MAIN/cases" "$MAIN/evidence" "$MAIN/home" "$MAIN/run" "$MAIN/cache"
for root in evidence home run cache; do mode700 "$MAIN/$root"; done
mkdir "$SHORT_TMP"
chmod 700 "$SHORT_TMP"
mode700 "$SHORT_TMP"

materialize_case() {
  local label=$1 keeper=$2 sha=$3 tree=$4 dest="$MAIN/cases/$1"
  mkdir -p "$dest"
  chmod 700 "$dest"
  git clone --no-local --no-hardlinks --no-checkout "$keeper" "$dest/source" >/dev/null
  git -C "$dest/source" checkout --detach "$sha" >/dev/null
  clean_repo "$dest/source"
  test "$(git -C "$dest/source" rev-parse HEAD)" = "$sha" || die "materialized commit mismatch: $label"
  test "$(git -C "$dest/source" rev-parse HEAD^{tree})" = "$tree" || die "materialized tree mismatch: $label"
  mkdir -p "$dest/evidence" "$dest/home" "$dest/run" "$dest/cache"
  chmod 700 "$dest" "$dest/evidence" "$dest/home" "$dest/run" "$dest/cache"
  test ! -e "$dest/source/node_modules" || die "source keeper already has a graph: $label"
  tar -xzf "$GRAPH_ARCHIVE" --no-same-owner --no-same-permissions -C "$dest/source"
  test -d "$dest/source/node_modules" || die "graph missing after extraction: $label"
  test "$(realpath "$dest/source/node_modules")" != "$(realpath /home/user/work/app/node_modules)" || die "shared node_modules selected: $label"
  test -z "$(find "$dest/source/node_modules" -type l -print -quit)" || die "graph contains a link: $label"
  for pkg_ver in \
    '@banodoco/timeline-composition:0.0.13' \
    'react:18.3.1' \
    'react-dom:18.3.1' \
    'remotion:4.0.509' \
    '@remotion/player:4.0.509' \
    'three:0.185.1' \
    'playwright:1.60.0' \
    '@playwright/test:1.60.0'; do
    IFS=: read -r pkg ver <<< "$pkg_ver"
    got=$(NODE_PATH="$dest/source/node_modules" "$NODE" -e "console.log(require('$pkg/package.json').version)")
    test "$got" = "$ver" || die "package version mismatch $pkg in $label: $got"
  done
  test ! -e "$dest/source/READY" || die "refusing to copy stale READY: $label"
  test ! -e "$dest/source/LEASE" || die "refusing to copy stale LEASE: $label"
}

materialize_case auto1490 "$APP1490_KEEPER" "$APP1490" "$APP1490_TREE"
materialize_case Trim0cc "$APP0CC_KEEPER" "$APP0CC" "$APP0CC_TREE"
materialize_case split92c "$APP92C_KEEPER" "$APP92C" "$APP92C_TREE"

cat > "$MAIN/preparation.env" <<EOF
MAIN=$MAIN
NODE=$NODE
AGENT=$AGENT
AGENT_VENDOR=$AGENT_VENDOR
RUNTIME=$RUNTIME
AGENT_PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
GRAPH_ARCHIVE=$GRAPH_ARCHIVE
GRAPH_SHA=$GRAPH_SHA
AUTO1490_APP=$MAIN/cases/auto1490/source
TRIM0CC_APP=$MAIN/cases/Trim0cc/source
SPLIT92C_APP=$MAIN/cases/split92c/source
SHORT_TMP=$SHORT_TMP
PORT=$PORT
EOF
chmod 600 "$MAIN/preparation.env"

cat >&2 <<EOF
Materialized private App source and physical graph roots under $MAIN.
STOP: run the existing r25 graph qualifier and the existing r69 normal
credential helper; this script intentionally does not create READY, LEASE,
credentials, servers, browsers, build output, installs, or actual evidence.
EOF
