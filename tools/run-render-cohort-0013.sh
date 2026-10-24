#!/bin/sh
set -eu

MODE=${1:-run}
case "$MODE" in
    run|preflight) ;;
    tests/*) MODE=selected ;;
    *) printf '%s\n' 'usage: run-render-cohort-0013.sh [run|preflight]' >&2; exit 2 ;;
esac

# F/D18/D21/D22: bounded rendering-originals qualification only. The
# producer remains the existing canonical render executor.
WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-managed-0013
EVIDENCE="$WORKER/evidence"
[ "$MODE" = selected ] && EVIDENCE="$WORKER/evidence-path-node-five"
mkdir -p "$EVIDENCE"
CHILD=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
PYTHON="$CHILD/bin/python"
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
NODE_BIN=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
OUTCOMES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-qualified-full-sol-2225/outcomes-.test-agent-full-post-g5-2225-1023222822-25691-17158.jsonl.gz
INDEX=/home/user/work/bench-store/index.json
export CHILD RUNTIME PROFILE NODE NODE_BIN SCHEMA OUTCOMES INDEX

export HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$PWD:$RUNTIME"
# Keep the managed child environment first, while making the existing pinned
# Node toolchain visible to both this caller and every managed-child process.
export PATH="$CHILD/bin:$NODE_BIN:/usr/bin:/bin"
export ASTRID_HOST_EXECUTION_PROFILE=installed
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset PYTEST_PLUGINS PYTEST_ADDOPTS PYTHONNOUSERSITE

"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EVIDENCE/expected-nodeids.txt" <<'PY'
import ast
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

out, expected_path = map(Path, sys.argv[1:])
root = Path.cwd().resolve()
child = Path(os.environ["CHILD"]).resolve()
runtime = Path(os.environ["RUNTIME"]).resolve()
profile = Path(os.environ["PROFILE"]).resolve()
node = Path(os.environ["NODE"]).resolve()
node_bin = Path(os.environ["NODE_BIN"]).resolve()
schema = Path(os.environ["SCHEMA"]).resolve()
index_path = Path(os.environ["INDEX"])
direct_files = {
    "tests/core/rendering/test_freeze.py": 1,
    "tests/core/rendering/test_service.py": 3,
    "tests/packs/rendering/test_builtin_registration.py": 1,
    "tests/packs/rendering/test_ffmpeg_backend.py": 1,
    "tests/packs/rendering/test_remotion_backend.py": 1,
    "tests/packs/rendering/test_threejs_backend.py": 6,
    "tests/stage1/test_media_handoff_render_boundary.py": 1,
}
conformance_file = "tests/core/rendering/test_conformance.py"
export_file = "tests/packs/rendering/test_render_export_task_adapter.py"
source_files = [*direct_files, conformance_file, export_file]
source_hashes = {
    "tests/core/rendering/test_conformance.py": "0432b08e11c18db61e68fac747dad9e7a44f59cf42297a8aa15f071ba59d3a46",
    "tests/core/rendering/test_freeze.py": "ae0e4c3d0752f5953e65e549b5c65dff324c75fd1d6953fb9f2adb8073aa8f7d",
    "tests/core/rendering/test_service.py": "6341d59c3189bf5af79fc9b06c45a55081255597aa98a30456d324cc33e6679a",
    "tests/packs/rendering/test_builtin_registration.py": "e71865f4b70e6da9e8f93de0393fc12aee062d9995d256630b2b9bd319722cfb",
    "tests/packs/rendering/test_ffmpeg_backend.py": "ed0f97098dfd544c3dd0e08f8cc533b2f54dfc03efa003a8d4716b766e1edc69",
    "tests/packs/rendering/test_remotion_backend.py": "d55004cd934bc3614f22bcb8fc223fb1f47e2da37282af8556fc821ac69d15bb",
    "tests/packs/rendering/test_render_export_task_adapter.py": "e7baa7597359ee72cefef672a9c6e6f2719213b971594d5034889011ba3fa5a8",
    "tests/packs/rendering/test_threejs_backend.py": "9efe493cb2f8339177e07616b976afe6f9813ae4d415923ff25701b471e991c7",
    "tests/stage1/test_media_handoff_render_boundary.py": "1e11ffaef51c875a55274e4cd8249e06ab76d0899ca6c83a2b51a8ed8e859adc",
}
body_names = {
    "tests/core/rendering/test_conformance.py": {"test_minimal_render_wire_parity", "test_request_sensitive_support_wire_parity", "test_passthrough_audio_wire_parity", "test_no_audio_wire_parity", "test_attachment_wire_parity", "test_intentional_failure_wire_parity"},
    "tests/core/rendering/test_freeze.py": {"test_freeze_real_ffmpeg_transport_one_video_one_committed_sidecar"},
    "tests/core/rendering/test_service.py": {"test_real_ffmpeg_renders_through_generic_service", "test_real_ffmpeg_audio_reactive_through_generic_service"},
    "tests/packs/rendering/test_builtin_registration.py": {"test_real_ffmpeg_render_through_registered_backend"},
    "tests/packs/rendering/test_ffmpeg_backend.py": {"test_manifest_command_dispatches_from_pack_root"},
    "tests/packs/rendering/test_remotion_backend.py": {"test_manifest_command_runs_from_owning_pack_root"},
    "tests/packs/rendering/test_render_export_task_adapter.py": {"test_render_export_adapter_writes_real_mp4_and_is_callable"},
    "tests/packs/rendering/test_threejs_backend.py": {"test_threejs_support_accepts_empty_and_exact_text_fields", "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons", "test_threejs_support_rejects_non_rendered_audio_ownership", "test_threejs_support_accepts_window_and_rejects_fps_mismatch", "test_threejs_identity_invariants_never_claim_remotion", "test_threejs_own_namespace_config_is_strict"},
    "tests/stage1/test_media_handoff_render_boundary.py": {"test_host_derived_registry_executes_canonical_ffmpeg_executor"},
}

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ast_hashes(path, names):
    tree = ast.parse(path.read_text(), filename=str(path))
    return {node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest() for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names}

def git_facts(cwd):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()
    status = git("status", "--porcelain", "--untracked-files=all")
    if cwd == root:
        status = "\n".join(line for line in status.splitlines() if "tools/run-render-cohort-0013.sh" not in line)
    return {"head": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}"), "status": status}

def profile_facts():
    rows, writable = [], []
    for path in sorted(profile.rglob("*")):
        rel, mode = path.relative_to(profile).as_posix(), stat.S_IMODE(path.lstat().st_mode)
        kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
        if kind != "link" and mode & 0o222:
            writable.append(rel)
        rows.append((rel, kind, mode, path.stat().st_size if kind == "file" else 0, digest(path) if kind == "file" else ""))
    return {"count": len(rows), "writable": writable, "sha256": hashlib.sha256("\n".join("|".join(map(str, row)) for row in rows).encode()).hexdigest()}

def registry_facts():
    result = {}
    for rel in (".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"):
        path = profile / rel
        result[rel] = {"exists": path.exists(), "mode": stat.S_IMODE(path.stat().st_mode) if path.exists() else None, "sha256": digest(path) if path.is_file() else None}
    return result

assert child == Path("/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e")
assert runtime == Path("/home/user/work/wt/rt-pin-8ea0766f")
assert profile == Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110")
assert schema.is_dir() and node.is_file() and os.access(node, os.X_OK)
assert node.parent == node_bin
assert os.environ.get("PYTHONNOUSERSITE") is None
for name in ("ASTRID_NORMAL_RUNTIME_SOURCE", "ASTRID_PARENT_MEDIA_SEED_RUNTIME", "ASTRID_WORD_ANCHOR_SEED_RUNTIME", "ASTRID_RUNTIME_SOURCE_MANIFEST"):
    assert name not in os.environ, name
path_node = Path(shutil.which("node") or "")
path_npx = Path(shutil.which("npx") or "")
assert path_node == node, (path_node, node, os.environ["PATH"])
assert path_npx == node_bin / "npx", (path_npx, node_bin, os.environ["PATH"])
node_version = subprocess.check_output([str(path_node), "--version"], text=True).strip()
npx_version = subprocess.check_output([str(path_npx), "--version"], text=True).strip()
assert node_version == "v20.19.4"
assert npx_version == "10.8.2"
agent = git_facts(root)
runtime_git = git_facts(runtime)
if agent["head"] != "c36ca8c94b695b0e25b7d42c89f194661f187423":
    parent = subprocess.check_output(["git", "rev-parse", "HEAD^1"], cwd=root, text=True).strip()
    parent_tree = subprocess.check_output(["git", "rev-parse", "HEAD^1^{tree}"], cwd=root, text=True).strip()
    assert {
        "c36ca8c94b695b0e25b7d42c89f194661f187423": "50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92",
        "a8b737d9a5bee638f30cb947b5e58edccb0954f8": "654e2052922b54c321f066242b7b713b3c73b2d1",
    }.get(parent) == parent_tree
assert runtime_git == {"head": "8ea0766f5e9fb23cea26c7398770a8aaac06b258", "tree": "6047ac3033c3594b8f83db3afd8bb2c47cafa6d6", "status": ""}
assert {rel: digest(root / rel) for rel in source_files} == source_hashes
body_hashes = {rel: ast_hashes(root / rel, body_names[rel]) for rel in source_files}
assert len(body_hashes[conformance_file]) == 6 and len(body_hashes) == 9

with gzip.open(os.environ["OUTCOMES"], "rt") as stream:
    rows = [json.loads(line) for line in stream]
failed = [row for row in rows if row.get("outcome") == "failed"]
assert len(failed) == len({row["nodeid"] for row in failed}) == 267
selected = sorted(row["nodeid"] for row in failed if row["nodeid"].split("::", 1)[0] in {conformance_file, export_file, *direct_files})
assert len(selected) == 21
assert all(row["when"] == "call" for row in failed if row["nodeid"] in selected)
assert sum(nodeid.startswith(conformance_file + "::") for nodeid in selected) == 6
assert sum(nodeid.startswith(export_file + "::") for nodeid in selected) == 1
assert sum(nodeid.startswith(path + "::") for nodeid in selected for path in direct_files) == 14
expected_path.write_text("\n".join(selected) + "\n")

index = json.loads(index_path.read_text())
entry = index["entries"][child.name]
assert entry["identity"]["agent_sha"] == "c36ca8c94b695b0e25b7d42c89f194661f187423"
assert entry["identity"]["backend_sha"] == "abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e"
assert set(entry["identity"]["client_tuple"]) == {"packages/python/astrid_runtime_client/__init__.py", "packages/python/astrid_runtime_client/contract_metadata.py", "packages/python/astrid_runtime_client/generated.py", "packages/python/astrid_runtime_client/timeline_commit_types.py"}
assert entry["path"] == str(child)
registration = index["registrations"]["venv-agent-child-f-post-g5-c36-abd47-store"]
lock = profile / "package-lock.json"
archive = profile / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
assert digest(lock) == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"
assert digest(archive) == "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
assert json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"] == "0.0.14"

tools = {name: shutil.which(name) for name in ("ffmpeg", "ffprobe", "fc-match")}
assert all(tools.values()), tools
font = subprocess.check_output([tools["fc-match"], "-f", "%{file}\\n", "sans"], text=True).splitlines()[0]
assert Path(font).is_file(), font
media = {name: {"path": path, "version": subprocess.check_output([path, "-version"], text=True, stderr=subprocess.STDOUT).splitlines()[0]} for name, path in tools.items() if name != "fc-match"}
out.write_text(json.dumps({"status": "passed", "source": {"agent": agent, "runtime": runtime_git, "source_hashes": source_hashes, "body_hashes": body_hashes}, "bench_store": {"index": str(index_path), "entry": entry, "registration": registration}, "environment": {"mode": "installed", "child": str(child), "child_site": str(child / "lib/python3.13/site-packages"), "runtime": str(runtime), "profile": str(profile), "node": str(node), "node_bin": str(node_bin), "node_path": str(path_node), "node_version": node_version, "npx_path": str(path_npx), "npx_version": npx_version, "PATH": os.environ["PATH"], "schema_path": str(schema), "PYTHONPATH": os.environ["PYTHONPATH"], "PYTHONNOUSERSITE": None}, "profile": {"package_lock_sha256": digest(lock), "composition_archive_sha256": digest(archive), "composition_version": "0.0.14", "inventory": profile_facts(), "registry": registry_facts()}, "inputs": {"executables": media, "font": {"path": font, "sha256": digest(font)}}, "inventory": {"archive": os.environ["OUTCOMES"], "archive_sha256": digest(Path(os.environ["OUTCOMES"])), "failed_original_nodes": 267, "selected_nodes": selected, "counts": {"direct": 14, "sdk_conformance": 6, "export_adapter": 1}}, "supported_invocation": {"parent": "source checkout c36ca8c94b695b0e25b7d42c89f194661f187423", "child": "installed package via -I", "source_required_tests": selected, "note": "The parent caller uses the source checkout while the managed child proves installed identity; no fixture identity was forced."}}, indent=2, sort_keys=True) + "\n")
print("selected 21 rendering nodes from actual 267-call-failure inventory")
PY

"$PYTHON" -I -B - <<'PY' > "$EVIDENCE/installed-import-before.json"
import importlib.metadata, json, os, sys
from pathlib import Path
site = next((Path(sys.executable).resolve().parent.parent / "lib").glob("python*/site-packages"))
import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol
modules = {name: Path(module.__file__).resolve() for name, module in {"astrid": astrid, "astrid_runtime": astrid_runtime, "astrid_runtime_client": astrid_runtime_client, "runtime_protocol": runtime_protocol}.items()}
assert all(path.is_relative_to(site) for path in modules.values()), modules
metadata = {}
for name in ("astrid", "astrid-runtime"):
    dist = importlib.metadata.distribution(name)
    direct = json.loads((Path(dist._path) / "direct_url.json").read_text())
    record = Path(dist._path) / "RECORD"
    assert record.is_file() and direct["url"].startswith("file:")
    metadata[name] = {"version": dist.version, "direct_url": direct, "record": str(record), "record_sha256": __import__("hashlib").sha256(record.read_bytes()).hexdigest()}
print(json.dumps({"python": sys.executable, "site": str(site), "origins": {name: str(path) for name, path in modules.items()}, "metadata": metadata, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE"), "sys_path": sys.path}, sort_keys=True))
PY

"$PYTHON" -P - <<'PY' > "$EVIDENCE/source-import-before.json"
import json, os
from pathlib import Path
import astrid, astrid_runtime_client, runtime_protocol
import astrid.core.timeline.banodoco_schema as schema
import banodoco_timeline_schema as shared_schema
root, runtime = Path.cwd().resolve(), Path(os.environ["RUNTIME"]).resolve()
assert Path(astrid.__file__).resolve() == root / "astrid/__init__.py"
assert Path(astrid_runtime_client.__file__).resolve() == root / "astrid_runtime_client/__init__.py"
assert Path(runtime_protocol.__file__).resolve() == runtime / "runtime_protocol/__init__.py"
assert Path(schema.__file__).resolve() == root / "astrid/core/timeline/banodoco_schema.py"
assert Path(shared_schema.__file__).resolve() == Path(os.environ["SCHEMA"]) / "banodoco_timeline_schema/__init__.py"
print(json.dumps({"origins": {"astrid": str(Path(astrid.__file__).resolve()), "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()), "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()), "schema": str(Path(schema.__file__).resolve()), "shared_schema": str(Path(shared_schema.__file__).resolve())}, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}, sort_keys=True))
PY

if [ "$MODE" = preflight ]; then
    printf '%s\n' 'render cohort 0013 preflight passed'
    exit 0
fi

EXPECTED="$EVIDENCE/expected-nodeids.txt"
if [ "$MODE" = selected ]; then
    "$PYTHON" - "$EXPECTED" "$@" <<'PY'
import sys
from pathlib import Path

expected_path = Path(sys.argv[1])
requested = set(sys.argv[2:])
selected = {
    "tests/packs/rendering/test_threejs_backend.py::test_threejs_identity_invariants_never_claim_remotion",
    "tests/packs/rendering/test_threejs_backend.py::test_threejs_own_namespace_config_is_strict",
    "tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_empty_and_exact_text_fields",
    "tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_window_and_rejects_fps_mismatch",
    "tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons",
}
assert requested == selected, {"requested": sorted(requested), "required": sorted(selected)}
original = set(expected_path.read_text().splitlines())
assert selected <= original, {"missing_from_original": sorted(selected - original)}
expected_path.write_text("\n".join(sorted(selected)) + "\n")
PY
fi
"$PYTHON" -P - "$EXPECTED" > "$EVIDENCE/collect.txt" 2>&1 <<'PY'
import sys
from pathlib import Path
import pytest
raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--collect-only", *Path(sys.argv[1]).read_text().splitlines()]))
PY
python3 - "$EVIDENCE/collect.txt" "$EXPECTED" <<'PY'
from pathlib import Path
import sys
actual = {line.strip() for line in Path(sys.argv[1]).read_text().splitlines() if line.startswith("tests/")}
expected = set(Path(sys.argv[2]).read_text().splitlines())
assert actual == expected, {"actual": sorted(actual), "expected": sorted(expected)}
print(f"exact collect: {len(actual)} nodeids")
PY

set +e
timeout 1500 "$PYTHON" -P - "$EXPECTED" "$EVIDENCE/junit.xml" > "$EVIDENCE/pytest.log" 2>&1 <<'PY'
import sys
from pathlib import Path
import pytest
raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", f"--junitxml={sys.argv[2]}", *Path(sys.argv[1]).read_text().splitlines()]))
PY
test_status=$?
set -e

"$PYTHON" -I -B - <<'PY' > "$EVIDENCE/installed-import-after.json"
import importlib.metadata, json, os, sys
from pathlib import Path
site = next((Path(sys.executable).resolve().parent.parent / "lib").glob("python*/site-packages"))
import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol
modules = {name: Path(module.__file__).resolve() for name, module in {"astrid": astrid, "astrid_runtime": astrid_runtime, "astrid_runtime_client": astrid_runtime_client, "runtime_protocol": runtime_protocol}.items()}
assert all(path.is_relative_to(site) for path in modules.values()), modules
metadata = {}
for name in ("astrid", "astrid-runtime"):
    dist = importlib.metadata.distribution(name)
    direct = json.loads((Path(dist._path) / "direct_url.json").read_text())
    record = Path(dist._path) / "RECORD"
    assert record.is_file() and direct["url"].startswith("file:")
    metadata[name] = {"version": dist.version, "direct_url": direct, "record": str(record), "record_sha256": __import__("hashlib").sha256(record.read_bytes()).hexdigest()}
print(json.dumps({"python": sys.executable, "site": str(site), "origins": {name: str(path) for name, path in modules.items()}, "metadata": metadata, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}, sort_keys=True))
PY

"$PYTHON" -P - <<'PY' > "$EVIDENCE/source-import-after.json"
import json, os
from pathlib import Path
import astrid, astrid_runtime_client, runtime_protocol
import astrid.core.timeline.banodoco_schema as schema
import banodoco_timeline_schema as shared_schema
root, runtime = Path.cwd().resolve(), Path(os.environ["RUNTIME"]).resolve()
assert Path(astrid.__file__).resolve() == root / "astrid/__init__.py"
assert Path(astrid_runtime_client.__file__).resolve() == root / "astrid_runtime_client/__init__.py"
assert Path(runtime_protocol.__file__).resolve() == runtime / "runtime_protocol/__init__.py"
assert Path(schema.__file__).resolve() == root / "astrid/core/timeline/banodoco_schema.py"
assert Path(shared_schema.__file__).resolve() == Path(os.environ["SCHEMA"]) / "banodoco_timeline_schema/__init__.py"
print(json.dumps({"origins": {"astrid": str(Path(astrid.__file__).resolve()), "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()), "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()), "schema": str(Path(schema.__file__).resolve()), "shared_schema": str(Path(shared_schema.__file__).resolve())}, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}, sort_keys=True))
PY

"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EVIDENCE/postflight.json" <<'PY'
import ast, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
before = json.loads(Path(sys.argv[1]).read_text())
root, profile = Path.cwd().resolve(), Path(os.environ["PROFILE"])
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def body_hashes(path, names):
    tree = ast.parse(path.read_text(), filename=str(path))
    return {node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest() for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names}
def git_facts(cwd):
    def git(*args): return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()
    status = git("status", "--porcelain", "--untracked-files=all")
    if cwd == root:
        status = "\n".join(line for line in status.splitlines() if "tools/run-render-cohort-0013.sh" not in line)
    return {"head": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}"), "status": status}
def profile_facts():
    rows, writable = [], []
    for path in sorted(profile.rglob("*")):
        rel, mode = path.relative_to(profile).as_posix(), stat.S_IMODE(path.lstat().st_mode)
        kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
        if kind != "link" and mode & 0o222: writable.append(rel)
        rows.append((rel, kind, mode, path.stat().st_size if kind == "file" else 0, digest(path) if kind == "file" else ""))
    return {"count": len(rows), "writable": writable, "sha256": hashlib.sha256("\n".join("|".join(map(str, row)) for row in rows).encode()).hexdigest()}
def registry_facts():
    result = {}
    for rel in (".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"):
        path = profile / rel
        result[rel] = {"exists": path.exists(), "mode": stat.S_IMODE(path.stat().st_mode) if path.exists() else None, "sha256": digest(path) if path.is_file() else None}
    return result
agent, runtime = git_facts(root), git_facts(Path(os.environ["RUNTIME"]))
assert agent["head"] == before["source"]["agent"]["head"]
assert runtime == before["source"]["runtime"]
assert {rel: digest(root / rel) for rel in before["source"]["source_hashes"]} == before["source"]["source_hashes"]
assert {rel: body_hashes(root / rel, before["source"]["body_hashes"][rel].keys()) for rel in before["source"]["body_hashes"]} == before["source"]["body_hashes"]
assert profile_facts() == before["profile"]["inventory"]
assert registry_facts() == before["profile"]["registry"]
Path(sys.argv[2]).write_text(json.dumps({"source": {"agent": agent, "runtime": runtime, "source_hashes": before["source"]["source_hashes"], "body_hashes": before["source"]["body_hashes"]}, "profile": {"inventory": before["profile"]["inventory"], "registry": before["profile"]["registry"]}, "environment": {"PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}}, indent=2, sort_keys=True) + "\n")
PY

python3 - "$EVIDENCE/junit.xml" "$EVIDENCE/outcome-map.json" "$EVIDENCE/pytest.log" "$EXPECTED" <<'PY'
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
expected = set(Path(sys.argv[4]).read_text().splitlines())
cases = []
for case in ET.parse(sys.argv[1]).getroot().iter("testcase"):
    child = next(iter(case), None)
    outcome = "passed" if child is None else {"failure": "failed", "error": "error", "skipped": "skipped"}.get(child.tag, child.tag)
    longrepr = "" if child is None else child.text or ""
    nodeid = f"{case.get('classname').replace('.', '/')}.py::{case.get('name')}"
    assert nodeid in expected, nodeid
    observed = {label: sorted(set(re.findall(pattern, longrepr))) for label, pattern in {"stderr": r"(?im)^.*(?:stderr|traceback|modulenotfounderror|error:).*$", "cwd": r"(?im)^.*(?:cwd|working directory).*$", "result_producer": r"(?im)^.*(?:result(?:\\.json| file)?|producer|executor).*$"}.items()}
    cases.append({"nodeid": nodeid, "phase": "call", "outcome": outcome, "duration": case.get("time"), "longrepr": longrepr, "observed": observed})
assert {case["nodeid"] for case in cases} == expected
Path(sys.argv[2]).write_text(json.dumps({"selected": len(cases), "cases": cases, "source_cause": {"direct": "managed-child environment owner when runtime_protocol stderr is observed; preserve renderer predicates", "sdk_conformance": "missing result producer remains unconfirmed unless child stderr/result path identifies it", "export_adapter": "canonical executor failure remains unconfirmed unless child stderr/result path identifies it"}}, indent=2, sort_keys=True) + "\n")
PY

selected_count=$(wc -l < "$EXPECTED")
printf 'pytest_exit=%s\nselected=%s\n' "$test_status" "$selected_count" > "$EVIDENCE/result.txt"
printf 'render cohort 0013: pytest_exit=%s; selected=%s; phase outcomes and longrepr retained in %s\n' "$test_status" "$selected_count" "$EVIDENCE/outcome-map.json"
exit "$test_status"
