"""Synthetic settlement -> captured output -> atomic acceptance. No live media."""
import copy
import json
import threading
from urllib.parse import urlencode

import pytest

from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import AuthorizationError, ConflictError, NotFoundError, ValidationError
from runtime_protocol.server import RuntimeHTTPServer, RuntimeHandler
from runtime_protocol.util import MANAGED_OUTPUT_ASSOCIATION_KEY as KEY
from packages.python.banodoco_workspace_client.generated import WorkspaceClient
from http_helpers import Api
from test_generation_publish_v1_settlement import _fixture, _effect, _output, _settle
from test_selected_media_commit import mutate, snapshot, request_for, prepare
from test_shot_composition_runtime import _publication
from test_timeline_accept import IDENTITY


def effect(project):
    return _effect(project, groups=[{'group_key': 'main', 'selectors': [
        {'selector': 'first', 'ordinal': 0, 'variant_key': 'first', 'output_port': 'video'},
        {'selector': 'second', 'ordinal': 1, 'variant_key': 'second', 'output_port': 'video'},
    ]}])


def outputs():
    return [_output(b'synthetic video', output_port='video', group_key='main', variant_key=key,
                    ordinal=i, media_type='video/mp4', filename='synthetic.mp4', duration_seconds=2.5)
            for i, key in enumerate(('first', 'second'))] + [
        _output(b'preview', output_port='preview', group_key='aux', variant_key='preview', ordinal=0)]


@pytest.fixture
def settled(tmp_path):
    s, project, task, attempt, declared = _fixture(tmp_path, effect_factory=effect)
    try:
        s.publish_parent_composition(project['id'], 'main', _publication(project['id']), idempotency_key='initial')
        result = _settle(s, attempt, outputs(), effect=declared)
        associations = {a['variant_key']: a for a in s.managed_outputs(task['task']['id'])}
        yield s, project['id'], associations, task, attempt, declared, result
    finally:
        s.close()


def capture(s, p, a):
    return s.get_project_media_selection(p, association_id=a['association_id'],
                                        object_id=a['object_id'], version=a['lifecycle']['version'])


def test_exact_settlement_binding_same_bytes_distinct_variants_and_retry(settled):
    s, p, a, task, attempt, declared, result = settled
    before = snapshot(s)
    first, second = [capture(s, p, a[key]) for key in ('first', 'second')]
    assert set(first) == {'asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'}
    assert first['asset'] == first['variant_id'] != second['asset'] == second['variant_id']
    assert first['object_id'] == second['object_id']
    assert first['catalog_digest'] != second['catalog_digest']
    for key, selected in [('first', first), ('second', second)]:
        assert s.get_variant(selected['variant_id'])['metadata'][KEY] == a[key]['association_id']
    assert s.store.conn.total_changes > 0
    assert snapshot(s) == before  # GET is read-only.
    assert _settle(s, attempt, outputs(), effect=declared) == result
    mutate(s, 'UPDATE generation_variants SET metadata_json=json_set(metadata_json,\'$.is_primary\',0)')
    assert capture(s, p, a['first']) == first
    request = request_for(p, first)
    port = s._request_commit_port(request, IDENTITY)
    record = port.selected_media(first)
    assert set(record) == {'realm_id', 'project_id', *first, 'generation', 'variant', 'entry'}
    assert record['entry']['duration_seconds'] == 2.5
    prepared = prepare(s, p, request)
    accepted = port.accept(prepared)
    mutate(s, "UPDATE managed_output_lifecycle SET state='reclaimed',version=version+1")
    before = snapshot(s)
    assert port.accept(prepared)['stored_result'] == accepted['stored_result']
    assert s.commit_timeline(p, 'main', request, idempotency_key=request['request_id'], identity=IDENTITY) == accepted['stored_result']
    assert snapshot(s) == before
    changed = copy.deepcopy(request)
    changed['change']['commands'][0]['args']['at'] = 9
    with pytest.raises(ConflictError):
        s.commit_timeline(p, 'main', changed, idempotency_key=request['request_id'], identity=IDENTITY)


@pytest.mark.parametrize('sql', [
    'DELETE FROM managed_output_lifecycle',
    'DELETE FROM managed_output_associations',
    "UPDATE managed_output_lifecycle SET state='expired',version=version+1",
    'UPDATE managed_output_lifecycle SET version=version+1',
    "UPDATE managed_output_associations SET generation_id=NULL",
    "UPDATE managed_output_associations SET project_id='foreign'",
    "UPDATE managed_output_associations SET object_digest=(SELECT digest FROM objects WHERE digest != managed_output_associations.object_digest LIMIT 1)",
    "UPDATE generation_variants SET metadata_json=json_remove(metadata_json,'$." + KEY + "')",
    "UPDATE generation_variants SET metadata_json=json_set(metadata_json,'$.duration_seconds',3)",
    "UPDATE generations SET status='failed'",
    "UPDATE tasks SET status='failed'",
    'UPDATE attempts SET settled=0',
    'UPDATE attempts SET fence=fence+1',
    "UPDATE tasks SET capability='mutated-capability'",
    'DELETE FROM project_objects',
])
def test_changed_or_revoked_identity_refuses_first_acceptance_atomically(settled, sql):
    s, p, a, *_ = settled
    selected = capture(s, p, a['first'])
    request = request_for(p, selected)
    port = s._request_commit_port(request, IDENTITY)
    port.selected_media(selected)
    prepared = prepare(s, p, request)
    if "project_id='foreign'" in sql:
        other = s.create_project({'slug': 'foreign', 'name': 'Foreign'}, idempotency_key='foreign')['id']
        mutate(s, 'UPDATE managed_output_associations SET project_id=?', (other,))
    else:
        mutate(s, sql)
    before = snapshot(s)
    with pytest.raises((ConflictError, NotFoundError, ValidationError)):
        port.accept(prepared)
    assert snapshot(s) == before


def test_exact_tuple_refusals_unregistered_ambiguous_and_missing_duration(settled):
    s, p, a, *_ = settled
    other = s.create_project({'slug': 'other', 'name': 'Other'}, idempotency_key='other')['id']
    for project, association, obj, version, error in [
        (other, a['first']['association_id'], a['first']['object_id'], 1, NotFoundError),
        (p, 'missing', a['first']['object_id'], 1, NotFoundError),
        (p, a['first']['association_id'], 'sha256:' + '0' * 64, 1, ConflictError),
        (p, a['first']['association_id'], a['first']['object_id'], 2, ConflictError),
        (p, a['preview']['association_id'], a['preview']['object_id'], 1, NotFoundError),
    ]:
        before = snapshot(s)
        with pytest.raises(error):
            s.get_project_media_selection(project, association_id=association, object_id=obj, version=version)
        assert snapshot(s) == before
    first, second = [capture(s, p, a[key]) for key in ('first', 'second')]
    mutate(s, 'UPDATE generation_variants SET metadata_json=json_set(metadata_json,?,?) WHERE id=?',
           ('$.' + KEY, a['first']['association_id'], second['variant_id']))
    with pytest.raises(ConflictError, match='ambiguous'):
        capture(s, p, a['first'])
    mutate(s, 'DELETE FROM generation_variants WHERE id=?', (second['variant_id'],))
    mutate(s, "UPDATE generation_variants SET metadata_json=json_remove(metadata_json,'$.duration_seconds')")
    with pytest.raises(ValidationError, match='metadata'):
        capture(s, p, a['first'])


@pytest.mark.parametrize('location', ['effect', 'output', 'provenance', 'producer'])
def test_reserved_field_refused_without_partial_publication(tmp_path, location):
    s, p, task, attempt, declared = _fixture(tmp_path, effect_factory=effect)
    try:
        before = snapshot(s)
        if location == 'effect':
            bad = effect(p['id'])
            bad['payload']['metadata'][KEY] = 'forged'
            with pytest.raises(ValidationError, match='Runtime-owned'):
                s.create_task({'capability_id': 'generation.publish.v1', 'project': p['id'],
                               'settlement_effect': bad, 'idempotency_key': 'forged'})
        else:
            values = outputs()
            if location == 'output':
                values[0][KEY] = 'forged'
            else:
                values[0][location] = {KEY: 'forged'}
            with pytest.raises(ValidationError, match='Runtime-owned'):
                _settle(s, attempt, values, effect=declared)
        assert snapshot(s) == before
    finally:
        s.close()


def test_binding_write_rolls_back_with_settlement_failure(tmp_path, monkeypatch):
    s, p, task, attempt, declared = _fixture(tmp_path, effect_factory=effect)
    original = s.store._associate_managed_outputs
    def fail(*args, **kwargs):
        associations = original(*args, **kwargs)
        assert s.store.conn.in_transaction
        assert s.store.conn.execute('SELECT COUNT(*) FROM generation_variants WHERE metadata_json LIKE ?',
                                    ('%' + KEY + '%',)).fetchone()[0] == 2
        raise ConflictError('injected post-binding failure')
    monkeypatch.setattr(s.store, '_associate_managed_outputs', fail)
    try:
        before = snapshot(s)
        with pytest.raises(ConflictError, match='post-binding'):
            _settle(s, attempt, outputs(), effect=declared)
        assert snapshot(s) == before
        monkeypatch.setattr(s.store, '_associate_managed_outputs', original)
        _settle(s, attempt, outputs(), effect=declared)
        a = next(a for a in s.managed_outputs(task['task']['id']) if a['variant_key'] == 'first')
        capture(s, p['id'], a)
    finally:
        s.close()


def test_authenticated_output_endpoint_and_generated_python_client(settled, tmp_path):
    s, p, a, *_ = settled
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('reader', ['projects:read'])
    server = RuntimeHTTPServer(('127.0.0.1', 0), RuntimeHandler)
    server.runtime, server.credentials = s, credentials
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    selectors = dict(association_id=a['first']['association_id'], object_id=a['first']['object_id'], version=1)
    try:
        client = WorkspaceClient(base, token)
        expected = capture(s, p, a['first'])
        assert client.get_project_media_selection_for_output(p, **selectors) == expected
        for query in [
            urlencode({**selectors, 'asset': 'forged'}),
            urlencode(selectors) + '&version=1',
            *[urlencode({**selectors, 'version': v}) for v in ('0', '-1', '1.0', 'true', '')],
            urlencode({k: v for k, v in selectors.items() if k != 'object_id'}),
        ]:
            with pytest.raises(RuntimeError) as exc:
                Api(base, token).request('GET', f'/v1/projects/{p}/media-selection?' + query)
            assert exc.value.status == 400
        with pytest.raises(RuntimeError) as exc:
            Api(base, None).request('GET', f'/v1/projects/{p}/media-selection?' + urlencode(selectors))
        assert exc.value.status == 401
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=5)
        assert not thread.is_alive()


def test_create_append_and_thumbnail_attach_bind_only_exact_creative_output(tmp_path):
    from test_generation_thumbnail_settlement import _create_effect, _thumbnail
    s, project, task, attempt, declared = _fixture(tmp_path, effect_factory=_create_effect, with_input=True)
    p = project['id']
    try:
        video = _output(b'legacy creative', name='video', output_port='video', group_key='default',
                        variant_key='0', ordinal=0, media_type='video/mp4', duration_seconds=2.5)
        thumbnail = _thumbnail(b'legacy thumbnail', [video['digest']])
        first = _settle(s, attempt, [video, thumbnail], effect=declared)
        initial = first['data']['result']['generation_variant']
        associations = s.managed_outputs(task['task']['id'])
        selected = capture(s, p, next(a for a in associations if a['role'] != 'thumbnail'))
        assert selected['variant_id'] == initial['variant_id']
        with pytest.raises(ConflictError, match='creative'):
            capture(s, p, next(a for a in associations if a['role'] == 'thumbnail'))
        assert len(s.list_variants(initial['generation_id'])['items']) == 1
        append = dict(effect_type='generation.variant.append', target_id=initial['generation_id'], expected_version=1,
                      payload=dict(source_variant_id=initial['variant_id'], source_object_id=video['digest'],
                                   variant_type='new-video', output_name='video', output_ordinal=0, primary_policy='promote'))
        second_task = s.create_task(dict(capability_id='generation.publish.v1', project=p,
            input_object_ids=[video['digest']], settlement_effect=append, idempotency_key='append'), _host_owned=True)
        second_attempt = s.claim_next(dict(executor_id='publish-worker', capability_ids=['generation.publish.v1'],
                                          runtime_epoch=s.health()['runtime_epoch']), idempotency_key='append-claim')
        new_video = dict(video)  # Same bytes, distinct variant identity.
        _settle(s, second_attempt, [new_video, thumbnail], effect=append, key='append-settle')
        new_associations = s.managed_outputs(second_task['task']['id'])
        new_selection = capture(s, p, next(a for a in new_associations if a['role'] != 'thumbnail'))
        assert new_selection['object_id'] == selected['object_id']
        assert new_selection['variant_id'] != selected['variant_id']
        # Primary changes must never select the new variant on retry.
        assert capture(s, p, next(a for a in associations if a['role'] != 'thumbnail')) == selected
        bound = {v['metadata'][KEY] for v in s.list_variants(initial['generation_id'])['items']}
        assert bound == {a['association_id'] for a in associations + new_associations if a['role'] != 'thumbnail'}
    finally:
        s.close()


def test_binding_recheck_occurs_inside_atomic_acceptance(settled, monkeypatch):
    s, p, a, *_ = settled
    selected = capture(s, p, a['first'])
    request = request_for(p, selected)
    port = s._request_commit_port(request, IDENTITY)
    port.selected_media(selected)
    prepared = prepare(s, p, request)
    original = s._output_selection_binding
    calls = []
    def checked(*args):
        calls.append(s.store.conn.in_transaction)
        return original(*args)
    monkeypatch.setattr(s, '_output_selection_binding', checked)
    assert port.accept(prepared)['outcome'] == 'accepted'
    assert calls == [True]
