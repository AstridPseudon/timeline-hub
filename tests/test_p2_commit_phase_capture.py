from __future__ import annotations

import http.client
import io
import json
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
                              "status", "last_phase", "phases", "truncated"}
               for event in capture.events)


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
    for phase in ("handler_entry", "authorization", "coordinator_admission", "coordinator_lock",
                  "provider", "accept", "receipt", "http_response"):
        assert phases[phase]["status"] == "observed", (phase, summaries)
    for phase in ("coordinator_admission", "coordinator_lock"):
        assert phases[phase]["count"] == 1
        assert phases[phase]["end_ms"] is not None
    assert summaries[0]["last_phase"] == "http_response"
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
