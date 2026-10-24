#!/usr/bin/env python3
"""Guarded, non-default installer for the v2 final Runtime service rows.

The installer is intentionally inert unless ``--install`` is supplied.  A
release must provide the final four-repository source tuple; no ambient
checkout is accepted as a substitute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


REGISTRY_SHA256 = "fdb9e9e9b9e964c92f4a6b3e3464cd300f51f33044b6f8f4ed4060ad69cfc81f"
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
    "core-v2-final-integration": "c93c84a88dd9425ef28e7f636c1f1c38a70a2319a2c45fbebe40663be822263e",
    "delivery-v2-final": "625e90f3b1b1b64884c19081f440677862768c879b2c358d92614175fb34b3b6",
    "delivery-v2-dryrun": "31950de6338707d02502c0b8e4bb322361d618cc3ad81915ba1922755734a39e",
}
NEW_NAMES = {
    "core-v2-final-integration",
    "delivery-v2-final",
    "delivery-v2-dryrun",
}
REQUIRED_TUPLE_REPOS = {"agent", "runtime", "app", "composition"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
        if not stripped or stripped.startswith(b"#"):
            continue
        try:
            repo, name, command = row_fields(line, source=f"registry line {number}")
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        rows.append((line, repo, name, command))
    return rows


def validate_registry(raw: bytes, candidate: bytes) -> tuple[dict[str, bytes], dict[str, bytes]]:
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


def validate_builder(path: Path, expected: str) -> None:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"builder is not a regular file: {path}")
    actual = digest(path.read_bytes())
    if actual != expected:
        raise ValueError(f"reviewed builder hash mismatch: {actual} != {expected}")


def git_value(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", *args],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot inspect source tuple repository {root}: {exc}") from exc


def git_status(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot inspect source status {root}: {exc}") from exc


def validate_source_tuple(path: Path) -> dict[str, dict[str, str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid final source tuple: {path}: {exc}") from exc
    if not isinstance(value, dict) or set(value) != REQUIRED_TUPLE_REPOS:
        raise ValueError("final source tuple must name exactly agent, runtime, app, composition")
    for name, item in value.items():
        if not isinstance(item, dict) or set(item) != {"root", "sha", "tree"}:
            raise ValueError(f"final source tuple entry {name} must contain root, sha, tree")
        root = Path(item["root"]).resolve()
        sha = item["sha"]
        tree = item["tree"]
        if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError(f"final source tuple {name}.sha is not a lowercase Git SHA")
        if not isinstance(tree, str) or len(tree) != 40 or any(c not in "0123456789abcdef" for c in tree):
            raise ValueError(f"final source tuple {name}.tree is not a lowercase Git tree")
        if git_value(root, "HEAD") != sha or git_value(root, "HEAD^{tree}") != tree:
            raise ValueError(f"final source tuple does not match current {name} source: {root}")
        if git_status(root):
            raise ValueError(f"final source tuple source is dirty: {root}")
    return value


def install(registry: Path, candidate: Path, backup: Path) -> None:
    if not registry.is_file() or registry.is_symlink():
        raise ValueError(f"registry is not a regular file: {registry}")
    old = registry.read_bytes()
    new_rows = candidate.read_bytes()
    validate_registry(old, new_rows)
    if not new_rows.endswith(b"\n"):
        raise ValueError("candidate must end with LF")
    if backup.resolve() == registry.resolve():
        raise ValueError("predecessor backup must be a distinct path")
    if backup.exists() or backup.is_symlink():
        raise ValueError(f"predecessor backup already exists: {backup}")
    replacement = old + new_rows
    if not replacement.startswith(old):
        raise ValueError("replacement does not preserve predecessor bytes")

    if not backup.parent.is_dir():
        raise ValueError(f"predecessor backup directory does not exist: {backup.parent}")
    os.link(registry, backup)
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=registry.parent, prefix=f".{registry.name}.", suffix=".tmp", delete=False
        ) as temp:
            temporary = Path(temp.name)
            temp.write(replacement)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temporary, registry)
        directory_fd = os.open(registry.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        if "temporary" in locals() and temporary.exists():
            temporary.unlink()
        raise
    if digest(registry.read_bytes()) != digest(replacement) or digest(backup.read_bytes()) != digest(old):
        raise RuntimeError("post-install registry or predecessor backup hash mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--builder", type=Path, required=True)
    parser.add_argument("--builder-sha", default=REVIEWED_BUILDER_SHA256)
    parser.add_argument("--source-tuple", type=Path, required=True)
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--install", action="store_true", help="atomically install after every guard passes")
    args = parser.parse_args()

    raw = args.registry.read_bytes()
    candidate = args.candidate.read_bytes()
    validate_registry(raw, candidate)
    validate_builder(args.builder, args.builder_sha)
    validate_source_tuple(args.source_tuple)
    if not args.install:
        print("candidate and release guards PASS; no installation requested")
        return 0
    install(args.registry, args.candidate, args.backup)
    print(f"installed {args.candidate} into {args.registry}; predecessor backup {args.backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
