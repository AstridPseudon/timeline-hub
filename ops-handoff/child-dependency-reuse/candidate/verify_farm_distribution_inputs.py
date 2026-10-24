"""Validate the immutable inputs to the normal Farm maker.

This module is deliberately a source-only component.  It does not fetch,
install, build, provision, inspect an installed child, or talk to Store.  The
maker's integration point is::

    receipt = validate_farm_distribution_inputs(
        schema_source=agent_checkout,
        wheelhouse=reviewed_wheelhouse,
        additional_wheels=reviewed_additional_wheels,
    )
    # retain ``receipt`` and use receipt["component_identity"] in the normal
    # maker/Store identity before create and on every reuse verification.

``schema_source`` is the Agent source tree, not an installed distribution.
The five approved wheels are the independently reviewed original packet.  No
caller-supplied additional wheel authority exists until an independent review
register is wired in; caller labels and hashes cannot grant admission.
Source custody uses the normal maker's real OS UID/GID and physical descriptor
reads. Safe copies and sealed modes are admitted explicitly; copied snapshots
without selected Git object authority fail closed. The receipt describes the
checked bytes and paths, and must be revalidated at every later maker use.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import tomllib
import zipfile
from collections.abc import Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass
from email import message_from_bytes
from pathlib import Path, PurePosixPath
from typing import Any, Final, NoReturn

SCHEMA_PACKAGE: Final = "banodoco-timeline-schema"
SCHEMA_VERSION: Final = "0.0.2"
SCHEMA_COMMIT: Final = "242f9c4306bf3b501222cb041a9eb246ef47bc85"
SCHEMA_SUBDIRECTORY: Final = "packages/timeline-schema/python"
SCHEMA_DECLARATION: Final = (
    "banodoco-timeline-schema @ "
    "git+https://github.com/banodoco/astrid-agent.git@"
    f"{SCHEMA_COMMIT}#subdirectory={SCHEMA_SUBDIRECTORY}"
)

_WHEEL_NAME = re.compile(
    r"\A(?P<name>.+)-(?P<version>[^-]+)-(?P<python>[^-]+)-"
    r"(?P<abi>[^-]+)-(?P<platform>[^.]+)\.whl\Z"
)


class ValidationError(ValueError):
    """A fail-closed input refusal suitable for the normal maker."""


@dataclass(frozen=True)
class WheelInput:
    """An independently reviewed wheel the maker wants retained.

    The expected identity is checked against the archive.  The fixed five
    packet entries below are the only approved inputs.  ``additional_wheels``
    remains in the interface for the later independently authenticated join,
    but is refused while that authority is absent.
    """

    path: Path
    filename: str
    name: str
    version: str
    sha256: str
    size: int
    role: str
    source: str


def _wheel(
    filename: str, name: str, version: str, sha256: str, size: int, role: str
) -> WheelInput:
    return WheelInput(
        path=Path(filename),
        filename=filename,
        name=name,
        version=version,
        sha256=sha256,
        size=size,
        role=role,
        source="reviewed-original-wheel-input-0932",
    )


APPROVED_WHEELS: Final[tuple[WheelInput, ...]] = (
    _wheel(
        "pip-26.2.1-py3-none-any.whl",
        "pip",
        "26.2.1",
        "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
        1816632,
        "bootstrap3",
    ),
    _wheel(
        "setuptools-80.9.0-py3-none-any.whl",
        "setuptools",
        "80.9.0",
        "062d34222ad13e0cc312a4c02d73f059e86a4acbfbdea8f8f76b28c99f306922",
        1201486,
        "bootstrap3",
    ),
    _wheel(
        "wheel-0.46.3-py3-none-any.whl",
        "wheel",
        "0.46.3",
        "4b399d56c9d9338230118d705d9737a2a468ccca63d5e813e2a4fc7815d8bc4d",
        30557,
        "bootstrap3",
    ),
    _wheel(
        "pytest_xdist-3.8.0-py3-none-any.whl",
        "pytest-xdist",
        "3.8.0",
        "202ca578cfeb7370784a8c33d6d05bc6e13b4f25b5053c30a152269fd10f0b88",
        46396,
        "test2",
    ),
    _wheel(
        "execnet-2.1.2-py3-none-any.whl",
        "execnet",
        "2.1.2",
        "67fba928dd5a544b783f6056f449e5e3931a5c378b128bc18501f7ea79e296ec",
        40708,
        "test2",
    ),
)

_APPROVED_BY_FILENAME: Final[Mapping[str, WheelInput]] = {
    item.filename: item for item in APPROVED_WHEELS
}


def _fail(message: str) -> NoReturn:
    raise ValidationError(message)


def _canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _json_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _physical_directory(value: Path, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        _fail(f"{label} must be an existing absolute directory, not a symlink")
    resolved = path.resolve()
    if resolved != path:
        _fail(f"{label} must have a physical path")
    return path


def _safe_member(name: str, label: str) -> None:
    pure = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or "\x00" in name
        or pure.is_absolute()
        or str(pure) != name
        or any(part in ("", ".", "..") for part in pure.parts)
    ):
        _fail(f"{label} has an unsafe path: {name!r}")


def _read_regular(path: Path, label: str) -> bytes:
    try:
        info = path.lstat()
    except OSError as exc:
        _fail(f"{label} cannot be read: {exc}")
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        _fail(f"{label} is not an owned, unlinked regular file")
    try:
        with path.open("rb") as stream:
            return stream.read()
    except OSError as exc:
        _fail(f"{label} cannot be read: {exc}")


def _parse_record(
    data: bytes, members: Mapping[str, bytes], display: str, self_record: str
) -> tuple[dict[str, Any], ...]:
    try:
        rows = list(csv.reader(io.StringIO(data.decode("utf-8"), newline="")))
    except (UnicodeDecodeError, csv.Error) as exc:
        _fail(f"{display} RECORD is invalid: {exc}")
    if not rows:
        _fail(f"{display} RECORD is empty")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if len(row) != 3:
            _fail(f"{display} RECORD row does not have three columns")
        name, digest, size_text = row
        _safe_member(name, f"{display} RECORD")
        if name in seen:
            _fail(f"{display} RECORD contains duplicate ownership: {name}")
        seen.add(name)
        if name not in members:
            _fail(f"{display} RECORD owns a missing archive member: {name}")
        if name == self_record:
            if digest or size_text:
                _fail(f"{display} RECORD must have a blank self-row")
        else:
            if not digest and not size_text:
                # Wheels may deliberately leave generated __pycache__ rows
                # unhashed.  Preserve the row, while still requiring that it
                # names a real archive member and that both fields are blank.
                pass
            else:
                if not digest.startswith("sha256=") or not size_text.isdigit():
                    _fail(f"{display} RECORD has an incomplete hash/size row: {name}")
                encoded = digest.removeprefix("sha256=")
                try:
                    expected = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
                except ValueError as exc:
                    _fail(f"{display} RECORD hash is invalid: {name}: {exc}")
                actual = hashlib.sha256(members[name]).digest()
                if expected != actual or int(size_text) != len(members[name]):
                    _fail(f"{display} RECORD hash/size mismatch: {name}")
        result.append({"path": name, "sha256": digest, "size": size_text})
    if set(members) != seen:
        missing = sorted(set(members) - seen)
        _fail(f"{display} RECORD does not own complete archive: {missing[0]}")
    return tuple(result)


def _validate_wheel(path: Path, expected: WheelInput) -> dict[str, Any]:
    data = _read_regular(path, f"wheel {expected.filename}")
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if len(data) != expected.size or actual_sha256 != expected.sha256:
        _fail(f"wheel {expected.filename} does not match approved bytes")
    match = _WHEEL_NAME.fullmatch(expected.filename)
    if match is None or match.group("python", "abi", "platform") != ("py3", "none", "any"):
        _fail(f"wheel {expected.filename} is not the approved py3-none-any tag")
    if _canonical_name(match.group("name")) != _canonical_name(expected.name):
        _fail(f"wheel {expected.filename} filename name is not expected")
    if match.group("version") != expected.version:
        _fail(f"wheel {expected.filename} filename version is not expected")

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            names: set[str] = set()
            folded: set[str] = set()
            member_bytes: dict[str, bytes] = {}
            for entry in entries:
                name = entry.filename
                _safe_member(name, f"wheel {expected.filename}")
                if name in names or name.casefold() in folded:
                    _fail(f"wheel {expected.filename} contains duplicate archive paths")
                names.add(name)
                folded.add(name.casefold())
                mode = (entry.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK or mode not in (0, stat.S_IFREG):
                    _fail(f"wheel {expected.filename} contains an unsafe member: {name}")
                member_bytes[name] = archive.read(name)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        _fail(f"wheel {expected.filename} is not a valid archive: {exc}")

    metadata_dirs = {
        name.split("/", 1)[0]
        for name in names
        if "/" in name and name.split("/", 1)[0].endswith(".dist-info")
    }
    if len(metadata_dirs) != 1:
        _fail(f"wheel {expected.filename} must contain exactly one dist-info directory")
    metadata_dir = next(iter(metadata_dirs))
    stem = metadata_dir.removesuffix(".dist-info")
    metadata_name, separator, metadata_version = stem.rpartition("-")
    if (
        not separator
        or _canonical_name(metadata_name) != _canonical_name(expected.name)
        or metadata_version != expected.version
    ):
        _fail(f"wheel {expected.filename} metadata directory is not exact")
    required = {f"{metadata_dir}/METADATA", f"{metadata_dir}/WHEEL", f"{metadata_dir}/RECORD"}
    if not required.issubset(names):
        _fail(f"wheel {expected.filename} is missing required metadata")
    metadata = message_from_bytes(member_bytes[f"{metadata_dir}/METADATA"])
    if _canonical_name(metadata.get("Name", "")) != _canonical_name(expected.name):
        _fail(f"wheel {expected.filename} METADATA name is not exact")
    if metadata.get("Version", "") != expected.version:
        _fail(f"wheel {expected.filename} METADATA version is not exact")
    wheel_metadata = message_from_bytes(member_bytes[f"{metadata_dir}/WHEEL"])
    tags = [value.strip() for value in wheel_metadata.get_all("Tag", [])]
    if tags != ["py3-none-any"]:
        _fail(f"wheel {expected.filename} WHEEL tags are not exact")

    members = {name: value for name, value in member_bytes.items() if not name.endswith("/")}
    records = _parse_record(
        member_bytes[f"{metadata_dir}/RECORD"],
        members,
        expected.filename,
        f"{metadata_dir}/RECORD",
    )
    return {
        "filename": expected.filename,
        "name": expected.name,
        "version": expected.version,
        "role": expected.role,
        "source": expected.source,
        "sha256": actual_sha256,
        "size": len(data),
        "compatible_tags": ["py3-none-any"],
        "archive_members": len(names),
        "record": list(records),
    }


def validate_wheel_inputs(
    wheelhouse: Path, *, additional_wheels: Sequence[WheelInput] = ()
) -> dict[str, Any]:
    """Authenticate the fixed packet and refuse unauthenticated additions.

    This function does not require schema custody, making it useful for the
    maker's finite input stage.  ``validate_farm_distribution_inputs`` is the
    production gate and additionally requires the exact Agent source tree.
    A future independently authenticated register may extend this finite
    packet; caller-provided metadata is not that register.
    """

    root = _physical_directory(Path(wheelhouse), "wheelhouse")
    extras = list(additional_wheels)
    if extras:
        _fail(
            "additional wheel authority is unavailable; only the reviewed "
            "original packet is admitted"
        )
    expected = _APPROVED_BY_FILENAME
    actual: dict[str, Path] = {}
    for entry in os.scandir(root):
        path = Path(entry.path)
        if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
            _fail(f"wheelhouse contains a non-file or symlink: {path.name}")
        if path.suffix != ".whl":
            _fail(f"wheelhouse contains an unexpected file: {path.name}")
        actual[path.name] = path
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        _fail(f"wheelhouse set mismatch: missing={missing!r} extra={extra!r}")

    distributions = [
        _validate_wheel(actual[filename], expectation)
        for filename, expectation in sorted(expected.items())
    ]
    owners: dict[str, str] = {}
    for distribution in distributions:
        for record in distribution["record"]:
            path = record["path"]
            previous = owners.get(path)
            if previous is not None:
                _fail(
                    f"wheel RECORD ownership overlaps: {path} "
                    f"({previous}, {distribution['filename']})"
                )
            owners[path] = distribution["filename"]
    lock = [
        f"{item['name']}=={item['version']} --hash=sha256:{item['sha256']}"
        for item in distributions
    ]
    result: dict[str, Any] = {
        "schema": "timeline.farm-distribution-inputs.v1",
        "roles": {
            "bootstrap3": [
                item["filename"] for item in distributions if item["role"] == "bootstrap3"
            ],
            "test2": [item["filename"] for item in distributions if item["role"] == "test2"],
            "additional": [
                item["filename"]
                for item in distributions
                if item["role"] in {"additional-source", "additional-test"}
            ],
        },
        "lock": lock,
        "distributions": distributions,
        "ownership": dict(sorted(owners.items())),
    }
    result["component_identity"] = _json_digest(result)
    return result


def _git(root: int, *args: str) -> str:
    # The maker process, Git executable and OS are trusted. Caller Git env,
    # global config, replacement objects and the working index are not authority.
    env = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    env.update(
        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS="0"
    )
    try:
        completed = subprocess.run(
            ["git", "--no-replace-objects", "-c", "core.fsmonitor=false", *args],
            cwd=f"/proc/self/fd/{root}",
            pass_fds=(root,),
            env=env,
            capture_output=True,
            check=False,
        )
    except (OSError, UnicodeError) as exc:
        _fail(f"schema source Git probe failed: {exc}")
    if completed.returncode != 0:
        _fail(
            "schema source Git probe refused; missing interface: authenticated "
            "selected Agent Git object source for copied snapshots"
        )
    if (
        args == ("cat-file", "commit", SCHEMA_COMMIT)
        and _git_object_digest("commit", completed.stdout) != SCHEMA_COMMIT
    ):
        _fail("schema source selected commit content cannot be authenticated")
    try:
        return completed.stdout.decode("utf-8")
    except UnicodeError as exc:
        _fail(f"schema source Git output is not supported UTF-8: {exc}")


def _node(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_uid,
        info.st_gid,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


class _SourceCustody(ExitStack):
    """Pin physical paths from /; authenticate before open and after use.

    Ownership comes from the maker's real UID/GID, never caller metadata.
    Root-owned, nonwritable system ancestors are allowed. The root-owned sticky
    system /tmp namespace is allowed only ABOVE the source root; its pinned
    child must belong to the maker. Same-UID writers are outside isolation:
    this is a checked read, not a lock or authority to install later by path.
    """

    def __init__(self, root: Path):
        super().__init__()
        self.root = root
        self.nodes: dict[Path, tuple[int, os.stat_result]] = {}
        self.uid, self.gid = os.getuid(), os.getgid()
        self.contents: dict[Path, bytes] = {}

    def directory(self, path: Path) -> int:
        if path in self.nodes:
            return self.nodes[path][0]
        parent = None if path == Path("/") else self.directory(path.parent)
        return self.open(path, directory=True, parent=parent)

    def open(self, path: Path, *, directory: bool, parent: int | None) -> int:
        name = "/" if parent is None else path.name
        info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if path in self.nodes:
            fd, original = self.nodes[path]
            if _node(info) != _node(original) or _node(os.fstat(fd)) != _node(original):
                _fail(f"schema source path changed before reuse: {path}")
            return fd
        mode = stat.S_IMODE(info.st_mode)
        ancestor = path != self.root and path in self.root.parents
        if stat.S_ISLNK(info.st_mode):
            _fail(f"schema source path contains a symlink: {path}")
        expected = stat.S_ISDIR if directory else stat.S_ISREG
        if not expected(info.st_mode) or (not directory and info.st_nlink != 1):
            _fail(f"schema source path is not an owned physical entry: {path}")
        owners = {0, self.uid} if ancestor else {self.uid}
        groups = {0, self.gid} if ancestor else {self.gid}
        if info.st_uid not in owners or info.st_gid not in groups:
            _fail(f"schema source unexpected owner/group: {path}")
        sticky_namespace = path == Path("/tmp") and ancestor and info.st_uid == 0 and mode == 0o1777
        if not sticky_namespace and (mode & 0o7022):
            _fail(f"schema source unsafe writable/special mode: {path}")
        if (
            directory
            and not ancestor
            and mode not in {0o500, 0o550, 0o555, 0o700, 0o750, 0o755}
        ):
            _fail(f"schema source directory mode is not a supported copy mode: {path}")
        if not directory and mode not in {
            0o400,
            0o440,
            0o444,
            0o600,
            0o640,
            0o644,
            0o500,
            0o550,
            0o555,
            0o700,
            0o750,
            0o755,
        }:
            _fail(f"schema source file mode is not a supported copy mode: {path}")
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
        if directory:
            flags |= os.O_DIRECTORY
        fd = os.open(name, flags, dir_fd=parent)
        self.callback(os.close, fd)
        if _node(os.fstat(fd)) != _node(info):
            _fail(f"schema source path changed while opening: {path}")
        self.nodes[path] = fd, info
        return fd

    def read(self, path: Path, git_mode: str | None = None) -> bytes:
        fd = self.open(path, directory=False, parent=self.directory(path.parent))
        info = self.nodes[path][1]
        mode = stat.S_IMODE(info.st_mode)
        # Normal copies may retain owner write or be sealed by the maker.
        allowed = {0o400, 0o440, 0o444, 0o600, 0o640, 0o644}
        if git_mode == "100755":
            allowed = {0o500, 0o550, 0o555, 0o700, 0o750, 0o755}
        if mode not in allowed:
            _fail(f"schema source mode does not match Git for: {path}")
        if path in self.contents:
            return self.contents[path]
        with os.fdopen(os.dup(fd), "rb") as stream:
            data = stream.read()
        if _node(os.fstat(fd)) != _node(info):
            _fail(f"schema source file changed while reading: {path}")
        self.contents[path] = data
        return data

    def preflight(self) -> None:
        """Authenticate selected physical entries before status/content reads."""

        self.open(
            self.root / "pyproject.toml",
            directory=False,
            parent=self.directory(self.root),
        )
        pending = [self.root / SCHEMA_SUBDIRECTORY]
        while pending:
            directory = pending.pop()
            fd = self.directory(directory)
            for name in os.listdir(fd):
                target = directory / name
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                is_directory = stat.S_ISDIR(info.st_mode)
                self.open(target, directory=is_directory, parent=fd)
                if is_directory:
                    pending.append(target)

    def finish(self) -> list[dict[str, Any]]:
        result = []
        for path, (fd, info) in sorted(self.nodes.items()):
            parent = None if path == Path("/") else self.nodes[path.parent][0]
            current = os.stat(
                "/" if parent is None else path.name,
                dir_fd=parent,
                follow_symlinks=False,
            )
            count = 5 if path != self.root and path in self.root.parents else 9
            if (
                _node(current)[:count] != _node(info)[:count]
                or _node(os.fstat(fd))[:count] != _node(info)[:count]
            ):
                _fail(f"schema source path changed during validation: {path}")
            result.append(
                {
                    "path": str(path),
                    "uid": info.st_uid,
                    "gid": info.st_gid,
                    "mode": oct(stat.S_IMODE(info.st_mode)),
                    "device": info.st_dev,
                    "inode": info.st_ino,
                    **(
                        {
                            "nlink": info.st_nlink,
                            "size": info.st_size,
                            "mtime_ns": info.st_mtime_ns,
                            "ctime_ns": info.st_ctime_ns,
                        }
                        if count == 9
                        else {}
                    ),
                }
            )
        return result


def _contains_value(value: object, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, Mapping):
        return any(_contains_value(item, expected) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_contains_value(item, expected) for item in value)
    return False


def _tracked_schema_files(root: int, tree: str) -> dict[str, tuple[str, str]]:
    """Authenticate tree objects down to the full package, never the index."""

    tracked: dict[str, tuple[str, str]] = {}

    def walk(oid: str, prefix: str) -> None:
        raw = _git(root, "ls-tree", "-z", oid)
        entries = []
        serialized = bytearray()
        for entry in raw.split("\0"):
            if not entry:
                continue
            metadata, separator, name = entry.partition("\t")
            fields = metadata.split()
            if not separator or len(fields) != 3 or "/" in name:
                _fail("schema source Git tree has an invalid entry")
            mode, kind, child = fields
            _safe_member(name, "schema source Git tree")
            if not re.fullmatch(r"[0-9a-f]{40}", child):
                _fail("schema source Git tree has an invalid object identity")
            serialized.extend(
                mode.lstrip("0").encode()
                + b" "
                + name.encode()
                + b"\0"
                + bytes.fromhex(child)
            )
            entries.append((mode, kind, child, name))
        if _git_object_digest("tree", bytes(serialized)) != oid:
            _fail("schema source tree content does not match committed identity")
        for mode, kind, child, name in entries:
            relative = f"{prefix}/{name}" if prefix else name
            selected = relative == "pyproject.toml" or relative.startswith(
                f"{SCHEMA_SUBDIRECTORY}/"
            )
            ancestor = (
                SCHEMA_SUBDIRECTORY == relative
                or SCHEMA_SUBDIRECTORY.startswith(f"{relative}/")
            )
            if ancestor or (selected and kind == "tree"):
                if mode != "040000" or kind != "tree":
                    _fail("schema source selected path is not a committed directory")
                walk(child, relative)
            elif selected:
                if mode not in {"100644", "100755"} or kind != "blob":
                    _fail(
                        f"schema source selected package has an unsafe Git mode: {relative}"
                    )
                tracked[relative] = mode, child

    walk(tree, "")
    if "pyproject.toml" not in tracked or not any(
        path.startswith(f"{SCHEMA_SUBDIRECTORY}/") for path in tracked
    ):
        _fail("schema source subdirectory is not tracked")
    return tracked


def _git_object_digest(kind: str, data: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(data)}\0".encode() + data).hexdigest()


def _read_authenticated_schema_files(
    custody: _SourceCustody, tracked: Mapping[str, tuple[str, str]]
) -> list[dict[str, Any]]:
    expected_dirs: set[str] = {SCHEMA_SUBDIRECTORY}
    for relative in tracked:
        parts = relative.split("/")
        expected_dirs.update("/".join(parts[:index]) for index in range(1, len(parts)))
    pending = [custody.root / SCHEMA_SUBDIRECTORY]
    physical: set[str] = {"pyproject.toml"}
    while pending:
        directory = pending.pop()
        fd = custody.directory(directory)
        for name in os.listdir(fd):
            target = directory / name
            relative = target.relative_to(custody.root).as_posix()
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                _fail(f"schema source package subtree contains a symlink: {relative}")
            if stat.S_ISDIR(info.st_mode):
                if relative not in expected_dirs:
                    _fail(
                        f"schema source package subtree contains an unowned directory: {relative}"
                    )
                custody.directory(target)
                pending.append(target)
            elif relative not in tracked:
                _fail(
                    f"schema source package subtree contains an unowned file: {relative}"
                )
            else:
                physical.add(relative)
    if physical != set(tracked):
        _fail("schema package source tree is incomplete")
    files = []
    for relative, (mode, blob) in sorted(tracked.items()):
        data = custody.read(custody.root / relative, mode)
        if _git_object_digest("blob", data) != blob:
            _fail(f"schema source bytes differ from committed blob: {relative}")
        files.append(
            {
                "path": relative,
                "mode": mode,
                "blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            }
        )
    return files


def validate_schema_source(schema_source: Path) -> dict[str, Any]:
    """Check selected Git source under the normal maker's OS ownership.

    A bare copied snapshot has no Git authority; it fails closed until the
    maker supplies a separately authenticated selected object-source interface.
    No observed seal or caller-provided UID can substitute for that interface.
    """

    root = Path(schema_source)
    if root.anchor != "/" or ".." in root.parts:
        _fail("schema source must have an absolute physical path")
    try:
        with _SourceCustody(root) as custody:
            fd = custody.directory(root)
            top = _git(fd, "rev-parse", "--show-toplevel").strip()
            if Path(top) != root:
                _fail(
                    "schema source Git root does not match the supplied physical tree"
                )
            if _git(fd, "rev-parse", "HEAD").strip() != SCHEMA_COMMIT:
                _fail("schema source commit is not the selected Agent commit")
            if (
                _git(fd, "rev-parse", f"{SCHEMA_COMMIT}^{{commit}}").strip()
                != SCHEMA_COMMIT
            ):
                _fail("schema source selected commit cannot be authenticated")
            custody.preflight()
            if _git(fd, "status", "--porcelain=v1", "--untracked-files=all"):
                _fail("schema source tree is not clean")
            if any(
                line.startswith("120000 ")
                for line in _git(fd, "ls-files", "-s").splitlines()
            ):
                _fail("schema source tree contains a symlink")
            tree = _git(fd, "rev-parse", f"{SCHEMA_COMMIT}^{{tree}}").strip()
            if not tree or _git(fd, "rev-parse", "HEAD^{tree}").strip() != tree:
                _fail("schema source tree is not bound to the selected Agent commit")
            # Git resolves the pinned object; independently hash its bytes so
            # neither an index flag nor an altered loose object grants custody.
            commit_data = _git(fd, "cat-file", "commit", SCHEMA_COMMIT).encode()
            if commit_data.split(b"\n", 1)[0] != f"tree {tree}".encode():
                _fail("schema source tree is not bound to the selected Agent commit")
            tracked = _tracked_schema_files(fd, tree)
            required = {
                "pyproject.toml",
                f"{SCHEMA_SUBDIRECTORY}/pyproject.toml",
                f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema/__init__.py",
            }
            if not required.issubset(tracked):
                _fail("schema package source tree is incomplete")
            files = _read_authenticated_schema_files(custody, tracked)
            agent_metadata = tomllib.loads(
                custody.read(
                    root / "pyproject.toml", tracked["pyproject.toml"][0]
                ).decode()
            )
            if not _contains_value(agent_metadata, SCHEMA_DECLARATION):
                _fail(
                    "Agent pyproject does not contain the exact selected schema declaration"
                )
            package_metadata = tomllib.loads(
                custody.read(
                    root / SCHEMA_SUBDIRECTORY / "pyproject.toml",
                    tracked[f"{SCHEMA_SUBDIRECTORY}/pyproject.toml"][0],
                ).decode()
            )
            project = package_metadata.get("project")
            if (
                not isinstance(project, Mapping)
                or project.get("name") != SCHEMA_PACKAGE
                or project.get("version") != SCHEMA_VERSION
            ):
                _fail("schema package metadata name/version is not exact")
            nodes = custody.finish()
            return {
                "package": SCHEMA_PACKAGE,
                "version": SCHEMA_VERSION,
                "source_url": "git+https://github.com/banodoco/astrid-agent.git",
                "commit": SCHEMA_COMMIT,
                "tree": tree,
                "subdirectory": SCHEMA_SUBDIRECTORY,
                "content_sha256": _json_digest(files),
                "files": files,
                "custody": {
                    "authority": "maker-real-uid-gid",
                    "uid": custody.uid,
                    "gid": custody.gid,
                    "root": str(root),
                    "nodes": nodes,
                    "reuse": "revalidate; receipt is not an installation lease",
                },
            }
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        _fail(f"schema source physical custody refused: {exc}")


def validate_farm_distribution_inputs(
    *,
    schema_source: Path,
    wheelhouse: Path,
    additional_wheels: Sequence[WheelInput] = (),
) -> dict[str, Any]:
    """Return the maker/Store input receipt after all source/input checks."""

    schema = validate_schema_source(schema_source)
    distributions = validate_wheel_inputs(
        wheelhouse, additional_wheels=additional_wheels
    )
    receipt: dict[str, Any] = {"schema_source": schema, "wheel_inputs": distributions}
    receipt["component_identity"] = _json_digest(receipt)
    return receipt


__all__ = [
    "APPROVED_WHEELS",
    "SCHEMA_COMMIT",
    "SCHEMA_DECLARATION",
    "SCHEMA_PACKAGE",
    "SCHEMA_SUBDIRECTORY",
    "SCHEMA_VERSION",
    "ValidationError",
    "WheelInput",
    "validate_farm_distribution_inputs",
    "validate_schema_source",
    "validate_wheel_inputs",
]
