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
import json
import marshal
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import types
import venv
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

ENTRY_POINT_TARGET = re.compile(
    r"\A(?P<module>\w+(?:\.\w+)*):(?P<function>\w+(?:\.\w+)*)"
    r"(?:\s*\[\s*[\w-]+(?:=\w+)?(?:,\s*\w+(?:=\w+)?)*\s*\])?\Z"
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


def validated_record_path(root: Path, site: Path, dist: object, record: str, name: str) -> Path:
    pure = PurePosixPath(record)
    if (
        not record
        or "\\" in record
        or "\x00" in record
        or pure.is_absolute()
        or str(pure) != record
        or ".." in pure.parts
    ):
        fail(f"unsafe dependency RECORD ownership: {name}")
    path = site / record
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        fail(f"dependency RECORD escapes child: {name}")
    cursor = site
    for part in pure.parts:
        cursor /= part
        if cursor.is_symlink():
            fail(f"symlinked dependency RECORD: {name}")
    dist_path = getattr(dist, "_path", None)
    if not isinstance(dist_path, Path) or not dist_path.is_absolute() or dist_path.is_symlink():
        fail(f"dependency RECORD ownership is unavailable: {name}")
    if dist_path != dist_path.resolve():
        fail(f"dependency RECORD owner is not physical: {name}")
    dist_resolved = dist_path.resolve()
    if not dist_path.is_relative_to(site) or not dist_resolved.is_relative_to(root):
        fail(f"dependency RECORD owner escapes child: {name}")
    try:
        dist_rel = dist_path.relative_to(site)
    except ValueError:
        fail(f"dependency RECORD owner escapes site-packages: {name}")
    owner_cursor = site
    for part in dist_rel.parts:
        owner_cursor /= part
        if owner_cursor.is_symlink():
            fail(f"symlinked dependency RECORD owner: {name}")
    if resolved != dist_resolved / "RECORD":
        fail(f"dependency RECORD is not owned by distribution: {name}")
    try:
        info = path.stat(follow_symlinks=False)
    except OSError as exc:
        fail(f"cannot stat dependency RECORD: {name}: {exc}")
    if not stat.S_ISREG(info.st_mode):
        fail(f"dependency RECORD is not a regular file: {name}")
    return path


def child_file(root: Path, path: Path) -> None:
    if not path.is_relative_to(root) or not path.resolve().is_relative_to(root):
        fail("installed dependency file escapes child")
    cursor = root
    for part in path.relative_to(root).parts:
        cursor /= part
        info = cursor.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != os.getuid():
            fail("symlinked or foreign installed dependency path")
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        fail("installed dependency path is not a regular file")


# Independently reviewed original input0932 / publication0940. Test-only wheels
# remain in the archive and never enter the bootstrap installation snapshot.
BOOTSTRAP_ARCHIVE_SHA256 = "443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548"
BOOTSTRAP_WHEELS = {
    "pip-26.2.1-py3-none-any.whl": "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
    "setuptools-80.9.0-py3-none-any.whl": "062d34222ad13e0cc312a4c02d73f059e86a4acbfbdea8f8f76b28c99f306922",
    "wheel-0.46.3-py3-none-any.whl": "4b399d56c9d9338230118d705d9737a2a468ccca63d5e813e2a4fc7815d8bc4d",
}
BOOTSTRAP_LOCK = "".join(
    f"{name.split('-')[0]}=={name.split('-')[1]} --hash=sha256:{digest}\n"
    for name, digest in BOOTSTRAP_WHEELS.items()
).encode()


def bootstrap_artifacts(archive_path: Path) -> dict[str, bytes]:
    if not archive_path.is_file() or archive_path.is_symlink():
        fail("missing genuine bootstrap input0932 archive " + str(archive_path) + " SHA256 " + BOOTSTRAP_ARCHIVE_SHA256)
    data = captured_bytes(archive_path)
    if hashlib.sha256(data).hexdigest() != BOOTSTRAP_ARCHIVE_SHA256:
        fail("missing genuine bootstrap input0932 archive SHA256 " + BOOTSTRAP_ARCHIVE_SHA256)
    artifacts = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for name, digest in BOOTSTRAP_WHEELS.items():
            member = archive.getmember("timeline-bootstrap-wheel-input-0932/wheelhouse/" + name)
            if not member.isfile():
                fail("bootstrap archive wheel is not a file")
            stream = archive.extractfile(member)
            if stream is None:
                fail("bootstrap archive wheel is missing")
            content = stream.read()
            if hashlib.sha256(content).hexdigest() != digest:
                fail("bootstrap original wheel hash mismatch: " + name)
            package, version, _, tags = parse_wheel_filename(name)
            archive_identity(content, name, str(package), str(version), set(tags))
            artifacts[name] = content
    return artifacts


def trusted_venv_sources() -> dict[str, bytes]:
    source = Path(venv.__file__).resolve()
    paths = [source, *sorted((source.parent / "scripts/common").rglob("*")),
             *sorted((source.parent / "scripts" / os.name).rglob("*"))]
    result = {}
    for path in paths:
        if path.is_dir():
            continue
        if not path.is_relative_to(Path(sys.base_prefix).resolve()):
            fail("venv source is outside trusted host Python")
        for item in [path, *path.parents]:
            info = item.lstat()
            if info.st_uid != 0 or info.st_mode & 0o022 or stat.S_ISLNK(info.st_mode):
                fail("venv source requires immutable root-owned host Python input")
        result[str(path)] = captured_bytes(path)
    return result


def bootstrap_identity(interpreter: Path) -> str:
    sources = trusted_venv_sources()
    identity = {"inventory": "whole-child-root-v1", "archive": BOOTSTRAP_ARCHIVE_SHA256,
                "lock": hashlib.sha256(BOOTSTRAP_LOCK).hexdigest(),
                "wheels": BOOTSTRAP_WHEELS,
                "python": str(interpreter.resolve()),
                "python_sha256": hashlib.sha256(captured_bytes(interpreter.resolve())).hexdigest(),
                "version": sys.version,
                "venv": {p: hashlib.sha256(b).hexdigest() for p, b in sources.items()}}
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()


def venv_files(root: Path) -> dict[str, bytes]:
    # Render from trusted host templates; never derive authority from child bytes.
    sources = trusted_venv_sources()
    base_executable = Path(sys._base_executable)  # type: ignore[attr-defined]
    context = types.SimpleNamespace(env_dir=str(root), env_name=root.name,
                                    prompt="child", bin_name="bin",
                                    env_exe=str(root / "bin" / base_executable.name))
    builder = venv.EnvBuilder(prompt="child")
    result = {}
    for source, content in sources.items():
        path = Path(source)
        if path.name == "__init__.py":
            continue
        context.script_path = source
        result["bin/" + path.name] = builder.replace_variables(content.decode(), context).encode()
    # A deterministic, non-executable configuration established before pip runs.
    result["pyvenv.cfg"] = (
        f"home = {base_executable.parent}\n"
        "include-system-site-packages = false\n"
        f"version = {'.'.join(map(str, sys.version_info[:3]))}\n"
        "prompt = 'child'\n"
    ).encode()
    return result


def verify_venv_files(root: Path) -> set[str]:
    owned = set()
    for rel, expected in venv_files(root).items():
        child_file(root, root / rel)
        if captured_bytes(root / rel) != expected:
            fail("venv-owned file differs from trusted host source: " + rel)
        owned.add(rel)
    return owned


def retained_bootstrap(root: Path, interpreter: Path) -> dict[str, bytes]:
    authority = bootstrap_identity(interpreter)
    child_file(root, root / ".bootstrap-authority")
    child_file(root, root / ".bootstrap-input.tgz")
    if captured_bytes(root / ".bootstrap-authority") != (authority + "\n").encode():
        fail("retained bootstrap source/interpreter authority mismatch")
    artifacts = bootstrap_artifacts(root / ".bootstrap-input.tgz")
    seed = root / ".bootstrap-wheelhouse"
    if seed != seed.resolve() or {p.name for p in seed.iterdir()} != {"requirements.txt", *artifacts}:
        fail("retained bootstrap snapshot inventory mismatch")
    for name, data in {"requirements.txt": BOOTSTRAP_LOCK, **artifacts}.items():
        child_file(root, seed / name)
        if captured_bytes(seed / name) != data:
            fail("retained bootstrap snapshot differs from original input: " + name)
    return artifacts


# The component is imported only from the reviewed maker kit, never its inputs.
FARM_COMPONENT_SHA256 = "c2163184ed51e893c6d194930c061474de08bfe707907a2f43abb5332b62397d"


def farm_component():
    path = Path(__file__).with_name("verify_farm_distribution_inputs.py")
    data = captured_bytes(path)
    if path != path.resolve() or hashlib.sha256(data).hexdigest() != FARM_COMPONENT_SHA256:
        fail("untrusted Farm distribution component")
    module = types.ModuleType("farm_distribution_inputs")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    # Execute these authenticated source bytes; a timestamp-matching pyc is
    # neither the reviewed component nor an additional source authority.
    exec(compile(data, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def farm_inputs(schema_source: Path, archive_path: Path) -> dict:
    component = farm_component()
    data = captured_bytes(archive_path)
    if hashlib.sha256(data).hexdigest() != BOOTSTRAP_ARCHIVE_SHA256:
        fail("Farm requires genuine reviewed original five-wheel archive")
    # This private, temporary extraction is never an installed-source authority.
    with tempfile.TemporaryDirectory(prefix="farm-inputs-") as temporary:
        wheelhouse = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for item in component.APPROVED_WHEELS:
                member = archive.getmember("timeline-bootstrap-wheel-input-0932/wheelhouse/" + item.filename)
                if not member.isfile() or member.size != item.size:
                    fail("Farm original wheel archive member mismatch")
                stream = archive.extractfile(member)
                if stream is None:
                    fail("Farm original wheel is missing")
                (wheelhouse / item.filename).write_bytes(stream.read())
        return component.validate_farm_distribution_inputs(schema_source=schema_source, wheelhouse=wheelhouse)


def schema_archive(receipt: dict) -> bytes:
    schema = receipt["schema_source"]
    source = schema["custody"]["root"]
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS="0")
    data = subprocess.check_output(
        ["git", "--no-replace-objects", "-C", source, "archive", "--format=tar",
         schema["commit"] + ":" + schema["subdirectory"]], env=env)
    prefix = schema["subdirectory"] + "/"
    expected = {item["path"][len(prefix):]: item for item in schema["files"] if item["path"].startswith(prefix)}
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for entry in archive:
            pure = PurePosixPath(entry.name)
            if pure.is_absolute() or ".." in pure.parts or str(pure) != entry.name or entry.name in seen:
                fail("unsafe schema Git archive path")
            seen.add(entry.name)
            if entry.isdir():
                if not any(name.startswith(entry.name + "/") for name in expected):
                    fail("unowned schema Git archive directory")
                continue
            item = expected.get(entry.name)
            if not entry.isfile() or item is None:
                fail("unowned schema Git archive file")
            stream = archive.extractfile(entry)
            if stream is None:
                fail("missing schema Git archive content")
            content = stream.read()
            if (len(content) != item["size"] or hashlib.sha256(content).hexdigest() != item["sha256"]
                    or entry.mode != int(item["mode"], 8) & 0o777):
                fail("schema Git archive differs from authenticated selected blobs")
    if set(expected) != {name for name in seen if name in expected}:
        fail("incomplete schema Git archive")
    return data


def farm_test_inputs(receipt: dict, archive_path: Path) -> tuple[bytes, dict[str, bytes]]:
    artifacts = {}
    lock = []
    with tarfile.open(fileobj=io.BytesIO(captured_bytes(archive_path))) as archive:
        for item in receipt["wheel_inputs"]["distributions"]:
            if item["role"] == "test2":
                stream = archive.extractfile("timeline-bootstrap-wheel-input-0932/wheelhouse/" + item["filename"])
                if stream is None:
                    fail("missing Farm original test wheel")
                artifacts[item["filename"]] = stream.read()
                lock.append(f'{item["name"]}=={item["version"]} --hash=sha256:{item["sha256"]}\n')
    return "".join(lock).encode(), artifacts


def prepare_farm(root: Path, source: Path, authority: str) -> None:
    receipt = farm_inputs(source, root / ".bootstrap-input.tgz")
    if receipt["component_identity"] != authority:
        fail("Farm inputs changed before staging")
    data = schema_archive(receipt)
    snapshot = next(root.glob(".child-venv-source-*")) / "schema"
    snapshot.mkdir(mode=0o700)
    # Only the authenticated archive file set is materialized, never .git or a
    # new object backend. The original selected Git checkout remains required.
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for entry in archive:
            target = snapshot / entry.name
            if entry.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(entry)
                if stream is None:
                    fail("missing schema Git archive content")
                target.write_bytes(stream.read())
                target.chmod(entry.mode & 0o777)
    carrier = root / ".source-inputs/schema.tar"
    carrier.write_bytes(data)
    carrier.chmod(0o400)
    lock, artifacts = farm_test_inputs(receipt, root / ".bootstrap-input.tgz")
    write_snapshot(root / ".farm-test-wheelhouse", lock, artifacts)
    path = root / ".farm-receipt.json"
    path.write_bytes(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode())
    path.chmod(0o400)
    retained_farm(root, authority)


def retained_farm(root: Path, authority: str | None = None) -> tuple[dict, dict[str, bytes], set[str]]:
    custody = farm_component()._SourceCustody(root)
    with custody:
        return _retained_farm(root, authority, custody)


def _retained_farm(root: Path, authority: str | None, custody) -> tuple[dict, dict[str, bytes], set[str]]:
    custody.directory(root)
    marker = root / ".farm-receipt.json"
    child_file(root, marker)
    if marker.stat().st_size > 4 * 1024 * 1024:
        fail("oversized Farm receipt")
    raw = custody.read(marker, "100644")
    custody.read(root / ".bootstrap-input.tgz", "100644")
    claimed = json.loads(raw)
    source = Path(claimed["schema_source"]["custody"]["root"])
    receipt = farm_inputs(source, root / ".bootstrap-input.tgz")
    if (raw != json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
            or (authority is not None and receipt["component_identity"] != authority)):
        fail("retained Farm receipt/source authority mismatch")
    carrier = root / ".source-inputs/schema.tar"
    child_file(root, carrier)
    if custody.read(carrier, "100644") != schema_archive(receipt):
        fail("retained schema archive differs from original selected source")
    lock, artifacts = farm_test_inputs(receipt, root / ".bootstrap-input.tgz")
    seed = root / ".farm-test-wheelhouse"
    if seed.is_symlink() or seed != seed.resolve() or {path.name for path in seed.iterdir()} != {"requirements.txt", *artifacts}:
        fail("retained Farm test2 inventory mismatch")
    for name, content in {"requirements.txt": lock, **artifacts}.items():
        child_file(root, seed / name)
        if custody.read(seed / name, "100644") != content:
            fail("retained Farm test2 differs from original wheel role/bytes")
    owned = {marker.name, carrier.relative_to(root).as_posix()}
    owned.update(".farm-test-wheelhouse/" + name for name in {"requirements.txt", *artifacts})
    custody.finish()
    return receipt, artifacts, owned


def store_metadata(root: Path, interpreter: Path) -> set[str]:
    marker = root / ".bench-owner.json"
    if not marker.exists() and not marker.is_symlink():
        return set()
    child_file(root, marker)
    store = root.parent.parent
    if root.parent.name not in {"staging", "entries"} or store != store.resolve():
        fail("Store metadata is outside normal child custody")
    owner = json.loads(captured_bytes(store / "owner.json"))
    value = json.loads(captured_bytes(marker))
    if set(value) != {"owner", "component", "key", "identity"} or value["component"] != "child" or value["owner"] != owner["id"] or owner["root"] != str(store):
        fail("retained Store ownership metadata mismatch")
    identity = value["identity"]
    if set(identity) not in ({"agent_sha", "backend_sha", "client_tuple", "bootstrap_authority"},
                             {"agent_sha", "backend_sha", "client_tuple", "bootstrap_authority", "farm_authority"}) or identity["bootstrap_authority"] != bootstrap_identity(interpreter):
        fail("Store child lacks genuine bootstrap authority")
    parts = ["child", identity["agent_sha"], identity["backend_sha"], identity["client_tuple"], identity["bootstrap_authority"]]
    if "farm_authority" in identity:
        if not isinstance(identity["farm_authority"], str) or not re.fullmatch("[0-9a-f]{64}", identity["farm_authority"]):
            fail("Store child lacks genuine Farm authority")
        receipt, _, _ = retained_farm(root, identity["farm_authority"])
        parts.append(receipt["component_identity"])
    elif (root / ".farm-receipt.json").exists() or (root / ".farm-receipt.json").is_symlink():
        fail("Farm child lacks authenticated Store identity")
    key = hashlib.sha256(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if value["key"] != key or root.name != (("child-" if root.parent.name == "entries" else "") + key):
        fail("retained Store key differs from bootstrap/source identity")
    if captured_bytes(marker) != json.dumps(value, sort_keys=True, separators=(",", ":")).encode():
        fail("noncanonical retained Store metadata")
    return {marker.name}


def installed_integrity(
    root: Path,
    artifacts: dict[str, bytes],
    *,
    interpreter: Path | None = None,
    local_inventory: dict[str, set[str]] | None = None,
    bootstrap: bool = False,
) -> None:
    """Compare installed bytes to authenticated original wheels, not RECORD claims."""
    if not root.is_absolute() or root != root.resolve() or root.stat().st_uid != os.getuid():
        fail("installed child root is not physical or owned")
    sites = list((root / "lib").glob("python*/site-packages"))
    if (len(sites) != 1 or root.is_symlink() or sites[0].is_symlink()
            or sites[0] != root / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"):
        fail("installed child layout is missing or ambiguous")
    site = sites[0]
    if site != site.resolve() or not site.is_relative_to(root):
        fail("installed site-packages escapes child")
    distributions = list(md.distributions(path=[str(site)]))
    # Distribution.files reads RECORD internally. Validate its physical owner
    # before asking importlib.metadata to read either metadata or the file list.
    for dist in distributions:
        dist_path = getattr(dist, "_path", None)
        if not isinstance(dist_path, Path) or not dist_path.is_relative_to(site):
            fail("dependency RECORD owner escapes child")
        record_path = validated_record_path(root, site, dist, str(dist_path.relative_to(site) / "RECORD"), "installed")
        child_file(root, record_path)
        child_file(root, dist_path / "METADATA")
    # Only the maker's committed-source verifier can supply local ownership.
    # This is deliberately not an on-disk/CLI allowlist or a package exemption.
    local_inventory = local_inventory or {}
    allowed_local = {"astrid", "astrid-runtime", "__root__"}
    if (root / ".farm-receipt.json").exists() or (root / ".farm-receipt.json").is_symlink():
        if not bootstrap:
            fail("Farm requires authenticated complete-root bootstrap")
        receipt, farm_wheels, farm_owned = retained_farm(root)
        if artifacts.keys() & farm_wheels.keys():
            fail("Farm test2 overlaps dependency/bootstrap role")
        artifacts = {**artifacts, **farm_wheels}
        local_inventory = dict(local_inventory)
        local_inventory["__root__"] = set(local_inventory.get("__root__", set())) | farm_owned
        if receipt["schema_source"]["package"] not in local_inventory:
            fail("Farm schema requires authenticated committed-source inventory")
        allowed_local.add(receipt["schema_source"]["package"])
    if set(local_inventory) - allowed_local:
        fail("unsupported local distribution ownership")
    # __root__ is supplied only by the authenticated committed-source verifier,
    # after validating each maker/Store/source file. It is never read from disk.
    root_owned = local_inventory.pop("__root__", set())
    owned: set[str] = verify_venv_files(root) if bootstrap else set()
    for rel in root_owned:
        child_file(root, root / rel)
        owned.add(rel)
    if bootstrap:
        owned.update(store_metadata(root, interpreter or Path(sys.executable)))
        retained_bootstrap(root, interpreter or Path(sys.executable))
        owned.update({".bootstrap-authority", ".bootstrap-input.tgz"})
        owned.update(".bootstrap-wheelhouse/" + name for name in {"requirements.txt", *BOOTSTRAP_WHEELS})
    expected_distributions: set[object] = set()
    for dist in distributions:
        name = canonicalize_name(dist.metadata.get("Name", ""))
        if name in local_inventory:
            expected_distributions.add(getattr(dist, "_path", None))
            for rel in local_inventory[name]:
                path = site / rel
                child_file(root, path)
                physical = str(path.resolve().relative_to(root))
                if physical in owned:
                    fail("overlapping local distribution ownership")
                owned.add(physical)
    for filename, data in artifacts.items():
        name, version, _, _ = parse_wheel_filename(filename)
        matches = [dist for dist in distributions
                   if canonicalize_name(dist.metadata.get("Name", "")) == name]
        if len(matches) != 1 or matches[0].version != str(version):
            fail(f"missing or ambiguous installed dependency: {name}")
        dist = matches[0]
        expected_distributions.add(getattr(dist, "_path", None))
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
        generated_scripts: dict[str, set[bytes]] = {}
        entrypoint_files = [
            rel for rel in wheel_files if rel == str(Path(record).parent / "entry_points.txt")
        ]
        if len(entrypoint_files) > 1:
            fail(f"ambiguous console entry-point metadata: {name}")
        if entrypoint_files:
            parser = configparser.ConfigParser(interpolation=None, strict=True)
            parser.optionxform = str  # type: ignore[method-assign, assignment]
            try:
                parser.read_string(wheel_files[entrypoint_files[0]].decode("utf-8"))
                if parser.defaults():
                    fail(f"unsupported default console entry-point metadata: {name}")
                entrypoints = (
                    list(parser.items("console_scripts", raw=True))
                    if parser.has_section("console_scripts")
                    else []
                )
            except (configparser.Error, UnicodeDecodeError) as exc:
                fail(f"malformed console entry-point metadata: {name}: {exc}")
            if name == "pip" and filename in BOOTSTRAP_WHEELS and hashlib.sha256(data).hexdigest() == BOOTSTRAP_WHEELS[filename]:
                # pip's authenticated installer emits the versioned pip alias.
                entrypoints.append((f"pip{sys.version_info.major}.{sys.version_info.minor}", "pip._internal.cli.main:main"))
            for script_name, target in entrypoints:
                if (
                    not script_name
                    or "/" in script_name
                    or "\\" in script_name
                    or "\x00" in script_name
                    or any(character.isspace() for character in script_name)
                    or script_name.startswith("[")
                    or script_name in {".", ".."}
                ):
                    fail(f"unsafe console entry-point name: {name}:{script_name!r}")
                match = ENTRY_POINT_TARGET.fullmatch(target)
                if match is None:
                    fail(f"malformed console entry-point target: {name}:{script_name}")
                module = match.group("module")
                function = match.group("function")
                script_path = root / "bin" / script_name
                rel = str(Path(os.path.relpath(script_path, site)))
                if rel in generated_scripts:
                    fail(f"duplicate console entry-point script: {name}:{script_name}")
                body = (
                    "import sys\n"
                    f"from {module} import {function.split('.', 1)[0]}\n"
                    "if __name__ == '__main__':\n"
                    "    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n"
                    f"    sys.exit({function}())\n"
                ).encode()
                executable = str(root / "bin/python")
                if " " in executable:
                    executable = '"' + executable + '"'
                # Pip's long-path shell trampoline survives maker relocation.
                generated_scripts[rel] = {
                    f"#!{executable}\n".encode() + body,
                    (f"#!/bin/sh\n'''exec' {executable} \"$0\" \"$@\"\n' '''\n").encode() + body,
                }
        rows: set[str] = set()
        physical_rows: set[str] = set()
        record_path = validated_record_path(root, site, dist, record, name)
        child_file(root, record_path)
        for row in csv.reader(io.StringIO(captured_bytes(record_path).decode()), strict=True):
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
            child_file(root, resolved)
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
                if content not in generated_scripts[rel]:
                    fail(f"generated dependency script differs from wheel entry point: {rel}")
            elif Path(rel).parent != Path(record).parent or Path(rel).name not in {"INSTALLER", "REQUESTED"}:
                fail(f"unowned installed dependency file: {rel}")
            elif content != (b"pip\n" if Path(rel).name == "INSTALLER" else b""):
                fail(f"unexpected installer bookkeeping: {rel}")
            digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
            if encoded != "sha256=" + digest or size != str(len(content)):
                fail(f"dependency RECORD integrity mismatch: {rel}")
        if not set(wheel_files).issubset(rows):
            fail(f"incomplete installed dependency: {name}")
        if record not in rows:
            fail(f"missing installed dependency RECORD self-row: {name}")
        if not set(generated_scripts).issubset(rows):
            fail(f"missing installed console script: {name}")
        for prefix in {Path(rel).parts[0] for rel in wheel_files}:
            location = site / prefix
            for path in ([location] if location.is_file() else location.rglob("*")):
                if path.is_symlink():
                    fail(f"symlinked dependency package path: {path.name}")
                if path.is_file() and str(path.relative_to(site)) not in rows:
                    fail(f"unowned dependency package file: {path.name}")
        owned.update(physical_rows)

    # Reconcile every installed file, including metadata not discovered by
    # importlib and executables outside active package prefixes.
    for dist in distributions:
        if getattr(dist, "_path", None) not in expected_distributions:
            name = canonicalize_name(dist.metadata.get("Name", ""))
            if name in {"pip", "setuptools", "wheel"}:
                fail(f"missing authenticated original bootstrap wheel: {name}=={dist.version}")
            fail(f"unowned installed distribution: {name}")
    maker = (interpreter or Path(sys.executable)).resolve()
    if maker.is_relative_to(root):
        fail("maker interpreter must be outside the installed child")
    maker_bytes = captured_bytes(maker)
    aliases = {"python", "python3"}
    if re.fullmatch(r"python3\.[0-9]+", maker.name):
        aliases.add(maker.name)
    if bootstrap:
        aliases.add(f"python{sys.version_info.major}.{sys.version_info.minor}")
    for alias in aliases:
        path = root / "bin" / alias
        if bootstrap and not path.exists():
            fail("missing bootstrap interpreter: bin/" + alias)
        if path.exists() or path.is_symlink():
            child_file(root, path)
            if captured_bytes(path) != maker_bytes:
                fail("child interpreter differs from maker interpreter")
            physical = str(path.relative_to(root))
            if physical in owned:
                fail("dependency RECORD overlaps bootstrap interpreter")
            owned.add(physical)
    if "bin/python" not in owned:
        fail("missing bootstrap interpreter: bin/python")
    # Only ancestors of authenticated files and the exact empty venv include
    # layout are structural directories. No namespace grants file ownership.
    allowed_dirs = {root, root / "lib", site.parent, site, root / "include", root / "include" / f"python{sys.version_info.major}.{sys.version_info.minor}"}
    for rel in owned:
        allowed_dirs.update((root / rel).parents)
    for path in root.rglob("*"):
        info = path.lstat()
        if info.st_uid == os.getuid() and stat.S_ISLNK(info.st_mode) and path == root / "lib64" and path.readlink() == Path("lib") and (root / "lib") == (root / "lib").resolve():
            continue
        if stat.S_ISDIR(info.st_mode):
            if info.st_uid != os.getuid() or path not in allowed_dirs:
                fail(f"unowned installed directory: {path.relative_to(root)}")
            continue
        child_file(root, path)
        if str(path.relative_to(root)) not in owned:
            fail(f"unowned installed file: {path.relative_to(root)}")


def install_snapshot(wheelhouse: Path, requirements: bytes, flags: list[str], *, python: str | None = None) -> None:
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
        command = [python or sys.executable, "-I", "-m", "pip"]
        bootstrap_flags = []
        if wheelhouse.name == ".bootstrap-wheelhouse":
            pip_name = next(name for name in BOOTSTRAP_WHEELS if name.startswith("pip-"))
            if captured_bytes(wheelhouse / "requirements.txt") != BOOTSTRAP_LOCK or hashlib.sha256(captured_bytes(wheelhouse / pip_name)).hexdigest() != BOOTSTRAP_WHEELS[pip_name]:
                fail("bootstrap installer differs from original pip wheel")
            bootstrap_flags = ["--ignore-installed"]
            command = [python or sys.executable, "-I", "-c",
                       "import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('pip',run_name='__main__')",
                       f"/proc/self/fd/{directory_fd}/{pip_name}"]
        subprocess.run([*command, "install", *bootstrap_flags, *flags,
                        "--no-index", "--find-links", f"/proc/self/fd/{directory_fd}",
                        "--require-hashes", "--no-deps", "-r", f"/proc/self/fd/{lock_fd}"],
                       pass_fds=(lock_fd, directory_fd), check=True)
    finally:
        os.close(directory_fd)
        os.close(lock_fd)


def main(*, local_inventory: dict[str, set[str]] | None = None) -> int:
    interpreter: Path | None = None
    args = sys.argv[1:]
    if args and args[0] == "--farm-inputs":
        print(json.dumps(farm_inputs(Path(args[1]), Path(args[2])), sort_keys=True, separators=(",", ":")))
        return 0
    if args and args[0] == "--verify-farm":
        retained_farm(Path(args[1]), args[2])
        return 0
    if args and args[0] == "--prepare-farm":
        prepare_farm(Path(args[1]), Path(args[2]), args[3])
        return 0
    if args and args[0] == "--bootstrap-identity":
        print(bootstrap_identity(Path(args[1])))
        return 0
    if args and args[0] == "--verify-bootstrap":
        root, interpreter = map(Path, args[1:])
        installed_integrity(root, retained_bootstrap(root, interpreter), interpreter=interpreter, bootstrap=True)
        return 0
    if args and args[0] == "--prepare-bootstrap":
        archive, root, interpreter = map(Path, args[1:])
        artifacts = bootstrap_artifacts(archive)
        authority = bootstrap_identity(interpreter)
        write_snapshot(root / ".bootstrap-wheelhouse", BOOTSTRAP_LOCK, artifacts)
        (root / ".bootstrap-input.tgz").write_bytes(captured_bytes(archive))
        (root / ".bootstrap-authority").write_text(authority + "\n")
        (root / "pyvenv.cfg").write_bytes(venv_files(root)["pyvenv.cfg"])
        verify_venv_files(root)
        # Interpreter copies are checked before any dependent wheel executes.
        for alias in ("python", "python3", f"python3.{sys.version_info.minor}"):
            child_file(root, root / "bin" / alias)
            if captured_bytes(root / "bin" / alias) != captured_bytes(interpreter.resolve()):
                fail("child interpreter differs from maker interpreter")
        installed_integrity(root, {}, interpreter=interpreter, bootstrap=True)
        return 0
    bootstrap_root = None
    if "--bootstrap-root" in args:
        index = args.index("--bootstrap-root")
        bootstrap_root = Path(args[index + 1])
        args = args[:index] + args[index + 2:]
    install_python = None
    if "--install-python" in args:
        index = args.index("--install-python")
        install_python = args[index + 1]
        args = args[:index] + args[index + 2:]
    interpreter = None
    if "--maker-python" in args:
        index = args.index("--maker-python")
        if len(args) <= index + 1:
            fail("maker interpreter path is missing")
        executable = shutil.which(args[index + 1])
        if executable is None:
            fail("maker interpreter is unavailable")
        interpreter = Path(executable)
        args = args[:index] + args[index + 2:]
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
        if bootstrap_root is not None:
            if bootstrap_root != installed or interpreter is None:
                fail("bootstrap verification requires exact child and maker interpreter")
            bootstrap_wheels = retained_bootstrap(installed, interpreter)
            if artifacts.keys() & bootstrap_wheels.keys():
                fail("dependency seed overlaps bootstrap wheels")
            artifacts.update(bootstrap_wheels)
        local_inventory = dict(local_inventory or {})
        root_owned = set(local_inventory.get("__root__", set()))
        root_owned.update(str((wheelhouse / name).relative_to(installed)) for name in {"requirements.txt", *(path.name for path, _ in matched.values())})
        req = installed / ".provision-requirements.txt"
        if req.exists():
            child_file(installed, req)
            if captured_bytes(req) != requirements_bytes:
                fail("retained provision requirements differ from committed lock")
            root_owned.add(req.name)
        local_inventory["__root__"] = root_owned
        installed_integrity(installed, artifacts, interpreter=interpreter, local_inventory=local_inventory,
                            bootstrap=bootstrap_root is not None)
    if install_flags is not None:
        if wheelhouse.name == ".farm-test-wheelhouse":
            retained_farm(wheelhouse.parent)
        install_snapshot(wheelhouse, requirements_bytes, install_flags, python=install_python)
    if snapshot is not None:
        write_snapshot(snapshot, requirements_bytes, artifacts)
        print(f"verified dependency seed snapshot={snapshot} packages={len(matched)}")
    else:
        print(f"verified dependency seed wheelhouse={wheelhouse} packages={len(matched)}")
    return 0


if __name__ == "__main__":
    main()
