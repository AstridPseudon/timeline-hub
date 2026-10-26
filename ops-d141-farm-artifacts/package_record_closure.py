#!/usr/bin/env python3
"""Build a portable, RECORD-exact D141 installed-schema transport.

This is deliberately narrower than the child maker.  It reads the already
approved installed distribution, validates the maker's fixed TRUSTED_SCHEMA
literal and PEP 610 identity, then packages only the 18 RECORD entries.  It
never invokes a child, provisioner, registry, Store, network, or installer.
"""

from __future__ import annotations

import argparse
import base64
import csv
import gzip
import hashlib
import io
import json
import os
import pathlib
import re
import stat
import tarfile
import tempfile
from typing import Any


EXPECTED_MAKER_SHA256 = (
    "fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5"
)
EXPECTED_MANIFEST_SHA256 = (
    "c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d"
)
EXPECTED_RECORD_SHA256 = (
    "844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220"
)
EXPECTED_DIRECT_URL_SHA256 = (
    "b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e"
)
EXPECTED_UNHASHED = {
    "banodoco_timeline_schema-0.0.2.dist-info/RECORD",
    "banodoco_timeline_schema/__pycache__/__init__.cpython-313.pyc",
    "banodoco_timeline_schema/__pycache__/generated.cpython-313.pyc",
    "banodoco_timeline_schema/__pycache__/materialize.cpython-313.pyc",
    "banodoco_timeline_schema/__pycache__/theme.cpython-313.pyc",
    "banodoco_timeline_schema/__pycache__/validate.cpython-313.pyc",
}
TRANSPORT_ROOT = (
    "timeline-d141-schema-record-closure-"
    "c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d"
)
MAX_ARCHIVE_BYTES = 20 * 1024 * 1024
DIST_INFO = "banodoco_timeline_schema-0.0.2.dist-info"
RECORD_PATH = f"{DIST_INFO}/RECORD"
DIRECT_PATH = f"{DIST_INFO}/direct_url.json"
SAFE_RECEIVER = {
    "preflight": "python3 -I package_record_closure.py --verify-archive ARCHIVE --expected-sha256 MANAGER_PEER_SHA256",
    "extract": "tar --extract --gzip --file ARCHIVE --no-same-owner --same-permissions --keep-old-files --directory STAGE",
    "gate": "independent corrected review PASS; private empty physical STAGE; verified immutable archive; no TAR_OPTIONS",
    "binding": f"SCHEMA_INSTALLED_DISTRIBUTION=STAGE/{TRANSPORT_ROOT}/site-packages/{DIST_INFO}",
}
DIRECT_URL_SECRET = re.compile(
    rb"(?:token|secret|password|passwd|api[_-]?key|authorization|bearer)\s*[:=]|@",
    re.IGNORECASE,
)


class Refusal(RuntimeError):
    """A source or transport safety check failed."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def strict_json(data: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in pairs:
            if key in result:
                raise Refusal("duplicate JSON key")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise Refusal("nonstandard JSON constant")

    try:
        result = json.loads(data, object_pairs_hook=unique, parse_constant=invalid_constant)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise Refusal("invalid JSON") from error
    if not isinstance(result, dict):
        raise Refusal("JSON metadata must be an object")
    return result


def physical(path: pathlib.Path, kind: str, *, directory: bool = False) -> os.stat_result:
    try:
        info = path.lstat()
    except OSError as error:
        raise Refusal(f"missing {kind}: {path}") from error
    if path.resolve() != path or stat.S_ISLNK(info.st_mode):
        raise Refusal(f"{kind} must be a physical path: {path}")
    if not directory and (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1):
        raise Refusal(f"{kind} must be a regular single-link file: {path}")
    if directory and not stat.S_ISDIR(info.st_mode):
        raise Refusal(f"{kind} must be a directory: {path}")
    if info.st_uid not in {0, os.getuid()} or info.st_mode & 0o022:
        raise Refusal(f"{kind} has unsafe ownership or mode: {path}")
    return info


def extract_trusted_schema(maker: pathlib.Path) -> tuple[dict[str, str], str]:
    info = physical(maker, "maker")
    maker_bytes = maker.read_bytes()
    maker_sha = sha256(maker_bytes)
    if maker_sha != EXPECTED_MAKER_SHA256:
        raise Refusal("maker bytes are not the reviewed D139a copy")
    pattern = re.compile(
        r"TRUSTED_SCHEMA\s*=\s*\{'url':\s*'([^']+)',\s*"
        r"'commit':\s*'([0-9a-f]{40})',\s*"
        r"'subdirectory':\s*'([^']+)',\s*"
        r"'source_tree':\s*'([0-9a-f]{40})'\s*\}",
    )
    match = pattern.search(maker_bytes.decode("utf-8"))
    if not match:
        raise Refusal("maker TRUSTED_SCHEMA literal is missing or changed")
    schema = dict(zip(("url", "commit", "subdirectory", "source_tree"), match.groups()))
    if set(schema) != {"url", "commit", "subdirectory", "source_tree"}:
        raise Refusal("maker TRUSTED_SCHEMA does not have the approved four keys")
    if sha256(json_bytes(schema)) != EXPECTED_MANIFEST_SHA256:
        raise Refusal("maker TRUSTED_SCHEMA does not match the approved manifest digest")
    if info.st_nlink != 1:
        raise Refusal("maker is hard-linked")
    return schema, maker_sha


def safe_record_path(value: str) -> None:
    pure = pathlib.PurePosixPath(value)
    if not value or "\\" in value or str(pure) != value or pure.is_absolute() or ".." in pure.parts:
        raise Refusal(f"unsafe RECORD path: {value!r}")


def inspect_distribution(dist: pathlib.Path, schema: dict[str, str]) -> dict[str, Any]:
    physical(dist, "distribution directory", directory=True)
    if dist.name != "banodoco_timeline_schema-0.0.2.dist-info":
        raise Refusal("unexpected schema dist-info name")
    site = dist.parent
    physical(site, "site-packages directory", directory=True)
    package = site / "banodoco_timeline_schema"
    physical(package, "schema package directory", directory=True)
    record_path = dist / "RECORD"
    direct_path = dist / "direct_url.json"
    record_info = physical(record_path, "RECORD")
    direct_info = physical(direct_path, "direct_url.json")
    record_bytes = record_path.read_bytes()
    direct_bytes = direct_path.read_bytes()
    if sha256(record_bytes) != EXPECTED_RECORD_SHA256:
        raise Refusal("RECORD digest does not match the approved closure")
    if sha256(direct_bytes) != EXPECTED_DIRECT_URL_SHA256:
        raise Refusal("direct_url digest does not match the approved receipt")
    direct = strict_json(direct_bytes)
    expected_direct = {
        "subdirectory": schema["subdirectory"],
        "url": schema["url"],
        "vcs_info": {
            "commit_id": schema["commit"],
            "requested_revision": schema["commit"],
            "vcs": "git",
        },
    }
    if direct != expected_direct:
        raise Refusal("direct_url.json is not bound to the approved source identity")
    if DIRECT_URL_SECRET.search(direct_bytes):
        raise Refusal("direct_url.json contains a secret-like value; publication stopped")

    rows = list(csv.reader(io.StringIO(record_bytes.decode("utf-8")), strict=True))
    if len(rows) != 18:
        raise Refusal(f"RECORD row count is {len(rows)}, expected 18")
    paths: set[str] = set()
    entries: list[dict[str, Any]] = []
    for row in rows:
        if len(row) != 3:
            raise Refusal("malformed RECORD row")
        rel, encoded, size = row
        safe_record_path(rel)
        if rel in paths:
            raise Refusal(f"duplicate RECORD path: {rel}")
        paths.add(rel)
        target = site / pathlib.PurePosixPath(rel)
        if target.resolve() != target:
            raise Refusal(f"RECORD path escapes site-packages: {rel}")
        info = physical(target, f"RECORD target {rel}")
        data = target.read_bytes()
        digest = sha256(data)
        hashed = bool(encoded or size)
        if hashed:
            expected_encoded = "sha256=" + base64.urlsafe_b64encode(
                hashlib.sha256(data).digest()
            ).decode().rstrip("=")
            if encoded != expected_encoded or size != str(len(data)):
                raise Refusal(f"RECORD bytes mismatch: {rel}")
        elif rel not in EXPECTED_UNHASHED:
            raise Refusal(f"unapproved unhashed RECORD row: {rel}")
        entries.append(
            {
                "path": rel,
                "bytes": len(data),
                "sha256": digest,
                "record_hashed": hashed,
                "mode": format(stat.S_IMODE(info.st_mode), "04o"),
                "uid": info.st_uid,
                "gid": info.st_gid,
                "nlink": info.st_nlink,
            }
        )
    if sum(entry["record_hashed"] for entry in entries) != 12:
        raise Refusal("RECORD hashed row count is not 12")
    if {entry["path"] for entry in entries if not entry["record_hashed"]} != EXPECTED_UNHASHED:
        raise Refusal("RECORD unhashed rows do not match the six approved names")
    actual = {
        path.relative_to(site).as_posix()
        for root in (package, dist)
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != paths:
        raise Refusal("installed distribution has an unlisted or missing file")
    directories = {"."}
    for rel in paths:
        directories.update(str(parent) for parent in pathlib.PurePosixPath(rel).parents if str(parent) != ".")
    directory_entries = []
    for rel in sorted(directories):
        path = site if rel == "." else site / pathlib.PurePosixPath(rel)
        info = physical(path, f"closure directory {rel}", directory=True)
        directory_entries.append(
            {"path": rel, "mode": format(stat.S_IMODE(info.st_mode), "04o"), "uid": info.st_uid, "gid": info.st_gid}
        )
    return {
        "source_dist_info": dist.name,
        "record": {
            "path": "banodoco_timeline_schema-0.0.2.dist-info/RECORD",
            "bytes": record_info.st_size,
            "sha256": sha256(record_bytes),
            "rows": len(entries),
            "hashed_rows": sum(entry["record_hashed"] for entry in entries),
            "unhashed_rows": sorted(EXPECTED_UNHASHED),
        },
        "direct_url": {
            "path": "banodoco_timeline_schema-0.0.2.dist-info/direct_url.json",
            "bytes": direct_info.st_size,
            "sha256": sha256(direct_bytes),
            "privacy_checked": True,
            "raw_content_published": False,
            "pinned_identity_match": True,
        },
        "files": sorted(entries, key=lambda item: item["path"]),
        "directories": directory_entries,
        "closure_file_count": len(entries),
        "closure_bytes": sum(entry["bytes"] for entry in entries),
        "ownership_policy": "uid/gid and non-writable modes recorded; no symlink or hardlink permitted",
    }


def atomic_write(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(path, flags, 0o644)
    except FileExistsError:
        if path.read_bytes() != data:
            raise Refusal(f"refusing to overwrite immutable output: {path}")
        return
    with os.fdopen(fd, "wb") as output:
        output.write(data)


def add_tar_bytes(tar: tarfile.TarFile, name: str, data: bytes, mode: int, uid: int, gid: int) -> None:
    info = tarfile.TarInfo(name)
    info.mode = mode
    info.uid = uid
    info.gid = gid
    info.mtime = 0
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))


def add_tar_dir(tar: tarfile.TarFile, name: str, mode: int, uid: int, gid: int) -> None:
    info = tarfile.TarInfo(name.rstrip("/") + "/")
    info.type = tarfile.DIRTYPE
    info.mode = mode
    info.uid = uid
    info.gid = gid
    info.mtime = 0
    tar.addfile(info)


def build_archive(
    dist: pathlib.Path,
    schema: dict[str, str],
    closure: dict[str, Any],
    maker_sha: str,
    output_dir: pathlib.Path,
) -> tuple[pathlib.Path, str, bytes]:
    output_dir = output_dir.resolve()
    if output_dir.name != "artifacts" or not output_dir.is_dir():
        raise Refusal("output must be an existing ORCH/artifacts directory")
    root = TRANSPORT_ROOT
    transport_manifest = {
        "schema": "timeline.d141.record-exact-installed-schema-transport/v1",
        "transport_kind": "record_exact_installed_distribution",
        "source_identity": schema,
        "trusted_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "maker_sha256": maker_sha,
        "closure": closure,
        "payload_root": "site-packages",
        "trusted_manifest_path": "trusted-schema-manifest.json",
        "safe_receiver": SAFE_RECEIVER,
        "attestation": "transport only; not an installed child, Farm result, or PASS_INSTALL receipt",
    }
    manifest_data = json_bytes(transport_manifest) + b"\n"
    trusted_data = json_bytes(schema)
    with tempfile.TemporaryDirectory(prefix="d141-transport-") as temp:
        temp_path = pathlib.Path(temp) / "transport.tgz"
        with open(temp_path, "wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as gz:
                with tarfile.open(fileobj=gz, mode="w:") as tar:
                    add_tar_dir(tar, root, 0o755, os.getuid(), os.getgid())
                    add_tar_dir(tar, f"{root}/site-packages", 0o755, os.getuid(), os.getgid())
                    for entry in closure["directories"]:
                        rel = entry["path"]
                        if rel == ".":
                            continue
                        add_tar_dir(tar, f"{root}/site-packages/{rel}", int(entry["mode"], 8), entry["uid"], entry["gid"])
                    add_tar_bytes(tar, f"{root}/manifest.json", manifest_data, 0o644, os.getuid(), os.getgid())
                    add_tar_bytes(tar, f"{root}/trusted-schema-manifest.json", trusted_data, 0o644, os.getuid(), os.getgid())
                    for entry in closure["files"]:
                        data = (dist.parent / pathlib.PurePosixPath(entry["path"])).read_bytes()
                        add_tar_bytes(
                            tar,
                            f"{root}/site-packages/{entry['path']}",
                            data,
                            int(entry["mode"], 8),
                            entry["uid"],
                            entry["gid"],
                        )
        archive_data = temp_path.read_bytes()
    digest = sha256(archive_data)
    archive = output_dir / f"timeline-d141-schema-record-closure-{digest}.tgz"
    atomic_write(archive, archive_data)
    atomic_write(pathlib.Path(str(archive) + ".sha256"), (digest + "\n").encode())
    return archive, digest, manifest_data


def verify_received_archive(
    archive: pathlib.Path, expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Verify bytes against a digest supplied separately by the trusted manager peer.

    A filename, archive manifest, or adjacent sidecar is not an authority for this
    argument. No extraction or product import is performed.
    """
    if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise Refusal("external manager-peer --expected-sha256 is required")
    info = physical(archive, "file")
    if info.st_size > MAX_ARCHIVE_BYTES:
        raise Refusal("transport exceeds 20 MiB archive limit")
    # Parse the exact authenticated snapshot, never reopen the path for parsing.
    with archive.open("rb") as source:
        archive_bytes = source.read(MAX_ARCHIVE_BYTES + 1)
    if len(archive_bytes) > MAX_ARCHIVE_BYTES:
        raise Refusal("transport exceeds 20 MiB archive limit")
    if sha256(archive_bytes) != expected_sha256:
        raise Refusal("transport differs from external manager-peer SHA-256")
    sidecar = archive.with_name(archive.name + ".sha256")
    sidecar_info = physical(sidecar, "file")
    if sidecar_info.st_size != 65 or sidecar.read_bytes() != (expected_sha256 + "\n").encode():
        raise Refusal("transport SHA-256 sidecar does not match authenticated bytes")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(archive_bytes), mode="rb") as gz:
            tar_bytes = gz.read(MAX_ARCHIVE_BYTES + 1)
        if len(tar_bytes) > MAX_ARCHIVE_BYTES:
            raise Refusal("transport exceeds 20 MiB expanded limit")
        with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tar:
            return inspect_received_tar(tar, tar_bytes, archive, expected_sha256)
    except (tarfile.TarError, OSError, EOFError, ValueError, KeyError, TypeError, csv.Error, RecursionError) as error:
        raise Refusal("invalid transport structure") from error


def inspect_received_tar(
    tar: tarfile.TarFile, tar_bytes: bytes, archive: pathlib.Path, digest: str,
) -> dict[str, Any]:
    root = TRANSPORT_ROOT
    members: dict[str, tarfile.TarInfo] = {}
    for member in tar:
        safe_record_path(member.name)
        if member.name in members:
            raise Refusal("duplicate transport member")
        if len(members) >= 25:
            raise Refusal("transport has extra members")
        if member.type not in {tarfile.REGTYPE, tarfile.AREGTYPE, tarfile.DIRTYPE} \
                or member.sparse is not None or set(member.pax_headers) - {"path"}:
            raise Refusal("transport contains an unsupported member or extension")
        mode = 0o755 if member.isdir() else 0o644
        if member.mode != mode or member.uid != 0 or member.gid != 0 \
                or member.linkname or member.size < 0 or member.size > MAX_ARCHIVE_BYTES \
                or (member.isdir() and member.size):
            raise Refusal("transport member mode/ownership/size mismatch")
        members[member.name] = member
    if any(tar_bytes[tar.offset:]):
        raise Refusal("transport contains data after the tar terminator")

    def read(name: str) -> bytes:
        member = members.get(name)
        if member is None or not member.isfile():
            raise Refusal("transport required regular file is missing")
        data = tar.extractfile(member).read()
        if len(data) != member.size:
            raise Refusal("transport member is truncated")
        return data

    trusted_bytes = read(f"{root}/trusted-schema-manifest.json")
    schema = strict_json(trusted_bytes)
    if set(schema) != {"url", "commit", "subdirectory", "source_tree"} \
            or sha256(trusted_bytes) != EXPECTED_MANIFEST_SHA256 \
            or sha256(json_bytes(schema)) != EXPECTED_MANIFEST_SHA256:
        raise Refusal("transport trusted manifest identity mismatch")
    transport = strict_json(read(f"{root}/manifest.json"))
    if transport.get("schema") != "timeline.d141.record-exact-installed-schema-transport/v1" \
            or transport.get("transport_kind") != "record_exact_installed_distribution" \
            or transport.get("source_identity") != schema \
            or transport.get("trusted_manifest_sha256") != EXPECTED_MANIFEST_SHA256 \
            or transport.get("maker_sha256") != EXPECTED_MAKER_SHA256 \
            or transport.get("payload_root") != "site-packages" \
            or transport.get("trusted_manifest_path") != "trusted-schema-manifest.json":
        raise Refusal("transport entry manifest identity mismatch")
    closure = transport.get("closure")
    if not isinstance(closure, dict) or closure.get("source_dist_info") != DIST_INFO:
        raise Refusal("transport closure metadata is incomplete")
    record = read(f"{root}/site-packages/{RECORD_PATH}")
    if sha256(record) != EXPECTED_RECORD_SHA256:
        raise Refusal("received RECORD is not the approved closure")
    rows = list(csv.reader(io.StringIO(record.decode("utf-8")), strict=True))
    if len(rows) != 18 or any(len(row) != 3 for row in rows):
        raise Refusal("received RECORD must have 18 three-column rows")
    paths = set()
    entries = []
    for rel, encoded, size in rows:
        safe_record_path(rel)
        if rel in paths:
            raise Refusal("duplicate RECORD path")
        paths.add(rel)
        data = read(f"{root}/site-packages/{rel}")
        hashed = bool(encoded or size)
        if hashed:
            actual = "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
            if encoded != actual or size != str(len(data)):
                raise Refusal("received RECORD file bytes mismatch")
        elif rel not in EXPECTED_UNHASHED:
            raise Refusal("unapproved unhashed RECORD row")
        entries.append({
            "path": rel, "bytes": len(data), "sha256": sha256(data),
            "record_hashed": hashed, "mode": "0644", "uid": 0, "gid": 0, "nlink": 1,
        })
    if sum(entry["record_hashed"] for entry in entries) != 12 \
            or {entry["path"] for entry in entries if not entry["record_hashed"]} != EXPECTED_UNHASHED:
        raise Refusal("received RECORD must have 12 hashed and the six named unhashed rows")
    expected_record = {
        "path": RECORD_PATH, "bytes": len(record), "sha256": EXPECTED_RECORD_SHA256,
        "rows": 18, "hashed_rows": 12, "unhashed_rows": sorted(EXPECTED_UNHASHED),
    }
    if json_bytes(closure.get("files")) != json_bytes(sorted(entries, key=lambda entry: entry["path"])) \
            or json_bytes(closure.get("record")) != json_bytes(expected_record) \
            or closure.get("closure_file_count") != 18 \
            or closure.get("closure_bytes") != sum(entry["bytes"] for entry in entries):
        raise Refusal("received entry manifest does not match the RECORD closure")
    directories = {"."}
    for rel in paths:
        directories.update(str(parent) for parent in pathlib.PurePosixPath(rel).parents)
    expected_dirs = [
        {"path": rel, "mode": "0755", "uid": 0, "gid": 0} for rel in sorted(directories)
    ]
    if json_bytes(closure.get("directories")) != json_bytes(expected_dirs):
        raise Refusal("received directory manifest mismatch")
    expected_files = {f"{root}/manifest.json", f"{root}/trusted-schema-manifest.json"}
    expected_files.update(f"{root}/site-packages/{rel}" for rel in paths)
    expected_directories = {root, f"{root}/site-packages"}
    expected_directories.update(f"{root}/site-packages/{rel}" for rel in directories if rel != ".")
    if set(members) != expected_files | expected_directories:
        raise Refusal("transport member set is not exactly metadata plus RECORD closure")
    if any(not members[name].isdir() for name in expected_directories):
        raise Refusal("transport directory has wrong type")
    direct_bytes = read(f"{root}/site-packages/{DIRECT_PATH}")
    direct = strict_json(direct_bytes)
    expected_direct = {
        "subdirectory": schema["subdirectory"], "url": schema["url"],
        "vcs_info": {"commit_id": schema["commit"], "requested_revision": schema["commit"], "vcs": "git"},
    }
    if sha256(direct_bytes) != EXPECTED_DIRECT_URL_SHA256 or direct != expected_direct \
            or DIRECT_URL_SECRET.search(direct_bytes):
        raise Refusal("received direct_url is not the exact approved pinned source")
    if json_bytes(closure.get("direct_url")) != json_bytes({
        "path": DIRECT_PATH, "bytes": len(direct_bytes), "sha256": EXPECTED_DIRECT_URL_SHA256,
        "privacy_checked": True, "raw_content_published": False, "pinned_identity_match": True,
    }):
        raise Refusal("received direct_url entry manifest mismatch")
    return {
        "status": "PASS_TRANSPORT_CLOSURE", "archive": str(archive), "archive_sha256": digest,
        "authentication": "external manager-peer SHA-256; sidecar is consistency only",
        "trusted_manifest_sha256": EXPECTED_MANIFEST_SHA256, "source_identity": schema,
        "record_rows": 18, "record_hashed_rows": 12,
        "direct_url_sha256": EXPECTED_DIRECT_URL_SHA256, "raw_direct_url_printed": False,
        "safe_receiver": SAFE_RECEIVER,
    }


def build(args: argparse.Namespace) -> dict[str, Any]:
    maker = pathlib.Path(args.maker).resolve()
    dist = pathlib.Path(args.dist).resolve()
    schema, maker_sha = extract_trusted_schema(maker)
    closure = inspect_distribution(dist, schema)
    trusted_data = json_bytes(schema)
    if sha256(trusted_data) != EXPECTED_MANIFEST_SHA256:
        raise Refusal("new trusted manifest failed canonical digest check")
    if args.manifest_output:
        atomic_write(pathlib.Path(args.manifest_output).resolve(), trusted_data)
    archive, archive_sha, transport_manifest = build_archive(
        dist, schema, closure, maker_sha, pathlib.Path(args.output_dir)
    )
    verify_received_archive(archive, archive_sha)
    result = {
        "status": "PUBLISHED_TO_ORCH_ARTIFACTS_RECEIVER_PENDING",
        "trusted_manifest": {
            "path": str(pathlib.Path(args.manifest_output).resolve()) if args.manifest_output else None,
            "sha256": EXPECTED_MANIFEST_SHA256,
            "keys": list(schema),
            "newly_produced": True,
            "historical_recovery_claim": False,
        },
        "source": {"maker_sha256": maker_sha, "dist_info": dist.name, "closure": closure},
        "transport": {
            "path": str(archive),
            "sha256": archive_sha,
            "bytes": archive.stat().st_size,
            "sidecar": str(pathlib.Path(str(archive) + ".sha256")),
            "manifest_sha256": sha256(transport_manifest),
            "verified": True,
        },
        "privacy": {
            "direct_url_sha256": EXPECTED_DIRECT_URL_SHA256,
            "raw_direct_url_printed": False,
            "secret_match": False,
        },
    }
    if args.report_output:
        atomic_write(pathlib.Path(args.report_output).resolve(), (json.dumps(result, indent=2) + "\n").encode())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maker")
    parser.add_argument("--dist")
    parser.add_argument("--output-dir")
    parser.add_argument("--manifest-output")
    parser.add_argument("--report-output")
    parser.add_argument("--verify-archive")
    parser.add_argument("--expected-sha256", help="required manager-peer digest supplied outside the archive/sidecar")
    args = parser.parse_args()
    try:
        if args.verify_archive:
            print(json.dumps(verify_received_archive(pathlib.Path(args.verify_archive).absolute(), args.expected_sha256), sort_keys=True))
        elif not args.maker or not args.dist or not args.output_dir:
            parser.error("--maker, --dist and --output-dir are required when building a transport")
        else:
            print(json.dumps(build(args), sort_keys=True))
    except Refusal as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
