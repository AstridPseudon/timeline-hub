#!/usr/bin/env python3
"""Authenticate a finite wheelhouse against an active hash-locked requirements file."""

import hashlib
import re
import sys
from pathlib import Path
from typing import NoReturn

from packaging.markers import default_environment
from packaging.requirements import InvalidRequirement, Requirement
from packaging.tags import sys_tags
from packaging.utils import (
    InvalidWheelFilename,
    canonicalize_name,
    parse_wheel_filename,
)


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"REFUSED: dependency seed: {message}")


def logical_requirements(path: Path) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if current and not raw[:1].isspace() and not current[-1].endswith("\\"):
            blocks.append(" ".join(current))
            current = []
        current.append(line)
        if not line.endswith("\\"):
            blocks.append(" ".join(current))
            current = []
    if current:
        blocks.append(" ".join(current))
    return [block.replace("\\", " ") for block in blocks]


def main() -> int:
    if len(sys.argv) != 3:
        fail("usage is verify_dependency_seed.py WHEELHOUSE REQUIREMENTS")
    wheelhouse = Path(sys.argv[1])
    requirements = Path(sys.argv[2])
    if not wheelhouse.is_absolute() or wheelhouse != wheelhouse.resolve():
        fail("wheelhouse must be an absolute physical path")
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        fail("wheelhouse is missing or symlinked")
    if requirements.is_symlink() or not requirements.is_file():
        fail("requirements file is missing or symlinked")
    files = list(wheelhouse.iterdir())
    if any(item.is_symlink() or not item.is_file() for item in files):
        fail("wheelhouse contains a symlink or non-file")
    if any(item.suffix != ".whl" for item in files):
        fail("wheelhouse contains an unsupported artifact")

    active: dict[str, tuple[Requirement, set[str]]] = {}
    env = default_environment()
    for text in logical_requirements(requirements):
        requirement_text = text.split(" --hash=", 1)[0].strip()
        try:
            requirement = Requirement(requirement_text)
        except InvalidRequirement as exc:
            fail(f"invalid locked requirement: {exc}")
        if requirement.marker is not None and not requirement.marker.evaluate(env):
            continue
        if requirement.url or not requirement.specifier:
            fail("active requirement is not an exact pinned package")
        hashes = set(re.findall(r"--hash=sha256:([0-9a-f]{64})", text))
        if not hashes:
            fail(f"active requirement has no sha256 hashes: {requirement.name}")
        key = canonicalize_name(requirement.name)
        if key in active:
            fail(f"duplicate active requirement: {requirement.name}")
        active[key] = (requirement, hashes)
    if not active:
        fail("no active requirements")

    supported = set(sys_tags())
    matched: dict[str, Path] = {}
    for path in files:
        try:
            name, version, _build, tags = parse_wheel_filename(path.name)
        except InvalidWheelFilename as exc:
            fail(f"invalid wheel filename {path.name}: {exc}")
        key = canonicalize_name(str(name))
        item = active.get(key)
        if item is None:
            fail(f"unsupported wheel artifact: {path.name}")
        requirement, hashes = item
        if str(version) not in requirement.specifier:
            fail(f"wheel version does not satisfy lock: {path.name}")
        if not tags & supported:
            fail(f"wheel tags are incompatible with this interpreter/platform: {path.name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual not in hashes:
            fail(f"wheel hash is not listed in lock: {path.name}")
        if key in matched:
            fail(f"multiple wheel artifacts for active package: {path.name}")
        matched[key] = path
    missing = sorted(set(active) - set(matched))
    if missing:
        fail("missing compatible wheel for: " + ", ".join(missing))
    print(f"verified dependency seed wheelhouse={wheelhouse} packages={len(matched)}")
    return 0


if __name__ == "__main__":
    main()
