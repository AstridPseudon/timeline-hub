#!/usr/bin/env python3
"""Read-only readiness control for the presenter crop Composition graph.

This checks the exact snapshot attachment and the direct Node imports used by
the presenter helper.  It does not start a host, browser, server, renderer, or
capture process.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path


ARCHIVE_SHA256 = "9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738"
NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
IMPORTS = (
    "@banodoco/timeline-composition",
    "@banodoco/timeline-composition/evaluation",
    "@banodoco/timeline-composition/registries",
    "@banodoco/timeline-composition/theme-api",
    "@remotion/bundler",
    "@remotion/renderer",
    "@remotion/media",
    "@remotion/layout-utils",
    "esbuild",
    "react",
    "react-dom",
    "remotion",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_name(name: str) -> str:
    return "/".join(name.split("/")[:2]) if name.startswith("@") else name.split("/", 1)[0]


def resolve_node_imports(root: Path, node: Path, graph: Path) -> dict[str, dict[str, str]]:
    script = """
import {createRequire} from 'node:module';
import {realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const require = createRequire(import.meta.url);
const names = JSON.parse(process.env.READINESS_IMPORTS);
const packageName = name => name.startsWith('@') ? name.split('/').slice(0, 2).join('/') : name.split('/')[0];
const result = {};
for (const name of names) {
  result[name] = {
    path: realpathSync(fileURLToPath(import.meta.resolve(name))),
    manifest: realpathSync(require.resolve(`${packageName(name)}/package.json`)),
  };
}
console.log(JSON.stringify(result));
"""
    env = dict(os.environ)
    env.pop("ASTRID_REMOTION_PROJECT_DIR", None)
    env.pop("NODE_PATH", None)
    env["READINESS_IMPORTS"] = json.dumps(IMPORTS)
    completed = subprocess.run(
        [str(node), "--input-type=module", "-e", script],
        cwd=root / "remotion",
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    resolved = json.loads(completed.stdout)
    for name, paths in resolved.items():
        for key, value in paths.items():
            if not Path(value).is_relative_to(graph):
                raise AssertionError(f"{name} {key} escaped approved graph: {value}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--node", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve(strict=True)
    graph = args.graph.resolve(strict=True)
    artifact = args.artifact.resolve(strict=True)
    node = args.node.resolve(strict=True)
    attached = root / "remotion" / "node_modules"
    if not attached.is_symlink() or attached.resolve() != graph:
        raise AssertionError(f"attachment must resolve exactly to {graph}: {attached}")
    if (attached / "@banodoco").is_symlink() or not (attached / "@banodoco").is_dir():
        raise AssertionError("@banodoco scope must be a real graph directory")
    package = attached / "@banodoco" / "timeline-composition"
    if package.is_symlink() or not package.is_dir() or not (package / "package.json").is_file():
        raise AssertionError("Composition package must be present under the real graph scope")
    if sha256(artifact) != ARCHIVE_SHA256:
        raise AssertionError("Composition artifact hash changed")
    if sha256(node) != NODE_SHA256 or subprocess.check_output([str(node), "--version"], text=True).strip() != "v20.19.4":
        raise AssertionError("Node identity changed")

    with tarfile.open(artifact) as archive:
        members = [member for member in archive.getmembers() if member.name.startswith("package/") and member.name != "package/"]
        regular = [member for member in members if member.isfile()]
        links = [member for member in members if member.issym() or member.islnk()]
        archived = {
            member.name.removeprefix("package/"): hashlib.sha256(archive.extractfile(member).read()).hexdigest()
            for member in regular
        }
    installed = {
        str(path.relative_to(package)): sha256(path)
        for path in package.rglob("*")
        if path.is_file()
    }
    if len(regular) != 77 or links or len(installed) != 77 or installed != archived:
        raise AssertionError("Composition archive/install is not the exact 77-file public13 package")

    sys.path.insert(0, str(root))
    os.environ.pop("ASTRID_REMOTION_PROJECT_DIR", None)
    os.environ["ASTRID_NODE_EXECUTABLE"] = str(node)
    from scripts import gen_effect_registry

    registry_ids = gen_effect_registry._public_registry_ids()
    resolved = resolve_node_imports(root, node, graph)
    print(json.dumps({
        "attachment": str(attached),
        "attachment_realpath": str(attached.resolve()),
        "composition_manifest": str((package / "package.json").resolve()),
        "archive_sha256": ARCHIVE_SHA256,
        "archive_regular_members": len(regular),
        "node_version": "v20.19.4",
        "node_sha256": NODE_SHA256,
        "registry_ids": {kind: len(ids) for kind, ids in registry_ids.items()},
        "resolved_imports": resolved,
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
