"""Offline handoff checks and centrally run real startup/catalog/cleanup smoke."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from astrid.core._shared.boot_manifest import load_boot_manifest_hash
from astrid.core.execution.generic_host import (
    RuntimeProtocolClient,
    source_checkout_closure_digest,
    source_checkout_digest,
)
from astrid.sdk import host_bootstrap
from tests.packs.rendering import real_pack_host
from tests.packs.rendering.real_pack_host import RealPackHost, _handoff


@pytest.mark.parametrize("change", ["instance", "realm", "credential", "scopes", "symlink"])
def test_handoff_rejects_foreign_inputs_before_launch(tmp_path, change):
    support = tmp_path / "support"
    support.mkdir()
    value = {
        "runtime_instance_id": "instance", "realm_root": str(tmp_path / "realm"),
        "worker_credential_file": str(support / "credentials" / "astrid-pack-host.token"),
        "worker_actor": host_bootstrap.PACK_HOST_ACTOR,
        "worker_scopes": list(host_bootstrap.PACK_HOST_SCOPES),
    }
    if change == "instance":
        value["runtime_instance_id"] = "another"
    elif change == "realm":
        value["realm_root"] = str(tmp_path / "another")
    elif change == "credential":
        value["worker_credential_file"] = str(tmp_path / "foreign.token")
    elif change == "scopes":
        value["worker_scopes"] = ["admin"]
    discovery = support / "discovery.json"
    discovery.write_text(json.dumps(value))
    if change == "symlink":
        discovery.rename(support / "original.json")
        discovery.symlink_to(support / "original.json")
    with pytest.raises((ValueError, RuntimeError)):
        _handoff(tmp_path / "realm", support, discovery, Path(__file__).resolve().parents[3], "instance")


def test_cleanup_refuses_replaced_registration(tmp_path):
    original = {"pid": 123, "process_birth_id": "original"}
    replacement = {"pid": os.getpid(), "process_birth_id": "replacement"}
    marker = tmp_path / "generic-host.json"
    marker.write_text(json.dumps(replacement))
    host = RealPackHost(tmp_path, original, {})
    with pytest.raises(RuntimeError, match="registration changed"):
        host.close()
    assert json.loads(marker.read_text()) == replacement
    assert not host.closed


def _exercise_boundary(root, boundary, signum):
    """Isolated OS-signal test; doubles inject races, never qualify production launch."""
    support = Path(root)
    credential = support / "credentials" / "worker.token"
    credential.parent.mkdir()
    credential.write_text("offline-test-double")
    value = {"worker_credential_file": str(credential), "endpoint": "offline",
             "active_realm": "realm"}
    events = []
    children = []
    marker = support / "generic-host.json"
    ready_marker = support / "generic-host.ready.json"
    real_waitpid = os.waitpid
    signalled = False

    def inject(where):
        nonlocal signalled
        if boundary == where and not signalled:
            signalled = True
            os.kill(os.getpid(), signum)
            events.append("sent")

    def spawn():
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"],
                                 start_new_session=True)
        children.append(child)
        return child

    own = spawn()
    state = {"pid": own.pid, "process_birth_id": host_bootstrap._host_birth_identity(own.pid),
             "support_root": str(support)}
    result = {"host_pid": own.pid, "host_status": "ready",
              "host_ready_capabilities": ["rendering.render"]}

    def ensure(*_args, **_kwargs):
        blocked = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        assert not blocked.intersection({signal.SIGINT, signal.SIGTERM, signal.SIGALRM})
        registration = state.copy()
        if boundary == "replacement":
            foreign = spawn()
            registration.update(pid=foreign.pid,
                                process_birth_id=host_bootstrap._host_birth_identity(foreign.pid))
        elif boundary == "birth":
            registration["process_birth_id"] = "another-incarnation"
        elif boundary == "nonchild":
            result["host_pid"] = os.getpid()
            registration.update(pid=os.getpid(),
                                process_birth_id=host_bootstrap._host_birth_identity(os.getpid()))
        marker.write_text(json.dumps(registration))
        ready_marker.write_text("{}")
        inject("returned")
        return result

    def read(path):
        # A second lock acquisition must fail while adoption owns the real lock.
        if "read" not in events:
            with pytest.raises(Exception, match="lifecycle is busy"):
                with real_pack_host._pack_host_lock(support):
                    pass
        events.append("read")
        inject("adoption")
        return json.loads(path.read_text())

    def retire(adopted):
        assert adopted == state  # Never accept a replacement cleanup handle.
        events.append("retire")
        inject("retire")
        assert "delivered" not in events
        own.terminate()
        os.waitid(os.P_PID, own.pid, os.WEXITED | os.WNOWAIT)
        marker.unlink()
        ready_marker.unlink()
        if boundary == "cleanup-failure":
            inject("cleanup-failure")
            raise RuntimeError("injected cleanup failure")

    def waitpid(pid, options):
        inject("child-proof" if options else "reap")
        if not options:
            assert "delivered" not in events
            events.append("reap")
        return real_waitpid(pid, options)

    def interrupted(_sig, _frame):
        events.append("delivered")
        # Pending launch/cleanup signals reach the original handler AFTER cleanup.
        assert not marker.exists() and not ready_marker.exists()
        assert own.poll() is not None
        raise SystemExit(23)

    client = SimpleNamespace(
        health=lambda: {"runtime_instance_id": "instance"},
        _authenticate_worker=lambda _actor: "realm",
        generated=SimpleNamespace(list_capabilities=lambda **_kw: (
            [SimpleNamespace(capability_id="rendering.render", status="ready")], None)),
    )
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGALRM):
        signal.signal(sig, interrupted)
    try:
        with ExitStack() as patches:
            patches.enter_context(patch.object(real_pack_host, "_handoff", return_value=value))
            patches.enter_context(patch.object(real_pack_host, "RuntimeProtocolClient", return_value=client))
            adopted = patches.enter_context(patch.object(real_pack_host, "RealPackHost", wraps=RealPackHost))
            patches.enter_context(patch.object(host_bootstrap, "ensure_pack_host", side_effect=ensure))
            patches.enter_context(patch.object(host_bootstrap, "_read_object", side_effect=read))
            patches.enter_context(patch.object(host_bootstrap, "_registered_host_status", return_value="ours"))
            patches.enter_context(patch.object(host_bootstrap, "_retire_host_locked", side_effect=retire))
            patches.enter_context(patch.object(os, "waitpid", side_effect=waitpid))
            try:
                with real_pack_host.start_real_pack_host(
                        realm_dir=support, support_dir=support, discovery_file=support,
                        source_checkout=support, runtime_instance_id="instance"):
                    assert boundary in ("retire", "reap", "cleanup-failure")
            except SystemExit as exc:
                assert exc.code == 23
                assert events.index("retire") < events.index("delivered")
            except RuntimeError as exc:
                if boundary in ("replacement", "birth", "nonchild"):
                    adopted.assert_not_called()
                    assert "retire" not in events
                    assert marker.exists() and ready_marker.exists()
                    assert all(child.poll() is None for child in children)
                    assert "registration differs" in str(exc) or "not this helper's child" in str(exc)
                else:
                    assert boundary == "cleanup-failure"
                    assert str(exc) == "injected cleanup failure"
            else:
                raise AssertionError("expected signal or ownership refusal")
        assert signal.pthread_sigmask(signal.SIG_BLOCK, []) == set()
        assert all(signal.getsignal(sig) == interrupted
                   for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGALRM))
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
            child.wait(timeout=5)


@pytest.mark.parametrize("boundary", ["replacement", "birth", "nonchild"])
def test_adoption_never_constructs_replacement_cleanup_handle(tmp_path, boundary):
    _run_boundary_process(tmp_path, boundary, signal.SIGTERM)


@pytest.mark.parametrize("boundary", ["returned", "adoption", "child-proof", "retire", "reap"])
@pytest.mark.parametrize("sig", [signal.SIGINT, signal.SIGTERM, signal.SIGALRM])
def test_pending_signal_cleans_owned_child_before_delivery(tmp_path, boundary, sig):
    _run_boundary_process(tmp_path, boundary, sig)


def test_cleanup_failure_surfaces_with_pending_termination(tmp_path):
    _run_boundary_process(tmp_path, "cleanup-failure", signal.SIGTERM)


def _run_boundary_process(tmp_path, boundary, sig):
    code = ("from tests.packs.rendering.test_real_pack_host import _exercise_boundary; "
            "import sys; _exercise_boundary(sys.argv[1], sys.argv[2], int(sys.argv[3]))")
    result = subprocess.run([sys.executable, "-c", code, str(tmp_path), boundary, str(int(sig))],
                            capture_output=True, text=True, timeout=25)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.integration
@pytest.mark.timeout(240)
@pytest.mark.parametrize("stop", ["explicit", "eof", "sigterm"])
def test_real_host_cli_catalog_and_owned_group_cleanup(tmp_path, real_runtime, owned_process_groups, stop):
    # Match DirectHarness.start(), which creates private support before the daemon.
    (tmp_path / "support").mkdir(mode=0o700)
    daemon = real_runtime(production_worker_credentials=True)
    source = Path(__file__).resolve().parents[3]
    discovery = daemon.support_root / "discovery.json"
    value = json.loads(discovery.read_text())
    command = [sys.executable, "-m", "tests.packs.rendering.real_pack_host",
               "--realm-dir", str(daemon.root), "--support-dir", str(daemon.support_root),
               "--discovery-file", str(discovery), "--source-checkout", str(source),
               "--runtime-instance-id", value["runtime_instance_id"]]
    child_env = {**os.environ, "PYTHONPATH": str(source)}
    # conftest adds a pytest bytecode cache override, which authentic launch
    # validation correctly rejects. DirectHarness does not use that override.
    child_env.pop("PYTHONPYCACHEPREFIX", None)
    process = owned_process_groups.popen(
        command, cwd=source, env=child_env,
        start_new_session=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        line = process.stdout.readline()
        ready = json.loads(line)
        assert ready["status"] == "ready", ready
        pid = ready["host_pid"]
        assert pid != os.getpid() and os.getpgid(pid) == pid
        assert ready["host_runtime_instance_id"] == daemon.instance_id
        assert ready["host_source_checkout_digest"] == source_checkout_digest(source)
        assert ready["host_source_closure_digest"] == source_checkout_closure_digest(source)
        assert ready["host_boot_manifest_hash"] == load_boot_manifest_hash(
            Path(ready["host_boot_manifest_path"]), support_root=daemon.support_root)
        assert "rendering.render" in ready["host_ready_capabilities"]
        state = json.loads((daemon.support_root / "generic-host.json").read_text())
        assert state["remotion_validation"]
        # A second actual CLI must never attach to or retire the first one's host.
        foreign = subprocess.run(command, cwd=source, env=child_env, input="stop\n",
                                 capture_output=True, text=True, timeout=40)
        assert foreign.returncode == 1
        assert json.loads(foreign.stdout)["status"] == "failed"
        assert json.loads((daemon.support_root / "generic-host.json").read_text()) == state
        assert os.getpgid(pid) == pid
        assert RuntimeProtocolClient(daemon.endpoint, daemon.worker_token).health().status == "ok"
    finally:
        if stop == "sigterm":
            process.send_signal(signal.SIGTERM)
        stdout, stderr = process.communicate("stop\n" if stop == "explicit" else "", timeout=40)
    assert process.returncode == (1 if stop == "sigterm" else 0), stderr
    if stop != "sigterm":
        assert json.loads(stdout)["status"] == "stopped"
    assert not host_bootstrap._group_survivors(pid)
    assert not (daemon.support_root / "generic-host.json").exists()
    assert not (daemon.support_root / "generic-host.ready.json").exists()
    assert RuntimeProtocolClient(daemon.endpoint, daemon.worker_token).health().status == "ok"
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
