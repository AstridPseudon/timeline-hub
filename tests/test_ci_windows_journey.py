"""Guard against a journey going green on admission, stale readiness or PID reuse."""

import json
from pathlib import PureWindowsPath
import subprocess
import sys

import pytest

from scripts import ci_windows_journey as journey


def test_manifest_replaces_released_sources_and_keeps_app_tools(tmp_path, monkeypatch):
    app = tmp_path / "app"
    (app / "public").mkdir(parents=True)
    (app / "public" / "install-manifest.json").write_text(json.dumps({
        "schema_version": 1, "agent": {"sha": "released-agent"},
        "runtime": {"sha": "released-runtime", "schema_digest": "released-schema"},
        "tools": {"python": {"version": "3.11.13"}},
    }), encoding="utf-8")
    monkeypatch.setattr(journey, "source", lambda repo: {"sha": repo.name, "repo": str(repo)})
    manifest = journey.install_manifest(tmp_path / "agent", tmp_path / "runtime", app)
    assert manifest["agent"] == {"sha": "agent", "repo": str(tmp_path / "agent")}
    assert manifest["runtime"] == {"sha": "runtime", "repo": str(tmp_path / "runtime")}
    assert manifest["tools"] == {"python": {"version": "3.11.13"}}


def process(pid, ppid, created, exe="", command=""):
    return {"pid": pid, "ppid": ppid, "created": created, "exe": exe, "command": command}


def test_processes_include_generic_descendants_and_surviving_orphans():
    root = PureWindowsPath(r"C:\Users\runner\AppData\Local\Astrid")
    host = process(10, 1, "2026-10-26T10:00:00Z", exe=str(root / "py" / "python.exe").upper())
    child = process(11, 10, "2026-10-26T10:00:01Z", exe=r"C:\uv\python.exe")
    grandchild = process(12, 11, "2026-10-26T10:00:02Z", exe=r"C:\cache\chrome.exe")
    # Child-first ordering, plus a reused parent PID that belongs to an older child.
    unrelated = process(13, 10, "2026-10-26T09:00:00Z", exe=r"C:\other.exe")
    selected = journey.astrid_processes([grandchild, unrelated, child, host], [root])
    assert {row["pid"] for row in selected} == {10, 11, 12}
    assert journey.astrid_processes([grandchild], [root], {journey.process_key(grandchild)}) == [grandchild]
    reused = {**grandchild, "created": "2026-10-26T11:00:00Z"}
    assert journey.astrid_processes([reused], [root], {journey.process_key(grandchild)}) == []


@pytest.mark.parametrize("command", [
    r"C:\Temp\astrid-install-123\venv\Scripts\python.exe -m astrid install",
    r"C:\uv\python.exe -I -m astrid install",
])
def test_partial_install_and_unmarked_job_child_are_not_missed(command):
    installer = process(20, 1, "10:00", command=command)
    child = process(21, 20, "10:01", exe=r"C:\cache\python.exe")
    assert journey.astrid_processes([child, installer], []) == [child, installer]


@pytest.mark.parametrize("state,instance,expected", [
    ("starting", "current", False), ("running", "stale", False), ("running", "current", True),
])
def test_ready_file_must_belong_to_running_service(tmp_path, monkeypatch, state, instance, expected):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(journey, "data_root", lambda: tmp_path)
    (tmp_path / "runtime").mkdir()
    (tmp_path / "runtime" / "generic-host.ready.json").write_text(json.dumps({
        "status": "ready", "runtime_instance_id": instance,
    }), encoding="utf-8")
    monkeypatch.setattr(journey, "health", lambda: {
        "status": "ok", "runtime_instance_id": "current", "services": [{"name": "pack-host", "state": state}],
    })
    assert journey.host_ready() is expected


@pytest.mark.parametrize("state,outputs,expected", [
    ("queued", [], False), ("failed", [], False), ("succeeded", [], False),
    ("succeeded", [{"name": "sfx", "digest": "sha256:" + "a" * 64, "size": 9644}], False),
    ("succeeded", [{"name": name, "digest": "sha256:" + "a" * 64, "size": 100}
                   for name in ("sfx", "sfx_meta")], True),
])
def test_admission_is_not_task_settlement(monkeypatch, state, outputs, expected):
    def cli(module, argv, name, **kwargs):
        if argv[:2] == ["tasks", "show"]:
            return json.dumps({"ok": True, "data": {"state": state, "result": {"outputs": outputs}}})
        return json.dumps({"ok": True, "data": {"task_id": "task-1"}})

    monkeypatch.setattr(journey, "cli", cli)
    if expected:
        journey.task()
    else:
        with pytest.raises(RuntimeError, match="did not settle"):
            journey.task()


def test_failed_follow_cancels_and_settles_before_returning_failure(monkeypatch):
    calls = []
    state = "running"
    follow_count = 0

    def cli(module, argv, name, **kwargs):
        nonlocal state, follow_count
        calls.append(tuple(argv[:2]))
        if argv[:2] == ["projects", "create"]:
            return json.dumps({"ok": True})
        if argv[:2] == ["tasks", "create"]:
            return json.dumps({"ok": True, "data": {"task_id": "task-1"}})
        if argv[:2] == ["tasks", "follow"]:
            follow_count += 1
            if follow_count == 1:
                raise RuntimeError("task-follow.jsonl: exit 1")
            state = "cancelled"
            return ""
        if argv[:2] == ["tasks", "show"]:
            return json.dumps({"ok": True, "data": {"state": state, "result": {"outputs": []}}})
        if argv[:2] == ["tasks", "cancel"]:
            state = "cancel_requested"
            return json.dumps({"ok": True})
        if argv[:2] == ["tasks", "events"]:
            return json.dumps({"ok": True, "data": []})
        raise AssertionError(argv)

    monkeypatch.setattr(journey, "cli", cli)
    with pytest.raises(RuntimeError, match="reached terminal state 'cancelled'"):
        journey.task()

    assert ("tasks", "cancel") in calls
    assert follow_count == 2
    assert calls[-2:] == [("tasks", "show"), ("tasks", "events")]


def test_native_failure_keeps_log_and_fails_journey(tmp_path, monkeypatch):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path)
    with pytest.raises(RuntimeError, match="exit 7"):
        journey.run([sys.executable, "-c", "import sys; print('native error', file=sys.stderr); sys.exit(7)"],
                    "bootstrap.log")
    assert "native error" in (tmp_path / "bootstrap.log").read_text(encoding="utf-8")


@pytest.mark.parametrize("shell", ["powershell.exe", r"C:\Program Files\PowerShell\7\pwsh.exe"])
def test_powershell_child_rebuilds_module_path_without_mutating_environment(tmp_path, monkeypatch, shell):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path)
    monkeypatch.setenv("PSModulePath", r"C:\pwsh\Modules;C:\pwsh\7\Modules")
    monkeypatch.setenv("KEEP_ME", "inherited")
    original = dict(journey.os.environ)
    captured = {}

    def fake_run(argv, **kwargs):
        captured.update(kwargs)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(journey.subprocess, "run", fake_run)
    journey.run([shell, "-NoProfile"], "powershell.log", show=False)

    assert "PSModulePath" not in captured["env"]
    assert captured["env"]["KEEP_ME"] == "inherited"
    assert dict(journey.os.environ) == original


def test_powershell_explicit_environment_is_copied_and_preserved(tmp_path, monkeypatch):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path)
    inherited = {"PSModulePath": "pwsh-path", "KEEP_ME": "explicit"}
    captured = {}

    def fake_run(argv, **kwargs):
        captured.update(kwargs)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(journey.subprocess, "run", fake_run)
    journey.run(["pwsh.exe", "-NoProfile"], "pwsh.log", env=inherited, show=False)

    assert captured["env"] == {"KEEP_ME": "explicit"}
    assert inherited == {"PSModulePath": "pwsh-path", "KEEP_ME": "explicit"}


def test_non_powershell_child_keeps_explicit_environment(tmp_path, monkeypatch):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path)
    inherited = {"PSModulePath": "caller-value", "KEEP_ME": "explicit"}
    captured = {}

    def fake_run(argv, **kwargs):
        captured.update(kwargs)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(journey.subprocess, "run", fake_run)
    journey.run([sys.executable, "-c", "pass"], "python.log", env=inherited, show=False)

    assert captured["env"] is inherited
    assert inherited == {"PSModulePath": "caller-value", "KEEP_ME": "explicit"}
