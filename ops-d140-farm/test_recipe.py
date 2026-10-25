from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent
COMMANDS = (ROOT / "commands.md").read_text()
RECEIVER = (ROOT / "receive-farm.sh").read_text()


def run_receiver(tmp_path: Path, phase: str, **bindings: str) -> dict:
    env = os.environ.copy()
    for name in (
        "AGENT_CHECKOUT", "RUNTIME_CHECKOUT", "APP_CHECKOUT", "COMPOSITION_CHECKOUT",
        "MAKER_PATH", "WRAPPER_PATH", "CHECKER_PATH", "RECEIVED_MAKER",
        "SCHEMA_INSTALLED_DISTRIBUTION", "SCHEMA_SOURCE_MANIFEST", "SCHEMA_RECORD_CLOSURE",
        "SCHEMA_DIRECT_URL", "CANONICAL_CENSUS", "DEPENDENCY_SEED", "CENTRAL_SERVICE",
        "CENTRAL_SUITE", "D73_LAUNCHER", "NODE_BIN", "NORMAL_REQUEST_ROUTE",
        "IMPORT_CHECK_ROUTE", "D73_DRY_ROUTE", "CORE_ROUTE", "PROFILE", "DISK_ADMISSION",
        "RETAINED_ROOT", "P4_PYTHON", "CHILD_PYTHON", "CHILD_BOOTSTRAP", "CHILD_RECEIPT",
        "P4_D73_MANIFEST", "P4_D73_EVIDENCE", "P4_D73_REQUEST_ID", "OUTPUT_ROOT", "JUNIT_ROOT",
        "RAW_ROOT", "STARTSTOP_ROOT", "KEEP_ROOT", "POSITIVE_CONTROL", "POSITIVE_COUNTER",
        "POISON_CONTROL", "POISON_COUNTER", "POISON_MANIFEST", "FARM_CURRENT_AGENT_RECEIPT",
        "FARM_CURRENT_RUNTIME_RECEIPT", "FARM_CURRENT_APP_RECEIPT",
        "FARM_CURRENT_COMPOSITION_RECEIPT", "FARM_D139A_KIT_RECEIPT", "FARM_D73_RECEIPT",
    ):
        env.pop(name, None)
    env["D140_PHASE"] = phase
    env.update(bindings)
    result = subprocess.run(
        [str(ROOT / "receive-farm.sh"), "--check-only"],
        cwd=ROOT.parent,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    return json.loads(result.stdout)


def test_receiver_is_check_only_and_contains_current_tuple() -> None:
    assert '"$1" != "--check-only"' in RECEIVER
    for value in (
        "41ad656529fa8489829de9078b1b6e157c7433c8",
        "f103bb46866999c961a8865636f2e66d544e0c9b",
        "5696769dfca056676cde1ab46d8bc94354b3a44a",
        "635f4de06fda22a85fc2e4cfc764d0153a4c9f40",
    ):
        assert value in RECEIVER


def test_core_selector_has_exactly_22_unfiltered_roots() -> None:
    expected = [
        "tests/editing_conformance",
        "tests/sdk",
        "tests/timeline",
        "tests/core/timeline",
        "tests/core/test_timeline_element_orphan_cleanup.py",
        "tests/core/test_timeline_element_publication.py",
        "tests/core/test_timeline_element_publication_runtime.py",
        "tests/core/rendering/test_timeline_visualize_cli_grammar.py",
        "tests/core/rendering/test_local_schema.py",
        "tests/packs/timeline",
        "tests/packs/rendering/test_composition_package.py",
        "tests/packs/rendering/test_live_scene_composition.py",
        "tests/packs/rendering/test_render_export_task_adapter.py",
        "tests/packs/rendering/test_timeline_filmstrip_cards.py",
        "tests/packs/rendering/test_timeline_filmstrip_execution.py",
        "tests/packs/video_editing/test_runtime_publication_chain.py",
        "tests/stage1/test_cold_launch_autobootstrap.py",
        "tests/test_installer_schema.py",
        "tests/test_installer_sources.py",
        "tests/test_installer_bootstrap_schema.py",
        "tests/test_timeline_clip_replacement.py",
        "tests/v10/test_timelines_create.py",
    ]
    body = COMMANDS.split("agent-core-full", 1)[1]
    assert "-k " not in body
    assert "--collect-only" not in body
    assert body.count("tests/") >= len(expected)
    for root in expected:
        assert root in body
    assert len(expected) == 22


def test_schema_and_control_gates_are_literal() -> None:
    for token in (
        "--schema-installed-distribution",
        "--schema-source-manifest",
        "--census-file",
        "positive_rc",
        "poison_rc",
        "= 17",
        'POSITIVE_COUNTER\")" = 1',
        'POISON_COUNTER\")" = 0',
    ):
        assert token in COMMANDS
    assert "--farm-schema-source" in (ROOT / "README.md").read_text()


def test_no_alternate_launcher_or_profile_is_advertised() -> None:
    assert re.search(r"existing reviewed D73 launcher", (ROOT / "README.md").read_text())
    assert "fallback profile" in (ROOT / "README.md").read_text()
    assert "p4-d73-pinned-launch.sh" in COMMANDS


def test_phase_census_does_not_admit_future_inputs_or_start_routes(tmp_path: Path) -> None:
    marker = tmp_path / "route-called"
    route = tmp_path / "route"
    route.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
    route.chmod(0o755)
    pre = run_receiver(tmp_path, "pre-child", NORMAL_REQUEST_ROUTE=str(route))
    post = run_receiver(tmp_path, "post-child", NORMAL_REQUEST_ROUTE=str(route))
    pre_ids = {check["id"] for check in pre["checks"]}
    post_ids = {check["id"] for check in post["checks"]}
    assert pre["phase"] == "pre-child"
    assert post["phase"] == "post-child"
    assert "binding.CHILD_RECEIPT" not in pre_ids
    assert "binding.P4_D73_MANIFEST" not in pre_ids
    assert "binding.OUTPUT_ROOT" not in pre_ids
    assert "binding.CHILD_RECEIPT" in post_ids
    assert "binding.P4_D73_MANIFEST" in post_ids
    assert "binding.OUTPUT_ROOT" in post_ids
    assert not marker.exists()


def test_wrong_receipt_and_poison_content_are_not_presence_passes(tmp_path: Path) -> None:
    wrong_receipt = tmp_path / "wrong-receipt.json"
    wrong_receipt.write_text('{"status":"passed","commit":"wrong"}\n', encoding="utf-8")
    result = run_receiver(tmp_path, "pre-child", FARM_CURRENT_AGENT_RECEIPT=str(wrong_receipt))
    receipt_check = next(check for check in result["checks"] if check["id"] == "receipt.FARM_CURRENT_AGENT_RECEIPT")
    assert receipt_check["status"] == "MISMATCH"

    positive = tmp_path / "positive.manifest"
    poison = tmp_path / "poison.manifest"
    positive.write_text("format=p4-d73-v1\nagent_sha=" + "1" * 40 + "\nagent_tree=tree\n", encoding="utf-8")
    poison.write_text("format=p4-d73-v1\nagent_sha=" + "0" * 40 + "\nagent_tree=wrong\n", encoding="utf-8")
    result = run_receiver(
        tmp_path,
        "post-child",
        P4_D73_MANIFEST=str(positive),
        POISON_MANIFEST=str(poison),
    )
    poison_check = next(check for check in result["checks"] if check["id"] == "control.poison-content")
    assert poison_check["status"] == "MISMATCH"


def test_schema_paths_are_bound_to_the_physical_dist_info(tmp_path: Path) -> None:
    dist = tmp_path / "banodoco_timeline_schema-0.0.2.dist-info"
    dist.mkdir()
    record = tmp_path / "detached-RECORD"
    direct = tmp_path / "detached-direct_url.json"
    manifest = tmp_path / "manifest.json"
    for path in (record, direct, manifest):
        path.write_text("{}\n", encoding="utf-8")
    result = run_receiver(
        tmp_path,
        "pre-child",
        SCHEMA_INSTALLED_DISTRIBUTION=str(dist),
        SCHEMA_RECORD_CLOSURE=str(record),
        SCHEMA_DIRECT_URL=str(direct),
        SCHEMA_SOURCE_MANIFEST=str(manifest),
    )
    path_check = next(check for check in result["checks"] if check["id"] == "schema.bound-paths")
    assert path_check["status"] == "MISMATCH"


def test_import_failure_stops_before_controls_and_core() -> None:
    failure = COMMANDS.index('if [ "$imports_rc" -ne 0 ]')
    controls = COMMANDS.index("## 3. D73 dry controls")
    assert failure < controls
    assert 'exit "$imports_rc"' in COMMANDS[:controls]
    assert 'P4_D73_MANIFEST="$P4_D73_MANIFEST"' in COMMANDS
    assert 'P4_D73_EVIDENCE="$KEEP_ROOT"' in COMMANDS
    assert 'CORE_ROUTE="$CORE_ROUTE"' in COMMANDS
    assert '--junitxml="$2"' in COMMANDS
    assert 'test -s "$raw_log"' in COMMANDS
    assert 'test -s "$DISK_ADMISSION"' in COMMANDS


def test_poison_and_d124_controls_are_not_weakened() -> None:
    assert 'only agent_sha replaced by forty zeroes' in RECEIVER
    assert 'check_source_receipt' in RECEIVER
    assert 'check_d73_receipt' in RECEIVER
    assert '"git", "-C", repo' in RECEIVER
    assert COMMANDS.count("tests/") >= 22
    assert "-k " not in COMMANDS
    assert "--collect-only" not in COMMANDS
