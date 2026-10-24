"""Installed child loading keeps external-pack imports inside admission."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import (
    GenericPackHost,
    HostError,
    _source_digest_for_roots,
)
from astrid.core.pack.source_setup import (
    SourceDeclaration,
    active_source_inventory,
    provision,
)


class _LaunchReached(RuntimeError):
    pass


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _external_orchestrator(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    collision: bool = False,
    symlink_module: bool = False,
) -> tuple[GenericPackHost, dict, dict, Path]:
    checkout = tmp_path / "external-checkout"
    checkout.mkdir()
    _git(checkout, "init", "-q", "-b", "main")
    _git(checkout, "config", "user.email", "fixture@example.test")
    _git(checkout, "config", "user.name", "Astrid fixture")
    pack_root = checkout
    orchestrator_root = pack_root / "orchestrators" / "demo"
    module_root = pack_root / "external_pkg"
    orchestrator_root.mkdir(parents=True)
    module_root.mkdir()
    (pack_root / "pack.yaml").write_text(
        "schema_version: 2\nid: external_pack\nname: External Pack\nversion: '1.0.0'\n"
        "status: active\ndocumentation:\n  kind: none\n  reason: test fixture\n"
        "content:\n  orchestrators: orchestrators\n",
        encoding="utf-8",
    )
    (orchestrator_root / "orchestrator.yaml").write_text(
        "schema_version: 1\nid: external_pack.demo\nname: Demo\nkind: external\nversion: '1.0.0'\n"
        "runtime:\n  kind: python\n  module: external_pkg.run\n  function: run\n",
        encoding="utf-8",
    )
    (module_root / "__init__.py").write_text("", encoding="utf-8")
    (module_root / "run.py").write_text(
        "def run(request, orchestrator):\n    return {'returncode': 0}\n", encoding="utf-8"
    )
    if collision:
        (pack_root / "astrid").mkdir()
        (pack_root / "astrid" / "__init__.py").write_text("", encoding="utf-8")
    _git(checkout, "add", ".")
    _git(checkout, "commit", "-q", "-m", "fixture")
    revision = _git(checkout, "rev-parse", "HEAD")
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    provision(
        (
            SourceDeclaration.from_mapping(
                {"pack_id": "external_pack", "repository": str(checkout), "revision": revision}
            ),
        ),
        state_path=state_path,
        data_root=data_root,
    )
    monkeypatch.setenv("ASTRID_SOURCE_STATE", str(state_path))
    inventory = active_source_inventory()
    pack_root = inventory.sources[0].pack_root
    if symlink_module:
        outside = tmp_path / "outside.py"
        outside.write_text("def run(request, orchestrator):\n    return {'returncode': 99}\n", encoding="utf-8")
        (pack_root / "external_pkg" / "run.py").unlink()
        (pack_root / "external_pkg" / "run.py").symlink_to(outside)
    host = GenericPackHost(
        pack_roots=list(inventory.roots),
        source_inventory_identity=inventory.identity,
    )
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
    host, definition, admission, pack_root = _external_orchestrator(tmp_path, monkeypatch)
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
    assert captured["argv"][1:3] == ["-I", "-m"]


@pytest.mark.parametrize(
    "tamper, message",
    [
        ("outside", "trusted Runtime admission"),
        ("missing_digest", "trusted Runtime admission"),
    ],
)
def test_installed_external_root_admission_refuses_before_child_launch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tamper: str,
    message: str,
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(tmp_path, monkeypatch)
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
    host, definition, admission, pack_root = _external_orchestrator(tmp_path, monkeypatch)
    (pack_root / "external_pkg" / "run.py").write_text(
        "def run(request, orchestrator):\n    return {'returncode': 99}\n", encoding="utf-8"
    )
    captured = _capture_launch(monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")

    with pytest.raises(HostError, match="managed source checkout is dirty"):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
        )
    assert "env" not in captured


def test_installed_external_caller_cannot_replace_trusted_source_fence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(tmp_path, monkeypatch)
    foreign_root = tmp_path / "foreign"
    foreign_root.mkdir()
    (foreign_root / "foreign.py").write_text("foreign = True\n", encoding="utf-8")
    admission["source_root"] = str(foreign_root)
    admission["source_roots"] = [str(foreign_root)]
    admission["source_digest"] = _source_digest_for_roots((foreign_root,))
    ambient = tmp_path / "ambient"
    ambient.mkdir()
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")
    monkeypatch.setenv("PYTHONPATH", str(ambient))
    captured = _capture_launch(monkeypatch)

    with pytest.raises(HostError, match="trusted Runtime admission"):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
            child_env={"PYTHONPATH": str(ambient)},
        )

    assert "env" not in captured


def test_installed_external_symlink_escape_refuses_before_child_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(
        tmp_path, monkeypatch, symlink_module=True
    )
    captured = _capture_launch(monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")

    with pytest.raises(HostError, match="managed source checkout is dirty|contains a symlink"):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
        )
    assert "env" not in captured


def test_installed_external_package_collision_refuses_before_child_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    host, definition, admission, _pack_root = _external_orchestrator(
        tmp_path, monkeypatch, collision=True
    )
    captured = _capture_launch(monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "installed")

    with pytest.raises(HostError, match="collides with installed package"):
        host.invoke_capability(
            capability_kind="orchestrator",
            capability_id="external_pack.demo",
            request=_request(tmp_path),
            attempt=tmp_path / "attempt",
            definition=definition,
            admission=admission,
        )
    assert "env" not in captured
