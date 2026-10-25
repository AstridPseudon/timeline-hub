from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parent
COMMANDS = (ROOT / "commands.md").read_text()
RECEIVER = (ROOT / "receive-farm.sh").read_text()


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
