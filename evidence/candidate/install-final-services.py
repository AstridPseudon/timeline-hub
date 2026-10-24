"""Guarded installer for the joined private final-service rows.

The default action only validates preimages. ``--install`` is the later
release action and requires both the final refreshed source receipt and the
immutable frozen gate tuple; it is intentionally not run by this task.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import tempfile
from pathlib import Path

REGISTRY_SHA256 = "b0557c15f20fa6de47fc9202f80a4c7533d085611f05c8e1849c3e55239980d3"
REVIEWED_BUILDER_SHA256 = "f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708"
CANDIDATE_SHA256 = "5d678805fde6d840d07f32f3587ef5c38267b81fe10dab424199aef3934c3019"
NEW_ROW_SHA256 = {
    "core-v2-final-integration": "71bd3c8d7cbd9b48709a9490d58ed75e0228ecb31a9240de9fee577a9ce80c6c",
    "delivery-v2-final": "6a27b89d860abc86ff7c55a59d0359973ff8169cfa973f882709638509cd6850",
    "delivery-v2-dryrun": "ee41a9bf3d9b1e7ed9aa2e5bcfca1ec66571e6445f2c6f1fe0528c593cc92f8d",
}
REVIEWED_WRAPPER_SHA256 = "bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779"
CORE_RUNNER_SHA256 = "c2f319acb45bc5dbb7bc94336c0ab23980e3d681d74325ab0714672bb7f2fe15"
OLD_ROW_SHA256 = {
    "delivery-current-integration": "0c3bdc71eaa6d304a3430b6278c82bf2e02d86ff20b941853ad90c829fb9bf5e",
    "delivery-final-ref-integration": "2baeed4e2ef165d36cdb788674203851f4ada2aa1471aac7b6f4671c78e1d828",
    "delivery-owner-extras-actual": "5edd46a8c2d51e92c8d91d3f8bfd4a74414422d5b7f2f2d0666886b598feaf06",
    "delivery-owner-extras-integration-dryrun": "2037940e57e726cc6dce8af85708456b89bfee2dd0a6551f9345ea7250cad771",
    "gate2-atomic-integration": "e7a30aa934eb1798169daa38adf7255e5be6b69f930e8513f7b5209ab3e5170e",
    "gate4-door-integration": "399fb14bbcd6ec04a782ad8b1c0f4e8f2098816475a3d7289ab5ed0c8a08960a",
    "v2-auth-current-integration": "e5c6c4ccd2c2e05d19a8bfae7147ca07a7e0a6e1cdcc20bb29c70c747b25ef9a",
}
NEW_NAMES = {"core-v2-final-integration", "delivery-v2-final", "delivery-v2-dryrun"}
ARTIFACT_ROOT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-candidate-join-1612/evidence/candidate"
)
RUNNER = ARTIFACT_ROOT / "run-final-delivery.py"
CORE_RUNNER = ARTIFACT_ROOT / "run-final-services.py"
WRAPPER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-D68-review-1554/evidence/delivery_gate_build.py"
)
FINAL_TUPLE = ARTIFACT_ROOT / "final-source-tuple.json"
GATE_TUPLE = ARTIFACT_ROOT / "final-gate-tuple.json"
TUPLE_MARKER = b"FINAL_TUPLE_SHA256_PENDING"
GATE_MARKER = b"GATE_TUPLE_SHA256_PENDING"
RUNNER_SHA256 = "64c83b4e99a3b46f966b0d056122f6a58626e38d4ee490dc152a33937332455d"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_file(path: Path, label: str) -> bytes:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"{label} must be a regular non-symlink file: {path}")
    return path.read_bytes()


def check_hash(path: Path, expected: str, label: str) -> bytes:
    raw = regular_file(path, label)
    actual = digest(raw)
    if actual != expected:
        raise ValueError(f"{label} hash mismatch: {actual} != {expected}")
    return raw


def read_candidate(path: Path) -> bytes:
    raw = check_hash(path, CANDIDATE_SHA256, "candidate rows")
    if not raw.endswith(b"\n"):
        raise ValueError("candidate rows must end with LF")
    return raw


def row_fields(raw: bytes, *, source: str) -> tuple[str, str, str]:
    if not raw.endswith(b"\n"):
        raise ValueError(f"{source}: row must end with LF")
    try:
        fields = raw[:-1].decode("utf-8").split(None, 2)
    except UnicodeDecodeError as exc:
        raise ValueError(f"{source}: row is not UTF-8") from exc
    if len(fields) != 3 or not all(fields):
        raise ValueError(f"{source}: expected repo, unique suite name, and command")
    return fields[0], fields[1], fields[2]


def registry_rows(raw: bytes) -> list[tuple[bytes, str, str, str]]:
    result = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        if not line.strip() or line.lstrip().startswith(b"#"):
            continue
        result.append((*((line,) + row_fields(line, source=f"registry line {number}")),))
    return result


def validate_registry(raw: bytes, candidate: bytes) -> None:
    if digest(raw) != REGISTRY_SHA256:
        raise ValueError(f"predecessor registry hash mismatch: {digest(raw)} != {REGISTRY_SHA256}")
    old_rows = registry_rows(raw)
    keys = [(repo, name) for _, repo, name, _ in old_rows]
    if len(keys) != len(set(keys)):
        raise ValueError("predecessor registry contains duplicate repo/suite identities")
    old_by_name = {name: line for line, repo, name, _ in old_rows if repo == "runtime"}
    for name, expected in OLD_ROW_SHA256.items():
        if digest(old_by_name.get(name, b"")) != expected:
            raise ValueError(f"predecessor row {name} mismatch")
    lines = [line for line in candidate.splitlines(keepends=True) if line.strip()]
    if len(lines) != len(NEW_NAMES):
        raise ValueError("candidate must contain exactly the three final service rows")
    seen: set[str] = set()
    for number, line in enumerate(lines, 1):
        repo, name, _ = row_fields(line, source=f"candidate line {number}")
        if repo != "runtime" or name not in NEW_NAMES or name in seen or name in old_by_name:
            raise ValueError(f"invalid or duplicate candidate suite {name!r}")
        seen.add(name)
        if digest(line) != NEW_ROW_SHA256[name]:
            raise ValueError(f"candidate row {name} does not match the reviewed identity")
    if seen != NEW_NAMES:
        raise ValueError("candidate names do not match the final service set")


def load_runner():
    raw = check_hash(RUNNER, RUNNER_SHA256, "delivery caller")
    spec = importlib.util.spec_from_file_location("timeline_final_delivery", RUNNER)
    if spec is None:
        raise ValueError("cannot load delivery caller")
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(RUNNER), "exec"), module.__dict__)  # noqa: S102
    return module


def validate_artifacts(builder: Path) -> None:
    check_hash(CORE_RUNNER, CORE_RUNNER_SHA256, "core runner")
    check_hash(WRAPPER, REVIEWED_WRAPPER_SHA256, "reviewed D68 wrapper")
    check_hash(builder, REVIEWED_BUILDER_SHA256, "delivery builder")
    caller = load_runner()
    if caller.CORE_RUNNER_SHA256 != CORE_RUNNER_SHA256:
        raise ValueError("delivery caller core runner pin changed")
    if caller.REVIEWED_WRAPPER_SHA256 != REVIEWED_WRAPPER_SHA256:
        raise ValueError("delivery caller wrapper pin changed")
    if caller.REVIEWED_BUILDER_SHA256 != REVIEWED_BUILDER_SHA256:
        raise ValueError("delivery caller builder pin changed")


def install(registry: Path, candidate: Path, backup: Path, source_bytes: bytes, gate_bytes: bytes) -> None:
    if backup.exists() or backup.is_symlink():
        raise ValueError(f"predecessor backup already exists: {backup}")
    if FINAL_TUPLE.exists() or FINAL_TUPLE.is_symlink() or GATE_TUPLE.exists() or GATE_TUPLE.is_symlink():
        raise ValueError("retained final tuple path already exists")
    if candidate.resolve() == registry.resolve() or backup.resolve() == registry.resolve():
        raise ValueError("candidate and backup must be distinct from the registry")
    if source_bytes.find(TUPLE_MARKER) >= 0 or gate_bytes.find(GATE_MARKER) >= 0:
        raise ValueError("release tuple inputs must be concrete, not marker bytes")
    old = registry.read_bytes()
    rows = read_candidate(candidate)
    validate_registry(old, rows)
    if rows.count(TUPLE_MARKER) != len(NEW_NAMES) or rows.count(GATE_MARKER) != len(NEW_NAMES):
        raise ValueError("candidate rows must bind both tuple hashes once per service")
    if rows.count(RUNNER_SHA256.encode("ascii")) != len(NEW_NAMES):
        raise ValueError("candidate rows must bind the delivery caller hash once per service")
    replacement = old + rows.replace(TUPLE_MARKER, digest(source_bytes).encode()).replace(
        GATE_MARKER, digest(gate_bytes).encode()
    )
    FINAL_TUPLE.parent.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    temporary: Path | None = None
    replaced = False
    try:
        FINAL_TUPLE.write_bytes(source_bytes)
        GATE_TUPLE.write_bytes(gate_bytes)
        created.extend((FINAL_TUPLE, GATE_TUPLE))
        os.link(registry, backup)
        with tempfile.NamedTemporaryFile(mode="wb", dir=registry.parent, prefix=f".{registry.name}.", suffix=".tmp", delete=False) as temp:
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
        if temporary is not None and temporary.exists():
            temporary.unlink()
        if not replaced:
            for path in created:
                if path.is_file() and path.read_bytes() in (source_bytes, gate_bytes):
                    path.unlink()
        raise
    if digest(registry.read_bytes()) != digest(replacement) or digest(backup.read_bytes()) != digest(old):
        raise RuntimeError("post-install registry or predecessor backup hash mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--builder", type=Path, required=True)
    parser.add_argument("--source-tuple", type=Path)
    parser.add_argument("--gate-tuple", type=Path)
    parser.add_argument("--backup", type=Path)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    if not args.registry.is_file() or args.registry.is_symlink():
        raise ValueError("registry must be a regular non-symlink file")
    candidate = read_candidate(args.candidate)
    validate_registry(args.registry.read_bytes(), candidate)
    validate_artifacts(args.builder)
    if not args.install:
        print("D68 candidate, core runner, wrapper, builder, and predecessor guards PASS; no installation requested")
        return 0
    if args.source_tuple is None or args.gate_tuple is None or args.backup is None:
        parser.error("--source-tuple, --gate-tuple, and --backup are required with --install")
    source_bytes = regular_file(args.source_tuple, "final source tuple")
    gate_bytes = regular_file(args.gate_tuple, "frozen gate tuple")
    caller = load_runner()
    caller.source_identity(args.source_tuple, digest(source_bytes))
    caller.gate_identity(args.gate_tuple, digest(gate_bytes))
    install(args.registry, args.candidate, args.backup, source_bytes, gate_bytes)
    print(f"installed {args.candidate} into {args.registry}; predecessor backup {args.backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
