"""Every vendored copy in this repo matches its vendor.lock.json (testing plan C1, R-3)."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "vendor_lock.py"
_spec = importlib.util.spec_from_file_location("vendor_lock", SCRIPT)
vendor_lock = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vendor_lock)

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache"}


def _locks() -> list[Path]:
    found = []
    for directory, subdirs, files in os.walk(ROOT):
        subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS and not d.endswith(".egg-info")]
        found += [Path(directory) / "vendor.lock.json" for name in files if name == "vendor.lock.json"]
    return sorted(found)


LOCKS = _locks()


def _relative(lock: Path) -> str:
    return lock.relative_to(ROOT).as_posix()


def test_the_known_locks_are_not_dropped() -> None:
    assert {
        "astrid/core/timeline/schema/vendor.lock.json",
        "astrid_runtime_client/vendor.lock.json",
        "tests/fixtures/runtime-responses/vendor.lock.json",
        "tests/fixtures/vendor.lock.json",
    } <= {_relative(lock) for lock in LOCKS}


@pytest.mark.parametrize("lock", LOCKS, ids=_relative)
def test_vendored_copies_match_their_lock(lock: Path) -> None:
    assert vendor_lock.check(lock) == []


@pytest.mark.parametrize("lock", LOCKS, ids=_relative)
def test_a_one_byte_change_is_named(lock: Path, tmp_path: Path) -> None:
    files = json.loads(lock.read_text())["files"]
    for relative in [*files, _relative(lock)]:
        (tmp_path / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, tmp_path / relative)
    copied = tmp_path / _relative(lock)
    assert vendor_lock.check(copied, root=tmp_path) == []
    victim = sorted(files)[0]
    path = tmp_path / victim
    data = bytearray(path.read_bytes())
    data[len(data) // 2] ^= 0x01
    path.write_bytes(bytes(data))
    problems = vendor_lock.check(copied, root=tmp_path)
    assert problems[0] == f"{victim}: edited locally"
    assert problems[-1].startswith("re-vendor with: python scripts/vendor_lock.py update ")


def _producer(tmp_path: Path, artifacts: dict[str, str], version: str = "sha256:" + "1" * 64) -> Path:
    producer = tmp_path / "producer"
    (producer / "contract").mkdir(parents=True)
    (producer / "contract" / "artifacts.json").write_text(json.dumps({"producer": "p", "version": version, "artifacts": artifacts}))
    return producer


def test_a_producer_change_is_named_and_a_matching_producer_passes(tmp_path: Path) -> None:
    lock = ROOT / "tests" / "fixtures" / "vendor.lock.json"
    entry = next(iter(json.loads(lock.read_text())["files"].values()))
    state = json.loads(lock.read_text())
    assert vendor_lock.check(lock, _producer(tmp_path, {entry["from"]: entry["sha256"]}, state["producer_version"])) == []
    problems = vendor_lock.check(lock, _producer(tmp_path / "x", {entry["from"]: "sha256:" + "0" * 64}, state["producer_version"]))
    assert problems[0] == f"producer changed: {entry['from']}"
    # A producer change to files this consumer does not vendor (only the version moved) is not a failure.
    assert vendor_lock.check(lock, _producer(tmp_path / "y", {entry["from"]: entry["sha256"]})) == []


def test_update_copies_from_the_producer_and_rewrites_the_lock(tmp_path: Path) -> None:
    producer = tmp_path / "producer"
    (producer / "contract").mkdir(parents=True)
    (producer / "src").mkdir()
    (producer / "src" / "a.txt").write_text("one\n")
    subprocess.run(["git", "init", "-q", str(producer)], check=True)
    subprocess.run(["git", "-C", str(producer), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    digest = vendor_lock.digest(producer / "src" / "a.txt")
    (producer / "contract" / "artifacts.json").write_text(json.dumps({"producer": "p", "version": "sha256:" + "2" * 64, "artifacts": {"src/a.txt": digest}}))
    root = tmp_path / "consumer"
    root.mkdir()
    lock = root / "vendor.lock.json"
    lock.write_text(json.dumps({"producer": "p", "manifest": "contract/artifacts.json", "producer_version": "", "source_commit": None,
                                "files": {"vendored/a.txt": {"from": "src/a.txt", "sha256": ""}}}))
    message = vendor_lock.update(lock, producer, root=root)
    assert message.startswith("updated vendor.lock.json from p ")
    assert (root / "vendored" / "a.txt").read_text() == "one\n"
    written = json.loads(lock.read_text())
    assert written["files"]["vendored/a.txt"]["sha256"] == digest and written["producer_version"] == "sha256:" + "2" * 64
    assert len(written["source_commit"]) == 40
    assert vendor_lock.check(lock, producer, root=root) == []


def test_cli_exit_codes_and_messages(tmp_path: Path) -> None:
    lock = "tests/fixtures/vendor.lock.json"
    ok = subprocess.run([sys.executable, str(SCRIPT), "check", lock], cwd=ROOT, capture_output=True, text=True)
    assert (ok.returncode, ok.stdout.strip()) == (0, f"ok {lock}")
    usage = subprocess.run([sys.executable, str(SCRIPT), "update", lock], cwd=ROOT, capture_output=True, text=True)
    assert usage.returncode == 1 and usage.stderr.startswith("usage: vendor_lock.py check <lock>")
