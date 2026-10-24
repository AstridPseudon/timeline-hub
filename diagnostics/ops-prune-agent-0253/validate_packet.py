#!/usr/bin/env python3
"""Build and validate the private Agent actual-use prune packet."""

from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PACKET = Path(__file__).resolve().parent
SNAPSHOT = PACKET / "remote-snapshot.json"
BASELINE = PACKET / "baseline-suites.conf"
CANDIDATE = PACKET / "candidate-suites.conf"
PATCH = PACKET / "agent-source.patch"
ABA_ROW = PACKET / "agent-OPS-ABA-row-0245.txt"
ENV_DIR = PACKET / "env"
EXPECTED_TARGETS = {
    "agent-remotion-0013",
    "composition14-255b6856",
    "main95bd",
    "published14-091aa23e",
}
PROTECTED_NAMES = {"agent-remotion-current", "agent-remotion-v3-819acf-1110"}
RETIRE_STAMP = "2026-10-24T02:55Z"


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


def target_refs(line: str) -> set[str]:
    return {target for target in EXPECTED_TARGETS if target in line}


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
        assert dry_run.returncode == 0, dry_run.stderr
        applied = subprocess.run(command, capture_output=True, text=True)
        assert applied.returncode == 0, applied.stderr
        assert (root / "tests/suites.conf").read_bytes() == CANDIDATE.read_bytes()


def build() -> None:
    source_path = Path(
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    )
    snapshot_source = source_path / "scratchpad/orch/design/agent-OPS-suites-snapshot-0245.json"
    aba_source = source_path / "scratchpad/orch/design/agent-OPS-ABA-row-0245.txt"
    snapshot_bytes = snapshot_source.read_bytes()
    snapshot = json.loads(snapshot_bytes)
    source_files = {item["path"]: item for item in snapshot["files"]}
    suite_source = source_files["tests/suites.conf"]["text"].encode()
    candidate_lines = suite_source.splitlines(keepends=True)
    retirement = (
        b"# retired "
        + RETIRE_STAMP.encode()
        + b" (unused; runtime agent-remotion-composition14-255b6856 retired for disk)\n"
    )
    # These are the stale generic aliases. Named gate/provision rows remain exact.
    candidate_lines[20] = retirement
    candidate_lines[22] = retirement
    candidate = b"".join(candidate_lines)

    ENV_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_bytes(snapshot_bytes)
    BASELINE.write_bytes(suite_source)
    CANDIDATE.write_bytes(candidate)
    PATCH.write_bytes(expected_patch(suite_source, candidate))
    ABA_ROW.write_bytes(aba_source.read_bytes())
    for item in snapshot["files"]:
        if item["path"].startswith("tests/") and item["path"].endswith(".env"):
            (ENV_DIR / Path(item["path"]).name).write_bytes(item["text"].encode())

    source_docs = {
        "agent_status": source_path / "scratchpad/orch/managers/agent/STATUS.md",
        "runtime_status": source_path / "scratchpad/orch/managers/runtime/STATUS.md",
        "board_header": source_path / "scratchpad/orch/design/BOARD-HEADER.md",
        "current_full_recipe": source_path / "scratchpad/orch/design/agent-F-full-env-handoff-1229.md",
        "composition14_preflight": source_path / "scratchpad/orch/design/agent-composition14-runtime-preflight-1140.md",
        "main95bd_frozen": source_path / "scratchpad/orch/design/agent-main95bd-final-current-qualification.md",
        "published14_frozen": source_path / "scratchpad/orch/design/agent-published14-main497-final-review.md",
    }
    board_bytes = {
        name: path.read_bytes()
        for name, path in {
            "agent_status": source_docs["agent_status"],
            "runtime_status": source_docs["runtime_status"],
            "board_header": source_docs["board_header"],
        }.items()
    }
    board_captured_utc = datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    board_snapshot = {
        "captured_utc": board_captured_utc,
        "scope": "read-only content hashes captured at packet-build time; boards may change afterward",
        "files": {
            name: {
                "path": str(source_docs[name]),
                "bytes": len(data),
                "sha256": digest(data),
            }
            for name, data in board_bytes.items()
        },
    }
    evidence = {
        "base_runtime_integration": "f3208b26b",
        "snapshot": {
            "captured_utc": snapshot["captured_utc"],
            "machine": snapshot["machine"],
            "sha256": digest(snapshot_bytes),
            "active_rows": len(active_rows(suite_source)),
            "candidate_active_rows": len(active_rows(candidate)),
        },
        "aba_row": {
            "source": "design/agent-OPS-ABA-row-0245.txt",
            "bytes": len(ABA_ROW.read_bytes()),
            "sha256": digest(ABA_ROW.read_bytes()),
            "required_sha256": "962906266ee294a590958a4bcd5d4d7c1fda8dbcf9fc205f4e16ccbf3089d102",
            "preserved": True,
        },
        "source_documents": {
            name: {"path": str(path), "sha256": digest(path.read_bytes())}
            for name, path in source_docs.items()
        },
        "board_snapshot": board_snapshot,
        "classifications": {
            "agent-remotion-0013": {
                "active_rows": [],
                "current": "no exact 0245 suites.conf row",
                "gate": "no exact 0245 suites.conf row; historical evidence is not liveness proof",
                "final": "not selected by the current full-current-v3 recipe",
                "provision": "UNKNOWN; env-only reference remains and no remote lease/process evidence was supplied",
                "disposition": "UNKNOWN; do not remove tests/agent-remotion-0013.env in this packet",
                "evidence": [
                    "0245 suites.conf has zero active rows containing agent-remotion-0013",
                    "current full handoff selects full-current-v3-1229 with agent-remotion-v3-819acf-1110",
                    "retirement refusal/history is not used as unused proof",
                ],
            },
            "composition14-255b6856": {
                "active_rows": [141, 142],
                "retired_rows": [21, 23],
                "current": "generic full/targeted aliases are not the current full requester",
                "gate": "held by composition14-runtime-import-integration-1153 at line 142",
                "final": "not the final full recipe; current final recipe is full-current-v3-1229",
                "provision": "held by agent-remotion-composition14-255b6856-nodes at line 141",
                "disposition": "retire only generic aliases; preserve named gate/provision rows",
                "evidence": [
                    "current full handoff says not to reconstruct from old full or d09 rows",
                    "named composition14 node/import rows remain exact source custody",
                ],
            },
            "main95bd": {
                "active_rows": [8, 19, 123, 125, 126, 127, 128, 129, 130, 133],
                "current": "not selected by current full-current-v3-1229 requester",
                "gate": "historical/frozen gate1/D13/WC6 rows remain runnable; no current requester chain was cited",
                "final": "historical/frozen Main014 qualification remains custody evidence only",
                "provision": "registered by agent-remotion-main95bd-nodes at line 123 and env-bound rows; current use is not established",
                "disposition": "UNKNOWN; historical-only pending an explicit current/final requester citation; retain rows and env",
                "evidence": [
                    "agent-main95bd-final-current-qualification.md records an exact historical/frozen passing qualification",
                    "current full handoff selects full-current-v3-1229 and excludes the main95bd profile",
                    "current P1 evidence cites Runtime 2a9e347f and does not establish unrelated main95bd recipe use",
                    "no current/final requester chain proving this registration is needed was supplied",
                ],
            },
            "published14-091aa23e": {
                "active_rows": [14, 132, 134, 136],
                "current": "not selected by current full-current-v3-1229 requester",
                "gate": "historical/frozen public/integration proof rows remain runnable; no current requester chain was cited",
                "final": "historical/frozen published Main014/Main497 final review is retained evidence only",
                "provision": "registered by published14 nodes/full rows; current use is not established",
                "disposition": "UNKNOWN; historical-only pending an explicit current/final requester citation; retain rows and env",
                "evidence": [
                    "agent-published14-main497-final-review.md approves an exact historical/frozen publication proof",
                    "current full handoff selects full-current-v3-1229 and excludes the published14 profile",
                    "current P1 evidence cites Runtime 2a9e347f and does not establish unrelated published14 recipe use",
                    "no current/final requester chain proving this registration is needed was supplied",
                ],
            },
        },
        "guard_scan": {
            "comments_are_references": True,
            "candidate_target_occurrences": {
                target: sum(target in line.decode() for line in candidate.splitlines())
                for target in sorted(EXPECTED_TARGETS)
            },
            "env_target_occurrences": {
                target: sum(
                    target in item["text"]
                    for item in snapshot["files"]
                    if item["path"].endswith(".env")
                )
                for target in sorted(EXPECTED_TARGETS)
            },
            "retirement_eligibility": "not claimed; lead must run normal guarded retirement after review",
            "fully_unreferenced_targets": [],
            "fully_unreferenced_target_count": 0,
        },
    }
    (PACKET / "evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    )

    manifest = {
        "format_version": 3,
        "task": "OPS-suites-prune actual use 0253",
        "decision": "private proposal only; no live apply, retirement, deletion, install, or request",
        "base_commit": "f3208b26b",
        "remote_snapshot": {
            "path": "design/agent-OPS-suites-snapshot-0245.json",
            "machine": snapshot["machine"],
            "captured_utc": snapshot["captured_utc"],
            "bytes": len(snapshot_bytes),
            "sha256": digest(snapshot_bytes),
            "protected": snapshot["protected"],
        },
        "source": {
            "baseline_path": "baseline-suites.conf",
            "candidate_path": "candidate-suites.conf",
            "baseline_bytes": len(suite_source),
            "baseline_sha256": digest(suite_source),
            "candidate_bytes": len(candidate),
            "candidate_sha256": digest(candidate),
            "active_rows": len(active_rows(suite_source)),
            "candidate_active_rows": len(active_rows(candidate)),
            "unique_active_keys": len(
                {(r["repo"], r["suite"]) for r in active_rows(suite_source)}
            ),
            "candidate_unique_active_keys": len(
                {(r["repo"], r["suite"]) for r in active_rows(candidate)}
            ),
        },
        "patch": {
            "path": "agent-source.patch",
            "bytes": len(PATCH.read_bytes()),
            "sha256": digest(PATCH.read_bytes()),
            "hunks": PATCH.read_bytes().count(b"@@"),
            "comment_stamp": RETIRE_STAMP,
        },
        "aba_row": {
            "path": "agent-OPS-ABA-row-0245.txt",
            "bytes": len(ABA_ROW.read_bytes()),
            "sha256": digest(ABA_ROW.read_bytes()),
        },
        "env_sha256_verified": True,
        "protected_outside_bytes": True,
        "fully_unreferenced_targets": [],
        "fully_unreferenced_target_count": 0,
        "actual_disk_freed_gb": 0,
        "product_tests": "not run; source-only operational packet",
        "forbidden_actions_not_taken": [
            "live Agent/main config or env edits",
            "retire/request/daemon/provision/bench/kit",
            "process or lease probe",
            "old-refusal retry",
            "product/schema/client/pin/kit/tuple/Git writes",
            "deletion of live targets",
        ],
        "evidence_path": "evidence.json",
        "board_snapshot": board_snapshot,
    }
    (PACKET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def validate() -> None:
    snapshot = json.loads(SNAPSHOT.read_text())
    source_files = {item["path"]: item for item in snapshot["files"]}
    assert snapshot["machine"] == "vm"
    assert snapshot["captured_utc"] == "2026-10-24T02:45:20.793675+00:00"
    assert set(snapshot["protected"]) == PROTECTED_NAMES
    suite_source = source_files["tests/suites.conf"]["text"].encode()
    assert digest(suite_source) == source_files["tests/suites.conf"]["sha256"]
    assert len(suite_source) == source_files["tests/suites.conf"]["bytes"]
    assert BASELINE.read_bytes() == suite_source
    candidate = CANDIDATE.read_bytes()
    assert PATCH.read_bytes() == expected_patch(suite_source, candidate)
    rows = active_rows(suite_source)
    candidate_rows = active_rows(candidate)
    assert len(rows) == 141
    assert len(candidate_rows) == 139
    assert len({(row["repo"], row["suite"]) for row in rows}) == 141
    assert len({(row["repo"], row["suite"]) for row in candidate_rows}) == 139
    assert [row["line"] for row in candidate_rows if "composition14-255b6856" in str(row["text"])] == [141, 142]
    assert not any("agent-remotion-0013" in str(row["text"]) for row in candidate_rows)
    assert [row["line"] for row in candidate_rows if "main95bd" in str(row["text"])] == [8, 19, 123, 125, 126, 127, 128, 129, 130, 133]
    assert [row["line"] for row in candidate_rows if "published14-091aa23e" in str(row["text"])] == [14, 132, 134, 136]
    assert candidate.splitlines()[20].startswith(b"# retired 2026-10-24T02:55Z")
    assert candidate.splitlines()[22].startswith(b"# retired 2026-10-24T02:55Z")

    env_files = sorted(ENV_DIR.glob("*.env"))
    expected_env = {path for path in source_files if path.endswith(".env")}
    assert {"tests/" + path.name for path in env_files} == expected_env
    for path in env_files:
        item = source_files["tests/" + path.name]
        data = path.read_bytes()
        assert len(data) == item["bytes"]
        assert digest(data) == item["sha256"]
        assert data.decode() == item["text"]
    assert ABA_ROW.read_bytes() == Path(
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-OPS-ABA-row-0245.txt"
    ).read_bytes()
    assert len(ABA_ROW.read_bytes()) == 811
    assert digest(ABA_ROW.read_bytes()) == "962906266ee294a590958a4bcd5d4d7c1fda8dbcf9fc205f4e16ccbf3089d102"

    manifest = json.loads((PACKET / "manifest.json").read_text())
    assert manifest["base_commit"] == "f3208b26b"
    assert manifest["remote_snapshot"]["sha256"] == digest(SNAPSHOT.read_bytes())
    assert manifest["source"]["baseline_sha256"] == digest(BASELINE.read_bytes())
    assert manifest["source"]["candidate_sha256"] == digest(CANDIDATE.read_bytes())
    assert manifest["patch"]["sha256"] == digest(PATCH.read_bytes())
    assert manifest["source"]["active_rows"] == 141
    assert manifest["source"]["candidate_active_rows"] == 139
    assert manifest["protected_outside_bytes"] is True
    assert manifest["env_sha256_verified"] is True
    evidence = json.loads((PACKET / "evidence.json").read_text())
    assert evidence["aba_row"]["sha256"] == "962906266ee294a590958a4bcd5d4d7c1fda8dbcf9fc205f4e16ccbf3089d102"
    assert evidence["classifications"]["composition14-255b6856"]["retired_rows"] == [21, 23]
    assert evidence["classifications"]["agent-remotion-0013"]["disposition"].startswith("UNKNOWN")
    assert evidence["guard_scan"]["comments_are_references"] is True
    assert evidence["guard_scan"]["retirement_eligibility"].startswith("not claimed")
    assert evidence["guard_scan"]["fully_unreferenced_target_count"] == 0
    assert evidence["guard_scan"]["fully_unreferenced_targets"] == []
    assert manifest["fully_unreferenced_target_count"] == 0
    assert manifest["fully_unreferenced_targets"] == []
    assert manifest["actual_disk_freed_gb"] == 0
    board_snapshot = evidence["board_snapshot"]
    assert board_snapshot["captured_utc"].endswith("Z")
    assert "may change afterward" in board_snapshot["scope"]
    assert board_snapshot["files"] == manifest["board_snapshot"]["files"]
    assert evidence["classifications"]["main95bd"]["disposition"].startswith(
        "UNKNOWN; historical-only"
    )
    assert evidence["classifications"]["published14-091aa23e"]["disposition"].startswith(
        "UNKNOWN; historical-only"
    )
    candidate_guard_counts = {
        target: sum(target in line.decode() for line in candidate.splitlines())
        for target in sorted(EXPECTED_TARGETS)
    }
    assert candidate_guard_counts == {
        "agent-remotion-0013": 0,
        "composition14-255b6856": 4,
        "main95bd": 10,
        "published14-091aa23e": 4,
    }
    env_guard_counts = {
        target: sum(
            target in path.read_text()
            for path in ENV_DIR.glob("*.env")
        )
        for target in sorted(EXPECTED_TARGETS)
    }
    assert env_guard_counts == {
        "agent-remotion-0013": 1,
        "composition14-255b6856": 1,
        "main95bd": 1,
        "published14-091aa23e": 1,
    }

    private_replay()
    print("PASS: exact 0245 snapshot, actual-use classification, private replay, ABA custody, env hashes, and guard scan")


def main() -> None:
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == "--build":
        build()
        return
    validate()


if __name__ == "__main__":
    main()
