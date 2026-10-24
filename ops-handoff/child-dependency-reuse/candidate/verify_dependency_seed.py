#!/usr/bin/env python3
"""Authenticate a finite wheelhouse against an active hash-locked requirements file."""

import email
import hashlib
import io
import os
import re
import stat
import sys
import zipfile
from pathlib import Path
from typing import NoReturn

from packaging.markers import default_environment
from packaging.requirements import InvalidRequirement, Requirement
from packaging.tags import parse_tag, sys_tags
from packaging.utils import (
    InvalidWheelFilename,
    canonicalize_name,
    parse_wheel_filename,
)


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"REFUSED: dependency seed: {message}")


def logical_requirements(data: bytes) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"requirements file is not UTF-8: {exc}")
    for raw in lines:
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


def exact_lock_entry(text: str) -> tuple[Requirement, set[str]]:
    match = re.fullmatch(
        r"(?P<requirement>.+?)\s+(?P<hashes>--hash=sha256:[0-9a-f]{64}(?:\s+--hash=sha256:[0-9a-f]{64})*)",
        text,
    )
    if match is None:
        fail("active requirement must contain only sha256 lock hashes")
    try:
        requirement = Requirement(match.group("requirement"))
    except InvalidRequirement as exc:
        fail(f"invalid locked requirement: {exc}")
    if requirement.url or requirement.extras:
        fail("active requirement must identify one plain package")
    specifiers = list(requirement.specifier)
    if len(specifiers) != 1 or specifiers[0].operator != "==" or "*" in specifiers[0].version:
        fail(f"active requirement is not an exact == pin: {requirement.name}")
    hashes = set(re.findall(r"--hash=sha256:([0-9a-f]{64})", match.group("hashes")))
    if len(hashes) != len(re.findall(r"--hash=sha256:[0-9a-f]{64}", match.group("hashes"))):
        fail(f"duplicate sha256 hash for: {requirement.name}")
    return requirement, hashes


def captured_bytes(path: Path) -> bytes:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                fail(f"wheelhouse contains a non-file: {path.name}")
            with os.fdopen(fd, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(fd)
    except OSError as exc:
        fail(f"cannot capture wheelhouse file {path.name}: {exc}")


def archive_identity(data: bytes, display_name: str, filename_name: str, filename_version: str, filename_tags: set) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            names = [entry.filename for entry in entries]
            if len(names) != len(set(names)):
                fail(f"wheel contains duplicate archive paths: {display_name}")
            for entry in entries:
                name = entry.filename
                pure = Path(name.rstrip("/"))
                if (
                    not name
                    or "\\" in name
                    or "\x00" in name
                    or name.startswith("/")
                    or any(part in ("", ".", "..") for part in name.rstrip("/").split("/"))
                ):
                    fail(f"wheel contains an unsafe archive path: {display_name}:{name!r}")
                mode = (entry.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK or mode not in (0, stat.S_IFREG, stat.S_IFDIR):
                    fail(f"wheel contains an unsafe archive member: {display_name}:{name}")
                if pure.is_absolute():
                    fail(f"wheel contains an absolute archive path: {display_name}:{name}")
            expected = f"{canonicalize_name(filename_name).replace('-', '_')}-{filename_version}.dist-info"
            metadata_dirs = {name.split("/", 1)[0] for name in names if ".dist-info/" in name}
            if metadata_dirs != {expected}:
                fail(f"wheel metadata directory does not match filename: {display_name}")
            metadata = email.message_from_bytes(archive.read(f"{expected}/METADATA"))
            wheel_metadata = email.message_from_bytes(archive.read(f"{expected}/WHEEL"))
            if canonicalize_name(metadata.get("Name", "")) != canonicalize_name(filename_name):
                fail(f"wheel METADATA name does not match filename: {display_name}")
            if metadata.get("Version", "") != filename_version:
                fail(f"wheel METADATA version does not match filename: {display_name}")
            internal_tags = set()
            for value in wheel_metadata.get_all("Tag", []):
                internal_tags.update(parse_tag(value.strip()))
            if internal_tags != filename_tags:
                fail(f"wheel WHEEL tags do not match filename: {display_name}")
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        fail(f"invalid wheel archive {display_name}: {exc}")


def write_snapshot(snapshot: Path, requirements: bytes, artifacts: dict[str, bytes]) -> None:
    if not snapshot.is_absolute() or snapshot.exists() or snapshot.is_symlink():
        fail("snapshot destination must be a new absolute path")
    parent = snapshot.parent
    if parent.is_symlink() or not parent.is_dir() or parent != parent.resolve():
        fail("snapshot parent is missing or symlinked")
    try:
        snapshot.mkdir(mode=0o700)
        for name, data in [("requirements.txt", requirements), *artifacts.items()]:
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.+-]*", name):
                fail("snapshot contains an unsafe filename")
            fd = os.open(snapshot / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
            try:
                view = memoryview(data)
                while view:
                    view = view[os.write(fd, view):]
                os.fsync(fd)
            finally:
                os.close(fd)
        os.chmod(snapshot, 0o500)
        fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError as exc:
        fail(f"cannot create immutable snapshot: {exc}")


def main() -> int:
    if len(sys.argv) not in (3, 4):
        fail("usage is verify_dependency_seed.py WHEELHOUSE REQUIREMENTS [SNAPSHOT]")
    wheelhouse = Path(sys.argv[1])
    requirements = Path(sys.argv[2])
    snapshot = Path(sys.argv[3]) if len(sys.argv) == 4 else None
    if not wheelhouse.is_absolute() or wheelhouse != wheelhouse.resolve():
        fail("wheelhouse must be an absolute physical path")
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        fail("wheelhouse is missing or symlinked")
    if requirements.is_symlink() or not requirements.is_file():
        fail("requirements file is missing or symlinked")
    requirements_bytes = captured_bytes(requirements)
    files = list(wheelhouse.iterdir())
    if any(item.is_symlink() or not item.is_file() for item in files):
        fail("wheelhouse contains a symlink or non-file")
    if any(item.suffix != ".whl" for item in files):
        fail("wheelhouse contains an unsupported artifact")

    active: dict[str, tuple[Requirement, set[str]]] = {}
    env = default_environment()
    for text in logical_requirements(requirements_bytes):
        requirement, hashes = exact_lock_entry(text)
        if requirement.marker is not None and not requirement.marker.evaluate(env):
            continue
        key = canonicalize_name(requirement.name)
        if key in active:
            fail(f"duplicate active requirement: {requirement.name}")
        active[key] = (requirement, hashes)
    if not active:
        fail("no active requirements")

    supported = set(sys_tags())
    matched: dict[str, tuple[Path, bytes]] = {}
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
        if str(version) != next(iter(requirement.specifier)).version:
            fail(f"wheel version does not exactly match lock: {path.name}")
        if not tags & supported:
            fail(f"wheel tags are incompatible with this interpreter/platform: {path.name}")
        data = captured_bytes(path)
        actual = hashlib.sha256(data).hexdigest()
        if actual not in hashes:
            fail(f"wheel hash is not listed in lock: {path.name}")
        if key in matched:
            fail(f"multiple wheel artifacts for active package: {path.name}")
        archive_identity(data, path.name, str(name), str(version), set(tags))
        matched[key] = (path, data)
    missing = sorted(set(active) - set(matched))
    if missing:
        fail("missing compatible wheel for: " + ", ".join(missing))
    if snapshot is not None:
        write_snapshot(snapshot, requirements_bytes, {path.name: data for path, data in matched.values()})
        print(f"verified dependency seed snapshot={snapshot} packages={len(matched)}")
    else:
        print(f"verified dependency seed wheelhouse={wheelhouse} packages={len(matched)}")
    return 0


if __name__ == "__main__":
    main()
