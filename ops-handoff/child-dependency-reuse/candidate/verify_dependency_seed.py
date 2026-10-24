#!/usr/bin/env python3
"""Authenticate a finite wheelhouse against an active hash-locked requirements file."""

import base64
import configparser
import csv
import email
import fcntl
import hashlib
import importlib.metadata as md
import importlib.util
import io
import marshal
import os
import re
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import NoReturn

from packaging.markers import default_environment
from packaging.requirements import InvalidRequirement, Requirement
from packaging.tags import Tag, parse_tag, sys_tags
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
            metadata_dirs = {
                name.split("/", 1)[0]
                for name in names
                if "/" in name and name.split("/", 1)[0].endswith(".dist-info")
            }
            if len(metadata_dirs) != 1:
                fail(f"wheel metadata directory does not match filename: {display_name}")
            metadata_dir = next(iter(metadata_dirs))
            metadata_stem = metadata_dir.removesuffix(".dist-info")
            metadata_name, separator, metadata_version = metadata_stem.rpartition("-")
            if (
                not separator
                or canonicalize_name(metadata_name, validate=True) != canonicalize_name(filename_name)
                or metadata_version != filename_version
            ):
                fail(f"wheel metadata directory does not match filename: {display_name}")
            metadata = email.message_from_bytes(archive.read(f"{metadata_dir}/METADATA"))
            wheel_metadata = email.message_from_bytes(archive.read(f"{metadata_dir}/WHEEL"))
            if canonicalize_name(metadata.get("Name", "")) != canonicalize_name(filename_name):
                fail(f"wheel METADATA name does not match filename: {display_name}")
            if metadata.get("Version", "") != filename_version:
                fail(f"wheel METADATA version does not match filename: {display_name}")
            internal_tags: set[Tag] = set()
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


def installed_integrity(root: Path, artifacts: dict[str, bytes]) -> None:
    """Compare installed bytes to authenticated original wheels, not RECORD claims."""
    sites = list((root / "lib").glob("python*/site-packages"))
    if len(sites) != 1 or root.is_symlink() or sites[0].is_symlink():
        fail("installed child layout is missing or ambiguous")
    root = root.resolve()
    site = sites[0].resolve()
    if not site.is_relative_to(root):
        fail("installed site-packages escapes child")
    owned: set[str] = set()
    for filename, data in artifacts.items():
        name, version, _, _ = parse_wheel_filename(filename)
        distributions = [dist for dist in md.distributions(path=[str(site)])
                         if canonicalize_name(dist.metadata.get("Name", "")) == name]
        if len(distributions) != 1 or distributions[0].version != str(version):
            fail(f"missing or ambiguous installed dependency: {name}")
        dist = distributions[0]
        records = [str(item) for item in dist.files or [] if str(item).endswith(".dist-info/RECORD")]
        if len(records) != 1:
            fail(f"missing installed dependency RECORD: {name}")
        record = records[0]
        wheel_files: dict[str, bytes] = {}
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for entry in archive.infolist():
                if entry.is_dir() or entry.filename.endswith(".dist-info/RECORD"):
                    continue
                if any(part.endswith(".data") for part in Path(entry.filename).parts):
                    fail(f"unsupported relocated wheel layout: {filename}")
                wheel_files[entry.filename] = archive.read(entry)
        generated_scripts: dict[str, bytes] = {}
        entrypoint_files = [
            rel for rel in wheel_files if rel.endswith(".dist-info/entry_points.txt")
        ]
        if len(entrypoint_files) > 1:
            fail(f"ambiguous console entry-point metadata: {name}")
        if entrypoint_files:
            parser = configparser.ConfigParser(interpolation=None, strict=True)
            parser.optionxform = str  # type: ignore[method-assign, assignment]
            try:
                parser.read_string(wheel_files[entrypoint_files[0]].decode("utf-8"))
                entrypoints = (
                    list(parser.items("console_scripts", raw=True))
                    if parser.has_section("console_scripts")
                    else []
                )
            except (configparser.Error, UnicodeDecodeError) as exc:
                fail(f"malformed console entry-point metadata: {name}: {exc}")
            for script_name, target in entrypoints:
                if (
                    not script_name
                    or "/" in script_name
                    or "\\" in script_name
                    or "\x00" in script_name
                    or script_name in {".", ".."}
                ):
                    fail(f"unsafe console entry-point name: {name}:{script_name!r}")
                target = target.partition("[")[0].strip()
                module, separator, function = target.partition(":")
                if not separator or not module or not function:
                    fail(f"malformed console entry-point target: {name}:{script_name}")
                script_path = root / "bin" / script_name
                rel = str(Path(os.path.relpath(script_path, site)))
                generated_scripts[rel] = (
                    f"#!{root / 'bin/python'}\n"
                    "import sys\n"
                    f"from {module} import {function.split('.', 1)[0]}\n"
                    "if __name__ == '__main__':\n"
                    "    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n"
                    f"    sys.exit({function}())\n"
                ).encode()
        rows: set[str] = set()
        physical_rows: set[str] = set()
        for row in csv.reader(io.StringIO(captured_bytes(site / record).decode()), strict=True):
            if len(row) != 3:
                fail(f"malformed dependency RECORD: {name}")
            rel, encoded, size = row
            pure = PurePosixPath(rel)
            if (
                not rel
                or rel in rows
                or "\\" in rel
                or "\x00" in rel
                or pure.is_absolute()
                or str(pure) != rel
                or (".." in pure.parts and rel not in generated_scripts)
            ):
                fail(f"unsafe or overlapping dependency RECORD: {name}")
            path = site / rel
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                fail(f"unsafe or overlapping dependency RECORD: {name}")
            cursor = site
            for part in pure.parts:
                if part == "..":
                    cursor = cursor.parent
                else:
                    cursor /= part
                    if cursor.is_symlink():
                        fail(f"unsafe or overlapping dependency RECORD: {name}")
            physical = str(resolved.relative_to(root))
            if physical in physical_rows or physical in owned:
                fail(f"unsafe or overlapping dependency RECORD: {name}")
            rows.add(rel)
            physical_rows.add(physical)
            content = captured_bytes(path)
            original = wheel_files.get(rel)
            if original is not None:
                if content != original:
                    fail(f"installed dependency differs from original wheel: {rel}")
            elif rel == record:
                if encoded or size:
                    fail("dependency RECORD must be self-unhashed")
                continue
            elif rel.endswith(".pyc") and "__pycache__" in Path(rel).parts:
                source = importlib.util.source_from_cache(str(path))
                source_rel = str(Path(source).relative_to(site))
                if source_rel not in wheel_files or content[:4] != importlib.util.MAGIC_NUMBER or len(content) < 16:
                    fail(f"unowned dependency bytecode: {rel}")
                if marshal.loads(content[16:]) != compile(wheel_files[source_rel], source, "exec"):
                    fail(f"dependency bytecode differs from original wheel: {rel}")
                if not encoded and not size:
                    continue
            elif rel in generated_scripts:
                if content != generated_scripts[rel]:
                    fail(f"generated dependency script differs from wheel entry point: {rel}")
            elif Path(rel).parent != Path(record).parent or Path(rel).name not in {"INSTALLER", "REQUESTED"}:
                fail(f"unowned installed dependency file: {rel}")
            digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
            if encoded != "sha256=" + digest or size != str(len(content)):
                fail(f"dependency RECORD integrity mismatch: {rel}")
        if not set(wheel_files).issubset(rows):
            fail(f"incomplete installed dependency: {name}")
        if not set(generated_scripts).issubset(rows):
            fail(f"missing installed console script: {name}")
        for prefix in {Path(rel).parts[0] for rel in wheel_files}:
            location = site / prefix
            for path in ([location] if location.is_file() else location.rglob("*")):
                if path.is_file() and str(path.relative_to(site)) not in rows:
                    fail(f"unowned dependency package file: {path.name}")
        owned.update(physical_rows)


def install_snapshot(wheelhouse: Path, requirements: bytes, flags: list[str]) -> None:
    # pip rechecks every wheel hash against a kernel-sealed lock. Parent rename
    # or snapshot mutation cannot substitute requirements or authorize new bytes.
    lock_fd = os.memfd_create("dependency-lock", os.MFD_ALLOW_SEALING)
    directory_fd = os.open(wheelhouse, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        with os.fdopen(lock_fd, "wb", closefd=False) as stream:
            stream.write(requirements)
            stream.flush()
        fcntl.fcntl(lock_fd, fcntl.F_ADD_SEALS,
                    fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL)
        subprocess.run([sys.executable, "-m", "pip", "install", *flags,
                        "--no-index", "--find-links", f"/proc/self/fd/{directory_fd}",
                        "--require-hashes", "--no-deps", "-r", f"/proc/self/fd/{lock_fd}"],
                       pass_fds=(lock_fd, directory_fd), check=True)
    finally:
        os.close(directory_fd)
        os.close(lock_fd)


def main() -> int:
    args = sys.argv[1:]
    committed_lock = None
    if "--committed-lock" in args:
        index = args.index("--committed-lock")
        if len(args) < index + 5:
            fail("committed lock requires checkout, commit, path and SHA256")
        checkout, commit, lock_path, lock_hash = args[index + 1:index + 5]
        committed_lock = subprocess.check_output(["git", "-C", checkout, "show", commit + ":" + lock_path])
        if hashlib.sha256(committed_lock).hexdigest() != lock_hash:
            fail("committed lock SHA256 mismatch")
        committed_lock = b"\n".join(line for line in committed_lock.splitlines()
                                    if not line.startswith((b"astrid @", b"pip==", b"setuptools==", b"wheel=="))) + b"\n"
        args = args[:index] + args[index + 5:]
    install_flags = None
    installed = None
    if "--install" in args:
        index = args.index("--install")
        install_flags, args = args[index + 1:], args[:index]
    elif "--installed" in args:
        index = args.index("--installed")
        if len(args) != index + 2:
            fail("installed verification requires one child root")
        installed, args = Path(args[index + 1]), args[:index]
    if len(args) not in (2, 3):
        fail("usage is verify_dependency_seed.py WHEELHOUSE REQUIREMENTS [SNAPSHOT]")
    wheelhouse = Path(args[0])
    requirements = Path(args[1])
    snapshot = Path(args[2]) if len(args) == 3 else None
    if not wheelhouse.is_absolute() or wheelhouse != wheelhouse.resolve():
        fail("wheelhouse must be an absolute physical path")
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        fail("wheelhouse is missing or symlinked")
    if str(requirements) != "-" and (requirements.is_symlink() or not requirements.is_file()):
        fail("requirements file is missing or symlinked")
    requirements_bytes = (committed_lock if committed_lock is not None else
                          sys.stdin.buffer.read() if str(requirements) == "-" else captured_bytes(requirements))
    internal = installed is not None or install_flags is not None
    if internal and captured_bytes(wheelhouse / "requirements.txt") != requirements_bytes:
        fail("retained lock differs from requested committed lock")
    files = [item for item in wheelhouse.iterdir() if not (internal and item.name == "requirements.txt")]
    if any(item.is_symlink() or not item.is_file() for item in files):
        fail("wheelhouse contains a symlink or non-file")
    if any(item.suffix != ".whl" for item in files):
        fail("wheelhouse contains an unsupported artifact")

    active: dict[str, tuple[Requirement, set[str]]] = {}
    env = {key: str(value) for key, value in default_environment().items()}
    for text in logical_requirements(requirements_bytes):
        requirement, hashes = exact_lock_entry(text)
        if requirement.marker is not None and not requirement.marker.evaluate(dict(env)):
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
    artifacts = {path.name: data for path, data in matched.values()}
    if installed is not None:
        installed_integrity(installed, artifacts)
    if install_flags is not None:
        install_snapshot(wheelhouse, requirements_bytes, install_flags)
    if snapshot is not None:
        write_snapshot(snapshot, requirements_bytes, artifacts)
        print(f"verified dependency seed snapshot={snapshot} packages={len(matched)}")
    else:
        print(f"verified dependency seed wheelhouse={wheelhouse} packages={len(matched)}")
    return 0


if __name__ == "__main__":
    main()
