"""Installed child loading keeps external-pack imports inside admission."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError


class _LaunchReached(RuntimeError):
    pass


def _external_orchestrator(tmp_path: Path) -> tuple[GenericPackHost, dict, dict, Path]:
    pack_root = tmp_path / "external-pack"
    orchestrator_root = pack_root / "orchestrators" / "demo"
    module_root = pack_root / "external_pkg"
    orchestrator_root.mkdir(parents=True)
    module_root.mkdir()
    (pack_root / "pack.yaml").write_text(
        "schema_version: 2\nid: external_pack\nname: External Pack\nversion: '1.0'\n"
        "status: active\ndocumentation:\n  kind: none\n  reason: test fixture\n"
        "content:\n  orchestrators: orchestrators\n",
        encoding="utf-8",
    )
    (orchestrator_root / "orchestrator.yaml").write_text(
        "schema_version: 1\nid: external_pack.demo\nname: Demo\nkind: external\nversion: '1.0'\n"
        "runtime:\n  kind: python\n  module: external_pkg.run\n  function: run\n",
        encoding="utf-8",
    )
    (module_root / "__init__.py").write_text("", encoding="utf-8")
    (module_root / "run.py").write_text(
        "def run(request, orchestrator):\n    return {'returncode': 0}\n", encoding="utf-8"
    )
    host = GenericPackHost(pack_roots=[pack_root])
    definition, admission = host.admit("orchestrator", "external_pack.demo")
    return host, dict(definition), dict(admission), pack_root


def _request(tmp_path: Path) -> dict[str, object]:
    return {
        "orchestrator_id": "external_pack.demo",
        "project": "demo",
        "project_was_auto_resolved": True,
        "out": None,
        "run_root": str(tmp_path / "attempt"),
    }


def _capture_launch(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    captured: dict[str, object] = {}

    def launch(argv, **kwargs):
        captured["argv"] = argv
        captured["env"] = dict(kwargs["env"])
        raise _LaunchReached

    monkeypatch.setattr("astrid.core.execution.generic_host.spawn_task_scope", launch)
    return captured


def test_installed_child_receives_only_fenced_external_pack_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, pack_root = _external_orchestrator(tmp_path)
    ambient = tmp_path / "ambient-collision"
    ambient.mkdir()
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")
    monkeypatch.setenv("PYTHONPATH", str(ambient))
    captured = _capture_launch(monkeypatch)

    with pytest.raises(_LaunchReached):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
            child_env={"PYTHONPATH": str(ambient)},
        )

    child_env = captured["env"]
    assert isinstance(child_env, dict)
    assert child_env["PYTHONPATH"].split(os.pathsep) == [str(pack_root)]
    assert str(ambient) not in child_env["PYTHONPATH"]
    assert str(Path(__file__).resolve().parents[2]) not in child_env["PYTHONPATH"]


@pytest.mark.parametrize(
    "tamper, message",
    [
        ("outside", "outside the source fence"),
        ("missing_digest", "require a source digest"),
    ],
)
def test_installed_external_root_admission_refuses_before_child_launch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tamper: str,
    message: str,
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(tmp_path)
    if tamper == "outside":
        admission["python_path_roots"] = [str(tmp_path)]
    else:
        admission.pop("source_digest")
    captured = _capture_launch(monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")

    with pytest.raises(HostError, match=message):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
        )
    assert "env" not in captured


def test_installed_external_digest_change_refuses_before_child_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, pack_root = _external_orchestrator(tmp_path)
    (pack_root / "external_pkg" / "run.py").write_text(
        "def run(request, orchestrator):\n    return {'returncode': 99}\n", encoding="utf-8"
    )
    captured = _capture_launch(monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")

    with pytest.raises(HostError, match="source digest changed"):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
        )
    assert "env" not in captured


def test_installed_child_does_not_restore_ambient_path_without_admitted_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(tmp_path)
    admission["python_path_roots"] = []
    ambient = tmp_path / "ambient"
    ambient.mkdir()
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")
    monkeypatch.setenv("PYTHONPATH", str(ambient))
    captured = _capture_launch(monkeypatch)

    with pytest.raises(_LaunchReached):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
            child_env={"PYTHONPATH": str(ambient)},
        )

    child_env = captured["env"]
    assert isinstance(child_env, dict)
    assert "PYTHONPATH" not in child_env
