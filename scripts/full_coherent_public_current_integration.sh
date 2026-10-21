#!/usr/bin/env bash
# The manager-owned full lane for the exact current public Agent/runtime/C13
# tuple.  This wrapper is intentionally strict: it reports every setup miss
# before invoking pytest, and leaves pytest's normal temporary-directory and
# cache behavior unchanged.
set -euo pipefail

EXPECTED_AGENT_COMMIT=c4b964f6a050edf63a4278d35717e46a88a80386
EXPECTED_AGENT_TREE=d7796be264c341adbcb9765aae374b832dede144
EXPECTED_RUNTIME_COMMIT=b92d3e7a05eec65c142294ef4873edd059e9b31d
EXPECTED_RUNTIME_TREE=6abc2f117391de8e7e35c0283f575a002199894d
EXPECTED_CLIENT_COMMIT=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
EXPECTED_CLIENT_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
EXPECTED_C13_SOURCE=30da0a5e05d4529a2b97b3c1818cf9e15842d628
EXPECTED_C13_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
EXPECTED_NODE=v20.19.4
MIN_FREE_BYTES=$((13 * 1024 * 1024 * 1024))

SOURCE_ROOT=${SOURCE_ROOT:-$PWD}
RUNTIME_CHECKOUT=${ASTRID_RUNTIME_CHECKOUT:-/home/user/work/runtime}
CLIENT_CHECKOUT=${RUNTIME_CLIENT_CHECKOUT:-/home/user/work/wt/rt-pin-95bd3c5f}
COMPOSITION_ROOT=${ASTRID_REMOTION_PROJECT_DIR:-/home/user/work/runtimes/agent-remotion-0013}
NODE=${ASTRID_NODE_EXECUTABLE:-/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node}
VIBECOMFY=${ASTRID_VIBECOMFY_CHECKOUT:-/home/user/work/fixtures/vibecomfy}
PROFILE_ROOT=${FULL_COHERENT_PUBLIC_PROFILE_ROOT:-}
AGENT_WHEEL=${FULL_COHERENT_PUBLIC_AGENT_WHEEL:-}

failures=()
pass() { printf 'PASS %s\n' "$*"; }
fail() { failures+=("$*"); }
require_file() { [ -f "$1" ] && pass "file $1" || fail "missing file: $1"; }
require_dir() { [ -d "$1" ] && pass "directory $1" || fail "missing directory: $1"; }

git_identity() {
  local label=$1 root=$2 commit=$3 tree=$4
  if [ ! -d "$root" ]; then
    fail "$label checkout missing: $root"
    return
  fi
  local actual_commit actual_tree
  actual_commit=$(git -C "$root" rev-parse HEAD 2>/dev/null || true)
  actual_tree=$(git -C "$root" rev-parse HEAD^{tree} 2>/dev/null || true)
  [ "$actual_commit" = "$commit" ] && pass "$label commit $commit" || fail "$label commit expected $commit, got ${actual_commit:-unreadable}"
  [ "$actual_tree" = "$tree" ] && pass "$label tree $tree" || fail "$label tree expected $tree, got ${actual_tree:-unreadable}"
  [ -z "$(git -C "$root" status --porcelain 2>/dev/null)" ] && pass "$label clean" || fail "$label checkout is dirty: $root"
}

git_identity Agent "$SOURCE_ROOT" "$EXPECTED_AGENT_COMMIT" "$EXPECTED_AGENT_TREE"
git_identity Runtime "$RUNTIME_CHECKOUT" "$EXPECTED_RUNTIME_COMMIT" "$EXPECTED_RUNTIME_TREE"
git_identity Runtime-client "$CLIENT_CHECKOUT" "$EXPECTED_CLIENT_COMMIT" "$EXPECTED_CLIENT_TREE"

if [ -f "$SOURCE_ROOT/runtime.lock.json" ]; then
  lock_client=$(sed -n 's/.*"source_commit": "\([^"]*\)".*/\1/p' "$SOURCE_ROOT/runtime.lock.json" | head -1)
  [ "$lock_client" = "$EXPECTED_CLIENT_COMMIT" ] && pass "runtime.lock client source $EXPECTED_CLIENT_COMMIT" || fail "runtime.lock client source expected $EXPECTED_CLIENT_COMMIT, got ${lock_client:-missing}"
else
  fail "missing current source runtime.lock.json"
fi

if [ -n "$PROFILE_ROOT" ]; then
  PROFILE_ROOT=$(realpath "$PROFILE_ROOT" 2>/dev/null || printf '%s' "$PROFILE_ROOT")
  PROFILE_PY="$PROFILE_ROOT/venv/bin/python"
  PROFILE_SITE="$PROFILE_ROOT/venv/lib/python3.13/site-packages"
  PROFILE_JSON="$PROFILE_ROOT/profile/astrid.json"
  require_file "$PROFILE_PY"
  require_dir "$PROFILE_SITE"
  require_file "$PROFILE_JSON"
else
  PROFILE_PY=
  PROFILE_SITE=
  fail 'FULL_COHERENT_PUBLIC_PROFILE_ROOT is not set (current public profile not built)'
fi

if [ -n "$AGENT_WHEEL" ]; then
  require_file "$AGENT_WHEEL"
else
  fail 'FULL_COHERENT_PUBLIC_AGENT_WHEEL is not set (current c4b Agent wheel not built)'
fi

if [ -x "$NODE" ]; then
  [ "$($NODE --version 2>/dev/null)" = "$EXPECTED_NODE" ] && pass "Node $EXPECTED_NODE" || fail "Node expected $EXPECTED_NODE at $NODE, got $($NODE --version 2>/dev/null || printf unreadable)"
else
  fail "missing executable Node: $NODE"
fi
if [ -d "$COMPOSITION_ROOT/node_modules" ]; then pass "C13 node_modules $COMPOSITION_ROOT/node_modules"; else fail "missing C13 node_modules: $COMPOSITION_ROOT/node_modules"; fi
require_file "$COMPOSITION_ROOT/.source-commit"
if [ -f "$COMPOSITION_ROOT/.source-commit" ]; then
  [ "$(tr -d '\n' < "$COMPOSITION_ROOT/.source-commit")" = "$EXPECTED_C13_SOURCE" ] && pass "C13 source $EXPECTED_C13_SOURCE" || fail "C13 source expected $EXPECTED_C13_SOURCE, got $(tr -d '\n' < "$COMPOSITION_ROOT/.source-commit")"
fi
C13_TARBALL="$COMPOSITION_ROOT/artifacts/banodoco-timeline-composition-0.0.13.tgz"
require_file "$C13_TARBALL"
if [ -f "$C13_TARBALL" ]; then
  [ "$(sha256sum "$C13_TARBALL" | cut -d' ' -f1)" = "$EXPECTED_C13_SHA256" ] && pass "C13 artifact $EXPECTED_C13_SHA256" || fail "C13 artifact hash expected $EXPECTED_C13_SHA256"
fi
for tool in /usr/bin/ffmpeg /usr/bin/ffprobe; do require_file "$tool"; done
require_dir "$VIBECOMFY"

free_bytes=$(python3 -c 'import os; s=os.statvfs("/home/user/work"); print(s.f_bavail*s.f_frsize)')
if [ "$free_bytes" -gt "$MIN_FREE_BYTES" ]; then
  pass "disk $free_bytes bytes (>13 GiB admission reserve)"
else
  need_gib=$(python3 -c 'print((13*1024**3-int("'"$free_bytes"'"))/1024**3)')
  fail "STORAGE NEED ${need_gib} GiB for full-coherent-public-current-integration (free ${free_bytes} bytes; requires >13 GiB before profile/full scratch)"
fi

if [ -n "$PROFILE_PY" ] && [ -x "$PROFILE_PY" ] && [ -d "$PROFILE_SITE" ]; then
  PROFILE_ROOT="$PROFILE_ROOT" PROFILE_SITE="$PROFILE_SITE" AGENT_WHEEL="$AGENT_WHEEL" "$PROFILE_PY" -I -B - <<'PY' || fail "profile isolated origin/RECORD/source-byte preflight failed"
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
from zipfile import ZipFile

site = Path(os.environ["PROFILE_SITE"]).resolve()
root = Path(os.environ["PROFILE_ROOT"]).resolve()
if any(path.is_symlink() for path in root.rglob("*")):
    raise SystemExit("profile contains symlinks")
origins = {
    "action": "astrid.packs.rendering.actions.render.run",
    "astrid_runtime": "astrid_runtime",
    "child": "astrid.core.execution.generic_host_worker",
    "client": "astrid_runtime_client",
    "host": "astrid.core.execution.generic_host",
    "runtime_protocol": "runtime_protocol",
    "runtime_protocol.platform": "runtime_protocol.platform",
    "sdk": "astrid.sdk.invocation",
}
found = {}
for label, name in origins.items():
    spec = importlib.util.find_spec(name)
    if spec is None or not spec.origin:
        raise SystemExit(f"missing origin {label}: {name}")
    origin = Path(spec.origin).resolve()
    if site not in origin.parents:
        raise SystemExit(f"origin {label} escaped private site: {origin}")
    found[label] = str(origin)

records = sorted(site.glob("*.dist-info/RECORD"))
if len(records) != 166:
    raise SystemExit(f"expected 166 RECORD files, found {len(records)}")
for record in records:
    with record.open(newline="") as stream:
        for row in csv.reader(stream):
            if not row:
                continue
            raw_target = site / row[0]
            target = raw_target.resolve()
            if raw_target.is_symlink() or site not in target.parents or not target.is_file():
                raise SystemExit(f"invalid RECORD target: {record}: {row[0]}")
            if len(row) > 2 and row[1]:
                algorithm, expected = row[1].split("=", 1)
                if algorithm != "sha256":
                    raise SystemExit(f"unexpected RECORD hash algorithm: {record}: {algorithm}")
                digest = hashlib.sha256(target.read_bytes()).digest()
                import base64
                actual = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
                if actual != expected or str(target.stat().st_size) != row[2]:
                    raise SystemExit(f"RECORD mismatch: {record}: {row[0]}")

expected_versions = {
    "astrid": "0.1.0",
    "astrid-runtime": "0.1.0",
    "astrid-runtime-client": "0.2.14",
    "banodoco-timeline-schema": "0.0.2",
    "numpy": "2.5.2",
    "opencv-python-headless": "5.0.0.93",
    "pillow": "12.3.0",
    "pyyaml": "6.0.3",
}
for name, version in expected_versions.items():
    dist = importlib.metadata.distribution(name)
    if not dist or not dist.files or dist.version != version:
        raise SystemExit(f"distribution {name} expected {version}, got {getattr(dist, 'version', None)}")

profile = json.loads((root / "profile/astrid.json").read_text())
expected_profile = {
    "profile": "astrid",
    "runtime_checkout": str(site),
    "source_checkout": str(site),
    "runtime_environment": str(root / "venv"),
}
if profile != expected_profile:
    raise SystemExit(f"profile shape mismatch: {profile!r}")

wheelhouse = root / "wheelhouse"
wheel_paths = [Path(os.environ["AGENT_WHEEL"]), wheelhouse / "astrid_runtime-0.1.0-py3-none-any.whl", wheelhouse / "astrid_runtime_client-0.2.14-py3-none-any.whl"]
for wheel in wheel_paths:
    if not wheel.is_file():
        raise SystemExit(f"missing product wheel: {wheel}")
    with ZipFile(wheel) as archive:
        for member in archive.infolist():
            if member.is_dir() or member.filename.endswith(".dist-info/RECORD"):
                continue
            raw_target = site / member.filename
            target = raw_target.resolve()
            if raw_target.is_symlink() or site not in target.parents or not target.is_file():
                raise SystemExit(f"wheel target escaped or is not a regular file: {wheel}: {member.filename}")
            if target.read_bytes() != archive.read(member):
                raise SystemExit(f"wheel/install source-byte mismatch: {wheel}: {member.filename}")

print("PASS profile eight origins=" + repr(found))
print("PASS profile RECORD=166 hash-valid")
print("PASS profile exact product versions and wheel/install source bytes")
PY
fi

if [ "${#failures[@]}" -ne 0 ]; then
  printf 'SETUP FAILURES (%s):\n' "${#failures[@]}" >&2
  printf ' - %s\n' "${failures[@]}" >&2
  exit 2
fi

# Keep the original full lane: no integration marker, no cache-provider
# override, no --basetemp override, and no cleanup wrapper.  The central test
# service supplies PYTHONPATH=$PWD for the source snapshot.
export ASTRID_REMOTION_PROJECT_DIR="$COMPOSITION_ROOT"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$PROFILE_SITE"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"
export ASTRID_TEST_NODE_MODULES="$COMPOSITION_ROOT/node_modules"
export ASTRID_VIBECOMFY_CHECKOUT="$VIBECOMFY"
export PYTHONDONTWRITEBYTECODE=1
exec "$PROFILE_PY" -m pytest -q -n 3 "$@"
