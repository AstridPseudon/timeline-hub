#!/usr/bin/env bash
set -euo pipefail

# D13 input-only qualification. Builds one exact-source wheel in private TMPDIR,
# verifies immutable c886 inputs, then runs the original preflight once.
ROOT=$(git rev-parse --show-toplevel)
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/agt-F-D13-wheel-input-0039
EVIDENCE=$WORKER/evidence
TMPROOT=$TMPDIR/d13-wheel-input-0039-$(date +%s)-$$
BENCH=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
SITE=$BENCH/lib/python3.13/site-packages
PY=$BENCH/bin/python
BUILD_PY=/home/user/work/venv-agent/bin/python
REMOTION=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
BROWSER=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
FFMPEG=/usr/bin/ffmpeg
FFPROBE=/usr/bin/ffprobe
COMMIT=c36ca8c94b695b0e25b7d42c89f194661f187423
TREE=50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92

test "$(git -C "$ROOT" rev-parse HEAD)" = "$COMMIT"
test "$(git -C "$ROOT" rev-parse HEAD^{tree})" = "$TREE"
test -z "$(git -C "$ROOT" diff --name-only)"
test -x "$PY" && test -d "$SITE" && test ! -L "$SITE"
test -d "$REMOTION/node_modules" && test ! -L "$REMOTION/node_modules"
test -x "$NODE" && test -x "$BROWSER" && test -x "$FFMPEG" && test -x "$FFPROBE"
test ! -e "$TMPROOT"
mkdir -p "$TMPROOT/source" "$TMPROOT/wheelhouse" "$EVIDENCE"
git -C "$ROOT" archive --format=tar "$COMMIT" | tar -x -C "$TMPROOT/source"
"$BUILD_PY" -m build --wheel --no-isolation --outdir "$TMPROOT/wheelhouse" "$TMPROOT/source" >"$TMPROOT/build.log" 2>&1
WHEEL=$(find "$TMPROOT/wheelhouse" -maxdepth 1 -type f -name 'astrid-0.1.0-*.whl' -print -quit)
test -f "$WHEEL" && test ! -L "$WHEEL"

"$BUILD_PY" - "$ROOT" "$BENCH" "$SITE" "$PY" "$REMOTION" "$NODE" "$BROWSER" "$FFMPEG" "$FFPROBE" "$WHEEL" "$TMPROOT/source" "$EVIDENCE" <<'PY'
from __future__ import annotations
import ast, hashlib, json, os, subprocess, sys, zipfile
from pathlib import Path

root, bench, site, py, remotion, node, browser, ffmpeg, ffprobe, wheel, source, evidence = map(Path, sys.argv[1:])
expected_commit = "c36ca8c94b695b0e25b7d42c89f194661f187423"
expected_tree = "50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92"
failures = []

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def probe(code, *args):
    env = {"HOME": "/root", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": str(py.parent)+":/usr/bin:/bin"}
    p = subprocess.run([str(py), "-I", "-B", "-c", code, *args], env=env,
                       cwd=root, text=True, capture_output=True, check=False)
    if p.returncode:
        failures.append("installed python -I probe failed: " + p.stderr.strip())
        return {}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        failures.append("installed python -I probe returned non-JSON")
        return {}

def git(*args):
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if p.returncode:
        failures.append("git command failed: " + " ".join(args))
    return p.stdout

owner = (bench / ".bench-owner.json").read_text()
provision = (bench / ".provision-report").read_text()
distribution = (bench / ".astrid-distribution-metadata").read_text()
if f'"agent_sha":"{expected_commit}"' not in owner:
    failures.append("c886 owner metadata is not Agent c36")
if f"agent_sha={expected_commit}" not in provision:
    failures.append("c886 provision report is not Agent c36")
if "runtime_sha=abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e" not in provision:
    failures.append("c886 provision report is not Runtime abd47")
if "astrid_provenance=directory" not in distribution:
    failures.append("c886 Astrid direct-directory provenance missing")
if not (bench / ".astrid-source-commit").read_text().strip() == expected_commit:
    failures.append("c886 source commit marker mismatch")

profile = evidence / "d13-profile-c886.json"
bindings = evidence / "d13-bindings-c36-c886.json"
profile.write_text(json.dumps({"profile":"astrid","runtime_checkout":str(site),
    "source_checkout":str(site),"runtime_environment":str(bench)}, indent=2)+"\n")
profile_sha = sha(profile)

with zipfile.ZipFile(wheel) as z:
    names = [n for n in z.namelist() if not n.endswith("/")]
    records = [n for n in names if n.endswith(".dist-info/RECORD")]
    if len(records) != 1:
        failures.append("wheel does not contain exactly one RECORD")
    wheel_record = records[0] if records else ""
    metadata = [n for n in names if n.endswith(".dist-info/METADATA")]
    if len(metadata) != 1:
        failures.append("wheel does not contain exactly one METADATA")
    package_names = [n for n in names if n.startswith(("astrid/", "astrid_runtime_client/"))]
    for name in package_names:
        target = source / name
        if not target.is_file() or z.read(name) != target.read_bytes():
            failures.append("wheel differs from exact c36 archive: " + name)
    wheel_size = wheel.stat().st_size
    wheel_sha = sha(wheel)

orig = (root / "tests/packs/video_editing/test_runtime_publication_chain.py").read_bytes()
committed = git("show", f"{expected_commit}:tests/packs/video_editing/test_runtime_publication_chain.py")
if orig != committed:
    failures.append("original D13 test file differs from c36")
try:
    node_ast = next(n for n in ast.parse(orig.decode()).body
                    if isinstance(n, ast.FunctionDef) and n.name == "test_d13_installed_native_preflight")
    body_hash = hashlib.sha256(ast.get_source_segment(orig.decode(), node_ast).encode()).hexdigest()
except (StopIteration, SyntaxError, TypeError) as exc:
    failures.append("D13 test body hash failed: " + str(exc))
    body_hash = ""

origins = probe(
    "import json,sys,astrid,astrid_runtime,runtime_protocol,astrid_runtime_client;"
    "from pathlib import Path;"
    "print(json.dumps({'python':sys.executable,'origins':{"
    "'astrid':str(Path(astrid.__file__).resolve()),"
    "'astrid_runtime':str(Path(astrid_runtime.__file__).resolve()),"
    "'runtime_protocol':str(Path(runtime_protocol.__file__).resolve()),"
    "'astrid_runtime_client':str(Path(astrid_runtime_client.__file__).resolve())}}))")
for name, value in origins.get("origins", {}).items():
    if not Path(value).resolve().is_relative_to(site.resolve()):
        failures.append("installed origin escaped c886: " + name)
if origins.get("python") != str(py):
    failures.append("installed python executable mismatch")
source_digest = probe(
    "import json,sys; from astrid.core.execution.generic_host import source_checkout_digest;"
    "print(json.dumps({'digest':source_checkout_digest(sys.argv[1])}))", str(site)).get("digest", "")
if len(source_digest) != 64:
    failures.append("c886 source_checkout_digest is not SHA-256")

direct_url = site / "astrid-0.1.0.dist-info" / "direct_url.json"
if not direct_url.is_file() or direct_url.is_symlink():
    failures.append("c886 direct_url.json missing or symlinked")
elif "child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e" not in direct_url.read_text():
    failures.append("c886 direct_url.json does not identify managed source")

resources = {
    "node": sha(node), "remotion_lock": sha(remotion / "package-lock.json"),
    "browser": sha(browser), "ffmpeg": sha(ffmpeg), "ffprobe": sha(ffprobe)}
expected_resources = {
    "node": "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490",
    "remotion_lock": "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d",
    "browser": "85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95",
    "ffmpeg": "ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41",
    "ffprobe": "272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f"}
for name, expected in expected_resources.items():
    if resources[name] != expected:
        failures.append(f"819acf resource changed: {name}")

build_version = subprocess.run([sys.executable, "-m", "build", "--version"],
    text=True, capture_output=True, check=False).stdout.strip()
setuptools_version = subprocess.run([sys.executable, "-c", "import setuptools;print(setuptools.__version__)"],
    text=True, capture_output=True, check=False).stdout.strip()
wheel_version = subprocess.run([sys.executable, "-c", "import wheel;print(wheel.__version__)"],
    text=True, capture_output=True, check=False).stdout.strip()
if not build_version.startswith("build 1.4.0") or setuptools_version != "80.9.0" or wheel_version != "0.46.3":
    failures.append(f"builder mismatch: {build_version}, {setuptools_version}, {wheel_version}")

bindings_data = {"agent_commit":expected_commit, "agent_tree":expected_tree,
    "agent_wheel":str(wheel), "agent_wheel_sha256":wheel_sha,
    "source_checkout":str(site), "source_digest":source_digest,
    "runtime_environment":str(bench)}
bindings.write_text(json.dumps(bindings_data, indent=2)+"\n")
manifest = {"source_commit":expected_commit, "source_tree":expected_tree,
    "source_checkout_digest":source_digest, "source_archive":str(source),
    "wheel":str(wheel), "wheel_sha256":wheel_sha, "wheel_bytes":wheel_size,
    "wheel_record":wheel_record, "installed_record":str(site/"astrid-0.1.0.dist-info/RECORD"),
    "installed_direct_url":str(direct_url), "installed_origins":origins,
    "profile":str(profile), "profile_sha256":profile_sha, "bindings":str(bindings),
    "resources":resources, "builder":{"build":build_version,"setuptools":setuptools_version,"wheel":wheel_version},
    "test_file_sha256":hashlib.sha256(orig).hexdigest(), "test_body_sha256":body_hash,
    "python_no_user_site_override":False}
(evidence / "d13-wheel-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
if failures:
    print("D13 report-all preflight: FAIL")
    for failure in failures:
        print("- " + failure)
    raise SystemExit(1)
print("D13 report-all preflight: PASS")
print(json.dumps(manifest, sort_keys=True))
PY

RUNROOT=$TMPROOT/test-run
mkdir -p "$RUNROOT/home" "$RUNROOT/tmp" "$RUNROOT/pytest"
env -i HOME="$RUNROOT/home" LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH="$(dirname "$NODE"):$BENCH/bin:/usr/bin:/bin" PYTHONDONTWRITEBYTECODE=1 TMPDIR="$RUNROOT/tmp" \
    ASTRID_HOST_EXECUTION_PROFILE=installed ASTRID_PACK_HOST_PYTHON="$PY" \
    ASTRID_PACKS_PATH="$SITE/astrid/packs/rendering" ASTRID_REMOTION_PROJECT_DIR="$REMOTION" \
    ASTRID_REMOTION_BROWSER_EXECUTABLE="$BROWSER" ASTRID_NODE_EXECUTABLE="$NODE" \
    ASTRID_TEST_NODE_MODULES="$REMOTION/node_modules" ASTRID_FFMPEG_EXECUTABLE="$FFMPEG" \
    ASTRID_FFPROBE_EXECUTABLE="$FFPROBE" ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE" \
    ASTRID_RUNTIME_SOURCE_MANIFEST="$EVIDENCE/d13-profile-c886.json" ASTRID_RUNTIME_CHECKOUT="$SITE" \
    ASTRID_D13_SOURCE_PROFILE="$EVIDENCE/d13-profile-c886.json" \
    ASTRID_D13_EXPECTED_BINDINGS="$EVIDENCE/d13-bindings-c36-c886.json" \
    ASTRID_D13_NODE_SHA256=43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490 \
    ASTRID_D13_REMOTION_LOCK_SHA256=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d \
    ASTRID_D13_BROWSER_SHA256=85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95 \
    ASTRID_D13_FFMPEG_SHA256=ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41 \
    ASTRID_D13_FFPROBE_SHA256=272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f \
    "$PY" -B -m pytest -o addopts= -p no:cacheprovider --basetemp="$RUNROOT/pytest" \
    tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight -q

printf '%s\n' "D13 original installed preflight: PASS (one execution)"
printf '%s\n' "D13 wheel artifact: $WHEEL"
printf '%s\n' "D13 evidence manifest: $EVIDENCE/d13-wheel-manifest.json"

