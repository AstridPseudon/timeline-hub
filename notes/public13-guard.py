from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys
import tarfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PRIVATE = pathlib.Path(
    os.environ.get(
        "TIMELINE_PRIVATE13_NODE_MODULES",
        str(ROOT / "private13" / "node_modules"),
    )
)
ARCHIVE = ROOT / "vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz"
RUNTIME = pathlib.Path(
    os.environ.get(
        "TIMELINE_RUNTIME_CHECKOUT",
        "/home/user/work/wt/app-m3-runtime013-producer-source",
    )
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package_version(name: str) -> str:
    return json.loads((PRIVATE / name / "package.json").read_text())["version"]


def archive_manifest() -> dict[str, bytes]:
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = archive.getmembers()
        assert len(members) == 77 and all(member.isfile() for member in members)
        result: dict[str, bytes] = {}
        for member in members:
            relative = pathlib.PurePosixPath(member.name).relative_to("package")
            assert not relative.is_absolute() and ".." not in relative.parts
            key = str(relative)
            assert key not in result
            result[key] = archive.extractfile(member).read()
        return result


def installed_manifest(package: pathlib.Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(package)): path.read_bytes()
        for path in package.rglob("*")
        if path.is_file()
    }


def verify() -> dict[str, object]:
    assert PRIVATE.is_dir() and not PRIVATE.is_symlink()
    assert ARCHIVE.is_file()
    archive_bytes = ARCHIVE.read_bytes()
    assert len(archive_bytes) == 58477
    assert sha256(archive_bytes) == (
        "9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738"
    )

    composition = PRIVATE / "@banodoco/timeline-composition"
    expected = archive_manifest()
    installed = installed_manifest(composition)
    assert installed == expected
    assert composition.is_dir() and not composition.is_symlink()
    for scope in (PRIVATE / "@banodoco", PRIVATE / "@remotion"):
        assert scope.is_dir() and not scope.is_symlink(), scope
    for cache in (PRIVATE / ".vite", PRIVATE / ".vite-temp"):
        assert cache.is_dir() and not cache.is_symlink(), cache

    peers = {
        "react": "18.3.1",
        "react-dom": "18.3.1",
        "remotion": "4.0.509",
        "@remotion/player": "4.0.509",
        "@remotion/three": "4.0.509",
        "@remotion/layout-utils": "4.0.509",
        "@remotion/media": "4.0.509",
    }
    assert {name: package_version(name) for name in peers} == peers

    runtime_manifest = json.loads((RUNTIME / "contract/artifacts.json").read_text())
    assert len(runtime_manifest["artifacts"]) == 75
    app_lock = json.loads((ROOT / "runtime.lock.json").read_text())
    assert len(app_lock["files"]) == 13
    for name, item in app_lock["files"].items():
        app_file = ROOT / name
        runtime_file = RUNTIME / item["from"]
        app_bytes = app_file.read_bytes()
        assert app_bytes == runtime_file.read_bytes()
        digest = f"sha256:{sha256(app_bytes)}"
        assert digest == item["sha256"]
        assert digest == runtime_manifest["artifacts"][item["from"]]

    return {
        "archive": {"bytes": len(archive_bytes), "sha256": sha256(archive_bytes)},
        "composition": {
            "files": len(installed),
            "tree_sha256": sha256(
                b"".join(
                    key.encode() + b"\0" + installed[key]
                    for key in sorted(installed)
                )
            ),
            "animations_generated_bytes": len(
                installed["dist/animations.generated.js"]
            ),
        },
        "peers": peers,
        "runtime": {
            "artifacts": len(runtime_manifest["artifacts"]),
            "lock_files": len(app_lock["files"]),
            "source_commit": app_lock["source_commit"],
        },
        "private_node_modules": str(PRIVATE),
    }


if __name__ == "__main__":
    json.dump(verify(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
