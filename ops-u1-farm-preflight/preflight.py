"""Farm-only, read-only prerequisite census for the D135 Runtime proof.

This program deliberately imports the seven named modules in separate child
processes.  A broken import in one module therefore cannot prevent the other
six from being checked, and no pytest collection, fixture, test body, provider,
socket, Store, or acquisition path is entered.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_ROOT / "source-manifest.json"
CHILD_SENTINEL = "D135_IMPORT_RESULT:"
IMPORT_TIMEOUT_SECONDS = 30
MAX_CAPTURE_BYTES = 32_000
EXPECTED_INTERPRETER = Path("/home/user/work/venv-agent/bin/python")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _regular_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _top_level_imports(tree: ast.Module) -> list[dict[str, Any]]:
    """Collect imports executable while loading a module, not inside a body."""

    found: list[dict[str, Any]] = []

    def visit(nodes: list[ast.stmt], guarded: bool = False) -> None:
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.append(
                        {
                            "module": alias.name,
                            "names": [alias.asname or alias.name.split(".")[-1]],
                            "line": node.lineno,
                            "guarded": guarded,
                            "platform_optional": False,
                        }
                    )
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                found.append(
                    {
                        "module": node.module or "",
                        "names": [alias.asname or alias.name for alias in node.names],
                        "line": node.lineno,
                        "guarded": guarded,
                        "platform_optional": False,
                    }
                )
            if isinstance(node, (ast.If, ast.Try, ast.With, ast.AsyncWith)):
                children: list[ast.stmt] = list(getattr(node, "body", []))
                children.extend(getattr(node, "orelse", []))
                children.extend(getattr(node, "finalbody", []))
                for handler in getattr(node, "handlers", []):
                    children.extend(handler.body)
                visit(children, guarded=True)

    visit(tree.body)
    return found


def _dangerous_top_level_calls(tree: ast.Module) -> list[dict[str, Any]]:
    denied = {
        "pytest.main",
        "pytest.console_main",
        "socket.socket",
        "subprocess.run",
        "subprocess.Popen",
        "RuntimeService",
        "RealmStore.initialize",
        "RuntimeDaemon",
        "open",
        "os.system",
        "os.popen",
    }
    findings: list[dict[str, Any]] = []

    def dotted(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            parent = dotted(node.value)
            return f"{parent}.{node.attr}" if parent else node.attr
        return ""

    def visit(nodes: list[ast.stmt]) -> None:
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and dotted(child.func) in denied:
                    findings.append({"line": child.lineno, "call": dotted(child.func)})
            if isinstance(node, (ast.If, ast.Try, ast.With, ast.AsyncWith)):
                visit(list(getattr(node, "body", [])))
                visit(list(getattr(node, "orelse", [])))
                visit(list(getattr(node, "finalbody", [])))
                for handler in getattr(node, "handlers", []):
                    visit(handler.body)

    visit(tree.body)
    return findings


def _child_import(module: str, path_entries: list[Path], source_root: Path, agent_root: Path) -> dict[str, Any]:
    code = r'''
import importlib
import json
import sys

module = sys.argv[1]
try:
    imported = importlib.import_module(module)
    origins = {}
    for name, loaded in sorted(sys.modules.items()):
        origin = getattr(loaded, "__file__", None)
        if origin:
            origins[name] = origin
    print("D135_IMPORT_RESULT:" + json.dumps({"ok": True, "module": module, "origins": origins}, sort_keys=True))
except BaseException as exc:
    print("D135_IMPORT_RESULT:" + json.dumps({
        "ok": False,
        "module": module,
        "exception": type(exc).__name__,
        "message": str(exc),
        "missing_name": getattr(exc, "name", None),
        "traceback": __import__("traceback").format_exc(),
    }, sort_keys=True))
    raise SystemExit(1)
'''
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["ASTRID_CHECKOUT"] = str(agent_root)
    env["RUNTIME_CHECKOUT"] = str(source_root)
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in path_entries)
    result = subprocess.run(
        [sys.executable, "-c", code, module],
        cwd=source_root,
        env=env,
        capture_output=True,
        text=True,
        timeout=IMPORT_TIMEOUT_SECONDS,
        check=False,
    )
    payload: dict[str, Any] | None = None
    for line in result.stdout.splitlines():
        if line.startswith(CHILD_SENTINEL):
            payload = json.loads(line[len(CHILD_SENTINEL) :])
    if payload is None:
        payload = {
            "ok": False,
            "module": module,
            "exception": "NoCensusResult",
            "message": "import child did not emit its result sentinel",
        }
    payload["returncode"] = result.returncode
    payload["stdout"] = result.stdout[-MAX_CAPTURE_BYTES:]
    payload["stderr"] = result.stderr[-MAX_CAPTURE_BYTES:]
    if payload.get("ok"):
        origins = payload.get("origins", {})
        checked: list[dict[str, Any]] = []
        for name, origin in origins.items():
            origin_path = _resolved(Path(origin))
            owner = "runtime" if _inside(origin_path, source_root) else "agent" if _inside(origin_path, agent_root) else "external"
            item: dict[str, Any] = {"module": name, "origin": str(origin_path), "owner": owner}
            if _regular_file(origin_path):
                item["sha256"] = _sha256(origin_path)
            checked.append(item)
        payload["origins"] = checked
    return payload


def _package_check(requirements: list[dict[str, str]]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for requirement in requirements:
        name = requirement["distribution"]
        try:
            version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            missing.append({**requirement, "status": "missing"})
        else:
            item = {**requirement, "status": "installed", "version": version}
            try:
                importable = importlib.util.find_spec(requirement["import"]) is not None
            except (ImportError, ModuleNotFoundError, ValueError):
                importable = False
            item["importable"] = importable
            if not importable:
                item["status"] = "installed_but_not_importable"
            missing.append(item)
    return missing


def _source_checks(manifest: dict[str, Any], runtime_root: Path, agent_root: Path) -> list[dict[str, Any]]:
    roots = {"runtime": runtime_root, "agent": agent_root}
    checks: list[dict[str, Any]] = []
    for item in manifest["source_files"]:
        root = roots[item["owner"]]
        path = root / item["path"]
        result: dict[str, Any] = {
            "owner": item["owner"],
            "path": item["path"],
            "absolute_path": str(_resolved(path)),
            "expected_sha256": item["sha256"],
        }
        if not _regular_file(path):
            result["status"] = "missing_or_non_regular"
        else:
            result["actual_sha256"] = _sha256(path)
            result["status"] = "pass" if result["actual_sha256"] == item["sha256"] else "hash_mismatch"
        checks.append(result)
    return checks


def _manifest_checks(manifest: dict[str, Any], runtime_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in manifest["actual_modules"]:
        path = runtime_root / item["path"]
        result = {"module": item["module"], "path": item["path"], "status": "pass"}
        if not _regular_file(path):
            result["status"] = "missing_or_non_regular"
            results.append(result)
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            result["status"] = "parse_error"
            result["error"] = f"{type(exc).__name__}: {exc}"
            results.append(result)
            continue
        observed = _top_level_imports(tree)
        expected = item["top_level_imports"]
        if observed != expected:
            result["status"] = "manifest_coverage_mismatch"
            result["observed"] = observed
            result["expected"] = expected
        dangerous = _dangerous_top_level_calls(tree)
        if dangerous:
            result["status"] = "unexpected_top_level_side_effect"
            result["dangerous_calls"] = dangerous
        results.append(result)
    return results


def _check_output_dir(path: Path) -> dict[str, Any]:
    path.mkdir(parents=True, exist_ok=True)
    result = {"path": str(path), "exists": path.is_dir(), "writable": False}
    if not result["exists"]:
        return result
    try:
        with tempfile.TemporaryFile(dir=path, prefix="d135-write-test-"):
            pass
    except OSError as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    else:
        result["writable"] = True
    return result


def _origin_guards(
    manifest: dict[str, Any],
    imports: list[dict[str, Any]],
    runtime_root: Path,
) -> list[dict[str, Any]]:
    guards: list[dict[str, Any]] = []
    for item, result in zip(manifest["actual_modules"], imports, strict=True):
        expected = _resolved(runtime_root / item["path"])
        observed = next(
            (origin for origin in result.get("origins", []) if origin.get("module") == item["module"]),
            None,
        )
        guard: dict[str, Any] = {
            "module": item["module"],
            "expected_origin": str(expected),
            "expected_sha256": item["sha256"],
            "status": "pass",
        }
        if not result.get("ok") or observed is None:
            guard["status"] = "not_imported"
        else:
            guard["observed_origin"] = observed.get("origin")
            guard["observed_sha256"] = observed.get("sha256")
            if observed.get("origin") != str(expected):
                guard["status"] = "origin_mismatch"
            elif observed.get("sha256") != item["sha256"]:
                guard["status"] = "hash_mismatch"
        guards.append(guard)
    return guards


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-checkout", type=Path, required=True)
    parser.add_argument("--agent-checkout", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-interpreter", type=Path, default=EXPECTED_INTERPRETER)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output_dir = _resolved(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    runtime_root = _resolved(args.runtime_checkout)
    agent_root = _resolved(args.agent_checkout)
    source_results = _source_checks(manifest, runtime_root, agent_root)
    manifest_results = _manifest_checks(manifest, runtime_root)
    package_results = _package_check(manifest["required_distributions"])
    path_entries = [runtime_root, runtime_root / "packages" / "python", runtime_root / "tests", agent_root]
    path_result = {
        "entries": [str(path) for path in path_entries],
        "all_directories": all(path.is_dir() for path in path_entries),
        "astrid_checkout": str(agent_root),
        "runtime_checkout": str(runtime_root),
    }
    interpreter = {
        "sys_executable": str(_resolved(Path(sys.executable))),
        "expected": str(_resolved(args.expected_interpreter)),
        "exists": Path(sys.executable).is_file(),
        "matches_expected": _resolved(Path(sys.executable)) == _resolved(args.expected_interpreter),
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
    }
    output_result = _check_output_dir(output_dir)
    imports: list[dict[str, Any]] = []
    for item in manifest["actual_modules"]:
        try:
            imports.append(_child_import(item["module"], path_entries, runtime_root, agent_root))
        except (OSError, subprocess.TimeoutExpired) as exc:
            imports.append(
                {
                    "ok": False,
                    "module": item["module"],
                    "exception": type(exc).__name__,
                    "message": str(exc),
                }
            )
    origin_guards = _origin_guards(manifest, imports, runtime_root)

    all_missing: list[dict[str, Any]] = []
    for result in imports:
        if result.get("ok"):
            continue
        all_missing.append(
            {
                "module": result.get("module"),
                "exception": result.get("exception"),
                "missing_name": result.get("missing_name"),
                "message": result.get("message"),
            }
        )
    package_missing = [
        item
        for item in package_results
        if item["status"] != "installed" or not item.get("importable", False)
    ]
    failed_sources = [item for item in source_results if item["status"] != "pass"]
    failed_manifest = [item for item in manifest_results if item["status"] != "pass"]
    imported_failures = [item for item in imports if not item.get("ok")]
    failed_origins = [item for item in origin_guards if item["status"] != "pass"]
    readiness = {
        "task": manifest["task"],
        "venue": "Farm",
        "status": "PASS" if not (
            failed_sources
            or failed_manifest
            or package_missing
            or imported_failures
            or failed_origins
            or not interpreter["matches_expected"]
            or not path_result["all_directories"]
            or not output_result["writable"]
        ) else "REFUSED",
        "body_authorized": False,
        "test_body_run": False,
        "all_missing_count": len(all_missing),
        "exact_six_file_argv": manifest["test_argv"],
    }
    report = {
        "schema_version": 1,
        "task": manifest["task"],
        "venue": "Farm",
        "preflight_only": True,
        "body_not_run": True,
        "manifest": str(MANIFEST_PATH),
        "interpreter": interpreter,
        "source_roots": {"runtime": str(runtime_root), "agent": str(agent_root)},
        "pythonpath": path_result,
        "required_distributions": package_results,
        "source_checks": source_results,
        "manifest_checks": manifest_results,
        "imports": imports,
        "origin_guards": origin_guards,
        "all_missing": all_missing,
        "output": output_result,
        "readiness": readiness,
    }
    _write_json(output_dir / "preflight.json", report)
    _write_json(output_dir / "all-missing.json", {"task": manifest["task"], "all_missing": all_missing})
    (output_dir / "import.log").write_text(
        "\n".join(
            f"{item.get('module')}: {'PASS' if item.get('ok') else 'FAIL'}"
            for item in imports
        )
        + "\n",
        encoding="utf-8",
    )
    _write_json(output_dir / "readiness.json", readiness)
    print(json.dumps(readiness, sort_keys=True))
    return 0 if readiness["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
