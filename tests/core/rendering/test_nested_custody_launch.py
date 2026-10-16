"""Real confined rendering support launch; no backend or custody replacement."""

import json
import os
import sys
import sysconfig
import threading
import time
from dataclasses import replace
from pathlib import Path

import pytest

from astrid.core.execution import generic_host as host
from astrid.core.execution import process_group as groups
from astrid.core.execution.custody_broker import DARWIN_UNIX_SOCKET_PATH_MAX_BYTES
from astrid.core.execution.render_command_pipe import HostRenderCommandBridge
from tests.core.execution.test_confinement_launch_integration import (
    launch as confinement_launch,
)

launch = confinement_launch


def _nested_support_case(launch_state, tmp_path, *, cancelled=None):
    policy, _, _, _ = launch_state
    source = Path(__file__).resolve().parents[3]
    backend = source / "astrid/packs/rendering/rendering/renderers/remotion"
    imports = [str(source), sysconfig.get_path("purelib"), sysconfig.get_path("platlib")]
    policy = replace(
        policy,
        bootstrap_roots=tuple(
            dict.fromkeys(
                (
                    *policy.bootstrap_roots,
                    source,
                    *(Path(p) for p in imports[1:]),
                )
            )
        ),
    )
    program = r"""
import json,os,sys,traceback
from pathlib import Path
sys.path[:0]=json.loads(sys.argv[1])
from astrid.core.execution.render_command_pipe import install_render_command_client
install_render_command_client()
from astrid.core.rendering.transport import CommandTransport
from astrid.core.execution.custody_broker import default_process_identity
root=Path.cwd()
request=json.loads((Path(sys.argv[3])/'tests/core/rendering/fixtures/v1/request.json').read_text())
(root/'request.json').write_text(json.dumps(request))
try:
    os.lstat('/private/tmp')
except OSError:
    pass
else:
    raise AssertionError('worker can read private socket parent')
print(json.dumps({'worker':default_process_identity(os.getpid()),'private_tmp_readable':False}),flush=True)
try:
    result=CommandTransport('rendering.remotion').run(
        'support',[sys.executable,'run.py'],request_path=root/'request.json',
        result_path=root/'result.json',cwd=sys.argv[2],timeout=5)
except BaseException as error:
    traceback.print_exc()
    raise
print(json.dumps(result.to_dict()),flush=True)
"""
    plan = host._confined_launch_plan(
        [
            str(Path(sys.executable).resolve()),
            "-I",
            "-S",
            "-B",
            "-c",
            program,
            json.dumps(imports),
            str(backend),
            str(source),
        ],
        policy=policy,
    )
    assert plan.pass_fds == ()
    process = groups.popen_owned_group(list(plan.argv), **plan.subprocess_options(), text=True)
    bridge = HostRenderCommandBridge(
        process,
        policy=policy,
        backend_root=source / "astrid/packs/rendering",
        admission={
            "capability_id": "rendering.render",
            "capability_digest": "focused-source-admission",
        },
        launch_digest="focused-confined-launch",
        imports=imports,
    )
    try:
        broker = process._astrid_custody._launch_broker
        actual_path = str(broker.socket_path)
        assert len(os.fsencode(actual_path)) <= DARWIN_UNIX_SOCKET_PATH_MAX_BYTES
        print(
            json.dumps(
                {
                    "outer_pid": process.pid,
                    "outer_birth": process._astrid_process_birth,
                    "outer_registration": broker.registration,
                    "actual_socket_path": actual_path,
                    "actual_socket_path_bytes": len(os.fsencode(actual_path)),
                }
            )
        )
        deadline = time.monotonic() + 15
        while process.poll() is None:
            bridge.check()
            if cancelled is not None and cancelled.is_set():
                groups.terminate_tree(process)
                break
            assert time.monotonic() < deadline, bytes(bridge.stderr).decode()
            time.sleep(0.02)
        was_cancelled = cancelled is not None and cancelled.is_set()
        stdout, stderr = bridge.finish(cancelled=process.returncode != 0)
        groups.verify_tree_absent(process)
        print(stdout, stderr)
        print(
            json.dumps(
                {
                    "terminal_exit": process.returncode,
                    "outer_wait_outcome": process._custody_wait_outcome,
                    "socket_removed": not broker.socket_path.exists(),
                    "outer_settlement": broker.role_authority._read()["state"],
                }
            )
        )
        if not was_cancelled:
            assert process.returncode == 0, stderr
        else:
            assert process.returncode != 0
        assert len(bridge.children) == 1
        child = next(iter(bridge.children))
        child_broker = child._astrid_custody._launch_broker
        identity = child_broker.registration["identity"]
        assert identity["pid"] == child.pid
        assert identity["parent_pid"] == os.getpid()
        assert identity["birth_id"] == child._astrid_process_birth
        assert type(child.returncode) is int
        if not was_cancelled:
            assert child.returncode == 0
        assert not child_broker.socket_path.exists()
        assert len(os.fsencode(child_broker.socket_path)) <= DARWIN_UNIX_SOCKET_PATH_MAX_BYTES
        assert child_broker.role_authority._read()["state"] == "settled"
        print(
            json.dumps(
                {
                    "nested_registration": child_broker.registration,
                    "nested_socket_path": str(child_broker.socket_path),
                    "nested_socket_bytes": len(os.fsencode(child_broker.socket_path)),
                    "nested_exit": child.returncode,
                    "nested_socket_removed": True,
                }
            )
        )
    finally:
        if process.poll() is None:
            groups.terminate_tree(process)
        process.wait(timeout=5)
        bridge.finish(cancelled=True)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None:
                stream.close()


def test_nested_remotion_support_has_host_retained_custody(launch, tmp_path):
    _nested_support_case(launch, tmp_path)


def test_nested_support_cancel_cleans_real_host_retained_helper(launch, tmp_path, monkeypatch):
    started = threading.Event()
    exchange = HostRenderCommandBridge._exchange_backend

    def observed_exchange(self, process, timeout):
        # Observe only the actual retained helper at the production exchange
        # edge. No child/command replacement and no renderer proof is claimed.
        assert process in self.children
        started.set()
        assert self.cancelled.wait(10)
        return exchange(self, process, timeout)

    monkeypatch.setattr(HostRenderCommandBridge, "_exchange_backend", observed_exchange)
    _nested_support_case(launch, tmp_path, cancelled=started)


def test_nested_helper_bootstrap_failure_retains_and_cleans_original_child(
    launch, tmp_path, monkeypatch
):
    from astrid.core.execution import remotion_pipe

    original_write = remotion_pipe._write
    original_launch = HostRenderCommandBridge._launch_locked
    owners = []

    def write(fd, raw, **kwargs):
        if not raw.startswith(remotion_pipe.PREFIX):
            frame = json.loads(raw)
            if frame.get("binding", {}).get("role") == "backend":
                raise OSError("injected helper bootstrap write failure")
        return original_write(fd, raw, **kwargs)

    def retained_launch(self, *args, **kwargs):
        owners.append(self)
        return original_launch(self, *args, **kwargs)

    monkeypatch.setattr(remotion_pipe, "_write", write)
    monkeypatch.setattr(HostRenderCommandBridge, "_launch_locked", retained_launch)
    with pytest.raises(AssertionError, match="injected helper bootstrap write failure"):
        _nested_support_case(launch, tmp_path)
    assert len(owners) == 1
    (child,) = owners[0].children
    assert type(child.returncode) is int
    groups.verify_tree_absent(child)
    broker = child._astrid_custody._launch_broker
    assert not broker.socket_path.exists()
    assert broker.role_authority._read()["state"] == "settled"
