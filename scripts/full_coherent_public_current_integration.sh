#!/usr/bin/env bash
# The manager-owned full lane for the exact current public Agent/runtime/C13
# tuple.  This wrapper is intentionally strict: it reports every setup miss
# before invoking pytest, and leaves pytest's normal temporary-directory and
# cache behavior unchanged.
set -euo pipefail

EXPECTED_AGENT_COMMIT=b3c96a758c1cfa2a609d1498e0e9ee401b32cc40
EXPECTED_AGENT_TREE=3467b7bffb0fe6edf9178c9a9de4d446c8ab8857
EXPECTED_RUNTIME_COMMIT=b92d3e7a05eec65c142294ef4873edd059e9b31d
EXPECTED_RUNTIME_TREE=6abc2f117391de8e7e35c0283f575a002199894d
EXPECTED_CLIENT_COMMIT=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
EXPECTED_CLIENT_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
EXPECTED_C13_SOURCE=30da0a5e05d4529a2b97b3c1818cf9e15842d628
EXPECTED_C13_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
EXPECTED_NODE=v20.19.4
EXPECTED_CONSTRAINTS=164
EXPECTED_CONSTRAINTS_SHA256=478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761
MIN_FREE_BYTES=$((13 * 1024 * 1024 * 1024))

SOURCE_ROOT=${SOURCE_ROOT:-$PWD}
RUNTIME_CHECKOUT=${ASTRID_RUNTIME_CHECKOUT:-/home/user/work/runtime}
CLIENT_CHECKOUT=${RUNTIME_CLIENT_CHECKOUT:-/home/user/work/wt/rt-pin-95bd3c5f}
COMPOSITION_ROOT=${ASTRID_REMOTION_PROJECT_DIR:-/home/user/work/runtimes/agent-remotion-0013}
NODE=${ASTRID_NODE_EXECUTABLE:-/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node}
VIBECOMFY=${ASTRID_VIBECOMFY_CHECKOUT:-/home/user/work/fixtures/vibecomfy}
PROFILE_ROOT=${FULL_COHERENT_PUBLIC_PROFILE_ROOT:-}
AGENT_WHEEL=${FULL_COHERENT_PUBLIC_AGENT_WHEEL:-}
PINS_FILE=${FULL_COHERENT_PUBLIC_PINS:-}

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
  PINS_FILE=${PINS_FILE:-$PROFILE_ROOT/metadata/venv-agent-child-s2.txt}
  require_file "$PROFILE_PY"
  require_dir "$PROFILE_SITE"
  require_file "$PROFILE_JSON"
  require_file "$PINS_FILE"
else
  PROFILE_PY=
  PROFILE_SITE=
  PINS_FILE=
  fail 'FULL_COHERENT_PUBLIC_PROFILE_ROOT is not set (current public profile not built)'
fi

if [ -n "$AGENT_WHEEL" ]; then
  require_file "$AGENT_WHEEL"
else
  fail 'FULL_COHERENT_PUBLIC_AGENT_WHEEL is not set (current b3c Agent wheel not built)'
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

if [ -n "$PROFILE_PY" ] && [ -x "$PROFILE_PY" ] && [ -d "$PROFILE_SITE" ] && [ -n "$AGENT_WHEEL" ] && [ -n "$PINS_FILE" ]; then
  PROFILE_ROOT="$PROFILE_ROOT" PROFILE_SITE="$PROFILE_SITE" PINS_FILE="$PINS_FILE" AGENT_WHEEL="$AGENT_WHEEL" \
    RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" CLIENT_CHECKOUT="$CLIENT_CHECKOUT" \
    EXPECTED_AGENT_COMMIT="$EXPECTED_AGENT_COMMIT" EXPECTED_RUNTIME_COMMIT="$EXPECTED_RUNTIME_COMMIT" \
    EXPECTED_CLIENT_COMMIT="$EXPECTED_CLIENT_COMMIT" EXPECTED_CONSTRAINTS="$EXPECTED_CONSTRAINTS" \
    EXPECTED_CONSTRAINTS_SHA256="$EXPECTED_CONSTRAINTS_SHA256" "$PROFILE_PY" -I -B - <<'PY' || fail "profile isolated origin/RECORD/source-byte preflight failed"
import base64
import csv
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import tarfile
from io import BytesIO
from pathlib import Path
from pathlib import PurePosixPath
from zipfile import ZipFile

site = Path(os.environ["PROFILE_SITE"]).resolve()
root = Path(os.environ["PROFILE_ROOT"]).resolve()
if not site.is_dir() or site.is_symlink() or any(path.is_symlink() for path in root.rglob("*")):
    raise SystemExit("profile contains missing roots or symlinks")

def rel_target(raw: str, owner: Path) -> Path:
    parsed = PurePosixPath(raw)
    if parsed.is_absolute() or ".." in parsed.parts or "" in raw.split("/") or "\\" in raw:
        raise SystemExit(f"unsafe RECORD target: {owner}: {raw}")
    target = (site / Path(*parsed.parts)).resolve()
    if site not in target.parents or not target.is_file() or (site / Path(*parsed.parts)).is_symlink():
        raise SystemExit(f"invalid RECORD target: {owner}: {raw}")
    return target

def record_rows(record: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    with record.open(newline="") as stream:
        for row in csv.reader(stream):
            if len(row) != 3 or not row[0] or row[0] in rows:
                raise SystemExit(f"malformed or duplicate RECORD row: {record}")
            target = rel_target(row[0], record)
            if row[1]:
                algorithm, expected = row[1].split("=", 1)
                if algorithm != "sha256":
                    raise SystemExit(f"unexpected RECORD hash algorithm: {record}: {algorithm}")
                actual = base64.urlsafe_b64encode(hashlib.sha256(target.read_bytes()).digest()).rstrip(b"=").decode()
                if actual != expected or str(target.stat().st_size) != row[2]:
                    raise SystemExit(f"RECORD mismatch: {record}: {row[0]}")
            elif row[2]:
                raise SystemExit(f"unhashed RECORD row has a size: {record}: {row[0]}")
            rows[row[0]] = (row[1], row[2])
    return rows

records = sorted(site.rglob("*.dist-info/RECORD"))
if len(records) != 166:
    raise SystemExit(f"expected 166 RECORD files, found {len(records)}")
record_targets: set[str] = set()
for record in records:
    record_targets.update(record_rows(record))
actual_files = {
    path.relative_to(site).as_posix()
    for path in site.rglob("*")
    if path.is_file() and not path.is_symlink()
}
if actual_files != record_targets:
    raise SystemExit(
        "RECORD closure differs from installed files: "
        f"missing={sorted(actual_files - record_targets)[:3]} "
        f"extra={sorted(record_targets - actual_files)[:3]}"
    )

constraint_file = Path(os.environ["PINS_FILE"])
if not constraint_file.is_file() or constraint_file.is_symlink():
    raise SystemExit(f"constraint carrier is not a regular file: {constraint_file}")
if hashlib.sha256(constraint_file.read_bytes()).hexdigest() != os.environ["EXPECTED_CONSTRAINTS_SHA256"]:
    raise SystemExit("164-pin constraint carrier hash differs from the settled 0908 carrier")
constraints = [line.split(";", 1)[0].strip() for line in constraint_file.read_text().splitlines() if line.strip() and not line.lstrip().startswith("#")]
if len(constraints) != int(os.environ["EXPECTED_CONSTRAINTS"]) or len(set(constraints)) != len(constraints):
    raise SystemExit(f"expected {os.environ['EXPECTED_CONSTRAINTS']} unique constraints, found {len(constraints)}")

def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()

dists = list(importlib.metadata.distributions(path=[str(site)]))
if len(dists) != 166:
    raise SystemExit(f"expected 166 installed distributions, found {len(dists)}")
by_name = {normalized(str(dist.metadata.get("Name", ""))): dist for dist in dists}
if len(by_name) != len(dists):
    raise SystemExit("installed distribution names are not unique")
constraint_names = set()
for constraint in constraints:
    match = re.match(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:==([^ ]+)|\s*@\s*(.+))?$", constraint)
    if not match:
        raise SystemExit(f"unparseable constraint: {constraint}")
    name, version, source = match.groups()
    key = normalized(name)
    constraint_names.add(key)
    dist = by_name.get(key)
    if dist is None:
        raise SystemExit(f"constraint distribution is absent: {name}")
    if version and dist.version != version:
        raise SystemExit(f"constraint version differs: {name} expected {version}, got {dist.version}")
    if source and "@" in source:
        commit = source.rsplit("@", 1)[-1].split("#", 1)[0]
        if re.fullmatch(r"[0-9a-f]{40}", commit):
            direct = dist.read_text("direct_url.json")
            if not direct or json.loads(direct).get("vcs_info", {}).get("commit_id") != commit:
                raise SystemExit(f"VCS constraint source differs: {name} expected {commit}")
expected_product_names = {"astrid-runtime", "astrid-runtime-client"}
if set(by_name) != constraint_names | expected_product_names:
    raise SystemExit("installed distributions are not exactly the 164-pin closure plus Runtime/client")

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
    dist = by_name.get(normalized(name))
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

def wheel_rows(wheel: Path) -> tuple[str, dict[str, tuple[str, str]], dict[str, bytes]]:
    with ZipFile(wheel) as archive:
        record_names = [name for name in archive.namelist() if name.endswith(".dist-info/RECORD")]
        if len(record_names) != 1:
            raise SystemExit(f"wheel must contain exactly one RECORD: {wheel}")
        record_name = record_names[0]
        rows = {}
        for row in csv.reader(archive.read(record_name).decode("utf-8").splitlines()):
            if len(row) != 3 or not row[0] or row[0] in rows:
                raise SystemExit(f"malformed wheel RECORD: {wheel}")
            rows[row[0]] = (row[1], row[2])
        members = {name for name in archive.namelist() if not name.endswith("/")}
        if set(rows) != members:
            raise SystemExit(f"wheel RECORD does not enumerate exactly its members: {wheel}")
        for name in members:
            parsed = PurePosixPath(name)
            if parsed.is_absolute() or ".." in parsed.parts or "" in name.split("/") or "\\" in name:
                raise SystemExit(f"unsafe wheel member path: {wheel}: {name}")
        return record_name, rows, {name: archive.read(name) for name in members}

def canonical_package_bytes(
    entries: dict[str, bytes],
    source_roots: dict[str, str],
    label: str,
    *,
    allow_dist_info: bool,
) -> dict[str, bytes]:
    """Map one package's known source roots into its wheel namespace."""
    canonical = {}
    roots = tuple(sorted(source_roots.items(), key=lambda item: len(item[0]), reverse=True))
    if not roots or len({target for _, target in roots}) != len(roots):
        raise SystemExit(f"invalid or duplicate canonical source roots: {label}")
    dist_info_roots = {
        PurePosixPath(raw_name).parts[0]
        for raw_name in entries
        if PurePosixPath(raw_name).parts[0].endswith(".dist-info")
    }
    if allow_dist_info and len(dist_info_roots) != 1:
        raise SystemExit(f"wheel must have exactly one dist-info root: {label}")
    dist_info_root = next(iter(dist_info_roots), None)
    for raw_name, data in entries.items():
        parsed = PurePosixPath(raw_name)
        if parsed.is_absolute() or ".." in parsed.parts or "" in raw_name.split("/") or "\\" in raw_name:
            raise SystemExit(f"unsafe {label} member path: {raw_name}")
        if parsed.parts[0].endswith(".dist-info"):
            if allow_dist_info and parsed.parts[0] == dist_info_root:
                continue
            raise SystemExit(f"unexpected dist-info root: {label}: {raw_name}")
        matches = [(source, target) for source, target in roots if raw_name.startswith(source)]
        if len(matches) != 1:
            raise SystemExit(f"unexpected or missing {label} package root: {raw_name}")
        source, target = matches[0]
        suffix = raw_name[len(source):]
        if not suffix:
            raise SystemExit(f"empty {label} package member: {raw_name}")
        canonical_name = target + suffix
        if canonical_name in canonical:
            raise SystemExit(f"duplicate canonical {label} member: {canonical_name}")
        canonical[canonical_name] = data
    return canonical

def installed_wheel_bytes(wheel: Path) -> None:
    record_name, rows, members = wheel_rows(wheel)
    installed_record = site / Path(*PurePosixPath(record_name).parts)
    if not installed_record.is_file() or installed_record.is_symlink():
        raise SystemExit(f"installed wheel RECORD is missing: {installed_record}")
    installed = record_rows(installed_record)
    for name, (expected_hash, expected_size) in rows.items():
        if name == record_name:
            if expected_hash or expected_size:
                raise SystemExit(f"wheel RECORD must leave its own row unhashed: {wheel}")
            continue
        target = rel_target(name, wheel)
        data = target.read_bytes()
        if data != members[name] or installed.get(name) != (expected_hash, expected_size):
            raise SystemExit(f"wheel/install source-byte or RECORD mismatch: {wheel}: {name}")

wheelhouse = root / "wheelhouse"
wheel_paths = [
    (
        Path(os.environ["AGENT_WHEEL"]),
        Path(os.environ["EXPECTED_AGENT_COMMIT"]),
        Path(os.environ["RUNTIME_CHECKOUT"]),
        {
            "astrid/": "astrid/",
            "astrid_runtime_client/": "astrid_runtime_client/",
        },
    ),
    (
        wheelhouse / "astrid_runtime-0.1.0-py3-none-any.whl",
        Path(os.environ["EXPECTED_RUNTIME_COMMIT"]),
        Path(os.environ["RUNTIME_CHECKOUT"]),
        {
            "astrid_runtime/": "astrid_runtime/",
            "runtime_protocol/": "runtime_protocol/",
        },
    ),
    (
        wheelhouse / "astrid_runtime_client-0.2.14-py3-none-any.whl",
        Path(os.environ["EXPECTED_CLIENT_COMMIT"]),
        Path(os.environ["CLIENT_CHECKOUT"]),
        {
            "packages/python/astrid_runtime_client/": "astrid_runtime_client/",
        },
    ),
]
for wheel, commit, checkout, source_root_map in wheel_paths:
    if not wheel.is_file():
        raise SystemExit(f"missing product wheel: {wheel}")
    installed_wheel_bytes(wheel)
    if hashlib.sha256(wheel.read_bytes()).hexdigest() == "":
        raise SystemExit(f"unreadable wheel hash: {wheel}")
    with ZipFile(wheel) as archive:
        wheel_names = [name for name in archive.namelist() if not name.endswith("/")]
        if len(wheel_names) != len(set(wheel_names)):
            raise SystemExit(f"duplicate wheel member: {wheel}")
        wheel_source = {name: archive.read(name) for name in wheel_names}
    wheel_roots = {target: target for target in source_root_map.values()}
    wheel_bytes = canonical_package_bytes(
        wheel_source, wheel_roots, f"wheel {wheel}", allow_dist_info=True
    )
    source_prefixes = tuple(source.rstrip("/") for source in source_root_map)
    command = ["git", "-C", str(checkout), "archive", "--format=tar", commit.as_posix(), "--", *source_prefixes]
    result = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise SystemExit(f"could not archive exact product source for {wheel}: {result.stderr.decode(errors='replace')}")
    source_entries = {}
    with tarfile.open(fileobj=BytesIO(result.stdout), mode="r:") as archive:
        for item in archive.getmembers():
            if not item.isfile():
                continue
            name = item.name.removeprefix("./")
            if name in source_entries:
                raise SystemExit(f"duplicate source member: {name}")
            source_entries[name] = archive.extractfile(item).read()
    source_bytes = canonical_package_bytes(
        source_entries, source_root_map, f"archive {wheel}", allow_dist_info=False
    )
    if wheel_bytes != source_bytes:
        raise SystemExit(f"wheel payload differs from exact source commit: {wheel}")

agent_wheel = Path(os.environ["AGENT_WHEEL"])
with ZipFile(agent_wheel) as archive:
    agent_client = {
        name.removeprefix("astrid_runtime_client/"): archive.read(name)
        for name in archive.namelist()
        if name.startswith("astrid_runtime_client/") and not name.endswith("/")
    }
client_wheel = wheelhouse / "astrid_runtime_client-0.2.14-py3-none-any.whl"
with ZipFile(client_wheel) as archive:
    public_client = {
        name.removeprefix("astrid_runtime_client/"): archive.read(name)
        for name in archive.namelist()
        if name.startswith("astrid_runtime_client/") and not name.endswith("/")
    }
if agent_client != public_client:
    raise SystemExit("b3c Agent wheel does not carry the exact public95 client payload")

schema = __import__("banodoco_timeline_schema")
schema_origin = Path(schema.__file__).resolve()
if site not in schema_origin.parents or any(part.is_symlink() for part in (schema_origin, *schema_origin.parents)):
    raise SystemExit(f"timeline schema escaped private site: {schema_origin}")
from astrid.sdk.host_bootstrap import _installed_execution_origins
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
found = _installed_execution_origins(site, str(Path(os.sys.executable)))
if set(found) != set(origins):
    raise SystemExit(f"installed origin probe returned the wrong keys: {found}")
for label, name in origins.items():
    module = __import__(name, fromlist=["*"])
    origin = Path(module.__file__).resolve()
    if site not in origin.parents or any(part.is_symlink() for part in (origin, *origin.parents)):
        raise SystemExit(f"post-schema origin {label} escaped private site: {origin}")
    if Path(found[label]).resolve() != origin:
        raise SystemExit(f"post-schema origin changed for {label}: {found[label]} != {origin}")

print("PASS profile eight origins=" + repr(found))
print("PASS profile schema and eight origins are private after schema import")
print("PASS profile RECORD=166 closure and installed files are exact")
print("PASS profile 164 constraints=" + os.environ["EXPECTED_CONSTRAINTS_SHA256"] + " exact")
print("PASS profile exact product source/wheel/install bytes")
PY
fi

if [ "${#failures[@]}" -ne 0 ]; then
  printf 'SETUP FAILURES (%s):\n' "${#failures[@]}" >&2
  printf ' - %s\n' "${failures[@]}" >&2
  exit 2
fi

# Keep the original full lane: no integration marker, no cache-provider or
# --basetemp override, and no change to pytest's normal temporary-directory
# behavior.  The central test service supplies PYTHONPATH=$PWD for the source
# snapshot; the final child receives an explicit sanitized replacement below.
export ASTRID_REMOTION_PROJECT_DIR="$COMPOSITION_ROOT"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$PROFILE_SITE"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"
export ASTRID_TEST_NODE_MODULES="$COMPOSITION_ROOT/node_modules"
export ASTRID_VIBECOMFY_CHECKOUT="$VIBECOMFY"
export PYTHONDONTWRITEBYTECODE=1

# The central service deliberately supplies PYTHONPATH=$PWD.  Keep the source
# Agent package for public source tests, but bootstrap the private Runtime,
# client, and schema packages before pytest (and every xdist child) can see
# that checkout path.  The temporary sitecustomize is outside the worktree;
# it also re-raises SIGTERM so pytest's status remains 143.
PREFLIGHT_BOOTSTRAP=$(mktemp -d "${TMPDIR:-/tmp}/astrid-full-preflight.XXXXXX")
cat >"$PREFLIGHT_BOOTSTRAP/sitecustomize.py" <<'PY'
import atexit
import importlib
import os
from pathlib import Path
import shutil
import signal
import sys

site = Path(os.environ["ASTRID_FULL_PRIVATE_SITE"]).resolve()
source = Path(os.environ["ASTRID_FULL_SOURCE_ROOT"]).resolve()
original = list(sys.path)
sys.path[:] = [str(site)] + [entry for entry in original if entry and Path(entry).resolve() != source]
for name in ("banodoco_timeline_schema", "astrid_runtime_client", "astrid_runtime", "runtime_protocol"):
    module = importlib.import_module(name)
    origin = Path(module.__file__).resolve()
    if site not in origin.parents or any(part.is_symlink() for part in (origin, *origin.parents)):
        raise ImportError(f"private {name} import escaped profile: {origin}")
sys.path[:] = original
astrid = importlib.import_module("astrid")
astrid_origin = Path(astrid.__file__).resolve()
if source not in astrid_origin.parents or site in astrid_origin.parents:
    raise ImportError(f"source Agent import escaped checkout: {astrid_origin}")

def _cleanup() -> None:
    shutil.rmtree(os.environ.get("ASTRID_FULL_PREFLIGHT_BOOTSTRAP", ""), ignore_errors=True)

if "-m" in sys.argv and "pytest" in sys.argv:
    atexit.register(_cleanup)
    def _term(signum, _frame):
        _cleanup()
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
    signal.signal(signal.SIGTERM, _term)
PY
export ASTRID_FULL_PRIVATE_SITE="$PROFILE_SITE"
export ASTRID_FULL_SOURCE_ROOT="$SOURCE_ROOT"
export ASTRID_FULL_PREFLIGHT_BOOTSTRAP="$PREFLIGHT_BOOTSTRAP"
export PYTHONPATH="$PREFLIGHT_BOOTSTRAP:$SOURCE_ROOT:$PROFILE_SITE"
export PYTHONNOUSERSITE=1
export PYTHONSAFEPATH=1
exec "$PROFILE_PY" -m pytest -q -n 3 "$@"
