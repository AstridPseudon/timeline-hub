#!/bin/bash
# make-runtime NAME AGENT_SHA [LOCK_SHA256] — host dispatcher only.
# Queued exact-source form (also accepted by the unchanged request-runtime):
# NAME AGENT_SHA LOCK_SHA256 AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA [TEMPLATE_SUITE]
# Supply the entire group, full SHAs and absolute paths without shell metacharacters.
# Positional identities cannot be combined with inherited identity/template inputs.
# Templates: MAIN agent-remotion-0013-nodes (default), or remotion-env-nodes;
# both require the existing approved row/env hashes below. Other hosts must supply
# authentic template facts for review; a retired or fabricated row is refused.
# Build in private staging; never modify an existing runtime or toolchain.
# A qualified existing graph is selected by the committed remotion/ tree only.
# Runtime checkout identity is registration metadata, never a graph key.
set -Eeuo pipefail

O=${RUNTIME_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
A=${RUNTIME_AGENT_CHECKOUT:-/home/user/work/agent}
W=${RUNTIME_WORK_ROOT:-/home/user/work}
NODE_BIN=${RUNTIME_NODE_BIN:-}
NODE_VERSION=20.19.4
NPM_VERSION=10.8.2
# Authoritative hub/kit/bin/provision-agent-machine pins, not discovered over HTTP.
NODE_SHA=7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4
SUMS_SHA=f8537bd20c8fdc951a20a4278e380e03e58e0a1689eaaa5c170b221435f3a22e
N=${1:-}; S=${2:-}; L=${3:-}
R=${RUNTIME_RUNTIME_CHECKOUT:-}
RS=${RUNTIME_RUNTIME_SHA:-}
SUITE=${RUNTIME_TEMPLATE_SUITE:-agent-remotion-0013-nodes}
PROJECT_DIR=${RUNTIME_PROJECT_DIR:-}
case $# in
  2|3) ;; # Legacy callers still require inherited exact-source declarations.
  6|7)
    for key in RUNTIME_AGENT_CHECKOUT RUNTIME_RUNTIME_CHECKOUT RUNTIME_RUNTIME_SHA RUNTIME_TEMPLATE_SUITE; do
      if [[ -v "$key" ]]; then
        echo "REFUSED: ambiguous positional and inherited source: $key" >&2; exit 2
      fi
    done
    [[ "$L" =~ ^[0-9a-f]{64}$ ]] || { echo 'REFUSED: positional sources require lock SHA-256' >&2; exit 2; }
    A=$4; R=$5; RS=$6; SUITE=${7-agent-remotion-0013-nodes}
    for path in "$A" "$R"; do
      [[ "$path" = /* && "$path" != *[!a-zA-Z0-9_./-]* && "/$path/" != */../* && "/$path/" != */./* ]] || {
        echo 'REFUSED: source checkout must be a safe absolute path' >&2; exit 2;
      }
    done
    [[ "$RS" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: exact 40-character Runtime commit required' >&2; exit 2; }
    [[ "$SUITE" = agent-remotion-0013-nodes || "$SUITE" = remotion-env-nodes ]] || {
      echo 'REFUSED: unapproved registration template' >&2; exit 2;
    }
    ;;
  *) echo 'REFUSED: expected NAME AGENT_SHA [LOCK_SHA256] or NAME AGENT_SHA LOCK_SHA256 AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA [TEMPLATE_SUITE]' >&2; exit 2 ;;
esac
[[ -n "$A" ]] || { echo 'REFUSED: Agent checkout is required' >&2; exit 2; }
[[ "$N" =~ ^agent-remotion-[0-9a-z][0-9a-z-]*$ ]] || { echo 'REFUSED: invalid immutable runtime name' >&2; exit 2; }
[[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: exact 40-character Agent commit required' >&2; exit 2; }
[[ -z "$L" || "$L" =~ ^[0-9a-f]{64}$ ]] || { echo 'REFUSED: invalid lock SHA-256' >&2; exit 2; }
for root in "$O" "$W" "$A"; do
  [[ "$root" = /* && "$root" != *[!a-zA-Z0-9_./-]* && "/$root/" != */../* && "/$root/" != */./* ]] || {
    echo 'REFUSED: root must be a safe absolute path' >&2; exit 2;
  }
done
D=$W/runtimes/$N
if [ -e "$D" ] || [ -L "$D" ]; then
  echo "REFUSED: exists: $D (immutable; pick a fresh name)" >&2
  exit 2
fi

missing=()
for cmd in git tar xz sha256sum cut grep find mkdir chmod df awk sed date timeout curl python3 uname mktemp env bash cat; do
  command -v "$cmd" >/dev/null 2>&1 || missing+=("command:$cmd")
done
for dir in "$W" "$W/runtimes" "$A" "$O/tests"; do
  [ -d "$dir" ] || missing+=("directory:$dir")
done
for dir in "$W/runtimes" "$O/tests"; do
  [ -w "$dir" ] || missing+=("writable:$dir")
done
[ -r "$O/tests/suites.conf" ] && [ -w "$O/tests/suites.conf" ] || missing+=("read-write:$O/tests/suites.conf")
# MAIN registration adapter: select one declared, hash-locked current pair.
# Runtime source identity cannot be inferred from a Remotion package lock.
registration() {
  python3 - "$1" "$O" "$W" "$A" "$S" "$N" "${T:-}" "$NODE_BIN" \
    "$SUITE" \
    "$R" "$RS" <<'REGISTRATION'
import hashlib, os, pathlib, re, shlex, subprocess, sys
mode, orch, work, agent, sha, name, staging, node, suite, runtime, runtime_sha = sys.argv[1:]
tests = pathlib.Path(orch) / "tests"
# These are MAIN's existing rows and matching env bytes, never a retired alias.
approved = {
    "agent-remotion-0013-nodes": ("agent-remotion-0013.env", "9f7d51ce0a35ffb7d459b0fa20bb998344f39f944241198635f6d66605e8ae33", "e03e177251a99e37820c001f6fe6f88f2f503d1f939a5f67eed6ed59eeca2d07"),
    "remotion-env-nodes": ("agent-remotion.env", "ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036", "e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02"),
}
errors = []
env_text = row = ""
try:
    filename, row_hash, env_hash = approved[suite]
    rows = [line for line in (tests / "suites.conf").read_text().splitlines()
            if line.split()[:2] == ["agent", suite]]
    if len(rows) != 1:
        raise ValueError(f"suite row count={len(rows)} (requires exactly one)")
    row = rows[0]
    env_text = (tests / filename).read_text()
    if hashlib.sha256(row.encode()).hexdigest() != row_hash:
        raise ValueError("suite identity changed")
    if hashlib.sha256(env_text.encode()).hexdigest() != env_hash:
        raise ValueError("env identity changed")
    print(f"registration_template={suite} identity=validated", file=sys.stderr)
except (KeyError, OSError, ValueError) as error:
    errors.append(f"template:{suite}:{error}")

def exact_checkout(label, path, expected):
    if not pathlib.Path(path).is_absolute() or not re.fullmatch(r"[0-9a-f]{40}", expected):
        errors.append(f"{label}-identity:declare exact checkout and 40-character SHA")
        return
    try:
        actual = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True, timeout=10).strip()
        dirty = subprocess.check_output(["git", "-C", path, "status", "--porcelain"], text=True, timeout=10).strip()
        if actual != expected or dirty:
            raise ValueError(f"expected={expected},actual={actual},dirty={bool(dirty)}")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        errors.append(f"{label}-identity:{error}")

exact_checkout("agent", agent, sha)
exact_checkout("runtime", runtime, runtime_sha)
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(2)
if mode == "validate":
    sys.exit(0)
# Revalidate at registration time; never execute a template as shell input.
values = dict(line.split("=", 1) for line in env_text.splitlines())
project_dir = os.environ.get("RUNTIME_PROJECT_DIR") or str(pathlib.Path(work) / "runtimes" / name)
values.update(ASTRID_REMOTION_PROJECT_DIR=project_dir,
              ASTRID_NODE_EXECUTABLE=node + "/node", ASTRID_CHECKOUT=agent,
              ASTRID_RUNTIME_CHECKOUT=runtime, ASTRID_AGENT_SOURCE_COMMIT=sha,
              ASTRID_RUNTIME_SOURCE_COMMIT=runtime_sha,
              ASTRID_BUILD_ORIGIN_AGENT_COMMIT=os.environ.get("RUNTIME_BUILD_ORIGIN_AGENT_COMMIT", ""),
              ASTRID_RUNTIME_TEMPLATE=suite, ASTRID_RUNTIME_PROFILE=suite)
# Acquired tools move with the immutable runtime; rewrite only the staging prefix.
def relocated(value):
    return value.replace(staging + "/", str(pathlib.Path(work) / "runtimes" / name) + "/")
values["PATH"] = node + ":" + values["PATH"]
values = {key: relocated(value) for key, value in values.items()}
args = shlex.split(row)
command_index = next(i for i, arg in enumerate(args[4:], 4) if "=" not in arg)
assignments = dict(arg.split("=", 1) for arg in args[4:command_index])
assignments.update(values)
# Keep the approved runner and pytest arguments, including snapshot-relative PWD.
command = ["agent", name + "-nodes", *args[2:4],
           *(key + "=" + value for key, value in assignments.items()), *args[command_index:]]
pathlib.Path(staging, ".runtime-env").write_text("".join(key + "=" + shlex.quote(value) + "\n" for key, value in values.items()))
guards = " && ".join("test \"$(git -C " + shlex.quote(path) + " rev-parse HEAD)\" = " + expected
                     for path, expected in [(agent, sha), (runtime, runtime_sha)])
guards += " && " + " && ".join("test -z \"$(git -C " + shlex.quote(path) + " status --porcelain)\"" for path in [agent, runtime])
pathlib.Path(staging, ".runtime-suite").write_text("agent " + name + "-nodes " + guards + " && " + shlex.join(command[2:]) + "\n")
REGISTRATION
}
registration validate || missing+=("registration:template-or-exact-source-identity")
[[ "$(uname -s 2>/dev/null || true)/$(uname -m 2>/dev/null || true)" = Linux/x86_64 ]] || missing+=("platform:requires-Linux/x86_64")
python3 -c 'import ctypes; ctypes.CDLL(None, use_errno=True).renameat2' 2>/dev/null || missing+=("atomic-publish:libc.renameat2")
git -C "$A" rev-parse --is-inside-work-tree >/dev/null 2>&1 || missing+=("agent-checkout:$A")
git -C "$A" cat-file -e "$S^{commit}" 2>/dev/null || missing+=("agent-commit:$S")
for file in package.json package-lock.json; do
  git -C "$A" cat-file -e "$S:remotion/$file" 2>/dev/null || missing+=("agent-file:remotion/$file")
done
LOCK_SHA=$(git -C "$A" show "$S:remotion/package-lock.json" 2>/dev/null | sha256sum | cut -d' ' -f1) || LOCK_SHA=
PACKAGE_SHA=$(git -C "$A" show "$S:remotion/package.json" 2>/dev/null | sha256sum | cut -d' ' -f1) || PACKAGE_SHA=
REMOTION_TREE=$(git -C "$A" rev-parse "$S:remotion" 2>/dev/null) || REMOTION_TREE=
read -r COMPONENT_SHA REMOTION_VERSION COMPOSITION_VERSION < <(python3 - "$A" "$S" <<'PY'
import hashlib, json, subprocess, sys
agent, commit = sys.argv[1:]
show = lambda path: subprocess.check_output(["git", "-C", agent, "show", f"{commit}:remotion/{path}"])
lock = json.loads(show("package-lock.json"))
package = json.loads(show("package.json"))
packages = lock.get("packages", {})
names = ("remotion", "@banodoco/timeline-composition")
identity = {"package": package, "lock": {name: packages.get("node_modules/" + name) for name in names}}
print(hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest(), end=" ")
print(packages["node_modules/remotion"]["version"], end=" ")
print(packages["node_modules/@banodoco/timeline-composition"]["version"])
PY
) || { echo 'REFUSED: cannot determine authentic Remotion component identity' >&2; exit 2; }
[ "$REMOTION_TREE" ] || { echo 'REFUSED: missing committed remotion tree' >&2; exit 2; }
[ -z "$L" ] || [ "$LOCK_SHA" = "$L" ] || {
  echo "REFUSED: lock-sha256:expected=$L,actual=$LOCK_SHA" >&2; exit 2;
}
git -C "$A" show "$S:remotion/package.json" 2>/dev/null | python3 -c '
import json,sys
p=json.load(sys.stdin)
assert p["engines"] == {"node":"=20.19.4", "npm":"=10.8.2"}, p.get("engines")
' 2>/dev/null || { echo 'REFUSED: Agent Remotion requires exact Node20.19.4/npm10.8.2' >&2; exit 2; }

# The manifest excludes only generated identity/registration files. It covers
# source and installed bytes, so marker-only or partial graphs cannot qualify.
artifact_integrity() {
  python3 - "$1" <<'PY'
import hashlib, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
excluded = {".astrid-agent-source-commit", ".astrid-remotion-tree",
    ".astrid-package-lock-sha256", ".astrid-package-sha256",
    ".astrid-component-identity", ".astrid-node-version", ".astrid-npm-version",
    ".astrid-node-modules-lock-sha256", ".astrid-artifact-integrity",
    ".runtime-env", ".runtime-suite", ".provision-failure"}
out = hashlib.sha256()
for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
    if path.name in excluded: continue
    rel = path.relative_to(root).as_posix()
    if path.is_symlink(): value = b"L:" + path.readlink().as_posix().encode()
    elif path.is_file(): value = b"F:" + hashlib.sha256(path.read_bytes()).hexdigest().encode()
    else: continue
    out.update(rel.encode() + b"\0" + value + b"\n")
print(out.hexdigest())
PY
}

# 0 = exact qualified graph, 1 = no same-tree graph, 2 = matching-tree graph
# is incomplete/tampered/ambiguous and must not be silently rebuilt.
candidate_matches() {
  python3 - "$1" "$REMOTION_TREE" "$LOCK_SHA" "$PACKAGE_SHA" "$COMPONENT_SHA" "$NODE_VERSION" "$NPM_VERSION" "$A" <<'PY'
import hashlib, json, pathlib, re, sys
import subprocess
root = pathlib.Path(sys.argv[1])
tree, lock_sha, package_sha, component_sha, node_version, npm_version, agent = sys.argv[2:]
marker = root / ".astrid-remotion-tree"
if not marker.is_file(): raise SystemExit(1)
marker_tree = marker.read_text().strip()
if marker_tree != tree:
    # A graph for another source tree is normal build input. If its retained
    # origin authenticates to this requested tree, however, the marker itself
    # was tampered and must refuse closed.
    origin_path = root / ".astrid-agent-source-commit"
    if origin_path.is_file() and re.fullmatch(r"[0-9a-f]{40}", origin_path.read_text().strip()):
        origin = origin_path.read_text().strip()
        try:
            source_tree = subprocess.check_output(
                ["git", "-C", agent, "rev-parse", origin + ":remotion"], text=True).strip()
            if source_tree == tree:
                print("invalid same-tree graph: Remotion tree marker", file=sys.stderr)
                raise SystemExit(2)
        except (OSError, subprocess.CalledProcessError, ValueError) as error:
            if isinstance(error, ValueError):
                print("invalid same-tree graph: " + str(error), file=sys.stderr)
                raise SystemExit(2)
    raise SystemExit(1)
excluded = {".astrid-agent-source-commit", ".astrid-remotion-tree",
    ".astrid-package-lock-sha256", ".astrid-package-sha256",
    ".astrid-component-identity", ".astrid-node-version", ".astrid-npm-version",
    ".astrid-node-modules-lock-sha256", ".astrid-artifact-integrity",
    ".runtime-env", ".runtime-suite", ".provision-failure"}
def text(name):
    path = root / name
    if not path.is_file(): raise ValueError("missing " + name)
    return path.read_text().strip()
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def artifact():
    out = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        if path.name in excluded: continue
        rel = path.relative_to(root).as_posix()
        if path.is_symlink(): value = b"L:" + path.readlink().as_posix().encode()
        elif path.is_file(): value = b"F:" + digest(path).encode()
        else: continue
        out.update(rel.encode() + b"\0" + value + b"\n")
    return out.hexdigest()
try:
    if not root.is_dir() or root.is_symlink(): raise ValueError("not a physical directory")
    origin = text(".astrid-agent-source-commit")
    if not re.fullmatch(r"[0-9a-f]{40}", origin): raise ValueError("invalid truthful build-origin Agent SHA")
    try:
        subprocess.run(["git", "-C", agent, "cat-file", "-e", origin + "^{commit}"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        source_tree = subprocess.check_output(
            ["git", "-C", agent, "rev-parse", origin + ":remotion"], text=True).strip()
        if source_tree != tree: raise ValueError("build-origin Remotion tree")
        for filename, expected in (("package-lock.json", lock_sha), ("package.json", package_sha)):
            actual = subprocess.check_output(
                ["git", "-C", agent, "show", origin + ":remotion/" + filename])
            if hashlib.sha256(actual).hexdigest() != expected:
                raise ValueError("build-origin source bytes")
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        raise ValueError("unauthenticated build-origin source: " + str(error)) from error
    if text(".astrid-package-lock-sha256") != lock_sha: raise ValueError("lock identity")
    if text(".astrid-package-sha256") != package_sha: raise ValueError("package identity")
    if text(".astrid-component-identity") != component_sha: raise ValueError("component identity")
    if text(".astrid-node-version") != "v" + node_version: raise ValueError("Node engine")
    if text(".astrid-npm-version") != npm_version: raise ValueError("npm engine")
    if digest(root / "package-lock.json") != lock_sha or digest(root / "package.json") != package_sha:
        raise ValueError("source bytes")
    lock = json.loads((root / "package-lock.json").read_text())
    for name in ("remotion", "@banodoco/timeline-composition"):
        package = root / "node_modules" / name / "package.json"
        expected = lock["packages"]["node_modules/" + name]["version"]
        if not package.is_file() or json.loads(package.read_text())["version"] != expected:
            raise ValueError("installed component")
    installed_lock = root / "node_modules/.package-lock.json"
    if text(".astrid-node-modules-lock-sha256") != digest(installed_lock):
        raise ValueError("installed lock integrity")
    installed = json.loads(installed_lock.read_text()).get("packages", {})
    for name in ("remotion", "@banodoco/timeline-composition"):
        source_entry = lock["packages"]["node_modules/" + name]
        installed_entry = installed.get("node_modules/" + name)
        if not installed_entry or any(installed_entry.get(key) != source_entry.get(key)
                                      for key in ("version", "resolved", "integrity")
                                      if key in source_entry):
            raise ValueError("installed component provenance")
    if text(".astrid-artifact-integrity") != artifact(): raise ValueError("artifact integrity")
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_mode & 0o222: raise ValueError("writable artifact")
except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
    print("invalid same-tree graph: " + str(error), file=sys.stderr)
    raise SystemExit(2)
raise SystemExit(0)
PY
}

verify_node() {
  [ -x "$1/node" ] && [ -x "$1/npm" ] &&
    [ "$(timeout -k 2s 10s "$1/node" --version 2>/dev/null)" = "v$NODE_VERSION" ] &&
    [ "$(PATH="$1:$PATH" timeout -k 2s 10s "$1/npm" --version 2>/dev/null)" = "$NPM_VERSION" ]
}
if [ -n "$NODE_BIN" ]; then
  verify_node "$NODE_BIN" || missing+=("selected-toolchain:requires-Node$NODE_VERSION/npm$NPM_VERSION:$NODE_BIN")
else
  for candidate in "$W/toolchain/node-v$NODE_VERSION-linux-x64/bin" "/opt/node-v$NODE_VERSION-linux-x64/bin" "/opt/node$NODE_VERSION/bin"; do
    if verify_node "$candidate"; then NODE_BIN=$candidate; break; fi
  done
fi
[ -n "$NODE_BIN" ] || missing+=("selected-toolchain:requires-Node$NODE_VERSION/npm$NPM_VERSION")
if [ "${#missing[@]}" -ne 0 ]; then
  printf 'PREFLIGHT FAILED name=%s agent=%s\n' "$N" "$S" >&2
  printf 'missing_prerequisite=%s\n' "${missing[@]}" >&2
  exit 2
fi

# Store authority is mandatory on the normal dispatcher route, including env -i.
STORE_HELPER=$O/bin/bench_store.py
[ -f "$STORE_HELPER" ] && [ ! -L "$STORE_HELPER" ] || { echo 'REFUSED: bench store helper unavailable' >&2; exit 2; }
STORE_ROOT=$W/bench-store
export STORE_CONTEXT="$(declare -p O W A S N R RS SUITE NODE_BIN NODE_VERSION NPM_VERSION NODE_SHA SUMS_SHA LOCK_SHA PACKAGE_SHA REMOTION_TREE COMPONENT_SHA; declare -f registration candidate_matches artifact_integrity)"
python3 -I - "$0" "$STORE_HELPER" "$STORE_ROOT" "$O/tests" "$N" "$S" "$RS" "$REMOTION_TREE" <<'STORE_PY'
import importlib.util, os, pathlib, shlex, subprocess, sys, tempfile
script, helper, root, tests, name, agent, backend, tree = sys.argv[1:]
spec = importlib.util.spec_from_file_location('bench_store', helper)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
store = module.Store(root, tests)
source = pathlib.Path(script).read_text()
body = source.split('# STORE_BUILD_BEGIN\n', 1)[1].split('# STORE_BUILD_END', 1)[0]
context = os.environ['STORE_CONTEXT']
def shell(code, *args, **kw):
    return subprocess.run(['bash', '-Eeuo', 'pipefail', '-c', context + '\n' + code, 'store-adapter', *map(str, args)], check=True, **kw)
def build(stage, final):
    if os.environ.get('RUNTIME_BUILD_MOCK') == '1':
        raise RuntimeError('build required; installer not run (fixture control)')
    shell('T=$1; D=$2\n' + body, stage, final)
def verify(path):
    shell('candidate_matches "$1"', path)
def registration(path, final, reused):
    origin = (pathlib.Path(path) / '.astrid-agent-source-commit').read_text().strip()
    with tempfile.TemporaryDirectory(prefix='runtime-registration-', dir=os.environ.get('TMPDIR')) as temp:
        shell('T=$1; RUNTIME_PROJECT_DIR=$2 RUNTIME_BUILD_ORIGIN_AGENT_COMMIT=$3 registration render', temp, final, origin)
        return {'name': name, 'env': pathlib.Path(temp, '.runtime-env').read_text(),
                'suite': pathlib.Path(temp, '.runtime-suite').read_text(), 'requires': []}
try:
    entry = store.ensure('runtime', {'remotion_tree': tree}, registration, build, verify)
except Exception as error:
    print('REFUSED: bench store: ' + str(error), file=sys.stderr)
    sys.exit(2)
path = pathlib.Path(entry['path'])
origin = (path / '.astrid-agent-source-commit').read_text().strip()
print('status=' + ('reused' if entry['reused'] else 'created'))
print('runtime=' + str(path))
print('requested_name=' + name + '\nrequested_agent_sha=' + agent + '\nrequested_runtime_sha=' + backend)
print('build_origin_agent_sha=' + origin + '\nremotion_tree_sha=' + tree + '\nkey=' + entry['key'] + '\nreuse=verified')
STORE_PY
exit $?
: <<'STORE_BUILD_BODY'
# STORE_BUILD_BEGIN
stage=staging
fail() {
  local rc=$?
  trap - ERR TERM INT
  printf 'status=failed\nstage=%s\nagent_sha=%s\nlock_sha256=%s\npartial=%s\n' "$stage" "$S" "$LOCK_SHA" "$T" > "$T/.provision-failure" 2>/dev/null || true
  echo "FAILED stage=$stage; partial retained: $T" >&2
  [ "$rc" -ne 0 ] || rc=1
  exit "$rc"
}
trap fail ERR TERM INT
download() {
  timeout -k 5s 150s curl --fail --silent --show-error --location \
    --proto '=https' --proto-redir '=https' --connect-timeout 10 --max-time 60 \
    --retry 1 --retry-delay 2 --retry-max-time 125 --output "$2" "$1"
}
if [ -z "$NODE_BIN" ]; then
  stage=node-download
  mkdir "$T/.toolchain"
  ARCHIVE=node-v$NODE_VERSION-linux-x64.tar.xz
  BASE=https://nodejs.org/dist/v$NODE_VERSION
  download "$BASE/SHASUMS256.txt" "$T/.toolchain/SHASUMS256.txt"
  [ "$(sha256sum "$T/.toolchain/SHASUMS256.txt" | cut -d' ' -f1)" = "$SUMS_SHA" ]
  grep -Fx "$NODE_SHA  $ARCHIVE" "$T/.toolchain/SHASUMS256.txt" >/dev/null
  download "$BASE/$ARCHIVE" "$T/.toolchain/$ARCHIVE"
  stage=node-checksum
  [ "$(sha256sum "$T/.toolchain/$ARCHIVE" | cut -d' ' -f1)" = "$NODE_SHA" ]
  stage=node-extract
  tar -xJf "$T/.toolchain/$ARCHIVE" -C "$T/.toolchain" --no-same-owner
  NODE_BIN=$T/.toolchain/node-v$NODE_VERSION-linux-x64/bin
  [ "$(timeout -k 2s 10s "$NODE_BIN/node" --version)" = "v$NODE_VERSION" ]
  # If an official distribution's bundled npm differs, use its supported CLI
  # to install the exact release into this build's private prefix, never global.
  if [ "$(PATH="$NODE_BIN:$PATH" timeout -k 2s 10s "$NODE_BIN/npm" --version)" != "$NPM_VERSION" ]; then
    stage=npm-acquire
    PATH="$NODE_BIN:$PATH" npm_config_cache="$T/.npm-cache" npm_config_engine_strict=true \
      timeout -k 10s 120s "$NODE_BIN/npm" install --prefix "$T/.npm-exact" \
      --registry=https://registry.npmjs.org --no-audit --no-fund --ignore-scripts \
      --fetch-retries=1 --fetch-timeout=30000 "npm@$NPM_VERSION"
    NPM_CLI=$T/.npm-exact/node_modules/npm/bin/npm-cli.js
    NPM_BIN=$T/.npm-exact/node_modules/.bin
  fi
fi
NPM_CLI=${NPM_CLI:-$NODE_BIN/../lib/node_modules/npm/bin/npm-cli.js}
stage=exact-toolchain
[ "$(timeout -k 2s 10s "$NODE_BIN/node" --version)" = "v$NODE_VERSION" ]
[ "$(PATH="$NODE_BIN:$PATH" timeout -k 2s 10s "$NODE_BIN/node" "$NPM_CLI" --version)" = "$NPM_VERSION" ]
stage=archive
git -C "$A" archive "$S" remotion | tar -x -C "$T" --strip-components=1
check_sources() {
  [ "$(sha256sum "$T/package-lock.json" | cut -d' ' -f1)" = "$LOCK_SHA" ] &&
    [ "$(sha256sum "$T/package.json" | cut -d' ' -f1)" = "$PACKAGE_SHA" ]
}
check_sources
stage=npm-ci
( cd "$T" && PATH="${NPM_BIN:-$NODE_BIN}:$NODE_BIN:$PATH" npm_config_cache="$T/.npm-cache" npm_config_engine_strict=true \
  timeout -k 10s 600s "$NODE_BIN/node" "$NPM_CLI" ci --no-audit --no-fund --loglevel=error \
  --fetch-retries=1 --fetch-timeout=30000 )
stage=verify-installed
check_sources
( cd "$T" && "$NODE_BIN/node" -e '
const fs = require("fs");
const lock = JSON.parse(fs.readFileSync("package-lock.json"));
for (const name of ["remotion", "@banodoco/timeline-composition"]) {
  const key = "node_modules/" + name;
  const actual = JSON.parse(fs.readFileSync(key + "/package.json")).version;
  if (!lock.packages[key] || actual !== lock.packages[key].version) throw Error(name + " differs from lock");
  console.log(name + "=" + actual);
}
' ) > "$T/.astrid-installed-module-origins"
printf '%s\n' "$S" > "$T/.astrid-agent-source-commit"
printf '%s\n' "$LOCK_SHA" > "$T/.astrid-package-lock-sha256"
printf '%s\n' "$PACKAGE_SHA" > "$T/.astrid-package-sha256"
printf '%s\n' "$REMOTION_TREE" > "$T/.astrid-remotion-tree"
printf '%s\n' "$COMPONENT_SHA" > "$T/.astrid-component-identity"
printf 'v%s\n' "$NODE_VERSION" > "$T/.astrid-node-version"
printf '%s\n' "$NPM_VERSION" > "$T/.astrid-npm-version"
printf '%s\n' "$(sha256sum "$T/node_modules/.package-lock.json" | cut -d' ' -f1)" > "$T/.astrid-node-modules-lock-sha256"
printf '%s\n' "$(artifact_integrity "$T")" > "$T/.astrid-artifact-integrity"
stage=read-only
find "$T" -type f -exec chmod a-w {} +
# STORE_BUILD_END
STORE_BUILD_BODY
