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
DEFAULT_OUTPUT = {
    'resolution': '1280x720', 'fps': 30, 'file': 'output.mp4',
    'background': None, 'background_scale': None,
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
    """Synthetic transport fixture; not evidence of Runtime authority or wire acceptance."""

    _last_handshake = {"realm_id": "realm", "actor_id": "actor"}

    def __init__(self, *, shell_error=None):
        self.calls = []
        self._shell_error = shell_error
        self.documents = {}
        self.replays = {}
        self.head = None
        self.lose_ack = False
        self.failure = None

    def create_timeline(self, project_id, timeline_id, *, idempotency_key, name=None):
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
        'name': 'Main', 'slug': 'main',
        'config': {**DEFAULT_CONFIG, 'clips': [],
                   'output': {**DEFAULT_OUTPUT, 'resolution': '1920x1080'}},
        'registry': {'assets': {}}, 'clips': [], 'occurrences': []}
    assert document['shot_revisions'] == [] and document['internal_timeline_revisions'] == []
    assert body['label'] and body['merge'] == 'atomic' and 'reads' not in body
    step = body['steps'][-1]
    assert set(step) == {'id', 'label', 'intent', 'tags', 'command_ordinals', 'patch', 'reads'}
    assert step['patch'] == [change for command in body['commands'] for change in command['args'].get('changes', [])]
    assert body['commands'][0]['op'] == 'timeline.init'
    assert body['commands'][0]['args'] == {'name': 'Main', 'slug': 'main', 'output': DEFAULT_OUTPUT}
    assert any(read['ref'] == 'parent' and read['path'] == [] for read in body['commands'][0]['reads'])
    assert body['commands'][0]['expect']['parent::name'] == {'state': 'absent'}
    assert result.data['steps'][0]['dependencies'] and result.data['merge_mode'] == 'atomic'
    effects = result.data['steps'][0]['patch']
    assert any(change['path'] == ['name'] and change['value'] == 'Main' for change in effects)
    assert any(change['path'] == ['slug'] and change['value'] == 'main' for change in effects)
    assert any(change['path'] == ['config', 'output'] and change['value'] == DEFAULT_OUTPUT for change in effects)
    assert result.receipt.result['canonical_document'] == document


def test_remote_create_empty_generates_ulid_when_no_id_given(monkeypatch, tmp_path) -> None:
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(project="render-smoke")
    assert result.ok, result.error
    timeline_id = result.data['timeline_id']
    assert is_ulid(timeline_id)
    assert writer.calls[0][1] == ('render-smoke', timeline_id)
    assert writer.calls[1][1][1] == timeline_id
    assert writer.calls[1][2]['idempotency_key'] == f'{result.idempotency_key}-head'
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {
        'tracks': [], 'clips': [], 'output': DEFAULT_OUTPUT}
    assert result.data['canonical_document']['parent_revision']['payload']['name'] == 'Main'
    assert result.data['canonical_document']['parent_revision']['payload']['slug'] == 'main'


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
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {
        **config, 'clips': [], 'output': {**DEFAULT_OUTPUT, 'resolution': '1920x1080'}}
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
        draft = next((tmp_path / status / 'timeline-outbox').glob('*.json'))
        state = json.loads(draft.read_text())
        assert state['pending'] and state['flight'] and state['conflict']['details'] == details


@pytest.mark.parametrize('name,slug', [('Main', 'main'), ('Second Cut', 'second-cut')])
def test_remote_create_empty_authors_canonical_name_and_custom_canvas(monkeypatch, tmp_path, name, slug):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    config = {'tracks': [], 'theme_overrides': {'visual': {'canvas': {
        'width': 640, 'height': 360, 'fps': 24}}}, 'meta': {'org.example': {'raw': [None, False, 0]}}}
    original = copy.deepcopy(config)
    result = RemoteTimelines(writer).create_empty(
        project='render-smoke', timeline_id='film', name=name, config=config, idempotency_key='custom')
    assert result.ok, result.error
    payload = result.data['canonical_document']['parent_revision']['payload']
    assert payload['name'] == name and payload['slug'] == slug
    assert payload['config'] == {**config, 'clips': [], 'output': {
        **DEFAULT_OUTPUT, 'resolution': '640x360', 'fps': 24}}
    assert payload['config']['output']['background'] is None
    assert payload['config']['output']['background_scale'] is None
    assert config == original
    assert writer.documents['H-1']['parent_revision']['payload'] == payload
    assert result.receipt.result['canonical_document']['parent_revision']['payload'] == payload


def test_remote_create_empty_preserves_explicit_output_and_nulls(monkeypatch, tmp_path):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    output = {**DEFAULT_OUTPUT, 'resolution': '640x360', 'fps': 24, 'file': 'custom.mp4',
              'background': '#123456', 'background_scale': None}
    config = {'tracks': [], 'output': output, 'opaque': [None, False, 0]}
    result = RemoteTimelines(writer).create_empty(project='render-smoke', config=config)
    assert result.ok, result.error
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {**config, 'clips': []}


@pytest.mark.parametrize('config', [
    {'tracks': [], 'theme_overrides': None},
    {'tracks': [], 'theme_overrides': {'visual': None}},
])
def test_remote_create_empty_preserves_null_theme_config(monkeypatch, tmp_path, config):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(project='render-smoke', config=config)
    assert result.ok, result.error
    assert result.data['canonical_document']['parent_revision']['payload']['config'] == {
        **config, 'clips': [], 'output': DEFAULT_OUTPUT}


def test_remote_create_empty_requires_runtime_bootstrap_pair(monkeypatch, tmp_path):
    class Headless(_Writer):
        def create_timeline(self, *args, **kwargs):
            shell = super().create_timeline(*args, **kwargs)
            shell['data']['head_publication_id'] = None
            return shell

    writer = Headless()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(project='render-smoke')
    assert not result.ok and result.error.code == 'protocol_error'
    assert [call[0] for call in writer.calls] == ['create_timeline']
    assert writer.replays == {}


@pytest.mark.parametrize('field,value', [('name', None), ('opaque', {'raw': [None, False]})])
def test_remote_create_empty_never_initializes_nonpristine_payload(monkeypatch, tmp_path, field, value):
    class Nonpristine(_Writer):
        def create_timeline(self, *args, **kwargs):
            from astrid.sdk.timeline.commit import _digest

            shell = super().create_timeline(*args, **kwargs)
            parent = self.documents['bootstrap']['parent_revision']
            parent['payload'][field] = value
            parent['content_digest'] = _digest(parent['payload'])
            return shell

    writer = Nonpristine()
    _mount(monkeypatch, tmp_path, writer)
    result = RemoteTimelines(writer).create_empty(project='render-smoke')
    assert not result.ok and 'pristine' in result.error.message
    assert writer.documents['bootstrap']['parent_revision']['payload'][field] == value
    assert [call[0] for call in writer.calls] == ['create_timeline']
    assert writer.replays == {}


@pytest.mark.parametrize('lost_ack', [False, True])
@pytest.mark.parametrize('later', ['edit', 'undo'])
def test_remote_create_empty_exact_retry_never_overwrites_later_head(monkeypatch, tmp_path, lost_ack, later):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    writer.lose_ack = lost_ack
    first = RemoteTimelines(writer).create_empty(
        project='render-smoke', timeline_id='film', config=DEFAULT_CONFIG, idempotency_key='retry')
    assert first.ok is not lost_ack
    original_call = copy.deepcopy(writer.calls[-1])
    original_reply = copy.deepcopy(writer.replays['retry-head'][1])
    # Simulated later state is only a transport control; provider/history
    # authority is exercised separately by the real Runtime positive below.
    document = copy.deepcopy(writer.documents['bootstrap' if later == 'undo' else 'H-1'])
    if later == 'edit':
        document['parent_revision']['payload']['name'] = 'Later edit'
    writer.documents['later'] = document
    writer.head = {'revision_id': 'later', 'publication_id': 'later-publication'}
    before = copy.deepcopy((writer.documents, writer.head))
    result = RemoteTimelines(writer).create_empty(
        project='render-smoke', timeline_id='film', config=DEFAULT_CONFIG, idempotency_key='retry')
    assert result.ok, result.error
    assert writer.calls[-1] == original_call
    assert result.receipt.as_dict() == original_reply['receipt']
    assert result.data['canonical_document'] == original_reply['data']['canonical_document']
    assert (writer.documents, writer.head) == before


def test_remote_create_empty_changed_retry_preserves_original_flight(monkeypatch, tmp_path):
    writer = _Writer()
    _mount(monkeypatch, tmp_path, writer)
    writer.lose_ack = True
    assert not RemoteTimelines(writer).create_empty(
        project='render-smoke', timeline_id='film', config=DEFAULT_CONFIG, idempotency_key='retry').ok
    path = next((tmp_path / 'timeline-outbox').glob('*.json'))
    draft, calls = path.read_bytes(), len(writer.calls)
    result = RemoteTimelines(writer).create_empty(
        project='render-smoke', timeline_id='film', config={'tracks': []}, idempotency_key='retry')
    assert not result.ok and 'pending intent differs' in result.error.message
    assert path.read_bytes() == draft and len(writer.calls) == calls + 1


@pytest.mark.integration
@pytest.mark.parametrize('config', [None, DEFAULT_CONFIG, {
    'tracks': [], 'theme_overrides': {'visual': {'canvas': {'width': 640, 'height': 360, 'fps': 24}}},
    'meta': {'org.example': {'raw': [None, False, 0]}},
}])
def test_remote_create_empty_real_runtime_bootstrap_acceptance(monkeypatch, tmp_path, config):
    """Expected positive at the actual provider/document boundary; no fake authority."""
    from astrid.sdk import storage_root
    from astrid.sdk.timeline import commit, store
    from tests.helpers.runtime import use_runtime

    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_baseline import empty_bootstrap_document
    from runtime_protocol.timeline_commit_port import route_path

    RealmStore.initialize(tmp_path / 'realm').close()
    service = RuntimeService(tmp_path / 'realm')
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({'slug': 'bootstrap', 'name': 'Bootstrap'})['id']

    class ServiceTransport:
        _last_handshake = {'realm_id': service.realm['id'], 'actor_id': 'author'}

        def __init__(self):
            self.calls = []

        def __getattr__(self, operation):
            return getattr(service, operation)

        def create_timeline(self, *args, **kwargs):
            return service.create_timeline(*args, **kwargs)

        def list_timelines(self, *args, **kwargs):
            page = service.list_timelines(*args, **kwargs)
            return page['items'], page['next_cursor']

        def get_project_parent_composition_revision(self, *args):
            return service.get_project_parent_composition_revision(*args)

        def commit_timeline(self, project, timeline, body, *, idempotency_key):
            self.calls.append((copy.deepcopy(body), idempotency_key))
            try:
                return service.commit_timeline(
                    project, timeline, body, idempotency_key=idempotency_key,
                    publisher='author', invocation_path=route_path(project, timeline), authorize=lambda: None)
            except RuntimeErrorBase as exc:
                raise WorkspaceClientError(exc.status, exc.code, exc.message, exc.details or {}) from exc

    def resolve(project, timeline, **kwargs):
        row = service.get_project_timeline(project, timeline)
        return row['project_id'], row['timeline_id'], row['head_revision_id']

    monkeypatch.setattr(storage_root, 'resolve_runtime_data_root', lambda: tmp_path / 'outbox')
    monkeypatch.setattr(store, 'resolve_ids', resolve)
    transport = ServiceTransport()
    try:
        result = RemoteTimelines(transport).create_empty(
            project=project, timeline_id='film', name='Main', config=config, idempotency_key='create')
        assert transport.calls, result.error
        shell = service.create_timeline(project, 'film', name='Main', idempotency_key='create-shell')
        body, key = transport.calls[0]
        revision = shell['data']['head_revision_id']
        assert (body['base_revision_id'], body['base_publication_id']) == (
            revision, shell['data']['head_publication_id'])
        bootstrap = service.get_project_parent_composition_revision(project, 'film', revision)
        assert bootstrap['payload'] == empty_bootstrap_document(project, 'film', revision)['parent_revision']['payload']
        assert key == 'create-head' and body['commands'][0]['op'] == 'timeline.init'
        assert body['label'] == 'Create empty timeline' and body['merge'] == 'atomic'
        assert body['steps'][0]['reads'] == [{'kind': 'scope', 'ref': 'timeline', 'path': []}]
        assert result.ok, result.error
        payload = result.data['canonical_document']['parent_revision']['payload']
        assert payload['name'] == 'Main' and payload['slug'] == 'main'
        canvas = (config or {}).get('theme_overrides', {}).get('visual', {}).get('canvas', {})
        assert payload['config'] == {**(config or {'tracks': []}), 'clips': [], 'output': {
            **DEFAULT_OUTPUT, 'resolution': f"{canvas.get('width', 1280)}x{canvas.get('height', 720)}",
            'fps': canvas.get('fps', 30)}}
        assert result.receipt.result['canonical_document']['parent_revision']['payload'] == payload
        assert service.get_project_parent_composition_revision(
            project, 'film', result.data['head_revision_id'])['payload'] == payload
        assert result.data['steps'][0]['patch'] and result.data['steps'][0]['dependencies']
        assert RemoteTimelines(transport).create_empty(
            project=project, timeline_id='film', name='Main', config=config,
            idempotency_key='create').receipt == result.receipt
        assert transport.calls[-1] == transport.calls[0]
        # A retained initialization receipt must also replay after undo has
        # returned to equal bootstrap bytes under a later publication.
        accepted_head = service.get_project_timeline(project, 'film')
        undone = service.commit_timeline(project, 'film', {
            'api_version': 1, 'project_id': project, 'timeline_id': 'film',
            'base_revision_id': accepted_head['head_revision_id'],
            'base_publication_id': accepted_head['head_publication_id'],
            'commands': [{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                          'select': None, 'args': {'publications': [result.receipt.receipt_id]}}],
            'dry_run': False,
        }, idempotency_key='undo', publisher='author', invocation_path=route_path(project, 'film'),
            authorize=lambda: None)
        assert undone['data']['canonical_document']['parent_revision']['payload'] == bootstrap['payload']
        retired = service.get_project_timeline(project, 'film')
        replayed = RemoteTimelines(transport).create_empty(
            project=project, timeline_id='film', name='Main', config=config, idempotency_key='create')
        assert replayed.ok and replayed.receipt == result.receipt
        assert transport.calls[-1] == transport.calls[0]
        assert service.get_project_timeline(project, 'film') == retired
    finally:
        service.close()
