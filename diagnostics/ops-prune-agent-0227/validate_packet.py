#!/usr/bin/env python3
"""Validate the exact remote Agent suites/configuration prune packet."""

from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


PACKET = Path(__file__).resolve().parent
SNAPSHOT = PACKET / "remote-snapshot.json"
BASELINE = PACKET / "baseline-suites.conf"
CANDIDATE = PACKET / "candidate-suites.conf"
PATCH = PACKET / "agent-source.patch"
ENV_DIR = PACKET / "env"
EXPECTED_TARGETS = {
    "agent-remotion-0013",
    "composition14-255b6856",
    "main95bd",
    "published14-091aa23e",
}
PROTECTED_NAMES = {"agent-remotion-current", "agent-remotion-v3-819acf-1110"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def active_rows(data: bytes) -> list[dict[str, object]]:
    rows = []
    for number, raw in enumerate(data.splitlines(), 1):
        line = raw.decode("utf-8")
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split(None, 2)
        if len(fields) < 2:
            raise AssertionError(f"invalid active row at line {number}")
        rows.append(
            {
                "line": number,
                "repo": fields[0],
                "suite": fields[1],
                "bytes": len(raw),
                "sha256": digest(raw),
                "text": line,
            }
        )
    return rows


def project_refs(line: str) -> set[str]:
    return {
        target
        for target in EXPECTED_TARGETS
        if target in line
    }


def expected_patch(before: bytes, after: bytes) -> bytes:
    return b"".join(
        difflib.diff_bytes(
            difflib.unified_diff,
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=b"a/tests/suites.conf",
            tofile=b"b/tests/suites.conf",
            n=3,
            lineterm=b"\n",
        )
    )


def private_replay() -> None:
    with tempfile.TemporaryDirectory(prefix="ops-prune-agent-") as directory:
        root = Path(directory)
        (root / "tests").mkdir()
        (root / "tests/suites.conf").write_bytes(BASELINE.read_bytes())
        command = [
            "patch",
            "--batch",
            "--fuzz=0",
            "-p1",
            "-d",
            str(root),
            "-i",
            str(PATCH),
        ]
        dry_run = subprocess.run(
            [*command, "--dry-run"], capture_output=True, text=True
        )
        if PATCH.read_bytes():
            assert dry_run.returncode == 0, dry_run.stderr
            applied = subprocess.run(command, capture_output=True, text=True)
            assert applied.returncode == 0, applied.stderr
        else:
            assert BASELINE.read_bytes() == CANDIDATE.read_bytes()
        assert (root / "tests/suites.conf").read_bytes() == CANDIDATE.read_bytes()


def main() -> None:
    snapshot = json.loads(SNAPSHOT.read_text())
    assert snapshot["machine"] == "vm"
    assert snapshot["captured_utc"] == "2026-10-24T02:18Z"
    source_files = {item["path"]: item for item in snapshot["files"]}
    assert set(source_files) == {
        "tests/suites.conf",
        "tests/agent-remotion-0010.env",
        "tests/agent-remotion-0012.env",
        "tests/agent-remotion-0013.env",
        "tests/agent-remotion-composition14-255b6856.env",
        "tests/agent-remotion-current.env",
        "tests/agent-remotion-f4ed-0013.env",
        "tests/agent-remotion-main95bd.env",
        "tests/agent-remotion-published14-091aa23e.env",
        "tests/agent-remotion-v3-819acf-1110.env",
        "tests/agent-remotion.env",
    }
    assert set(snapshot["protected"]) == PROTECTED_NAMES

    suite_source = source_files["tests/suites.conf"]["text"].encode()
    assert digest(suite_source) == source_files["tests/suites.conf"]["sha256"]
    assert len(suite_source) == source_files["tests/suites.conf"]["bytes"]
    assert BASELINE.read_bytes() == suite_source
    candidate = CANDIDATE.read_bytes()
    assert candidate == suite_source
    assert PATCH.read_bytes() == expected_patch(suite_source, candidate) == b""

    rows = active_rows(suite_source)
    assert len(rows) == 140
    assert len({(row["repo"], row["suite"]) for row in rows}) == 140
    for row in rows:
        assert not row["text"].startswith("# retired ")

    by_target: dict[str, list[dict[str, object]]] = {
        target: [] for target in EXPECTED_TARGETS
    }
    for row in rows:
        for target in project_refs(str(row["text"])):
            by_target[target].append(row)
    assert not by_target["agent-remotion-0013"]
    assert [row["line"] for row in by_target["composition14-255b6856"]] == [21, 23, 141, 142]
    assert [row["line"] for row in by_target["main95bd"]] == [8, 19, 123, 125, 126, 127, 128, 129, 130, 133]
    assert [row["line"] for row in by_target["published14-091aa23e"]] == [14, 132, 134, 136]

    env_files = sorted(ENV_DIR.glob("*.env"))
    assert len(env_files) == 10
    for path in env_files:
        source_path = "tests/" + path.name
        item = source_files[source_path]
        data = path.read_bytes()
        assert len(data) == item["bytes"], source_path
        assert digest(data) == item["sha256"], source_path
        assert data.decode() == item["text"], source_path
    assert (ENV_DIR / "agent-remotion-current.env").read_bytes() == next(
        item["text"].encode()
        for item in snapshot["files"]
        if item["path"] == "tests/agent-remotion-current.env"
    )
    assert (ENV_DIR / "agent-remotion-v3-819acf-1110.env").read_bytes() == next(
        item["text"].encode()
        for item in snapshot["files"]
        if item["path"] == "tests/agent-remotion-v3-819acf-1110.env"
    )

    manifest = json.loads((PACKET / "manifest.json").read_text())
    assert manifest["decision"] == "proposal-only; no source apply, product merge, install, retirement, or deletion"
    assert manifest["base_commit"] == "45c3a7f47"
    assert manifest["remote_snapshot"]["machine"] == "vm"
    assert manifest["remote_snapshot"]["sha256"] == digest(SNAPSHOT.read_bytes())
    assert manifest["source"]["baseline_sha256"] == digest(BASELINE.read_bytes())
    assert manifest["source"]["candidate_sha256"] == digest(CANDIDATE.read_bytes())
    assert manifest["patch"]["sha256"] == digest(PATCH.read_bytes())
    assert manifest["source"]["active_rows"] == 140
    assert manifest["source"]["unique_active_keys"] == 140
    assert manifest["target_census"]["agent-remotion-0013"]["active_row_count"] == 0
    assert manifest["target_census"]["composition14-255b6856"]["disposition"].startswith("HELD")
    assert manifest["target_census"]["main95bd"]["disposition"].startswith("HELD")
    assert manifest["target_census"]["published14-091aa23e"]["disposition"].startswith("HELD")
    assert manifest["protected_outside_bytes"] is True
    assert manifest["env_sha256_verified"] is True
    assert manifest["product_tests"] == "not run; source-only registration packet"

    # The packet itself must be whitespace-clean; do not inspect product code.
    check = subprocess.run(
        ["git", "diff", "--check", "--no-index", "/dev/null", str(PATCH)],
        capture_output=True,
        text=True,
    )
    assert check.returncode in (0, 1), check.stderr
    private_replay()
    print("PASS: exact remote snapshot, source census, env SHA, no-op patch, and replay")


if __name__ == "__main__":
    main()
