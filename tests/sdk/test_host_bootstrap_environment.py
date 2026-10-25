from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest

from astrid.core.rendering import remotion_runtime
from astrid.sdk import host_bootstrap


def _validation_environment(tmp_path: Path, **extra: str) -> dict[str, str]:
    return {
        "HOME": str(tmp_path / "home"),
        "PATH": os.defpath,
        "ASTRID_REMOTION_PROJECT_DIR": str(tmp_path / "remotion"),
        "ASTRID_NODE_EXECUTABLE": sys.executable,
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(tmp_path / "schema"),
        **extra,
    }


def test_host_bootstrap_removes_inherited_python_startup_override_before_validation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    environment = _validation_environment(tmp_path, PYTHONNOUSERSITE="1")
    original = dict(environment)
    captured: dict[str, object] = {}
    with pytest.raises(remotion_runtime.RemotionValidationError, match="unsupported loader/interpreter overrides"):
        remotion_runtime.probe_context(environment=original, python_executable=sys.executable)

    def prepare(
        *,
        host_environment: dict[str, str],
        python_executable: str,
        contexts: dict[str, Mapping[str, str] | list[Mapping[str, str]]],
        **_: object,
    ) -> dict[str, str]:
        captured.update(host_environment=host_environment)
        for context in contexts.values():
            values = context if isinstance(context, list) else [context]
            for value in values:
                remotion_runtime.probe_context(environment=value, python_executable=python_executable)
        return {}

    monkeypatch.setattr(remotion_runtime, "prepare_remotion_validation", prepare)
    launch_id = host_bootstrap._prepare_render_validation(
        tmp_path, environment, tmp_path / "support", sys.executable,
    )

    assert launch_id is not None
    assert "PYTHONNOUSERSITE" not in environment
    assert environment["ASTRID_REMOTION_PROJECT_DIR"] == original["ASTRID_REMOTION_PROJECT_DIR"]
    assert environment["ASTRID_NODE_EXECUTABLE"] == original["ASTRID_NODE_EXECUTABLE"]
    assert environment["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"] == original["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"]
    assert captured["host_environment"] == environment


def test_host_bootstrap_does_not_mutate_caller_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PYTHONNOUSERSITE", "1")
    monkeypatch.setattr(host_bootstrap, "_provision_render_runtime_env", lambda *_: None)
    before = dict(os.environ)

    environment = host_bootstrap._host_render_environment(tmp_path)

    assert os.environ == before
    assert "PYTHONNOUSERSITE" not in environment


def test_stricter_interpreter_overrides_remain_rejected() -> None:
    base = {"HOME": "/tmp", "PATH": os.defpath}
    for name in ("NODE_OPTIONS", "PYTHONHOME"):
        with pytest.raises(remotion_runtime.RemotionValidationError, match="unsupported loader/interpreter overrides"):
            remotion_runtime.probe_context(
                environment={**base, name: "unsupported"}, python_executable=sys.executable,
            )
