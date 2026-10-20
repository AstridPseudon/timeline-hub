"""A pack host is acted on by its registration, whichever process launched it."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core._shared.boot_manifest import load_boot_manifest_hash
from astrid.core.execution import generic_host
from astrid.core.execution.generic_host import (
    source_checkout_closure_digest,
    source_checkout_digest,
)
from astrid.sdk import host_bootstrap
from tests.sdk.test_host_bootstrap_source_identity import _materialize_source_closure

FAKE_PID = 4242
MODULE_ARGS = ["-m", "astrid.core.execution.generic_host", "run", "--support-root"]
# A leader that optionally keeps one child running, then idles.
LEADER = ("import subprocess,sys,time;"
          "c=subprocess.Popen([sys.executable,'-c','import sys;sys.stdin.buffer.read()'],stdin=sys.stdin,start_new_session=sys.argv[1]=='task') if sys.argv[1] in ('child','task') else None;"
          "open(sys.argv[2],'w').write(str(c.pid if c else 0));"
          "time.sleep(300 if sys.argv[3]=='stay' else 0)")


class Harness:
    def __init__(self, tmp_path: Path, monkeypatch) -> None:
        self.tmp, self.mp = tmp_path, monkeypatch
        self.source = tmp_path / "source"
        (self.source / "astrid" / "packs").mkdir(parents=True)
        _materialize_source_closure(self.source)
        self.support = tmp_path / "support"
        (self.support / "credentials").mkdir(parents=True)
        self.credential = self.support / "credentials" / "worker.token"
        self.credential.write_text("worker", encoding="utf-8")
        os.chmod(self.credential, 0o600)
        self.value = {
            "worker_credential_file": str(self.credential), "source_checkout": str(self.source),
            "worker_actor": host_bootstrap.PACK_HOST_ACTOR, "worker_scopes": list(host_bootstrap.PACK_HOST_SCOPES),
            "endpoint": "http://runtime.test", "runtime_epoch": "epoch-1",
            "runtime_instance_id": "instance-1", "schema_digest": "schema-1",
        }
        self.launches: list[dict] = []
        self.procs: list[subprocess.Popen] = []
        # The fake host writes no Remotion launch marker, so ambient Remotion provisioning must not
        # make the reuse path refuse it; the Remotion gate has its own test below.
        monkeypatch.delenv("ASTRID_REMOTION_PROJECT_DIR", raising=False)
        inventory = SimpleNamespace(identity="", roots=(), sources=())
        monkeypatch.setattr("astrid.core.pack.source_setup.active_source_inventory", lambda: inventory)

        class Client:
            def __init__(self, *_a): pass
            def health(self):
                return {"status": "ok", "runtime_epoch": "epoch-1", "runtime_instance_id": "instance-1",
                        "schema_digest": "schema-1"}
            def _authenticate_worker(self, _executor_id):
                return "realm-1"
            @property
            def generated(self):
                return SimpleNamespace(get_executor=lambda _executor_id: SimpleNamespace(
                    executor_id=host_bootstrap.PACK_HOST_ACTOR, readiness="ready",
                    runtime_epoch="epoch-1", source_epoch="source-epoch-1",
                    source_digest="source-digest-1", dependency_digest="dependency-digest-1",
                    capabilities=[SimpleNamespace(status="ready")],
                ))
        monkeypatch.setattr(generic_host, "RuntimeProtocolClient", Client)
        real_birth = host_bootstrap._host_birth_identity
        monkeypatch.setattr(host_bootstrap, "_host_birth_identity",
                            lambda pid: "birth-1" if pid == FAKE_PID else real_birth(pid))
        monkeypatch.setattr(host_bootstrap, "popen_owned_group", self._popen)
        monkeypatch.setattr(host_bootstrap, "_IDLE_CHECK_INTERVAL_SECONDS", 0.0)
        monkeypatch.setattr(host_bootstrap, "_GROUP_GRACE_SECONDS", 2.0)

    def _popen(self, argv, **kwargs):
        self.launches.append({"argv": list(argv), "env": kwargs["env"]})
        manifest = self.support / "astrid-host" / "boot-manifest.json"
        (self.support / "generic-host.ready.json").write_text(json.dumps({
            "status": "ready", "pid": FAKE_PID, "process_birth_id": "birth-1",
            "python_executable": host_bootstrap._pack_host_python_executable(),
            "endpoint": "http://runtime.test", "executor_id": host_bootstrap.PACK_HOST_ACTOR,
            "ready_file": str(self.support / "generic-host.ready.json"),
            "credential_file": str(self.credential), "support_root": str(self.support),
            "source_checkout": str(self.source), "source_checkout_digest": source_checkout_digest(self.source),
            "source_closure_digest": source_checkout_closure_digest(self.source),
            "source_inventory_identity": "",
            "boot_manifest_path": str(manifest),
            "boot_manifest_hash": load_boot_manifest_hash(manifest, support_root=self.support),
            "runtime_instance_id": "instance-1", "runtime_epoch": "epoch-1", "schema_digest": "schema-1",
            "source_epoch": "source-epoch-1",
            "registration": {
                "source_epoch": "source-epoch-1", "source_digest": "source-digest-1",
                "dependency_digest": "dependency-digest-1",
            },
            "ready_capabilities": [],
        }), encoding="utf-8")
        return SimpleNamespace(pid=FAKE_PID, poll=lambda: None)

    def ensure(self):
        return host_bootstrap.ensure_pack_host(self.value, reconfigure_action="reconfigure")

    def marker(self, name="generic-host.json") -> dict:
        return json.loads((self.support / name).read_text(encoding="utf-8"))

    def register(self, pid: int, birth: str | None = None, **changes) -> None:
        """Point the markers a first (fake) launch wrote at *pid*."""
        for name in ("generic-host.json", "generic-host.ready.json"):
            data = self.marker(name)
            data.update(pid=pid, process_birth_id=birth or host_bootstrap._host_birth_identity(pid))
            if name == "generic-host.json":
                data.update(changes)
            (self.support / name).write_text(json.dumps(data), encoding="utf-8")

    def host(self, child: str = "none", stay: bool = True) -> tuple[subprocess.Popen, int]:
        """A real process leading its own session that looks like a pack host."""
        record = self.tmp / f"child-{len(self.procs)}.pid"
        proc = subprocess.Popen([sys.executable, "-c", LEADER, child, str(record), "stay" if stay else "go",
                                 *MODULE_ARGS, str(self.support)], start_new_session=True, stdin=subprocess.PIPE)
        self.procs.append(proc)
        deadline = time.monotonic() + 10
        while not record.exists() or not record.read_text():
            assert time.monotonic() < deadline
            time.sleep(0.05)
        return proc, int(record.read_text())

    def kill_leader(self, proc: subprocess.Popen) -> None:
        """Register the live leader (so its start time is recorded), then kill only it."""
        self.register(proc.pid)
        os.kill(proc.pid, signal.SIGKILL)
        proc.wait()

    def cleanup(self) -> None:
        for proc in self.procs:
            if proc.stdin is not None:
                proc.stdin.close()
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            proc.wait()


@pytest.fixture
def harness(tmp_path, monkeypatch):
    h = Harness(tmp_path, monkeypatch)
    h.ensure()  # a first launch writes the markers every case starts from
    h.launches.clear()
    yield h
    h.cleanup()


def test_launcher_attaches_to_healthy_host_from_another_checkout(harness, monkeypatch, tmp_path):
    h = harness
    second = tmp_path / "second-source"
    (second / "astrid" / "packs").mkdir(parents=True)
    _materialize_source_closure(second)
    h.value["source_checkout"] = str(second)
    monkeypatch.setattr(host_bootstrap, "_registered_host_status", lambda _state: "ours")
    from astrid.core.gateway import dispatch
    monkeypatch.setattr(
        dispatch, "compose_profile_handoff",
        lambda *_args, **_kwargs: pytest.fail("attach must preserve the resident boot manifest"),
    )

    result = host_bootstrap.ensure_pack_host(
        h.value, reconfigure_action="reconfigure", attach_healthy=True,
    )

    assert result["host_status"] == "ready"
    assert result["host_pid"] == FAKE_PID
    assert result["host_source_checkout_digest"] == source_checkout_digest(h.source)
    assert h.launches == []


@pytest.mark.parametrize("fault", [
    "unready-registration", "changed-registration-generation", "changed-resident-source",
])
def test_launcher_replaces_cross_checkout_host_when_resident_is_unhealthy(
    harness, monkeypatch, tmp_path, fault,
):
    h = harness
    resident_source = h.source
    second = tmp_path / "second-source"
    (second / "astrid" / "packs").mkdir(parents=True)
    _materialize_source_closure(second)
    h.value["source_checkout"] = str(second)
    h.source = second
    monkeypatch.setattr(host_bootstrap, "_registered_host_status", lambda _state: "ours")
    monkeypatch.setattr(host_bootstrap, "_host_idle", lambda *_args: True)
    retired = []
    monkeypatch.setattr(host_bootstrap, "_retire_host_locked", lambda state: retired.append(dict(state)))

    if fault == "unready-registration":
        client_type = generic_host.RuntimeProtocolClient

        class UnreadyClient(client_type):
            @property
            def generated(self):
                return SimpleNamespace(get_executor=lambda _executor_id: SimpleNamespace(
                    executor_id=host_bootstrap.PACK_HOST_ACTOR, readiness="starting",
                    runtime_epoch="epoch-1", source_epoch="source-epoch-1",
                    source_digest="source-digest-1", dependency_digest="dependency-digest-1",
                    capabilities=[SimpleNamespace(status="ready")],
                ))

        monkeypatch.setattr(generic_host, "RuntimeProtocolClient", UnreadyClient)
    elif fault == "changed-registration-generation":
        client_type = generic_host.RuntimeProtocolClient

        class SupersededClient(client_type):
            @property
            def generated(self):
                return SimpleNamespace(get_executor=lambda _executor_id: SimpleNamespace(
                    executor_id=host_bootstrap.PACK_HOST_ACTOR, readiness="ready",
                    runtime_epoch="epoch-1", source_epoch="source-epoch-2",
                    source_digest="source-digest-1", dependency_digest="dependency-digest-1",
                    capabilities=[SimpleNamespace(status="ready")],
                ))

        monkeypatch.setattr(generic_host, "RuntimeProtocolClient", SupersededClient)
    else:
        (resident_source / "astrid" / "packs" / "changed.marker").write_text("changed")
    result = host_bootstrap.ensure_pack_host(
        h.value, reconfigure_action="reconfigure", attach_healthy=True,
    )

    assert result["host_status"] == "ready"
    assert len(retired) == 1
    assert len(h.launches) == 1


def _defunct(pid: int) -> bool:
    """True for a terminated process whose parent has not reaped it yet."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
    except OSError:
        return False
    return stat.rpartition(")")[2].split()[:1] == ["Z"]


def _gone(pid: int, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except OSError:
            return True
        if _defunct(pid):
            return True  # killed, awaiting a reaper (a container's PID 1 may reap late)
        time.sleep(0.05)
    return False


def test_gone_host_with_empty_group_is_dropped_and_relaunched(harness):
    proc, _ = harness.host()
    harness.kill_leader(proc)
    harness.ensure()
    assert len(harness.launches) == 1
    assert harness.marker()["pid"] == FAKE_PID


def test_dead_leader_with_surviving_member_is_killed_then_dropped(harness):
    proc, member = harness.host(child="child")
    harness.kill_leader(proc)
    assert not _gone(member, 0.2), "the orphan must be alive before recovery"
    harness.ensure()
    assert _gone(member), "orphan in the dead host's group must be killed"
    assert len(harness.launches) == 1 and harness.marker()["pid"] == FAKE_PID


def test_live_host_with_stale_source_is_retired_by_registration_when_idle(harness):
    proc, _ = harness.host()
    harness.register(proc.pid, source_closure_digest="stale")
    harness.ensure()
    assert proc.wait(timeout=10) is not None
    assert len(harness.launches) == 1 and harness.marker()["pid"] == FAKE_PID


def test_busy_live_host_is_deferred_and_untouched(harness):
    proc, child = harness.host(child="task")  # task work runs in its own session
    harness.register(proc.pid, source_closure_digest="stale")
    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="busy"):
        harness.ensure()
    assert proc.poll() is None and not _gone(child, 0.2)
    assert harness.marker()["pid"] == proc.pid and not harness.launches


def test_live_matching_host_is_reused(harness):
    proc, _ = harness.host()
    harness.register(proc.pid)
    assert harness.ensure()["host_pid"] == proc.pid
    assert not harness.launches and proc.poll() is None


def test_spawn_env_excludes_job_lease(harness, monkeypatch):
    monkeypatch.setenv("OTTO_HEAVY_LEASE", "lease-123")
    monkeypatch.setenv("KEEP_ME", "1")
    harness.register(harness.host()[0].pid, source_closure_digest="stale")
    harness.ensure()
    env = harness.launches[0]["env"]
    assert "OTTO_HEAVY_LEASE" not in env and env["KEEP_ME"] == "1"


def test_pid_reused_by_unrelated_process_is_never_signalled(harness):
    proc, child = harness.host(child="child")
    harness.register(proc.pid, birth="not-its-start-time")
    harness.ensure()
    assert proc.poll() is None and not _gone(child, 0.2)
    assert len(harness.launches) == 1 and harness.marker()["pid"] == FAKE_PID
    with pytest.raises(host_bootstrap.PackHostBootstrapError):
        host_bootstrap._stop_group(os.getpgrp())  # never our own group


def test_host_whose_validation_does_not_cover_this_caller_is_replaced_not_refused(harness, monkeypatch):
    # Before: "prior Remotion launch validation is stale; reconfigure explicitly",
    # and the healthy host stayed unusable for this caller. Now it is replaced when idle.
    from astrid.core.rendering import remotion_runtime
    proc, _ = harness.host()
    reference = {"ASTRID_REMOTION_VALIDATION_PATH": "/x", "ASTRID_REMOTION_VALIDATION_SHA256": "a" * 64,
                 "ASTRID_REMOTION_VALIDATION_LAUNCH": "b" * 32, "ASTRID_REMOTION_VALIDATION_ROLE": "host"}
    harness.register(proc.pid, remotion_validation=reference)
    ready = harness.marker("generic-host.ready.json")
    ready["remotion_validation"] = reference
    (harness.support / "generic-host.ready.json").write_text(json.dumps(ready), encoding="utf-8")
    monkeypatch.setattr(host_bootstrap, "_host_render_environment",
                        lambda _source: {"ASTRID_REMOTION_PROJECT_DIR": str(harness.tmp)})
    def stale(*_a, **_k):
        raise remotion_runtime.RemotionValidationError("consumer context differs")
    monkeypatch.setattr(remotion_runtime, "_validated_runtime", stale)
    monkeypatch.setattr(host_bootstrap, "_prepare_render_validation", lambda *a, **k: None)  # the fresh launch
    harness.ensure()
    assert len(harness.launches) == 1 and harness.marker()["pid"] == FAKE_PID
    assert proc.wait(timeout=10) is not None


def test_host_helper_in_its_own_group_is_not_work(harness):
    # The per-claim git preflight runs in the host's own process group: not a task.
    proc, helper = harness.host(child="child")
    harness.register(proc.pid, source_closure_digest="stale")
    harness.ensure()
    assert proc.wait(timeout=10) is not None and len(harness.launches) == 1


def test_published_busy_record_decides(harness):
    proc, _ = harness.host()
    harness.register(proc.pid, source_closure_digest="stale")
    busy = harness.support / "generic-host.busy.json"
    busy.write_text(json.dumps({"pid": proc.pid, "active": 1}), encoding="utf-8")
    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="busy"):
        harness.ensure()
    assert proc.poll() is None
    busy.write_text(json.dumps({"pid": proc.pid, "active": 0}), encoding="utf-8")
    harness.ensure()
    assert proc.wait(timeout=10) is not None and len(harness.launches) == 1


def test_host_publishes_its_in_flight_task_count(tmp_path):
    from astrid.core.execution import generic_host
    path = tmp_path / generic_host.BUSY_NAME
    generic_host._publish_busy(path, +1)
    assert json.loads(path.read_text())["active"] >= 1 and json.loads(path.read_text())["pid"] == os.getpid()
    generic_host._publish_busy(path, -1)
    assert json.loads(path.read_text())["active"] == 0
    assert oct(path.stat().st_mode & 0o777) == oct(0o600)



def test_stop_group_signals_anchored_group_and_refuses_a_reused_leader(owned_process_groups):
    from astrid.core.execution.process_group import process_birth_identity
    code = ("import subprocess,sys,time;"
            "subprocess.Popen([sys.executable,'-c','import time;time.sleep(300)']);time.sleep(300)")
    proc = subprocess.Popen([sys.executable, "-c", code], start_new_session=True)
    owned_process_groups.record(proc)
    try:
        deadline = time.monotonic() + 15
        while len(host_bootstrap._group_survivors(proc.pid)) < 2 and time.monotonic() < deadline:
            time.sleep(0.05)
        birth = process_birth_identity(proc.pid)
        assert birth and len(host_bootstrap._group_survivors(proc.pid)) == 2
        with pytest.raises(host_bootstrap.PackHostBootstrapError, match="reused"):
            host_bootstrap._stop_group(proc.pid, leader_birth=birth + "x")
        assert proc.poll() is None
        host_bootstrap._stop_group(proc.pid, grace=2.0, leader_birth=birth)
        proc.wait(timeout=10)
        assert not host_bootstrap._group_survivors(proc.pid)
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.wait()


def test_stop_group_signals_only_the_registered_anchored_group(monkeypatch):
    calls = []
    census = {
        4321: SimpleNamespace(pid=4321, pgid=4321, birth="birth-current"),
        4322: SimpleNamespace(pid=4322, pgid=4321, birth="child-birth"),
    }
    monkeypatch.setattr(host_bootstrap, "_process_snapshot", lambda: census)
    monkeypatch.setattr(host_bootstrap, "_host_pid_alive", lambda _pid: True)
    monkeypatch.setattr(host_bootstrap.os, "getpid", lambda: 9999)
    monkeypatch.setattr(host_bootstrap.os, "getpgrp", lambda: 8765)
    def killpg(*args):
        calls.append(args)
        census.clear()
    monkeypatch.setattr(host_bootstrap.os, "killpg", killpg)

    host_bootstrap._stop_group(4321, grace=0, leader_birth="birth-current")
    assert calls == [(4321, signal.SIGTERM)]

    calls.clear()
    census.update({
        4321: SimpleNamespace(pid=4321, pgid=4321, birth="replacement-birth"),
        4322: SimpleNamespace(pid=4322, pgid=4321, birth="child-birth"),
    })
    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="reused"):
        host_bootstrap._stop_group(4321, grace=0, leader_birth="birth-current")
    assert calls == []

    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="unsafe"):
        host_bootstrap._stop_group(8765, grace=0, leader_birth="birth-current")
    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="lacks a leader birth anchor"):
        host_bootstrap._stop_group(4321, grace=0)
    assert calls == []


def test_stop_group_rechecks_leader_birth_before_escalation(monkeypatch):
    leader = SimpleNamespace(pid=4321, pgid=4321, birth="registered-birth")
    calls = []
    monkeypatch.setattr(host_bootstrap, "_process_snapshot", lambda: {4321: leader})
    monkeypatch.setattr(host_bootstrap, "_host_pid_alive", lambda _pid: True)
    monkeypatch.setattr(host_bootstrap.os, "getpid", lambda: 9999)
    monkeypatch.setattr(host_bootstrap.os, "getpgrp", lambda: 8765)
    def killpg(pgid, signum):
        calls.append((pgid, signum))
        leader.birth = "replacement-birth"
    monkeypatch.setattr(host_bootstrap.os, "killpg", killpg)

    with pytest.raises(host_bootstrap.PackHostBootstrapError, match="reused"):
        host_bootstrap._stop_group(4321, grace=0, leader_birth="registered-birth")
    assert calls == [(4321, signal.SIGTERM)]
