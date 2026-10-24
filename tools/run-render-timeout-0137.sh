#!/usr/bin/env bash
set -euo pipefail

# F-render-21: one original support case, with the current immutable child
# admitted through the normal dispatcher receipt.  This runner only prepares
# and proves the route; the original node is behind the explicit run mode.
MODE=${1:-preflight}
case "$MODE" in
    preflight|run) ;;
    *) printf '%s\n' 'usage: run-render-timeout-0137.sh [preflight|run]' >&2; exit 2 ;;
esac

ROOT=$(pwd -P)
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE_BIN=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin
NODE=$NODE_BIN/node
PARENT_PYTHON=/home/user/work/venv-agent/bin/python
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
CHILD_NAME=venv-agent-child-render-current-0134
RECEIPT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/childvenv-venv-agent-child-render-current-0134
PROVISION_REPORT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-render-current-0134.txt
BENCH_INDEX=/home/user/work/bench-store/index.json
EVIDENCE=$(mktemp -d "${TMPDIR:-/tmp}/render-timeout-0137.XXXXXX")

: "${EXPECTED_SOURCE_TREE:?set EXPECTED_SOURCE_TREE to the finalized source snapshot tree}"
EXPECTED_RUNTIME_TREE=6047ac3033c3594b8f83db3afd8bb2c47cafa6d6
EXPECTED_AGENT_SHA=521c88802330901281cc37ba25818baf2575f05e
EXPECTED_RUNTIME_SHA=8ea0766f5e9fb23cea26c7398770a8aaac06b258
EXPECTED_VALIDATOR_SHA=361f759eefeb133634d6b70af320fcb13bd1ad0fa33597860f1c6158696f9686
EXPECTED_TARGET_SHA=9efe493cb2f8339177e07616b976afe6f9813ae4d415923ff25701b471e991c7
EXPECTED_BODY_SHA=ca54f2d5059bb3b5cca1e8ee43156df6762d3a86739caa2aa18ffcb83f3ded82
EXPECTED_PROFILE_LOCK_SHA=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
EXPECTED_PROFILE_ARCHIVE_SHA=819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
EXPECTED_REGISTRY_STATE_SHA=d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96
EXPECTED_REGISTRY_ANIMATIONS_SHA=02326f12177879eb5905f9d9b6d476b2de185928ddeeeeb2321a68ebffb47ad6
EXPECTED_REGISTRY_EFFECTS_SHA=127e5653e0c66993726f8334b9f4ac122d24cdfbaa9e70cdaa142189afcf2bbe
EXPECTED_REGISTRY_TRANSITIONS_SHA=c46d6bbd88712e775812867ec1cbe6de67473664775266c5a0b9317344ceb989
EXPECTED_REQUIREMENTS_SHA=236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778
EXPECTED_PROVISION_REPORT_SHA=c087ef4d9ce8fa0bbeb8eceb255f120c09d8c252440eb24fdec735f0482117d7
EXPECTED_OLD_AGENT_SHA=c36ca8c94b695b0e25b7d42c89f194661f187423
EXPECTED_OLD_VALIDATOR_SHA=90644ccc8565be9c733dec452229cf7538c574b2d051625fb21392572745b785

export F_RENDER_ROOT="$ROOT" F_RENDER_RUNTIME="$RUNTIME" F_RENDER_PROFILE="$PROFILE"
export F_RENDER_NODE="$NODE" F_RENDER_NODE_BIN="$NODE_BIN" F_RENDER_SCHEMA="$SCHEMA"
export F_RENDER_CHILD_NAME="$CHILD_NAME" F_RENDER_RECEIPT="$RECEIPT"
export F_RENDER_PROVISION_REPORT="$PROVISION_REPORT" F_RENDER_BENCH_INDEX="$BENCH_INDEX"
export F_RENDER_EVIDENCE="$EVIDENCE"
export F_EXPECTED_SOURCE_TREE="$EXPECTED_SOURCE_TREE" F_EXPECTED_RUNTIME_TREE="$EXPECTED_RUNTIME_TREE"
export F_EXPECTED_AGENT_SHA="$EXPECTED_AGENT_SHA" F_EXPECTED_RUNTIME_SHA="$EXPECTED_RUNTIME_SHA"
export F_EXPECTED_VALIDATOR_SHA="$EXPECTED_VALIDATOR_SHA" F_EXPECTED_TARGET_SHA="$EXPECTED_TARGET_SHA"
export F_EXPECTED_BODY_SHA="$EXPECTED_BODY_SHA" F_EXPECTED_REQUIREMENTS_SHA="$EXPECTED_REQUIREMENTS_SHA"
export F_EXPECTED_PROVISION_REPORT_SHA="$EXPECTED_PROVISION_REPORT_SHA"
export F_EXPECTED_PROFILE_LOCK_SHA="$EXPECTED_PROFILE_LOCK_SHA"
export F_EXPECTED_PROFILE_ARCHIVE_SHA="$EXPECTED_PROFILE_ARCHIVE_SHA"
export F_EXPECTED_REGISTRY_STATE_SHA="$EXPECTED_REGISTRY_STATE_SHA"
export F_EXPECTED_REGISTRY_ANIMATIONS_SHA="$EXPECTED_REGISTRY_ANIMATIONS_SHA"
export F_EXPECTED_REGISTRY_EFFECTS_SHA="$EXPECTED_REGISTRY_EFFECTS_SHA"
export F_EXPECTED_REGISTRY_TRANSITIONS_SHA="$EXPECTED_REGISTRY_TRANSITIONS_SHA"
export F_EXPECTED_OLD_AGENT_SHA="$EXPECTED_OLD_AGENT_SHA" F_EXPECTED_OLD_VALIDATOR_SHA="$EXPECTED_OLD_VALIDATOR_SHA"

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT:$RUNTIME"
export PATH="$NODE_BIN:/home/user/work/venv-agent/bin:/usr/bin:/bin"
export ASTRID_HOST_EXECUTION_PROFILE=source
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset PYTEST_PLUGINS PYTEST_ADDOPTS PYTHONNOUSERSITE

set +e
"$PARENT_PYTHON" -P - "$EVIDENCE/preflight.json" "$EVIDENCE/child.path" <<'PY'
import ast
import hashlib
import importlib
import importlib.metadata
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

out_path, child_path_out = map(Path, sys.argv[1:])
root = Path(os.environ["F_RENDER_ROOT"]).resolve()
runtime = Path(os.environ["F_RENDER_RUNTIME"]).resolve()
profile = Path(os.environ["F_RENDER_PROFILE"]).resolve()
node = Path(os.environ["F_RENDER_NODE"]).resolve()
schema = Path(os.environ["F_RENDER_SCHEMA"]).resolve()
receipt_path = Path(os.environ["F_RENDER_RECEIPT"])
provision_path = Path(os.environ["F_RENDER_PROVISION_REPORT"])
index_path = Path(os.environ["F_RENDER_BENCH_INDEX"])
evidence = Path(os.environ["F_RENDER_EVIDENCE"])
expected = {name.removeprefix("F_"): value for name, value in os.environ.items() if name.startswith("F_EXPECTED_")}
failures = []
checks = []
child = None

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(*args: str, cwd: Path = root) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()

def git_status(cwd: Path) -> list[str]:
    return [line for line in subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=cwd,
        text=True,
    ).splitlines() if line]

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

def source_identity():
    tree = git("rev-parse", "HEAD^{tree}")
    changed = [line[3:] if len(line) >= 3 else line for line in git_status(root)]
    assert tree == expected["EXPECTED_SOURCE_TREE"], {"tree": tree, "expected": expected["EXPECTED_SOURCE_TREE"]}
    assert set(changed) <= {"tools/run-render-timeout-0137.sh"}, changed
    return {"head": git("rev-parse", "HEAD"), "tree": tree, "expected_tree": expected["EXPECTED_SOURCE_TREE"], "changed": changed}

def runtime_identity():
    assert git("rev-parse", "HEAD", cwd=runtime) == expected["EXPECTED_RUNTIME_SHA"]
    assert git("rev-parse", "HEAD^{tree}", cwd=runtime) == expected["EXPECTED_RUNTIME_TREE"]
    assert not git_status(runtime)
    return {"head": git("rev-parse", "HEAD", cwd=runtime), "tree": git("rev-parse", "HEAD^{tree}", cwd=runtime), "status": "clean"}

def target_identity():
    target = root / "tests/packs/rendering/test_threejs_backend.py"
    validator = root / "astrid/core/timeline/validators/timeline.py"
    tree = ast.parse(target.read_text(), filename=str(target))
    body = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons")
    target_sha = digest(target)
    body_sha = hashlib.sha256(ast.dump(body, include_attributes=False).encode()).hexdigest()
    assert target_sha == expected["EXPECTED_TARGET_SHA"], target_sha
    assert body_sha == expected["EXPECTED_BODY_SHA"], body_sha
    assert digest(validator) == expected["EXPECTED_VALIDATOR_SHA"], digest(validator)
    return {"target": str(target), "target_sha256": target_sha, "body_ast_sha256": body_sha, "validator_sha256": digest(validator), "validator": str(validator)}

def receipt_and_bench_lookup():
    global child
    text = receipt_path.read_text()
    assert "status=passed" in text, receipt_path
    assert f"requested_name={os.environ['F_RENDER_CHILD_NAME']}" in text, text
    assert f"agent={expected['EXPECTED_AGENT_SHA']}" in text, text
    assert f"runtime={expected['EXPECTED_RUNTIME_SHA']}" in text, text
    assert f"lock_sha256={expected['EXPECTED_REQUIREMENTS_SHA']}" in text, text
    assert provision_path.is_file()
    assert digest(provision_path) == expected["EXPECTED_PROVISION_REPORT_SHA"]
    provision = provision_path.read_text()
    assert "status=passed" in provision
    assert f"agent_sha={expected['EXPECTED_AGENT_SHA']}" in provision
    assert f"runtime_sha={expected['EXPECTED_RUNTIME_SHA']}" in provision
    assert f"requirements_lock_sha256={expected['EXPECTED_REQUIREMENTS_SHA']}" in provision
    index = json.loads(index_path.read_text())
    registration = index["registrations"][os.environ["F_RENDER_CHILD_NAME"]]
    assert registration["report_sha256"] == expected["EXPECTED_PROVISION_REPORT_SHA"]
    entries = [
        entry for entry in index["entries"].values()
        if entry.get("component") == "child"
        and entry.get("identity", {}).get("agent_sha") == expected["EXPECTED_AGENT_SHA"]
        and entry.get("identity", {}).get("backend_sha") == expected["EXPECTED_RUNTIME_SHA"]
    ]
    assert len(entries) == 1, entries
    entry = entries[0]
    child = Path(entry["path"]).resolve()
    assert child.is_dir() and not child.is_symlink()
    assert child.name == f"child-{entry['key']}"
    assert child.parent == Path("/home/user/work/bench-store/entries")
    assert (child / "bin/python").is_file() and os.access(child / "bin/python", os.X_OK)
    child_path_out.write_text(str(child) + "\n")
    return {"requested_name": os.environ["F_RENDER_CHILD_NAME"], "entry_key": entry["key"], "path": str(child), "identity": entry["identity"], "registration": {"hash": registration["hash"], "report_sha256": registration["report_sha256"]}}

def child_probe():
    assert child is not None
    child_python = child / "bin/python"
    code = r'''
import hashlib, importlib, importlib.metadata, json, sys
from pathlib import Path
from urllib.parse import unquote, urlparse
import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol
import astrid.core.timeline.validators.timeline as validator

def origin(module):
    return str(Path(module.__file__).resolve())

def direct_url(name):
    raw = importlib.metadata.distribution(name).read_text("direct_url.json")
    return json.loads(raw) if raw else None

validator_path = Path(validator.__file__).resolve()
print(json.dumps({
    "executable": str(Path(sys.executable).resolve()),
    "prefix": str(Path(sys.prefix).resolve()),
    "version": list(sys.version_info[:3]),
    "origins": {
        "astrid": origin(astrid),
        "astrid_runtime": origin(astrid_runtime),
        "astrid_runtime_client": origin(astrid_runtime_client),
        "runtime_protocol": origin(runtime_protocol),
        "validator": str(validator_path),
    },
    "validator_sha256": hashlib.sha256(validator_path.read_bytes()).hexdigest(),
    "direct_urls": {"astrid": direct_url("astrid"), "astrid-runtime": direct_url("astrid-runtime")},
}))
'''
    child_env = {"HOME": "/root", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"}
    result = subprocess.run([str(child_python), "-I", "-B", "-c", code], env=child_env, capture_output=True, text=True, check=False)
    assert result.returncode == 0, {"stdout": result.stdout, "stderr": result.stderr}
    facts = json.loads(result.stdout)
    site = child / "lib/python3.13/site-packages"
    assert facts["executable"] == str(child_python.resolve())
    assert facts["version"] == [3, 13, 16]
    for name, origin in facts["origins"].items():
        assert Path(origin).is_file() and Path(origin).resolve().is_relative_to(site), (name, origin)
    assert facts["validator_sha256"] == expected["EXPECTED_VALIDATOR_SHA"]
    assert facts["origins"]["validator"].endswith("astrid/core/timeline/validators/timeline.py")
    direct_paths = {}
    for name, raw in facts["direct_urls"].items():
        assert raw and raw.get("url", "").startswith("file://"), (name, raw)
        path = Path(unquote(urlparse(raw["url"]).path)).resolve()
        assert path.is_dir() and path.is_relative_to(child), (name, path)
        direct_paths[name] = str(path)
        source_validator = path / "astrid/core/timeline/validators/timeline.py" if name == "astrid" else path / "runtime_protocol/__init__.py"
        assert source_validator.is_file()
        if name == "astrid":
            assert digest(source_validator) == expected["EXPECTED_VALIDATOR_SHA"]
    return {"probe": facts, "site": str(site), "direct_source_paths": direct_paths}

def old_child_red_source():
    old = Path("/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e")
    old_validator = old / "lib/python3.13/site-packages/astrid/core/timeline/validators/timeline.py"
    assert digest(old_validator) == expected["EXPECTED_OLD_VALIDATOR_SHA"]
    return {"path": str(old), "agent_sha": expected["EXPECTED_OLD_AGENT_SHA"], "validator_sha256": digest(old_validator), "status": "stale-red-source"}

def parent_origins():
    import astrid
    import astrid_runtime_client
    import runtime_protocol
    import astrid.core.timeline.banodoco_schema as schema_module
    import banodoco_timeline_schema as shared_schema
    actual = {
        "python": str(Path(sys.executable).resolve()),
        "astrid": str(Path(astrid.__file__).resolve()),
        "validator": str(Path(importlib.import_module("astrid.core.timeline.validators.timeline").__file__).resolve()),
        "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
        "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
        "banodoco_schema": str(Path(schema_module.__file__).resolve()),
        "shared_schema": str(Path(shared_schema.__file__).resolve()),
    }
    assert actual["astrid"] == str(root / "astrid/__init__.py")
    assert actual["validator"] == str(root / "astrid/core/timeline/validators/timeline.py")
    assert actual["astrid_runtime_client"] == str(root / "astrid_runtime_client/__init__.py")
    assert actual["runtime_protocol"] == str(runtime / "runtime_protocol/__init__.py")
    assert actual["banodoco_schema"] == str(root / "astrid/core/timeline/banodoco_schema.py")
    assert actual["shared_schema"] == str(schema / "banodoco_timeline_schema/__init__.py")
    return actual

def profile_custody():
    assert profile.is_dir()
    writable = []
    external_links = []
    entries = 0
    for path in sorted(profile.rglob("*")):
        entries += 1
        if path.is_symlink():
            if not path.resolve().is_relative_to(profile):
                external_links.append(path.relative_to(profile).as_posix())
        elif path.is_file() and stat.S_IMODE(path.stat().st_mode) & 0o222:
            relative = path.relative_to(profile).as_posix()
            if relative not in {".astrid-registry-state.json", "src/animations.generated.ts", "src/effects.generated.ts", "src/transitions.generated.ts"}:
                writable.append(relative)
    assert not writable, writable
    assert not external_links, external_links
    fixed = {
        "package-lock.json": expected["EXPECTED_PROFILE_LOCK_SHA"],
        ".astrid-registry-state.json": expected["EXPECTED_REGISTRY_STATE_SHA"],
        "src/animations.generated.ts": expected["EXPECTED_REGISTRY_ANIMATIONS_SHA"],
        "src/effects.generated.ts": expected["EXPECTED_REGISTRY_EFFECTS_SHA"],
        "src/transitions.generated.ts": expected["EXPECTED_REGISTRY_TRANSITIONS_SHA"],
        "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz": expected["EXPECTED_PROFILE_ARCHIVE_SHA"],
    }
    assert {name: digest(profile / name) for name in fixed} == fixed
    package = json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())
    assert package["version"] == "0.0.14"
    return {"entries": entries, "writable": writable, "external_links": external_links, "fixed_sha256": fixed, "composition_version": package["version"]}

def node_facts():
    version = subprocess.check_output([str(node), "--version"], text=True).strip()
    npx = subprocess.check_output([str(Path(os.environ["F_RENDER_NODE_BIN"]) / "npx"), "--version"], text=True).strip()
    assert version == "v20.19.4"
    assert npx == "10.8.2"
    return {"node": str(node), "node_version": version, "npx": npx}

def environment_facts():
    forbidden = ("ASTRID_NORMAL_RUNTIME_SOURCE", "ASTRID_PARENT_MEDIA_SEED_RUNTIME", "ASTRID_WORD_ANCHOR_SEED_RUNTIME", "ASTRID_RUNTIME_SOURCE_MANIFEST")
    assert not any(name in os.environ for name in forbidden), {name: os.environ.get(name) for name in forbidden}
    assert os.environ.get("PYTEST_PLUGINS") is None and os.environ.get("PYTEST_ADDOPTS") is None
    return {"PATH": os.environ["PATH"], "PYTHONPATH": os.environ["PYTHONPATH"], "profile": os.environ["ASTRID_REMOTION_PROJECT_DIR"], "forbidden_absent": True}

def trivial_support():
    assert child is not None
    timeline = evidence / "trivial-empty.json"
    timeline.write_text(json.dumps({"theme": "banodoco-default", "theme_overrides": {"visual": {"canvas": {"width": 320, "height": 180, "fps": 24}}}, "tracks": [{"id": "v1", "kind": "visual", "label": "Empty"}], "clips": []}))
    code = "from astrid.sdk.rendering import support; import json, sys; report=support('rendering.threejs', timeline_path=sys.argv[1]); print(json.dumps(report.to_dict(), sort_keys=True)); assert report.supported and report.reasons == []"
    child_env = dict(os.environ)
    child_env["PATH"] = f"{child / 'bin'}:{os.environ['F_RENDER_NODE_BIN']}:/usr/bin:/bin"
    child_env["ASTRID_HOST_EXECUTION_PROFILE"] = "installed"
    child_env.pop("PYTHONPATH", None)
    result = subprocess.run([str(child / "bin/python"), "-I", "-B", "-c", code, str(timeline)], capture_output=True, text=True, env=child_env, check=False)
    (evidence / "trivial-support.log").write_text(result.stdout + result.stderr)
    assert result.returncode == 0, {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    return {"exit": result.returncode, "stdout": result.stdout.strip()}

check("Agent exact source tree and harness custody", source_identity)
check("Runtime exact pin and clean custody", runtime_identity)
check("validator and unchanged original body hashes", target_identity)
check("normal child receipt and bench-store lookup", receipt_and_bench_lookup)
check("current child installed import/source custody", child_probe)
check("old c886 RED source versus current child", old_child_red_source)
check("parent import origins", parent_origins)
check("Node20 and npx custody", node_facts)
check("read-only Remotion profile custody", profile_custody)
check("forbidden environment absent before body", environment_facts)
check("trivial supported preflight", trivial_support)

report = {
    "status": "passed" if not failures else "failed",
    "failures": failures,
    "checks": checks,
    "source": {
        "agent_sha": expected["EXPECTED_AGENT_SHA"],
        "runtime_sha": expected["EXPECTED_RUNTIME_SHA"],
        "validator_sha256": expected["EXPECTED_VALIDATOR_SHA"],
        "source_tree": expected["EXPECTED_SOURCE_TREE"],
    },
    "finite_suite": {
        "nodeids": ["tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"],
        "timeout_seconds": 45,
        "pytest": ["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45"],
        "target_sha256": expected["EXPECTED_TARGET_SHA"],
        "body_ast_sha256": expected["EXPECTED_BODY_SHA"],
    },
    "old_child": {"agent_sha": expected["EXPECTED_OLD_AGENT_SHA"], "validator_sha256": expected["EXPECTED_OLD_VALIDATOR_SHA"], "status": "RED/stale"},
    "original_case_executed": False,
}
out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(f"F_RENDER_0137_PREFLIGHT={'PASS' if not failures else 'FAIL'} failures={len(failures)} evidence={evidence}", flush=True)
raise SystemExit(bool(failures))
PY
PREFLIGHT=$?
set -e

CHILD=""
if [ -s "$EVIDENCE/child.path" ]; then
    CHILD=$(<"$EVIDENCE/child.path")
fi

if [ "$MODE" = preflight ] || [ "$PREFLIGHT" -ne 0 ]; then
    if [ "$PREFLIGHT" -ne 0 ] && [ -z "$CHILD" ]; then
        printf '%s\n' "remaining normal input: normal receipt + bench-store entry for $CHILD_NAME with Agent $EXPECTED_AGENT_SHA and Runtime $EXPECTED_RUNTIME_SHA" >&2
    fi
    exit "$PREFLIGHT"
fi

if [ -z "$CHILD" ]; then
    printf '%s\n' "refusing original node: current child was not admitted by normal receipt and bench-store lookup" >&2
    exit 1
fi

set +e
timeout 45 "$PARENT_PYTHON" -P -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
    tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons \
    >"$EVIDENCE/pytest.log" 2>&1
STATUS=$?
set -e
printf 'pytest_exit=%s\nchild=%s\ntimeout_seconds=45\n' "$STATUS" "$CHILD" > "$EVIDENCE/result.txt"
cat "$EVIDENCE/result.txt"
exit "$STATUS"
