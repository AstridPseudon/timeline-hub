"""Offline cache-resolution gate for the native fresh-frame handoff.

This controller never launches the frame worker.  It proves the existing
shared-browser lookup with an owned HOME and records why the native worker's
no-argument lookup is not yet reachable on the reviewed source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
WORKER = "vw-m3-native-frame-existing-browser-cache"
WORK = ORCH / "workers" / WORKER
PREFIX = ORCH / "design" / f"handoff-{WORKER}"
BASE = "ed6b371e3acbb83ed990e36809a2bc2bd7916a46"
RUNTIME = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
PEERS = Path("/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules")
PEER_ROOT = PEERS.parent
PUBLIC_ARCHIVE = Path("remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz")
NODE_ARCHIVE = Path("/tmp/node-v20.19.4-linux-x64.tar.xz")
CHROME = Path("/opt/google/chrome/chrome")
PYTHON = Path("/home/user/work/venv-agent/bin/python")
REMOTION_VERSION = "4.0.509"
CHROME_SHA = "cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76"
CHROME_TREE_SHA = "5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e"
NODE_SHA = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
PUBLIC_SHA = "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
RUNTIME_ARCHIVE_SHA = "eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669"
TEST = "tests/packs/rendering/test_native_fresh_export_label.py::test_one_fresh_saved_frame_exports_retained_revision"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def file_manifest(root: Path, *, exclude_prefix: str | None = None) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        relative = str(path.relative_to(root))
        if exclude_prefix and (relative == exclude_prefix or relative.startswith(exclude_prefix + "/")):
            continue
        if path.is_symlink():
            result[relative] = "link:" + os.readlink(path)
        elif path.is_file():
            result[relative] = sha(path.read_bytes())
    return result


def source_manifest(root: Path) -> dict[str, str]:
    names = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"]
    ).decode().split("\0")
    result: dict[str, str] = {}
    for name in sorted({name for name in names if name}):
        path = root / name
        if path.is_symlink():
            result[name] = "link:" + os.readlink(path)
        elif path.is_file():
            result[name] = sha(path.read_bytes())
    return result


def browser_tree() -> dict[str, object]:
    entries: list[list[str]] = []
    for path in sorted(CHROME.parent.rglob("*")):
        name = str(path.relative_to(CHROME.parent))
        if path.is_symlink():
            entries.append([name, "symlink", sha(os.readlink(path).encode())])
        elif path.is_file():
            kind = "executable" if path.stat().st_mode & 0o111 else "file"
            entries.append([name, kind, sha(path.read_bytes())])
    return {"sha256": sha(encoded(entries)), "fileCount": len(entries)}


def public_manifest(root: Path) -> dict[str, str]:
    archive = root / PUBLIC_ARCHIVE
    with tarfile.open(archive) as stream:
        return {
            member.name.removeprefix("package/"): sha(stream.extractfile(member).read())
            for member in stream
            if member.isfile()
        }


def make_cache(home: Path) -> Path:
    home.chmod(0o700)
    cache = (
        home
        / "Library/Caches/astrid-remotion-browser"
        / REMOTION_VERSION
        / "chrome-headless-shell/linux64/chrome-headless-shell-linux64"
    )
    cache.mkdir(parents=True, mode=0o700)
    target = cache / "chrome-headless-shell"
    target.symlink_to(CHROME)
    assert target.is_file()
    assert target.resolve() == CHROME
    return target


def helper_resolution(root: Path, node: str, home: Path, *, project: Path) -> dict[str, object]:
    """Run the unchanged helper with no browser override or custom cache root."""
    script = """
import fs from 'node:fs';
import {sharedBrowserExecutable, sharedBrowserRoot, remotionRendererVersion} from './shared-browser.mjs';
const selected = sharedBrowserExecutable({projectRoot: process.argv[1]});
const normal = sharedBrowserExecutable();
console.log(JSON.stringify({
  root: sharedBrowserRoot(),
  selected,
  selectedRealpath: selected ? fs.realpathSync(selected) : null,
  selectedVersion: remotionRendererVersion(process.argv[1]),
  normal,
  normalVersion: remotionRendererVersion(),
}));
"""
    env = {"HOME": str(home), "PATH": os.environ.get("PATH", "")}
    env.pop("ASTRID_REMOTION_BROWSER_EXECUTABLE", None)
    output = subprocess.check_output(
        [node, "--input-type=module", "-e", script, str(project)],
        cwd=root / "remotion",
        env=env,
        text=True,
    )
    result = json.loads(output)
    expected_root = str(home / "Library/Caches/astrid-remotion-browser")
    assert result["root"] == expected_root
    assert result["selectedRealpath"] == str(CHROME)
    assert result["selectedVersion"] == REMOTION_VERSION
    assert result["normal"] is None
    assert result["normalVersion"] is None
    return result


def inventory(root: Path) -> dict[str, object]:
    baseline = json.loads(
        (ORCH / "design/handoff-vw-m3-live-source-label-native-join-qualified-pre.json").read_text()
    )
    # The public12 package is replaced in the private capture stage by the
    # separately hashed archive; do not treat its mutable shared copy as part
    # of the frozen six-peer graph.
    peer_graph = file_manifest(PEERS, exclude_prefix="@banodoco/timeline-composition/package")
    assert peer_graph == baseline["peer_graph"], "clean f816 peer graph changed"
    public = public_manifest(root)
    assert len(public) == 77 and public == baseline["public12"]
    with tarfile.open(NODE_ARCHIVE) as stream:
        node_bytes = stream.extractfile("node-v20.19.4-linux-x64/bin/node").read()
    assert sha(node_bytes) == NODE_SHA
    assert sha((root / PUBLIC_ARCHIVE).read_bytes()) == PUBLIC_SHA
    assert sha(CHROME.read_bytes()) == CHROME_SHA
    assert browser_tree() == {"sha256": CHROME_TREE_SHA, "fileCount": 255}
    runtime = subprocess.check_output(["git", "-C", "/home/user/work/runtime", "archive", RUNTIME])
    assert sha(runtime) == RUNTIME_ARCHIVE_SHA
    return {
        "declared_base": subprocess.check_output(["git", "-C", str(root), "rev-parse", BASE], text=True).strip(),
        "source": source_manifest(root),
        "peer_graph": peer_graph,
        "public12": public,
        "runtime_commit": RUNTIME,
        "runtime_archive_sha256": sha(runtime),
        "node_sha256": NODE_SHA,
        "chrome": {
            "path": str(CHROME),
            "executable_sha256": CHROME_SHA,
            "version": "155.0.8059.84",
            "tree_sha256": browser_tree()["sha256"],
            "fileCount": 255,
        },
        "python": file_manifest(PYTHON.parent.parent),
    }


def preflight(root: Path, node: str) -> int:
    before = inventory(root)
    with tempfile.TemporaryDirectory(prefix="run-home-", dir=WORK) as temp:
        home = Path(temp)
        home.chmod(0o700)
        cached = make_cache(home)
        resolution = helper_resolution(root, node, home, project=PEER_ROOT)
        before["cache_resolution"] = {
            "resolved_path": str(cached.resolve()),
            "sha256": sha(cached.resolve().read_bytes()),
            "version": REMOTION_VERSION,
            "helper": {
                "selectedRealpath": resolution["selectedRealpath"],
                "selectedVersion": resolution["selectedVersion"],
                "normal": resolution["normal"],
                "normalVersion": resolution["normalVersion"],
            },
            "browser_env_present": False,
            "native_no_argument_result": "null",
        }
    before["controller_sha256"] = sha(Path(__file__).read_bytes())
    digest = sha(encoded(before))
    Path(str(PREFIX) + "-manifest.json").write_bytes(encoded({**before, "source_sha256": digest}))
    print(json.dumps({
        "source_sha256": digest,
        "agent_files": len(before["source"]),
        "peer_entries": len(before["peer_graph"]),
        "public12_files": len(before["public12"]),
        "cache_resolved_path": before["cache_resolution"]["resolved_path"],
        "native_no_argument_result": before["cache_resolution"]["native_no_argument_result"],
        "test": TEST,
    }, indent=2))
    return 0


def capture(root: Path, reviewed: str, node: str) -> int:
    current = inventory(root)
    with tempfile.TemporaryDirectory(prefix="run-home-", dir=WORK) as temp:
        home = Path(temp)
        home.chmod(0o700)
        make_cache(home)
        resolution = helper_resolution(root, node, home, project=PEER_ROOT)
        assert resolution["selectedRealpath"] == str(CHROME)
        assert resolution["normal"] is None
        current["cache_resolution"] = {
            "resolved_path": str(CHROME),
            "sha256": CHROME_SHA,
            "version": REMOTION_VERSION,
            "helper": {
                "selectedRealpath": resolution["selectedRealpath"],
                "selectedVersion": resolution["selectedVersion"],
                "normal": resolution["normal"],
                "normalVersion": resolution["normalVersion"],
            },
            "browser_env_present": False,
            "native_no_argument_result": "null",
        }
    digest = sha(encoded({**current, "controller_sha256": sha(Path(__file__).read_bytes())}))
    if reviewed != digest:
        raise RuntimeError("reviewed source/environment fingerprint does not match")
    raise RuntimeError(
        "refusing before browser setup: native frame worker sharedBrowserExecutable() "
        "returns null because its no-argument default project root is the parent of "
        "ASTRID_REMOTION_PROJECT_DIR, while @remotion/renderer/package.json is under "
        "the admitted project; HostRemotionSession._start also drops "
        "ASTRID_REMOTION_BROWSER_EXECUTABLE"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "capture"))
    parser.add_argument("--source", type=Path, default=Path.cwd())
    parser.add_argument("--node", default="node")
    parser.add_argument("--reviewed-sha256")
    args = parser.parse_args()
    root = args.source.resolve()
    if args.mode == "preflight":
        return preflight(root, args.node)
    if not args.reviewed_sha256:
        raise SystemExit("capture requires --reviewed-sha256")
    return capture(root, args.reviewed_sha256, args.node)


if __name__ == "__main__":
    raise SystemExit(main())
