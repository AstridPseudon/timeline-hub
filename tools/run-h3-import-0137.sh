#!/bin/sh
set -eu

MODE=${1:-run}
case "$MODE" in
    run|preflight) ;;
    *) printf '%s\n' 'usage: run-h3-import-0137.sh [run|preflight]' >&2; exit 2 ;;
esac

# F-D32: the seven original CPU host-readiness cases only.  This harness uses
# the already qualified installed child; it never provisions or mutates it.
WORKER=${H3_IMPORT_WORKER_DIR:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-h3-env-0137}
EVIDENCE="$WORKER/evidence"
mkdir -p "$EVIDENCE"

CHILD=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
CHILD_SOURCE="$CHILD/.child-venv-source-venv-agent-child-f-post-g5-c36-abd47-store/agent"
PYTHON="$CHILD/bin/python"
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
INDEX=/home/user/work/bench-store/index.json
RUNTIME_PIN=8ea0766f5e9fb23cea26c7398770a8aaac06b258
RUNTIME_TREE=6047ac3033c3594b8f83db3afd8bb2c47cafa6d6
AGENT_PIN=c36ca8c94b695b0e25b7d42c89f194661f187423
BACKEND_PIN=abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e
ARCHIVE_SHA=819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
LOCK_SHA=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
ARCHIVE="$PROFILE/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"

: "${EXPECTED_SOURCE_TREE:?set EXPECTED_SOURCE_TREE to the finalized source tree}"
export CHILD CHILD_SOURCE RUNTIME PROFILE NODE SCHEMA INDEX RUNTIME_PIN RUNTIME_TREE
export AGENT_PIN BACKEND_PIN ARCHIVE_SHA LOCK_SHA ARCHIVE EXPECTED_SOURCE_TREE
export HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$PWD:$RUNTIME"
export PATH="$CHILD/bin:/usr/bin:/bin"
export ASTRID_HOST_EXECUTION_PROFILE=installed
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset PYTEST_PLUGINS PYTEST_ADDOPTS PYTHONNOUSERSITE

EXPECTED="$EVIDENCE/expected-nodeids.txt"
cat > "$EXPECTED" <<'EOF'
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_revision]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[missing_content]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[revision_drift]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[content_drift]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[checkout_drift]
tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[profile_hash_drift]
EOF

set +e
"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EXPECTED" <<'PY'
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

out_path, expected_path = map(Path, sys.argv[1:])
root = Path.cwd().resolve()
child = Path(os.environ["CHILD"]).resolve()
child_source = Path(os.environ["CHILD_SOURCE"]).resolve()
runtime = Path(os.environ["RUNTIME"]).resolve()
profile = Path(os.environ["PROFILE"]).resolve()
node = Path(os.environ["NODE"]).resolve()
schema = Path(os.environ["SCHEMA"]).resolve()
index_path = Path(os.environ["INDEX"])
failures = []
checks = []

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(label, fn):
    try:
        value = fn()
        checks.append({"label": label, "status": "PASS", "value": value})
        print(f"PASS {label}: {value}", flush=True)
    except Exception as exc:
        value = f"{type(exc).__name__}: {exc}"
        failures.append(label)
        checks.append({"label": label, "status": "FAIL", "value": value})
        print(f"FAIL {label}: {value}", flush=True)

def git(*args: str, cwd: Path = root) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()

def status(cwd: Path):
    return [line for line in subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=cwd, text=True
    ).splitlines() if line]

def prerequisites():
    required = {
        "source root": root,
        "installed child": child,
        "installed interpreter": child / "bin/python",
        "installed Agent source": child_source,
        "Runtime checkout": runtime,
        "Runtime package": runtime / "runtime_protocol/__init__.py",
        "render profile": profile,
        "profile lock": profile / "package-lock.json",
        "profile archive": Path(os.environ["ARCHIVE"]),
        "Node20 executable": node,
        "schema site-packages": schema / "banodoco_timeline_schema/__init__.py",
        "bench index": index_path,
    }
    missing = [f"{label}={path}" for label, path in required.items() if not path.exists()]
    assert not missing, "missing prerequisites: " + "; ".join(missing)
    return {label: str(path) for label, path in required.items()}

def git_identity():
    tree = git("rev-parse", "HEAD^{tree}")
    assert tree == os.environ["EXPECTED_SOURCE_TREE"], {
        "tree": tree, "expected_tree": os.environ["EXPECTED_SOURCE_TREE"],
        "head": git("rev-parse", "HEAD"),
    }
    changed = status(root)
    allowed = {"tools/run-h3-import-0137.sh"}
    paths = [line[3:] if len(line) >= 3 else line for line in changed]
    assert set(paths) <= allowed, paths
    return {"head": git("rev-parse", "HEAD"), "tree": tree, "changed": paths}

def runtime_identity():
    assert git("rev-parse", "HEAD", cwd=runtime) == os.environ["RUNTIME_PIN"]
    assert git("rev-parse", "HEAD^{tree}", cwd=runtime) == os.environ["RUNTIME_TREE"]
    assert not status(runtime)
    return {"head": git("rev-parse", "HEAD", cwd=runtime), "tree": git("rev-parse", "HEAD^{tree}", cwd=runtime)}

SOURCE_HASHES = {
    "astrid/core/execution/generic_host.py": "fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3",
    "astrid/sdk/host_bootstrap.py": "50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07",
    "tests/helpers/h3_cpu_runtime.py": "8b5acd4db61b1cabea66389ee9c4858df6cc1ae55ddb7f5e74b6ccac00e22bd6",
    "tests/packs/h3_av/test_character_swap_cpu_boundary.py": "242ce54e59367aae0af8ac51b70d286f9fae7b8b29a5ab3b78920eeba91dd815",
}

def source_equality():
    rows = {}
    for rel, expected in SOURCE_HASHES.items():
        current, installed = root / rel, child_source / rel
        assert current.is_file() and installed.is_file(), rel
        current_sha, installed_sha = digest(current), digest(installed)
        assert current_sha == expected, {"path": rel, "current": current_sha, "expected": expected}
        assert current_sha == installed_sha, {"path": rel, "current": current_sha, "installed_c36": installed_sha}
        rows[rel] = {"current": current_sha, "installed_c36": installed_sha}
    return {"files": len(rows), "paths": rows}

BODY_HASH = "ae56aaf49eb0d3c7488405a2c930fc097a7789fecf06ec3ca349b3a38c04197c"
FAULTS = ["success", "missing_revision", "missing_content", "revision_drift", "content_drift", "checkout_drift", "profile_hash_drift"]

def target_body(path: Path):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "test_cpu_host_readiness_identity_reaches_real_installed_guard":
            return hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    raise AssertionError("target test body not found")

def target_body_hashes():
    current = target_body(root / "tests/packs/h3_av/test_character_swap_cpu_boundary.py")
    installed = target_body(child_source / "tests/packs/h3_av/test_character_swap_cpu_boundary.py")
    assert current == BODY_HASH and installed == current, {"current": current, "installed_c36": installed}
    source = (root / "tests/packs/h3_av/test_character_swap_cpu_boundary.py").read_text()
    assert '"fault", ["success", "missing_revision", "missing_content",\n                                  "revision_drift", "content_drift", "checkout_drift",\n                                  "profile_hash_drift"]' in source
    return {"body_sha256": current, "faults": FAULTS, "count": len(FAULTS)}

def parent_origins():
    import astrid
    import astrid_runtime_client
    import runtime_protocol
    import astrid.core.timeline.banodoco_schema as schema_module
    import banodoco_timeline_schema as shared_schema
    actual = {
        "executable": str(Path(sys.executable).resolve()),
        "astrid": str(Path(astrid.__file__).resolve()),
        "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
        "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
        "banodoco_schema": str(Path(schema_module.__file__).resolve()),
        "shared_schema": str(Path(shared_schema.__file__).resolve()),
    }
    expected = {
        "executable": str(child / "bin/python"),
        "astrid": str(root / "astrid/__init__.py"),
        "astrid_runtime_client": str(root / "astrid_runtime_client/__init__.py"),
        "runtime_protocol": str(runtime / "runtime_protocol/__init__.py"),
        "banodoco_schema": str(root / "astrid/core/timeline/banodoco_schema.py"),
        "shared_schema": str(schema / "banodoco_timeline_schema/__init__.py"),
    }
    assert actual == expected, {"actual": actual, "expected": expected}
    return actual

def installed_origins():
    code = """
import importlib, json, sys
from pathlib import Path
names = ('astrid', 'astrid_runtime', 'astrid_runtime_client', 'runtime_protocol')
mods = {name: importlib.import_module(name) for name in names}
site = Path(sys.prefix).resolve() / 'lib' / 'python3.13' / 'site-packages'
print(json.dumps({'executable': str(Path(sys.executable).resolve()), 'prefix': str(Path(sys.prefix).resolve()), 'origins': {name: str(Path(mod.__file__).resolve()) for name, mod in mods.items()}, 'version': list(sys.version_info[:3]), 'site': str(site)}))
"""
    result = subprocess.run([str(child / "bin/python"), "-I", "-B", "-c", code], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    actual = json.loads(result.stdout)
    site = child / "lib/python3.13/site-packages"
    assert actual["executable"] == str(child / "bin/python") and actual["prefix"] == str(child)
    assert actual["version"] == [3, 13, 16]
    assert all(Path(path).is_relative_to(site) for path in actual["origins"].values()), actual
    return actual

def bench_identity():
    entry = json.loads(index_path.read_text())["entries"][child.name]
    assert entry["path"] == str(child)
    assert entry["identity"]["agent_sha"] == os.environ["AGENT_PIN"]
    assert entry["identity"]["backend_sha"] == os.environ["BACKEND_PIN"]
    return {"key": entry["key"], "identity": entry["identity"], "path": entry["path"]}

def profile_facts():
    lock = profile / "package-lock.json"
    package = json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())
    assert digest(lock) == os.environ["LOCK_SHA"]
    assert digest(Path(os.environ["ARCHIVE"])) == os.environ["ARCHIVE_SHA"]
    assert package["version"] == "0.0.14"
    writable, external = [], []
    registry = {".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"}
    for path in profile.rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(profile):
            external.append(str(path.relative_to(profile)))
        elif path.is_file() and stat.S_IMODE(path.stat().st_mode) & 0o222 and str(path.relative_to(profile)) not in registry:
            writable.append(str(path.relative_to(profile)))
    assert not writable and not external, {"writable": writable, "external_links": external}
    return {"lock_sha256": digest(lock), "archive_sha256": digest(Path(os.environ["ARCHIVE"])), "composition_version": package["version"], "writable": writable, "external_links": external}

def node_facts():
    result = subprocess.run([str(node), "--version"], capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "v20.19.4"
    return {"path": str(node), "version": result.stdout.strip()}

def environment_facts():
    forbidden = ("ASTRID_NORMAL_RUNTIME_SOURCE", "ASTRID_PARENT_MEDIA_SEED_RUNTIME", "ASTRID_WORD_ANCHOR_SEED_RUNTIME", "ASTRID_RUNTIME_SOURCE_MANIFEST")
    assert not any(name in os.environ for name in forbidden), {name: os.environ.get(name) for name in forbidden}
    return {"PYTHONPATH": os.environ["PYTHONPATH"], "profile": os.environ["ASTRID_HOST_EXECUTION_PROFILE"], "forbidden_absent": True}

def collect_exact():
    expected = expected_path.read_text().splitlines()
    result = subprocess.run([str(child / "bin/python"), "-P", "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider", "--collect-only", *expected], capture_output=True, text=True, check=False)
    (out_path.parent / "collect.txt").write_text(result.stdout + result.stderr)
    actual = sorted(line.strip() for line in result.stdout.splitlines() if line.startswith("tests/"))
    assert result.returncode == 0, {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    assert actual == sorted(expected), {"expected": expected, "actual": actual}
    return {"count": len(actual), "nodeids": actual}

check("trivial boot prerequisites", prerequisites)
check("Agent source tree identity and custody", git_identity)
check("Runtime pin and clean checkout", runtime_identity)
check("installed child bench identity", bench_identity)
check("source equality with installed Agent c36", source_equality)
check("seven original body hashes and guard branches", target_body_hashes)
check("parent current-source import origins", parent_origins)
check("installed child isolated import origins", installed_origins)
check("Node20 and read-only render profile", lambda: {"node": node_facts(), "profile": profile_facts()})
check("qualified environment", environment_facts)
check("exact seven original selectors collect", collect_exact)

report = {"status": "passed" if not failures else "failed", "failures": failures, "checks": checks, "scope": {"selected": expected_path.read_text().splitlines(), "guard_faults": FAULTS, "installed_child": str(child), "installed_agent_revision": os.environ["AGENT_PIN"], "runtime_revision": os.environ["RUNTIME_PIN"]}}
out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(f"H3_IMPORT_PREFLIGHT={'PASS' if not failures else 'FAIL'} failures={len(failures)}", flush=True)
raise SystemExit(bool(failures))
PY
PREFLIGHT=$?
set -e

if [ "$MODE" = preflight ] || [ "$PREFLIGHT" -ne 0 ]; then
    exit "$PREFLIGHT"
fi

set +e
timeout 1500 "$PYTHON" -P - "$EXPECTED" "$EVIDENCE/junit.xml" > "$EVIDENCE/pytest.log" 2>&1 <<'PY'
import sys
from pathlib import Path
import pytest

selectors = Path(sys.argv[1]).read_text().splitlines()
raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", f"--junitxml={sys.argv[2]}", *selectors]))
PY
TEST_STATUS=$?
set -e

set +e
"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EVIDENCE/postflight.json" <<'PY'
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

before = json.loads(Path(sys.argv[1]).read_text())
root = Path.cwd().resolve()
child_source = Path(os.environ["CHILD_SOURCE"]).resolve()
failures = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for rel, expected in before["checks"][4]["value"]["paths"].items():
    current, installed = root / rel, child_source / rel
    if digest(current) != expected["current"] or digest(current) != digest(installed):
        failures.append({"source": rel, "current": digest(current), "installed_c36": digest(installed)})
test_path = root / "tests/packs/h3_av/test_character_swap_cpu_boundary.py"
tree = ast.parse(test_path.read_text())
body = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "test_cpu_host_readiness_identity_reaches_real_installed_guard")
body_sha = hashlib.sha256(ast.dump(body, include_attributes=False).encode()).hexdigest()
if body_sha != "ae56aaf49eb0d3c7488405a2c930fc097a7789fecf06ec3ca349b3a38c04197c":
    failures.append({"target_body_sha256": body_sha})
changed = [line for line in subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True).splitlines() if line]
paths = [line[3:] if len(line) >= 3 else line for line in changed]
if set(paths) - {"tools/run-h3-import-0137.sh"}:
    failures.append({"source_custody": paths})
runtime = Path(os.environ["RUNTIME"])
if subprocess.check_output(["git", "status", "--porcelain"], cwd=runtime, text=True):
    failures.append({"runtime_custody": "dirty"})
result = {"status": "passed" if not failures else "failed", "source_equality": "passed" if not failures else "failed", "changed_paths": paths, "failures": failures}
Path(sys.argv[2]).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(f"H3_IMPORT_POSTFLIGHT={'PASS' if not failures else 'FAIL'} failures={len(failures)}", flush=True)
raise SystemExit(bool(failures))
PY
POST_STATUS=$?
set -e

"$PYTHON" -P - "$EVIDENCE/junit.xml" "$EVIDENCE/outcome-map.json" "$EXPECTED" <<'PY'
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

junit, out, expected_path = map(Path, sys.argv[1:])
expected = set(expected_path.read_text().splitlines())
cases = []
for case in ET.parse(junit).getroot().iter("testcase"):
    child = next(iter(case), None)
    outcome = "passed" if child is None else {"failure": "failed", "error": "error", "skipped": "skipped"}.get(child.tag, child.tag)
    nodeid = f"{case.get('classname').replace('.', '/')}.py::{case.get('name')}"
    cases.append({"nodeid": nodeid, "outcome": outcome, "duration": case.get("time"), "detail": "" if child is None else child.text or ""})
actual = {case["nodeid"] for case in cases}
assert actual == expected, {"expected": sorted(expected), "actual": sorted(actual)}
out.write_text(json.dumps({"selected": len(cases), "cases": cases}, indent=2, sort_keys=True) + "\n")
PY

SCRIPT_SHA=$(sha256sum "$PWD/tools/run-h3-import-0137.sh" | awk '{print $1}')
TREE=$(git rev-parse HEAD^{tree})
printf 'pytest_exit=%s\npostflight_exit=%s\nselected=7\nscript_sha256=%s\ntarget_source_tree=%s\n' "$TEST_STATUS" "$POST_STATUS" "$SCRIPT_SHA" "$TREE" > "$EVIDENCE/result.txt"
exit "$((TEST_STATUS || POST_STATUS))"
