"""Abort requires live identity or positive child-wait proof before cleanup."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from astrid.sdk import host_bootstrap


@pytest.mark.parametrize("identity_raises", [False, True])
@pytest.mark.parametrize("wait_result", [0, None, True, "unproven", "timeout"])
def test_abort_requires_positive_wait_after_failed_identity(
    tmp_path, monkeypatch, identity_raises, wait_result,
):
    events = []
    identity_error = host_bootstrap.PackHostBootstrapError("native identity unavailable")

    def identity(state):
        events.append("identity")
        if identity_raises:
            raise identity_error
        return False

    def wait(*, timeout):
        assert timeout == 0
        events.append("wait")
        if wait_result == "timeout":
            raise subprocess.TimeoutExpired("parked-host", timeout)
        return wait_result

    def forbidden_termination(process):
        pytest.fail("failed identity observation must not authorize termination")

    ready_path = tmp_path / "ready.json"
    state = {"pid": 4242, "process_birth_id": "birth", "ready_file": str(ready_path)}
    ready_path.write_text(json.dumps(state))
    handle = host_bootstrap._ParkedPackHostHandle(
        SimpleNamespace(pid=4242, wait=wait),
        SimpleNamespace(close=lambda: events.append("close")),
        None, state, "operation", "channel",
    )
    preparer = host_bootstrap._ParkedPackHostPreparer(lambda reference: None)
    preparer._handle = handle
    monkeypatch.setattr(host_bootstrap, "_parked_host_identity_matches", identity)
    monkeypatch.setattr(host_bootstrap, "terminate_group", forbidden_termination)

    if type(wait_result) is int:
        preparer.abort(handle)
        assert events == ["identity", "wait", "close"]
        assert handle.aborted and handle.cleanup_error is None
        assert not ready_path.exists()
    else:
        with pytest.raises(host_bootstrap.PackHostBootstrapError, match="cannot be verified safely") as caught:
            preparer.abort(handle)
        assert events == ["identity", "wait"]
        assert not handle.aborted and handle.cleanup_error is caught.value
        assert json.loads(ready_path.read_text()) == state
        if identity_raises:
            assert caught.value.__cause__ is identity_error
