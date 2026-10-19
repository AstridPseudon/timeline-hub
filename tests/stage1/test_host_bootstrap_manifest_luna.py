from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk import host_bootstrap


# Published by the reconciled Runtime launcher/daemon contract. Keep this
# independent of Astrid's constant so the combined-tuple mismatch is visible.
_RUNTIME_WORKER_SCOPES = (
    "handshake", "worker:register", "worker:execute", "projects:read",
    "tasks:read", "objects:read", "objects:write",
)


@pytest.mark.parametrize("validation_mode", ["plain", "reference", "refuse", "stale", "foreground"])
def test_host_bootstrap_binds_manifest_in_argv_and_reuses_exact_binding(
    tmp_path: Path, monkeypatch, validation_mode
) -> None:
    support = tmp_path / "support"
    credentials = support / "credentials"
    credentials.mkdir(parents=True)
    worker_file = credentials / "astrid-pack-host.token"
    worker_file.write_text("worker-token\n", encoding="utf-8")
    worker_file.chmod(0o600)
    source = Path(__file__).resolve().parents[2]
    captured: list[list[str]] = []

    class FakeRuntime:
        def __init__(self, *_args, **_kwargs):
            pass

        def health(self):
            return {
                "status": "ok",
                "runtime_epoch": 7,
                "runtime_instance_id": "runtime-7",
                "schema_digest": "schema-7",
            }

    class FakeProcess:
        pid = 4242

        def poll(self):
            return None

    def fake_popen(argv, **_kwargs):
        captured.append(list(argv))
        ready = Path(argv[argv.index("--ready-file") + 1])
        manifest = Path(argv[argv.index("--boot-manifest-path") + 1])
        from astrid.core._shared.boot_manifest import load_boot_manifest_hash

        expected = {
            "status": "ready",
            "pid": FakeProcess.pid,
            "process_birth_id": "birth-4242",
            "python_executable": os.path.abspath(sys.executable),
            "endpoint": "http://127.0.0.1:9999",
            "executor_id": "astrid-pack-host",
            "ready_file": str(ready),
            "credential_file": str(worker_file.resolve()),
            "support_root": str(support.resolve()),
                "source_checkout": str(source.resolve()),
                "source_checkout_digest": "source-digest",
                "source_closure_digest": argv[argv.index("--source-closure-digest") + 1],
                "source_inventory_identity": "",
                "runtime_instance_id": "runtime-7",
            "runtime_epoch": 7,
            "schema_digest": "schema-7",
            "boot_manifest_path": str(manifest),
            "boot_manifest_hash": load_boot_manifest_hash(manifest, support_root=support),
            "ready_capabilities": ["shots.example"],
        }
        expected['remotion_validation'] = {
            k: v for k, v in _kwargs['env'].items() if k.startswith('ASTRID_REMOTION_VALIDATION_')
        } or None
        ready.parent.mkdir(parents=True, exist_ok=True)
        ready.write_text(json.dumps(expected), encoding="utf-8")
        return FakeProcess()

    # This test qualifies manifest binding; readiness validation is exercised
    # independently with production-shaped launch contexts below.
    monkeypatch.delenv("ASTRID_REMOTION_PROJECT_DIR", raising=False)
    monkeypatch.setattr(host_bootstrap, "_provision_render_runtime_env", lambda *_args: None)
    monkeypatch.setattr(host_bootstrap, "RuntimeProtocolClient", FakeRuntime, raising=False)
    monkeypatch.setattr(host_bootstrap, "popen_owned_group", fake_popen)
    monkeypatch.setattr(host_bootstrap, "_host_birth_identity", lambda _pid: "birth-4242")
    monkeypatch.setattr(host_bootstrap, "_capture_native_host_launch_identity", lambda pid: {
        "pid": pid, "uid": os.getuid(), "pgid": pid, "start_sec": 1700000000, "start_usec": 1})
    monkeypatch.setattr(host_bootstrap, "_registered_host_status", lambda _state: "ours")
    monkeypatch.setattr(host_bootstrap, "_host_pid_alive", lambda _pid: True)
    stopped_groups: list[int] = []
    monkeypatch.setattr(host_bootstrap, "_stop_group", lambda pgid, **_kwargs: stopped_groups.append(pgid))
    monkeypatch.setattr(host_bootstrap, "source_checkout_digest", lambda _path: "source-digest", raising=False)

    # The bootstrap module imports these two symbols lazily in ensure_pack_host.
    monkeypatch.setattr(
        "astrid.core.execution.generic_host.RuntimeProtocolClient",
        FakeRuntime,
    )
    monkeypatch.setattr(
        "astrid.core.execution.generic_host.source_checkout_digest",
        lambda _path: "source-digest",
    )
    monkeypatch.setattr(
        "astrid.core.pack.source_setup.active_source_inventory",
        lambda: SimpleNamespace(identity="", roots=(), sources=()),
    )

    value = {
        "worker_credential_file": str(worker_file),
        "worker_actor": host_bootstrap.PACK_HOST_ACTOR,
        "worker_scopes": _RUNTIME_WORKER_SCOPES,
        "source_checkout": str(source),
        "endpoint": "http://127.0.0.1:9999",
        "runtime_epoch": 7,
    }
    if validation_mode == "refuse":
        from astrid.core.rendering.remotion_runtime import RemotionValidationError
        primary = RemotionValidationError('owned validation failed before host creation')
        def refuse(*_args):
            raise primary
        monkeypatch.setattr(host_bootstrap, '_prepare_render_validation', refuse)
        with pytest.raises(RemotionValidationError) as failure:
            host_bootstrap.ensure_pack_host(value, reconfigure_action="reconfigure")
        assert failure.value is primary
        assert not captured
        return
    validations = []
    checks = []
    if validation_mode in {"reference", "stale"}:
        from astrid.core.rendering import remotion_runtime
        marker = {'ASTRID_REMOTION_VALIDATION_PATH': str(tmp_path / 'validation.json'),
                  'ASTRID_REMOTION_VALIDATION_SHA256': 'b' * 64,
                  'ASTRID_REMOTION_VALIDATION_LAUNCH': 'c' * 32,
                  'ASTRID_REMOTION_VALIDATION_ROLE': 'host'}
        def provision(_source, environment):
            environment['ASTRID_REMOTION_PROJECT_DIR'] = str(tmp_path / 'runtime')
        def prepared(_source, environment, *_args):
            validations.append(dict(environment))
            environment.update(marker)
            return 'c' * 32
        def verify(_project, *, environment, python_executable):
            checks.append(dict(environment))
            assert all(environment[k] == v for k, v in marker.items())
            assert python_executable == os.path.abspath(sys.executable)
            if validation_mode == 'stale':
                raise remotion_runtime.RemotionValidationError('installed inputs changed')
            return {'node_version': 'v20.19.4'}
        monkeypatch.setattr(host_bootstrap, '_provision_render_runtime_env', provision)
        monkeypatch.setattr(host_bootstrap, '_prepare_render_validation', prepared)
        monkeypatch.setattr(remotion_runtime, '_validated_runtime', verify)
    if validation_mode == "foreground":
        from astrid.core.execution import generic_host

        entered = []
        monkeypatch.setattr(sys, "argv", [])
        monkeypatch.setattr(sys, "path", list(sys.path))
        monkeypatch.setattr(os, "environ", dict(os.environ))
        monkeypatch.chdir(source)

        def foreground_loop():
            from runtime_protocol import platform as runtime_platform

            # The long-running worker must not retain the bootstrap lock.
            with runtime_platform.file_lock(support / "generic-host.lock", blocking=False):
                pass
            state = json.loads((support / "generic-host.json").read_text())
            assert state["pid"] == os.getpid()
            assert state["process_birth_id"] == "birth-4242"
            assert "--register" in sys.argv
            assert sys.argv[sys.argv.index("--credential-file") + 1] == str(worker_file)
            assert sys.argv[sys.argv.index("--runtime-endpoint") + 1] == value["endpoint"]
            entered.append(True)
            return 7

        monkeypatch.setattr(generic_host, "_cli", foreground_loop)
        assert host_bootstrap.run_pack_host_foreground(value) == 7
        assert entered == [True]
        assert captured == [], "the foreground entry point must not spawn a detached host"
        return
    first = host_bootstrap.ensure_pack_host(value, reconfigure_action="reconfigure")
    manifest = support / "astrid-host" / "boot-manifest.json"
    assert manifest.is_file()
    assert "--boot-manifest-path" in captured[0]
    assert captured[0][captured[0].index("--boot-manifest-path") + 1] == str(manifest)
    assert "--boot-manifest-hash" in captured[0]
    assert captured[0][captured[0].index("--boot-manifest-hash") + 1] == first["host_boot_manifest_hash"]
    assert first["host_boot_manifest_path"] == str(manifest)
    assert first["host_boot_manifest_hash"]

    if validation_mode == 'stale':
        # A live host whose validation no longer covers this caller is replaced
        # by registration when idle, not refused (612e2230).
        second = host_bootstrap.ensure_pack_host(value, reconfigure_action="reconfigure")
        assert len(captured) == 2 and len(validations) == 2 and len(checks) == 1
        assert stopped_groups == [FakeProcess.pid]
        assert second["host_boot_manifest_path"] == str(manifest)
        assert second["host_boot_manifest_hash"]
        return
    second = host_bootstrap.ensure_pack_host(value, reconfigure_action="reconfigure")
    assert second == first
    assert len(captured) == 1
    if validation_mode == 'reference':
        assert len(validations) == 1 and len(checks) == 1
        assert captured[0][captured[0].index('--remotion-validation-launch-id') + 1] == 'c' * 32
    assert not (tmp_path / ".astrid" / "astrid.sqlite3").exists()


def test_parked_host_validation_failure_precedes_socket_and_host_creation(tmp_path, monkeypatch):
    import pytest
    import socket
    from astrid.core.rendering.remotion_runtime import RemotionValidationError

    source = tmp_path / 'source'
    source.mkdir()
    reference = SimpleNamespace(
        effective_target={'kind': 'machine', 'id': socket.gethostname()},
        source_checkout=source, pack_roots=(source,), ready_file=tmp_path / 'ready.json',
        support_root=tmp_path, dependency_closure=(), digest=lambda: 'deployment', source_closure_digest='sha256:closure')
    launch = SimpleNamespace(deployment_digest='deployment', env=lambda: {'HOME': str(tmp_path)},
                             argv=(sys.executable, '-m', 'astrid.core.execution.generic_host'), cwd=source)
    preparer = host_bootstrap._ParkedPackHostPreparer(project_launch=lambda _ref: launch)
    primary = RemotionValidationError('owned probe refused')
    monkeypatch.setattr(host_bootstrap, '_dependency_pythonpath', lambda: ())
    monkeypatch.setattr(host_bootstrap, '_provision_render_runtime_env', lambda *_args: None)
    def refuse(*_args):
        raise primary
    def unexpected(*_args, **_kwargs):
        pytest.fail('validation refusal must precede channel and host acquisition')
    monkeypatch.setattr(host_bootstrap, '_prepare_render_validation', refuse)
    monkeypatch.setattr(host_bootstrap.socket, 'socketpair', unexpected)
    monkeypatch.setattr(host_bootstrap, 'popen_owned_group', unexpected)
    with pytest.raises(RemotionValidationError) as failure:
        preparer.prepare(reference)
    assert failure.value is primary
    assert preparer._handle is None


def test_parked_host_carries_owned_validation_reference_and_launch_argument(tmp_path, monkeypatch):
    import socket
    monkeypatch.setattr(host_bootstrap.sys, "platform", "darwin")
    monkeypatch.setenv("__CF_USER_TEXT_ENCODING", "1:0")
    monkeypatch.setenv("ASTRID_TASK_RUN_ID", "ambient-task")
    source = tmp_path / 'source'
    source.mkdir()
    reference = SimpleNamespace(
        effective_target={'kind': 'machine', 'id': socket.gethostname()},
        source_checkout=source, pack_roots=(source,), ready_file=tmp_path / 'ready.json',
        support_root=tmp_path, dependency_closure=(), digest=lambda: 'deployment',
        source_closure_digest='sha256:closure', credential_ref='file:' + str(tmp_path / 'credential'),
        runtime_endpoint='http://127.0.0.1:9999', boot_manifest_path=tmp_path / 'boot.json',
        boot_manifest_hash='sha256:' + 'a' * 64)
    launch = SimpleNamespace(deployment_digest='deployment', env=lambda: {'HOME': str(tmp_path)},
                             argv=(sys.executable, '-m', 'astrid.core.execution.generic_host'), cwd=source)
    marker = {'ASTRID_REMOTION_VALIDATION_PATH': str(tmp_path / 'validation.json'),
              'ASTRID_REMOTION_VALIDATION_SHA256': 'b' * 64,
              'ASTRID_REMOTION_VALIDATION_LAUNCH': 'c' * 32,
              'ASTRID_REMOTION_VALIDATION_ROLE': 'host'}
    order = []
    def prepared(_source, environment, *_args):
        order.append('owned-validation-complete')
        environment.update(marker)
        return marker['ASTRID_REMOTION_VALIDATION_LAUNCH']
    def host_created(argv, **kwargs):
        assert order == ['owned-validation-complete']
        assert argv[argv.index('--remotion-validation-launch-id') + 1] == 'c' * 32
        assert all(kwargs['env'][k] == v for k, v in marker.items())
        assert kwargs['env']['__CF_USER_TEXT_ENCODING'] == '1:0'
        assert 'ASTRID_TASK_RUN_ID' not in kwargs['env']
        order.append('host-created')
        return SimpleNamespace(pid=4244)
    monkeypatch.setattr(host_bootstrap, '_dependency_pythonpath', lambda: ())
    monkeypatch.setattr(host_bootstrap, '_provision_render_runtime_env', lambda *_args: None)
    monkeypatch.setattr(host_bootstrap, '_prepare_render_validation', prepared)
    monkeypatch.setattr(host_bootstrap, '_host_birth_identity', lambda _pid: 'exact-birth')
    monkeypatch.setattr(host_bootstrap, "_capture_native_host_launch_identity", lambda pid: {
        "pid": pid, "uid": os.getuid(), "pgid": pid, "start_sec": 1700000000, "start_usec": 1})
    monkeypatch.setattr(host_bootstrap, 'popen_owned_group', host_created)
    monkeypatch.setattr(host_bootstrap, '_RETAINED_HOSTS', {})
    preparer = host_bootstrap._ParkedPackHostPreparer(project_launch=lambda _ref: launch)
    handle = preparer.prepare(reference)
    try:
        assert handle.state['remotion_validation'] == marker
        assert host_bootstrap._RETAINED_HOSTS[(4244, 'exact-birth')] is handle.process
    finally:
        handle.control.close()


def test_parked_host_rejects_conflicting_projected_cf_encoding(tmp_path, monkeypatch):
    import socket

    from astrid.core.subprocess_env import SubprocessEnvPolicyError

    monkeypatch.setattr(host_bootstrap.sys, "platform", "darwin")
    monkeypatch.setenv("__CF_USER_TEXT_ENCODING", "1:0")
    source = tmp_path / 'source'
    source.mkdir()
    reference = SimpleNamespace(
        effective_target={'kind': 'machine', 'id': socket.gethostname()},
        source_checkout=source, pack_roots=(source,), ready_file=tmp_path / 'ready.json',
        support_root=tmp_path, dependency_closure=(), digest=lambda: 'deployment',
        source_closure_digest='sha256:closure', credential_ref='file:' + str(tmp_path / 'credential'),
        runtime_endpoint='http://127.0.0.1:9999', boot_manifest_path=tmp_path / 'boot.json',
        boot_manifest_hash='sha256:' + 'a' * 64)
    launch = SimpleNamespace(
        deployment_digest='deployment',
        env=lambda: {'HOME': str(tmp_path), '__CF_USER_TEXT_ENCODING': '2:0'},
        argv=(sys.executable, '-m', 'astrid.core.execution.generic_host'), cwd=source)
    preparer = host_bootstrap._ParkedPackHostPreparer(project_launch=lambda _ref: launch)

    with pytest.raises(SubprocessEnvPolicyError, match='conflicts with its inherited owner pin'):
        preparer.prepare(reference)
    assert preparer._handle is None


def test_launch_and_reuse_share_exact_canonical_host_registry_context(tmp_path, monkeypatch):
    from astrid.core.rendering.remotion_runtime import _registry_context, probe_context
    from astrid.core.rendering.remotion_runtime import _UNSUPPORTED_PYTHON_STARTUP
    for name in (*_UNSUPPORTED_PYTHON_STARTUP, 'PYTHONEXECUTABLE', '__PYVENV_LAUNCHER__', 'PYTHONHOME', 'NODE_OPTIONS', 'NODE_PATH', 'NODE_ICU_DATA', 'OPENSSL_CONF'):
        monkeypatch.delenv(name, raising=False)
    for name in tuple(os.environ):
        if name.startswith(('GIT_', 'DYLD_', 'LD_')):
            monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('ASTRID_PACKS_PATH', str(tmp_path / 'foreign-pack-root'))
    monkeypatch.setenv('PYTHONPATH', str(tmp_path / 'foreign-import'))
    monkeypatch.setattr(host_bootstrap, '_dependency_pythonpath', lambda: (str(tmp_path / 'dependency'),))
    monkeypatch.setattr(host_bootstrap, '_provision_render_runtime_env', lambda source, env: env.update(ASTRID_REMOTION_PROJECT_DIR=str(source / 'remotion')))
    source = tmp_path / 'trusted-source'
    launch = host_bootstrap._host_render_environment(source)
    reuse = host_bootstrap._host_render_environment(source)
    assert 'ASTRID_PACKS_PATH' not in launch and launch == reuse
    assert launch['PYTHONPATH'] == os.pathsep.join((str(source), str(tmp_path / 'dependency')))
    assert _registry_context(launch, generator=False) == _registry_context(reuse, generator=False)
    assert probe_context(environment=launch, python_executable=sys.executable) == probe_context(environment=reuse, python_executable=sys.executable)


@pytest.mark.parametrize("defect", ["missing_project_read", "extra_admin", "reordered", "duplicate", "wrong_actor"])
def test_host_bootstrap_refuses_noncanonical_runtime_worker_handoff_before_use(
    tmp_path: Path, monkeypatch, defect: str
) -> None:
    worker = tmp_path / "credentials" / "astrid-pack-host.token"
    worker.parent.mkdir()
    worker.write_text("unused-fixture-token\n")
    worker.chmod(0o600)
    scopes = list(_RUNTIME_WORKER_SCOPES)
    actor = "astrid-pack-host"
    if defect == "missing_project_read":
        scopes.remove("projects:read")
    elif defect == "extra_admin":
        scopes.append("admin")
    elif defect == "reordered":
        scopes[0], scopes[1] = scopes[1], scopes[0]
    elif defect == "duplicate":
        scopes.append("projects:read")
    else:
        actor = "foreign-worker"
    monkeypatch.setattr(
        "astrid.core.pack.source_setup.active_source_inventory",
        lambda: SimpleNamespace(identity="", roots=(), sources=()),
    )
    used = []
    def forbidden(*_args, **_kwargs):
        used.append(True)
        raise AssertionError("invalid handoff reached credential use or child acquisition")
    monkeypatch.setattr("astrid.core.execution.generic_host.RuntimeProtocolClient", forbidden)
    monkeypatch.setattr(host_bootstrap, "_prepare_render_validation", forbidden)
    monkeypatch.setattr(host_bootstrap, "popen_owned_group", forbidden)
    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="least-privilege pack-host contract"):
        host_bootstrap.ensure_pack_host({
            "source_checkout": str(Path(__file__).resolve().parents[2]),
            "worker_credential_file": str(worker), "worker_actor": actor,
            "worker_scopes": scopes, "endpoint": "http://127.0.0.1:9999",
        }, reconfigure_action="reconfigure")
    assert not used
    assert not (tmp_path / "remotion-validation").exists()
