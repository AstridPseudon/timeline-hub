#!/bin/sh
set -eu

# F/D18/D21/D22: installed-child environment cohort only.  This is a harness
# entry point; it deliberately does not alter the product or test sources.
WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-env-cohort-2356
EVIDENCE="$WORKER/evidence"
mkdir -p "$EVIDENCE"
CHILD=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
PYTHON="$CHILD/bin/python"
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
OUTCOMES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-qualified-full-sol-2225/outcomes-.test-agent-full-post-g5-2225-1023222822-25691-17158.jsonl.gz
INDEX=/home/user/work/bench-store/index.json
export CHILD RUNTIME PROFILE NODE SCHEMA OUTCOMES INDEX

export HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$PWD:$RUNTIME"
export PATH="$CHILD/bin:/usr/bin:/bin"
export ASTRID_HOST_EXECUTION_PROFILE=installed
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset PYTEST_PLUGINS PYTEST_ADDOPTS PYTHONNOUSERSITE

python3 - "$EVIDENCE/preflight.json" "$EVIDENCE/expected-nodeids.txt" <<'PY'
import ast, gzip, hashlib, json, os, stat, subprocess, sys
from pathlib import Path

out, expected = map(Path, sys.argv[1:])
root = Path.cwd().resolve()
child = Path(os.environ["CHILD"]).resolve()
runtime = Path(os.environ["RUNTIME"]).resolve()
profile = Path(os.environ["PROFILE"]).resolve()
node = Path(os.environ["NODE"]).resolve()
schema = Path(os.environ["SCHEMA"]).resolve()
source_files = [
    "tests/core/execution/test_generic_host_actions_v3.py",
    "tests/core/execution/test_remotion_host_session.py",
    "tests/core/execution/test_worker_startup_identity.py",
    "tests/sdk/test_host_bootstrap_source_identity.py",
    "tests/core/pack/test_source_setup.py",
    "tests/packs/test_vibecomfy_ir_bridge.py",
    "tests/stage1/test_zero_shim_execution_pack_deletion.py",
    "tests/reshape/test_doctor_contract_shapes.py",
]
counts = {
    source_files[0]: 60, source_files[1]: 1, source_files[2]: 1,
    source_files[3]: 15, source_files[4]: 2, source_files[5]: 4,
    source_files[6]: 1, source_files[7]: 2,
}
owners = {
    source_files[3]: "startup/host + Runtime OPS",
    source_files[7]: "installed-profile/bootstrap",
}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def body_hashes(path, names):
    tree = ast.parse(path.read_text(), filename=str(path))
    return {
        node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names
    }

def profile_facts():
    rows, writable = [], []
    for path in sorted(profile.rglob("*")):
        rel, mode = path.relative_to(profile).as_posix(), stat.S_IMODE(path.lstat().st_mode)
        kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
        if kind != "link" and mode & 0o222:
            writable.append(rel)
        rows.append((rel, kind, mode, path.stat().st_size if kind == "file" else 0, sha(path) if kind == "file" else ""))
    return {
        "count": len(rows),
        "writable": writable,
        "sha256": hashlib.sha256("\n".join("|".join(map(str, row)) for row in rows).encode()).hexdigest(),
    }

def registry_facts():
    result = {}
    for rel in (".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"):
        path = profile / rel
        result[rel] = {"exists": path.exists(), "mode": stat.S_IMODE(path.stat().st_mode) if path.exists() else None, "sha256": sha(path) if path.is_file() else None}
    return result

head = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], check=True, capture_output=True, text=True).stdout.strip()
if head != "c36ca8c94b695b0e25b7d42c89f194661f187423":
    parent = subprocess.run(["git", "rev-parse", "HEAD^1"], check=True, capture_output=True, text=True).stdout.strip()
    parent_tree = subprocess.run(["git", "rev-parse", "HEAD^1^{tree}"], check=True, capture_output=True, text=True).stdout.strip()
    assert parent == "c36ca8c94b695b0e25b7d42c89f194661f187423" and parent_tree == "50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92"
else:
    assert tree == "50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92"
assert child == Path("/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e")
assert runtime == Path("/home/user/work/wt/rt-pin-8ea0766f")
assert profile == Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110")
assert schema.is_dir() and node.is_file() and os.access(node, os.X_OK)
assert os.environ.get("PYTHONNOUSERSITE") is None
for name in ("ASTRID_NORMAL_RUNTIME_SOURCE", "ASTRID_PARENT_MEDIA_SEED_RUNTIME", "ASTRID_WORD_ANCHOR_SEED_RUNTIME", "ASTRID_RUNTIME_SOURCE_MANIFEST"):
    assert name not in os.environ, name
assert subprocess.run([str(node), "--version"], check=True, capture_output=True, text=True).stdout.strip() == "v20.19.4"

with gzip.open(os.environ["OUTCOMES"], "rt") as stream:
    rows = [json.loads(line) for line in stream]
failed = [row for row in rows if row["outcome"] == "failed"]
assert len(failed) == len({row["nodeid"] for row in failed}) == 267
selected = [row for row in failed if row["nodeid"].split("::", 1)[0] in counts]
selected_ids = sorted(row["nodeid"] for row in selected)
assert len(selected_ids) == 86
assert {path: sum(nodeid.startswith(path + "::") for nodeid in selected_ids) for path in counts} == counts
assert not any("test_d09_managed_scene_only.py" in nodeid for nodeid in selected_ids)
expected.write_text("\n".join(selected_ids) + "\n")

source_hashes = {rel: sha(root / rel) for rel in source_files}
body = {}
for rel in source_files:
    names = {nodeid.split("::", 1)[1].split("[", 1)[0] for nodeid in selected_ids if nodeid.startswith(rel + "::")}
    body[rel] = body_hashes(root / rel, names)
index = json.loads(Path(os.environ["INDEX"]).read_text())
entry = index["entries"][child.name]
assert entry["identity"]["agent_sha"] == "c36ca8c94b695b0e25b7d42c89f194661f187423"
assert entry["identity"]["backend_sha"] == "abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e"
assert set(entry["identity"]["client_tuple"]) == {
    "packages/python/astrid_runtime_client/__init__.py",
    "packages/python/astrid_runtime_client/contract_metadata.py",
    "packages/python/astrid_runtime_client/generated.py",
    "packages/python/astrid_runtime_client/timeline_commit_types.py",
}
lock = profile / "package-lock.json"
archive = profile / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
assert sha(lock) == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"
assert sha(archive) == "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
assert json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"] == "0.0.14"
out.write_text(json.dumps({
    "status": "passed",
    "source": {"agent_sha": "c36ca8c94b695b0e25b7d42c89f194661f187423", "agent_tree": "50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92", "runtime_sha": "abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e", "runtime_tree": "6047ac3033c3594b8f83db3afd8bb2c47cafa6d6", "source_hashes": source_hashes, "body_hashes": body},
    "inventory": {"archive": os.environ["OUTCOMES"], "archive_sha256": sha(Path(os.environ["OUTCOMES"])), "failed_original_nodes": 267, "selected_nodes": 86, "counts_by_file": counts, "selected_nodeids": selected_ids, "owners": {nodeid: owners.get(nodeid.split("::", 1)[0], "Agent execution/host + Runtime OPS") for nodeid in selected_ids}},
    "environment": {"mode": "installed", "child": str(child), "child_site": str(child / "lib/python3.13/site-packages"), "runtime": str(runtime), "profile": str(profile), "node": str(node), "node_version": "v20.19.4", "schema_path": str(schema), "parent_pythonpath": os.environ["PYTHONPATH"], "PYTHONNOUSERSITE": None, "PYTEST_PLUGINS": None, "unsupported_variables_absent": True},
    "profile": {"package_lock_sha256": sha(lock), "composition_archive_sha256": sha(archive), "composition_version": "0.0.14", "inventory": profile_facts(), "registry": registry_facts()},
    "bench_store": {"index": os.environ["INDEX"], "entry": entry, "registration": index["registrations"]["venv-agent-child-f-post-g5-c36-abd47-store"]},
}, indent=2, sort_keys=True) + "\n")
print("selected 86 nodes from actual 267-failure inventory")
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
import json, os, sys
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
print(json.dumps({"origins": {"astrid": str(Path(astrid.__file__).resolve()), "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()), "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()), "schema": str(Path(schema.__file__).resolve()), "shared_schema": str(Path(shared_schema.__file__).resolve())}, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE"), "sys_path": sys.path}, sort_keys=True))
PY

EXPECTED="$EVIDENCE/expected-nodeids.txt"
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
assert actual == expected and len(actual) == 86, {"actual": len(actual), "expected": len(expected)}
print(f"exact collect: {len(actual)} nodeids")
PY

set +e
timeout 1500 "$PYTHON" -P - "$EXPECTED" "$EVIDENCE/junit.xml" > "$EVIDENCE/pytest.log" 2>&1 <<'PY'
import sys
from pathlib import Path
import pytest
raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", f"--junitxml={sys.argv[2]}", *Path(sys.argv[1]).read_text().splitlines()]))
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
print(json.dumps({"python": sys.executable, "site": str(site), "origins": {name: str(path) for name, path in modules.items()}, "metadata": metadata, "PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE"), "sys_path": sys.path}, sort_keys=True))
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
import hashlib, json, os, stat, sys
from pathlib import Path
before = json.loads(Path(sys.argv[1]).read_text())
profile = Path(os.environ["PROFILE"])
rows, writable = [], []
for path in sorted(profile.rglob("*")):
    rel, mode = path.relative_to(profile).as_posix(), stat.S_IMODE(path.lstat().st_mode)
    kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
    if kind != "link" and mode & 0o222:
        writable.append(rel)
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if kind == "file" else ""
    rows.append((rel, kind, mode, path.stat().st_size if kind == "file" else 0, digest))
inventory = {"count": len(rows), "writable": writable, "sha256": hashlib.sha256("\n".join("|".join(map(str, row)) for row in rows).encode()).hexdigest()}
registry = {}
for rel in (".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"):
    path = profile / rel
    registry[rel] = {"exists": path.exists(), "mode": stat.S_IMODE(path.stat().st_mode) if path.exists() else None, "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None}
after = {"source": before["source"], "inventory": before["inventory"], "environment": before["environment"], "profile": before["profile"], "post_profile_inventory": inventory, "post_registry": registry}
assert inventory == before["profile"]["inventory"]
assert writable == before["profile"]["inventory"]["writable"]
Path(sys.argv[2]).write_text(json.dumps(after, indent=2, sort_keys=True) + "\n")
PY
python3 - "$EVIDENCE/junit.xml" "$EVIDENCE/outcome-map.json" <<'PY'
import json, sys
import xml.etree.ElementTree as ET
from pathlib import Path
cases = []
for case in ET.parse(sys.argv[1]).getroot().iter("testcase"):
    result, detail = "passed", ""
    child = next(iter(case), None)
    if child is not None:
        result = {"failure": "failed", "error": "error", "skipped": "skipped"}.get(child.tag, child.tag)
        detail = child.text or ""
    cases.append({"source": case.get("classname"), "name": case.get("name"), "time": case.get("time"), "outcome": result, "longrepr": detail})
Path(sys.argv[2]).write_text(json.dumps({"selected": 86, "junit_cases": len(cases), "cases": cases}, indent=2, sort_keys=True) + "\n")
PY
printf 'pytest_exit=%s\ncollect_exit=0\nselected=86\n' "$test_status" > "$EVIDENCE/result.txt"
exit "$test_status"
