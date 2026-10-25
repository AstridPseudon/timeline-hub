"""Exercise the generated Pinokio foreground launcher in an isolated venv."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import venv
from pathlib import Path

import pytest

from astrid.installer.core import Version, switch, write_json
from astrid.installer.launcher import install as install_launcher


@pytest.mark.posix_native
@pytest.mark.parametrize("shutdown_signal", [signal.SIGTERM, signal.SIGINT])
def test_pinokio_run_executes_foreground_runtime_and_drains_its_child(
    tmp_path, monkeypatch, shutdown_signal,
):
    import runtime_protocol

    app_root = tmp_path / "Astrid"
    version_root = app_root / "versions" / "fixture"
    environment = version_root / "py"
    venv.EnvBuilder(with_pip=False).create(environment)
    python = environment / "bin" / "python"
    site_packages = next((environment / "lib").glob("python*/site-packages"))

    # `-I` still processes venv .pth files. These two paths expose this checkout's
    # launcher code and the Runtime protocol package to the isolated interpreter.
    checkout = Path(__file__).resolve().parents[1]
    protocol_root = Path(runtime_protocol.__file__).resolve().parent.parent
    (site_packages / "astrid-pinokio-test.pth").write_text(
        f"{checkout}\n{protocol_root}\n", encoding="utf-8"
    )

    data_root = tmp_path / "workspace"
    profile = version_root / "profile.json"
    profile.write_text("{}\n", encoding="utf-8")
    version = Version(version_root, python, profile, {
        "ASTRID_TEST_VERSION": "from-version",
        "ASTRID_INSTALL_MANAGED_BY": "wrong-manager",
        "PATH": os.defpath,
    })
    write_json(version_root / "version.json", version.document())
    write_json(app_root / "install.json", {
        "owner": "haus.astrid.runtime", "managed_by": "pinokio",
        "data_root": str(data_root),
    })
    write_json(app_root / "service-env.json", {
        "ASTRID_WARM_IDLE_SECONDS": "73",
        "ASTRID_ALLOW_UNQUALIFIED_GPU": "true",
    })
    switch(app_root, version)
    install_launcher(app_root)

    capture = tmp_path / "runtime-capture.json"
    stopped = tmp_path / "runtime-stopped.json"
    fake_runtime = site_packages / "astrid_runtime"
    fake_runtime.mkdir()
    (fake_runtime / "__init__.py").write_text("", encoding="utf-8")
    (fake_runtime / "cli.py").write_text(
        "import json, os, signal, subprocess, sys\n"
        "from pathlib import Path\n"
        "def main(argv):\n"
        "    capture = Path(os.environ['ASTRID_TEST_CAPTURE'])\n"
        "    stopped = Path(os.environ['ASTRID_TEST_STOPPED'])\n"
        "    child = subprocess.Popen([sys.executable, '-I', '-c', 'import signal; signal.pause()'])\n"
        "    record = {'argv': list(argv), 'pid': os.getpid(), 'child_pid': child.pid, "
        "'env': {key: os.environ.get(key) for key in ('ASTRID_INSTALL_MANAGED_BY', "
        "'ASTRID_TEST_BASE', 'ASTRID_TEST_VERSION', 'ASTRID_WARM_IDLE_SECONDS', "
        "'ASTRID_ALLOW_UNQUALIFIED_GPU', 'PYTHONPATH', 'PYTHONHOME', "
        "'ASTRID_WORKSPACE_ENDPOINT', 'ASTRID_WORKSPACE_CREDENTIAL', "
        "'ASTRID_RUNTIME_SOURCE_MANIFEST', 'ASTRID_RUNTIME_DATA_ROOT', 'ASTRID_PACKS_PATH')}}\n"
        "    capture.write_text(json.dumps(record), encoding='utf-8')\n"
        "    def stop(signum, frame):\n"
        "        child.terminate()\n"
        "        child.wait()\n"
        "        stopped.write_text(json.dumps({'signal': signum, 'child_pid': child.pid}), encoding='utf-8')\n"
        "        raise SystemExit(0)\n"
        "    signal.signal(signal.SIGTERM, stop)\n"
        "    signal.signal(signal.SIGINT, stop)\n"
        "    fd = int(os.environ['ASTRID_TEST_READY_FD'])\n"
        "    os.write(fd, (json.dumps(record) + '\\n').encode())\n"
        "    os.close(fd)\n"
        "    signal.pause()\n"
        "    return 0\n",
        encoding="utf-8",
    )

    read_fd, write_fd = os.pipe()
    caller_env = os.environ.copy()
    caller_env.update({
        "ASTRID_TEST_CAPTURE": str(capture),
        "ASTRID_TEST_STOPPED": str(stopped),
        "ASTRID_TEST_READY_FD": str(write_fd),
        "ASTRID_TEST_BASE": "from-pinokio",
        "PYTHONPATH": str(tmp_path / "must-be-scrubbed"),
        "PYTHONHOME": str(tmp_path / "must-be-scrubbed-home"),
        "ASTRID_WORKSPACE_ENDPOINT": "must-be-scrubbed",
        "ASTRID_WORKSPACE_CREDENTIAL": "must-be-scrubbed",
        "ASTRID_RUNTIME_SOURCE_MANIFEST": "must-be-scrubbed",
        "ASTRID_RUNTIME_DATA_ROOT": "must-be-scrubbed",
        "ASTRID_PACKS_PATH": "must-be-scrubbed",
    })
    process = None
    child_pid = None
    try:
        process = subprocess.Popen(
            [str(app_root / "run"), "--hosted-origin", "off"],
            cwd=tmp_path,
            env=caller_env,
            pass_fds=(write_fd,),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        os.close(write_fd)
        write_fd = -1

        ready = bytearray()
        while b"\n" not in ready:
            chunk = os.read(read_fd, 1)
            if not chunk:
                stderr = process.stderr.read().decode("utf-8", errors="replace")
                process.wait()
                raise AssertionError(f"The foreground Runtime exited before readiness: {stderr}")
            ready.extend(chunk)
        observed = json.loads(ready)
        child_pid = observed["child_pid"]
        record = json.loads(capture.read_text(encoding="utf-8"))

        assert process.pid == observed["pid"] == record["pid"]
        assert record["argv"] == [
            "run", "--profile", "astrid", "--data-root", str(data_root),
            "--source-manifest", str(profile), "--hosted-origin", "off",
        ]
        assert record["env"] == {
            "ASTRID_INSTALL_MANAGED_BY": "pinokio",
            "ASTRID_TEST_BASE": "from-pinokio",
            "ASTRID_TEST_VERSION": "from-version",
            "ASTRID_WARM_IDLE_SECONDS": "73",
            "ASTRID_ALLOW_UNQUALIFIED_GPU": "true",
            "PYTHONPATH": None,
            "PYTHONHOME": None,
            "ASTRID_WORKSPACE_ENDPOINT": None,
            "ASTRID_WORKSPACE_CREDENTIAL": None,
            "ASTRID_RUNTIME_SOURCE_MANIFEST": None,
            "ASTRID_RUNTIME_DATA_ROOT": None,
            "ASTRID_PACKS_PATH": None,
        }
        os.kill(child_pid, 0)

        process.send_signal(shutdown_signal)
        process.wait()
        assert process.returncode == 0
        termination = json.loads(stopped.read_text(encoding="utf-8"))
        assert termination == {"signal": int(shutdown_signal), "child_pid": child_pid}
        with pytest.raises(ProcessLookupError):
            os.kill(child_pid, 0)
    finally:
        os.close(read_fd)
        if write_fd >= 0:
            os.close(write_fd)
        if process is not None and process.poll() is None:
            process.send_signal(signal.SIGTERM)
            process.wait()
        if process is not None and process.stderr is not None:
            process.stderr.close()
        if child_pid is None and capture.exists():
            child_pid = json.loads(capture.read_text(encoding="utf-8"))["child_pid"]
        if child_pid is not None:
            try:
                os.kill(child_pid, 0)
            except ProcessLookupError:
                pass
            else:
                os.kill(child_pid, signal.SIGKILL)
