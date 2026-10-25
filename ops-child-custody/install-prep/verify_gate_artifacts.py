"""Verify the two exact, manager-supplied D125b gate artifacts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


CANDIDATE_SHA256 = "c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e"
SOURCE_COMMIT = "09ed4999741b822fba7e8b3033ca28db6bcf8fa1"
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
    if len(sys.argv) != 3:
        fail("usage: verify_gate_artifacts.py E2E_RESULT INDEPENDENT_REVIEW")
    e2e_path, e2e = load_json(sys.argv[1])
    review_path, review = load_json(sys.argv[2])
    require(e2e.get("whole_make_e2e"), "PASS", "E2E whole_make_e2e")
    require(e2e.get("parent_red"), True, "E2E parent_red")
    require(e2e.get("candidate_green"), True, "E2E candidate_green")
    require(e2e.get("verifier_mocked"), False, "E2E verifier_mocked")
    require(e2e.get("store_initialized_by_worker"), False, "E2E store_initialized_by_worker")
    require(e2e.get("admission_changed"), False, "E2E admission_changed")
    adversarial_checks = e2e.get("adversarial_checks")
    if not isinstance(adversarial_checks, int) or isinstance(adversarial_checks, bool):
        fail("E2E adversarial_checks is not an integer")
    if adversarial_checks <= 0:
        fail("E2E has no adversarial checks")
    require(review.get("verdict"), "PASS", "independent review verdict")
    require(review.get("result_path"), str(e2e_path), "independent review result_path")
    require(
        review.get("result_sha256"),
        hashlib.sha256(e2e_path.read_bytes()).hexdigest(),
        "independent review result_sha256",
    )
    require(review.get("candidate_sha256"), CANDIDATE_SHA256, "independent review candidate_sha256")
    require(review.get("source_commit"), SOURCE_COMMIT, "independent review source_commit")
    require(review.get("reviewed_artifact"), "agt-OPS-inventory-E2E-receive-1800", "independent review reviewed_artifact")
    require(review.get("review_path"), str(review_path), "independent review review_path")
    print("PASS: exact E2E and independent review gates accepted")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        raise SystemExit(2)
