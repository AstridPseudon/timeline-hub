"""Run the three-case D1 scene qualification against the admitted f816 graph."""

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
PEERS = Path("/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules")
GRAPH_MANIFEST = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/design/handoff-vw-m3-main-cap-controller-final-gate-graph-pre.json"
)
NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
GRAPH_REVISION = "f8164bef73215272562c4d6974acadbd82c2898a"
GRAPH_ENTRIES = 21488
GRAPH_SHA256 = "9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425"
PUBLIC12_NAME = "banodoco-timeline-composition-0.0.12.tgz"
PUBLIC12_SHA256 = "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
PUBLIC12_FILES = 77
SIX_PEERS = {
    "@remotion/player/dist/cjs/PlayerUI.js": "5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb",
    "@remotion/player/dist/cjs/use-playback.js": "6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0",
    "@remotion/player/dist/cjs/use-player-methods.js": "ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46",
    "@remotion/player/dist/esm/index.mjs": "d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12",
    "remotion/dist/cjs/audio/shared-audio-tags.js": "471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c",
    "remotion/dist/esm/index.mjs": "9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8",
}
TESTS = (
    "tests/packs/rendering/test_scene_answers.py::"
    "test_prepared_host_query_replaces_named_occluder_semantic_presence_positive",
    "tests/packs/rendering/test_scene_answers.py::"
    "test_prepared_host_query_refuses_missing_or_stale_source_pair_and_cleans",
)


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _graph_state(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}

    def walk(directory: Path, ancestors: set[Path]) -> None:
        real = directory.resolve(strict=True)
        if real in ancestors:
            raise RuntimeError(f"recursive dependency link: {directory}")
        for path in sorted(directory.iterdir()):
            key = str(path.relative_to(root))
            if path.is_symlink():
                result[key + "@link"] = os.readlink(path)
            if path.is_dir():
                walk(path, ancestors | {real})
            elif path.is_file():
                result[key] = _digest(path)
            else:
                raise RuntimeError(f"non-regular graph entry: {path}")

    walk(root, set())
    return result


def _admit_graph() -> dict[str, object]:
    if not PEERS.is_dir() or PEERS.is_symlink() or PEERS.resolve() != PEERS:
        raise RuntimeError(f"peer graph is not the expected real directory: {PEERS}")
    manifest = json.loads(GRAPH_MANIFEST.read_text(encoding="utf-8"))
    current = _graph_state(PEERS)
    expected = {str(key): value for key, value in manifest.items()}
    if current != expected:
        missing = sorted(set(expected) - set(current))[:3]
        added = sorted(set(current) - set(expected))[:3]
        changed = sorted(key for key in set(current) & set(expected)
                         if current[key] != expected[key])[:3]
        raise RuntimeError(f"f816 graph mismatch: missing={missing} changed={changed} added={added}")
    canonical = hashlib.sha256(
        json.dumps(current, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    revision = subprocess.check_output(
        ["git", "-C", str(PEERS.parent.parent), "rev-parse", "HEAD"], text=True
    ).strip()
    six = {name: _digest(PEERS / name) for name in SIX_PEERS}
    if len(current) != GRAPH_ENTRIES or canonical != GRAPH_SHA256:
        raise RuntimeError(f"unexpected f816 graph identity: {len(current)} / {canonical}")
    if revision != GRAPH_REVISION:
        raise RuntimeError(f"unexpected peer checkout: {revision}")
    if six != SIX_PEERS:
        raise RuntimeError("f816 six-peer hashes changed")
    return {"entries": len(current), "sha256": canonical, "revision": revision, "six_peers": six}


def _admit_node() -> dict[str, str]:
    if NODE_PIN.is_symlink() or not NODE_PIN.is_file() or not os.access(NODE_PIN, os.X_OK):
        raise RuntimeError(f"pinned Node is not a real executable: {NODE_PIN}")
    digest = _digest(NODE_PIN)
    version = subprocess.check_output([str(NODE_PIN), "--version"], text=True).strip()
    if digest != NODE_SHA256 or version != "v20.19.4":
        raise RuntimeError(f"unexpected Node: {version} / {digest}")
    return {"path": str(NODE_PIN), "sha256": digest, "version": version}


def _admit_artifact(repo: Path) -> tuple[Path, dict[str, str]]:
    artifact = repo / "remotion" / "artifacts" / PUBLIC12_NAME
    if _digest(artifact) != PUBLIC12_SHA256:
        raise RuntimeError("Composition public12 archive hash mismatch")
    with tarfile.open(artifact) as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        if len(members) != PUBLIC12_FILES:
            raise RuntimeError(f"unexpected public12 member count: {len(members)}")
        files = {
            member.name.removeprefix("package/"): _digest_stream(archive.extractfile(member))
            for member in members
        }
    return artifact, files


def _digest_stream(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def _leaf_link(source: Path, destination: Path) -> None:
    if source.is_symlink():
        source = source.resolve(strict=True)
    if destination.exists() or destination.is_symlink():
        raise RuntimeError(f"private dependency target already exists: {destination}")
    destination.symlink_to(source)


def _build_private_project(repo: Path, stage: Path, artifact: Path) -> tuple[Path, dict[str, object]]:
    project = stage / "runtime" / "remotion"
    shutil.copytree(
        repo / "remotion", project,
        ignore=shutil.ignore_patterns("node_modules", ".pytest_cache"),
        symlinks=False,
    )
    modules = project / "node_modules"
    modules.mkdir()
    for entry in sorted(PEERS.iterdir()):
        target = modules / entry.name
        if entry.name.startswith("@"):
            target.mkdir()
            for child in sorted(entry.iterdir()):
                if entry.name == "@banodoco" and child.name == "timeline-composition":
                    continue
                _leaf_link(child.resolve(strict=True), target / child.name)
        else:
            _leaf_link(entry.resolve(strict=True), target)
    extracted = stage / "public12-extracted"
    extracted.mkdir()
    with tarfile.open(artifact) as archive:
        for member in archive.getmembers():
            if member.name == "package" or not member.name.startswith("package/"):
                continue
            relative = Path(member.name.removeprefix("package/"))
            destination = extracted / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if member.isfile():
                destination.write_bytes(archive.extractfile(member).read())
    package = modules / "@banodoco" / "timeline-composition"
    package.mkdir()
    for source in sorted(extracted.rglob("*")):
        destination = package / source.relative_to(extracted)
        if source.is_dir():
            destination.mkdir(exist_ok=True)
        elif source.is_file():
            shutil.copy2(source, destination)
    members = {str(path.relative_to(package)): _digest(path) for path in package.rglob("*") if path.is_file()}
    if members != _artifact_members(artifact):
        raise RuntimeError("private public12 package differs from admitted archive")
    if modules.resolve() != modules:
        raise RuntimeError("private dependency root is not real")
    return project, {"private_graph": str(modules), "public12_files": len(members), "public12_sha256": _digest(artifact)}


def _artifact_members(artifact: Path) -> dict[str, str]:
    with tarfile.open(artifact) as archive:
        return {
            member.name.removeprefix("package/"): _digest_stream(archive.extractfile(member))
            for member in archive.getmembers() if member.isfile()
        }


def _environment(repo: Path, stage: Path, project: Path) -> dict[str, str]:
    runtime_source = stage / "runtime-source"
    shutil.copytree(
        RUNTIME_PIN, runtime_source,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        symlinks=False,
    )
    source_link = project.parent / "astrid"
    source_link.symlink_to(repo / "astrid", target_is_directory=True)
    environment = {
        key: value for key, value in os.environ.items()
        if key not in {"NODE_OPTIONS", "NODE_PATH", "PYTHONPATH", "PYTHONPYCACHEPREFIX", "ASTRID_PACKS_PATH"}
        and not key.startswith("GIT_")
    }
    environment.update(
        ASTRID_NODE_EXECUTABLE=str(NODE_PIN),
        ASTRID_REMOTION_PROJECT_DIR=str(project),
        ASTRID_RUNTIME_CHECKOUT=str(runtime_source),
        ASTRID_TEST_NODE_MODULES=str(project / "node_modules"),
        ASTRID_TIMELINE_SCHEMA_PYTHONPATH=sysconfig.get_paths()["purelib"],
        PATH=os.pathsep.join((str(NODE_PIN.parent), environment.get("PATH", ""))),
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONPATH=os.pathsep.join((str(repo), str(runtime_source))),
    )
    return environment


def main() -> int:
    repo = Path.cwd().resolve()
    graph = _admit_graph()
    node = _admit_node()
    if subprocess.check_output(["git", "-C", str(RUNTIME_PIN), "rev-parse", "HEAD"], text=True).strip() != RUNTIME_SHA:
        raise RuntimeError("Runtime source pin mismatch")
    artifact, artifact_members = _admit_artifact(repo)
    stage = Path(tempfile.mkdtemp(prefix=".scene-only-central-", dir=repo))
    try:
        project, composition = _build_private_project(repo, stage, artifact)
        environment = _environment(repo, stage, project)
        found = Path(shutil.which("node", path=environment["PATH"]) or "").resolve()
        if found != NODE_PIN.resolve():
            raise RuntimeError(f"PATH Node mismatch: {found}")
        print(json.dumps({
            "phase": "preflight", "runtime_sha": RUNTIME_SHA, "node": node,
            "graph": graph, "composition": composition,
            "artifact_members": len(artifact_members), "selected_tests": list(TESTS),
        }, sort_keys=True))
        if "--preflight" in sys.argv[1:]:
            return 0
        command = [
            sys.executable, "-B", "-m", "pytest", "-q", "-o", "addopts=",
            "-p", "no:cacheprovider", "--tb=short", f"--basetemp={stage / 'pytest-central'}",
            *TESTS,
        ]
        result = subprocess.run(command, cwd=repo, env=environment, check=False)
        post_graph = _admit_graph()
        if post_graph != graph:
            raise RuntimeError("f816 graph changed during tests")
        print(json.dumps({
            "phase": "postflight", "pytest_returncode": result.returncode,
            "selected_tests": list(TESTS), "graph": post_graph,
        }, sort_keys=True))
        return result.returncode
    finally:
        if stage.is_symlink():
            raise RuntimeError(f"refusing to remove symlink stage: {stage}")
        shutil.rmtree(stage, ignore_errors=False)
        print(json.dumps({"phase": "cleanup", "stage_removed": not stage.exists()}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
