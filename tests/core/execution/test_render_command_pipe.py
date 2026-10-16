"""Refusal boundaries of the finite render relay; no renderer substitutes."""

import sys
from pathlib import Path

import pytest

from astrid.core.execution import render_command_pipe as relay


@pytest.mark.parametrize(
    "mutation", ["command", "backend", "verb", "cwd", "source", "role", "fields"]
)
def test_backend_refuses_drift_before_process_launch(tmp_path, mutation):
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role = "executor"
    owner.backend_root = tmp_path
    owner.source_digest = "pinned"
    owner._source_digest = lambda: "pinned"
    owner.binding = {"admission": {}}
    request = dict(
        verb="support",
        command=[sys.executable, "run.py"],
        backend="rendering.remotion",
        request_path=str(tmp_path / "request.json"),
        result_path=str(tmp_path / "result.json"),
        cwd=str(tmp_path),
        timeout=5,
        required_binaries=[],
    )
    if mutation == "command":
        request["command"] = [sys.executable, "-c", "raise AssertionError()"]
    elif mutation == "backend":
        request["backend"] = "rendering.ffmpeg"
    elif mutation == "verb":
        request["verb"] = "finalize"
    elif mutation == "cwd":
        request["cwd"] = str(tmp_path.parent)
    elif mutation == "source":
        owner.source_digest = "different"
    elif mutation == "role":
        owner.role = "backend"
    elif mutation == "fields":
        request["env"] = {"PATH": "/untrusted"}
    with pytest.raises(ValueError, match="admitted Remotion backend"):
        owner._backend(request)


def test_executor_cannot_request_cli_or_supply_an_executable():
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role = "executor"
    with pytest.raises(ValueError, match="admitted backend pipe"):
        owner._cli(
            {
                "argv": [sys.executable, "-c", "raise AssertionError()"],
                "cwd": "/",
                "render_environment": {},
            }
        )


@pytest.mark.parametrize("escape", ["outside", "symlink", "traversal"])
def test_protocol_artifact_must_stay_inside_retained_private_root(tmp_path, escape):
    from types import SimpleNamespace

    private = tmp_path / "private"
    private.mkdir()
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.policy = SimpleNamespace(private_write_root=private)
    if escape == "outside":
        path = tmp_path / "result.json"
    elif escape == "symlink":
        path = private / "alias"
        path.symlink_to(tmp_path)
    else:
        path = private / ".." / "result.json"
    with pytest.raises(ValueError, match="retained scratch"):
        owner._artifact(str(path), exists=False)


def test_cli_refuses_absent_host_closure_before_any_spawn(tmp_path):
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role, owner.closure = "backend", None
    with pytest.raises(ValueError, match="host admitted installed closure"):
        owner._cli(
            {
                "argv": [
                    str(Path(sys.executable)),
                    str(tmp_path / "cli"),
                    "render",
                    "TimelineComposition",
                    "--props",
                    "/props",
                    "--output",
                    "/output",
                    "--concurrency=1",
                ],
                "cwd": str(tmp_path),
                "render_environment": {},
            }
        )
