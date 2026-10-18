from __future__ import annotations

import inspect
import io
import json
import subprocess
import urllib.error
from pathlib import Path

import pytest

from astrid.sdk import autobootstrap
from astrid.sdk.client import AstridClient
from astrid.sdk.exceptions import ServiceUnavailableError
from astrid.sdk.remote import RemoteAstridClient, RemoteTimelines
from astrid.sdk.workspace_client import (
    PROTOCOL,
    SCHEMA_DIGEST,
    WorkspaceClient,
    WorkspaceClientError,
    resolve_runtime_connection,
)


def _open_timeout_client(monkeypatch, **options):
    """Exercise the real generated transport without contacting a runtime."""
    calls = []

    def urlopen(request, *, timeout):
        calls.append((request, timeout))
        assert request.get_header("Authorization") == "Bearer token"
        if request.full_url.endswith("/v1/health"):
            value = {
                "status": "ok", "protocol": PROTOCOL, "schema_digest": SCHEMA_DIGEST,
                "runtime_epoch": 1, "runtime_instance_id": "instance-1",
                "runtime_session_id": "runtime-session-1",
            }
        elif request.full_url.endswith("/v1/handshake"):
            value = {
                "protocol": PROTOCOL, "schema_digest": SCHEMA_DIGEST,
                "session_id": "session-1", "actor_id": "actor-1", "realm_id": "realm-1",
                "scopes": json.loads(request.data)["requested_scopes"],
                "capabilities": ["execution_binding.targeted.v1"],
            }
        else:
            raise urllib.error.URLError(TimeoutError("test deadline"))
        response = io.BytesIO(json.dumps(value).encode())
        response.status = 200
        response.headers = {}
        return response

    monkeypatch.setattr("banodoco_workspace_client.generated.urllib.request.urlopen", urlopen)
    client = AstridClient.open(
        endpoint="http://127.0.0.1:8443", credential="token",
        realm_id="realm-1", actor_id="actor-1", client_name="test", client_version="1",
        protocol_version=PROTOCOL, **options,
    )
    return client, calls


@pytest.mark.parametrize("options, expected", [({}, 30.0), ({"timeout": None}, 30.0), ({"timeout": 180.5}, 180.5)])
def test_public_timeout_reaches_generated_transport(monkeypatch, options, expected):
    client, calls = _open_timeout_client(monkeypatch, **options)
    assert client._remote._transport._generated.timeout == expected
    assert [timeout for _, timeout in calls] == [expected, expected]
    assert [request.get_method() for request, _ in calls] == ["GET", "POST"]


@pytest.mark.parametrize("dry_run", [True, False])
def test_public_timeout_preserves_commit_failure_without_retry(monkeypatch, dry_run):
    client, calls = _open_timeout_client(monkeypatch, timeout=180.5)
    body = {
        "project_id": "project-1", "timeline_id": "timeline-1",
        "request_id": "commit-request-1", "session_id": "session-1", "dry_run": dry_run,
    }
    with pytest.raises(WorkspaceClientError) as caught:
        client._remote._transport.commit_timeline(body)

    assert len(calls) == 3  # Health, handshake, and exactly one COMMIT attempt.
    request, timeout = calls[-1]
    assert timeout == 180.5
    assert request.get_method() == "POST"
    assert request.full_url.endswith("/astrid/v1/projects/project-1/timelines/timeline-1/commit")
    assert json.loads(request.data) == body
    assert request.get_header("Idempotency-key") == "commit-request-1"
    assert request.get_header("X-astrid-session") == "session-1"
    error = caught.value
    generated_error = error.__cause__
    assert (error.status, error.code, error.message) == (0, "transport_timeout", "runtime request timed out")
    assert (error.status, error.code, error.message, error.details, error.request_id) == (
        generated_error.status, generated_error.code, generated_error.message,
        generated_error.details, generated_error.request_id,
    )
    assert error.request_id == request.get_header("X-request-id")


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf"), -float("inf")])
def test_public_timeout_rejects_unbounded_values_before_requests(monkeypatch, timeout):
    monkeypatch.setattr(
        "banodoco_workspace_client.generated.urllib.request.urlopen",
        lambda *args, **kwargs: pytest.fail("invalid timeout made a request"),
    )
    with pytest.raises(ValueError, match="timeout must be finite and positive"):
        WorkspaceClient("http://127.0.0.1:8443", "token", timeout=timeout)
    with pytest.raises(ServiceUnavailableError, match="timeout must be finite and positive") as caught:
        AstridClient.open(
            endpoint="http://127.0.0.1:8443", credential="token",
            realm_id="realm-1", actor_id="actor-1", client_name="test", client_version="1",
            protocol_version=PROTOCOL, timeout=timeout,
        )
    assert isinstance(caught.value.__cause__, ValueError)


def test_open_requires_explicit_context_and_never_bootstraps(monkeypatch):
    monkeypatch.setattr(
        "astrid.sdk.autobootstrap.ensure_runtime",
        lambda: pytest.fail("ordinary SDK open invoked the launcher"),
    )
    with pytest.raises(Exception, match="banodoco-local up --profile astrid"):
        AstridClient.open()


def test_connection_resolution_does_not_guess_a_checkout_or_catalog(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("BANODOCO_RUNTIME_ENDPOINT", "http://wrong")
    monkeypatch.setenv("BANODOCO_RUNTIME_CREDENTIAL", str(tmp_path / "wrong-token"))
    with pytest.raises(WorkspaceClientError):
        resolve_runtime_connection("", "")
    assert resolve_runtime_connection("https://127.0.0.1:8443/", "Bearer token") == (
        "https://127.0.0.1:8443",
        "token",
    )


def test_connection_resolution_accepts_host_injected_runtime_context(tmp_path: Path, monkeypatch):
    credential = tmp_path / "owner.token"
    credential.write_text("child-token\n", encoding="utf-8")
    credential.chmod(0o600)
    monkeypatch.setenv("BANODOCO_RUNTIME_ENDPOINT", "http://127.0.0.1:8443/")
    monkeypatch.setenv("BANODOCO_RUNTIME_CREDENTIAL", str(credential))

    assert resolve_runtime_connection() == ("http://127.0.0.1:8443", "child-token")


def test_generated_failure_keeps_request_correlation(monkeypatch):
    class GeneratedFailure(RuntimeError):
        status = 503
        code = "registration_unavailable"
        message = "registration unavailable"
        request_id = "request-sdk-1"
        details = {"retryable": False}

    class Generated:
        def __init__(self, *_args, **_kwargs):
            pass

        def health(self):
            raise GeneratedFailure()

    monkeypatch.setattr("astrid.sdk.workspace_client.GeneratedWorkspaceClient", Generated)
    client = WorkspaceClient("http://127.0.0.1:8443", "token")

    with pytest.raises(WorkspaceClientError) as caught:
        client.health()

    assert caught.value.code == "registration_unavailable"
    assert caught.value.request_id == "request-sdk-1"
    assert caught.value.details == {"retryable": False}


def test_timeline_creation_has_only_atomic_generated_route():
    class Client:
        def create_timeline_document(self, *args, **kwargs):
            assert kwargs["config"] == {"tracks": []}
            assert kwargs["registry"] == {"assets": {}}
            return {"timeline_id": args[1], "receipt": {"receipt_id": "r"}}

    remote = RemoteTimelines(Client())
    result = remote.create(
        project="project-1",
        config={"tracks": []},
        registry={"assets": {}},
        slug="main",
        idempotency_key="timeline-1",
    )
    assert result.ok
    assert not hasattr(remote, "create_timeline")


def test_remote_has_no_retired_alias_surface():
    names = {
        "selected_project_ref",
        "read_events",
        "subscribe_events",
        "render",
        "close",
    }
    assert names.isdisjoint(vars(RemoteAstridClient))


def test_top_level_sdk_has_no_event_aliases():
    import astrid

    assert not hasattr(astrid, "read_events")
    assert not hasattr(astrid, "subscribe_events")


def test_launcher_uses_installed_command_and_explicit_manifest(monkeypatch, tmp_path: Path):
    manifest = tmp_path / "source-manifest.json"
    manifest.write_text(json.dumps({"profile": "astrid"}), encoding="utf-8")
    monkeypatch.setenv("BANODOCO_LOCAL_SOURCE_MANIFEST", str(manifest))
    monkeypatch.setenv("BANODOCO_LOCAL_LAUNCHER", "/usr/local/bin/banodoco-local")
    seen: dict[str, object] = {}

    def run(command, **kwargs):
        seen["command"] = command
        assert "env" not in kwargs
        return subprocess.CompletedProcess(
            command,
            0,
            json.dumps({"status": "started", "realm_id": "realm", "endpoint": "http://127.0.0.1:1", "actor_id": "actor"}),
            "",
        )

    monkeypatch.setattr(autobootstrap.subprocess, "run", run)
    result = autobootstrap.ensure_runtime()
    assert result["status"] == "started"
    assert seen["command"][:5] == ["/usr/local/bin/banodoco-local", "up", "--profile", "astrid", "--source-manifest"]


def test_public_open_signature_has_no_auto_bootstrap_keyword():
    assert "auto_bootstrap" not in inspect.signature(AstridClient.open).parameters


def test_sdk_boundary_has_no_checkout_or_dynamic_import_injection():
    root = Path(__file__).resolve().parents[2] / "astrid" / "sdk"
    workspace_source = (root / "workspace_client.py").read_text(encoding="utf-8")
    bootstrap_source = (root / "autobootstrap.py").read_text(encoding="utf-8")
    assert "sys.path" not in workspace_source
    assert "importlib" not in workspace_source
    assert "BANODOCO_RUNTIME_CHECKOUT" not in workspace_source
    assert "source_checkout" not in bootstrap_source
    assert "PYTHONPATH" not in bootstrap_source
