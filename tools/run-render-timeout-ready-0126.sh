#!/usr/bin/env bash
set -euo pipefail

# F-render-21: one-node, current-source qualification runner.  This script
# deliberately refuses to run the original node until a current immutable
# child supplied by the manager has passed the admission checks below.
MODE=${1:-preflight}
case "$MODE" in
  preflight|run) ;;
  *) echo "usage: $0 [preflight|run]" >&2; exit 2 ;;
esac

ROOT=$(pwd -P)
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE_BIN=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin
NODE=$NODE_BIN/node
PARENT_PYTHON=/home/user/work/venv-agent/bin/python
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
CHILD=${ASTRID_RENDER_CHILD_VENV:-}
EVIDENCE=$(mktemp -d "${TMPDIR:-/tmp}/render-timeout-ready-0126.XXXXXX")

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT:$RUNTIME"
export PATH="$NODE_BIN:/usr/bin:/bin"
export ASTRID_HOST_EXECUTION_PROFILE=source
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset PYTEST_PLUGINS PYTEST_ADDOPTS PYTHONNOUSERSITE

export F_RENDER_EVIDENCE="$EVIDENCE"
export F_RENDER_ROOT="$ROOT"
export F_RENDER_RUNTIME="$RUNTIME"
export F_RENDER_PROFILE="$PROFILE"
export F_RENDER_NODE="$NODE"
export F_RENDER_NODE_BIN="$NODE_BIN"
export F_RENDER_SCHEMA="$SCHEMA"
export F_RENDER_CHILD="$CHILD"

"$PARENT_PYTHON" -P - <<'PY'
import ast
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(os.environ["F_RENDER_ROOT"])
runtime = Path(os.environ["F_RENDER_RUNTIME"])
profile = Path(os.environ["F_RENDER_PROFILE"])
evidence = Path(os.environ["F_RENDER_EVIDENCE"])
node = Path(os.environ["F_RENDER_NODE"])
node_bin = Path(os.environ["F_RENDER_NODE_BIN"])
schema = Path(os.environ["F_RENDER_SCHEMA"])
child = os.environ.get("F_RENDER_CHILD")

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git(cwd, *args):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()

def facts(cwd):
    return {"head": git(cwd, "rev-parse", "HEAD"), "tree": git(cwd, "rev-parse", "HEAD^{tree}"), "status": git(cwd, "status", "--porcelain", "--untracked-files=all")}

def result(ok, value=None, error=None):
    row = {"ok": ok}
    if value is not None:
        row["value"] = value
    if error is not None:
        row["error"] = error
    return row

report = {
    "runner": "tools/run-render-timeout-ready-0126.sh",
    "mode": os.environ.get("ASTRID_HOST_EXECUTION_PROFILE"),
    "evidence": str(evidence),
    "source": {},
    "environment": {},
    "admission": {},
}

validator = root / "astrid/core/timeline/validators/timeline.py"
target = root / "tests/packs/rendering/test_threejs_backend.py"
tree = ast.parse(target.read_text(), filename=str(target))
target_node = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons")
report["source"].update({
    "agent": facts(root),
    "runtime": facts(runtime),
    "validator": {"path": str(validator), "sha256": digest(validator), "blob": git(root, "hash-object", str(validator))},
    "target_file_sha256": digest(target),
    "target_function_ast_sha256": hashlib.sha256(ast.dump(target_node, include_attributes=False).encode()).hexdigest(),
})
report["environment"].update({
    "python": sys.executable,
    "python_version": sys.version,
    "runtime_checkout": str(runtime),
    "runtime_source_root": os.environ.get("ASTRID_RUNTIME_SOURCE_ROOT"),
    "profile": str(profile),
    "node": str(node),
    "node_version": subprocess.check_output([str(node), "--version"], text=True).strip(),
    "npx": str(node_bin / "npx"),
    "npx_version": subprocess.check_output([str(node_bin / "npx"), "--version"], text=True).strip(),
    "schema": str(schema),
    "pythonpath": os.environ.get("PYTHONPATH"),
})
report["profile"] = {
    "package_lock_sha256": digest(profile / "package-lock.json"),
    "composition_archive_sha256": digest(profile / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"),
    "composition_version": json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"],
    "registry_state_sha256": digest(profile / ".astrid-registry-state.json"),
    "transitions_generated_sha256": digest(profile / "src/transitions.generated.ts"),
}

def origin(name):
    spec = importlib.util.find_spec(name)
    return None if spec is None else str(Path(spec.origin).resolve())

report["admission"]["parent_origins"] = {
    name: origin(name) for name in ("astrid", "astrid.core.timeline.validators.timeline", "runtime_protocol", "astrid_runtime_client", "banodoco_timeline_schema")
}
report["admission"]["parent_origins_expected"] = {
    "astrid": str(root / "astrid/__init__.py"),
    "astrid.core.timeline.validators.timeline": str(validator),
    "runtime_protocol": str(runtime / "runtime_protocol/__init__.py"),
    "astrid_runtime_client": str(root / "astrid_runtime_client/__init__.py"),
    "banodoco_timeline_schema": str(schema / "banodoco_timeline_schema/__init__.py"),
}
report["admission"]["source_profile_selectors"] = {
    name: os.environ.get(name) for name in ("ASTRID_HOST_EXECUTION_PROFILE", "ASTRID_RUNTIME_CHECKOUT", "ASTRID_RUNTIME_SOURCE_ROOT", "ASTRID_REMOTION_PROJECT_DIR")
}

if child:
    child_python = Path(child) / "bin/python"
    report["child"] = {"path": child, "python": str(child_python), "exists": child_python.is_file()}
    if child_python.is_file():
        probe = subprocess.run([str(child_python), "-I", "-B", "-c", """
import hashlib, importlib.util, json
from pathlib import Path
import astrid.core.timeline.validators.timeline as validator
import runtime_protocol
path = Path(validator.__file__).resolve()
print(json.dumps({"validator": str(path), "validator_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "runtime_protocol": str(Path(runtime_protocol.__file__).resolve())}))
"""], text=True, capture_output=True)
        report["child"]["probe_exit"] = probe.returncode
        report["child"]["probe_stdout"] = probe.stdout.strip()
        report["child"]["probe_stderr"] = probe.stderr.strip()
        if probe.returncode == 0:
            try:
                child_facts = json.loads(probe.stdout)
                report["child"]["current_validator"] = child_facts["validator_sha256"] == report["source"]["validator"]["sha256"]
                report["child"]["runtime_protocol_origin"] = child_facts["runtime_protocol"]
            except (KeyError, json.JSONDecodeError):
                report["child"]["current_validator"] = False
else:
    report["child"] = {"supplied": False, "reason": "manager has not supplied a current immutable child"}

report["finite_suite"] = {
    "nodeids": ["tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"],
    "timeout_seconds": 45,
    "pytest": ["-q", "-o", "addopts=", "-p", "no:cacheprovider"],
    "body_sha256": report["source"]["target_function_ast_sha256"],
}
(evidence / "preflight.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(json.dumps(report, indent=2, sort_keys=True))
PY

set +e
"$PARENT_PYTHON" -P - <<'PY' > "$EVIDENCE/source-profile-support.txt" 2>&1
from astrid.sdk.rendering import support

try:
    support("rendering.threejs", timeline_path="tests/editing_scenarios/fixtures/empty.json")
except Exception as exc:
    print(type(exc).__name__)
    print(getattr(exc, "error", exc))
    raise SystemExit(1)
PY
source_status=$?
set -e
printf 'source_profile_support_exit=%s\n' "$source_status" > "$EVIDENCE/source-profile-support.result"

if [ "$MODE" = preflight ]; then
  if [ -n "$CHILD" ] && grep -q '"current_validator": true' "$EVIDENCE/preflight.json"; then
    echo "preflight passed: current child admitted; evidence=$EVIDENCE"
    exit 0
  fi
  echo "preflight blocked: no current immutable child admitted; evidence=$EVIDENCE" >&2
  exit 1
fi

if [ -z "$CHILD" ] || ! grep -q '"current_validator": true' "$EVIDENCE/preflight.json"; then
  echo "refusing original node: run preflight with a manager-supplied current child first" >&2
  exit 1
fi

set +e
timeout 45 "$PARENT_PYTHON" -P -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons \
  >"$EVIDENCE/pytest.log" 2>&1
status=$?
set -e
printf 'pytest_exit=%s\n' "$status" > "$EVIDENCE/result.txt"
cat "$EVIDENCE/result.txt"
exit "$status"
