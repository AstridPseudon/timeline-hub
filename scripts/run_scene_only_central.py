#!/usr/bin/env python3
"""Run the bounded prepared-Root scene qualification in a clean snapshot.

The central test service invokes this file from its snapshot checkout.  The
runner owns the temporary Runtime and Remotion roots, while the repaired peer
graph, pinned Node, and Composition archive remain read-only inputs.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
from pathlib import Path

RUNTIME_PIN = Path("/home/user/work/wt/rt-pin-2c4ac180")
RUNTIME_SHA = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
NODE_PIN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node"
)
PEERS = Path("/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules")
READY_MANIFEST = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/design/handoff-vw-m3-repaired-graphs-ready-fingerprints-"
    "scene-physical-manifest.json"
)
NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
PUBLIC12_SHA256 = "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
PUBLIC12_FILES = 77
READY_GRAPH_ENTRIES = 21495
PUBLIC12_NAME = "banodoco-timeline-composition-0.0.12.tgz"

SCOPED_PEERS = {
    "react": {
        "version": "18.3.1",
        "files": 20,
        "tree": "2f56e0708f2b43ad352087679b7b728e13d873197949013aa1d3362cd19dcb07",
        "manifest": "d4e68a5c96babb20cad1daafea8b78822eae45b341552cf5418d06a5304fa64c",
    },
    "react-dom": {
        "version": "18.3.1",
        "files": 32,
        "tree": "9ca1761200e64fb5671d26f2772453571bafc53eda3e3b66fe83bf35c0cd97c2",
        "manifest": "d2f29e31bd48b833e48cd7bbf41f192e8ee4ff8da249fdbe10d4ac4114b8b12e",
    },
    "remotion": {
        "version": "4.0.509",
        "files": 400,
        "tree": "20c668f523ff2a89a7ab2f40fbf767d5b49b9ef8a4aafb264ae7086de477812f",
        "manifest": "1260b76eb109b0ebfff6cfb57f0e2b9b5fc8c6511f18bd43b047bddca068bd01",
    },
    "@remotion/media": {
        "version": "4.0.509",
        "files": 66,
        "tree": "5c6498f88c1aa1a2fdff1f8cc9732830354019f9efa9522dd1a86dee2ec390a8",
        "manifest": "59e90c2e2d182faf420dd8b9461a74bedd21d6680a627ea6f2fb66c4efb9ee95",
    },
    "@remotion/player": {
        "version": "4.0.509",
        "files": 108,
        "tree": "6de5135118e232772317773a1ec65eca97ed25d74e231a521e55ca73568493d7",
        "manifest": "89595cb2ec1e0231f576cf32408e81aa3dab522ebe0c2154dc4adb41746f7abf",
    },
    "@remotion/layout-utils": {
        "version": "4.0.509",
        "files": 13,
        "tree": "76a94579d6f198109e5f2b35ee9ae3e44ff6cb2505b20532281979acd059581a",
        "manifest": "244521ec2c97085930463bd476366cdf7f6392793a57d787b6f0576dbdeaafda",
    },
}

TESTS = (
    "tests/packs/rendering/test_scene_answers.py::"
    "test_prepared_host_query_replaces_named_occluder_semantic_presence_positive",
    "tests/packs/rendering/test_scene_answers.py::"
    "test_prepared_host_query_refuses_missing_or_stale_source_pair_and_cleans",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_path(path: Path, *, directory: bool = False) -> Path:
    resolved = path.resolve(strict=False)
    if directory:
        valid = resolved.is_dir()
    else:
        valid = resolved.is_file()
    if not valid:
        kind = "directory" if directory else "file"
        raise RuntimeError(f"required {kind} is unavailable: {path} -> {resolved}")
    return resolved


def _assert_private(path: Path, *shared: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"private path is a symlink: {path}")
    resolved = path.resolve(strict=False)
    for shared_path in shared:
        shared_resolved = shared_path.resolve(strict=False)
        if resolved == shared_resolved or shared_resolved in resolved.parents:
            raise RuntimeError(f"private stage resolves into shared path: {resolved}")


def _git_sha(checkout: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _tree_fingerprint(root: Path) -> dict[str, object]:
    entries: list[list[str]] = []

    def visit(directory: Path, prefix: str = "") -> None:
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            relative = f"{prefix}{path.name}"
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                visit(path, f"{relative}/")
            elif stat.S_ISREG(mode):
                kind = "executable" if mode & 0o111 else "file"
                entries.append([relative, kind, _sha256_file(path)])
            elif stat.S_ISLNK(mode):
                target = path.resolve(strict=True)
                if not target.is_file() or not (target == root or root in target.parents):
                    raise RuntimeError(f"dependency link escapes private graph: {path}")
                entries.append([relative, "symlink", _sha256_bytes(os.readlink(path).encode())])
            else:
                raise RuntimeError(f"unsupported dependency entry: {path}")

    visit(root)
    entries.sort(key=lambda row: row[0])
    return {
        "sha256": _sha256_bytes(json.dumps(entries, separators=(",", ":")).encode()),
        "fileCount": len(entries),
    }


def _physical_manifest(root: Path) -> dict[str, tuple[object, ...]]:
    result: dict[str, tuple[object, ...]] = {}

    def visit(directory: Path, prefix: str = "") -> None:
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            relative = f"{prefix}{path.name}"
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", stat.S_IMODE(mode))
                visit(path, f"{relative}/")
            elif stat.S_ISREG(mode):
                kind = "executable" if mode & 0o111 else "file"
                result[relative] = (kind, stat.S_IMODE(mode), _sha256_file(path))
            elif stat.S_ISLNK(mode):
                target = path.resolve(strict=True)
                if not target.is_file() or not (target == root or root in target.parents):
                    raise RuntimeError(f"dependency link escapes graph: {path}")
                link = os.readlink(path)
                result[relative] = (
                    "symlink", stat.S_IMODE(mode), link, _sha256_bytes(link.encode())
                )
            else:
                raise RuntimeError(f"unsupported dependency entry: {path}")

    visit(root)
    return result


def _ready_graph_fingerprint(root: Path) -> dict[str, object]:
    manifest = json.loads(READY_MANIFEST.read_text(encoding="utf-8"))
    expected: dict[str, tuple[object, ...]] = {}
    for entry in manifest["entries"]:
        kind = entry["kind"]
        if kind == "directory":
            expected[entry["path"]] = (kind, entry["mode"] & 0o7777)
        elif kind == "symlink":
            expected[entry["path"]] = (
                kind, entry["mode"] & 0o7777, entry["target"], entry["sha256"]
            )
        else:
            expected[entry["path"]] = (
                kind, entry["mode"] & 0o7777, entry["sha256"]
            )
    actual = _physical_manifest(root)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))[:3]
        added = sorted(set(actual) - set(expected))[:3]
        changed = sorted(path for path in set(actual) & set(expected)
                         if actual[path] != expected[path])[:3]
        raise RuntimeError(
            f"repaired peer graph differs: missing={missing} changed={changed} added={added}"
        )
    files = sum(1 for value in actual.values() if value[0] in {"file", "executable"})
    links = sum(1 for value in actual.values() if value[0] == "symlink")
    # The repaired-graph handoff's entry count includes symlink leaves twice:
    # once as files through stat() and once as links through lstat().
    graph_entries = files + (2 * links)
    if graph_entries != READY_GRAPH_ENTRIES:
        raise RuntimeError(f"unexpected repaired peer graph entries: {graph_entries}")
    return {
        "manifest_entries": len(actual),
        "graph_entries": graph_entries,
        "repair_delta": {"missing": 0, "changed": 0, "added": 0},
        "tree": _tree_fingerprint(root),
        "scope6": _scoped_fingerprints(root),
    }


def _scoped_fingerprints(root: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for name, expected in SCOPED_PEERS.items():
        package = root / name
        if package.is_symlink() or not package.is_dir():
            raise RuntimeError(f"scope package is not a real directory: {name}")
        metadata_path = package / "package.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        fingerprint = {
            "version": metadata.get("version"),
            "tree": _tree_fingerprint(package),
            "manifest": _sha256_file(metadata_path),
        }
        if fingerprint["version"] != expected["version"]:
            raise RuntimeError(f"unexpected {name} version: {fingerprint['version']}")
        if fingerprint["tree"] != {"sha256": expected["tree"], "fileCount": expected["files"]}:
            raise RuntimeError(f"unexpected {name} scoped tree")
        if fingerprint["manifest"] != expected["manifest"]:
            raise RuntimeError(f"unexpected {name} package manifest")
        result[name] = fingerprint
    return result


def _copy_runtime(destination: Path) -> None:
    _assert_private(destination, RUNTIME_PIN, PEERS)
    shutil.copytree(
        RUNTIME_PIN,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        symlinks=False,
    )


def _prepare_project(repo: Path, stage: Path) -> tuple[Path, dict[str, object]]:
    project = stage / "runtime" / "remotion"
    _assert_private(project, RUNTIME_PIN, PEERS)
    shutil.copytree(
        repo / "remotion",
        project,
        ignore=shutil.ignore_patterns("node_modules", ".pytest_cache"),
        symlinks=False,
    )
    modules = project / "node_modules"
    _assert_private(modules, RUNTIME_PIN, PEERS)
    shutil.copytree(PEERS, modules, symlinks=True)
    scope = modules / "@banodoco"
    if scope.is_symlink() or scope.is_file():
        scope.unlink()
    elif scope.exists():
        shutil.rmtree(scope)
    scope.mkdir()
    artifact = _require_path(repo / "remotion" / "artifacts" / PUBLIC12_NAME)
    if _sha256_file(artifact) != PUBLIC12_SHA256:
        raise RuntimeError("Composition public12 archive hash mismatch")
    extracted = stage / "public12-extracted"
    _assert_private(extracted, RUNTIME_PIN, PEERS)
    extracted.mkdir()
    with tarfile.open(artifact) as archive:
        archive.extractall(extracted, filter="data")
    package = extracted / "package"
    target = scope / "timeline-composition"
    package.rename(target)
    members = [path for path in target.rglob("*") if path.is_file()]
    if len(members) != PUBLIC12_FILES:
        raise RuntimeError(f"Composition public12 member count mismatch: {len(members)}")
    if _sha256_file(artifact) != PUBLIC12_SHA256:
        raise RuntimeError("Composition public12 archive changed")
    if modules.resolve() != modules:
        raise RuntimeError("private dependency root is not a real directory")
    for name in SCOPED_PEERS:
        if (modules / name).is_symlink():
            raise RuntimeError(f"private scope escaped through a directory link: {name}")
    return project, {
        "public12_files": len(members),
        "public12_sha256": PUBLIC12_SHA256,
        "private_graph": str(modules),
    }


def _environment(repo: Path, stage: Path, project: Path) -> dict[str, str]:
    runtime_source = stage / "runtime-source"
    _copy_runtime(runtime_source)
    source_link = project.parent / "astrid"
    _assert_private(source_link, RUNTIME_PIN, PEERS)
    source_link.symlink_to(repo / "astrid", target_is_directory=True)
    if source_link.resolve() != (repo / "astrid").resolve():
        raise RuntimeError("Runtime project did not retain the snapshot Agent source")
    python = Path(sys.executable)
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {
            "NODE_OPTIONS", "NODE_PATH", "PYTHONPATH", "PYTHONPYCACHEPREFIX",
            "ASTRID_PACKS_PATH",
        }
        and not key.startswith("GIT_")
    }
    environment.update(
        ASTRID_NODE_EXECUTABLE=str(NODE_PIN),
        ASTRID_REMOTION_PROJECT_DIR=str(project),
        ASTRID_RUNTIME_CHECKOUT=str(runtime_source),
        ASTRID_TEST_NODE_MODULES=str(project / "node_modules"),
        ASTRID_TIMELINE_SCHEMA_PYTHONPATH=sysconfig.get_paths()["purelib"],
        PATH=os.pathsep.join([str(NODE_PIN.parent), environment.get("PATH", "")]),
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONPATH=os.pathsep.join([str(repo), str(runtime_source)]),
    )
    if not python.exists():
        raise RuntimeError(f"venv Python is unavailable: {python}")
    return environment


def _node_preflight(environment: dict[str, str]) -> dict[str, str]:
    node = _require_path(NODE_PIN)
    if node.is_symlink() or not os.access(node, os.X_OK):
        raise RuntimeError(f"pinned Node is not a real executable: {node}")
    digest = _sha256_file(node)
    if digest != NODE_SHA256:
        raise RuntimeError(f"pinned Node hash mismatch: {digest}")
    version = subprocess.check_output([str(node), "--version"], text=True).strip()
    if version != "v20.19.4":
        raise RuntimeError(f"pinned Node version mismatch: {version}")
    found = Path(shutil.which("node", path=environment["PATH"]) or "")
    if found.resolve() != node.resolve():
        raise RuntimeError(f"PATH Node mismatch: {found} != {node}")
    return {"path": str(node), "sha256": digest, "version": version, "which": str(found)}


def _origins(environment: dict[str, str], repo: Path) -> dict[str, object]:
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
        [sys.executable, "-B", "-c", probe],
        cwd=repo,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _run(repo: Path, *, preflight_only: bool) -> int:
    stage = Path(tempfile.mkdtemp(prefix=".scene-only-central-", dir=repo))
    _assert_private(stage, RUNTIME_PIN, PEERS)
    python = Path(sys.executable)
    completed: subprocess.CompletedProcess[str] | None = None
    try:
        _require_path(RUNTIME_PIN, directory=True)
        _require_path(PEERS, directory=True)
        _require_path(READY_MANIFEST)
        if _git_sha(RUNTIME_PIN) != RUNTIME_SHA:
            raise RuntimeError("Runtime source pin mismatch")
        graph = _ready_graph_fingerprint(PEERS)
        project, composition = _prepare_project(repo, stage)
        environment = _environment(repo, stage, project)
        preflight = {
            "phase": "preflight",
            "agent_root": str(repo / "astrid"),
            "runtime_source": str((stage / "runtime-source").resolve()),
            "project": str(project.resolve()),
            "runtime_sha": RUNTIME_SHA,
            "node": _node_preflight(environment),
            "graph": graph,
            "composition": composition,
            "origins": _origins(environment, repo),
        }
        print(json.dumps(preflight, sort_keys=True))
        if preflight_only:
            return 0
        command = [
            str(python), "-B", "-m", "pytest", "-q", "-o", "addopts=",
            "-p", "no:cacheprovider", "--tb=short",
            f"--basetemp={stage / 'pytest-central'}", *TESTS,
        ]
        completed = subprocess.run(command, cwd=repo, env=environment, check=False)
        post_graph = _ready_graph_fingerprint(PEERS)
        post_origins = _origins(environment, repo)
        if post_graph != graph:
            raise RuntimeError("repaired peer graph changed during tests")
        print(json.dumps({
            "phase": "postflight",
            "pytest_returncode": completed.returncode,
            "selected_tests": list(TESTS),
            "graph": post_graph,
            "origins": post_origins,
            "composition": composition,
        }, sort_keys=True))
        return completed.returncode
    finally:
        if stage.exists() or stage.is_symlink():
            if stage.is_symlink():
                raise RuntimeError(f"refusing to remove symlink stage: {stage}")
            shutil.rmtree(stage)
        print(json.dumps({"phase": "cleanup", "stage_removed": not stage.exists()}, sort_keys=True))


def main() -> int:
    repo = Path.cwd()
    if not (repo / "astrid").is_dir() or not (repo / "tests").is_dir():
        raise SystemExit(f"run this wrapper from an Agent snapshot root: {repo}")
    return _run(repo, preflight_only="--preflight" in sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
