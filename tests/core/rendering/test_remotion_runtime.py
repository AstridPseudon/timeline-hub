"""Direct render admission checks do not depend on a host launch artifact."""
from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering import remotion_runtime as runtime
from astrid.core.subprocess_env import build_child_subprocess_env
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion_run


@pytest.fixture
def installed_runtime(tmp_path, monkeypatch):
    project = tmp_path / "remotion"
    project.mkdir()
    (project / "package.json").write_text('{"engines":{"node":"=20.19.4"}}')
    for name in runtime._REQUIRED_PACKAGES:
        manifest = project / "node_modules/@banodoco" / name / "package.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("{}")
    cli = project / runtime.REMOTION_CLI_RELATIVE_PATH
    cli.parent.mkdir(parents=True)
    cli.write_text("// locked CLI")
    schema = tmp_path / "schema"
    for name in runtime._REQUIRED_SCHEMA_FILES:
        path = schema / "banodoco_timeline_schema" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}" if name.endswith(".json") else "# installed")
    node = tmp_path / "node"
    node.write_text("server-owned Node")
    node.chmod(0o700)
    for name, value in ((runtime.REMOTION_PROJECT_DIR_ENV, project),
                        (runtime.NODE_EXECUTABLE_ENV, node),
                        (runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV, schema)):
        monkeypatch.setenv(name, str(value))
    calls = []
    def owned(argv, **kwargs):
        calls.append((argv, kwargs))
        stdout = "v20.19.4\n" if argv[-1] == "--version" else str(schema / "banodoco_timeline_schema/__init__.py")
        return subprocess.CompletedProcess(argv, 0, stdout, ""), {}
    monkeypatch.setattr(runtime, "_owned_probe", owned)
    return SimpleNamespace(project=project, schema=schema, node=node, cli=cli, calls=calls)


def test_direct_status_runs_bounded_node_and_isolated_schema_checks(installed_runtime):
    world = installed_runtime
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert status.available, status.reason
    assert (status.node_executable, status.remotion_cli, status.node_version) == (world.node, world.cli, "v20.19.4")
    assert world.calls[0][0] == [str(world.node), "--version"]
    assert world.calls[1][0][:3] == [sys.executable, "-I", "-c"]
    assert all(kwargs["timeout"] == 5 for _, kwargs in world.calls)
    assert not list(world.project.parent.rglob("remotion-validation-*.json"))


@pytest.mark.parametrize("configured", ["", "relative-node", "missing-node", "directory", "not-executable"])
def test_bad_node_is_unavailable_with_reason(installed_runtime, monkeypatch, configured):
    world = installed_runtime
    value = configured
    if configured == "missing-node":
        value = str(world.node.with_name("absent"))
    elif configured == "directory":
        value = str(world.project)
    elif configured == "not-executable":
        monkeypatch.setattr(runtime.os, "access", lambda _path, _mode: False)
        value = str(world.node)
    monkeypatch.setenv(runtime.NODE_EXECUTABLE_ENV, value)
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available
    assert runtime.NODE_EXECUTABLE_ENV in status.reason
    assert not world.calls


@pytest.mark.parametrize("version,code", [("v26.0.0", 0), ("not node", 0), ("v20.19.4", 1)])
def test_wrong_node_is_unavailable(installed_runtime, monkeypatch, version, code):
    monkeypatch.setattr(runtime, "_owned_probe", lambda argv, **kw: (subprocess.CompletedProcess(argv, code, version, "bad node"), {}))
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available and "Node" in status.reason


@pytest.mark.parametrize("package", runtime._REQUIRED_PACKAGES)
def test_each_required_package_is_checked(installed_runtime, package):
    (installed_runtime.project / "node_modules/@banodoco" / package / "package.json").unlink()
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available and f"@banodoco/{package}" in status.reason
    assert not installed_runtime.calls


def test_cli_cannot_escape_server_project(installed_runtime, monkeypatch):
    world = installed_runtime
    outside = world.project.parent / "foreign-cli.js"
    outside.write_text("// foreign")
    original = Path.resolve
    def resolve(path, *args, **kwargs):
        return outside if path == world.cli else original(path, *args, **kwargs)
    monkeypatch.setattr(Path, "resolve", resolve)
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available and "CLI escapes" in status.reason


@pytest.mark.parametrize("origin", ["relative/__init__.py", "/foreign/banodoco_timeline_schema/__init__.py"])
def test_foreign_schema_origin_is_unavailable(installed_runtime, monkeypatch, origin):
    original = runtime._owned_probe
    def owned(argv, **kwargs):
        if argv[-1] == "--version":
            return original(argv, **kwargs)
        return subprocess.CompletedProcess(argv, 0, origin, ""), {}
    monkeypatch.setattr(runtime, "_owned_probe", owned)
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available and "origin escaped trusted root" in status.reason


def test_filmstrip_backend_requires_schema_origin_before_registry_or_render(
    installed_runtime, monkeypatch, tmp_path
):
    world = installed_runtime
    launched = []

    def owned(argv, **kwargs):
        if argv[-1] == "--version":
            return subprocess.CompletedProcess(argv, 0, "v20.19.4\n", ""), {}
        return subprocess.CompletedProcess(
            argv, 0, "/foreign/banodoco_timeline_schema/__init__.py\n", ""
        ), {}

    monkeypatch.setattr(runtime, "_owned_probe", owned)
    monkeypatch.setattr(
        remotion_run,
        "_regenerate_element_registries",
        lambda *args: launched.append("registry regeneration"),
    )

    with pytest.raises(FileNotFoundError, match="origin escaped trusted root"):
        remotion_run.capture_remotion_frames(
            tmp_path / "timeline.json",
            tmp_path / "assets.json",
            tmp_path / "frames",
            [0],
            project_dir=world.project,
        )
    assert launched == []


def test_filmstrip_backend_accepts_good_schema_for_selected_server_project(
    installed_runtime, monkeypatch, tmp_path
):
    world = installed_runtime

    class ReachedRegistry(Exception):
        pass

    def stop_after_runtime_validation(*_args):
        raise ReachedRegistry

    monkeypatch.setattr(
        remotion_run, "_regenerate_element_registries", stop_after_runtime_validation
    )
    with pytest.raises(ReachedRegistry):
        remotion_run.capture_remotion_frames(
            tmp_path / "timeline.json",
            tmp_path / "assets.json",
            tmp_path / "frames",
            [0],
            project_dir=world.project,
        )


@pytest.mark.parametrize("failure", [OSError("unreadable runtime"), RuntimeError("probe cleanup unproved"), subprocess.TimeoutExpired("node", 5)])
def test_probe_failure_returns_unavailable_instead_of_raising(installed_runtime, monkeypatch, failure):
    def fail(*args, **kwargs):
        raise failure
    monkeypatch.setattr(runtime, "_owned_probe", fail)
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available and str(failure) in status.reason


def test_missing_home_preserves_windows_probe_environment(installed_runtime, monkeypatch):
    monkeypatch.delenv("HOME", raising=False)
    monkeypatch.setenv("USERPROFILE", str(installed_runtime.project.parent))
    monkeypatch.setenv("SYSTEMROOT", r"C:\Windows")
    monkeypatch.setenv("NODE_OPTIONS", "--require task-controlled.js")
    monkeypatch.setenv("PYTHONPATH", "/task-controlled")
    monkeypatch.setattr(runtime.sys, "platform", "win32")
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert status.available, status.reason
    for _, kwargs in installed_runtime.calls:
        assert "HOME" not in kwargs["env"]
        assert kwargs["env"]["USERPROFILE"] == str(installed_runtime.project.parent)
        assert kwargs["env"]["SYSTEMROOT"] == r"C:\Windows"
        assert "NODE_OPTIONS" not in kwargs["env"] and "PYTHONPATH" not in kwargs["env"]


def test_windows_stat_fstat_mode_divergence_cannot_block_status(installed_runtime, monkeypatch):
    original = os.fstat
    def windows_fstat(fd):
        facts = original(fd)
        # Windows fstat omits the path stat's permission bits for the same file.
        values = list(facts)
        values[0] = stat.S_IFMT(facts.st_mode)
        return os.stat_result(values)
    monkeypatch.setattr(os, "fstat", windows_fstat)
    status = runtime.remotion_runtime_status(require_explicit_project=True)
    assert status.available, status.reason


def test_worker_environment_keeps_server_owned_render_paths(installed_runtime):
    world = installed_runtime
    server = {runtime.NODE_EXECUTABLE_ENV: str(world.node),
              runtime.REMOTION_PROJECT_DIR_ENV: str(world.project),
              runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV: str(world.schema)}
    child = build_child_subprocess_env(base={}, parent=server, explicit_env={key: "/task-controlled" for key in server})
    assert all(child[key] == value for key, value in server.items())


def test_real_isolated_schema_probe_uses_configured_origin(tmp_path):
    import banodoco_timeline_schema
    root = Path(banodoco_timeline_schema.__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "-I", "-c", runtime._SCHEMA_PROBE, str(root),
         str(runtime.REPO_ROOT / "astrid/core/timeline/schema/timeline-config.schema.json")],
        cwd=tmp_path, env={"PATH": os.defpath}, capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).is_relative_to(root / "banodoco_timeline_schema")


@pytest.mark.parametrize("defect", ["node", "cli", "package", "schema_origin"])
def test_bad_runtime_refuses_render_with_preflight_reason_and_host_keeps_other_work(
    installed_runtime, tmp_path, monkeypatch, defect,
):
    import json

    from astrid.core.execution.generic_host import GenericPackHost
    from astrid.packs.rendering.actions.render.task_adapter import (
        RenderExportRefused,
        RenderExportTaskAdapter,
    )
    from tests.packs.rendering.test_render_export_task_adapter import _task
    from tests.test_generic_host import _write_manifest

    world = installed_runtime
    if defect == "node":
        monkeypatch.setenv(runtime.NODE_EXECUTABLE_ENV, "relative-node")
    elif defect == "cli":
        world.cli.unlink()
    elif defect == "package":
        (world.project / "node_modules/@banodoco/timeline-schema/package.json").unlink()
    else:
        original = runtime._owned_probe
        def owned(argv, **kwargs):
            if argv[-1] == "--version":
                return original(argv, **kwargs)
            return subprocess.CompletedProcess(argv, 0, "/foreign/schema.py", ""), {}
        monkeypatch.setattr(runtime, "_owned_probe", owned)
    root = tmp_path / "packs"
    _write_manifest(root / "plain", capability_id="test.plain")
    manifest = _write_manifest(root / "render", capability_id="test.render")
    definition = json.loads(manifest.read_text())
    definition["metadata"].update(adapter_family="cpu", requires_remotion=True)
    manifest.write_text(json.dumps(definition))
    host = GenericPackHost(pack_roots=[root])
    host.discover()
    host.preflight()
    assert host.capabilities["test.plain"].ready
    refused = host.capabilities["test.render"]
    assert not refused.ready
    reason = refused.preflight["remotion"]["reason"]
    assert reason == runtime.remotion_runtime_status(require_explicit_project=True).reason
    task = _task(root=tmp_path)
    task.spec["timeline_snapshot"]["config"]["clips"] = [
        {"id": "title", "at": 0, "track": "v", "clipType": "text-card", "hold": 1}]
    with pytest.raises(RenderExportRefused) as caught:
        RenderExportTaskAdapter().execute(task=task, staging_dir=tmp_path / "staging")
    assert reason in str(caught.value)


@pytest.mark.parametrize("generated", ["missing", "stale"])
def test_renderer_refuses_unsuccessful_registry_repair(tmp_path, monkeypatch, generated):
    from astrid.packs.rendering.rendering.renderers.remotion import run
    project = tmp_path / "remotion"
    src = project / "node_modules/@banodoco/timeline-composition/typescript/src"
    src.mkdir(parents=True)
    state = {"hash": "current", "content_hashes": {kind: "a" * 64 for kind in ("effects", "animations", "transitions")}}
    monkeypatch.setattr(run, "gen_effect_registry", object())
    monkeypatch.setattr(run, "_effective_registry_state", lambda _theme: state)
    if generated == "stale":
        for path in run._registry_output_paths(project):
            path.write_text("// stale")
    monkeypatch.setattr(run.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0))
    with run.remotion_lock.remotion_render_lock():
        with pytest.raises(RuntimeError, match="missing or stale after regeneration"):
            run._regenerate_element_registries_locked(project, None)
    assert not (project / run._REGISTRY_STATE_PATH).exists()


def test_installed_bundle_refuses_stale_provisioned_registry(tmp_path, monkeypatch):
    from astrid.packs.rendering.rendering.renderers.remotion import run
    project = tmp_path / "remotion"
    (project / "node_modules/@banodoco/timeline-composition/typescript/src").mkdir(parents=True)
    monkeypatch.setattr(run, "gen_effect_registry", None)
    for path in run._registry_output_paths(project):
        path.write_text("// stale")
    run._write_registry_state(project, {"content_hashes": {"effects": "a" * 64}})
    with pytest.raises(RuntimeError, match="stale generated element registries"):
        run._regenerate_element_registries_locked(project, None)
