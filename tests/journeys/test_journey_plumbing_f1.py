"""Plumbing for the journey's F1 items: env scrubbing, backend, disk preflight, revisions, the App's
render request, the killed-task read-back and outcome kinds.  No Runtime, Remotion or launcher is started."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core import timeline
from astrid.core.dev import journey, reference_realm
from astrid.core.dev.journey import JourneyFailure, Runner

CAPABILITY = {"capability_id": "rendering.render", "definition_digest": "sha256:" + "ab" * 32, "status": "ready",
              "estimated_scratch_bytes": 123, "estimated_output_bytes": 456}


# -- 1. env scrubbing ------------------------------------------------------------------------
POLLUTED = {
    "NODE_OPTIONS": "--require x", "NODE_PATH": "/n", "LD_PRELOAD": "/x.so", "LD_LIBRARY_PATH": "/l",
    "DYLD_INSERT_LIBRARIES": "/x", "DYLD_LIBRARY_PATH": "/d", "GIT_DIR": "/g", "GIT_CONFIG_GLOBAL": "/c",
    "GIT_WORK_TREE": "/w", "ASTRID_NODE_EXECUTABLE": "/node", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": "/p",
    "OTTO_HEAVY_LEASE": "lease", "ASTRID_REMOTION_VALIDATION_PATH": "/v", "ASTRID_RENDER_CACHE": "/r",
    "PYTHONHOME": "/py", "PYTHONSTARTUP": "/s", "NODE_ICU_DATA": "/i", "OPENSSL_CONF": "/o",
}
KEPT = {"PATH": "/usr/bin", "HOME": "/home/x", "TMPDIR": "/tmp", "GIT_EDITOR": "vi", "GIT_TERMINAL_PROMPT": "0",
        "GIT_AUTHOR_NAME": "n", "ASTRID_PACKS_PATH": "/packs", "BANODOCO_LOCAL_DATA_ROOT": "/data"}


def test_scrub_removes_what_remotion_refuses_and_keeps_the_rest() -> None:
    scrubbed = journey.scrub_child_env({**POLLUTED, **KEPT})
    assert scrubbed == KEPT


@pytest.mark.parametrize("key", sorted(POLLUTED))
def test_each_scrubbed_variable_is_one_remotion_refuses_or_the_journey_replaces(key: str) -> None:
    from astrid.core.rendering.remotion_runtime import RemotionValidationError, _registry_context
    env = {"HOME": "/home/x", "PATH": "/usr/bin", key: POLLUTED[key]}
    if not key.startswith(("ASTRID_", "OTTO_")):
        with pytest.raises(RemotionValidationError):  # the validation that fails closed on it ...
            _registry_context(env, generator=True)
    assert key not in journey.scrub_child_env(env)
    _registry_context(journey.scrub_child_env(env), generator=True)  # ... passes once scrubbed


def test_scrubbed_env_with_interactive_git_set_still_passes_validation() -> None:
    from astrid.core.rendering.remotion_runtime import _registry_context
    assert _registry_context(journey.scrub_child_env({**POLLUTED, **KEPT}), generator=True) is not None


def test_every_runner_child_gets_the_scrubbed_env(tmp_path: Path) -> None:
    runner = Runner(tmp_path, tmp_path / "s.json")
    code = "import json, os; print(json.dumps(sorted(k for k in os.environ if k in %r)))" % sorted(POLLUTED)
    seen = runner.command("adopt", [sys.executable, "-c", code], {**POLLUTED, "PATH": os.environ.get("PATH", "")})
    assert seen == []


# -- 2. backend ----------------------------------------------------------------------------------
ASTRID = ["py", "-m", "astrid"]


def test_render_argv_defaults_to_remotion_with_review_and_wait() -> None:
    argv = journey.render_argv(ASTRID, "main", "film", "out.mp4", backend=journey.REMOTION_BACKEND,
                               window=(1.0, 9.0), review=True, timeout=60)
    assert argv == ASTRID + ["timelines", "render", "main", "--project", "film", "--range", "1.0", "9.0",
                             "--backend", "rendering.remotion", "--output-name", "out.mp4", "--review",
                             "--wait", "--timeout-seconds", "60", "--json"]


def test_ffmpeg_backend_never_asks_for_review_and_detach_has_no_timeout() -> None:
    argv = journey.render_argv(ASTRID, "main", "film", "out.mp4", backend="rendering.ffmpeg", window=(0, 6),
                               review=True, detach=True, timeout=60)
    assert "--review" not in argv and "--timeout-seconds" not in argv and "--wait" not in argv
    assert argv[argv.index("--backend") + 1] == "rendering.ffmpeg" and "--detach" in argv and argv[-1] == "--json"
    assert "--range" in argv and "--range" not in journey.render_argv(ASTRID, "m", "p", "o.mp4", backend="rendering.ffmpeg")


class RecordingRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []
        self.details: dict = {}

    def command(self, phase, argv, env, **kwargs):
        self.calls.append(argv)
        return {"data": {"kernel_task_id": "t1"}}


@pytest.mark.parametrize(("backend", "review"), [("rendering.remotion", True), ("rendering.ffmpeg", False)])
def test_journey_render_calls_use_the_backend_and_kill_render_drops_review_for_ffmpeg(tmp_path: Path, backend: str, review: bool) -> None:
    runner = RecordingRunner()
    j = journey.Journey(runner=runner, root=tmp_path, env={}, project="p", timeline="main", start=2.0, end=6.0,
                        kill_start=0.0, checkout=tmp_path, backend=backend)
    j.render("kill_render", "killed", j.kill_start, j.end, detach=True, review=True)
    argv = runner.calls[0]
    assert argv[argv.index("--backend") + 1] == backend and ("--review" in argv) is review


def test_node_pin_preflight_runs_only_for_remotion(tmp_path: Path, monkeypatch) -> None:
    from astrid.core.rendering import node_pin
    monkeypatch.setattr(node_pin, "resolve_pinned_node", lambda *a, **k: node_pin.NodeResolution(
        None, None, "v20.19.4", "nowhere", "no Node v20.19.4 for the renderer"))
    monkeypatch.setattr(journey, "disk_preflight", lambda *a: {})

    class Reached(Exception):
        pass

    def stop(**kwargs):
        raise Reached
    monkeypatch.setattr(journey.tempfile, "mkdtemp", stop)
    reference = tmp_path / "ref"
    reference.mkdir()
    with pytest.raises(JourneyFailure, match="no Node v20.19.4"):
        journey.run(reference, "film/main", tmp_path / "s.json", backend="rendering.remotion")
    with pytest.raises(Reached):  # past every preflight: ffmpeg needs no renderer Node
        journey.run(reference, "film/main", tmp_path / "s.json", backend="rendering.ffmpeg")
    with pytest.raises(JourneyFailure, match="backend must be one of"):
        journey.run(reference, "film/main", tmp_path / "s.json", backend="rendering.other")


# -- 3. disk preflight ----------------------------------------------------------------------------
GIB = 1024**3


def test_runtime_disk_floor_is_read_like_the_runtime_reads_it() -> None:
    assert journey.runtime_disk_floor({}) == 4 * GIB
    assert journey.runtime_disk_floor({journey.DISK_FLOOR_ENV: "0"}) == 0
    assert journey.runtime_disk_floor({journey.DISK_FLOOR_ENV: str(GIB)}) == GIB
    for bad in ("many", "-1", ""):
        with pytest.raises(JourneyFailure, match=journey.DISK_FLOOR_ENV):
            journey.runtime_disk_floor({journey.DISK_FLOOR_ENV: bad})


def test_the_default_floor_matches_the_runtime() -> None:
    store = pytest.importorskip("runtime_protocol.store")
    assert store.LEASE_SECONDS == journey.LEASE_SECONDS
    source = Path(store.__file__).read_text()
    assert f'"{journey.DISK_FLOOR_ENV}", str(4 * 1024**3)' in source


def test_expected_scratch_scales_with_the_window_and_backend() -> None:
    assert journey.expected_render_scratch("rendering.remotion", 32) == 10 * GIB
    assert journey.expected_render_scratch("rendering.remotion", 0) == 0
    assert 0 < journey.expected_render_scratch("rendering.ffmpeg", 8) < journey.expected_render_scratch("rendering.remotion", 8)


def test_disk_preflight_reports_its_numbers_and_refuses_below_floor_plus_scratch(tmp_path: Path) -> None:
    report = journey.disk_preflight(10 * GIB, 4 * GIB, 3 * GIB, tmp_path)
    assert report == {"path": str(tmp_path), "free_bytes": 10 * GIB, "runtime_floor_bytes": 4 * GIB,
                      "expected_render_scratch_bytes": 3 * GIB, "required_bytes": 7 * GIB}
    assert journey.disk_preflight(7 * GIB, 4 * GIB, 3 * GIB, tmp_path)["required_bytes"] == 7 * GIB
    with pytest.raises(JourneyFailure, match=r"preflight: free disk 6.99 GiB .*floor 4.00 GiB \+ expected render scratch 3.00 GiB = 7.00 GiB"):
        journey.disk_preflight(7 * GIB - 1024**2 * 10, 4 * GIB, 3 * GIB, tmp_path)


def test_run_refuses_to_start_on_a_full_disk_before_creating_anything(tmp_path: Path, monkeypatch) -> None:
    reference = tmp_path / "ref"
    reference.mkdir()
    monkeypatch.setattr(journey.shutil, "disk_usage", lambda path: SimpleNamespace(total=1, used=1, free=GIB))
    monkeypatch.setattr(journey.tempfile, "mkdtemp", lambda **k: pytest.fail("work started before the disk preflight"))
    with pytest.raises(JourneyFailure, match="Runtime floor"):
        journey.run(reference, "film/main", tmp_path / "s.json", backend="rendering.ffmpeg")


# -- 4. revisions -----------------------------------------------------------------------------------
def _git(path: Path, *args: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True, env=env)


def test_git_revision_reports_head_and_dirtiness(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    (tmp_path / "a").write_text("1")
    _git(tmp_path, "add", "a")
    _git(tmp_path, "commit", "-qm", "one")
    head = subprocess.run(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    assert journey.git_revision(tmp_path) == {"path": str(tmp_path), "head": head, "dirty": False}
    (tmp_path / "a").write_text("2")
    assert journey.git_revision(tmp_path)["dirty"] is True


def test_git_revision_of_a_non_checkout_is_an_error_entry_not_an_exception(tmp_path: Path) -> None:
    result = journey.git_revision(tmp_path / "nowhere")
    assert result["head"] is None and result["error"]


def test_manifest_version_is_read_only_when_a_string(tmp_path: Path) -> None:
    (tmp_path / "artifacts.json").write_text(json.dumps({"version": "sha256:abc", "artifacts": {}}))
    assert journey.manifest_version(tmp_path / "artifacts.json") == "sha256:abc"
    (tmp_path / "bad.json").write_text("not json")
    (tmp_path / "num.json").write_text(json.dumps({"version": 3}))
    assert [journey.manifest_version(tmp_path / n) for n in ("bad.json", "num.json", "missing.json")] == [None, None, None]


def test_collect_revisions_gathers_astrid_runtime_app_and_manifest_versions(tmp_path: Path) -> None:
    astrid, runtime, app = tmp_path / "astrid", tmp_path / "runtime", tmp_path / "app"
    for repo in (astrid, runtime, app):
        repo.mkdir()
        _git(repo, "init", "-q")
        (repo / "f").write_text(repo.name)
        _git(repo, "add", "f")
        _git(repo, "commit", "-qm", "c")
    (astrid / "artifacts.json").write_text(json.dumps({"version": "sha256:astrid"}))
    (runtime / "contract").mkdir()
    (runtime / "contract" / "artifacts.json").write_text(json.dumps({"version": "sha256:runtime"}))
    revisions = journey.collect_revisions(astrid, runtime, app)
    assert revisions["astrid"]["manifest_version"] == "sha256:astrid" and revisions["runtime"]["manifest_version"] == "sha256:runtime"
    assert all(revisions[k]["head"] and len(revisions[k]["head"]) == 40 for k in ("astrid", "runtime", "app"))
    assert journey.collect_revisions(astrid, runtime, None)["app"] is None


def test_summary_records_the_revisions_in_json_and_text(tmp_path: Path) -> None:
    runner = Runner(tmp_path, tmp_path / "s.json")
    runner.details["revisions"] = {"astrid": {"head": "a" * 40, "dirty": True, "manifest_version": "sha256:m"}, "app": None}
    runner.write_summary()
    assert json.loads((tmp_path / "s.json").read_text())["revisions"]["astrid"]["head"] == "a" * 40
    text = (tmp_path / "s.txt").read_text()
    assert f"astrid: {'a' * 40} (dirty) manifest sha256:m" in text and "app:" not in text


# -- 6. the App's render request and the killed-task read-back ------------------------------------
def test_app_render_admission_has_the_apps_exact_shape() -> None:
    admission = journey.build_app_render_admission(project="film", timeline_id="main", output_name="out.mp4",
                                                   capability=CAPABILITY, token="tok")
    assert admission == {
        "method": "POST", "path": "/v1/tasks",
        "headers": {"Content-Type": "application/json", "Authorization": "Bearer tok",
                    "Idempotency-Key": "reigh.render:v1:main:head:download:out.mp4"},
        "body": {"project": "film", "capability_id": "rendering.render", "capability_digest": "sha256:" + "ab" * 32,
                 "schema_version": "1", "input_object_ids": [],
                 "spec": {"family": "rendering.render",
                          "params": {"timeline_ref": "main", "selector": "rendering.remotion", "output_name": "out.mp4"},
                          "output_policy": {"format": "mp4", "destination": "download", "filename": "out.mp4"}},
                 "storage_estimate": {"scratch_bytes": 123, "output_bytes": 456}, "settlement_effect": {}},
    }


def test_app_render_admission_with_a_version_and_the_ffmpeg_selector() -> None:
    admission = journey.build_app_render_admission(project="p", timeline_id="t", output_name="o.mp4", capability=CAPABILITY,
                                                   token="x", backend="rendering.ffmpeg", expected_version=7)
    assert admission["headers"]["Idempotency-Key"] == "reigh.render:v1:t:7:download:o.mp4"
    assert admission["body"]["spec"]["params"] == {"timeline_ref": "t", "expected_version": 7,
                                                   "selector": "rendering.ffmpeg", "output_name": "o.mp4"}


class FakeRuntime:
    """A loopback HTTP server standing in for the Runtime: records requests, answers from ``routes``."""

    def __init__(self, routes: dict) -> None:
        self.routes, self.requests = routes, []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def _answer(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length)) if length else None
                outer.requests.append({"method": self.command, "path": self.path, "headers": dict(self.headers), "body": body})
                status, payload = outer.routes[(self.command, self.path.split("?")[0])](self.path, body)
                raw = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            do_GET = do_POST = _answer

            def log_message(self, *args) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.endpoint = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def runtime_server():
    servers: list[FakeRuntime] = []

    def make(routes: dict) -> FakeRuntime:
        servers.append(FakeRuntime(routes))
        return servers[-1]
    yield make
    for server in servers:
        server.close()


def test_the_admission_travels_unchanged_over_http(runtime_server) -> None:
    server = runtime_server({("POST", "/v1/tasks"): lambda path, body: (201, {"data": {"task_id": "t1"}, "receipt": {}})})
    admission = journey.build_app_render_admission(project="film", timeline_id="main", output_name="o.mp4", capability=CAPABILITY, token="tok")
    answer = journey.runtime_request(server.endpoint, admission["method"], admission["path"], headers=admission["headers"], body=admission["body"])
    sent = server.requests[0]
    assert answer["data"]["task_id"] == "t1" and sent["body"] == admission["body"] and sent["method"] == "POST"
    assert {k: sent["headers"][k] for k in ("Content-Type", "Idempotency-Key", "Authorization")} == admission["headers"]


def test_runtime_request_adds_the_bearer_token_and_reports_refusals(runtime_server) -> None:
    server = runtime_server({("GET", "/v1/ok"): lambda p, b: (200, {"fine": True}),
                             ("GET", "/v1/no"): lambda p, b: (409, {"error": "stale"})})
    assert journey.runtime_request(server.endpoint, "GET", "/v1/ok", token="abc") == {"fine": True}
    assert server.requests[0]["headers"]["Authorization"] == "Bearer abc"
    with pytest.raises(JourneyFailure, match="HTTP 409.*stale"):
        journey.runtime_request(server.endpoint, "GET", "/v1/no")


def test_runtime_access_comes_from_discovery_and_the_astrid_credential(tmp_path: Path) -> None:
    (tmp_path / "runtime").mkdir()
    (tmp_path / "credentials").mkdir()
    (tmp_path / "runtime" / "discovery.json").write_text(json.dumps({"endpoint": "http://127.0.0.1:9/"}))
    (tmp_path / "credentials" / "astrid.json").write_text(json.dumps({"token": "t0k"}))
    assert journey.read_runtime_access(tmp_path) == ("http://127.0.0.1:9", "t0k")
    with pytest.raises(JourneyFailure, match="no running Runtime"):
        journey.read_runtime_access(tmp_path / "other")


def test_task_events_follow_the_cursor(runtime_server) -> None:
    pages = {None: {"items": [{"sequence": 1}], "next_cursor": "c1"}, "c1": {"items": [{"sequence": 2}], "next_cursor": None}}
    server = runtime_server({("GET", "/v1/tasks/t1/events"):
                             lambda path, body: (200, pages["c1" if "cursor=c1" in path else None])})
    assert journey.task_events(server.endpoint, "tok", "t1") == [{"sequence": 1}, {"sequence": 2}]


def _event(sequence: int, kind: str, task: str = "t1") -> dict:
    return {"sequence": sequence, "event_type": kind, "aggregate_id": task}


KILLED = [_event(1, "task.admitted"), _event(2, "task.claimed"), _event(3, "task.lease_expired"), _event(4, "task.claimed")]


def test_a_killed_task_that_lapsed_and_was_cancelled_passes() -> None:
    verdict = journey.evaluate_killed_task_events([*KILLED, _event(5, "task.cancel_requested"), _event(6, "task.cancelled")],
                                                  task_id="t1", final_state="cancelled")
    assert verdict["end_event"] == "task.cancelled" and verdict["lease_expired"] == 1


def test_a_killed_task_that_was_re_run_to_completion_passes() -> None:
    verdict = journey.evaluate_killed_task_events([*KILLED, _event(5, "task.completed")], task_id="t1", final_state="succeeded")
    assert verdict["end_event"] == "task.completed"


def test_events_are_judged_in_sequence_order_and_only_for_the_task() -> None:
    shuffled = [_event(6, "task.cancelled"), _event(1, "task.admitted"), _event(3, "task.lease_expired"),
                _event(4, "task.completed", task="other"), _event(5, "task.failed", task="other")]
    assert journey.evaluate_killed_task_events(shuffled, task_id="t1")["end_event"] == "task.cancelled"


@pytest.mark.parametrize(("events", "message"), [
    ([_event(1, "task.claimed"), _event(2, "task.cancelled")], "no task.lease_expired"),
    (KILLED, "exactly one end state, saw 0"),
    ([*KILLED, _event(5, "task.completed"), _event(6, "task.completed")], "exactly one end state, saw 2"),
    ([*KILLED, _event(5, "task.failed"), _event(6, "task.cancelled")], "exactly one end state, saw 2"),
    ([_event(1, "task.completed"), _event(2, "task.lease_expired")], "ended before its lease expired"),
    ([], "no task.lease_expired"),
])
def test_a_killed_task_without_a_lapse_or_one_end_state_fails(events, message) -> None:
    with pytest.raises(JourneyFailure, match=message):
        journey.evaluate_killed_task_events(events, task_id="t1")


def test_the_reported_state_must_agree_with_the_end_event() -> None:
    with pytest.raises(JourneyFailure, match="contradicts"):
        journey.evaluate_killed_task_events([*KILLED, _event(5, "task.cancelled")], task_id="t1", final_state="succeeded")


def test_lease_snapshot_and_capability_lookup() -> None:
    task = {"state": "running", "attempt_id": "a1", "lease_fence": 2, "lease_expires_at": "t", "lease_token": "secret"}
    assert journey.lease_snapshot(task) == {"state": "running", "attempt_id": "a1", "lease_fence": 2, "lease_expires_at": "t"}
    assert journey.find_ready_capability([CAPABILITY], "rendering.render") is CAPABILITY
    assert journey.find_ready_capability([{**CAPABILITY, "status": "unavailable"}], "rendering.render") is None
    assert journey.find_ready_capability([CAPABILITY], "other") is None


def _restart_journey(tmp_path: Path, server: FakeRuntime, *, app_render: bool = True) -> tuple[journey.Journey, RecordingRunner]:
    (tmp_path / "data" / "runtime").mkdir(parents=True)
    (tmp_path / "data" / "credentials").mkdir()
    (tmp_path / "data" / "runtime" / "discovery.json").write_text(json.dumps({"endpoint": server.endpoint}))
    (tmp_path / "data" / "credentials" / "astrid.json").write_text(json.dumps({"token": "tok"}))
    runner = RecordingRunner()
    j = journey.Journey(runner=runner, root=tmp_path, env={}, project="film", timeline="main", start=2, end=6, kill_start=0,
                        checkout=tmp_path, restart_argv=["restart"], app_render=app_render)
    return j, runner


def _recorded(case: str) -> dict:
    """The Runtime's recorded response body (tests/fixtures/runtime-responses, vendored under a lock)."""
    return json.loads((Path(__file__).resolve().parents[1] / "fixtures" / "runtime-responses" / f"{case}.json").read_text())["body"]


def _runtime_routes(state: str) -> dict:
    def admitted(path, body):
        recorded = _recorded("task_admission_201")
        recorded["data"]["task_id"] = "t9"
        return 201, recorded

    def task(path, body):
        recorded = {**_recorded("task_read_200"), "task_id": "t9", "state": state}
        if state != "queued":  # the Runtime reports a result only once the task has one
            recorded["result"] = {"why": "x"}
        return 200, recorded

    return {("GET", "/v1/capabilities"): lambda p, b: (200, {"items": [CAPABILITY], "next_cursor": None}),
            ("POST", "/v1/tasks"): admitted, ("GET", "/v1/tasks/t9"): task}


def test_runtime_restart_restarts_then_admits_the_apps_request_and_waits(tmp_path: Path, runtime_server) -> None:
    server = runtime_server(_runtime_routes("succeeded"))
    j, runner = _restart_journey(tmp_path, server)
    j.runtime_restart()
    assert runner.calls == [["restart"]]
    post = next(r for r in server.requests if r["method"] == "POST")
    assert post["path"] == "/v1/tasks" and post["body"]["spec"]["params"]["selector"] == "rendering.remotion"
    assert post["headers"]["Idempotency-Key"].startswith("reigh.render:v1:main:head:download:v6-app-")
    assert runner.details["runtime_restart"]["app_render_state"] == "succeeded"


def test_runtime_restart_fails_when_the_app_render_does_not_complete(tmp_path: Path, runtime_server) -> None:
    j, _ = _restart_journey(tmp_path, runtime_server(_runtime_routes("failed")))
    with pytest.raises(JourneyFailure, match="ended failed"):
        j.runtime_restart()


def test_runtime_restart_can_skip_the_app_render(tmp_path: Path, runtime_server) -> None:
    server = runtime_server({})
    j, runner = _restart_journey(tmp_path, server, app_render=False)
    j.runtime_restart()
    assert server.requests == [] and runner.details["runtime_restart"]["app_render"] == "skipped"


# -- 7. outcome kinds --------------------------------------------------------------------------------
def _outcome(tmp_path: Path, argv: list[str]) -> tuple[str, dict]:
    runner = Runner(tmp_path, tmp_path / "summary.json")
    kind, error = "success", None
    try:
        runner.phase("adopt", lambda: runner.command("adopt", argv, {}, json_result=False))
    except JourneyFailure as exc:
        kind, error = exc.kind, str(exc)
    runner.write_summary(error=error, outcome=None if kind == "success" else kind)
    return kind, json.loads((tmp_path / "summary.json").read_text())


def test_a_command_that_exits_zero_is_a_success(tmp_path: Path) -> None:
    kind, summary = _outcome(tmp_path, ["true"])
    assert (kind, summary["ok"], summary["outcome"], summary["error"]) == ("success", True, "success", None)
    assert "PASS (success)" in (tmp_path / "summary.txt").read_text()


def test_a_command_that_exits_nonzero_is_a_failure_not_a_hang(tmp_path: Path) -> None:
    kind, summary = _outcome(tmp_path, ["false"])
    assert (kind, summary["ok"], summary["outcome"]) == ("failure", False, "failure")
    assert "adopt: exit 1" in summary["error"] and "hung" not in summary["error"]
    assert "FAIL (failure)" in (tmp_path / "summary.txt").read_text()


def test_a_command_that_never_exits_is_hung_at_the_ceiling(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setitem(journey.HANG_SECONDS, "adopt", 0.5)
    kind, summary = _outcome(tmp_path, ["sleep", "30"])
    assert (kind, summary["ok"], summary["outcome"]) == ("hung", False, "hung")
    assert "hung (no exit after 0.5s)" in summary["error"]
    assert "FAIL (hung)" in (tmp_path / "summary.txt").read_text()
    assert summary["phase_seconds"]["adopt"] < 10  # stopped at the ceiling, not after the 30 s sleep


# -- 5 (cli). options ----------------------------------------------------------------------------------
def _captured_main(monkeypatch, tmp_path: Path, argv: list[str]) -> dict:
    seen: dict = {}

    def fake_run(reference, timeline, summary, **kwargs):
        seen.update(reference=reference, timeline=timeline, **kwargs)
        summary.write_text(json.dumps({"ok": True}))
        return 0
    monkeypatch.setattr(journey, "run", fake_run)
    assert journey.main([*argv, "--summary", str(tmp_path / "s.json")]) == 0
    return seen


def test_generated_reference_needs_no_timeline_and_gets_the_short_excerpt(monkeypatch, tmp_path: Path) -> None:
    seen = _captured_main(monkeypatch, tmp_path, ["--tier", "smoke", "--reference", "generated"])
    assert seen["reference"] is None and seen["timeline"] == "journey/main"
    assert (seen["start"], seen["end"]) == journey.GENERATED_RANGE and seen["backend"] == "rendering.remotion"
    assert seen["app_checkout"] is None and seen["app_render"] is True


def test_cli_passes_backend_app_checkout_and_range_through(monkeypatch, tmp_path: Path) -> None:
    seen = _captured_main(monkeypatch, tmp_path, ["--tier", "smoke", "--reference", str(tmp_path), "--timeline", "a/b",
                                                  "--backend", "rendering.ffmpeg", "--app-checkout", str(tmp_path / "app"),
                                                  "--range", "1", "3", "--skip-app-render"])
    assert seen["reference"] == tmp_path and seen["backend"] == "rendering.ffmpeg" and seen["app_render"] is False
    assert seen["app_checkout"] == tmp_path / "app" and (seen["start"], seen["end"]) == (1.0, 3.0)


def test_cli_refuses_an_unknown_backend_and_a_missing_timeline(tmp_path: Path) -> None:
    base = ["--tier", "smoke", "--summary", str(tmp_path / "s.json")]
    with pytest.raises(SystemExit):
        journey.main([*base, "--reference", "generated", "--backend", "rendering.other"])
    with pytest.raises(SystemExit):
        journey.main([*base, "--reference", str(tmp_path)])


# -- 5. the generated reference -------------------------------------------------------------------------
def test_generator_pure_parts() -> None:
    argv = reference_realm.ffmpeg_clip_argv(Path("c.mp4"), 1)
    assert argv[0] == "ffmpeg" and "sine=frequency=440:duration=4" in argv and argv[-1] == "c.mp4"
    assert any(a.startswith("testsrc2=size=640x360") for a in argv)
    media = [{"object_id": f"sha256:{n}", "digest": f"sha256:{n}"} for n in "abc"]
    publication = reference_realm.media_only_publication("proj", media)
    clips = publication["parent_composition"]["clips"]
    assert [c["at"] for c in clips] == [0, 4, 8] and {c["clipType"] for c in clips} == {"media"}
    assert [c["asset"] for c in clips] == sorted(publication["parent_composition"]["registry"]["assets"])
    assert publication["expected_head"] is None and len(publication["dependency_manifest"]["media"]) == 3
    # The render validates the same canonical timeline schema, so an invalid reference fails here, not on a Mac run.
    timeline.validate_timeline({**publication["parent_composition"]["config"], "clips": clips})
    assert reference_realm.source_manifest(Path("/a"), Path("/r"), "/env") == {
        "profile": "astrid", "source_checkout": "/a", "runtime_checkout": "/r", "runtime_environment": "/env"}


# integration: builds a realm with the Runtime package (a second checkout) in subprocesses.
@pytest.mark.integration
def test_generated_reference_is_a_valid_stopped_reference(tmp_path: Path) -> None:
    pytest.importorskip("runtime_protocol.service")
    pytest.importorskip("banodoco_local")
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode:
        pytest.skip("ffmpeg is not installed")
    checkout = Path(journey.__file__).resolve().parents[3]
    reference = reference_realm.build_reference(
        tmp_path, env=journey.scrub_child_env(os.environ), source_checkout=checkout,
        runtime_checkout=journey.runtime_checkout_path(), runtime_environment=sys.prefix).resolve()
    realm_id, realm = journey.select_reference_realm(reference)
    assert realm_id == reference_realm.REALM_ID and (realm / "realm.sqlite3").is_file()
    assert not list(realm.glob("realm.sqlite3-*")), "a stopped reference leaves no WAL behind"
    assert json.loads((reference / "runtime" / "source-profiles" / "astrid.json").read_text())["profile"] == "astrid"
    described = reference_realm.describe_reference(reference)
    [project] = described["projects"]
    assert project["slug"] == "journey" and project["objects"] == 3
    assert project["timelines"] == [{"timeline_id": "main", "head": "parent-1"}]
