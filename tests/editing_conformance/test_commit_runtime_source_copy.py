"""D17 semantics through the staged Runtime source-authority port."""
from __future__ import annotations

import copy

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.fixture
def source_copy(tmp_path):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({'slug': 'copy', 'name': 'Copy'})['id']
    service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    for timeline in ('source', 'destination'):
        service.create_timeline(project, timeline, idempotency_key='create-' + timeline)

    def document(timeline):
        head = service.get_project_timeline(project, timeline)
        return service._timeline_commits()[0].revision_closure(project, timeline, head['head_revision_id'])

    def request(timeline, calls):
        head = service.get_project_timeline(project, timeline)
        return {'api_version': 1, 'project_id': project, 'timeline_id': timeline,
                'base_revision_id': head['head_revision_id'], 'base_publication_id': head['head_publication_id'],
                'commands': calls, 'label': 'Copy source', 'merge': 'atomic', 'reads': [],
                'steps': [{'id': 'copy', 'label': 'Copy source', 'intent': 'Keep full source',
                           'tags': ['copy'], 'command_ordinals': list(range(len(calls))), 'patch': [], 'reads': []}],
                'dry_run': False, 'source': {'via': 'python'}, 'rationale': 'D17', 'group_id': 'copy'}

    def commit(timeline, body, key):
        return service.commit_timeline(project, timeline, body, idempotency_key=key, publisher='editor',
            invocation_path=f'/v1/projects/{project}/timelines/{timeline}/commit', authorize=lambda: None)

    from astrid.sdk.timeline.capture import capture_track_create
    bundle = bundle_from_document(document('source'))
    commit('source', request('source', [capture_track_create(bundle, 'parent', {'id': 'picture', 'kind': 'visual'})]), 'track')
    bundle = bundle_from_document(document('source'))
    commit('source', request('source', [capture_occurrence_create(bundle, 'one', 'shared', name='Shared',
        track='picture', on=0, duration=10)]), 'shot')
    source = document('source')
    head = service.get_project_timeline(project, 'source')
    command = {'schema_version': 1, 'op': 'timeline.duplicate', 'version': '1', 'select': 'parent',
               'args': {'source_ref': {'project_id': project, 'timeline_id': 'source',
                        'revision_id': head['head_revision_id'], 'publication_id': head['head_publication_id'],
                        'content_digest': source['parent_revision']['content_digest']},
                        'shots': {'shared': 'copied'}, 'occurrences': {'one': 'copy-one'}}}
    command['created'] = ['shot:copied', 'occurrence:copy-one']
    try:
        yield service, document, request, commit, command
    finally:
        service.close()


def test_source_copy_real_port_receipts_preview_undo_redo(source_copy):
    service, document, request, commit, command = source_copy
    before, source = document('destination'), document('source')
    body = request('destination', [command])
    preview = commit('destination', {**body, 'dry_run': True}, 'preview')
    assert preview['receipt'] is None and preview['data']['would_status'] == 'accepted'
    assert document('destination') == before
    result = commit('destination', body, 'copy')
    after = document('destination')
    rows = after['parent_revision']['payload']['occurrences']
    assert [row['occurrence_id'] for row in rows] == ['copy-one']
    assert {row['shot_id'] for row in rows} == {'copied'}
    assert len({row['shot_revision_id'] for row in rows}) == 1
    assert rows[0]['placement']['start_ms'] == 0
    assert len(after['shot_revisions']) == len(after['internal_timeline_revisions']) == 1
    assert document('source') == source
    assert commit('destination', body, 'copy') == result
    assert result['data']['steps'][0]['patch']
    record = service.list_timeline_commits(after['project_id'], 'destination', authorize=lambda: None)['items'][-1]['records']['commands'][0]
    assert {item['ref'] for item in record['created']} == {'shot:copied', 'occurrence:copy-one'}
    def inverse(accepted, key):
        call = {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
                'args': {'publications': [accepted['receipt']['receipt_id']]}}
        return commit('destination', request('destination', [call]), key)
    undo = inverse(result, 'undo')
    assert document('destination') == before
    inverse(undo, 'redo')
    assert document('destination') == after


@pytest.mark.parametrize('damage', ['foreign', 'outside', 'pair', 'digest', 'same', 'occupied', 'sharing', 'order', 'media', 'created', 'archived'])
def test_source_copy_refuses_bad_authority_or_claims_without_writes(source_copy, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    service, document, request, commit, command = source_copy
    call = copy.deepcopy(command)
    args, ref = call['args'], call['args']['source_ref']
    if damage == 'foreign':
        ref['project_id'] = 'foreign'
    elif damage == 'outside':
        ref['timeline_id'] = 'outside'
    elif damage == 'pair':
        ref['publication_id'] = 'wrong'
    elif damage == 'digest':
        ref['content_digest'] = 'sha256:' + '0' * 64
    elif damage == 'same':
        ref['timeline_id'] = 'destination'
    elif damage == 'occupied':
        args['shots']['shared'] = 'shared'
    elif damage == 'sharing':
        args['shots']['unrequested'] = 'extra'
    elif damage == 'order':
        args['occurrences']['two'] = 'copy-one'
    elif damage == 'media':
        args['media'] = [{'media_id': 'sha256:' + 'f' * 64}]
    elif damage == 'archived':
        row = service.get_project_timeline(ref['project_id'], 'source')
        service.archive_timeline('source', {'expected_version': row['version']}, idempotency_key='archive')
    else:
        call['created'] = ['shot:forged']
    before = document('destination')
    history = service.list_timeline_commits(before['project_id'], 'destination', authorize=lambda: None)
    with pytest.raises(RuntimeErrorBase):
        commit('destination', request('destination', [call]), damage)
    assert document('destination') == before
    assert service.list_timeline_commits(before['project_id'], 'destination', authorize=lambda: None) == history


def test_production_duplicate_caller_uses_authenticated_semantic_and_archives_failures(source_copy, tmp_path, monkeypatch):
    from types import SimpleNamespace

    from astrid.sdk.contracts import DomainResult
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline_duplicate import duplicate_timeline
    from tests.sdk.test_timeline_sync import bundle_connection

    service, document, request, commit, command = source_copy
    project = command['args']['source_ref']['project_id']
    client, generated = bundle_connection(tmp_path, monkeypatch, bundle_from_document(document('destination')))
    client._remote._transport._last_handshake = {'realm_id': service.realm['id'], 'actor_id': 'editor'}
    client.timelines._resolve_timeline = lambda p, t: DomainResult.success({'project_id': project, 'timeline_id': t})
    client.timelines.open_bundle = lambda p, t, revision_id=None: DomainResult.success({'bundle': bundle_from_document(
        service._timeline_commits()[0].revision_closure(project, t,
            revision_id or service.get_project_timeline(project, t)['head_revision_id']))})
    generated.list_timeline_commits = lambda p, t, cursor=None, limit=200: service.list_timeline_commits(
        project, t, cursor=cursor, limit=limit, authorize=lambda: None)
    bodies = []
    def send(p, t, body, *, idempotency_key):
        bodies.append(copy.deepcopy(body))
        return commit(t, body, idempotency_key)
    generated.commit_timeline = send
    client.timelines.create_empty = lambda **kw: SimpleNamespace(ok=True, data={'timeline_id': 'destination'})
    archived = []
    client.timelines.archive = lambda p, t: archived.append(t) or SimpleNamespace(ok=True)
    result = duplicate_timeline(project, 'source', slug='destination', client=client)
    assert result['timeline_id'] == 'destination' and result['shots'] == 1
    assert [call['op'] for call in bodies[0]['commands']] == ['timeline.duplicate']
    assert bodies[0]['commands'][0]['args']['source_ref'] == command['args']['source_ref']
    assert document('source')['parent_revision']['revision_id'] == command['args']['source_ref']['revision_id']
    assert archived == []

    # The failed destination publication is cleaned up by the same production wrapper.
    from astrid.sdk.timeline._common import TimelineEditError
    with pytest.raises(TimelineEditError, match='archived again'):
        duplicate_timeline(project, 'source', slug='destination', client=client)
    assert archived == ['destination']


def test_source_copy_rejects_project_wide_occupied_shot_without_writes(source_copy):
    from runtime_protocol.errors import RuntimeErrorBase

    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    service, document, request, commit, command = source_copy
    # Advance the source after capturing its exact historical pair. The new
    # shot reserves the proposed destination identity project-wide.
    bundle = bundle_from_document(document('source'))
    born = capture_occurrence_create(bundle, 'occupied-owner', 'copied', name='Occupied',
                                    track='picture', on=20, duration=1)
    commit('source', request('source', [born]), 'occupied-shot')
    before = document('destination')
    service.list_timeline_commits(before['project_id'], 'destination', authorize=lambda: None)
    rows = tuple(service.store.conn.iterdump())
    with pytest.raises(RuntimeErrorBase):
        commit('destination', request('destination', [command]), 'copy-occupied')
    assert document('destination') == before
    assert tuple(service.store.conn.iterdump()) == rows
