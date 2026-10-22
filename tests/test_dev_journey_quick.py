from __future__ import annotations

import sys
from pathlib import Path

import pytest

from astrid.core.dev.journey import (
    JourneyFailure,
    Runner,
    _isolate_quick_pack_home,
    _keep_failure_logs,
)
from astrid.core.extensions.scopes import contribution_roots
from astrid.core.pack.source_setup import source_data_root, source_state_path
from astrid.core.rendering.remotion_runtime import probe_context


def test_quick_pack_home_keeps_mutable_pack_paths_under_disposable_data(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "journey"
    env = {name: str(tmp_path / "global") for name in (
        "HOME", "ASTRID_HOME", "ASTRID_ENV_FILE", "ASTRID_PACKS_PATH",
        "ASTRID_SOURCE_DECLARATIONS", "ASTRID_SOURCE_DATA", "ASTRID_SOURCE_STATE",
        "ASTRID_USER_PACKS", "ASTRID_HIVEMIND_REPOSITORY", "ASTRID_HIVEMIND_REVISION")}
    _isolate_quick_pack_home(env, root)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    packhome = root / "data" / "packhome"
    data_root = source_data_root()
    state_path = source_state_path()
    user_root = next(
        row.path for row in contribution_roots(cwd=tmp_path, home=tmp_path, env=env, installed=())
        if row.scope == "user"
    )

    assert data_root == packhome / "data" / "astrid" / "packs"
    assert state_path == packhome / "state" / "astrid" / "pack-sources.json"
    assert user_root == packhome / "config" / "astrid" / "packs"
    assert Path(env["HOME"]) == packhome
    assert Path(env["ASTRID_HOME"]) == packhome / ".astrid"
    for key in ("ASTRID_ENV_FILE", "ASTRID_PACKS_PATH", "ASTRID_SOURCE_DECLARATIONS",
                "ASTRID_HIVEMIND_REPOSITORY", "ASTRID_HIVEMIND_REVISION"):
        assert key not in env
    assert probe_context(environment=env, python_executable=sys.executable)["schema_env"]["HOME"] == str(packhome)
    for path in (data_root, state_path, user_root):
        path.relative_to(root / "data")


def test_quick_failing_command_output_is_in_failure_evidence(tmp_path: Path) -> None:
    root = tmp_path / "journey"
    root.mkdir()
    runner = Runner(root, tmp_path / "summary.json", tier="quick")

    with pytest.raises(JourneyFailure, match="exit 3"):
        runner.command("first_open", [sys.executable, "-c", "import sys; print('open-out'); print('open-err', file=sys.stderr); sys.exit(3)"], {})

    evidence = Path(_keep_failure_logs(root, tmp_path / "summary.json"))
    assert (evidence / "first_open.stdout.log").read_text().strip() == "open-out"
    assert (evidence / "first_open.stderr.log").read_text().strip() == "open-err"


def test_a_failed_journey_exits_nonzero_through_the_dev_command(tmp_path: Path, monkeypatch) -> None:
    """The process status is the gate: a summary that says ok=false must never come with exit 0."""
    import json

    from astrid.core.dev import journey
    from astrid.core.gateway import dev_operator

    summary = tmp_path / "quick.json"

    def failing_run(*_args, **_kwargs) -> int:
        summary.write_text(json.dumps({"ok": False, "outcome": "failure", "error": "quick_browser: exit 1"}))
        return 1

    monkeypatch.setattr(journey, "run", failing_run)
    argv = ["journey", "--tier", "quick", "--reference", "generated", "--summary", str(summary)]
    assert dev_operator.main(argv) == 1
    assert json.loads(summary.read_text())["ok"] is False
