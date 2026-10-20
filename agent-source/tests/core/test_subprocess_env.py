from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from astrid.core.execution.executor import runner as executor_runner
from astrid.core.rendering import transport as rendering_transport
from astrid.core.rendering.contracts import SCHEMA_VERSION, SupportReport
from astrid.core.rendering.transport import CommandTransport
from astrid.core.subprocess_env import build_child_subprocess_env


def test_render_process_group_marker_survives_executor_and_transport(
    tmp_path: Path, monkeypatch
) -> None:
    marker = "ASTRID_RENDER_INHERIT_PROCESS_GROUP"
    monkeypatch.setenv(marker, "1")
    monkeypatch.setattr(executor_runner, "_external_pack_pythonpath_env", lambda *_: {})
    monkeypatch.setattr(executor_runner, "_project_subprocess_env", lambda *_: {})
    monkeypatch.setattr(executor_runner, "_emit_scoped_config_env", lambda *_: {})
    monkeypatch.setattr(executor_runner, "dependency_pythonpath", lambda: ())
    executor = SimpleNamespace(
        isolation=SimpleNamespace(env_passthrough=(), secrets_required=()),
        metadata={},
        scoped_configs=(),
    )
    request = SimpleNamespace(project="render-project")

    executor_environment = executor_runner._command_subprocess_env(
        executor, request, {}
    )
    assert executor_environment[marker] == "1"

    launched = {}

    def fake_popen(argv, **kwargs):
        launched.update(kwargs)
        result_path = Path(argv[argv.index("--result") + 1])
        result_path.write_text(
            json.dumps(
                SupportReport(
                    schema_version=SCHEMA_VERSION,
                    supported=True,
                    reasons=[],
                    features={},
                    alternatives=[],
                    backend="rendering.remotion",
                ).to_dict()
            ),
            encoding="utf-8",
        )
        return SimpleNamespace(
            pid=12345,
            returncode=0,
            communicate=lambda **_: ("", ""),
        )

    monkeypatch.setattr(rendering_transport, "_resolve_executable", lambda name, **_: name)
    monkeypatch.setattr(rendering_transport, "popen_owned_process", fake_popen)
    monkeypatch.setattr(rendering_transport, "observe_tree", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(
        rendering_transport, "_terminate_leftover_group", lambda *_args, **_kwargs: None
    )

    report = CommandTransport("rendering.remotion").run(
        "support",
        ["python3"],
        request_path=tmp_path / "request.json",
        result_path=tmp_path / "result.json",
        cwd=tmp_path,
        env=executor_environment,
    )

    assert report.supported is True
    assert launched["start_new_session"] is False
    assert launched["env"][marker] == "1"


def test_remotion_browser_executable_is_parent_owned_and_unlisted_env_is_dropped() -> None:
    selector = "ASTRID_REMOTION_BROWSER_EXECUTABLE"
    child = build_child_subprocess_env(
        base={selector: "/base/browser", "ASTRID_UNLISTED_BASE": "base"},
        parent={selector: "/parent/browser", "ASTRID_UNLISTED_PARENT": "parent"},
        explicit_env={selector: "/explicit/browser"},
    )

    assert child[selector] == "/parent/browser"
    assert "ASTRID_UNLISTED_BASE" not in child
    assert "ASTRID_UNLISTED_PARENT" not in child
