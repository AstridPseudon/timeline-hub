#!/usr/bin/env python3
"""Guarded, non-default installer for the v2 final Runtime service rows.

The installer is intentionally inert unless ``--install`` is supplied.  A
release must provide the final four-repository source tuple; no ambient
checkout is accepted as a substitute.

Source: tl/rt-F-final-service-lock-return-sol-1305, successor to 15f78c995.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile


REGISTRY_SHA256 = "fdb9e9e9b9e964c92f4a6b3e3464cd300f51f33044b6f8f4ed4060ad69cfc81f"
CANDIDATE_SHA256 = "23b2cdf81202c70a3aa5f6e6fcbd3dfc3c1afa23e5524284d97e5af7b1be0497"
REVIEWED_BUILDER_SHA256 = (
    "f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708"
)
OLD_ROW_SHA256 = {
    "delivery-current-integration": "0c3bdc71eaa6d304a3430b6278c82bf2e02d86ff20b941853ad90c829fb9bf5e",
    "delivery-final-ref-integration": "2baeed4e2ef165d36cdb788674203851f4ada2aa1471aac7b6f4671c78e1d828",
    "delivery-owner-extras-actual": "5edd46a8c2d51e92c8d91d3f8bfd4a74414422d5b7f2f2d0666886b598feaf06",
    "delivery-owner-extras-integration-dryrun": "2037940e57e726cc6dce8af85708456b89bfee2dd0a6551f9345ea7250cad771",
    "gate2-atomic-integration": "e7a30aa934eb1798169daa38adf7255e5be6b69f930e8513f7b5209ab3e5170e",
    "gate4-door-integration": "399fb14bbcd6ec04a782ad8b1c0f4e8f2098816475a3d7289ab5ed0c8a08960a",
    "v2-auth-current-integration": "e5c6c4ccd2c2e05d19a8bfae7147ca07a7e0a6e1cdcc20bb29c70c747b25ef9a",
}
NEW_ROW_SHA256 = {
    "core-v2-final-integration": "4cd770d6f63a6104b59a6900e494f929c0404cbc7e7355397c3b07aa745a961f",
    "delivery-v2-final": "23a86a5fb3bef7aca7d012c8b785fc995769bab9327d6e65572c4d9bdb89f5dc",
    "delivery-v2-dryrun": "cd88c8b53e5690bae75df9efdac81be6679c03d570860177a4d13b221b53e67a",
}

NEW_NAMES = {
    "core-v2-final-integration",
    "delivery-v2-final",
    "delivery-v2-dryrun",
}
ARTIFACT_ROOT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-service-lock-return-sol-1305"
)
RUNNER = ARTIFACT_ROOT / "run-final-services.py"
FINAL_TUPLE = ARTIFACT_ROOT / "final-source-tuple.json"
RUNNER_SHA256 = "2611b13745e5b6ecd1f2f2ba4346743093c5f150cae89384f2024f10fa4a98de"
TUPLE_MARKER = b"FINAL_TUPLE_SHA256_PENDING"


def reviewed_runner():
    if not RUNNER.is_file() or RUNNER.is_symlink():
        raise ValueError(f"runner must be a retained regular file: {RUNNER}")
    raw = RUNNER.read_bytes()
    if digest(raw) != RUNNER_SHA256:
        raise ValueError("retained runner hash mismatch")
    spec = importlib.util.spec_from_file_location("timeline_final_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    # Execute exactly the bytes checked above; do not read an unchecked pyc.
    exec(compile(raw, str(RUNNER), "exec"), module.__dict__)
    return module


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_candidate(path: Path) -> bytes:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"candidate must be a regular non-symlink file: {path}")
    return path.read_bytes()


def row_fields(raw: bytes, *, source: str) -> tuple[str, str, str]:
    if not raw.endswith(b"\n"):
        raise ValueError(f"{source}: row must end with LF")
    try:
        text = raw[:-1].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{source}: row is not UTF-8") from exc
    fields = text.split(None, 2)
    if len(fields) != 3 or not fields[0] or not fields[1] or not fields[2]:
        raise ValueError(f"{source}: expected repo, unique suite name, and command")
    return fields[0], fields[1], fields[2]


def registry_rows(raw: bytes) -> list[tuple[bytes, str, str, str]]:
    rows: list[tuple[bytes, str, str, str]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        stripped = line.lstrip()
        if not stripped.strip() or stripped.startswith(b"#"):
            continue
        try:
            repo, name, command = row_fields(line, source=f"registry line {number}")
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        rows.append((line, repo, name, command))
    return rows


def validate_registry(raw: bytes, candidate: bytes) -> tuple[dict[str, bytes], dict[str, bytes]]:
    if digest(candidate) != CANDIDATE_SHA256:
        raise ValueError("candidate file does not match the reviewed source bytes")
    if digest(raw) != REGISTRY_SHA256:
        raise ValueError(
            f"predecessor registry hash mismatch: {digest(raw)} != {REGISTRY_SHA256}"
        )
    old_rows = registry_rows(raw)
    keys = [(repo, name) for _, repo, name, _ in old_rows]
    if len(keys) != len(set(keys)):
        raise ValueError("predecessor registry contains duplicate repo/suite identities")
    old_by_name = {name: line for line, repo, name, _ in old_rows if repo == "runtime"}
    for name, expected in OLD_ROW_SHA256.items():
        actual = digest(old_by_name.get(name, b""))
        if actual != expected:
            raise ValueError(f"predecessor row {name} mismatch: {actual} != {expected}")

    candidate_rows = [line for line in candidate.splitlines(keepends=True) if line.strip()]
    if len(candidate_rows) != len(NEW_NAMES):
        raise ValueError("candidate must contain exactly the three final service rows")
    candidate_by_name: dict[str, bytes] = {}
    for number, line in enumerate(candidate_rows, 1):
        repo, name, _ = row_fields(line, source=f"candidate line {number}")
        if repo != "runtime":
            raise ValueError(f"candidate line {number}: repository must be runtime")
        if name not in NEW_NAMES:
            raise ValueError(f"candidate line {number}: unexpected suite name {name!r}")
        if name in candidate_by_name or name in old_by_name:
            raise ValueError(f"duplicate suite name {name!r}")
        if digest(line) != NEW_ROW_SHA256[name]:
            raise ValueError(f"candidate row {name} does not match the reviewed identity")
        candidate_by_name[name] = line
    if set(candidate_by_name) != NEW_NAMES:
        raise ValueError("candidate names do not match the final service set")
    return old_by_name, candidate_by_name


def install(registry: Path, candidate: Path, backup: Path, tuple_bytes: bytes) -> None:
    reviewed_runner()
    if not registry.is_file() or registry.is_symlink():
        raise ValueError(f"registry is not a regular file: {registry}")
    old = registry.read_bytes()
    new_rows = read_candidate(candidate)
    validate_registry(old, new_rows)
    if not new_rows.endswith(b"\n"):
        raise ValueError("candidate must end with LF")
    if backup.resolve() == registry.resolve():
        raise ValueError("predecessor backup must be a distinct path")
    if backup.exists() or backup.is_symlink():
        raise ValueError(f"predecessor backup already exists: {backup}")
    if FINAL_TUPLE.exists() or FINAL_TUPLE.is_symlink():
        raise ValueError(f"retained final tuple already exists: {FINAL_TUPLE}")
    if new_rows.count(TUPLE_MARKER) != len(NEW_NAMES):
        raise ValueError("candidate must bind the final tuple once per service")
    replacement = old + new_rows.replace(TUPLE_MARKER, digest(tuple_bytes).encode("ascii"))
    if not replacement.startswith(old):
        raise ValueError("replacement does not preserve predecessor bytes")

    if not backup.parent.is_dir():
        raise ValueError(f"predecessor backup directory does not exist: {backup.parent}")
    replaced = False
    tuple_created = False
    try:
        # Retain the approved tuple independently of the input file's lifetime.
        with FINAL_TUPLE.open("xb") as target:
            tuple_created = True
            target.write(tuple_bytes)
            target.flush()
            os.fsync(target.fileno())
        os.link(registry, backup)
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=registry.parent, prefix=f".{registry.name}.", suffix=".tmp", delete=False
        ) as temp:
            temporary = Path(temp.name)
            temp.write(replacement)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temporary, registry)
        replaced = True
        directory_fd = os.open(registry.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        if "temporary" in locals() and temporary.exists():
            temporary.unlink()
        if tuple_created and not replaced and FINAL_TUPLE.is_file() and FINAL_TUPLE.read_bytes() == tuple_bytes:
            FINAL_TUPLE.unlink()
        raise
    if digest(registry.read_bytes()) != digest(replacement) or digest(backup.read_bytes()) != digest(old):
        raise RuntimeError("post-install registry or predecessor backup hash mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--builder", type=Path)
    parser.add_argument("--source-tuple", type=Path)
    parser.add_argument("--backup", type=Path)
    parser.add_argument("--install", action="store_true", help="atomically install after every guard passes")
    args = parser.parse_args()

    if any(value is None for value in (args.registry, args.candidate, args.builder)):
        parser.error("--registry, --candidate, and --builder are required")

    raw = args.registry.read_bytes()
    candidate = read_candidate(args.candidate)
    validate_registry(raw, candidate)
    runner = reviewed_runner()
    runner.validate_builder(args.builder, REVIEWED_BUILDER_SHA256)
    runner.validate_builder(runner.BUILDER, REVIEWED_BUILDER_SHA256)
    if not args.install:
        print("candidate and release guards PASS; no installation requested")
        return 0
    if args.source_tuple is None or args.backup is None:
        parser.error("--source-tuple and --backup are required with --install")
    tuple_bytes = args.source_tuple.read_bytes()
    value = runner.validate_source_tuple(args.source_tuple, digest(tuple_bytes))
    runner.validate_roots(value)
    runner.validate_agent_lock(value)
    for name, item in value.items():
        if runner.git_value(Path(item["root"]), "rev-parse", "tl/integration^{commit}") != item["sha"]:
            raise ValueError(f"final source tuple integration ref drift for {name}")
    install(args.registry, args.candidate, args.backup, tuple_bytes)
    print(f"installed {args.candidate} into {args.registry}; predecessor backup {args.backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
