"""Actual start-worker CLI entry with an injected HTTP refusal; no live endpoint."""
from __future__ import annotations

from email.message import Message
import hashlib
import io
import json
from pathlib import Path
import urllib.error

import pytest

from banodoco_local import cli
from banodoco_local import capture_result
from banodoco_local.paths import RuntimePaths

RID = "request-" + "a" * 32
HEADER_RID = "b" * 32
SECRET = "private-message-token-endpoint"


@pytest.fixture
def invoke(monkeypatch, tmp_path, capsys):
    paths = RuntimePaths.sandbox(tmp_path)
    monkeypatch.setattr(cli, "_paths", lambda _args: paths)
    monkeypatch.setattr(cli, "_validate_support_paths", lambda _paths: None)
    monkeypatch.setattr(cli, "_read_support_json", lambda _path: {"endpoint": "http://127.0.0.1:4321"})
    monkeypatch.setattr(cli, "_credential", lambda _paths: SECRET)
    calls = []
    streams = []

    def run(body, *, status=401, header=None):
        headers = Message()
        if header is not None:
            headers["X-Request-ID"] = header
        stream = io.BytesIO(body)
        streams.append(stream)
        error = urllib.error.HTTPError("http://private-endpoint", status, SECRET, headers, stream)
        def open_request(request, timeout):
            calls.append((request, timeout))
            assert request.method == "POST"
            assert request.full_url == "http://127.0.0.1:4321/v1/control/local-worker/start"
            assert request.get_header("Authorization") == "Bearer " + SECRET
            assert json.loads(request.data) == {"profile_id": "astrid", "expected_workspace_uuid": "own-workspace"}
            assert timeout == 30
            raise error
        monkeypatch.setattr(cli.urllib.request, "urlopen", open_request)
        assert cli.main(["start-worker", "--expected-workspace-uuid", "own-workspace", "--json"]) == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        assert SECRET not in captured.out
        assert "private-endpoint" not in captured.out
        assert "message" not in captured.out and "details" not in captured.out
        result = json.loads(captured.out)
        assert result["ok"] is False
        assert set(result) == {"ok", "error"}
        assert stream.closed
        return result["error"]
    return run


def test_shipped_serializer_is_the_byte_identical_sealed_projection():
    assert hashlib.sha256(Path(capture_result.__file__).read_bytes()).hexdigest() == "6a42c112f9a9289c5cc0a1a265176494463e6c25c4366ecc72e737a8cbb5d781"


@pytest.mark.parametrize("code", sorted(capture_result.PUBLIC_ERROR_CODES))
def test_actual_cli_retains_finite_code_status_and_matching_request_id(invoke, code):
    raw = json.dumps({"code": code, "request_id": RID, "message": SECRET, "details": {"token": SECRET}}).encode()
    assert invoke(raw, status=403, header=RID) == {"code": code, "status": 403, "request_id": RID}


@pytest.mark.parametrize("body", [
    b"", b"not JSON", b"\xff", b"[]", b"null", b'{"code":"unauthorized","code":"forbidden"}',
    b'{"code":"unauthorized","status":NaN}',
    b'{"message":"unauthorized","details":{"code":"forbidden"}}',
    b'{"error":{"code":"unauthorized","request_id":"' + RID.encode() + b'"}}',
    b'{"code":true}', b'{"code":"enospc"}', b'{"code":"foreign_error"}',
])
def test_absent_malformed_or_nonpublic_body_fields_are_not_classified(invoke, body):
    assert invoke(body) == {"status": 401}


@pytest.mark.parametrize("body_id,header,expected", [
    (None, HEADER_RID, HEADER_RID), ("unsafe-token", HEADER_RID, HEADER_RID),
    (RID, None, RID), (RID, RID, RID), (RID, HEADER_RID, None),
    (None, "unsafe-token", None), ("unsafe-token", None, None),
    (RID, "unsafe-token", RID), ("a" * 32, None, "a" * 32),
])
def test_request_id_body_header_parsing_is_validated_and_conflicts_are_omitted(invoke, body_id, header, expected):
    result = invoke(json.dumps({"code": "unauthorized", "request_id": body_id}).encode(), header=header)
    assert result == {"code": "unauthorized", "status": 401, **({"request_id": expected} if expected else {})}


@pytest.mark.parametrize("status", [True, "401", 401.0, 99, 600, None])
def test_only_actual_numeric_http_status_is_projected(invoke, status):
    assert invoke(b'{"code":"unauthorized","status":200}', status=status) == {"code": "unauthorized"}


def test_oversized_body_has_no_body_projection_but_keeps_valid_header(invoke):
    body = b'{"code":"unauthorized","message":"' + b"x" * 1_048_576 + b'"}'
    assert invoke(body, header=HEADER_RID) == {"status": 401, "request_id": HEADER_RID}


def test_original_response_bytes_stay_private_in_memory_and_refusal_is_unchanged():
    raw = json.dumps({"code": "unauthorized", "message": SECRET}).encode()
    error = urllib.error.HTTPError("http://private-endpoint", 401, SECRET, Message(), io.BytesIO(raw))
    refusal = cli._worker_http_refusal(error)
    assert isinstance(refusal, cli.BootstrapError)
    assert SECRET not in str(refusal) and SECRET not in repr(refusal)
    assert refusal.safe_error() == {"code": "unauthorized", "status": 401}
    assert vars(refusal)["_LocalWorkerHTTPRefusal__result_bytes"] == raw
    assert raw not in [refusal.safe_error()]


def test_body_read_and_close_failure_preserve_http_refusal_without_text():
    class BrokenBody:
        def read(self, *_args):
            raise OSError(SECRET)
        def close(self):
            raise OSError(SECRET)
    error = urllib.error.HTTPError("http://private-endpoint", 401, SECRET, Message(), BrokenBody())
    assert cli._worker_http_refusal(error).safe_error() == {"status": 401}


def test_success_metadata_route_is_unchanged(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, "_validate_support_paths", lambda _paths: None)
    monkeypatch.setattr(cli, "_read_support_json", lambda _path: {"endpoint": "http://127.0.0.1:4321"})
    monkeypatch.setattr(cli, "_credential", lambda _paths: "own-test-token")
    class Response(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *_args): self.close()
    expected = {"state": "ready", "executor_incarnation": "qualified-test-input"}
    monkeypatch.setattr(cli.urllib.request, "urlopen", lambda *a, **k: Response(json.dumps(expected).encode()))
    assert cli.main(["start-worker", "--home", str(tmp_path), "--expected-workspace-uuid", "own-workspace", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == expected


def test_missing_discovery_guard_still_refuses_before_any_transport(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, "_validate_support_paths", lambda _paths: None)
    monkeypatch.setattr(cli, "_read_support_json", lambda _path: None)
    monkeypatch.setattr(cli.urllib.request, "urlopen", lambda *a, **k: pytest.fail("transport crossed discovery guard"))
    assert cli.main(["start-worker", "--home", str(tmp_path), "--expected-workspace-uuid", "own-workspace", "--json"]) == 1
    assert json.loads(capsys.readouterr().out) == {"ok": False, "error": "No runtime discovery is available; run banodoco-local up --profile astrid."}
