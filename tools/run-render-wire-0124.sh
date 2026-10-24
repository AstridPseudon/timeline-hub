#!/bin/sh
set -eu

MODE=${1:-run}
case "$MODE" in
    run|preflight) ;;
    *) printf '%s\n' 'usage: run-render-wire-0124.sh [run|preflight]' >&2; exit 2 ;;
esac

# F-D32: the six original SDK/raw rendering-wire cases only.  This harness
# reuses the existing immutable installed child and qualified render route.
WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-wire-env-0124
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
BASE_AGENT=92baf961275baa42514bc120351ea512bfbe6e6b
RUNTIME_PIN=8ea0766f5e9fb23cea26c7398770a8aaac06b258
RUNTIME_TREE=6047ac3033c3594b8f83db3afd8bb2c47cafa6d6
AGENT_PIN=c36ca8c94b695b0e25b7d42c89f194661f187423
ARCHIVE_SHA=819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
LOCK_SHA=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
REGISTRY_STATE_SHA=d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96
REGISTRY_ANIMATIONS_SHA=02326f12177879eb5905f9d9b6d476b2de185928ddeeeeb2321a68ebffb47ad6
REGISTRY_EFFECTS_SHA=127e5653e0c66993726f8334b9f4ac122d24cdfbaa9e70cdaa142189afcf2bbe
REGISTRY_TRANSITIONS_SHA=c46d6bbd88712e775812867ec1cbe6de67473664775266c5a0b9317344ceb989
ARCHIVE="$PROFILE/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"

export CHILD CHILD_SOURCE RUNTIME PROFILE NODE SCHEMA INDEX BASE_AGENT RUNTIME_PIN RUNTIME_TREE AGENT_PIN
export ARCHIVE_SHA LOCK_SHA ARCHIVE
export REGISTRY_STATE_SHA REGISTRY_ANIMATIONS_SHA REGISTRY_EFFECTS_SHA REGISTRY_TRANSITIONS_SHA
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
tests/core/rendering/test_conformance.py::test_attachment_wire_parity
tests/core/rendering/test_conformance.py::test_intentional_failure_wire_parity
tests/core/rendering/test_conformance.py::test_minimal_render_wire_parity
tests/core/rendering/test_conformance.py::test_no_audio_wire_parity
tests/core/rendering/test_conformance.py::test_passthrough_audio_wire_parity
tests/core/rendering/test_conformance.py::test_request_sensitive_support_wire_parity
EOF

set +e
"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EXPECTED" <<'PY'
import ast
import hashlib
import importlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

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
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

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

def git_status(cwd: Path):
    return [line for line in git("status", "--porcelain", "--untracked-files=all", cwd=cwd).splitlines() if line]

def git_identity():
    head = git("rev-parse", "HEAD")
    parent = git("rev-parse", "HEAD^1")
    tree = git("rev-parse", "HEAD^{tree}")
    allowed = {"tools/run-render-wire-0124.sh"}
    changed = []
    for line in git_status(root):
        changed.append(line[3:] if len(line) >= 3 else line)
    assert head == os.environ["BASE_AGENT"] or parent == os.environ["BASE_AGENT"], {
        "head": head,
        "parent": parent,
    }
    assert set(changed) <= allowed, changed
    return {"head": head, "parent": parent, "tree": tree, "allowed_harness_changes": changed}

def runtime_identity():
    assert git("rev-parse", "HEAD", cwd=runtime) == os.environ["RUNTIME_PIN"]
    assert git("rev-parse", "HEAD^{tree}", cwd=runtime) == os.environ["RUNTIME_TREE"]
    assert not git_status(runtime)
    return {"head": git("rev-parse", "HEAD", cwd=runtime), "tree": git("rev-parse", "HEAD^{tree}", cwd=runtime), "status": "clean"}

def source_files():
    fixed = [
        "astrid/sdk/rendering.py",
        "astrid/core/foundation/atomic_io.py",
        "astrid/core/subprocess_env.py",
        "astrid/core/rendering/__init__.py",
        "astrid/core/rendering/transport.py",
        "tests/core/rendering/test_conformance.py",
    ]
    fixtures = subprocess.check_output(
        ["git", "ls-files", "tests/fixtures/renderer_packs/sdk"], cwd=root, text=True
    ).splitlines()
    return fixed + fixtures

def source_equality():
    paths = source_files()
    rows = {}
    for rel in paths:
        current, installed = root / rel, child_source / rel
        assert current.is_file() and installed.is_file(), rel
        current_sha, installed_sha = digest(current), digest(installed)
        rows[rel] = {"current": current_sha, "installed_c36": installed_sha, "equal": current_sha == installed_sha}
        assert current_sha == installed_sha, rel
    return {"files": len(rows), "paths": rows}

BODY_NAMES = [
    "test_minimal_render_wire_parity",
    "test_request_sensitive_support_wire_parity",
    "test_passthrough_audio_wire_parity",
    "test_no_audio_wire_parity",
    "test_attachment_wire_parity",
    "test_intentional_failure_wire_parity",
]

def body_hashes(path: Path):
    tree = ast.parse(path.read_text(), filename=str(path))
    result = {
        node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in BODY_NAMES
    }
    assert list(result) == BODY_NAMES, {"expected": BODY_NAMES, "actual": sorted(result)}
    return result

def six_body_hashes():
    current = body_hashes(root / "tests/core/rendering/test_conformance.py")
    installed = body_hashes(child_source / "tests/core/rendering/test_conformance.py")
    assert current == installed
    return {name: {"current": current[name], "installed_c36": installed[name]} for name in BODY_NAMES}

def source_origins():
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
print(json.dumps({'executable': str(Path(sys.executable).resolve()), 'prefix': str(Path(sys.prefix).resolve()), 'site': str(site), 'origins': {name: str(Path(mod.__file__).resolve()) for name, mod in mods.items()}, 'version': list(sys.version_info[:3])}))
"""
    result = subprocess.run([str(child / "bin/python"), "-I", "-B", "-c", code], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    actual = json.loads(result.stdout)
    site = child / "lib/python3.13/site-packages"
    assert actual["executable"] == str(child / "bin/python")
    assert actual["prefix"] == str(child)
    assert actual["version"] == [3, 13, 16]
    assert all(Path(path).is_relative_to(site) for path in actual["origins"].values()), actual
    return actual

def profile_inventory():
    assert profile.is_dir()
    registry_files = {
        ".astrid-registry-state.json",
        "src/animations.generated.ts",
        "src/effects.generated.ts",
        "src/transitions.generated.ts",
    }
    rows, writable, external_links = [], [], []
    for path in sorted(profile.rglob("*")):
        mode = stat.S_IMODE(path.lstat().st_mode)
        kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
        if kind == "link":
            if not path.resolve().is_relative_to(profile):
                external_links.append(path.relative_to(profile).as_posix())
            size, sha = 0, ""
        elif kind == "file":
            size, sha = path.stat().st_size, digest(path)
            if mode & 0o222 and path.relative_to(profile).as_posix() not in registry_files:
                writable.append(path.relative_to(profile).as_posix())
        else:
            size, sha = 0, ""
        rows.append((path.relative_to(profile).as_posix(), kind, mode, size, sha))
    assert not writable, writable
    assert not external_links, external_links
    registry = {
        ".astrid-registry-state.json": os.environ["REGISTRY_STATE_SHA"],
        "src/animations.generated.ts": os.environ["REGISTRY_ANIMATIONS_SHA"],
        "src/effects.generated.ts": os.environ["REGISTRY_EFFECTS_SHA"],
        "src/transitions.generated.ts": os.environ["REGISTRY_TRANSITIONS_SHA"],
    }
    assert {name: digest(profile / name) for name in registry} == registry
    return {"entries": len(rows), "writable": writable, "external_links": external_links, "registry": registry, "sha256": hashlib.sha256("\n".join("|".join(map(str, row)) for row in rows).encode()).hexdigest()}

def profile_facts():
    lock = profile / "package-lock.json"
    archive = Path(os.environ["ARCHIVE"])
    package = json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())
    assert digest(lock) == os.environ["LOCK_SHA"]
    assert digest(archive) == os.environ["ARCHIVE_SHA"]
    assert package["version"] == "0.0.14"
    return {"inventory": profile_inventory(), "package_lock_sha256": digest(lock), "archive_sha256": digest(archive), "composition_version": package["version"]}

def bench_identity():
    index = json.loads(index_path.read_text())
    entry = index["entries"][child.name]
    assert entry["path"] == str(child)
    assert entry["identity"]["agent_sha"] == os.environ["AGENT_PIN"]
    assert entry["identity"]["backend_sha"] == "abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e"
    assert set(entry["identity"]["client_tuple"]) == {
        "packages/python/astrid_runtime_client/__init__.py",
        "packages/python/astrid_runtime_client/contract_metadata.py",
        "packages/python/astrid_runtime_client/generated.py",
        "packages/python/astrid_runtime_client/timeline_commit_types.py",
    }
    return {"key": entry["key"], "identity": entry["identity"], "path": entry["path"]}

def node_facts():
    result = subprocess.run([str(node), "--version"], capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "v20.19.4"
    return {"path": str(node), "version": result.stdout.strip()}

def environment_facts():
    assert os.environ.get("PYTHONNOUSERSITE") is None
    assert os.environ.get("PYTEST_PLUGINS") is None and os.environ.get("PYTEST_ADDOPTS") is None
    forbidden = ("ASTRID_NORMAL_RUNTIME_SOURCE", "ASTRID_PARENT_MEDIA_SEED_RUNTIME", "ASTRID_WORD_ANCHOR_SEED_RUNTIME", "ASTRID_RUNTIME_SOURCE_MANIFEST")
    assert not any(name in os.environ for name in forbidden), {name: os.environ.get(name) for name in forbidden}
    return {"PYTHONPATH": os.environ["PYTHONPATH"], "ASTRID_RUNTIME_CHECKOUT": os.environ["ASTRID_RUNTIME_CHECKOUT"], "ASTRID_RUNTIME_SOURCE_ROOT": os.environ["ASTRID_RUNTIME_SOURCE_ROOT"], "forbidden_absent": True}

def collect_exact():
    expected = expected_path.read_text().splitlines()
    result = subprocess.run(
        [str(child / "bin/python"), "-P", "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider", "--collect-only", *expected],
        capture_output=True,
        text=True,
        check=False,
    )
    (out_path.parent / "collect.txt").write_text(result.stdout + result.stderr)
    actual = sorted(line.strip() for line in result.stdout.splitlines() if line.startswith("tests/"))
    assert result.returncode == 0, {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    assert actual == sorted(expected), {"expected": expected, "actual": actual}
    return {"count": len(actual), "nodeids": actual}

check("installed executable and Python pin", lambda: {"executable": str(child / "bin/python"), "version": subprocess.check_output([str(child / "bin/python"), "-V"], text=True, stderr=subprocess.STDOUT).strip()})
check("Agent source identity", git_identity)
check("Runtime pin and clean checkout", runtime_identity)
check("installed child bench identity", bench_identity)
check("source equality with installed Agent c36", source_equality)
check("six original body hashes", six_body_hashes)
check("parent Agent and Runtime import origins", source_origins)
check("installed child import origins", installed_origins)
check("Node20 and render profile", node_facts)
check("installed profile read-only custody", profile_facts)
check("qualified environment", environment_facts)
check("exact six original selectors collect", collect_exact)

report = {
    "status": "passed" if not failures else "failed",
    "failures": failures,
    "checks": checks,
    "scope": {
        "selected": expected_path.read_text().splitlines(),
        "excluded": ["tests/core/rendering/test_conformance.py::test_fixture_pack_static_surface"],
        "installed_component_scope": ["sdk renderer", "atomic_io", "subprocess_env", "core rendering transport", "SDK fixture tree"],
    },
}
out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(f"D32_PREFLIGHT_RESULT={report['status'].upper()} failures={len(failures)}", flush=True)
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
import json
import os
import subprocess
import sys
from pathlib import Path

before = json.loads(Path(sys.argv[1]).read_text())
root = Path.cwd().resolve()
runtime = Path(os.environ["RUNTIME"]).resolve()
changed = [line for line in subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True).splitlines() if line]
changed_paths = [line[3:] if len(line) >= 3 else line for line in changed]
failures = []
if set(changed_paths) - {"tools/run-render-wire-0124.sh"}:
    failures.append({"check": "source custody after body", "value": changed_paths})
if subprocess.check_output(["git", "-C", str(runtime), "status", "--porcelain"], text=True):
    failures.append({"check": "Runtime custody after body", "value": "dirty"})
after = {"before": before, "changed_paths": changed_paths, "failures": failures}
Path(sys.argv[2]).write_text(json.dumps(after, indent=2, sort_keys=True) + "\n")
print(f"D32_POSTFLIGHT={'PASS' if not failures else 'FAIL'} failures={len(failures)}", flush=True)
raise SystemExit(bool(failures))
PY
POST_STATUS=$?
set -e

"$PYTHON" -P - "$EVIDENCE/junit.xml" "$EVIDENCE/outcome-map.json" "$EXPECTED" <<'PY'
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

junit, out, expected_path = map(Path, sys.argv[1:])
expected = set(expected_path.read_text().splitlines())
cases = []
for case in ET.parse(junit).getroot().iter("testcase"):
    child = next(iter(case), None)
    outcome = "passed" if child is None else {"failure": "failed", "error": "error", "skipped": "skipped"}.get(child.tag, child.tag)
    longrepr = "" if child is None else child.text or ""
    nodeid = f"{case.get('classname').replace('.', '/')}.py::{case.get('name')}"
    cases.append({
        "nodeid": nodeid,
        "phase": "call",
        "outcome": outcome,
        "duration": case.get("time"),
        "longrepr": longrepr,
        "observed": {
            "stderr": sorted(set(re.findall(r"(?im)^.*(?:stderr|traceback|modulenotfounderror|error:).*$", longrepr))),
            "cwd": sorted(set(re.findall(r"(?im)^.*(?:cwd|working directory).*$", longrepr))),
            "result_producer": sorted(set(re.findall(r"(?im)^.*(?:result(?:\\.json| file)?|producer|executor).*$", longrepr))),
        },
    })
actual = {case["nodeid"] for case in cases}
assert actual == expected, {"expected": sorted(expected), "actual": sorted(actual)}
out.write_text(json.dumps({"selected": len(cases), "cases": cases}, indent=2, sort_keys=True) + "\n")
PY

printf 'pytest_exit=%s\npostflight_exit=%s\nselected=6\n' "$TEST_STATUS" "$POST_STATUS" > "$EVIDENCE/result.txt"
exit "$TEST_STATUS"
