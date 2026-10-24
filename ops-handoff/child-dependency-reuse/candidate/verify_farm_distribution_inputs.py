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
The five approved wheels are the independently reviewed original packet.  An
additional wheel is admitted only when its caller-supplied expectation agrees
with its filename, metadata, bytes, RECORD, and safe archive contents.  The
caller cannot turn an arbitrary label or digest into source authority.
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

_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_WHEEL_NAME = re.compile(
    r"\A(?P<name>.+)-(?P<version>[^-]+)-(?P<python>[^-]+)-"
    r"(?P<abi>[^-]+)-(?P<platform>[^.]+)\.whl\Z"
)
_SAFE_COMPONENT = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9_.+-]*\Z")


class ValidationError(ValueError):
    """A fail-closed input refusal suitable for the normal maker."""


@dataclass(frozen=True)
class WheelInput:
    """An independently reviewed wheel the maker wants retained.

    The expected identity is checked against the archive.  The fixed five
    packet entries below are the only built-in approvals.  Callers may add a
    source or test wheel with their own reviewed expectation, but cannot omit
    or relabel one of the fixed entries.
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
    """Authenticate the fixed packet and optional reviewed wheel inputs.

    This function does not require schema custody, making it useful for the
    maker's finite input stage.  ``validate_farm_distribution_inputs`` is the
    production gate and additionally requires the exact Agent source tree.
    """

    root = _physical_directory(Path(wheelhouse), "wheelhouse")
    extras = list(additional_wheels)
    extra_by_filename: dict[str, WheelInput] = {}
    for item in extras:
        if item.role not in {"additional-source", "additional-test"}:
            _fail(f"additional wheel role is unsupported: {item.role!r}")
        if not _SAFE_COMPONENT.fullmatch(item.filename) or not item.filename.endswith(".whl"):
            _fail(f"additional wheel filename is unsafe: {item.filename!r}")
        if item.filename in _APPROVED_BY_FILENAME or item.filename in extra_by_filename:
            _fail(f"duplicate wheel identity: {item.filename}")
        if not _SHA256.fullmatch(item.sha256) or item.size <= 0:
            _fail(f"additional wheel expectation is not an exact hash/size: {item.filename}")
        if not item.source or not _SAFE_COMPONENT.fullmatch(item.source):
            _fail(f"additional wheel source is not a stable label: {item.filename}")
        if Path(item.path).name != item.filename or Path(item.path).parent != root:
            _fail(f"additional wheel path must be a direct wheelhouse child: {item.filename}")
        extra_by_filename[item.filename] = item

    expected = {**_APPROVED_BY_FILENAME, **extra_by_filename}
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


def _git(root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True, check=False
        )
    except OSError as exc:
        _fail(f"schema source Git probe failed: {exc}")
    if completed.returncode != 0:
        _fail(f"schema source Git probe refused: git {' '.join(args)}")
    return completed.stdout


def _contains_value(value: object, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, Mapping):
        return any(_contains_value(item, expected) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_contains_value(item, expected) for item in value)
    return False


def validate_schema_source(schema_source: Path) -> dict[str, Any]:
    """Validate a clean Agent checkout containing the selected schema source."""

    root = _physical_directory(Path(schema_source), "schema source")
    top = _git(root, "rev-parse", "--show-toplevel").strip()
    if Path(top).resolve() != root:
        _fail("schema source Git root does not match the supplied physical tree")
    if _git(root, "rev-parse", "HEAD").strip() != SCHEMA_COMMIT:
        _fail("schema source commit is not the selected Agent commit")
    if _git(root, "status", "--porcelain=v1", "--untracked-files=all"):
        _fail("schema source tree is not clean")
    if any(line.startswith("120000 ") for line in _git(root, "ls-files", "-s").splitlines()):
        _fail("schema source tree contains a symlink")

    agent_pyproject = root / "pyproject.toml"
    try:
        agent_metadata = tomllib.loads(_read_regular(agent_pyproject, "Agent pyproject").decode())
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        _fail(f"Agent pyproject is invalid: {exc}")
    if not _contains_value(agent_metadata, SCHEMA_DECLARATION):
        _fail("Agent pyproject does not contain the exact selected schema declaration")

    subpath = root / SCHEMA_SUBDIRECTORY
    if subpath.is_symlink() or not subpath.is_dir() or subpath.resolve() != subpath:
        _fail("selected schema subdirectory is absent or symlinked")
    package_pyproject = subpath / "pyproject.toml"
    try:
        package_metadata = tomllib.loads(
            _read_regular(package_pyproject, "schema package pyproject").decode()
        )
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        _fail(f"schema package pyproject is invalid: {exc}")
    project = package_metadata.get("project")
    if (
        not isinstance(project, Mapping)
        or project.get("name") != SCHEMA_PACKAGE
        or project.get("version") != SCHEMA_VERSION
    ):
        _fail("schema package metadata name/version is not exact")
    package_dir = subpath / "banodoco_timeline_schema"
    init = package_dir / "__init__.py"
    if (
        package_dir.is_symlink()
        or not package_dir.is_dir()
        or init.is_symlink()
        or not init.is_file()
    ):
        _fail("schema package source tree is incomplete")

    tracked = _git(root, "ls-files", "-z", "--", SCHEMA_SUBDIRECTORY).split("\0")
    tracked = [item for item in tracked if item]
    if not tracked:
        _fail("schema source subdirectory is not tracked")
    files: list[dict[str, Any]] = []
    for relative in tracked:
        target = root / relative
        if target.is_symlink() or not target.is_file():
            _fail(f"schema source contains a non-regular tracked file: {relative}")
        data = _read_regular(target, f"schema source {relative}")
        files.append(
            {"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        )
    files.sort(key=lambda item: item["path"])
    return {
        "package": SCHEMA_PACKAGE,
        "version": SCHEMA_VERSION,
        "source_url": "git+https://github.com/banodoco/astrid-agent.git",
        "commit": SCHEMA_COMMIT,
        "subdirectory": SCHEMA_SUBDIRECTORY,
        "tree": _git(root, "rev-parse", "HEAD^{tree}").strip(),
        "content_sha256": _json_digest(files),
        "files": files,
    }


def validate_farm_distribution_inputs(
    *,
    schema_source: Path,
    wheelhouse: Path,
    additional_wheels: Sequence[WheelInput] = (),
) -> dict[str, Any]:
    """Return the maker/Store input receipt after all source/input checks."""

    schema = validate_schema_source(schema_source)
    distributions = validate_wheel_inputs(wheelhouse, additional_wheels=additional_wheels)
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
