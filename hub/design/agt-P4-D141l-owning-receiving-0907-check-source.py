from __future__ import annotations

import hashlib
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "inputs"
PRIVATE = ROOT / "private controls"
MANIFEST = INPUTS / "p4-d141l-receiving.manifest"
POISON = INPUTS / "p4-d141l-poison-agent-sha.manifest"
STUB = INPUTS / "p4-d141l-positive-stub.sh"
LAUNCHER = Path("/home/user/work/agent/tools/p4-d73-pinned-launch.sh")
INSTALLER = Path("/home/user/work/agent/tools/install_p4_launcher.py")
POSITIVE = PRIVATE / "launcher-evidence/positive"
POISON_EVIDENCE = PRIVATE / "launcher-evidence/poison"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(path: str, *args: str) -> str:
    return subprocess.check_output(["git", "-C", path, *args], text=True).strip()


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        assert sep and key not in result, f"malformed or duplicate manifest key: {line!r}"
        result[key] = value
    return result


def assert_git_pin(pin: dict[str, str], name: str) -> None:
    path = pin[f"{name}_path"]
    assert Path(path).is_dir() and Path(path).resolve() == Path(path), f"non-exact {name} path"
    assert git(path, "rev-parse", "HEAD") == pin[f"{name}_sha"], f"{name} SHA mismatch"
    assert git(path, "rev-parse", "HEAD^{tree}") == pin[f"{name}_tree"], f"{name} tree mismatch"
    assert git(path, "rev-list", "--parents", "-n1", "HEAD") == pin[f"{name}_parents"], f"{name} parent mismatch"
    assert git(path, "status", "--porcelain", "--untracked-files=all") == "", f"{name} checkout dirty"
    assert git(path, "config", "--get", "remote.origin.url") == pin[f"{name}_origin"], f"{name} origin mismatch"


def main() -> None:
    pin = parse_manifest(MANIFEST)
    poison = parse_manifest(POISON)
    assert pin["format"] == "p4-d73-v1"
    for name in ("agent", "runtime", "app", "composition"):
        assert_git_pin(pin, name)
    assert poison["agent_sha"] == "0" * 40
    assert pin["agent_sha"] != poison["agent_sha"]

    assert sha256(LAUNCHER) == "9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd"
    assert sha256(INSTALLER) == "1fbcbc866a170212709e3e0f647f6d7082338eb819d42199f74b25b7e9d01805"
    assert sha256(STUB) == "38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0"
    assert pin["node_version"] == subprocess.check_output([pin["node"], "--version"], text=True).strip()
    assert sha256(Path(pin["profile"]) / "package-lock.json") == pin["profile_lock_sha"]
    archive = Path(pin["profile"]) / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
    assert sha256(archive) == pin["profile_archive_sha"]
    assert sha256(Path(pin["profile"]) / ".astrid-registry-state.json") == pin["profile_registry_sha"]
    assert sha256(Path(pin["agent_path"]) / "runtime.lock.json") == pin["runtime_lock_sha256"]
    test_paths = [
        Path(pin["agent_path"]) / "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py",
        Path(pin["agent_path"]) / "tests/editing_conformance/test_p4_ten_note_v2_runtime.py",
        Path(pin["agent_path"]) / "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py",
    ]
    aggregate = subprocess.check_output(
        ["sha256sum", *(str(path) for path in test_paths)], text=True
    )
    aggregate = hashlib.sha256(aggregate.encode()).hexdigest()
    assert aggregate == pin["original_p4_test_hash"]

    materialized = POSITIVE / "p4-d141l-positive.manifest"
    assert materialized.is_file() and sha256(materialized) == sha256(MANIFEST)
    assert (POSITIVE / "p4-d141l-positive.preflight.exit").read_text().strip() == "0"
    assert (POSITIVE / "p4-d141l-positive.body.exit").read_text().strip() == "17"
    assert (POSITIVE / "counter").read_text().splitlines() == ["called"]
    assert not (POISON_EVIDENCE / "p4-d141l-poison.manifest").exists()
    assert not (POISON_EVIDENCE / "counter").exists()
    assert not any(PRIVATE.rglob("*.xml")), "body XML must not exist before body"

    row = (ROOT / "evidence/candidate-row.txt").read_text()
    assert "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back" in row
    assert "-o addopts= -p no:cacheprovider --timeout=45 -m integration" in row
    assert str(PRIVATE / "launcher-evidence") in row
    assert "$P4_D73_EVIDENCE/p4-d141l-cli.xml" in row
    print("PASS: current source tuple, profile custody, launcher controls, and one-selector row")


if __name__ == "__main__":
    main()
