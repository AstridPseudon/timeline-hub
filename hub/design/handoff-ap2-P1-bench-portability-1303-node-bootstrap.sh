#!/bin/bash
# Host-only exact Node selector/bootstrap for the make-runtime route.
# The dispatcher may provide RUNTIME_NODE_BIN; otherwise use the canonical
# immutable archive already staged by the host. This script never downloads.
set -u -o pipefail

W=${RUNTIME_WORK_ROOT:-/home/user/work}
NODE_VERSION=20.19.4
NPM_VERSION=10.8.2
NODE_DIR=$W/toolchain/node-v$NODE_VERSION-linux-x64
NODE_BIN=${RUNTIME_NODE_BIN:-$NODE_DIR/bin}
ARCHIVE=$W/toolchain/dl/node-v$NODE_VERSION-linux-x64.tar.xz
ARCHIVE_SHA=7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4

verify() {
  [ -x "$1/node" ] && [ -x "$1/npm" ] || return 1
  [ "$($1/node --version 2>/dev/null)" = "v$NODE_VERSION" ] || return 1
  [ "$(PATH="$1:$PATH" "$1/npm" --version 2>/dev/null)" = "$NPM_VERSION" ]
}

if verify "$NODE_BIN"; then
  printf '%s\n' "$NODE_BIN"
  exit 0
fi

[ -e "$NODE_DIR" ] && { echo "REFUSED: existing Node path is not exact: $NODE_DIR" >&2; exit 2; }
[ -f "$ARCHIVE" ] || { echo "REFUSED: canonical Node archive missing: $ARCHIVE" >&2; exit 2; }
[ "$(sha256sum "$ARCHIVE" | cut -d' ' -f1)" = "$ARCHIVE_SHA" ] || { echo "REFUSED: canonical Node archive checksum mismatch" >&2; exit 2; }

PARTIAL=$NODE_DIR.partial.$$
[ -e "$PARTIAL" ] && { echo "REFUSED: partial path already exists: $PARTIAL" >&2; exit 2; }
mkdir -p "$PARTIAL"
tar -xJf "$ARCHIVE" -C "$PARTIAL" --no-same-owner
[ -d "$PARTIAL/node-v$NODE_VERSION-linux-x64" ] || { echo "REFUSED: archive layout is not canonical; partial retained: $PARTIAL" >&2; exit 2; }
mv -T "$PARTIAL/node-v$NODE_VERSION-linux-x64" "$NODE_DIR"
verify "$NODE_DIR/bin" || { echo "REFUSED: extracted Node toolchain failed exact version check: $NODE_DIR" >&2; exit 2; }
printf '%s\n' "$NODE_DIR/bin"
