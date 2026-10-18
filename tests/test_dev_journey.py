from __future__ import annotations

from contextlib import nullcontext
from types import SimpleNamespace

from astrid.core.dev.journey import run_render


class _Timelines:
    def __init__(self, heads, *, version=7):
        self.heads = iter(heads)
        self.version = version
        self.shown = []

    def resolve_scope(self, project, timeline):
        return SimpleNamespace(ok=True, data={
            "project_ref": project,
            "timeline_ref": timeline,
            "timeline_id": "timeline-id",
            "version": self.version,
        })

    def show(self, project, timeline):
        self.shown.append((project, timeline))
        return SimpleNamespace(ok=True, data={"summary": {
            "authority": "canonical_head",
            "is_current_head": True,
            "head_revision_id": next(self.heads),
        }})


class _Client:
    def __init__(self, timelines, render_result):
        self.timelines = timelines
        self.render_result = render_result
        self.invocations = []

    def invoke_result(self, capability_id, **kwargs):
        self.invocations.append((capability_id, kwargs))
        return self.render_result


def test_render_journey_pins_observed_version_and_reports_head_and_output():
    timelines = _Timelines(["rev-1", "rev-1"])
    render_result = SimpleNamespace(
        ok=True,
        raw_result={"state": "completed"},
        kernel_run_id="run-1",
        run_id=None,
        kernel_task_id="task-1",
        kernel_attempt_id="attempt-1",
        outputs={"video": "managed://output"},
    )
    client = _Client(timelines, render_result)
    result = run_render(
        project="demo",
        timeline="main",
        range_value="0..3.5",
        client_opener=lambda: nullcontext(client),
    )

    assert result["ok"] is True
    assert result["head_before"] == result["head_after"] == "rev-1"
    assert result["head_unchanged"] is True
    assert result["run_id"] == "run-1"
    assert result["task_id"] == "task-1"
    assert result["attempt_id"] == "attempt-1"
    capability, call = client.invocations[0]
    assert capability == "rendering.render"
    assert call["kind"] == "executor"
    assert call["project"] == "demo"
    assert call["inputs"] == {
        "timeline_ref": "main",
        "expected_version": 7,
        "range": "0..3.5",
    }
    assert call["wait"] is True
    assert len(timelines.shown) == 2


def test_render_journey_reports_concurrent_head_change_without_claiming_stability():
    timelines = _Timelines(["rev-1", "rev-2"])
    client = _Client(timelines, SimpleNamespace(ok=True, raw_result={}, outputs={}))

    result = run_render(project="demo", timeline="main", client_opener=lambda: nullcontext(client))

    assert result["ok"] is True
    assert result["head_unchanged"] is False
    assert result["head_before"] == "rev-1"
    assert result["head_after"] == "rev-2"


def test_render_journey_refuses_before_render_when_head_is_unavailable():
    class MissingHeadTimelines(_Timelines):
        def show(self, project, timeline):
            return SimpleNamespace(ok=True, data={"summary": {"is_current_head": False}})

    client = _Client(MissingHeadTimelines([]), SimpleNamespace(ok=True))
    result = run_render(project="demo", timeline="main", client_opener=lambda: nullcontext(client))

    assert result["ok"] is False
    assert result["state"] == "refused"
    assert client.invocations == []


def test_journey_help_is_available_without_opening_runtime(capsys):
    from astrid.core.gateway import main as gateway_main

    assert gateway_main(["dev", "journey", "--help"]) == 0
    output = capsys.readouterr().out
    assert "already-running Runtime" in output

    assert gateway_main(["dev", "journey", "render", "--help"]) == 0
    output = capsys.readouterr().out
    assert "--range START..END" in output
