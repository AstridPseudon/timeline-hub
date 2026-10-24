from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

PACKET = Path(__file__).parent
SOURCE = json.loads((PACKET / "runtime-source-selection.json").read_text())
ROW = (PACKET / "registration-row.txt").read_text()
BRIEF = (PACKET / "FARM-CODEX-BRIEF.md").read_text()
README = (PACKET / "README.md").read_text()


def installer_source() -> str:
    return BRIEF.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]


def test_manifest_is_reproducible():
    for line in (PACKET / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert hashlib.sha256((PACKET.parent.parent / name).read_bytes()).hexdigest() == digest


def test_exact_source_and_graph_are_carryovers():
    assert SOURCE["agent_commit_tested_by_checkpoint"] == "9cd3dbe865a941c052bda04ae0d61306d18f8f26"
    assert SOURCE["agent_tree_tested_by_checkpoint"] == "57f0231da0d7904ecd8778169973d6384e0ae141"
    assert SOURCE["required_runtime_source_commit"] == "1d9ddba546f8fb1300f55ff62607ed492719cbaa"
    assert SOURCE["required_runtime_tree"] == "f56c396c4495547680b46e832565278d2c375e69"
    assert SOURCE["declared_runtime_source_commit"].startswith("45c3a7f4")
    assert SOURCE["remotion_base_suite"] == "remotion-env-nodes"
    assert SOURCE["remotion_registration"] == "agent-remotion-farm-v2-9cd"
    assert SOURCE["remotion_lock_sha256"] == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"


def test_request_is_the_supported_normal_maker_route():
    assert "request-child-venv" in README
    for value in (
        "venv-agent-child-farm-v3-9cd",
        "9cd3dbe865a941c052bda04ae0d61306d18f8f26",
        "remotion-env-nodes",
        "agent-remotion-farm-v2-9cd",
        "/home/user/work/wt/agt-pin-9cd3dbe8",
        "/home/user/work/wt/rt-pin-1d9ddba5",
        "1d9ddba546f8fb1300f55ff62607ed492719cbaa",
    ):
        assert value in README
    assert "--source-carrier" in README
    assert "request-runtime" not in README


def test_candidate_row_is_one_line_isolated_and_preserves_remotion_carriers():
    assert ROW.count("\n") == 1
    assert " PYTHONPATH=" not in ROW
    assert " -I -c " in ROW
    assert "@CHILD_ROOT@" in ROW
    assert "@CHILD_INTERPRETER@" in ROW
    assert "@MANAGED_PROFILE@" in ROW
    assert "@RUNTIME_CHECKOUT@" in ROW
    assert "ASTRID_TEST_NODE_MODULES=@MANAGED_PROFILE@/node_modules" in ROW
    assert "v20.19.4" in ROW and "10.8.2" in ROW
    assert "pytest.main([\"-q\",\"-n\",\"3\"])" in ROW


def test_installer_is_syntax_valid_and_never_creates_a_child():
    compile(installer_source(), "farm-agent-full-v3-installer", "exec")
    assert "Store.initialize" not in installer_source()
    assert "request-child-venv" not in installer_source()
    assert "pip install" not in installer_source()
    assert '"git", "-C"' in installer_source()


@pytest.mark.parametrize(
    ("case", "required"),
    [
        ("wrong Agent", "Agent marker mismatch"),
        ("wrong Runtime", "Runtime marker mismatch"),
        ("wrong client", "client tuple mismatch"),
        ("missing receipt", "D21b child receipt/registration missing"),
        ("wrong interpreter", "child interpreter is not retained"),
        ("wrong Node", "Node20/npm"),
        ("wrong graph", "managed Remotion registration missing"),
        ("wrong Store owner", "child receipt is not singular managed custody"),
        ("wrong key", "client tuple mismatch"),
        ("wrong proof lock", "declared Runtime lock drift"),
    ],
)
def test_installer_names_each_refusal_boundary(case, required):
    # These are deliberately source-level private-fixture contracts: the live
    # Store and Farm are out of scope for this packet, while each refusal must
    # remain visible in the installer body for a fixture to exercise.
    text = installer_source() + "\n" + ROW
    if case == "wrong Node":
        assert "Node version mismatch" in text and "npm version mismatch" in text
    elif case == "wrong graph":
        assert required in text
    else:
        assert required in text


def test_child_identity_requires_exact_receipt_markers_and_origins():
    text = installer_source()
    for marker in (
        ".provision-report",
        ".astrid-source-commit",
        ".astrid-runtime-source-commit",
        ".astrid-runtime-client-identity",
        ".astrid-import-origins",
        "status=passed",
        "is_relative_to(child)",
        "registration_entries(child_name)",
    ):
        assert marker in text
    assert "existence-only" not in text


def test_registry_update_is_scoped_atomic_and_recoverable():
    text = installer_source()
    for marker in (
        "rows.count(full) == 1",
        "len(old) == 1",
        "with store.mutex()",
        "api.atomic",
        "backup.open(\"xb\")",
        "registry drift",
        "outside_bytes=unchanged",
    ):
        assert marker in text
    assert "owner.json" not in text and "index.json" not in text


def test_no_source_overlay_or_isolation_bypass_is_encoded():
    forbidden = (".pth", " PYTHONPATH=", "sys.path.insert", "sys.path.append", "pip install", "Store.initialize")
    assert all(token not in ROW + installer_source() for token in forbidden)
    assert "python -I" in BRIEF or " -I -c " in ROW


def test_missing_actual_farm_inputs_are_named():
    normalized = " ".join(BRIEF.split())
    for phrase in (
        "current Store owner/index",
        "current registry bytes",
        "existing `agent full` and single `agent full-farm` rows",
        "successful D21b child receipt",
        "Farm must stop",
        "not an actual Farm READY result",
    ):
        assert phrase in normalized or phrase in README


def test_no_literal_staging_head_or_synthetic_ready_claim():
    all_text = ROW + BRIEF + (PACKET / "README.md").read_text()
    assert "stagingHEAD" not in all_text
    assert "Farm READY" in all_text
    assert "synthetic packet test is not an actual Farm READY result" in all_text
