from __future__ import annotations

import hashlib
import io
import json
import secrets
from email.message import Message
from types import SimpleNamespace

import pytest

from packages.python.banodoco_workspace_client.generated import WorkspaceClient
from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.server import RuntimeHandler
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore


def _digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def _service(root) -> RuntimeService:
    RealmStore.initialize(root).close()
    return RuntimeService(root)


def _descriptor(capability_id: str, declaration=None, *, digest=None, **extra):
    value = {
        "capability_id": capability_id,
        "definition_digest": digest or _digest(capability_id),
        "required_resource_keys": [],
        "estimated_scratch_bytes": 0,
        "estimated_output_bytes": 1024,
        **extra,
    }
    if declaration is not None:
        value["action_declaration"] = declaration
    return value


def _register(service, executor_id, descriptors, *, readiness="ready"):
    return service.register_executor(
        {
            "executor_id": executor_id,
            "capabilities": descriptors,
            "readiness": readiness,
        },
        idempotency_key=f"register-{executor_id}",
    )


def _catalog(service):
    return {item["capability_id"]: item for item in service.list_capabilities()["items"]}


def test_summary_only_capability_stays_usable_without_a_declaration(tmp_path):
    service = _service(tmp_path / "realm")
    try:
        registered = _register(service, "summary-worker", [_descriptor("legacy.summary")])
        assert "action_declaration" not in registered["capabilities"][0]
        capability = _catalog(service)["legacy.summary"]
        assert capability["status"] == "ready"
        assert capability["action_declaration_status"] == "unavailable"
        assert capability["action_declaration_reason"] == "not_advertised"
        assert "action_declaration" not in capability
    finally:
        service.close()


def test_action_and_generator_declarations_include_only_declared_presentation_fields(tmp_path):
    service = _service(tmp_path / "realm")
    action_ids = ("music.align", "music.level", "music.beats")
    declarations = []
    for capability_id in action_ids:
        declarations.append(_descriptor(capability_id, {
            "name": capability_id.rsplit(".", 1)[1].title(),
            "short_description": f"Help for {capability_id}",
            "inputs": [{"name": "audio", "type": "file", "required": True, "description": "Source audio."}],
            "outputs": [{"name": "analysis", "type": "file", "artifact_type": "application/json", "description": "Analysis."}],
        }))
    declarations.append(_descriptor("chiptune.compose", {
        "kind": "generator",
        "name": "Chiptune Compose",
        "description": "Compose a cue.",
        "keywords": ["music", "generator"],
        "invocation": {"kind": "command", "command": {"argv": ["SECRET_ARGV"]}},
        "metadata": {"pack": "PRIVATE_PACK_METADATA"},
        "resources": [{"path": "resources/private.json"}],
        "inputs": [
            {"name": "duration_s", "type": "number", "required": True, "description": "Length."},
            {"name": "sections", "type": "json", "required": True, "default": None, "description": "Sections."},
        ],
        "outputs": [{
            "name": "music", "type": "file", "artifact_type": "audio", "description": "Managed audio.",
            "path_template": "{out}/music.wav",
        }],
    }))
    try:
        _register(service, "music-worker", declarations)
        capabilities = _catalog(service)
        for capability_id in action_ids:
            item = capabilities[capability_id]
            assert item["action_declaration_status"] == "available"
            assert item["action_declaration"]["kind"] == "action"
        generator = capabilities["chiptune.compose"]["action_declaration"]
        assert generator == {
            "kind": "generator",
            "name": "Chiptune Compose",
            "description": "Compose a cue.",
            "keywords": ["music", "generator"],
            "inputs": [
                {"name": "duration_s", "type": "number", "required": True, "description": "Length."},
                {"name": "sections", "type": "json", "required": True, "default": None, "description": "Sections."},
            ],
            "outputs": [{"name": "music", "type": "file", "artifact_type": "audio", "description": "Managed audio."}],
        }
        payload = json.dumps(capabilities, sort_keys=True)
        for forbidden in ("SECRET_ARGV", "PRIVATE_PACK_METADATA", "resources/private.json", "path_template", "{out}"):
            assert forbidden not in payload
        stored = json.loads(service.store.conn.execute(
            "SELECT capabilities_json FROM executors WHERE id='music-worker'"
        ).fetchone()["capabilities_json"])
        assert stored[-1]["action_declaration"] == generator
        assert "invocation" not in stored[-1]["action_declaration"]
    finally:
        service.close()


@pytest.mark.parametrize(
    ("declaration", "reason"),
    [
        ({"inputs": [{"name": "mystery", "type": "custom.schema"}]}, "unsupported_inputs_type"),
        ({"inputs": [{"name": "untyped"}]}, "input_type_missing"),
        ({"inputs": "inputs.json"}, "unsupported_inputs_schema"),
        ({"kind": "tool"}, "unsupported_action_kind"),
    ],
)
def test_unsupported_declaration_shapes_are_explicit_and_not_guessed(tmp_path, declaration, reason):
    service = _service(tmp_path / "realm")
    try:
        _register(service, "unsupported-worker", [_descriptor("unsupported.action", declaration)])
        capability = _catalog(service)["unsupported.action"]
        assert capability["status"] == "ready"
        assert capability["action_declaration_status"] == "unsupported"
        assert capability["action_declaration_reason"] == reason
        assert "action_declaration" not in capability
    finally:
        service.close()


@pytest.mark.parametrize(
    "port",
    [
        {"name": "api_token", "type": "string", "default": "secret-token-value"},
        {"name": "options", "type": "json", "default": {"resource_path": "/private/pack/resource.json"}},
        {"name": "workspace", "type": "path", "default": "~/private/workspace"},
    ],
)
def test_unsafe_input_defaults_are_unavailable_without_echoing_values(tmp_path, port):
    service = _service(tmp_path / "realm")
    try:
        _register(service, "unsafe-default-worker", [
            _descriptor("unsafe.default", {"inputs": [port]}),
        ])
        capability = _catalog(service)["unsafe.default"]
        assert capability["action_declaration_status"] == "unsupported"
        assert capability["action_declaration_reason"] == "unsafe_input_default"
        assert "action_declaration" not in capability
        assert all(value not in json.dumps(capability) for value in (
            "secret-token-value", "/private/pack/resource.json", "~/private/workspace",
        ))
    finally:
        service.close()


def test_declaration_is_bound_to_the_exact_current_capability_digest(tmp_path):
    service = _service(tmp_path / "realm")
    old_digest = _digest("old-definition")
    new_digest = _digest("new-definition")
    try:
        _register(service, "digest-worker", [
            _descriptor("music.beats", {"name": "Old declaration"}, digest=old_digest),
        ])
        service.register_capability({
            "capability_id": "music.beats",
            "definition_digest": new_digest,
            "required_resource_keys": [],
        })
        capability = _catalog(service)["music.beats"]
        assert capability["definition_digest"] == new_digest
        assert capability["action_declaration_status"] == "unavailable"
        assert capability["action_declaration_reason"] == "not_advertised"
        assert "action_declaration" not in capability
    finally:
        service.close()


@pytest.mark.parametrize("reverse_registration", [False, True])
def test_conflicting_declarations_for_one_id_and_digest_are_unavailable(tmp_path, reverse_registration):
    service = _service(tmp_path / "realm")
    digest = _digest("music.align-v1")
    registrations = [
        ("worker-a", _descriptor("music.align", {"name": "Align A"}, digest=digest)),
        ("worker-b", _descriptor("music.align", {"name": "Align B"}, digest=digest)),
    ]
    if reverse_registration:
        registrations.reverse()
    try:
        for executor_id, descriptor in registrations:
            _register(service, executor_id, [descriptor])
        capability = _catalog(service)["music.align"]
        assert capability["action_declaration_status"] == "unsupported"
        assert capability["action_declaration_reason"] == "conflicting_declarations"
        assert "action_declaration" not in capability
    finally:
        service.close()


def test_host_unavailable_readiness_does_not_discard_declaration(tmp_path):
    service = _service(tmp_path / "realm")
    try:
        _register(service, "offline-worker", [
            _descriptor("chiptune.compose", {"kind": "generator", "name": "Compose"}),
        ], readiness="not_ready")
        capability = _catalog(service)["chiptune.compose"]
        assert capability["status"] == "unavailable"
        assert capability["action_declaration_status"] == "available"
        assert capability["action_declaration"] == {"kind": "generator", "name": "Compose"}
    finally:
        service.close()


def test_authenticated_catalog_read_keeps_declaration_and_existing_scope_refusal(tmp_path):
    realm = tmp_path / "realm"
    RealmStore.initialize(realm).close()
    service = RuntimeService(realm)
    credentials = CredentialStore(tmp_path / "credentials")
    reader_token = secrets.token_hex(32)
    denied_token = secrets.token_hex(32)
    credentials.provision_static("catalog-reader", reader_token, ["tasks:read"])
    credentials.provision_static("catalog-denied", denied_token, ["projects:read"])
    service.register_executor({
        "executor_id": "http-worker",
        "capabilities": [_descriptor("music.level", {"name": "Music Level"})],
    }, idempotency_key="http-worker-register")
    server = SimpleNamespace(
        runtime=service, credentials=credentials,
        accepting_authenticated_requests=True, paired_sessions=None,
    )

    def transport(method, path, headers, body=None):
        handler = object.__new__(RuntimeHandler)
        handler.server = server
        handler.command = method
        handler.path = path
        handler.headers = Message()
        for name, value in headers.items():
            handler.headers.add_header(name, value)
        payload = bytes(body or b"")
        if handler.headers.get("Content-Length") is None:
            handler.headers.add_header("Content-Length", str(len(payload)))
        handler.rfile = io.BytesIO(payload)
        response = {}

        def send(status, value=None, **kwargs):
            response_headers = dict(kwargs.get("headers") or {})
            raw = kwargs.get("body")
            if raw is None:
                value = kwargs.get("error", value)
                raw = json.dumps(value, sort_keys=True).encode()
                response_headers.setdefault("Content-Type", "application/json")
            response.update(status=status, headers=response_headers, body=bytes(raw))

        handler._send = send
        try:
            with service.store._mutex:
                handler._route()
        except RuntimeErrorBase as exc:
            response.update(
                status=exc.status,
                headers={"Content-Type": "application/json"},
                body=json.dumps(exc.as_dict(), sort_keys=True).encode(),
            )
        return response["status"], response.get("headers", {}), response.get("body", b"")

    try:
        status, _, raw = transport("GET", "/v1/capabilities", {"Authorization": f"Bearer {reader_token}"})
        catalog = json.loads(raw)
        assert status == 200
        item = next(row for row in catalog["items"] if row["capability_id"] == "music.level")
        assert item["action_declaration"] == {"kind": "action", "name": "Music Level"}
        client = WorkspaceClient("http://runtime.test", reader_token, transport=transport)
        rows, _ = client.list_capabilities()
        assert any(row.capability_id == "music.level" for row in rows)
        denied_status, _, denied_body = transport(
            "GET", "/v1/capabilities", {"Authorization": f"Bearer {denied_token}"},
        )
        assert denied_status == 401
        assert json.loads(denied_body)["message"] == "credential lacks required scope"
        anonymous_status, _, anonymous_body = transport("GET", "/v1/capabilities", {})
        assert anonymous_status == 401
        assert json.loads(anonymous_body)["message"] == "bearer credential required"
    finally:
        service.close()
