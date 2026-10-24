#!/usr/bin/env python3
"""Prepare/run the one original discovery qualification row.

This runner is deliberately fail-closed.  It never falls back to the older
3b5c child, never adds a source checkout to product imports, and never wraps
the production caller.  The ``--child`` phase is launched with the exact
installed child interpreter and uses the existing
``renderer_execution_environment`` fixture before invoking pytest.
"""

from __future__ import annotations

import ast
import base64
import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
WORKER = ORCH / "workers/agt-F-discovery-child-bind-0603"
EVIDENCE = Path(os.environ.get("DISCOVERY_EVIDENCE", str(WORKER / "evidence")))
SCRATCH = Path(os.environ.get("DISCOVERY_TMPDIR", os.environ.get("TMPDIR", str(WORKER / "tmpdir"))))
RECEIPT = ORCH / "tests/provision/venv-agent-child-discovery-bb50-f320.txt"
TARGET = "tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"
TARGET_FILE = ROOT / "tests/packs/rendering/test_threejs_backend.py"

EXPECTED_AGENT = "bb50a43c915ec00c05c5ee34569a040bab8e817c"
EXPECTED_RUNTIME = "f3208b26b53c4d7053e5464eaa7c5e15b1505812"
EXPECTED_PROFILE = "agent-remotion-v3-819acf-1110"
PROFILE = Path("/home/user/work/runtimes") / EXPECTED_PROFILE
NODE = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node")
SCHEMA_SITE = Path("/home/user/work/venv-agent/lib/python3.13/site-packages")
EXPECTED_NODE_VERSION = "v20.19.4"
EXPECTED_COMPOSITION_ARCHIVE_SHA256 = (
    "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
)
EXPECTED_DISCOVERY_SHA256 = "40ae7c5945529bb65dbeb3853a80b1b03650e7dcc5f4a60ddaa04c4dc9f37999"
EXPECTED_DISCOVERY_TEST_SHA256 = "9faabadd340c1b2df04f0ab6e83c9d00ac1e6f9cf68fd2f8ed2b81af7e108e5f"
EXPECTED_TARGET_FILE_SHA256 = "9efe493cb2f8339177e07616b976afe6f9813ae4d415923ff25701b471e991c7"
EXPECTED_TARGET_FUNCTION_SHA256 = "ca54f2d5059bb3b5cca1e8ee43156df6762d3a86739caa2aa18ffcb83f3ded82"
EXPECTED_TARGET_ASSERTIONS_SHA256 = (
    "087c80d0211e714a7c073d12adb2e260d5de299ba3d251ac31b853562eb6de1e"
)
EXPECTED_CLIENT_FILES = {
    "astrid_runtime_client/__init__.py": "d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2",
    "astrid_runtime_client/contract_metadata.py": "a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae",
    "astrid_runtime_client/generated.py": "9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904",
    "astrid_runtime_client/timeline_commit_types.py": "88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616",
}
EXPECTED_CLIENT_IDENTITY_SHA256 = "10fc7e77b3ab381df46108b68ead23864d2f679fa069b41d113629efc1135a9e"
DECLARED_ENV_KEYS = (
    "HOME",
    "LANG",
    "LC_ALL",
    "PATH",
    "PYTHONPATH",
    "PYTHONDONTWRITEBYTECODE",
    "TMPDIR",
    "ASTRID_HOST_EXECUTION_PROFILE",
    "ASTRID_RUNTIME_CHECKOUT",
    "ASTRID_RUNTIME_SOURCE_ROOT",
    "ASTRID_REMOTION_PROJECT_DIR",
    "ASTRID_NODE_EXECUTABLE",
    "ASTRID_TEST_NODE_MODULES",
    "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
)
REQUIRED_PRODUCT_FILES = (
    "astrid/core/pack/discovery.py",
    "astrid/sdk/rendering.py",
    "astrid/core/rendering/transport.py",
    "astrid/core/rendering/registry.py",
    "astrid/packs/rendering/rendering/renderers/threejs/run.py",
    "astrid/packs/rendering/rendering/renderers/threejs/renderer.yaml",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def scrub(text: str) -> str:
    text = re.sub(
        r"(?i)(api[_-]?key|authorization|credential|password|secret|token)\s*[:=]\s*[^\s,;]+",
        r"\1=[redacted]",
        text,
    )
    return text.replace("\x00", "\ufffd")[:65536]


def write_json(name: str, value: Any) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def error_record(exc: Exception) -> dict[str, str]:
    return {"type": type(exc).__name__, "message": scrub(str(exc))}


def body_facts(path: Path) -> dict[str, Any]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node
        for node in ast.walk(module)
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"
    )
    assertions = [node for node in ast.walk(function) if isinstance(node, ast.Assert)]
    reasons_calls = sorted(
        node.lineno
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "reasons_for"
    )
    # The first call is inside the four-value clip-type loop.  The transition
    # assignment is therefore invocation six, while the body has nine asserts.
    return {
        "file_sha256": sha(path),
        "function_ast_sha256": sha_bytes(
            ast.dump(function, annotate_fields=True, include_attributes=False).encode()
        ),
        "assertions_ast_sha256": sha_bytes(
            ast.dump(
                ast.Module(body=assertions, type_ignores=[]),
                annotate_fields=True,
                include_attributes=False,
            ).encode()
        ),
        "assertion_count": len(assertions),
        "reasons_for_call_lines": reasons_calls,
        "support_invocation_count": 10
        if reasons_calls == [208, 217, 229, 241, 295, 309, 324]
        else -1,
        "transition_invocation": 6 if 229 in reasons_calls else -1,
        "transition_source_line": 229,
        "line_start": function.lineno,
        "line_end": function.end_lineno,
    }


def source_facts() -> dict[str, Any]:
    return {
        "agent_head": git("rev-parse", "HEAD"),
        "agent_status": git("status", "--porcelain", "--untracked-files=all").splitlines(),
        "runtime_head": git("rev-parse", "HEAD", cwd=Path("/home/user/work/wt/rt-pin-f3208b26")),
        "runtime_status": git(
            "status",
            "--porcelain",
            "--untracked-files=all",
            cwd=Path("/home/user/work/wt/rt-pin-f3208b26"),
        ).splitlines(),
        "discovery_sha256": sha(ROOT / "astrid/core/pack/discovery.py"),
        "discovery_test_sha256": sha(ROOT / "tests/packs/test_pack_discovery_single_scan.py"),
        "target_body": body_facts(TARGET_FILE),
    }


def resolve_child() -> Path:
    if not RECEIPT.is_file():
        raise RuntimeError(f"candidate receipt is unavailable: {RECEIPT}")
    text = RECEIPT.read_text(encoding="utf-8")
    if "status=passed" not in text.splitlines():
        raise RuntimeError("candidate receipt is not a passed normal-queue result")
    origin = next(
        (line.split("=", 1)[1] for line in text.splitlines() if line.startswith("astrid=")),
        None,
    )
    if not origin:
        raise RuntimeError("candidate receipt has no installed astrid origin")
    marker = "/lib/python3.13/site-packages/astrid/"
    if marker not in origin:
        raise RuntimeError(f"candidate origin is not a Python 3.13 site package: {origin}")
    child = Path(origin.split(marker, 1)[0])
    if "child-" not in child.name or not child.is_dir():
        raise RuntimeError(f"candidate child root is invalid: {child}")
    return child


def declared(env: dict[str, str]) -> dict[str, str | None]:
    return {key: env.get(key) for key in DECLARED_ENV_KEYS}


def initial_before() -> dict[str, Any]:
    return {
        "status": "before-execution",
        "runner_sha256": sha(Path(__file__).resolve()),
        "root": str(ROOT),
        "source": source_facts(),
        "expected": {
            "agent": EXPECTED_AGENT,
            "runtime": EXPECTED_RUNTIME,
            "client_identity_sha256": EXPECTED_CLIENT_IDENTITY_SHA256,
            "profile": EXPECTED_PROFILE,
            "node": str(NODE),
            "node_version": EXPECTED_NODE_VERSION,
            "composition_archive_sha256": EXPECTED_COMPOSITION_ARCHIVE_SHA256,
            "discovery_sha256": EXPECTED_DISCOVERY_SHA256,
            "discovery_test_sha256": EXPECTED_DISCOVERY_TEST_SHA256,
            "target_file_sha256": EXPECTED_TARGET_FILE_SHA256,
            "target_function_sha256": EXPECTED_TARGET_FUNCTION_SHA256,
            "target_assertions_sha256": EXPECTED_TARGET_ASSERTIONS_SHA256,
        },
        "receipt": {
            "path": str(RECEIPT),
            "exists": RECEIPT.is_file(),
            "sha256": sha(RECEIPT) if RECEIPT.is_file() else None,
        },
    }


def child_environment(child: Path) -> dict[str, str]:
    shim = SCRATCH / "import-shim"
    if shim.exists() and not shim.is_dir():
        raise RuntimeError(f"private import shim is not a directory: {shim}")
    shim.mkdir(parents=True, exist_ok=True)
    for name in ("tests", "scripts"):
        link = shim / name
        target = ROOT / name
        if link.exists() or link.is_symlink():
            if link.resolve() != target.resolve():
                raise RuntimeError(f"import shim link mismatch: {link}")
        else:
            link.symlink_to(target, target_is_directory=True)
    return {
        "HOME": "/root",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TMPDIR": str(SCRATCH),
        "PYTHONPATH": str(shim),
        "PATH": f"{child / 'bin'}:{NODE.parent}:/usr/bin:/bin",
        "ASTRID_HOST_EXECUTION_PROFILE": "installed",
        "ASTRID_RUNTIME_CHECKOUT": "/home/user/work/wt/rt-pin-f3208b26",
        "ASTRID_RUNTIME_SOURCE_ROOT": "/home/user/work/wt/rt-pin-f3208b26",
        "ASTRID_REMOTION_PROJECT_DIR": str(PROFILE),
        "ASTRID_NODE_EXECUTABLE": str(NODE),
        "ASTRID_TEST_NODE_MODULES": str(PROFILE / "node_modules"),
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(SCHEMA_SITE),
    }


def verify_record(site: Path) -> dict[str, Any]:
    records = sorted(site.glob("astrid-*.dist-info/RECORD"))
    if len(records) != 1:
        raise RuntimeError(f"expected one astrid RECORD, found {records}")
    rows = {row[0]: row for row in csv.reader(records[0].read_text().splitlines()) if row}
    checked: dict[str, Any] = {}
    for relative, expected in EXPECTED_CLIENT_FILES.items():
        row = rows.get(relative)
        path = site / relative
        if row is None or not path.is_file():
            raise RuntimeError(f"client RECORD row/file missing: {relative}")
        actual = sha(path)
        if actual != expected:
            raise RuntimeError(f"client identity mismatch: {relative}")
        wanted = "sha256=" + base64.urlsafe_b64encode(bytes.fromhex(actual)).decode().rstrip("=")
        if row[1] != wanted:
            raise RuntimeError(f"client RECORD digest mismatch: {relative}")
        checked[relative] = {"sha256": actual, "record": row}
    return {"path": str(records[0]), "sha256": sha(records[0]), "checked": checked}


def verify_direct_urls(child: Path, site: Path) -> dict[str, Any]:
    direct: dict[str, Any] = {}
    for name, suffix in (("astrid", "/agent"), ("astrid-runtime", "/runtime")):
        matches = sorted(site.glob(f"{name.replace('-', '_')}-*.dist-info/direct_url.json"))
        if len(matches) != 1:
            raise RuntimeError(f"expected one {name} direct_url.json, found {matches}")
        value = json.loads(matches[0].read_text(encoding="utf-8"))
        url = value.get("url", "")
        expected_root = (
            child / ".child-venv-source-venv-agent-child-discovery-bb50-f320" / suffix[1:]
        )
        if (
            not url.startswith("file://")
            or Path(url.removeprefix("file://")).resolve() != expected_root.resolve()
        ):
            raise RuntimeError(f"{name} direct_url does not bind the discovery child source: {url}")
        info = value.get("dir_info", value.get("directory_info", {}))
        if info.get("editable", False):
            raise RuntimeError(f"{name} is editable")
        direct[name] = {"path": str(matches[0]), "sha256": sha(matches[0]), "value": value}
    return direct


def run_child() -> int:
    child = Path(sys.prefix).resolve()
    site = child / "lib/python3.13/site-packages"
    preflight: dict[str, Any] = {
        "status": "started",
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "env_keys": sorted(os.environ),
        "declared_env": declared(dict(os.environ)),
        "timings": {"start_monotonic": time.monotonic()},
    }
    write_json("preflight.json", preflight)
    try:
        if git("rev-parse", "HEAD") != EXPECTED_AGENT:
            raise RuntimeError("author source is not the expected bb50 candidate")
        if (
            git("rev-parse", "HEAD", cwd=Path("/home/user/work/wt/rt-pin-f3208b26"))
            != EXPECTED_RUNTIME
        ):
            raise RuntimeError("Runtime source is not the expected f320 candidate")
        if not site.is_dir() or not Path(sys.executable).is_relative_to(child):
            raise RuntimeError("child interpreter is not the candidate installed venv")
        if (child / ".astrid-source-commit").read_text().strip() != EXPECTED_AGENT:
            raise RuntimeError("installed child source marker mismatch")
        if (child / ".astrid-runtime-source-commit").read_text().strip() != EXPECTED_RUNTIME:
            raise RuntimeError("installed child Runtime marker mismatch")
        if sha(ROOT / "astrid/core/pack/discovery.py") != EXPECTED_DISCOVERY_SHA256:
            raise RuntimeError("discovery source hash changed")
        if (
            sha(ROOT / "tests/packs/test_pack_discovery_single_scan.py")
            != EXPECTED_DISCOVERY_TEST_SHA256
        ):
            raise RuntimeError("discovery test source hash changed")
        target = body_facts(TARGET_FILE)
        if (
            target["file_sha256"] != EXPECTED_TARGET_FILE_SHA256
            or target["function_ast_sha256"] != EXPECTED_TARGET_FUNCTION_SHA256
            or target["assertions_ast_sha256"] != EXPECTED_TARGET_ASSERTIONS_SHA256
            or target["assertion_count"] != 9
            or target["support_invocation_count"] != 10
            or target["transition_invocation"] != 6
        ):
            raise RuntimeError("original qualification body/hash/count guard failed")
        preflight["target_body_before"] = target
        preflight["source_files"] = {}
        for relative in REQUIRED_PRODUCT_FILES:
            source = ROOT / relative
            installed = site / relative
            if source.read_bytes() != installed.read_bytes():
                raise RuntimeError(f"source/install product bytes differ: {relative}")
            preflight["source_files"][relative] = {
                "source_sha256": sha(source),
                "installed_sha256": sha(installed),
            }
        names = (
            "astrid",
            "astrid.sdk.rendering",
            "astrid.core.pack.discovery",
            "astrid.core.rendering.registry",
            "astrid.core.rendering.transport",
            "astrid.packs.rendering.rendering.renderers.threejs.run",
            "astrid_runtime_client",
            "runtime_protocol",
        )
        origins = {
            name: str(importlib.util.find_spec(name).origin)
            for name in names
            if importlib.util.find_spec(name) is not None
        }
        if set(origins) != set(names) or any(
            not Path(origin).resolve().is_relative_to(site.resolve()) for origin in origins.values()
        ):
            raise RuntimeError(f"product import escaped installed site-packages: {origins}")
        preflight["import_origins"] = origins
        preflight["record"] = verify_record(site)
        preflight["direct_urls"] = verify_direct_urls(child, site)
        identity = (child / ".astrid-runtime-client-identity").read_text(encoding="utf-8").strip()
        if sha_bytes(identity.encode()) != EXPECTED_CLIENT_IDENTITY_SHA256:
            raise RuntimeError("runtime client identity marker mismatch")
        archive = (
            PROFILE
            / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
        )
        if sha(archive) != EXPECTED_COMPOSITION_ARCHIVE_SHA256:
            raise RuntimeError("Remotion composition archive changed")
        if (
            sha(PROFILE / "package-lock.json")
            != "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
        ):
            raise RuntimeError("Remotion graph package lock changed")
        if not (PROFILE / "node_modules").is_dir() or not NODE.is_file():
            raise RuntimeError("qualified Remotion graph or Node is unavailable")
        node_version = subprocess.check_output([str(NODE), "--version"], text=True).strip()
        if node_version != EXPECTED_NODE_VERSION:
            raise RuntimeError(f"Node version mismatch: {node_version}")
        preflight["profile"] = {
            "path": str(PROFILE),
            "node": str(NODE),
            "node_version": node_version,
            "node_modules": str(PROFILE / "node_modules"),
            "composition_archive_sha256": sha(archive),
            "package_lock_sha256": sha(PROFILE / "package-lock.json"),
        }

        from astrid.core.rendering import transport
        from astrid.core.subprocess_env import build_child_subprocess_env
        from tests.packs.conftest import renderer_execution_environment

        fixture = renderer_execution_environment.__wrapped__()
        next(fixture)
        try:
            caller_env = dict(os.environ)
            projected = build_child_subprocess_env(base=caller_env, parent=caller_env)
            actual = transport._build_environment(None)
            if actual != projected:
                raise RuntimeError(
                    "transport environment differs from production policy projection"
                )
            if "ASTRID_HOST_EXECUTION_PROFILE" in actual:
                raise RuntimeError("caller HOSTPROFILE was not intentionally dropped")
            preflight["fixture"] = {
                "caller_declared_env": declared(caller_env),
                "projected_declared_env": declared(projected),
                "actual_declared_env": declared(actual),
                "caller_env_keys": sorted(caller_env),
                "projected_env_keys": sorted(projected),
                "actual_env_keys": sorted(actual),
                "dropped_caller_hostprofile": "ASTRID_HOST_EXECUTION_PROFILE" not in actual,
            }
        finally:
            try:
                next(fixture)
            except StopIteration:
                pass
        preflight["status"] = "passed"
        preflight["timings"]["end_monotonic"] = time.monotonic()
        write_json("preflight.json", preflight)
        (EVIDENCE / "body-started").write_text(
            time.strftime("%Y-%m-%dT%H:%M:%SZ"), encoding="utf-8"
        )
        command = [
            str(Path(sys.executable)),
            "-P",
            "-m",
            "pytest",
            "--import-mode=importlib",
            "-q",
            "-oaddopts=",
            "-pno:cacheprovider",
            "--timeout=45",
            TARGET,
        ]
        started = time.monotonic()
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=dict(os.environ),
            capture_output=True,
            text=True,
            check=False,
        )
        finished = time.monotonic()
        result = {
            "status": "passed" if completed.returncode == 0 else "failed",
            "argv": command,
            "cwd": str(ROOT),
            "env_keys": sorted(os.environ),
            "returncode": completed.returncode,
            "timings": {
                "start_monotonic": started,
                "end_monotonic": finished,
                "elapsed": finished - started,
            },
            "stdout": {
                "sha256": sha_bytes(completed.stdout.encode()),
                "text": scrub(completed.stdout),
            },
            "stderr": {
                "sha256": sha_bytes(completed.stderr.encode()),
                "text": scrub(completed.stderr),
            },
            "result_paths": [str(path) for path in SCRATCH.rglob("*support-result.json")],
        }
        write_json("result.json", result)
        return completed.returncode
    except Exception as exc:  # noqa: BLE001 - retain durable failure evidence
        preflight["status"] = "failed"
        preflight["failure"] = {"type": type(exc).__name__, "message": scrub(str(exc))}
        preflight["timings"]["end_monotonic"] = time.monotonic()
        write_json("preflight.json", preflight)
        write_json(
            "result.json",
            {
                "status": "blocked-before-body",
                "argv": None,
                "cwd": str(ROOT),
                "env_keys": sorted(os.environ),
                "returncode": 2,
                "failure": preflight["failure"],
                "timings": preflight["timings"],
                "stdout": {"sha256": None, "text": ""},
                "stderr": {"sha256": None, "text": ""},
                "result_paths": [],
            },
        )
        return 2
    finally:
        try:
            before = json.loads((EVIDENCE / "before.json").read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - after evidence must survive setup failures
            before = {"source": {}, "failure": error_record(exc)}
        try:
            source_after = source_facts()
            target_after = body_facts(TARGET_FILE)
        except Exception as exc:  # noqa: BLE001 - after evidence must survive setup failures
            source_after = {"failure": error_record(exc)}
            target_after = {"failure": error_record(exc)}
        post = {
            "status": "after-execution",
            "source": source_after,
            "target_body_after": target_after,
            "target_body_unchanged": target_after == before.get("source", {}).get("target_body"),
            "runtime_status": git(
                "status",
                "--porcelain",
                "--untracked-files=all",
                cwd=Path("/home/user/work/wt/rt-pin-f3208b26"),
            ).splitlines(),
            "body_started": (EVIDENCE / "body-started").is_file(),
        }
        write_json("postflight.json", post)


def run_parent(mode: str) -> int:
    try:
        before = initial_before()
    except Exception as exc:  # noqa: BLE001 - before evidence must survive setup failures
        before = {"status": "before-execution-failed", "failure": error_record(exc)}
    write_json("before.json", before)
    started = time.monotonic()
    child = None
    completed: subprocess.CompletedProcess[str] | None = None
    failure: dict[str, str] | None = None
    try:
        child = resolve_child()
        environment = child_environment(child)
        command = [str(child / "bin/python"), "-P", str(Path(__file__).resolve()), "--child", mode]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        returncode = completed.returncode
    except Exception as exc:  # noqa: BLE001 - retain durable failure evidence
        returncode = 2
        failure = {"type": type(exc).__name__, "message": scrub(str(exc))}
    finally:
        finished = time.monotonic()
        after = {
            "status": "completed" if failure is None else "blocked-before-child",
            "child": str(child) if child else None,
            "argv": command if child else None,
            "cwd": str(ROOT),
            "env_keys": sorted(environment) if child else [],
            "returncode": returncode,
            "timings": {
                "start_monotonic": started,
                "end_monotonic": finished,
                "elapsed": finished - started,
            },
            "stdout": (
                {"sha256": sha_bytes(completed.stdout.encode()), "text": scrub(completed.stdout)}
                if completed
                else {"sha256": None, "text": ""}
            ),
            "stderr": (
                {"sha256": sha_bytes(completed.stderr.encode()), "text": scrub(completed.stderr)}
                if completed
                else {"sha256": None, "text": ""}
            ),
            "failure": failure,
        }
        write_json("after.json", after)
    return returncode


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if "--child" in sys.argv:
        SCRATCH.mkdir(parents=True, exist_ok=True)
        return run_child()
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode not in {"run", "preflight"}:
        print("usage: run-discovery-original-0603.py [preflight|run]", file=sys.stderr)
        return 2
    return run_parent(mode)


if __name__ == "__main__":
    raise SystemExit(main())
