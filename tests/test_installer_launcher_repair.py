"""Installed launcher behavior and repair's service health decision."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from astrid.installer.backend import Backend
from astrid.installer.core import Installer, VerificationError, Version, write_json
from astrid.installer.launcher import install
from runtime_protocol.door import DEFAULT_DOOR_PORT


def test_absolute_launcher_works_with_clean_home_and_unchanged_path(tmp_path):
    root = tmp_path / "Astrid Program Folder"
    version_root = root / "versions" / "v1"
    python = version_root / "py" / "bin" / "python"
    python.parent.mkdir(parents=True)
    record = {
        "root": str(version_root), "python": str(python),
        "profile": str(version_root / "profile.json"),
        "env": {"ASTRID_TEST_MANAGED": "yes"},
    }
    write_json(version_root / "version.json", record)
    (root / "current").write_text("v1\n", encoding="utf-8")
    launcher, runner = install(root)
    assert launcher.is_absolute() and runner.is_file()

    fake_python = (
        f"#!{sys.executable}\n"
        "import json, os, runpy, sys\n"
        "if len(sys.argv) > 2 and sys.argv[1] == '-I' and sys.argv[2].endswith('run_astrid.py'):\n"
        "    script = sys.argv[2]; sys.argv = [script, *sys.argv[3:]]; runpy.run_path(script, run_name='__main__')\n"
        "else:\n"
        "    print(json.dumps({'args': sys.argv[1:], 'path': os.environ['PATH'], 'home': os.environ['HOME'], 'managed': os.environ['ASTRID_TEST_MANAGED'], 'root': os.environ['ASTRID_INSTALL_PROGRAM_ROOT']}))\n"
    )
    python.write_text(fake_python, encoding="utf-8")
    python.chmod(0o755)
    home = tmp_path / "fresh-home"
    home.mkdir()
    inherited_path = os.environ.get("PATH", "/usr/bin:/bin")
    env = {"HOME": str(home), "PATH": inherited_path}
    result = subprocess.run([str(launcher)], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True)

    assert json.loads(result.stdout) == {
        "args": ["-I", "-m", "astrid.omp_agent"],
        "path": inherited_path,
        "home": str(home),
        "managed": "yes",
        "root": str(root),
    }

    next_root = root / "versions" / "v2"
    next_python = next_root / "py" / "bin" / "python"
    next_python.parent.mkdir(parents=True)
    next_python.write_text(fake_python, encoding="utf-8")
    next_python.chmod(0o755)
    record.update({"root": str(next_root), "python": str(next_python),
                   "profile": str(next_root / "profile.json"), "env": {"ASTRID_TEST_MANAGED": "new"}})
    write_json(next_root / "version.json", record)
    (root / "current").write_text("v2\n", encoding="utf-8")
    result = subprocess.run([str(launcher)], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True)
    assert json.loads(result.stdout)["managed"] == "new"


@pytest.mark.parametrize("service_state,raises", [("running", False), ("failed", True)])
def test_verification_rejects_failed_declared_service(tmp_path, monkeypatch, service_state, raises):
    root, data = tmp_path / "program", tmp_path / "workspace"
    version_root = root / "versions" / "v1"
    version = Version(version_root, Path(sys.executable), version_root / "profile.json", {})
    endpoint = f"http://127.0.0.1:{DEFAULT_DOOR_PORT}"
    write_json(data / "runtime" / "discovery.json", {
        "door_endpoint": endpoint, "active_realm": "realm", "runtime_instance_id": "instance",
    })
    status = {"discovery": {"runtime_instance_id": "instance"}, "support": {"pid_alive": True}}
    health = {"status": "ok", "runtime_instance_id": "instance", "services": [
        {"name": "chat", "state": service_state},
    ]}
    realm = {"realm_id": "realm"}

    class Response:
        def __init__(self, value):
            self.value = value

        def __enter__(self):
            return self

        def __exit__(self, *_):
            pass

        def read(self):
            return json.dumps(self.value).encode()

    class Opener:
        def open(self, request, timeout):
            path = request.full_url.removeprefix(endpoint)
            return Response({"/api/runtime/v1/health": health, "/api/runtime/v1/realm": realm}[path])

    backend = Backend(root, tmp_path / "log", Path(sys.executable))
    monkeypatch.setattr(backend, "runtime", lambda *_args, **_kwargs: status)
    monkeypatch.setattr("astrid.installer.backend.urllib.request.build_opener", lambda *_: Opener())
    monkeypatch.setattr("astrid.installer.backend.time.sleep", lambda _: None)

    if raises:
        with pytest.raises(VerificationError, match="declared Astrid service is failed"):
            backend.verify(version, data, "realm", timeout=0.01)
    else:
        backend.verify(version, data, "realm", timeout=0.01)


class ProcessBackend:
    def __init__(self, root, data, *, failed_service):
        self.root, self.data, self.failed_service = root, data, failed_service
        self.runtime = self._child()
        self.service = self._child()
        self.old_processes = ()
        self.verify_count = 0

    @staticmethod
    def _child():
        return subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])

    def workspace(self, *_):
        return {"realm_id": "realm", "realm_root": str(self.data / "realm")}

    def verify(self, *_args, **_kwargs):
        self.verify_count += 1
        if self.failed_service and self.verify_count == 1:
            raise VerificationError("a declared service is failed")

    def restart_required(self):
        return False

    def stop(self, *_):
        self.old_processes = (self.runtime, self.service)
        for child in self.old_processes:
            child.terminate()
            child.wait(timeout=5)

    def register(self, *_):
        self.runtime = self._child()
        self.service = self._child()

    def start(self, *_):
        pass

    def open(self):
        pass

    def close(self):
        for child in (self.runtime, self.service):
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=5)


@pytest.mark.parametrize("failed_service", [False, True])
def test_repair_restart_decision_preserves_or_replaces_real_processes(tmp_path, failed_service):
    root, data = tmp_path / "program", tmp_path / "workspace"
    version_root = root / "versions" / "v1"
    version_root.mkdir(parents=True)
    version = Version(version_root, Path(sys.executable), version_root / "profile.json", {})
    write_json(version_root / "version.json", version.document())
    (root / "current").write_text("v1\n", encoding="utf-8")
    backend = ProcessBackend(root, data, failed_service=failed_service)
    old_pids = (backend.runtime.pid, backend.service.pid)
    try:
        Installer(root, data, backend).run("repair", {})
        if failed_service:
            assert backend.verify_count == 2
            assert backend.runtime.pid != old_pids[0]
            assert backend.service.pid != old_pids[1]
            assert all(child.poll() is not None for child in backend.old_processes)
        else:
            assert backend.verify_count == 1
            assert (backend.runtime.pid, backend.service.pid) == old_pids
            assert backend.runtime.poll() is None
            assert backend.service.poll() is None
    finally:
        backend.close()
