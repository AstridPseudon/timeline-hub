#!/usr/bin/env python3
"""Run the scene-only Runtime lane from a clean, snapshot-local source graph.

This is a test harness, not a product entry point.  The central test service
executes it with its snapshot checkout as the current directory, so every
source path used by the child process is derived from that snapshot rather
than from a recycled worker worktree.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

RUNTIME_PIN = Path("/home/user/work/wt/rt-pin-2c4ac180")
RUNTIME_SHA = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
NODE_PIN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node"
)
PEERS = Path("/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules")
NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
PUBLIC12_SHA256 = "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
PUBLIC12_FILES = 77
PUBLIC12_NAME = "banodoco-timeline-composition-0.0.12.tgz"


def _require_path(path: Path, *, directory: bool = False) -> Path:
    resolved = path.resolve(strict=False)
    if (resolved.is_dir() if directory else resolved.is_file()) is False:
        kind = "directory" if directory else "file"
        raise RuntimeError(f"required {kind} is unavailable: {path} -> {resolved}")
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_private(path: Path, *shared: Path) -> None:
    resolved = path.resolve(strict=False)
    for shared_path in shared:
        shared_resolved = shared_path.resolve(strict=False)
        if resolved == shared_resolved or shared_resolved in resolved.parents:
            raise RuntimeError(f"private stage resolves into shared path: {resolved}")


def _copy_runtime(runtime_source: Path, runtime_pin: Path) -> None:
    shutil.copytree(
        runtime_pin,
        runtime_source,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        symlinks=False,
    )


def _link_peer_graph(project: Path, peers: Path, artifact: Path) -> tuple[int, str]:
    modules = project / "node_modules"
    modules.mkdir()
    for entry in os.scandir(peers):
        source = Path(entry.path)
        if source.name == "@banodoco":
            continue
        target = modules / source.name
        target.symlink_to(source.resolve(), target_is_directory=source.is_dir())

    scope = modules / "@banodoco"
    scope.mkdir()
    extracted = project.parent / "public12-extracted"
    extracted.mkdir()
    with tarfile.open(artifact) as archive:
        archive.extractall(extracted, filter="data")
    package = extracted / "package"
    target = scope / "timeline-composition"
    package.rename(target)
    files = [path for path in target.rglob("*") if path.is_file()]
    return len(files), _sha256(artifact)


def _environment(repo: Path, stage: Path) -> tuple[dict[str, str], dict[str, Path | str]]:
    agent_root = _require_path(repo / "astrid", directory=True)
    runtime_pin = _require_path(RUNTIME_PIN, directory=True)
    _assert_private(stage, runtime_pin, PEERS)
    _require_path(runtime_pin / "astrid_runtime", directory=True)
    _require_path(runtime_pin / "runtime_protocol", directory=True)
    node = _require_path(NODE_PIN)
    if _sha256(node) != NODE_SHA256:
        raise RuntimeError(f"Node hash mismatch: {node}")
    node_version = subprocess.check_output([str(node), "--version"], text=True).strip()
    if node_version != "v20.19.4":
        raise RuntimeError(f"Node pin mismatch: {node} reports {node_version}")
    peers = _require_path(PEERS, directory=True)
    _require_path(peers / "esbuild", directory=True)
    artifact = _require_path(repo / "remotion" / "artifacts" / PUBLIC12_NAME)
    if _sha256(artifact) != PUBLIC12_SHA256:
        raise RuntimeError(f"public12 artifact hash mismatch: {artifact}")

    runtime_source = stage / "runtime-source"
    _copy_runtime(runtime_source, runtime_pin)
    project = stage / "runtime" / "remotion"
    shutil.copytree(
        repo / "remotion",
        project,
        ignore=shutil.ignore_patterns("node_modules", ".pytest_cache"),
        symlinks=False,
    )
    public12_files, public12_sha256 = _link_peer_graph(project, peers, artifact)
    if (public12_files, public12_sha256) != (PUBLIC12_FILES, PUBLIC12_SHA256):
        raise RuntimeError("public12 package verification failed")

    # Keep the compatibility leaf inside the owned stage tied to this exact
    # central snapshot.  No stale worker path or installed Agent is consulted.
    runtime_agent = stage / "runtime" / "astrid"
    runtime_agent.symlink_to(agent_root, target_is_directory=True)
    if runtime_agent.resolve() != agent_root:
        raise RuntimeError("runtime/astrid does not resolve to the snapshot Agent")

    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"NODE_OPTIONS", "NODE_PATH", "PYTHONPATH", "PYTHONPYCACHEPREFIX"}
        and not key.startswith("GIT_")
    }
    pythonpath = [repo, runtime_source]
    environment.update(
        ASTRID_NODE_EXECUTABLE=str(node),
        ASTRID_REMOTION_PROJECT_DIR=str(project),
        ASTRID_RUNTIME_CHECKOUT=str(runtime_source),
        ASTRID_TEST_NODE_MODULES=str(peers),
        ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(Path(sysconfig_path())),
        PATH=os.pathsep.join([str(node.parent), environment.get("PATH", "")]),
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONPATH=os.pathsep.join(str(path) for path in pythonpath),
    )
    values = {
        "agent_root": str(agent_root),
        "runtime_source": str(runtime_source.resolve()),
        "project": str(project.resolve()),
        "node": str(node.resolve()),
        "peers": str(peers),
        "public12_files": public12_files,
        "public12_sha256": public12_sha256,
        "node_sha256": NODE_SHA256,
        "runtime_sha": _git_sha(runtime_pin),
    }
    if values["runtime_sha"] != RUNTIME_SHA:
        raise RuntimeError(f"Runtime pin mismatch: {values['runtime_sha']}")
    return environment, values


def sysconfig_path() -> str:
    # Keep the schema helper on the shared venv; it is a dependency, not a
    # source root.  sysconfig is deliberately imported lazily for this path.
    import sysconfig

    return sysconfig.get_paths()["purelib"]


def _git_sha(checkout: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"could not identify Runtime checkout: {checkout}")
    return result.stdout.strip()


def _origins(environment: dict[str, str], python: Path) -> dict[str, object]:
    probe = """
import importlib.util, json, os
from pathlib import Path
names = ("astrid", "runtime_protocol", "astrid_runtime")
origins = {}
for name in names:
    spec = importlib.util.find_spec(name)
    if spec is None or not spec.origin:
        raise SystemExit(f"missing import origin: {name}")
    origins[name] = str(Path(spec.origin).resolve())
roots = [Path(item).resolve() for item in os.environ["PYTHONPATH"].split(os.pathsep)]
for name, origin in origins.items():
    path = Path(origin)
    if not any(path == root or root in path.parents for root in roots):
        raise SystemExit(f"installed-source shortcut: {name}={origin}")
print(json.dumps({"origins": origins, "pythonpath": [str(root) for root in roots]}, sort_keys=True))
"""
    result = subprocess.run(
        [str(python), "-B", "-c", probe],
        cwd=environment["PYTHONPATH"].split(os.pathsep)[0],
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _run(repo: Path, *, preflight_only: bool) -> int:
    stage = Path(tempfile.mkdtemp(prefix=".scene-only-central-", dir=repo))
    python = Path(sys.executable).resolve()
    environment: dict[str, str] | None = None
    try:
        environment, values = _environment(repo, stage)
        preflight = {"phase": "preflight", **values, **_origins(environment, python)}
        print(json.dumps(preflight, sort_keys=True))
        if preflight_only:
            return 0
        command = [
            str(python),
            "-B",
            "-m",
            "pytest",
            "-q",
            "-o",
            "addopts=",
            "-p",
            "no:cacheprovider",
            "--tb=short",
            f"--basetemp={stage / 'pytest-central'}",
            "tests/packs/rendering/test_live_source_label_native.py",
        ]
        completed = subprocess.run(command, cwd=repo, env=environment, check=False)
        postflight = {"phase": "postflight", **values, **_origins(environment, python)}
        print(json.dumps({"pytest_returncode": completed.returncode, **postflight}, sort_keys=True))
        return completed.returncode
    finally:
        shutil.rmtree(stage, ignore_errors=False)
        print(json.dumps({"phase": "cleanup", "stage_removed": not stage.exists()}, sort_keys=True))


def main() -> int:
    repo = Path.cwd().resolve()
    if not (repo / "astrid").is_dir() or not (repo / "tests").is_dir():
        raise SystemExit(f"run this wrapper from an Agent snapshot root: {repo}")
    return _run(repo, preflight_only="--preflight" in sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
