#!/usr/bin/env python3
"""Readonly qualification for the current normal working-venv service route.

This deliberately does not start Runtime or call a service.  It verifies the
frozen tuple in current-service-inputs.json at the actual import/artifact seams
and exits nonzero when source moves or a reusable input changes.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
RECIPE_PATH = HERE / "current-service-inputs.json"
CLIENT_FILES = (
    "__init__.py",
    "generated.py",
    "contract_metadata.py",
    "timeline_commit_types.py",
)


def fail(message: str) -> "NoReturn":
    raise RuntimeError(message)


def git(checkout: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", checkout, *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"git refused at {checkout}: {result.stderr.strip()}")
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def source_tuple(recipe: dict, name: str) -> dict:
    expected = recipe["source"][name]
    checkout = expected["checkout"]
    actual = {
        "checkout": checkout,
        "head": git(checkout, "rev-parse", "HEAD"),
        "tree": git(checkout, "rev-parse", "HEAD^{tree}"),
        "parent": git(checkout, "rev-parse", "HEAD^1"),
        "clean": git(checkout, "status", "--porcelain") == "",
    }
    for field in ("head", "tree", "parent"):
        require(actual[field] == expected[field], f"{name} {field} moved: {actual[field]} != {expected[field]}")
    require(actual["clean"], f"{name} checkout is not clean")
    if name == "agent":
        actual["remotion_tree"] = git(checkout, "rev-parse", "HEAD:remotion")
        require(actual["remotion_tree"] == expected["remotion_tree"], "Agent Remotion tree moved")
    return actual


def probe(python: str, names: list[str], distributions: list[str]) -> dict:
    source = r'''
import importlib.metadata as metadata
import importlib.util
import json
from pathlib import Path

def origin(name):
    spec = importlib.util.find_spec(name)
    return str(Path(spec.origin).resolve()) if spec and spec.origin else None

print(json.dumps({
    "python": str(Path(__import__("sys").executable).resolve()),
    "imports": {name: origin(name) for name in NAMES},
    "distributions": {name: metadata.version(name) if _has(name) else None for name in DISTRIBUTIONS},
}))
'''
    source = "def _has(name):\n    try:\n        metadata.version(name)\n        return True\n    except metadata.PackageNotFoundError:\n        return False\nNAMES=" + repr(names) + "\nDISTRIBUTIONS=" + repr(distributions) + "\n" + source
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [python, "-c", source],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode:
        fail(f"supported import probe refused by {python}: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"invalid probe output from {python}: {exc}")


def check_probe(recipe: dict, role: str, names: list[str], distributions: list[str]) -> dict:
    expected = recipe["interpreters"][role]
    path = expected["path"]
    actual = probe(path, names, distributions)
    require(actual["python"] == expected["realpath"], f"{role} interpreter changed: {actual['python']}")
    for name, origin in expected["imports"].items():
        require(actual["imports"].get(name) == origin, f"{role} origin mismatch for {name}: {actual['imports'].get(name)} != {origin}")
    for name, version in expected["distributions"].items():
        require(actual["distributions"].get(name) == version, f"{role} version mismatch for {name}")
    return actual


def check_client(recipe: dict) -> dict:
    expected = recipe["client_contract"]
    roots = [Path(path) for path in expected["source_roots"]]
    observed = {}
    for relative in CLIENT_FILES:
        key = f"astrid_runtime_client/{relative}"
        paths = [root / relative for root in roots]
        require(all(path.is_file() for path in paths), f"missing client source for {key}")
        hashes = [sha256(path) for path in paths]
        require(len(set(hashes)) == 1, f"Agent/Runtime client mismatch for {key}")
        require(hashes[0] == expected["files"][key], f"client hash changed for {key}")
        observed[key] = hashes[0]
    metadata = roots[0] / "contract_metadata.py"
    text = metadata.read_text(encoding="utf-8")
    require("CONTRACT_VERSION = '0.2.14'" in text, "client contract version changed")
    require(expected["schema_digest"] in text, "client schema digest changed")
    for raw_path, expected_hash in expected["runtime_artifacts"].items():
        path = Path(raw_path)
        require(sha256(path) == expected_hash, f"Runtime artifact hash changed: {path}")
    return observed


def check_remotion(recipe: dict) -> dict:
    expected = recipe["remotion"]
    bench = Path(expected["bench"])
    require(bench.is_dir(), f"Remotion bench missing: {bench}")
    markers = {
        ".astrid-remotion-tree": expected["current_agent_remotion_tree"],
        ".astrid-agent-source-commit": expected["historical_source_commit_marker"],
        ".astrid-package-sha256": expected["package_sha256"],
        ".astrid-package-lock-sha256": expected["package_lock_sha256"],
        ".astrid-component-identity": expected["component_identity"],
        ".astrid-artifact-integrity": expected["artifact_integrity"],
        ".astrid-installed-module-origins": expected["installed_module_origins"],
        ".astrid-node-modules-lock-sha256": expected["node_modules_lock_sha256"],
        ".astrid-node-version": expected["node"],
        ".astrid-npm-version": expected["npm"],
    }
    for marker, value in markers.items():
        require((bench / marker).read_text(encoding="utf-8").strip() == value, f"Remotion marker changed: {marker}")
    agent_remotion = Path("/home/user/work/agent/remotion")
    require(sha256(agent_remotion / "package.json") == expected["package_sha256"], "current Remotion package changed")
    require(sha256(agent_remotion / "package-lock.json") == expected["package_lock_sha256"], "current Remotion lock changed")
    return {"bench": str(bench), "source_commit_marker": expected["historical_source_commit_marker"]}


def check_graph(recipe: dict) -> dict:
    expected = recipe["composition"]
    artifact = Path(expected["artifact"])
    graph = Path(expected["qualified_graph"])
    require(sha256(artifact) == expected["artifact_sha256"], f"Composition artifact changed: {artifact}")
    package = graph / "@banodoco" / "timeline-composition" / "package.json"
    require(package.is_file(), f"Composition graph package missing: {package}")
    package_data = json.loads(package.read_text(encoding="utf-8"))
    require(package_data.get("name") == expected["package"], "Composition package name changed")
    require(package_data.get("version") == expected["version"], "Composition package version changed")
    files = {
        str(path.relative_to(graph)): sha256(path)
        for path in graph.rglob("*")
        if path.is_file()
    }
    require(len(files) == expected["file_count"], "Composition graph file count changed")
    actual_map = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(actual_map == expected["file_map_sha256"], "Composition graph file map changed")
    return {"file_count": len(files), "file_map_sha256": actual_map}


def main() -> int:
    recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
    before = {name: source_tuple(recipe, name) for name in ("app", "agent", "runtime")}
    probes = {
        "agent": check_probe(recipe, "agent", ["astrid", "astrid_runtime_client", "banodoco_timeline_schema", "astrid_runtime", "runtime_protocol"], ["astrid", "banodoco-timeline-schema"]),
        "runtime": check_probe(recipe, "runtime", ["astrid_runtime", "runtime_protocol", "astrid", "astrid_runtime_client", "banodoco_timeline_schema"], ["astrid-runtime"]),
    }
    client = check_client(recipe)
    remotion = check_remotion(recipe)
    graph = check_graph(recipe)
    after = {name: source_tuple(recipe, name) for name in ("app", "agent", "runtime")}
    require(before == after, "source tuple moved during qualification; reject this use")
    print(json.dumps({
        "status": "qualified_existing_inputs_not_live",
        "source": after,
        "probes": probes,
        "client_sha256": client,
        "remotion": remotion,
        "composition": graph,
        "service_execution": "not run",
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"current-service-inputs: REFUSED: {exc}", file=sys.stderr)
        raise SystemExit(1)
