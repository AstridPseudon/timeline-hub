"""``timelines create``: the empty-timeline route from a fresh project.

The CLI verb is one SDK call (``client.timelines.create_empty``).  The SDK
method makes the runtime identity shell and then the first, empty
parent-composition head, because checkout, show, visualize, and render all
refuse a timeline that has no head.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from astrid.core.cli.domain_product import run_product_family
from astrid.core.ids import is_ulid
from astrid.core.receipts.contract import CommandReceipt
from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.remote import RemoteTimelines
from astrid.sdk.workspace_client import WorkspaceClientError

ENVELOPE_KEYS = {"ok", "data", "error", "receipt", "idempotency_key"}
DEFAULT_CONFIG = {
    "tracks": [],
    "theme_overrides": {
        "visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}
    },
}


def _receipt(key: str) -> CommandReceipt:
    return CommandReceipt(
        command_kind="timeline.create",
        idempotency_key=key,
        project_id="P-1",
        receipt_id="txn-1",
        request_hash="0" * 64,
        result={},
        event_ids=(),
        project_seq=(1, 1),
        created_at="2026-10-09T12:00:00+00:00",
    )


class _RecordingTimelines:
    def __init__(self, owner: "_FakeClient") -> None:
        self._owner = owner

    def create_empty(self, *, project, timeline_id=None, config=None, idempotency_key=None):
        self._owner.calls.append(
            (
                "timelines.create_empty",
                {
                    "project": project,
                    "timeline_id": timeline_id,
                    "config": config,
                    "idempotency_key": idempotency_key,
                },
            )
        )
        key = idempotency_key or "generated-key"
        return DomainResult.success(
            {"project_id": "P-1", "timeline_id": timeline_id or "T-1", "head_revision_id": "H-1", "created": True},
            receipt=_receipt(key),
            idempotency_key=key,
        )


class _FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.timelines = _RecordingTimelines(self)


def _run(args: list[str], client: _FakeClient | None = None) -> int:
    return run_product_family("timelines", args, client=client or _FakeClient())


def test_timelines_create_is_one_sdk_call_with_default_canvas(capsys) -> None:
    client = _FakeClient()
    rc = _run(["create", "--project", "render-smoke", "--json"], client=client)
    assert rc == 0
    assert client.calls == [
        (
            "timelines.create_empty",
            {
                "project": "render-smoke",
                "timeline_id": None,
                "config": DEFAULT_CONFIG,
                "idempotency_key": None,
            },
        )
    ]
    envelope = json.loads(capsys.readouterr().out)
    assert set(envelope) == ENVELOPE_KEYS
    assert envelope["ok"] is True
    assert envelope["data"]["head_revision_id"] == "H-1"


def test_timelines_create_forwards_id_canvas_fps_and_key(capsys) -> None:
    client = _FakeClient()
    rc = _run(
        [
            "create",
            "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            "--project",
            "render-smoke",
            "--canvas",
            "640x360",
            "--fps",
            "24",
            "--idempotency-key",
            "caller-key-1",
            "--json",
        ],
        client=client,
    )
    assert rc == 0
    _, kwargs = client.calls[0]
    assert kwargs["timeline_id"] == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    assert kwargs["idempotency_key"] == "caller-key-1"
    assert kwargs["config"] == {
        "tracks": [],
        "theme_overrides": {"visual": {"canvas": {"width": 640, "height": 360, "fps": 24}}},
    }
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["idempotency_key"] == "caller-key-1"


def test_timelines_create_requires_project_flag() -> None:
    client = _FakeClient()
    with pytest.raises(SystemExit) as excinfo:
        _run(["create", "--json"], client=client)
    assert excinfo.value.code == 2
    assert client.calls == []


@pytest.mark.parametrize(
    "extra",
    [
        ["--canvas", "1920"],
        ["--canvas", "0x1080"],
        ["--canvas", "wide"],
        ["--fps", "0"],
        ["--fps", "thirty"],
    ],
)
def test_timelines_create_rejects_malformed_canvas_or_fps(extra: list[str]) -> None:
    client = _FakeClient()
    with pytest.raises(SystemExit) as excinfo:
        _run(["create", "--project", "render-smoke", *extra], client=client)
    assert excinfo.value.code == 2
    assert client.calls == []


def test_timelines_create_failure_envelope_exits_one(capsys) -> None:
    class _Conflict(_RecordingTimelines):
        def create_empty(self, **kwargs):
            return DomainResult.failure(
                ErrorObject("conflict", "timeline already exists", {"timeline_id": "T-1"}),
                idempotency_key="k",
            )

    client = _FakeClient()
    client.timelines = _Conflict(client)
    rc = _run(["create", "T-1", "--project", "render-smoke", "--json"], client=client)
    assert rc == 1
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["ok"] is False
    assert envelope["error"]["code"] == "conflict"


@pytest.mark.parametrize("argv", [["create", "--help"]])
def test_timelines_create_help_is_executable(argv: list[str]) -> None:
    from astrid.packs.timeline.cli import build_parser

    with pytest.raises(SystemExit) as excinfo:
        build_parser(_FakeClient()).parse_args(argv)
    assert excinfo.value.code == 0


# -- SDK route ------------------------------------------------------------


class _SessionOutbox:
    def __init__(self, session: "_Session") -> None:
        self.session = session

    def locked(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


class _Session:
    def __init__(self, writer: "_Writer") -> None:
        from astrid.sdk.timeline.commit import bundle_from_document
        from tests.editing_conformance.test_pristine_initialize import empty_document

        self.writer = writer
        self.bundle = bundle_from_document(empty_document())
        self.outbox = _SessionOutbox(self)
        self.calls: list[tuple[list[dict[str, Any]], str]] = []

    def _state(self):
        return {"base": {"revision_id": "bootstrap", "publication_id": "bootstrap-publication"},
                "pending": [], "flight": None}

    def _bundle(self, _state):
        return self.bundle

    def commit_many(self, commands, *, idempotency_key, label, steps, merge, reads):
        import copy

        from astrid.sdk.timeline.commands import execute
        from astrid.sdk.timeline.commit import _digest, document_from_bundle

        self.calls.append((copy.deepcopy(commands), idempotency_key))
        self.writer.calls.append(("commit_timeline", tuple(commands), {"idempotency_key": idempotency_key}))
        plan = execute(self.bundle, commands)
        document = document_from_bundle(plan.bundle)
        data = {
            "status": "accepted", "accepted_revision_id": "H-1",
            "base_revision_id": "bootstrap", "base_publication_id": "bootstrap-publication",
            "previous_revision_id": "bootstrap", "previous_publication_id": "bootstrap-publication",
            "rebased_onto": None, "canonical_document": document,
            "document_digest": _digest(document), "commands": plan.commands,
            "id_map": {}, "steps": steps, "merge_mode": merge,
            "reads": reads,
            "provider_version": "astrid-v1", "compiler_version": "authoring-bundle-1",
            "publisher": "actor",
        }
        receipt = {
            "receipt_id": "publication-1", "command_kind": "timeline.commit",
            "idempotency_key": idempotency_key, "request_hash": "0" * 64,
            "project_id": "P-1", "project_seq": [1, 1], "event_ids": ["event-1"],
            "result": copy.deepcopy(data), "created_at": "2026-10-23T00:00:00Z",
        }
        self.writer.history.append({"receipt": receipt})
        return {"data": data, "receipt": receipt}


class _Writer:
    """Records the native shell/history/commit calls; no legacy writer exists."""

    _last_handshake = {"realm_id": "realm", "actor_id": "actor"}

    def __init__(self, *, shell_error: WorkspaceClientError | None = None) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self._shell_error = shell_error
        self.history: list[dict[str, Any]] = []

    def create_timeline(self, project_id, timeline_id, *, idempotency_key, name=None):
        self.calls.append(("create_timeline", (project_id, timeline_id), {"idempotency_key": idempotency_key}))
        if self._shell_error is not None:
            raise self._shell_error
        return {
            "data": {"project_id": "P-1", "timeline_id": timeline_id,
                     "head_revision_id": "bootstrap", "head_publication_id": "bootstrap-publication"},
            "receipt": None,
        }

    def list_timeline_commits(self, project_id, timeline_id, *, cursor=None, limit=100):
        self.calls.append(("list_timeline_commits", (project_id, timeline_id),
                           {"cursor": cursor, "limit": limit}))
        return {"head": {"revision_id": "bootstrap", "publication_id": "bootstrap-publication"},
                "items": list(self.history), "next_cursor": None}


def _native_session(monkeypatch, writer):
    from astrid.sdk.timeline.sync import TimelineSession

    session = _Session(writer)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)
    return session


def test_remote_create_empty_creates_shell_then_native_commit(monkeypatch) -> None:
    writer = _Writer()
    session = _native_session(monkeypatch, writer)
    result = RemoteTimelines(writer).create_empty(
        project="render-smoke", timeline_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        config=DEFAULT_CONFIG, idempotency_key="caller-1",
    )
    assert result.ok, result.error
    assert result.data["project_id"] == "P-1"
    assert result.data["timeline_id"] == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    assert result.data["head_revision_id"] == "H-1"
    assert result.data["created"] is True
    assert result.idempotency_key == "caller-1"
    assert writer.calls[0] == (
        "create_timeline", ("render-smoke", "01ARZ3NDEKTSV4RRFFQ69G5FAV"),
        {"idempotency_key": "caller-1-shell"},
    )
    assert writer.calls[1][0] == "list_timeline_commits"
    command, key = session.calls[0]
    assert key == "caller-1-head"
    assert command[0]["op"] == "timeline.init"
    assert command[0]["args"]["name"] == "Main"
    assert session.writer.history[0]["receipt"]["result"]["steps"][0]["reads"] == [
        {"kind": "scope", "ref": "timeline", "path": []},
    ]
    assert not any(name == "publish_parent_composition" for name, _, _ in writer.calls)


def test_remote_create_empty_generates_ulid_when_no_id_given(monkeypatch) -> None:
    writer = _Writer()
    _native_session(monkeypatch, writer)
    result = RemoteTimelines(writer).create_empty(project="render-smoke")
    assert result.ok, result.error
    timeline_key = result.data["timeline_id"]
    assert is_ulid(timeline_key)
    assert writer.calls[0][1] == ("render-smoke", timeline_key)
    assert writer.calls[1][0] == "list_timeline_commits"
    assert result.data["canonical_document"]["parent_revision"]["payload"]["config"]["tracks"] == []


def test_remote_create_empty_emits_guarded_raw_config_and_replays_exact_receipt(monkeypatch) -> None:
    writer = _Writer()
    session = _native_session(monkeypatch, writer)
    config = {
        "tracks": [],
        "theme_overrides": {
            "visual": {"canvas": {"width": 640, "height": 360, "fps": 24}},
            "opaque_theme": [None, False],
        },
        "meta": {"org.example": {"null": None, "opaque": [None, False, 0]}},
    }
    result = RemoteTimelines(writer).create_empty(
        project="render-smoke", timeline_id="film", name="Second Cut",
        config=config, idempotency_key="raw-config",
    )
    assert result.ok, result.error
    payload = result.data["canonical_document"]["parent_revision"]["payload"]
    assert payload["name"] == "Second Cut" and payload["slug"] == "second-cut"
    assert payload["config"]["theme_overrides"] == config["theme_overrides"]
    assert payload["config"]["meta"] == config["meta"]
    assert payload["config"]["output"]["resolution"] == "640x360"
    assert payload["config"]["output"]["fps"] == 24
    assert any(command["op"] == "doc.patch" for command in session.calls[0][0][1:])
    calls_before_retry = len(session.calls)
    replayed = RemoteTimelines(writer).create_empty(
        project="render-smoke", timeline_id="film", name="Second Cut",
        config=config, idempotency_key="raw-config",
    )
    assert replayed.ok, replayed.error
    assert replayed.receipt == result.receipt
    assert replayed.data["canonical_document"] == result.data["canonical_document"]
    assert len(session.calls) == calls_before_retry


def test_d69_upstream_remote_create_empty_generates_ulid_when_no_id_given() -> None:
    writer = _Writer()
    result = RemoteTimelines(writer).create_empty(project="render-smoke")
    assert result.ok, result.error
    timeline_id = result.data["timeline_id"]
    assert is_ulid(timeline_id)
    assert writer.calls[0][1] == ("render-smoke", timeline_id)
    assert writer.calls[1][1][1] == timeline_id
    assert writer.calls[1][2]["idempotency_key"] == f"{result.idempotency_key}-head"
    assert writer.calls[1][1][2]["parent_composition"]["config"] == {"tracks": []}


def test_remote_create_empty_stops_when_shell_is_rejected() -> None:
    writer = _Writer(shell_error=WorkspaceClientError(409, "conflict", "timeline already exists"))
    result = RemoteTimelines(writer).create_empty(project="render-smoke", timeline_id="T-1", idempotency_key="k")
    assert not result.ok
    assert result.error.code == "conflict"
    assert [name for name, _, _ in writer.calls] == ["create_timeline"]


# D66 restore of upstream-924 selector 12306.  The old positive is retained
# beside the native commit case; no old-route retirement is inferred here.
def test_d66_upstream_remote_create_empty_creates_shell_then_empty_head() -> None:
    writer = _Writer()
    result = RemoteTimelines(writer).create_empty(
        project="render-smoke",
        timeline_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        config=DEFAULT_CONFIG,
        idempotency_key="caller-1",
    )
    assert result.ok, result.error
    assert result.data == {
        "project_id": "P-1",
        "timeline_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
        "head_revision_id": "H-1",
        "created": True,
    }
    assert result.idempotency_key == "caller-1"
    shell, head = writer.calls
    assert shell == (
        "create_timeline",
        ("render-smoke", "01ARZ3NDEKTSV4RRFFQ69G5FAV"),
        {"idempotency_key": "caller-1-shell"},
    )
    name, args, kwargs = head
    assert name == "publish_parent_composition"
    assert args[0] == "P-1"  # the runtime's project id, not the slug
    publication = args[2]
    assert publication["expected_head"] is None
    assert publication["parent_composition"] == {
        "config": DEFAULT_CONFIG,
        "registry": {},
        "clips": [],
        "occurrences": [],
    }
    assert publication["shot_revisions"] == []
    assert publication["internal_timeline_revisions"] == []
    assert kwargs == {"idempotency_key": "caller-1-head"}
