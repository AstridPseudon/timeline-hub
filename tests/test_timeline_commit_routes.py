import io
import json
from types import SimpleNamespace

import pytest

from runtime_protocol.door import classify
from runtime_protocol.errors import ConflictError, InvalidRequestError, ProtocolError
from runtime_protocol.server import RuntimeHandler


PROJECT = "project-1"
TIMELINE = "timeline-1"


def request_body(**overrides):
    body = {
        "api_version": 1,
        "project_id": PROJECT,
        "timeline_id": TIMELINE,
        "base_revision_id": "revision-1",
        "base_publication_id": "publication-1",
        "commands": [{
            "schema_version": 1,
            "op": "clip.move",
            "version": "1",
            "select": "parent/clip:clip-1",
            "args": {"on": 1.0},
        }],
    }
    body.update(overrides)
    return body


class RouteHandler(RuntimeHandler):
    def _identity(self, scope):
        self.scopes_seen.append(scope)
        return {"actor": "publisher-1", "scopes": ["projects:write", "projects:read"]}

    def _send(self, status, payload=None, **kwargs):
        self.reply = status, payload


def make_handler(runtime, body, *, path=None, headers=None):
    handler = object.__new__(RouteHandler)
    handler.server = SimpleNamespace(runtime=runtime)
    handler.command = "POST"
    handler.path = path or f"/v1/projects/{PROJECT}/timelines/{TIMELINE}/commit"
    raw = body if isinstance(body, bytes) else json.dumps(body, separators=(",", ":")).encode()
    handler.rfile = io.BytesIO(raw)
    handler.headers = {"Content-Length": str(len(raw)), "Idempotency-Key": "commit-key-1", **(headers or {})}
    handler.scopes_seen = []
    return handler


def test_commit_route_passes_canonical_envelope_and_publisher_unchanged():
    calls = []

    def commit(project_id, timeline_id, body, *, idempotency_key, publisher, invocation_path, authorize):
        calls.append((project_id, timeline_id, body, idempotency_key, publisher, invocation_path))
        assert authorize()["actor"] == publisher
        return {"data": {"status": "accepted"}, "receipt": {"receipt_id": "r1"}}

    handler = make_handler(SimpleNamespace(commit_timeline=commit), request_body())
    handler._route()
    assert handler.reply == (200, {"data": {"status": "accepted"}, "receipt": {"receipt_id": "r1"}})
    assert calls[0][:2] == (PROJECT, TIMELINE)
    assert calls[0][2] == request_body()
    assert calls[0][3:] == ("commit-key-1", "publisher-1", f"/v1/projects/{PROJECT}/timelines/{TIMELINE}/commit")
    assert handler.scopes_seen == ["projects:write", "projects:write"]


@pytest.mark.parametrize("body", [
    {"api_version": 1},
    request_body(commands=[]),
    request_body(project_id="other-project"),
])
def test_commit_route_rejects_malformed_or_path_mismatched_envelope(body):
    handler = make_handler(SimpleNamespace(commit_timeline=lambda *args, **kwargs: pytest.fail("provider called")), body)
    with pytest.raises((InvalidRequestError, ConflictError)):
        handler._route()


def test_commit_route_rejects_duplicate_fields_and_duplicate_idempotency_headers():
    duplicate = b'{"api_version":1,"api_version":1,"project_id":"project-1","timeline_id":"timeline-1","base_revision_id":"r","base_publication_id":"p","commands":[]}'
    handler = make_handler(SimpleNamespace(commit_timeline=lambda *args, **kwargs: pytest.fail("provider called")), duplicate)
    with pytest.raises(ProtocolError):
        handler._route()

    class DuplicateHeaders(dict):
        def get_all(self, name, default=None):
            if name.lower() == "idempotency-key":
                return ["one", "two"]
            return [self.get(name)] if name in self else (default or [])

    handler = make_handler(SimpleNamespace(commit_timeline=lambda *args, **kwargs: pytest.fail("provider called")), request_body())
    handler.headers = DuplicateHeaders(handler.headers)
    with pytest.raises(ProtocolError):
        handler._route()


def test_commit_route_neutral_runtime_returns_503_without_provider_call():
    handler = make_handler(SimpleNamespace(), request_body())
    with pytest.raises(Exception) as caught:
        handler._route()
    assert caught.value.status == 503
    assert caught.value.as_dict()["details"]["reason"] == "runtime_unavailable"


def test_new_door_routes_are_exact():
    assert classify("/api/runtime/v1/projects/project-1/timelines/timeline-1/commit", "POST")
    assert classify("/api/runtime/v1/projects/project-1/timelines/timeline-1/commits", "GET")
    assert classify("/api/runtime/v1/projects/project-1/media-selection?asset=a&generation_id=g&variant_id=v", "GET")
    assert classify("/api/runtime/v1/projects/project-1/timelines/timeline-1/commit/extra", "POST") is None
