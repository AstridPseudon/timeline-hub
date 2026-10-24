#!/usr/bin/env python3
"""Refresh and authenticate the existing normal working-venv inputs.

The refresh is read-only with respect to the integrations and installed
artifacts. It writes only this recipe after every observed source, import,
client, Runtime blob, Remotion, and Composition fact has been checked twice
for stability. It never starts Runtime or calls a service.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


HERE = Path(__file__).resolve().parent
RECIPE_PATH = HERE / "current-service-inputs.json"
NORMAL_REF = "tl/integration"
CHECKOUTS = {
    "app": "/home/user/work/app",
    "agent": "/home/user/work/agent",
    "runtime": "/home/user/work/runtime",
}
CLIENT_FILES = ("__init__.py", "generated.py", "contract_metadata.py", "timeline_commit_types.py")
CLIENT_ROOTS = (
    "/home/user/work/agent/astrid_runtime_client",
    "/home/user/work/runtime/packages/python/astrid_runtime_client",
)
RUNTIME_ARTIFACTS = (
    "/home/user/work/runtime/contract/artifacts.json",
    "/home/user/work/runtime/contract/component-manifest.json",
    "/home/user/work/runtime/contract/schemas/timeline-config.schema.json",
    "/home/user/work/runtime/runtime_protocol/schemas/timeline-commit-bundle.json",
)
RUNTIME_LOCKS = {"app": 14, "agent": 15}
ENVIRONMENT_FILE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion.env"
)
REMOTION_ROOT = Path("/home/user/work/agent/remotion")
IMPORT_PROBES = {
    "agent": (
        ["astrid", "astrid_runtime_client", "banodoco_timeline_schema", "astrid_runtime", "runtime_protocol"],
        ["astrid", "banodoco-timeline-schema"],
    ),
    "runtime": (
        ["astrid_runtime", "runtime_protocol", "astrid", "astrid_runtime_client", "banodoco_timeline_schema"],
        ["astrid-runtime"],
    ),
}


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git(checkout: str, *args: str) -> str:
    result = subprocess.run(["git", "-C", checkout, *args], check=False, capture_output=True, text=True)
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


def read_text(path: Path) -> str:
    try:
        require(path.is_file() and not path.is_symlink(), f"input is not a regular file: {path}")
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")


def source_tuple(checkout: str, name: str, expected: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(checkout)
    require(root.is_absolute() and root.resolve() == root and not root.is_symlink() and root.is_dir(),
            f"{name} checkout is not a physical directory: {checkout}")
    require(git(checkout, "rev-parse", "--show-toplevel") == checkout, f"{name} is not the checkout root")
    actual = {
        "checkout": checkout,
        "ref": git(checkout, "symbolic-ref", "--short", "HEAD"),
        "head": git(checkout, "rev-parse", "HEAD"),
        "tree": git(checkout, "rev-parse", "HEAD^{tree}"),
        "parents": git(checkout, "show", "-s", "--format=%P", "HEAD").split(),
        "clean": git(checkout, "status", "--porcelain", "--untracked-files=all") == "",
    }
    require(actual["ref"] == NORMAL_REF, f"{name} is not on {NORMAL_REF}: {actual['ref']}")
    require(actual["parents"], f"{name} has no parent list")
    require(actual["clean"], f"{name} checkout is dirty")
    if name == "agent":
        actual["remotion_tree"] = git(checkout, "rev-parse", "HEAD:remotion")
    if expected is not None:
        for key in ("checkout", "ref", "head", "tree", "parents"):
            require(actual[key] == expected.get(key), f"{name} {key} moved: {actual[key]} != {expected.get(key)}")
        if name == "agent":
            require(actual["remotion_tree"] == expected.get("remotion_tree"), "Agent Remotion tree moved")
    return actual


def current_sources() -> dict[str, dict[str, Any]]:
    return {name: source_tuple(path, name) for name, path in CHECKOUTS.items()}


def probe(python: str, names: list[str], distributions: list[str]) -> dict[str, Any]:
    source = r'''
import importlib.metadata as metadata
import importlib.util
import json
import sys
import sysconfig
from pathlib import Path

def origin(name):
    spec = importlib.util.find_spec(name)
    return str(Path(spec.origin).resolve()) if spec and spec.origin else None

def present(name):
    try:
        metadata.version(name)
        return True
    except metadata.PackageNotFoundError:
        return False

print(json.dumps({
    "python": str(Path(sys.executable).resolve()),
    "site_packages": str(Path(sysconfig.get_paths()["purelib"]).resolve()),
    "imports": {name: origin(name) for name in NAMES},
    "distributions": {name: metadata.version(name) if present(name) else None for name in DISTRIBUTIONS},
}))
'''
    source = "NAMES=" + repr(names) + "\nDISTRIBUTIONS=" + repr(distributions) + "\n" + source
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run([python, "-c", source], check=False, capture_output=True, text=True, env=env)
    if result.returncode:
        fail(f"supported import probe refused by {python}: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"invalid probe output from {python}: {exc}")


def check_probe(recipe: dict[str, Any], role: str, names: list[str], distributions: list[str]) -> dict[str, Any]:
    expected = recipe["interpreters"][role]
    actual = probe(expected["path"], names, distributions)
    require(actual["python"] == expected["realpath"], f"{role} interpreter changed")
    for key in ("site_packages", "imports", "distributions"):
        require(actual[key] == expected[key], f"{role} {key} changed")
    return actual


def interpreter_snapshot(base: dict[str, Any]) -> dict[str, Any]:
    result = {}
    for role, (names, distributions) in IMPORT_PROBES.items():
        old = base["interpreters"][role]
        observed = probe(old["path"], names, distributions)
        result[role] = {
            "path": old["path"],
            "realpath": observed["python"],
            "role": old["role"],
            "site_packages": observed["site_packages"],
            "imports": observed["imports"],
            "distributions": observed["distributions"],
        }
    return result


def check_client(recipe: dict[str, Any]) -> dict[str, Any]:
    expected = recipe["client_contract"]
    roots = [Path(path) for path in expected["source_roots"]]
    observed_files = {}
    for relative in CLIENT_FILES:
        key = f"astrid_runtime_client/{relative}"
        paths = [root / relative for root in roots]
        require(all(path.is_file() and not path.is_symlink() for path in paths), f"missing client source for {key}")
        hashes = [sha256(path) for path in paths]
        require(len(set(hashes)) == 1, f"Agent/Runtime client mismatch for {key}")
        require(hashes[0] == expected["files"].get(key), f"client hash changed for {key}")
        observed_files[key] = hashes[0]
    metadata = read_text(roots[0] / "contract_metadata.py")
    matches = {
        "contract_version": re.search(r"CONTRACT_VERSION = ['\"]([^'\"]+)", metadata),
        "protocol": re.search(r"PROTOCOL = ['\"]([^'\"]+)", metadata),
        "schema_digest": re.search(r"SCHEMA_DIGEST = ['\"]([^'\"]+)", metadata),
        "component_manifest_sha256": re.search(r"COMPONENT_MANIFEST_SHA256 = ['\"]([^'\"]+)", metadata),
    }
    require(all(matches.values()), "generated client metadata is incomplete")
    for key, match in matches.items():
        require(match.group(1) == expected[key], f"client {key} changed")
    observed_artifacts = {}
    for raw_path, expected_hash in expected["runtime_artifacts"].items():
        path = Path(raw_path)
        observed_artifacts[raw_path] = sha256(path)
        require(observed_artifacts[raw_path] == expected_hash, f"Runtime artifact hash changed: {path}")
    return {"files": observed_files, "runtime_artifacts": observed_artifacts, **{key: match.group(1) for key, match in matches.items()}}


def client_snapshot(base: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base["client_contract"])
    value["source_roots"] = list(CLIENT_ROOTS)
    value["files"] = {}
    for relative in CLIENT_FILES:
        key = f"astrid_runtime_client/{relative}"
        paths = [Path(root) / relative for root in CLIENT_ROOTS]
        require(all(path.is_file() and not path.is_symlink() for path in paths), f"missing client source for {key}")
        hashes = [sha256(path) for path in paths]
        require(len(set(hashes)) == 1, f"Agent/Runtime client mismatch for {key}")
        value["files"][key] = hashes[0]
    metadata = read_text(Path(CLIENT_ROOTS[0]) / "contract_metadata.py")
    for key, pattern in {
        "contract_version": r"CONTRACT_VERSION = ['\"]([^'\"]+)",
        "protocol": r"PROTOCOL = ['\"]([^'\"]+)",
        "schema_digest": r"SCHEMA_DIGEST = ['\"]([^'\"]+)",
        "component_manifest_sha256": r"COMPONENT_MANIFEST_SHA256 = ['\"]([^'\"]+)",
    }.items():
        match = re.search(pattern, metadata)
        require(match is not None, f"generated client metadata is missing {key}")
        value[key] = match.group(1)
    value["runtime_artifacts"] = {path: sha256(Path(path)) for path in RUNTIME_ARTIFACTS}
    return value


def check_remotion(recipe: dict[str, Any]) -> dict[str, Any]:
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
        require(read_text(bench / marker).strip() == value, f"Remotion marker changed: {marker}")
    current_tree = git(CHECKOUTS["agent"], "rev-parse", "HEAD:remotion")
    require(current_tree == expected["current_agent_remotion_tree"], "current Agent Remotion tree changed")
    require(sha256(REMOTION_ROOT / "package.json") == expected["package_sha256"], "current Remotion package changed")
    require(sha256(REMOTION_ROOT / "package-lock.json") == expected["package_lock_sha256"], "current Remotion lock changed")
    return {"bench": str(bench), "source_commit_marker": expected["historical_source_commit_marker"], "current_agent_remotion_tree": current_tree}


def remotion_snapshot(base: dict[str, Any], agent: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base["remotion"])
    bench = Path(value["bench"])
    value["current_agent_remotion_tree"] = agent["remotion_tree"]
    value["package_sha256"] = sha256(REMOTION_ROOT / "package.json")
    value["package_lock_sha256"] = sha256(REMOTION_ROOT / "package-lock.json")
    for marker, key in {
        ".astrid-agent-source-commit": "historical_source_commit_marker",
        ".astrid-component-identity": "component_identity",
        ".astrid-artifact-integrity": "artifact_integrity",
        ".astrid-installed-module-origins": "installed_module_origins",
        ".astrid-node-modules-lock-sha256": "node_modules_lock_sha256",
        ".astrid-node-version": "node",
        ".astrid-npm-version": "npm",
    }.items():
        value[key] = read_text(bench / marker).strip()
    return value


def check_graph(recipe: dict[str, Any]) -> dict[str, Any]:
    expected = recipe["composition"]
    artifact = Path(expected["artifact"])
    graph = Path(expected["qualified_graph"])
    require(sha256(artifact) == expected["artifact_sha256"], f"Composition artifact changed: {artifact}")
    package = graph / "@banodoco" / "timeline-composition" / "package.json"
    require(package.is_file() and not package.is_symlink(), f"Composition graph package missing: {package}")
    package_data = json.loads(read_text(package))
    require(package_data.get("name") == expected["package"], "Composition package name changed")
    require(package_data.get("version") == expected["version"], "Composition package version changed")
    files = {str(path.relative_to(graph)): sha256(path) for path in graph.rglob("*") if path.is_file() and not path.is_symlink()}
    require(len(files) == expected["file_count"], "Composition graph file count changed")
    actual_map = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(actual_map == expected["file_map_sha256"], "Composition graph file map changed")
    return {"file_count": len(files), "file_map_sha256": actual_map}


def graph_snapshot(base: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base["composition"])
    artifact = Path(value["artifact"])
    graph = Path(value["qualified_graph"])
    value["artifact_sha256"] = sha256(artifact)
    package_data = json.loads(read_text(graph / "@banodoco" / "timeline-composition" / "package.json"))
    value["package"] = package_data["name"]
    value["version"] = package_data["version"]
    files = {str(path.relative_to(graph)): sha256(path) for path in graph.rglob("*") if path.is_file() and not path.is_symlink()}
    value["file_count"] = len(files)
    value["file_map_sha256"] = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return value


def environment_snapshot() -> dict[str, str]:
    values = {"file": str(ENVIRONMENT_FILE)}
    for line in read_text(ENVIRONMENT_FILE).splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            if key in {"ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH"}:
                values[key] = value
    required = {"file", "ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH"}
    require(set(values) == required, "existing Remotion environment inputs are incomplete")
    return values


def runtime_bindings(runtime_head: str) -> dict[str, Any]:
    result: dict[str, Any] = {"runtime_producer": runtime_head, "consumers": {}}
    producer_files: dict[str, str] = {}
    for role, count in RUNTIME_LOCKS.items():
        root = Path(CHECKOUTS[role])
        lock_path = root / "runtime.lock.json"
        lock = json.loads(read_text(lock_path))
        files = lock.get("files")
        require(lock.get("source_commit") == runtime_head and isinstance(files, dict) and len(files) == count,
                f"{role} Runtime lock is not the current producer mapping")
        mappings = {}
        for destination, entry in files.items():
            require(isinstance(entry, dict) and isinstance(entry.get("from"), str), f"invalid {role} Runtime mapping")
            digest = entry.get("sha256", "")
            require(re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is not None, f"invalid {role} Runtime digest")
            require(sha256(root / destination) == digest[7:], f"{role} consumer hash mismatch: {destination}")
            source = entry["from"]
            producer = subprocess.run(["git", "-C", CHECKOUTS["runtime"], "show", f"{runtime_head}:{source}"],
                                      capture_output=True, check=False)
            require(producer.returncode == 0, f"Runtime producer blob unavailable: {source}")
            producer_hash = hashlib.sha256(producer.stdout).hexdigest()
            require(producer_hash == digest[7:], f"Runtime producer mismatch: {role} {source}")
            producer_files[source] = producer_hash
            mappings[destination] = {"from": source, "sha256": producer_hash}
        result["consumers"][role] = {"file_count": len(files), "lock_sha256": sha256(lock_path), "mappings": mappings}
    result["producer_files"] = producer_files
    return result


def check_runtime_bindings(recipe: dict[str, Any]) -> dict[str, Any]:
    expected = recipe.get("runtime_bindings")
    require(isinstance(expected, dict), "Runtime blob mapping snapshot is missing")
    observed = runtime_bindings(recipe["source"]["runtime"]["head"])
    require(observed == expected, "Runtime blob mapping snapshot changed")
    return observed


def canonical_recipe(recipe: dict[str, Any]) -> bytes:
    value = deepcopy(recipe)
    value.pop("_authenticated_snapshot", None)
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def authenticate_current(recipe: dict[str, Any]) -> dict[str, Any]:
    before = current_sources()
    for name, source in before.items():
        source_tuple(source["checkout"], name, recipe["source"][name])
    probes = {role: check_probe(recipe, role, *IMPORT_PROBES[role]) for role in IMPORT_PROBES}
    client = check_client(recipe)
    remotion = check_remotion(recipe)
    graph = check_graph(recipe)
    bindings = check_runtime_bindings(recipe)
    after = current_sources()
    require(before == after, "source tuple moved during qualification; refuse concurrent facts")
    return {
        **deepcopy(recipe),
        "_authenticated_snapshot": {
            "digest": hashlib.sha256(canonical_recipe(recipe)).hexdigest(),
            "source": before,
            "checks": {"probes": probes, "client": client, "remotion": remotion, "composition": graph,
                        "runtime_bindings": bindings},
        },
    }


def build_recipe(base: dict[str, Any]) -> dict[str, Any]:
    before = current_sources()
    value = deepcopy(base)
    value["qualified_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    value["source"] = before
    value["interpreters"] = interpreter_snapshot(base)
    value["client_contract"] = client_snapshot(base)
    value["remotion"] = remotion_snapshot(base, before["agent"])
    value["composition"] = graph_snapshot(base)
    value["environment"] = environment_snapshot()
    value["runtime_bindings"] = runtime_bindings(before["runtime"]["head"])
    authenticated = authenticate_current(value)
    after = current_sources()
    require(before == after, "source tuple moved while refreshing; refuse concurrent facts")
    return authenticated


def strip_authentication(recipe: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(recipe)
    value.pop("_authenticated_snapshot", None)
    return value


def refresh() -> dict[str, Any]:
    base = json.loads(read_text(RECIPE_PATH))
    value = strip_authentication(build_recipe(base))
    temporary = RECIPE_PATH.with_name(f".{RECIPE_PATH.name}.refreshing")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    os.replace(temporary, RECIPE_PATH)
    return value


def main() -> int:
    refresh_requested = "--refresh" in sys.argv[1:]
    recipe = refresh() if refresh_requested else json.loads(read_text(RECIPE_PATH))
    authenticated = authenticate_current(recipe)
    print(json.dumps({
        "status": "REFRESHED" if refresh_requested else "PASS",
        "source": authenticated["source"],
        "runtime_bindings": authenticated["_authenticated_snapshot"]["checks"]["runtime_bindings"],
        "probes": authenticated["_authenticated_snapshot"]["checks"]["probes"],
        "service_execution": "not run",
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"current-service-inputs: REFUSED: {exc}", file=sys.stderr)
        raise SystemExit(1)
