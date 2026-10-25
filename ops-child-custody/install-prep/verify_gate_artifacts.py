"""Verify the exact manager-supplied D137 install decision input."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import sys


CANDIDATE_SHA256 = "5b6bfa01a74e7760e2cefe6713c0557cca695abb61074b3f01c9391949cfb064"
CANDIDATE_BYTES = 93300
PREIMAGE_SHA256 = "f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f"
PREIMAGE_BYTES = 75541
MAX_ARTIFACT_BYTES = 2 * 1024 * 1024


def fail(message: str) -> None:
    raise RuntimeError(message)


def safe_artifact(raw_path: str) -> tuple[Path, bytes]:
    path = Path(raw_path)
    if not path.is_absolute():
        fail("gate artifact must be an absolute path")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        fail(f"gate artifact cannot be resolved: {error}")
    if resolved != path:
        fail("gate artifact path must contain no symlink")
    uid = os.getuid()
    current = resolved
    while True:
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            fail("gate artifact ancestry contains a symlink")
        if current != resolved and not stat.S_ISDIR(info.st_mode):
            fail("gate artifact ancestry is not a directory")
        mode = stat.S_IMODE(info.st_mode)
        if mode & 0o022 and not (
            info.st_uid == 0 and mode & stat.S_ISVTX
        ):
            fail("gate artifact ancestry is broadly writable")
        if info.st_uid not in {0, uid}:
            fail("gate artifact ancestry owner mismatch")
        if current == current.parent:
            break
        current = current.parent
    if not stat.S_ISREG(resolved.lstat().st_mode):
        fail("gate artifact is not a regular file")
    info = resolved.lstat()
    if info.st_nlink != 1 or info.st_uid != uid:
        fail("gate artifact shape or owner mismatch")
    if stat.S_IMODE(info.st_mode) & 0o022:
        fail("gate artifact is broadly writable")
    if info.st_size > MAX_ARTIFACT_BYTES:
        fail("gate artifact is too large")
    return resolved, resolved.read_bytes()


def load_json(raw_path: str) -> tuple[Path, dict[str, object]]:
    path, raw = safe_artifact(raw_path)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        fail(f"gate artifact is not JSON: {error}")
    if not isinstance(value, dict):
        fail("gate artifact root is not an object")
    return path, value


def require(value: object, expected: object, label: str) -> None:
    if value != expected:
        fail(f"{label} is not {expected!r}")


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: verify_gate_artifacts.py D137_DECISION")
    decision_path, decision = load_json(sys.argv[1])
    require(decision.get("authorization"), "D137", "authorization")
    require(decision.get("fixture_e2e_gate"), "WITHDRAWN", "fixture_e2e_gate")
    require(decision.get("e2e_result"), "NOTRUN", "e2e_result")
    require(decision.get("e2e_pass"), False, "e2e_pass")
    require(decision.get("install_route"), "CAS_MANAGER_ONLY", "install_route")
    require(decision.get("production_install"), False, "production_install")
    require(decision.get("candidate_sha256"), CANDIDATE_SHA256, "candidate_sha256")
    source_commit = decision.get("source_commit")
    if not isinstance(source_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        fail("source_commit is not an exact commit")
    require(decision.get("candidate_bytes"), CANDIDATE_BYTES, "candidate_bytes")
    require(decision.get("preimage_sha256"), PREIMAGE_SHA256, "preimage_sha256")
    require(decision.get("preimage_bytes"), PREIMAGE_BYTES, "preimage_bytes")
    require(decision.get("reviewed_installer"), "installer1826", "reviewed_installer")
    require(decision.get("decision_path"), str(decision_path), "decision_path")
    print(f"PASS: exact D137 decision input accepted; E2E remains NOTRUN\nsource_commit={source_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        raise SystemExit(2)

