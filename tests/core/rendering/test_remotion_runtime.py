"""Remotion admission consumes launch-bound Runtime validation."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering import remotion_runtime as runtime
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion_run


@pytest.fixture
def installed_runtime(tmp_path, monkeypatch):
    # Reuse the launch-owner fixture: direct status consumers must carry the
    # same owned probe and local-schema proof as a real host launch.
    from tests.packs.rendering.test_render_export_task_adapter import _owned_validation_fixture

    owned_probe = runtime._owned_probe
    project, schema, node, environment, reference, calls = _owned_validation_fixture(
        tmp_path, monkeypatch
    )
    def admission_probe(argv, *, cwd, env, timeout):
        assert argv == [str(node), "--version"]
        assert cwd == project and timeout == 5
        calls.append((argv, dict(env)))
        return subprocess.CompletedProcess(argv, 0, "v20.19.4\n", ""), {}

    monkeypatch.setattr(runtime, "_owned_probe", admission_probe)
    monkeypatch.setattr(runtime, "_UNRESOLVED_PROBE_CUSTODY", [])
    monkeypatch.setattr(runtime, "_UNRESOLVED_VALIDATION_PROBES", [])
    return SimpleNamespace(
        project=project, schema=schema, node=node, environment=environment,
        reference=reference, calls=calls, owned_probe=owned_probe,
    )


def _activate_server_environment(monkeypatch, world, *, overrides=None):
    # Match the launch fixture exactly; ambient loader and task inputs must not
    # change the validation context after launch.
    values = {**world.environment, **world.reference, **(overrides or {})}
    values = {name: str(value) for name, value in values.items()}
    monkeypatch.setattr(os, "environ", values)
    return values


def test_status_uses_explicit_server_environment_and_launch_reference(installed_runtime, monkeypatch):
    world = installed_runtime
    server = {**world.environment, **world.reference}
    monkeypatch.setenv(runtime.REMOTION_PROJECT_DIR_ENV, "/ambient/foreign-remotion")
    monkeypatch.setenv(runtime.NODE_EXECUTABLE_ENV, "/ambient/foreign-node")
    monkeypatch.setenv(runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV, "/ambient/foreign-schema")

    status = runtime.remotion_runtime_status(require_explicit_project=True, environment=server)

    assert status.available, status.reason
    assert status.project_dir == world.project
    assert status.node_executable == world.node
    assert status.remotion_cli == world.project / runtime.REMOTION_CLI_RELATIVE_PATH
    assert status.node_version == "v20.19.4"
    # Admission retains the three-probe launch proof and freshly checks Node.
    assert len(world.calls) == 4


@pytest.mark.parametrize("defect", ["node", "cli", "cli_escape", "package", "schema"])
def test_bad_launch_binding_disables_remotion_before_render_but_keeps_plain_work(
    installed_runtime, tmp_path, monkeypatch, defect,
):
    from astrid.core.execution.generic_host import GenericPackHost
    from astrid.packs.rendering.actions.render.task_adapter import (
        RenderExportRefused,
        RenderExportTaskAdapter,
    )
    from tests.packs.rendering.test_render_export_task_adapter import _task
    from tests.test_generic_host import _write_manifest

    world = installed_runtime
    overrides = {}
    if defect == "node":
        overrides[runtime.NODE_EXECUTABLE_ENV] = "relative-node"
    elif defect == "cli":
        (world.project / runtime.REMOTION_CLI_RELATIVE_PATH).unlink()
    elif defect == "cli_escape":
        cli = world.project / runtime.REMOTION_CLI_RELATIVE_PATH
        outside = tmp_path / "foreign-cli.js"
        outside.write_text("// foreign", encoding="utf-8")
        cli.unlink()
        cli.symlink_to(outside)
    elif defect == "package":
        (world.project / "node_modules/@banodoco/timeline-composition/package.json").unlink()
    else:
        overrides[runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV] = str(tmp_path / "foreign-schema")
    _activate_server_environment(monkeypatch, world, overrides=overrides)

    packs = tmp_path / "packs"
    _write_manifest(packs / "plain", capability_id="test.plain")
    manifest = _write_manifest(packs / "render", capability_id="test.render")
    definition = json.loads(manifest.read_text(encoding="utf-8"))
    definition["metadata"].update(adapter_family="cpu", requires_remotion=True)
    manifest.write_text(json.dumps(definition), encoding="utf-8")
    host = GenericPackHost(pack_roots=[packs])
    host.discover()
    host.preflight()

    assert host.capabilities["test.plain"].ready
    refused = host.capabilities["test.render"]
    assert not refused.ready
    reason = refused.preflight["remotion"]["reason"]
    task = _task(root=tmp_path)
    task.spec["timeline_snapshot"]["config"]["clips"] = [
        {"id": "title", "at": 0, "track": "v", "clipType": "text-card", "hold": 1}
    ]
    with pytest.raises(RenderExportRefused) as caught:
        RenderExportTaskAdapter().execute(task=task, staging_dir=tmp_path / "staging")
    assert reason in str(caught.value)


def test_windows_probe_environment_keeps_only_platform_safe_projection(monkeypatch, tmp_path):
    monkeypatch.setattr(runtime.sys, "platform", "win32")
    source = {
        "USERPROFILE": str(tmp_path), "SYSTEMROOT": r"C:\Windows",
        "NODE_OPTIONS": "--require task-controlled.js", "PYTHONPATH": "/task-controlled",
    }

    projected = runtime._probe_environment(source)

    assert projected["USERPROFILE"] == str(tmp_path)
    assert projected["SYSTEMROOT"] == r"C:\Windows"
    assert "NODE_OPTIONS" not in projected and "PYTHONPATH" not in projected


def test_schema_admission_tolerates_windows_fstat_mode_divergence(installed_runtime, monkeypatch):
    world = installed_runtime
    original = os.fstat

    def windows_fstat(fd):
        facts = original(fd)
        values = list(facts)
        values[0] = facts.st_mode & 0o170000
        return os.stat_result(values)

    monkeypatch.setattr(os, "fstat", windows_fstat)
    status = runtime.remotion_runtime_status(
        require_explicit_project=True,
        environment={**world.environment, **world.reference},
    )

    assert status.available, status.reason


def test_unresolved_probe_custody_is_fatal_to_launch_and_host_preflight(
    installed_runtime, tmp_path, monkeypatch,
):
    from astrid.core.execution import process_group
    from astrid.core.execution.generic_host import GenericPackHost, HostError
    from astrid.sdk import host_bootstrap
    from tests.test_generic_host import _write_manifest

    world = installed_runtime
    _activate_server_environment(monkeypatch, world)
    monkeypatch.setattr(runtime, "_owned_probe", world.owned_probe)
    child = SimpleNamespace(pid=12345, returncode=None)

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("node", 5)

    def cleanup_refusal(*_args, **_kwargs):
        raise RuntimeError("simulated live child; cleanup unproved")

    monkeypatch.setattr(process_group, "popen_owned_group", lambda *_a, **_k: child)
    monkeypatch.setattr(child, "communicate", timeout, raising=False)
    monkeypatch.setattr(process_group, "terminate_group", cleanup_refusal)
    with pytest.raises(runtime.RemotionProbeCleanupError) as probe_error:
        runtime._owned_probe([str(world.node), "--version"], cwd=world.project,
                             env={"PATH": os.defpath, "HOME": str(tmp_path)}, timeout=5)
    assert probe_error.value.process is child
    assert probe_error.value.cleanup_error.args == ("simulated live child; cleanup unproved",)

    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="launch is blocked") as bootstrap:
        host_bootstrap._verify_remotion_probe_custody({**world.environment, **world.reference})
    assert bootstrap.value.__cause__ is probe_error.value

    packs = tmp_path / "packs"
    manifest = _write_manifest(packs / "render", capability_id="test.render")
    definition = json.loads(manifest.read_text(encoding="utf-8"))
    definition["metadata"].update(adapter_family="cpu", requires_remotion=True)
    manifest.write_text(json.dumps(definition), encoding="utf-8")
    host = GenericPackHost(pack_roots=[packs])
    host.discover()
    with pytest.raises(HostError, match="probe cleanup is unproved") as caught:
        host.preflight()
    assert caught.value.__cause__ is probe_error.value


def test_direct_backend_validates_schema_before_registry_or_render(
    installed_runtime, monkeypatch, tmp_path,
):
    world = installed_runtime
    _activate_server_environment(
        monkeypatch, world,
        overrides={runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV: str(tmp_path / "foreign-schema")},
    )
    launched = []
    monkeypatch.setattr(
        remotion_run, "_regenerate_element_registries",
        lambda *_args: launched.append("registry regeneration"),
    )

    with pytest.raises(FileNotFoundError, match="timeline schema"):
        remotion_run.capture_remotion_frames(
            tmp_path / "timeline.json", tmp_path / "assets.json", tmp_path / "frames", [0],
            project_dir=world.project,
        )
    assert launched == []


def test_direct_backend_accepts_launch_bound_schema_before_registry(
    installed_runtime, monkeypatch, tmp_path,
):
    world = installed_runtime
    _activate_server_environment(monkeypatch, world)

    class ReachedRegistry(Exception):
        pass

    monkeypatch.setattr(
        remotion_run, "_regenerate_element_registries",
        lambda *_args: (_ for _ in ()).throw(ReachedRegistry()),
    )
    with pytest.raises(ReachedRegistry):
        remotion_run.capture_remotion_frames(
            tmp_path / "timeline.json", tmp_path / "assets.json", tmp_path / "frames", [0],
            project_dir=world.project,
        )


@pytest.mark.parametrize("generated", ["missing", "stale"])
def test_renderer_refuses_unsuccessful_registry_repair(tmp_path, monkeypatch, generated):
    project = tmp_path / "remotion"
    src = project / "node_modules/@banodoco/timeline-composition/typescript/src"
    src.mkdir(parents=True)
    state = {"hash": "current", "content_hashes": {
        kind: "a" * 64 for kind in ("effects", "animations", "transitions")
    }}
    monkeypatch.setattr(remotion_run, "gen_effect_registry", object())
    monkeypatch.setattr(remotion_run, "_effective_registry_state", lambda _theme: state)
    if generated == "stale":
        for path in remotion_run._registry_output_paths(project):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("// stale")

    def generated_process(*args, **kwargs):
        token = kwargs["env"][remotion_run.remotion_lock.REMOTION_LOCK_TOKEN_ENV]
        receipt = remotion_run.remotion_lock.REMOTION_LOCK_RECEIPT_PREFIX + token + "\n"
        return subprocess.CompletedProcess(args[0], 0, receipt, "")

    monkeypatch.setattr(remotion_run.subprocess, "run", generated_process)
    with remotion_run.remotion_lock.remotion_render_lock():
        with pytest.raises(RuntimeError, match="missing or stale after regeneration"):
            remotion_run._regenerate_element_registries_locked(project, None)
    assert not (project / remotion_run._REGISTRY_STATE_PATH).exists()
