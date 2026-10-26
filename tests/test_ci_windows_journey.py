"""Guard against a journey going green on admission, stale readiness or PID reuse."""

import json
from pathlib import PureWindowsPath
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


def test_native_failure_keeps_log_and_fails_journey(tmp_path, monkeypatch):
    monkeypatch.setattr(journey, "EVIDENCE", tmp_path)
    with pytest.raises(RuntimeError, match="exit 7"):
        journey.run([sys.executable, "-c", "import sys; print('native error', file=sys.stderr); sys.exit(7)"],
                    "bootstrap.log")
    assert "native error" in (tmp_path / "bootstrap.log").read_text(encoding="utf-8")
