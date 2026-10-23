"""``timelines create``: the empty-timeline route from a fresh project.

The CLI verb is one SDK call (``client.timelines.create_empty``).  The SDK
method makes the runtime identity shell and then the first, empty
parent-composition head, because checkout, show, visualize, and render all
refuse a timeline that has no head.
"""

from __future__ import annotations

import copy
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


class _Writer:
    """Runtime transport seam: real v2 execution, bootstrap and immutable reads."""

    _last_handshake = {"realm_id": "realm", "actor_id": "actor"}

    def __init__(self, *, shell_error=None):
        self.calls = []
        self._shell_error = shell_error
        self.documents = {}
        self.replays = {}
        self.head = None
        self.lose_ack = False
        self.failure = None

    def create_timeline(self, project_id, timeline_id, *, idempotency_key):
        from astrid.sdk.timeline.commit import _digest

        self.calls.append(("create_timeline", (project_id, timeline_id), {"idempotency_key": idempotency_key}))
        if self._shell_error:
            raise self._shell_error
        if not self.documents:
            payload = {"config": {"tracks": [], "clips": []}, "registry": {}, "clips": [], "occurrences": []}
            self.documents['bootstrap'] = {
                "schema_version": 1, "project_id": "P-1", "timeline_id": timeline_id,
                "parent_revision": {"revision_id": "bootstrap", "content_digest": _digest(payload), "payload": payload},
                "shot_revisions": [], "internal_timeline_revisions": [],
                "dependency_manifest": {"shots": [], "internal_timelines": [], "media": [], "documents": []},
            }
            self.head = {"revision_id": "bootstrap", "publication_id": "bootstrap-publication"}
        return {"data": {"project_id": "P-1", "timeline_id": timeline_id,
                         "head_revision_id": "bootstrap", "head_publication_id": "bootstrap-publication"}, "receipt": None}

    def get_project_parent_composition_revision(self, project, timeline, revision):
        document = self.documents[revision]
        assert (project, timeline) == (document['project_id'], document['timeline_id'])
        return {**copy.deepcopy(document['parent_revision']),
                'dependency_manifest': copy.deepcopy(document['dependency_manifest'])}

    def get_project_shot_revision(self, project, shot, revision):
        return copy.deepcopy(next(row for document in self.documents.values() for row in document['shot_revisions']
                                  if row['shot_id'] == shot and row['revision_id'] == revision))

    def get_project_timeline_revision(self, project, timeline, revision):
        return copy.deepcopy(next(row for document in self.documents.values() for row in document['internal_timeline_revisions']
                                  if row['timeline_id'] == timeline and row['revision_id'] == revision))

    def list_timelines(self, project, **kwargs):
        doc = next(iter(self.documents.values()))
        return ([{'project_id': doc['project_id'], 'timeline_id': doc['timeline_id']}], None)

    def list_timeline_commits(self, project, timeline, **kwargs):
        return {'head': copy.deepcopy(self.head), 'items': [
            {'revision_id': revision, 'publication_id': ('bootstrap-publication' if revision == 'bootstrap'
                else self.head['publication_id'] if revision == self.head['revision_id'] else 'publication-1')}
            for revision in self.documents], 'next_cursor': None}

    def commit_timeline(self, project, timeline, body, *, idempotency_key):
        import hashlib

        from astrid.core.receipts.canonical import canonical_json
        from astrid.sdk.timeline.commands import execute
        from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle

        self.calls.append(('commit_timeline', (project, timeline, copy.deepcopy(body)), {'idempotency_key': idempotency_key}))
        if self.failure:
            raise self.failure
        if idempotency_key in self.replays:
            original, result = self.replays[idempotency_key]
            assert body == original
            return copy.deepcopy(result)
        plan = execute(bundle_from_document(self.documents[body['base_revision_id']]), body['commands'], commit_request=body)
        document = document_from_bundle(plan.bundle)
        document['parent_revision']['revision_id'] = 'H-1'
        data = {'status': 'preview' if body.get('dry_run') else 'accepted',
                'base_revision_id': body['base_revision_id'], 'base_publication_id': body['base_publication_id'],
                'previous_revision_id': self.head['revision_id'], 'previous_publication_id': self.head['publication_id'],
                'accepted_revision_id': 'H-1', 'rebased_onto': None, 'canonical_document': document,
                'document_digest': _digest(document), 'commands': plan.commands, 'id_map': {},
                'steps': copy.deepcopy(plan.steps), 'merge_mode': plan.merge_mode,
                'provider_version': 'astrid-v1', 'compiler_version': 'authoring-bundle-1', 'publisher': 'actor'}
        receipt = {'receipt_id': 'publication-2', 'command_kind': 'timeline.commit',
                   'idempotency_key': idempotency_key, 'project_id': project, 'project_seq': [1, 1],
                   'request_hash': hashlib.sha256(canonical_json({'operation': 'commitTimeline',
                       'path': f'/v1/projects/{project}/timelines/{timeline}/commit', 'publisher': 'actor', 'request': body}).encode()).hexdigest(),
                   'event_ids': ['event-1'], 'result': copy.deepcopy(data), 'created_at': 'now'}
        if body.get('dry_run'):
            for field in ('accepted_revision_id', 'publisher'):
                data.pop(field)
            data['evaluated_head'] = copy.deepcopy(self.head)
            return {'data': data, 'receipt': None}
        result = {'data': data, 'receipt': receipt}
        self.documents['H-1'] = document
        self.head = {'revision_id': 'H-1', 'publication_id': 'publication-2'}
        self.replays[idempotency_key] = (copy.deepcopy(body), copy.deepcopy(result))
        if self.lose_ack:
            self.lose_ack = False
            raise ConnectionError('response lost after acceptance')
        return result


def _mount(monkeypatch, tmp_path, writer):
    from astrid.sdk import storage_root
    from astrid.sdk.timeline import store

    monkeypatch.setattr(storage_root, 'resolve_runtime_data_root', lambda: tmp_path)
    def resolve(project, timeline, **kwargs):
        document = next(iter(writer.documents.values()))
        return document['project_id'], document['timeline_id'], writer.head['revision_id']
    monkeypatch.setattr(store, 'resolve_ids', resolve)


def test_remote_create_empty_creates_shell_then_empty_head(monkeypatch, tmp_path) -> None:
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(
        project="render-smoke", timeline_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        config=DEFAULT_CONFIG, idempotency_key="caller-1")
    assert result.ok, result.error
    assert {key: result.data[key] for key in ('project_id', 'timeline_id', 'head_revision_id', 'created')} == {
        'project_id': 'P-1', 'timeline_id': '01ARZ3NDEKTSV4RRFFQ69G5FAV', 'head_revision_id': 'H-1', 'created': True}
    assert result.idempotency_key == "caller-1"
    shell, head = writer.calls
    assert shell == ('create_timeline', ('render-smoke', '01ARZ3NDEKTSV4RRFFQ69G5FAV'), {'idempotency_key': 'caller-1-shell'})
    assert head[0] == 'commit_timeline' and head[1][:2] == ('P-1', '01ARZ3NDEKTSV4RRFFQ69G5FAV')
    body = head[1][2]
    assert (body['base_revision_id'], body['base_publication_id']) == ('bootstrap', 'bootstrap-publication')
    assert head[2] == {'idempotency_key': 'caller-1-head'}
    document = result.data['canonical_document']
    # U1's canonical bootstrap has a redundant clips mirror; it remains empty.
    assert document['parent_revision']['payload'] == {
        'config': {**DEFAULT_CONFIG, 'clips': []}, 'registry': {}, 'clips': [], 'occurrences': []}
    assert document['shot_revisions'] == [] and document['internal_timeline_revisions'] == []
    assert body['label'] and body['merge'] == 'atomic' and 'reads' not in body
    step = body['steps'][0]
    assert set(step) == {'id', 'label', 'intent', 'tags', 'command_ordinals', 'patch', 'reads'}
    assert step['patch'] == [change for command in body['commands'] for change in command['args']['changes']]
    assert result.data['steps'][0]['dependencies'] and result.data['merge_mode'] == 'atomic'
    assert result.receipt.result['canonical_document'] == document


def test_remote_create_empty_generates_ulid_when_no_id_given(monkeypatch, tmp_path) -> None:
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(project="render-smoke")
    assert result.ok, result.error
    timeline_id = result.data['timeline_id']
    assert is_ulid(timeline_id)
    assert writer.calls[0][1] == ('render-smoke', timeline_id)
    # Runtime already bootstraps the default empty head; no second write is needed.
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {'tracks': [], 'clips': []}


def test_remote_create_empty_stops_when_shell_is_rejected() -> None:
    writer = _Writer(shell_error=WorkspaceClientError(409, "conflict", "timeline already exists"))
    result = RemoteTimelines(writer).create_empty(project="render-smoke", timeline_id="T-1", idempotency_key="k")
    assert not result.ok
    assert result.error.code == 'conflict'
    assert [name for name, _, _ in writer.calls] == ['create_timeline']


def test_remote_create_empty_retries_original_defaults_after_lost_ack(monkeypatch, tmp_path):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    writer.lose_ack = True
    config = {**DEFAULT_CONFIG, 'meta': {'org.example': {'null': None, 'opaque': [False, 0]}}}
    timelines = RemoteTimelines(writer)
    failed = timelines.create_empty(project='render-smoke', timeline_id='film', config=config, idempotency_key='retry')
    assert not failed.ok
    first = copy.deepcopy(writer.calls[-1])
    result = timelines.create_empty(project='render-smoke', timeline_id='film', config=config, idempotency_key='retry')
    assert result.ok, result.error
    assert writer.calls[-1] == first
    assert len(writer.replays) == 1
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {**config, 'clips': []}
    assert result.receipt.idempotency_key == 'retry-head'


def test_remote_create_empty_retains_structured_commit_failures(monkeypatch, tmp_path):
    for status, http_status in (('conflict', 409), ('invalid', 422)):
        writer = _Writer()
        _mount(monkeypatch, tmp_path / status, writer)
        details = {'status': status, 'reason': 'dependency_changed', 'code': 'previous_value_mismatch',
                   'path': ['config', 'theme_overrides'], 'hint': 'Read the base',
                   'suggested_command': 'astrid timelines show film',
                   'current': {'revision_id': 'other', 'publication_id': 'other-publication'}}
        writer.failure = WorkspaceClientError(http_status, 'conflict' if status == 'conflict' else 'invalid',
                                              'changed', details)
        result = RemoteTimelines(writer).create_empty(
            project='render-smoke', timeline_id='film', config=DEFAULT_CONFIG, idempotency_key=status)
        assert not result.ok
        assert result.error.details == details
        assert len(writer.documents) == 1 and writer.head['revision_id'] == 'bootstrap'
