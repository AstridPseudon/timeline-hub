#!/bin/sh
# Source-only CAS preflight.  It never writes to the installed Store.
set -eu

if [ "$#" -ne 2 ]; then
  echo "usage: $0 REPO PREIMAGE_REF" >&2
  exit 2
fi

repo=$1
preimage=$2
expected=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2
actual=$(git -C "$repo" show "$preimage:ops-d131/bench_store.py" | sha256sum | cut -d' ' -f1)
[ "$actual" = "$expected" ] || { echo "CAS preimage mismatch" >&2; exit 1; }
[ "$(stat -c '%a' "$repo/ops-d131/bench_store.py")" = 755 ] || { echo "source mode mismatch" >&2; exit 1; }
echo "PASS: preimage $actual and mode 755; no installation performed"
