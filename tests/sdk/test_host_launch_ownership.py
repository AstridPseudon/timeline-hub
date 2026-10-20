from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

import pytest

from astrid.core.execution import process_group
from astrid.sdk import host_bootstrap
from tests.sdk.test_host_recovery import Harness


@pytest.fixture
def startup(tmp_path, monkeypatch):
    # Reuse only the preflight doubles; launch and cleanup retain real custody.
    h = Harness(tmp_path, monkeypatch)
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "source")
    processes = []
    write = host_bootstrap._write_object
    state = h.support / "generic-host.json"
    ready = h.support / "generic-host.ready.json"

    def launch(argv, **kwargs):
        process = process_group.popen_owned_group(
            [sys.executable, "-c", "import time; time.sleep(300)", *argv[1:]],
            **kwargs,
        )
        processes.append(process)
        return process

    def register(path, payload):
        write(path, payload)
        if path == state:
            write(ready, {**payload, "status": "ready", "ready_capabilities": []})

    def forbidden(*_args, **_kwargs):
        pytest.fail("returned-child cleanup must not adopt a registration")

    monkeypatch.setattr(host_bootstrap, "popen_owned_group", launch)
    monkeypatch.setattr(host_bootstrap, "_write_object", register)
    monkeypatch.setattr(host_bootstrap, "_retire_host_locked", forbidden)
    monkeypatch.setattr(host_bootstrap, "_terminate_old_host", forbidden)
    monkeypatch.setattr(host_bootstrap, "_stop_group", forbidden)
    previous = signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        yield h, processes, state, ready, register
    finally:
        signal.signal(signal.SIGINT, previous)
        for process in processes:
            try:
                process_group.terminate_group(process)
            finally:
                shutil.rmtree(process._astrid_custody.root, ignore_errors=True)


def _assert_reaped(process):
    assert process.returncode is not None  # before fixture cleanup can intervene
    with pytest.raises(ChildProcessError):
        os.waitpid(process.pid, os.WNOHANG)
    with pytest.raises(ProcessLookupError):
        os.killpg(process.pid, 0)


@pytest.mark.parametrize("stage,interrupt", [
    (stage, interrupt)
    for stage in ("returned", "birth", "state-before", "state-partial", "state-after", "ready-read")
    for interrupt in (False, True)
] + [("birth-empty", False), ("ready-invalid", False)])
def test_startup_failure_reaps_returned_owned_child(startup, monkeypatch, stage, interrupt):
    h, processes, state, ready, register = startup

    def fail():
        if interrupt:
            signal.raise_signal(signal.SIGINT)
        raise RuntimeError("injected startup failure")

    if stage == "returned":
        open_path = Path.open

        class Log:
            def __init__(self, stream):
                self.stream = stream

            def fileno(self):
                return self.stream.fileno()

            def close(self):
                self.stream.close()
                assert len(processes) == 1
                fail()

        def open_log(path, *args, **kwargs):
            stream = open_path(path, *args, **kwargs)
            return Log(stream) if path.name == "generic-host.log" and args == ("ab",) else stream

        monkeypatch.setattr(Path, "open", open_log)
    elif stage in {"birth", "birth-empty"}:
        def birth(_pid):
            if stage == "birth":
                fail()
            return ""

        monkeypatch.setattr(host_bootstrap, "_host_birth_identity", birth)
    elif stage.startswith("state-"):
        def write(path, payload):
            if stage == "state-partial":
                path.write_text('{"pid":', encoding="utf-8")
            elif stage == "state-after":
                register(path, payload)
            fail()

        monkeypatch.setattr(host_bootstrap, "_write_object", write)
    else:
        read = host_bootstrap._read_object

        def read_ready(path):
            result = read(path)
            if path == ready and result is not None:
                monkeypatch.setattr(host_bootstrap, "_read_object", read)
                if stage == "ready-read":
                    fail()
                return {**result, "source_closure_digest": "different-source"}
            return result

        monkeypatch.setattr(host_bootstrap, "_read_object", read_ready)

    error = (host_bootstrap.PackHostBootstrapError if stage in {"birth-empty", "ready-invalid"}
             else KeyboardInterrupt if interrupt else RuntimeError)
    with pytest.raises(error):
        h.ensure()

    assert len(processes) == 1
    _assert_reaped(processes[0])
    assert not ready.exists()
    if stage == "state-partial":
        # An incomplete record cannot establish an identity for marker deletion.
        assert state.read_text(encoding="utf-8") == '{"pid":'
    else:
        assert not state.exists()


@pytest.mark.parametrize("marker", ["state", "ready", "both"])
@pytest.mark.parametrize("replacement", ["foreign", "birth", "source", "command"])
def test_failed_registration_preserves_replacement_and_foreign_process(
    startup, monkeypatch, marker, replacement,
):
    h, processes, state, ready, register = startup
    foreign = process_group.popen_owned_group(
        [sys.executable, "-c", "import time; time.sleep(300)"],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    # Fixture teardown may clean this process only after the preservation check.
    processes.append(foreign)
    preserved = {}

    def write(path, payload):
        register(path, payload)
        targets = (state, ready) if marker == "both" else (state if marker == "state" else ready,)
        for target in targets:
            record = dict(host_bootstrap._read_object(target))
            if replacement == "foreign":
                record.update(pid=foreign.pid, process_birth_id=foreign._astrid_process_birth)
            elif replacement == "birth":
                record["process_birth_id"] = "replacement-birth"
            elif replacement == "source":
                record["source_closure_digest"] = "replacement-source"
            else:
                record["python_executable"] = "/other/python"
            target.write_text(json.dumps(record), encoding="utf-8")
            preserved[target] = target.read_bytes()
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(host_bootstrap, "_write_object", write)
    with pytest.raises(KeyboardInterrupt):
        h.ensure()

    assert len(processes) == 2
    _assert_reaped(processes[1])
    assert foreign.poll() is None
    for target, contents in preserved.items():
        assert target.read_bytes() == contents
    for target in {state, ready} - preserved.keys():
        assert not target.exists()


def test_successful_startup_keeps_returned_child_running(startup):
    h, processes, state, ready, _register = startup
    result = h.ensure()
    assert result["host_status"] == "ready"
    assert result["host_pid"] == processes[0].pid
    assert processes[0].poll() is None
    assert state.exists() and ready.exists()
