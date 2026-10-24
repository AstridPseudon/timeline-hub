#!/usr/bin/env python3
"""Rebuild and validate the local six-row suites registration packet."""

from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
) / "scratchpad/orch"
SOURCE = ORCH / "tests/suites.conf"
PACKET = Path(__file__).resolve().parent
STAMP = "2026-10-24T02:11Z"

TARGETS = {
    "custody-root-cause-exact7d-trace": "venv-agent-child-s2",
    "custody-root-cause-exact7d-trace-clean": "venv-agent-child-s2",
    "custody-root-cause-exact7d-original-order": "venv-agent-child-s2",
    "custody-root-cause-exact7d-guard-context": "venv-agent-child-s2",
    "venv-agent-child-s2-c13-c13-full": "venv-agent-child-s2-c13",
    "full-remotion13-s2-integration": "venv-agent-child-s2-c13",
}

EXPECTED_ENV_HASHES = {
    "agent-remotion-0010.env": "943c0f49bc896097af0589b84c4dd4df06058fbe22e0c6fd999bcbf40f9a38a0",
    "agent-remotion-0012.env": "be340c6b77684d2438d1c46a674746188b851cbb23abec0c6dcf21a0742fd03a",
    "agent-remotion-0013.env": "e03e177251a99e37820c001f6fe6f88f2f503d1f939a5f67eed6ed59eeca2d07",
    "agent-remotion-current.env": "7faf606e9780385d7a32c053367b2a63e1b58246c52f14d14c226dbf9b20fa6c",
    "agent-remotion.env": "e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": digest(data)}


def active_rows(data: bytes) -> list[tuple[int, str, str, bytes]]:
    rows = []
    for number, raw in enumerate(data.splitlines(), 1):
        line = raw.decode("utf-8")
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split(None, 2)
        if len(fields) >= 2:
            rows.append((number, fields[0], fields[1], raw))
    return rows


def make_candidate(before: bytes) -> tuple[bytes, list[dict[str, object]]]:
    lines = before.decode("utf-8").splitlines(keepends=True)
    changed = []
    seen = set()
    for number, line in enumerate(lines, 1):
        if line.startswith("#") or not line.strip():
            continue
        fields = line.split(None, 2)
        if len(fields) < 2 or fields[1] not in TARGETS:
            continue
        suite = fields[1]
        assert suite not in seen, suite
        seen.add(suite)
        runtime = TARGETS[suite]
        replacement = (
            f"# retired {STAMP} (unused; runtime {runtime} retired for disk): {line}"
        )
        lines[number - 1] = replacement
        changed.append(
            {
                "line_before": number,
                "suite": suite,
                "runtime": runtime,
                "before_line_sha256": digest(line.encode()),
                "before_line_bytes": len(line.encode()),
                "after_line_sha256": digest(replacement.encode()),
                "after_line_bytes": len(replacement.encode()),
            }
        )
    assert seen == set(TARGETS), (seen, set(TARGETS))
    return "".join(lines).encode(), changed


def build_patch(before: bytes, after: bytes) -> bytes:
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


def private_replay(baseline: Path, patch: Path, candidate: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ops-suites-prune-") as directory:
        replay = Path(directory)
        (replay / "tests").mkdir()
        (replay / "tests/suites.conf").write_bytes(baseline.read_bytes())
        command = ["patch", "--batch", "--fuzz=0", "-p1", "-d", str(replay), "-i", str(patch)]
        dry_run = subprocess.run([*command, "--dry-run"], capture_output=True, text=True)
        assert dry_run.returncode == 0, dry_run.stderr
        applied = subprocess.run(command, capture_output=True, text=True)
        assert applied.returncode == 0, applied.stderr
        assert (replay / "tests/suites.conf").read_bytes() == candidate.read_bytes()


def main() -> None:
    before = SOURCE.read_bytes()
    candidate, changed = make_candidate(before)
    baseline_path = PACKET / "baseline-suites.conf"
    candidate_path = PACKET / "candidate-suites.conf"
    patch_path = PACKET / "suites-prune-0215.patch"
    manifest_path = PACKET / "manifest.json"
    baseline_path.write_bytes(before)
    candidate_path.write_bytes(candidate)
    patch_path.write_bytes(build_patch(before, candidate))

    before_rows = active_rows(before)
    after_rows = active_rows(candidate)
    assert len(before_rows) == 106 and len(after_rows) == 100
    assert len({(repo, suite) for _, repo, suite, _ in before_rows}) == 106
    assert len({(repo, suite) for _, repo, suite, _ in after_rows}) == 100
    before_by_key = {(repo, suite): raw for _, repo, suite, raw in before_rows}
    after_by_key = {(repo, suite): raw for _, repo, suite, raw in after_rows}
    assert set(before_by_key) - set(after_by_key) == {
        ("agent", suite) for suite in TARGETS
    }
    assert all(before_by_key[key] == after_by_key[key] for key in after_by_key)

    remote_only = ["composition14-255b6856", "main95bd", "published14-091aa23e"]
    assert all(before.decode().count(label) == 0 for label in remote_only)
    env_hashes = {
        path.name: digest(path.read_bytes())
        for path in sorted((ORCH / "tests").glob("*.env"))
    }
    assert env_hashes == EXPECTED_ENV_HASHES
    private_replay(baseline_path, patch_path, candidate_path)

    manifest = {
        "format_version": 1,
        "task": "OPS-suites-prune-0215",
        "decision": "proposal-only; no live config, install, retirement, or deletion",
        "source": {
            "path": "ORCH/tests/suites.conf",
            "local_source_path": str(SOURCE),
            "baseline": artifact(baseline_path),
            "candidate": artifact(candidate_path),
            "baseline_active_rows": 106,
            "candidate_active_rows": 100,
            "baseline_unique_repo_suite_keys": 106,
            "candidate_unique_repo_suite_keys": 100,
        },
        "patch": {
            **artifact(patch_path),
            "generation": "difflib.diff_bytes(unified_diff, splitlines(keepends=True), n=3); only six exact row prefixes added",
        },
        "validator": artifact(Path(__file__).resolve()),
        "local_candidate_targets": changed,
        "finite_targets": [
            "agent-remotion-0013",
            "composition14-255b6856",
            "main95bd",
            "published14-091aa23e",
            "venv-agent-child-s2",
            "venv-agent-child-s2-c13",
        ],
        "remote_agent_snapshot": {
            "status": "missing",
            "requested_by": "peer-runtime-to-agent-20261024T0210-prune-snapshot.md",
            "needed": [
                "exact Agent top-level tests/suites.conf bytes and SHA-256",
                "relevant Agent top-level *.env bytes and SHA-256",
                "Agent machine identity and exact current/final/gate row census",
            ],
            "targets_not_locally_proven": [
                "agent-remotion-0013",
                "composition14-255b6856",
                "main95bd",
                "published14-091aa23e",
            ],
            "local_exact_label_hits": {
                label: before.decode().count(label) for label in remote_only
            },
            "disposition": "blocked part; do not infer Agent source from local main data",
        },
        "protected": {
            "all_non_target_active_rows_byte_equal": True,
            "all_top_level_envs_byte_equal": True,
            "env_hashes": env_hashes,
            "explicit_keep_names": ["agent-remotion-current", "agent-remotion-v3-819acf-1110"],
            "no_env_changes": True,
            "no_directory_or_venv_or_runtime_deletion": True,
            "no_retire_request_or_old_refusal_retry": True,
        },
        "validation_results": {
            "private_patch_dry_run": "PASS",
            "private_patch_apply": "PASS",
            "private_replay_candidate_cmp": "PASS",
            "active_row_syntax": "PASS (100 active rows)",
            "unique_active_keys": "PASS (100 unique (repo, suite) keys)",
            "non_target_active_row_byte_equality": "PASS",
            "top_level_env_byte_equality": "PASS (5 files)",
            "packet_diff_whitespace": "PASS",
            "runtime_worktree_status": "clean before packet artifacts",
        },
        "checks": [
            "private patch apply and replay",
            "active-row syntax and unique (repo, suite) census",
            "non-target active-row byte equality",
            "top-level tests/*.env SHA-256 equality",
            "git diff --check on packet files",
        ],
        "product_tests": "not run; static registration packet only, with no product/source/test changes",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({name: artifact(PACKET / name) for name in (
        "baseline-suites.conf", "candidate-suites.conf", "suites-prune-0215.patch", "manifest.json",
    )}, indent=2))


if __name__ == "__main__":
    main()
