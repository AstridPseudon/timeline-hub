from __future__ import annotations

import http.client
import io
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from typing import Any

import pytest

pytest_plugins = ("test_timeline_commit_port",)

from test_timeline_commit_port import request as commit_request

from runtime_protocol.server import RuntimeHandler, RuntimeHTTPServer
from tests.helpers.p2_commit_phase_capture import PHASES, P2CommitPhaseCapture


class _Credentials:
    def require(self, token, scope):
        assert token == "phase-token"
        assert scope == "projects:write"
        return {"actor": "phase-editor", "scopes": ["projects:write"]}


def _handler(runtime, body, *, key="phase-key"):
    raw = json.dumps(body, separators=(",", ":")).encode()
    handler: Any = object.__new__(RuntimeHandler)
    handler.server = SimpleNamespace(runtime=runtime, credentials=_Credentials())
    handler.command = "POST"
    handler.path = f"/v1/projects/{body['project_id']}/timelines/{body['timeline_id']}/commit"
    handler.headers = {
        "Content-Length": str(len(raw)),
        "Authorization": "Bearer phase-token",
        "Idempotency-Key": key,
    }
    handler.rfile = io.BytesIO(raw)
    handler.wfile = io.BytesIO()
    handler.send_response = lambda status: setattr(handler, "sent_status", status)
    handler.send_header = lambda *_args: None
    handler.end_headers = lambda: None
    handler._defer_response = False
    return handler


def _summary(capture):
    return [event for event in capture.events if event["phase"] == "summary"]


class _FakeTimer:
    def __init__(self, delay, callback):
        self.delay = delay
        self.callback = callback
        self.daemon = False
        self.started = False
        self.cancelled = False

    def start(self):
        self.started = True

    def cancel(self):
        self.cancelled = True

    def fire(self):
        self.callback()


def test_capture_is_disabled_by_default_and_explicitly_bounded(tmp_path):
    capture = P2CommitPhaseCapture(tmp_path / "disabled.jsonl")
    with capture:
        capture._begin(1, "handler_entry")
    assert capture.events == []
    assert not (tmp_path / "disabled.jsonl").exists()

    bounded = P2CommitPhaseCapture(enabled=True, max_requests=2, max_events=4, max_bytes=1024)
    bounded.start()
    first = bounded._new_request()
    second = bounded._new_request()
    third = bounded._new_request()
    assert first is not None
    assert first == 1 and second == 2 and third is None
    bounded._begin(first, "handler_entry")
    bounded._end(first, "handler_entry")
    bounded.stop()
    assert len(bounded.events) <= 4
    assert bounded.truncated


def test_capture_attach_detach_restores_process_and_thread_traces():
    previous_process = sys.gettrace()
    previous_threads = threading.gettrace()
    capture = P2CommitPhaseCapture(enabled=True)
    capture.start()
    assert sys.gettrace() == capture._trace
    assert threading.gettrace() == capture._trace
    capture.stop()
    assert sys.gettrace() == previous_process
    assert threading.gettrace() == previous_threads


def test_capture_allowlist_redacts_by_not_retaining_transport_values(tmp_path):
    capture = P2CommitPhaseCapture(tmp_path / "phase.jsonl", enabled=True)
    capture.start()
    request = capture._new_request()
    assert request is not None
    capture._begin(request, "handler_entry", status="not-allowlisted")
    capture._end(request, "handler_entry", error=True)
    capture.stop()

    serialized = (tmp_path / "phase.jsonl").read_text()
    assert {event["phase"] for event in capture.events} <= set(PHASES) | {"summary"}
    assert "phase-token" not in serialized
    assert "not-allowlisted" not in serialized
    assert "error" not in serialized or '"error":true' not in serialized
    assert all(set(event) <= {"schema_version", "request", "phase", "state", "at_ms", "count",
                              "status", "last_phase", "phases", "durations_ms",
                              "unknown_boundaries", "truncated", "retention"}
               for event in capture.events)


def test_ring_retains_late_failing_request_after_successful_setup_events():
    capture = P2CommitPhaseCapture(enabled=True, max_events=8, max_bytes=64 * 1024)
    capture.start()
    try:
        setup = capture._new_request()
        assert setup is not None
        for _index in range(90):
            capture._begin(setup, "provider")
        capture._end(setup, "provider")
        capture._requests[setup]["dispatch_finished"] = True

        failing = capture._new_request()
        assert failing is not None
        for _index in range(150):
            capture._begin(failing, "provider")
        capture._end(failing, "provider", error=True)
        capture._requests[failing]["dispatch_finished"] = True
    finally:
        capture.stop()

    final_events = [event for event in capture.events
                    if event.get("request") == failing and event["phase"] != "summary"]
    assert len(final_events) == capture._requests[failing]["events_seen"]
    assert capture.retention["final_request"] == {
        "request": failing,
        "outcome": "failed",
        "events_seen": capture._requests[failing]["events_seen"],
        "events_retained": len(final_events),
        "complete": True,
        "incomplete_limit": None,
    }
    assert capture.retention["rolling"]["capacity_events"] == 8
    assert capture.retention["rolling"]["capacity_dropped_events"] > 128
    assert capture.retention["output"]["bytes"] <= capture.max_bytes


def test_final_request_byte_bound_reports_exact_incomplete_limit():
    capture = P2CommitPhaseCapture(enabled=True, max_events=4, max_bytes=512)
    capture.start()
    try:
        request = capture._new_request()
        assert request is not None
        for _index in range(30):
            capture._begin(request, "provider")
        capture._end(request, "provider", error=True)
        capture._requests[request]["dispatch_finished"] = True
    finally:
        capture.stop()

    final = capture.retention["final_request"]
    assert final["request"] == request
    assert final["outcome"] == "failed"
    assert not final["complete"]
    limit = final["incomplete_limit"]
    assert limit["reason"] == "max_bytes"
    assert limit["limit_bytes"] == capture.max_bytes
    assert limit["required_bytes"] == capture._requests[request]["events_required_bytes"]
    assert limit["dropped_events"] == capture._requests[request]["events_dropped"]
    assert limit["dropped_bytes"] == capture._requests[request]["events_dropped_bytes"]
    assert capture.retention["output"]["bytes"] <= capture.max_bytes


def test_pending_request_is_the_final_correlated_request_and_shutdown_is_deterministic():
    def snapshot():
        capture = P2CommitPhaseCapture(enabled=True, max_events=6, clock_ns=lambda: 0)
        capture.start()
        request = capture._new_request()
        assert request is not None
        capture._begin(request, "handler_entry")
        capture.stop()
        return capture.events, capture.retention

    first_events, first_retention = snapshot()
    second_events, second_retention = snapshot()
    assert first_events == second_events
    assert first_retention["final_request"]["request"] == 1
    assert first_retention["final_request"]["outcome"] == "pending"
    assert first_retention == second_retention


def test_observer_failure_does_not_replace_original_exception():
    marker = RuntimeError("original exception text must stay outside capture")

    class Runtime:
        def commit_timeline(self, *_args, **_kwargs):
            raise marker

    body = {
        "api_version": 1,
        "project_id": "project/opaque",
        "timeline_id": "timeline/opaque",
        "base_revision_id": "revision-1",
        "base_publication_id": "publication-1",
        "commands": [],
    }
    handler = _handler(Runtime(), body)
    capture = P2CommitPhaseCapture(enabled=True)
    capture.start()
    try:
        with pytest.raises(RuntimeError) as caught:
            handler._timeline_commit("project/opaque", "timeline/opaque", "commit")
    finally:
        capture.stop()
    assert caught.value is marker
    assert "original exception text" not in json.dumps(capture.events)


def test_concurrent_requests_keep_local_ordinals_and_phase_state_isolated():
    calls = []

    class Runtime:
        def commit_timeline(self, project, timeline, body, *, authorize, **_kwargs):
            authorize()
            calls.append((project, timeline))
            time.sleep(0.01)
            return {"data": {"status": "accepted"}, "receipt": None}

    bodies = [
        {
            "api_version": 1,
            "project_id": f"project-{index}",
            "timeline_id": f"timeline-{index}",
            "base_revision_id": "revision-1",
            "base_publication_id": "publication-1",
            "commands": [],
        }
        for index in (1, 2)
    ]
    capture = P2CommitPhaseCapture(enabled=True)
    capture.start()
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda body: _handler(Runtime(), body)._timeline_commit(
                body["project_id"], body["timeline_id"], "commit"), bodies))
    finally:
        capture.stop()
    assert len(results) == 2
    summaries = _summary(capture)
    assert {summary["request"] for summary in summaries} == {1, 2}
    assert all(summary["phases"]["handler_entry"]["status"] == "observed" for summary in summaries)
    assert all(summary["phases"]["authorization"]["status"] == "observed" for summary in summaries)
    assert all(summary["last_phase"] == "http_response" for summary in summaries)
    assert sorted(calls) == [("project-1", "timeline-1"), ("project-2", "timeline-2")]


def test_mounted_http_commit_route_and_provider_are_observed(service, tmp_path):
    body = commit_request(service, commands=[{
        "schema_version": 1,
        "op": "clip.move",
        "version": "1",
        "select": "parent/clip:clip-1",
        "args": {"on": 2},
    }])
    server: Any = RuntimeHTTPServer(("127.0.0.1", 0), RuntimeHandler)
    server.runtime = service
    server.credentials = _Credentials()
    capture = P2CommitPhaseCapture(tmp_path / "mounted-phase.jsonl", enabled=True)
    capture.start()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        path = f"/v1/projects/{body['project_id']}/timelines/main/commit"
        connection.request("POST", path, body=json.dumps(body), headers={
            "Authorization": "Bearer phase-token",
            "Content-Type": "application/json",
            "Idempotency-Key": "mounted-phase",
        })
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        capture.stop()

    assert response.status == 200
    assert payload["data"]["status"] == "accepted"
    summaries = _summary(capture)
    assert len(summaries) == 1
    phases = summaries[0]["phases"]
    assert phases["dispatch_queue"]["status"] == "observed"
    assert phases["dispatch_queue"]["end_ms"] is not None
    for phase in ("handler_entry", "authorization", "coordinator_admission", "coordinator_lock",
                  "provider", "accept", "receipt", "http_response"):
        assert phases[phase]["status"] == "observed", (phase, summaries)
    for phase in ("coordinator_admission", "coordinator_lock"):
        assert phases[phase]["count"] == 1
        assert phases[phase]["end_ms"] is not None
    assert summaries[0]["last_phase"] == "http_response"
    durations = summaries[0]["durations_ms"]
    assert durations["dispatch_queue_ms"] is not None
    assert durations["handler_ms"] is not None
    assert durations["dispatch_total_ms"] is not None
    assert durations["provider_wall_ms"] == pytest.approx(
        phases["provider"]["end_ms"] - phases["provider"]["start_ms"], abs=0.001)
    assert durations["execution_lock_wait_ms"] is None
    assert durations["caller_receipt_ms"] is None
    assert summaries[0]["unknown_boundaries"]["client_request_to_server_receive"] == "outside Runtime process"
    serialized = (tmp_path / "mounted-phase.jsonl").read_text()
    assert body["project_id"] not in serialized
    assert "mounted-phase" not in serialized
    assert "phase-token" not in serialized
    assert capture.failures == 0


def test_dispatch_scope_expires_after_deferred_response_before_handler_reuse(service):
    body = commit_request(service, commands=[{
        "schema_version": 1,
        "op": "clip.move",
        "version": "1",
        "select": "parent/clip:clip-1",
        "args": {"on": 2},
    }])
    handler = _handler(service, body, key="dispatch-scope")
    capture = P2CommitPhaseCapture(enabled=True)
    capture.start()
    try:
        handler._dispatch()
        assert handler.wfile.getvalue()
        assert capture._handler_requests == {}
        assert capture._thread_requests == {}

        # Reuse the handler and thread for unrelated traffic after the real
        # deferred response has been flushed.
        handler.command = "GET"
        handler.path = "/v1/health"
        handler.headers = {}
        handler.rfile = io.BytesIO()
        handler.wfile = io.BytesIO()
        handler._dispatch()
    finally:
        capture.stop()

    summaries = _summary(capture)
    assert len(summaries) == 1
    phases = summaries[0]["phases"]
    assert phases["http_response"]["count"] == 2
    assert capture._handler_requests == {}
    assert capture._thread_requests == {}


def test_observer_avoids_line_events_and_unrelated_request_lookups(service):
    counts = {"line": 0, "unrelated_lookup": 0}

    class CountingCapture(P2CommitPhaseCapture):
        def _trace_inner(self, frame, event, arg):
            if event == "line":
                counts["line"] += 1
            return super()._trace_inner(frame, event, arg)

        def _request_for_frame(self, frame):
            if (self._phase(frame) is None
                    and frame.f_code.co_qualname != "CommitExecutionCoordinator.execute"
                    and frame.f_code not in self._frames):
                counts["unrelated_lookup"] += 1
            return super()._request_for_frame(frame)

    body = commit_request(service)
    handler = _handler(service, body)
    capture = CountingCapture(enabled=True)
    with capture:
        handler._dispatch()

    assert handler.sent_status == 200
    assert json.loads(handler.wfile.getvalue())["data"]["status"] == "accepted"
    assert _summary(capture)[0]["phases"]["receipt"]["status"] == "observed"
    assert capture.failures == 0
    assert counts == {"line": 0, "unrelated_lookup": 0}


def test_watchdog_captures_a_genuine_pending_handler_with_all_python_threads(tmp_path):
    entered = threading.Event()
    release = threading.Event()
    timers = []
    dumps = []

    class Runtime:
        def commit_timeline(self, *_args, **_kwargs):
            entered.set()
            assert release.wait(2)
            return {"data": {"status": "accepted"}, "receipt": None}

    def timer_factory(delay, callback):
        timer = _FakeTimer(delay, callback)
        timers.append(timer)
        return timer

    def dump_traceback(*, file, all_threads):
        dumps.append((file, all_threads))
        file.write("Thread watchdog pending\n")

    now = [0]
    capture = P2CommitPhaseCapture(
        tmp_path / "phase.jsonl",
        enabled=True,
        watchdog_seconds=20,
        timer_factory=timer_factory,
        clock_ns=lambda: now[0],
        dump_traceback=dump_traceback,
    )
    handler = _handler(Runtime(), {
        "api_version": 1,
        "project_id": "project-watchdog",
        "timeline_id": "timeline-watchdog",
        "base_revision_id": "revision-1",
        "base_publication_id": "publication-1",
        "commands": [],
    })
    thread = threading.Thread(target=handler._dispatch, name="watchdog-handler")
    capture.start()
    try:
        thread.start()
        assert entered.wait(2)
        assert len(timers) == 1 and timers[0].started and timers[0].daemon
        now[0] = 20_000_000_000
        timers[0].fire()
        release.set()
        thread.join(timeout=2)
    finally:
        release.set()
        thread.join(timeout=2)
        capture.stop()

    assert not thread.is_alive()
    assert dumps and dumps[0][1] is True
    assert capture.watchdog_captures == 1
    assert capture.watchdog_sink is not None
    assert capture.watchdog_sink.stat().st_mode & 0o777 == 0o600
    assert capture.watchdog_sink.read_text() == "Thread watchdog pending\n"
    assert _summary(capture)[0]["phases"]["handler_entry"]["status"] == "observed"


def test_five_second_watchdog_schedules_one_bounded_thirty_second_followup(tmp_path):
    timers = []
    dumps = []

    def timer_factory(delay, callback):
        timer = _FakeTimer(delay, callback)
        timers.append(timer)
        return timer

    def dump_traceback(*, file, all_threads):
        dumps.append(all_threads)
        file.write("bounded pending\n")

    capture = P2CommitPhaseCapture(
        tmp_path / "five-thirty.jsonl", enabled=True, watchdog_seconds=5,
        timer_factory=timer_factory, dump_traceback=dump_traceback,
    )
    capture.start()
    try:
        ordinal = capture._new_request(handler=object(), emit_handler=True)
        assert ordinal == 1
        timers[0].fire()
        assert len(timers) == 2
        assert timers[0].delay == 5
        assert timers[1].delay == 25
        timers[1].fire()
    finally:
        capture.stop()

    assert dumps == [True, True]
    assert capture.watchdog_captures == 2
    assert timers[1].cancelled is False


def test_watchdog_finish_raised_disabled_and_late_callbacks_are_safe(tmp_path):
    timers = []

    class FinishedRuntime:
        def commit_timeline(self, *_args, **_kwargs):
            return {"data": {"status": "accepted"}, "receipt": None}

    def timer_factory(delay, callback):
        timer = _FakeTimer(delay, callback)
        timers.append(timer)
        return timer

    capture = P2CommitPhaseCapture(tmp_path / "finish.jsonl", enabled=True,
                                   timer_factory=timer_factory)
    handler = _handler(FinishedRuntime(), {
        "api_version": 1,
        "project_id": "project-watchdog",
        "timeline_id": "timeline-watchdog",
        "base_revision_id": "revision-1",
        "base_publication_id": "publication-1",
        "commands": [],
    })
    capture.start()
    try:
        handler._dispatch()
        assert timers[0].cancelled
        timers[0].fire()
        assert capture.watchdog_captures == 0
    finally:
        capture.stop()

    raised_timer = []

    class RaisedRuntime:
        def commit_timeline(self, *_args, **_kwargs):
            raise RuntimeError("raised commit")

    raised = P2CommitPhaseCapture(tmp_path / "raised.jsonl", enabled=True,
                                  timer_factory=lambda delay, callback: raised_timer.append(
                                      _FakeTimer(delay, callback)) or raised_timer[-1])
    raised.start()
    try:
        _handler(RaisedRuntime(), {
            "api_version": 1,
            "project_id": "project-watchdog",
            "timeline_id": "timeline-watchdog",
            "base_revision_id": "revision-1",
            "base_publication_id": "publication-1",
            "commands": [],
        })._dispatch()
    finally:
        raised.stop()
    assert raised_timer[0].cancelled
    assert raised.watchdog_captures == 0

    aborted_timer = []

    class AbortedRuntime:
        def commit_timeline(self, *_args, **_kwargs):
            raise KeyboardInterrupt

    aborted = P2CommitPhaseCapture(
        tmp_path / "aborted.jsonl", enabled=True,
        timer_factory=lambda delay, callback: aborted_timer.append(
            _FakeTimer(delay, callback)) or aborted_timer[-1],
    )
    aborted.start()
    try:
        with pytest.raises(KeyboardInterrupt):
            _handler(AbortedRuntime(), {
                "api_version": 1,
                "project_id": "project-watchdog",
                "timeline_id": "timeline-watchdog",
                "base_revision_id": "revision-1",
                "base_publication_id": "publication-1",
                "commands": [],
            })._dispatch()
    finally:
        aborted.stop()
    assert aborted_timer[0].cancelled
    assert aborted.watchdog_captures == 0

    disabled_timer = []
    disabled = P2CommitPhaseCapture(tmp_path / "disabled-watchdog.jsonl",
                                    timer_factory=lambda *_args: disabled_timer.append(True))
    disabled.start()
    assert disabled_timer == []
    disabled.stop()


def test_watchdog_overlap_is_request_owned_and_global_capture_cap_is_bounded(tmp_path):
    entered = {"one": threading.Event(), "two": threading.Event()}
    release = {"one": threading.Event(), "two": threading.Event()}
    dumps = []

    class Runtime:
        def commit_timeline(self, project, *_args, **_kwargs):
            name = project.rsplit("-", 1)[-1]
            entered[name].set()
            assert release[name].wait(2)
            return {"data": {"status": "accepted"}, "receipt": None}

    def dump_traceback(*, file, all_threads):
        dumps.append(all_threads)
        file.write("overlap\n")

    capture = P2CommitPhaseCapture(
        tmp_path / "overlap.jsonl", enabled=True, max_watchdog_captures=1,
        timer_factory=lambda delay, callback: _FakeTimer(delay, callback),
        dump_traceback=dump_traceback,
    )
    bodies = [
        {"api_version": 1, "project_id": f"project-{name}", "timeline_id": "timeline-watchdog",
         "base_revision_id": "revision-1", "base_publication_id": "publication-1", "commands": []}
        for name in ("one", "two")
    ]
    handlers = [_handler(Runtime(), body, key=f"overlap-{index}") for index, body in enumerate(bodies)]
    threads = [threading.Thread(target=handler._dispatch) for handler in handlers]
    capture.start()
    try:
        threads[0].start()
        assert entered["one"].wait(2)
        threads[1].start()
        assert entered["two"].wait(2)
        first_timer = capture._requests[1]["watchdog_timer"]
        second_timer = capture._requests[2]["watchdog_timer"]
        assert first_timer is not None and second_timer is not None
        first_timer.fire()
        second_timer.fire()
        release["one"].set()
        threads[0].join(timeout=2)
        assert first_timer.cancelled is False
        assert second_timer.cancelled is False
        release["two"].set()
        threads[1].join(timeout=2)
    finally:
        for event in release.values():
            event.set()
        for thread in threads:
            thread.join(timeout=2)
        capture.stop()

    assert dumps == [True]
    assert capture.watchdog_captures == 1
    assert capture._handler_requests == {}
    assert capture._thread_requests == {}


def test_live_watchdog_uses_real_handler_and_private_faulthandler_output(tmp_path):
    entered = threading.Event()
    release = threading.Event()

    class Runtime:
        def commit_timeline(self, *_args, **_kwargs):
            entered.set()
            assert release.wait(2)
            return {"data": {"status": "accepted"}, "receipt": None}

    body = {
        "api_version": 1,
        "project_id": "project-live-watchdog",
        "timeline_id": "timeline-live-watchdog",
        "base_revision_id": "revision-1",
        "base_publication_id": "publication-1",
        "commands": [],
    }
    server: Any = RuntimeHTTPServer(("127.0.0.1", 0), RuntimeHandler)
    server.runtime = Runtime()
    server.credentials = _Credentials()
    capture = P2CommitPhaseCapture(tmp_path / "live.jsonl", enabled=True, watchdog_seconds=0.01)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    request_result = []

    def request():
        connection = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        connection.request("POST", "/v1/projects/project-live-watchdog/timelines/timeline-live-watchdog/commit",
                           body=json.dumps(body), headers={
                               "Authorization": "Bearer phase-token",
                               "Content-Type": "application/json",
                               "Idempotency-Key": "live-watchdog",
                           })
        response = connection.getresponse()
        request_result.append(response.status)
        response.read()
        connection.close()

    capture.start()
    server_thread.start()
    request_thread = threading.Thread(target=request)
    request_thread.start()
    try:
        assert entered.wait(2)
        time.sleep(0.05)
        release.set()
        request_thread.join(timeout=2)
    finally:
        release.set()
        request_thread.join(timeout=2)
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=2)
        capture.stop()

    assert request_result == [200]
    assert capture.watchdog_sink is not None
    assert capture.watchdog_sink.exists()
    assert os.stat(capture.watchdog_sink).st_mode & 0o777 == 0o600
    assert "Thread" in capture.watchdog_sink.read_text()


def test_watchdog_stop_is_truthful_before_a_new_daemon_capture(tmp_path):
    timers = []

    def timer_factory(delay, callback):
        timer = _FakeTimer(delay, callback)
        timers.append(timer)
        return timer

    first = P2CommitPhaseCapture(tmp_path / "restart-1.jsonl", enabled=True,
                                 timer_factory=timer_factory)
    first.start()
    request = first._new_request(handler=object(), emit_handler=True)
    assert request == 1
    first.stop()
    assert timers[0].cancelled
    timers[0].fire()
    assert first.watchdog_captures == 0

    second = P2CommitPhaseCapture(tmp_path / "restart-2.jsonl", enabled=True,
                                  timer_factory=timer_factory)
    second.start()
    try:
        assert second.active
    finally:
        second.stop()
    assert not second.active
