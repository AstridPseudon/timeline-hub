#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-run}
ROOT=$(git rev-parse --show-toplevel)
CHILD=/home/user/work/bench-store/entries/child-3b5cb98c4f2dfc20ce8747f68bf2e1124ff47b9dd5f04dabaada3a22278fdfc9
RUNTIME=/home/user/work/wt/rt-pin-f3208b26
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE_BIN=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin
SCHEMA_SITE=/home/user/work/venv-agent/lib/python3.13/site-packages
WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-timeout-qualify-0509
EVIDENCE=$WORKER/evidence
TMPDIR=${TMPDIR:-$WORKER/tmpdir}
IMPORT_SHIM=$TMPDIR/import-shim
TARGET=tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons

mkdir -p "$EVIDENCE" "$TMPDIR"
export ROOT CHILD RUNTIME PROFILE NODE_BIN SCHEMA_SITE EVIDENCE TMPDIR IMPORT_SHIM TARGET

env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  NODE_BIN="$NODE_BIN" \
  PATH="$CHILD/bin:$NODE_BIN:/usr/bin:/bin" \
  "$CHILD/bin/python" -I -B - "$ROOT" "$CHILD" "$RUNTIME" "$PROFILE" "$EVIDENCE" "$TARGET" <<'PY'
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

root, child, runtime, profile, evidence, target = map(Path, sys.argv[1:])
site = child / "lib/python3.13/site-packages"
receipt = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-d40-ba8f-f320.txt")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def status(path: Path) -> list[str]:
    return [line for line in git("status", "--porcelain", cwd=path).splitlines() if line]


def body_facts(path: Path) -> dict[str, object]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node for node in ast.walk(module)
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"
    )
    body_dump = ast.dump(function, annotate_fields=True, include_attributes=False)
    assertions = [node for node in ast.walk(function) if isinstance(node, ast.Assert)]
    assertion_dump = ast.dump(
        ast.Module(body=assertions, type_ignores=[]),
        annotate_fields=True,
        include_attributes=False,
    )
    return {
        "file_sha256": sha(path),
        "function_ast_sha256": hashlib.sha256(body_dump.encode()).hexdigest(),
        "assertions_ast_sha256": hashlib.sha256(assertion_dump.encode()).hexdigest(),
        "assertion_count": len(assertions),
        "line_start": function.lineno,
        "line_end": function.end_lineno,
    }


test_path = root / "tests/packs/rendering/test_threejs_backend.py"
before_body = body_facts(test_path)
origin_names = [
    "astrid",
    "astrid.sdk.rendering",
    "astrid.core.rendering.registry",
    "astrid.core.rendering.transport",
    "astrid.packs.rendering.rendering.renderers.threejs.run",
    "astrid_runtime_client",
    "runtime_protocol",
]
probe = subprocess.run(
    [str(child / "bin/python"), "-I", "-B", "-c", """
import importlib.util, json, sys
names = %r
print(json.dumps({
    "executable": sys.executable,
    "prefix": sys.prefix,
    "path": sys.path,
    "origins": {name: (str(importlib.util.find_spec(name).origin) if importlib.util.find_spec(name) else None) for name in names},
}))
""" % origin_names],
    cwd=str(root), capture_output=True, text=True, check=False,
)
if probe.returncode:
    raise SystemExit(f"isolated installed-origin probe failed: {probe.stderr}")
child_facts = json.loads(probe.stdout)
origins = child_facts["origins"]
expected_site = str(site)
if any(not value or not value.startswith(expected_site + "/") for value in origins.values()):
    raise SystemExit(f"installed-origin probe escaped site-packages: {origins}")

relevant = [
    "astrid/sdk/rendering.py",
    "astrid/core/rendering/transport.py",
    "astrid/core/rendering/registry.py",
    "astrid/packs/rendering/rendering/renderers/threejs/run.py",
    "astrid/packs/rendering/rendering/renderers/threejs/renderer.yaml",
]
source_installed = {}
for rel in relevant:
    source = root / rel
    installed = site / rel
    source_installed[rel] = {
        "source": str(source),
        "source_sha256": sha(source),
        "installed": str(installed),
        "installed_sha256": sha(installed),
        "byte_equal": source.read_bytes() == installed.read_bytes(),
    }
if not all(item["byte_equal"] for item in source_installed.values()):
    raise SystemExit(f"source/installed rendering bytes differ: {source_installed}")

source_manifest = root / "astrid/packs/rendering/rendering/renderers/threejs/renderer.yaml"
manifest = site / "astrid/packs/rendering/rendering/renderers/threejs/renderer.yaml"
contract = runtime / "contract/commit-v2.md"
profile_archive = profile / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
node = Path(os.environ["NODE_BIN"]) / "node"
ba8_test = subprocess.check_output(
    ["git", "show", "ba8f0bc8be:tests/packs/rendering/test_threejs_backend.py"], cwd=root
)
ba8_body = body_facts_from_ba8 = next(
    node for node in ast.walk(ast.parse(ba8_test.decode()))
    if isinstance(node, ast.FunctionDef)
    and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"
)
ba8_body_hash = hashlib.sha256(
    ast.dump(ba8_body, annotate_fields=True, include_attributes=False).encode()
).hexdigest()

preflight = {
    "status": "passed",
    "mode": "preflight",
    "host": {
        "root": str(root),
        "commit": git("rev-parse", "HEAD", cwd=root),
        "tree": git("rev-parse", "HEAD^{tree}", cwd=root),
        "status": status(root),
    },
    "installed_child": {
        "path": str(child),
        "python": str(child / "bin/python"),
        "site_packages": str(site),
        "recorded_source_commit": (child / ".astrid-source-commit").read_text().strip(),
        "recorded_runtime_commit": (child / ".astrid-runtime-source-commit").read_text().strip(),
        "isolated_executable": child_facts["executable"],
        "isolated_prefix": child_facts["prefix"],
        "isolated_sys_path": child_facts["path"],
        "import_origins": origins,
        "actual_installed_site_packages": True,
        "source_as_installed_via_pythonpath": False,
    },
    "receipt": {"path": str(receipt), "sha256": sha(receipt), "text": receipt.read_text(encoding="utf-8")},
    "runtime": {
        "checkout": str(runtime),
        "commit": git("rev-parse", "HEAD", cwd=runtime),
        "tree": git("rev-parse", "HEAD^{tree}", cwd=runtime),
        "status": status(runtime),
        "contract_sha256": sha(contract),
    },
    "source_vs_installed": source_installed,
    "package": {
        "manifest_source_sha256": sha(source_manifest),
        "manifest_installed_sha256": sha(manifest),
        "astrid_distribution_metadata_sha256": sha(child / ".astrid-distribution-metadata"),
    },
    "profile": {
        "path": str(profile),
        "package_lock_sha256": sha(profile / "package-lock.json"),
        "composition_archive_sha256": sha(profile_archive),
        "node": str(node),
        "node_version": subprocess.check_output([str(node), "--version"], text=True).strip(),
        "node_modules": str(profile / "node_modules"),
    },
    "original_test": {
        "nodeid": str(target),
        "body_before": before_body,
        "body_ba8": {"function_ast_sha256": ba8_body_hash},
        "body_matches_ba8": before_body["function_ast_sha256"] == ba8_body_hash,
    },
    "production_caller": {
        "entry": "astrid.sdk.rendering.support",
        "dispatch": "support -> _support_report -> CommandTransport.run",
        "candidate": "load_default_registries -> rendering.threejs",
        "command": ["python3", "rendering/renderers/threejs/run.py", "support", "--request", "<tmp>/support-request.json", "--result", "<tmp>/support-result.json"],
        "pack_root_origin": origins["astrid.packs.rendering.rendering.renderers.threejs.run"],
        "result_parsed_before_return": True,
        "support_is_read_only": True,
        "before_raster_mp4_browser": True,
    },
    "scope": {
        "exactly_one_body": True,
        "no_whole_module": True,
        "no_real_render": True,
        "no_browser": True,
        "no_provision_or_install": True,
        "no_source_fix": True,
        "command_transport_timeout_unchanged": 45,
    },
}
if not preflight["original_test"]["body_matches_ba8"]:
    raise SystemExit("original target body differs from installed ba8 source")
(evidence / "preflight.json").write_text(json.dumps(preflight, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "status": "passed",
    "host_commit": preflight["host"]["commit"],
    "installed_agent": preflight["installed_child"]["recorded_source_commit"],
    "installed_runtime": preflight["installed_child"]["recorded_runtime_commit"],
    "target_body": before_body,
    "body_matches_ba8": preflight["original_test"]["body_matches_ba8"],
    "import_origins": origins,
}, sort_keys=True))
PY

if [[ "$MODE" == preflight ]]; then
  exit 0
fi
if [[ "$MODE" != run ]]; then
  echo "usage: $0 [preflight|run]" >&2
  exit 2
fi

mkdir -p "$IMPORT_SHIM"
if [[ ! -e "$IMPORT_SHIM/tests" ]]; then
  ln -s "$ROOT/tests" "$IMPORT_SHIM/tests"
fi
if [[ ! -e "$IMPORT_SHIM/scripts" ]]; then
  ln -s "$ROOT/scripts" "$IMPORT_SHIM/scripts"
fi

set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  TMPDIR="$TMPDIR" PYTHONPATH="$IMPORT_SHIM" PATH="$CHILD/bin:$NODE_BIN:/usr/bin:/bin" \
  ASTRID_HOST_EXECUTION_PROFILE=installed \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME" \
  ASTRID_REMOTION_PROJECT_DIR="$PROFILE" \
  ASTRID_NODE_EXECUTABLE="$NODE_BIN/node" \
  ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules" \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA_SITE" \
  "$CHILD/bin/python" -P -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider \
  --collect-only "$TARGET" >"$EVIDENCE/collect.log" 2>&1
COLLECT_STATUS=$?
set -e
printf 'collect_exit=%s\n' "$COLLECT_STATUS" >"$EVIDENCE/collect.result"
if [[ "$COLLECT_STATUS" -ne 0 ]]; then
  exit "$COLLECT_STATUS"
fi

if [[ -e "$EVIDENCE/body-started" ]]; then
  echo "refusing a second target body execution" >&2
  exit 125
fi
printf '%s\n' "$(date -u +%FT%TZ)" >"$EVIDENCE/body-started"

set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  TMPDIR="$TMPDIR" PYTHONPATH="$IMPORT_SHIM" PATH="$CHILD/bin:$NODE_BIN:/usr/bin:/bin" \
  ASTRID_HOST_EXECUTION_PROFILE=installed \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME" \
  ASTRID_REMOTION_PROJECT_DIR="$PROFILE" \
  ASTRID_NODE_EXECUTABLE="$NODE_BIN/node" \
  ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules" \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA_SITE" \
  "$CHILD/bin/python" -P -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider \
  --timeout=45 "$TARGET" >"$EVIDENCE/pytest.log" 2>&1
TEST_STATUS=$?
set -e
printf 'pytest_exit=%s\n' "$TEST_STATUS" >"$EVIDENCE/result.txt"

env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PATH="$CHILD/bin:$NODE_BIN:/usr/bin:/bin" \
  "$CHILD/bin/python" -I -B - "$ROOT" "$EVIDENCE" <<'PY'
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root, evidence = map(Path, sys.argv[1:])
test_path = root / "tests/packs/rendering/test_threejs_backend.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body(path: Path) -> dict[str, str]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    fn = next(node for node in ast.walk(module) if isinstance(node, ast.FunctionDef)
              and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons")
    assertions = [node for node in ast.walk(fn) if isinstance(node, ast.Assert)]
    return {
        "file_sha256": sha(path),
        "function_ast_sha256": hashlib.sha256(ast.dump(fn, annotate_fields=True, include_attributes=False).encode()).hexdigest(),
        "assertions_ast_sha256": hashlib.sha256(ast.dump(ast.Module(body=assertions, type_ignores=[]), annotate_fields=True, include_attributes=False).encode()).hexdigest(),
    }


pre = json.loads((evidence / "preflight.json").read_text(encoding="utf-8"))
after_body = body(test_path)
expected_body = {key: pre["original_test"]["body_before"][key] for key in after_body}
post = {
    "status": "passed",
    "host_status": subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True).splitlines(),
    "target_body_after": after_body,
    "target_body_unchanged": after_body == expected_body,
    "runtime_status": subprocess.check_output(["git", "-C", "/home/user/work/wt/rt-pin-f3208b26", "status", "--porcelain"], text=True).splitlines(),
    "installed_child": pre["installed_child"]["path"],
}
if not post["target_body_unchanged"] or post["runtime_status"]:
    post["status"] = "failed"
(evidence / "postflight.json").write_text(json.dumps(post, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(post, sort_keys=True))
raise SystemExit(0 if post["status"] == "passed" else 1)
PY
POST_STATUS=$?

exit "$TEST_STATUS"
