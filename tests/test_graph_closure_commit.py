"""Request-owned immutable closure reads and the atomic acceptance fence."""
import copy
import json

import pytest

from runtime_protocol.errors import AuthorizationError, ConflictError, NotFoundError, ValidationError
from runtime_protocol.timeline_commit import digest
from test_timeline_accept import IDENTITY, acceptance, fixture, wire  # noqa: F401
from test_selected_media_commit import mutate, snapshot


def restore_request(s, p, *, revision='parent-1', known=True, key='restore-image'):
    head = s.head(p, 'main')
    selected = s.get_project_parent_composition_revision(p, 'main', revision)
    args = dict(revision_id=revision, content_digest=selected['content_digest'])
    if known:
        args['publication_id'] = next(row['publication_id'] for row in
            s.list_project_parent_composition_revisions(p, 'main')['items'] if row['revision_id'] == revision)
    elif known is None:
        args['publication_id'] = None
    request = wire(p, key=key)
    request.update(base_revision_id=head['revision_id'], base_publication_id=head['publication_id'])
    request['scope']['complete'] = ['clips', 'tracks']
    request['change']['commands'] = [dict(op='timeline.restore', select=None, args=args)]
    return request


def restore_prepared(s, p, request, closure):
    value = acceptance(s, p, request=request)
    value['expected_head_revision_id'] = request['base_revision_id']
    value['publication'] = dict(parent_composition=copy.deepcopy(closure['parent_revision']['payload']),
        shot_revisions=[{k: copy.deepcopy(row[k]) for k in
            ('shot_id', 'revision_id', 'internal_timeline_revision_id', 'content_digest', 'payload')}
            for row in closure['shot_revisions']],
        internal_timeline_revisions=[{k: copy.deepcopy(row[k]) for k in
            ('timeline_id', 'revision_id', 'content_digest', 'payload')}
            for row in closure['internal_timeline_revisions']])
    value['result'].update(canonical_document=copy.deepcopy(closure['parent_revision']['payload']),
                           document_digest=closure['parent_revision']['content_digest'], rebased_onto=None)
    value['evidence']['commands'] = copy.deepcopy(request['change']['commands'])
    value['result']['change']['commands'] = copy.deepcopy(request['change']['commands'])
    value['evidence']['digests']['after'] = value['result']['document_digest']
    value['restore'] = dict(request['change']['commands'][0]['args'],
                           expected_publication_id=request['base_publication_id'])
    return value


@pytest.mark.parametrize('known', [True, False, None])
def test_restore_complete_historical_image_manifest_and_provenance(fixture, known):
    from test_shot_composition_runtime import _publication
    s, p = fixture
    media = s.ingest(p, b'manifest-only', media_type='audio/wav', original_name='tone.wav', idempotency_key='media')['data']['object_id']
    body = _publication(p, expected_head='parent-1', parent_revision_id='historical')
    body['parent_composition']['config'] = {'opaque': {'source': 'external:unparsed/identity', 'provenance': None}}
    body['dependency_manifest'] = {'media': [media]}
    s.publish_parent_composition(p, 'main', body, idempotency_key='historical')
    s.accept(acceptance(s, p, key='advance'), identity=IDENTITY)
    request = restore_request(s, p, revision='historical', known=known)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure('historical')
    # General publications are available only on this restore-bound port.
    rows = port.revisions({'limit': 1})
    assert rows[0]['revision_id'] == request['base_revision_id']
    rows = port.revisions({'limit': 1, 'before': rows[0]['publication_id']})
    assert rows[0]['revision_id'] == 'historical'
    with pytest.raises(NotFoundError):
        port.revisions({'before': 'unknown-publication'})
    before_count = s.store.conn.execute('SELECT count(*) FROM parent_composition_publications').fetchone()[0]
    value = restore_prepared(s, p, request, closure)
    result = port.accept(value)
    restored = port.revision_closure(result['revision_id'])
    assert restored['parent_revision']['payload'] == closure['parent_revision']['payload']
    assert restored['parent_revision']['content_digest'] == closure['parent_revision']['content_digest']
    assert restored['shot_revisions'] == closure['shot_revisions']
    assert restored['internal_timeline_revisions'] == closure['internal_timeline_revisions']
    assert s.store.conn.execute('SELECT count(*) FROM parent_composition_publications').fetchone()[0] == before_count + 1
    assert s.store.conn.execute("SELECT dependency_id FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_kind='media'", (result['revision_id'],)).fetchone()[0] == media
    row = s.list_project_parent_composition_revisions(p, 'main')['items'][0]
    assert row['restored_from_revision_id'] == 'historical'
    assert row['previous_revision_id'] == request['base_revision_id']
    assert row['previous_publication_id'] == request['base_publication_id']
    assert row['provenance']['publisher'] == IDENTITY['actor']
    assert s.revisions(p, 'main', {'limit': 1})[0]['restored_from_revision_id'] == 'historical'
    assert s.lookup_request(p, 'main', request['request_id'])['result'] == result['stored_result']
    assert s.evidence(result['receipt']['evidence_digest']) == value['evidence']
    assert ('publication_id' in value['restore']) == (known is not False)
    if not known: assert value['restore'].get('publication_id') is None
    assert s.store.integrity_report()['checks']['revisions']['ok']


@pytest.mark.parametrize('mode', ['revision', 'publication'])
def test_restore_stale_captured_head_has_no_effects(fixture, mode):
    from test_shot_composition_runtime import _publication
    s, p = fixture
    request = restore_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    value = restore_prepared(s, p, request, port.revision_closure('parent-1'))
    if mode == 'revision':
        s.accept(acceptance(s, p, key='advance'), identity=IDENTITY)
    else:
        s.publish_parent_composition(p, 'main', _publication(p, expected_head='parent-1'), idempotency_key='repeat')
    before = snapshot(s)
    with pytest.raises(ConflictError, match='StaleHead'):
        port.accept(value)
    assert snapshot(s) == before


@pytest.mark.parametrize('damage', ['digest', 'publication', 'missing-shot', 'cross-project', 'wrong-timeline', 'missing-media', 'unowned-media'])
def test_restore_dependency_refusal_has_no_effects(fixture, damage):
    from test_shot_composition_runtime import _publication
    s, p = fixture
    if damage in {'missing-media', 'unowned-media'}:
        media = s.ingest(p, b'manifest-only', media_type='audio/wav', original_name='tone.wav', idempotency_key='media')['data']['object_id']
        body = _publication(p, expected_head='parent-1', parent_revision_id='with-media')
        body['dependency_manifest'] = {'media': [media]}
        s.publish_parent_composition(p, 'main', body, idempotency_key='with-media')
        request = restore_request(s, p, revision='with-media')
        if damage == 'unowned-media':
            mutate(s, 'DELETE FROM project_objects WHERE project_id=? AND digest=?', (p, media[7:]))
        else:
            s.cas.path_for(media[7:]).unlink()
    else:
        request = restore_request(s, p)
        args = request['change']['commands'][0]['args']
        if damage == 'digest': args['content_digest'] = 'sha256:' + '0' * 64
        elif damage == 'publication': args['publication_id'] = 'unknown'
        elif damage == 'missing-shot':
            payload = s.get_project_parent_composition_revision(p, 'main', 'parent-1')['payload']
            payload['occurrences'][0]['shot_revision_id'] = 'missing-shot'
            args['content_digest'] = digest(payload)
            mutate(s, "UPDATE parent_composition_revisions SET payload_json=?, content_digest=? WHERE id='parent-1'",
                   (json.dumps(payload), args['content_digest']))
        elif damage == 'wrong-timeline': request['timeline_id'] = 'different'
        else:
            other = s.create_project(dict(slug='other', name='Other'), idempotency_key='other')['id']
            mutate(s, "UPDATE shot_revisions SET project_id=? WHERE id='shot-rev-1'", (other,))
    before = snapshot(s)
    port = s._request_commit_port(request, IDENTITY)
    with pytest.raises((ConflictError, NotFoundError, FileNotFoundError)):
        port.revision_closure(request['change']['commands'][0]['args']['revision_id'])
    assert snapshot(s) == before


@pytest.mark.parametrize('damage', ['parent', 'shot', 'internal', 'publication', 'manifest'])
def test_restore_changed_capture_rechecked_in_transaction(fixture, monkeypatch, damage):
    s, p = fixture
    request = restore_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure('parent-1')
    value = restore_prepared(s, p, request, closure)
    if damage in {'parent', 'shot', 'internal'}:
        table, row = {'parent': ('parent_composition_revisions', closure['parent_revision']),
                      'shot': ('shot_revisions', closure['shot_revisions'][0]),
                      'internal': ('internal_timeline_revisions', closure['internal_timeline_revisions'][0])}[damage]
        payload = dict(row['payload'], opaque_changed=True)
        mutate(s, 'UPDATE '+table+' SET payload_json=?, content_digest=? WHERE id=?',
               (json.dumps(payload), digest(payload), row['revision_id']))
    elif damage == 'publication':
        mutate(s, "UPDATE parent_composition_publications SET provenance_json='{}' WHERE publication_id=?", (request['base_publication_id'],))
    else:
        mutate(s, "DELETE FROM composition_revision_dependencies WHERE parent_revision_id='parent-1'")
    original = s._commit_restore_capture
    def checked(*args):
        assert s.store.conn.in_transaction
        return original(*args)
    monkeypatch.setattr(s, '_commit_restore_capture', checked)
    before = snapshot(s)
    with pytest.raises(ConflictError): port.accept(value)
    assert snapshot(s) == before


@pytest.mark.parametrize('damage', ['missing-marker', 'marker', 'candidate', 'numeric-bytes', 'head', 'ordinary', 'mixed', 'batch', 'scope', 'unread'])
def test_restore_marker_and_command_are_bound(fixture, damage):
    s, p = fixture
    request = restore_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure('parent-1')
    value = restore_prepared(s, p, request, closure)
    if damage == 'missing-marker': value.pop('restore')
    elif damage == 'marker': value['restore']['expected_publication_id'] = 'other'
    elif damage == 'candidate': value['publication']['parent_composition']['config']['forged'] = True
    elif damage == 'numeric-bytes':
        occurrence = value['publication']['parent_composition']['occurrences'][0]
        occurrence['speed'] = 1.0 if type(occurrence['speed']) is int else 1
        assert value['publication']['parent_composition'] == closure['parent_revision']['payload']
        assert digest(value['publication']['parent_composition']) != closure['parent_revision']['content_digest']
    elif damage == 'head': value['expected_head_revision_id'] = 'other'
    elif damage == 'ordinary':
        request['change']['commands'] = []
        port = s._request_commit_port(request, IDENTITY)
        value['request_hash'] = value['result']['request_hash'] = digest(request)
    elif damage == 'unread': port = s._request_commit_port(request, IDENTITY)
    before = snapshot(s)
    with pytest.raises(ValidationError):
        if damage in {'mixed', 'batch', 'scope'}:
            if damage == 'mixed': request['change']['commands'].append(dict(op='timeline.add', args={}))
            elif damage == 'batch': request['change']['commands'] = [dict(op='timeline.batch', args={'commands':request['change']['commands']})]
            else: request['scope']['complete'] = []
            s._request_commit_port(request, IDENTITY)
        else: port.accept(value)
    assert snapshot(s) == before


def test_restore_lost_response_replay_precedes_dependencies(fixture, monkeypatch):
    from runtime_protocol.contract_metadata import SCHEMA_DIGEST
    s, p = fixture
    request = restore_request(s, p)
    class Provider:
        interface_version = 1
        contract_digest = SCHEMA_DIGEST
        def commit(self, request, port):
            closure = port.revision_closure('parent-1')
            return port.accept(restore_prepared(s, p, request, closure))['stored_result']
    s.register_timeline_commit_provider(Provider())
    def lost(result): raise TimeoutError('lost durable restore response')
    monkeypatch.setattr(s, '_after_timeline_commit', lost, raising=False)
    with pytest.raises(TimeoutError):
        s.commit_timeline(p, 'main', request, idempotency_key=request['request_id'], identity=IDENTITY)
    saved = s.lookup_request(p, 'main', request['request_id'])['result']
    monkeypatch.delattr(s, '_after_timeline_commit')
    s.accept(acceptance(s, p, key='later'), identity=IDENTITY)
    before = snapshot(s)
    monkeypatch.setattr(s, '_commit_restore_capture', lambda *a: pytest.fail('replay reopened historical dependencies'))
    assert s.commit_timeline(p, 'main', request, idempotency_key=request['request_id'], identity=IDENTITY) == saved
    changed = copy.deepcopy(request); changed['change']['commands'][0]['args']['publication_id'] = None
    with pytest.raises(ConflictError):
        s.commit_timeline(p, 'main', changed, idempotency_key=request['request_id'], identity=IDENTITY)
    assert snapshot(s) == before


def test_restore_provenance_and_publication_roll_back_with_ledger(fixture, monkeypatch):
    s, p = fixture
    request = restore_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    value = restore_prepared(s, p, request, port.revision_closure('parent-1'))
    original = s._command_record
    def fail(kind, *args, **kwargs):
        if kind == 'timeline.commit':
            row = s.store.conn.execute('SELECT restored_from_revision_id, provenance_json FROM parent_composition_publications ORDER BY sequence DESC LIMIT 1').fetchone()
            assert row['restored_from_revision_id'] == 'parent-1'
            assert json.loads(row['provenance_json'])['publisher'] == IDENTITY['actor']
            raise RuntimeError('injected ledger failure')
        return original(kind, *args, **kwargs)
    monkeypatch.setattr(s, '_command_record', fail)
    before = snapshot(s)
    with pytest.raises(RuntimeError, match='injected ledger'): port.accept(value)
    assert snapshot(s) == before


def request_for(project, revision='parent-1'):
    request = wire(project)
    request['change']['commands'] = [dict(op='occurrence.set', select='occurrence:occurrence-1', args=dict(
        source=dict(parent_revision_id=revision, occurrence_id='occurrence-1', shot_id='shot-1', shot_revision_id='shot-rev-1', internal_revision_id='internal-rev-1'), placement=dict(start_ms=2000)))]
    return request


def test_closure_reads_are_declared_and_detached(fixture):
    s, p = fixture
    request = request_for(p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure('parent-1')
    closure['shot_revisions'][0]['payload']['provenance']['opaque'] = 'changed'
    assert 'opaque' not in port.revision_closure('parent-1')['shot_revisions'][0]['payload']['provenance']
    with pytest.raises(AuthorizationError, match='outside captured'):
        port.revision_closure('not-declared')
    request['change']['commands'][0]['args']['source']['parent_revision_id'] = 'not-declared'
    with pytest.raises(AuthorizationError):
        port.revision_closure('not-declared')


def test_declared_source_must_be_read_before_accept(fixture):
    s, p = fixture
    request = request_for(p)
    port = s._request_commit_port(request, IDENTITY)
    before = snapshot(s)
    with pytest.raises(ValidationError, match='must be read'):
        port.accept(acceptance(s, p, request=request))
    assert snapshot(s) == before


@pytest.mark.parametrize('kind', ['parent', 'shot', 'internal'])
def test_immutable_closure_rechecked_inside_accept_and_rollback(fixture, monkeypatch, kind):
    s, p = fixture
    request = request_for(p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure('parent-1')
    value = acceptance(s, p, request=request)
    if kind == 'parent':
        table, row = 'parent_composition_revisions', closure['parent_revision']
    elif kind == 'shot':
        table, row = 'shot_revisions', closure['shot_revisions'][0]
    else:
        table, row = 'internal_timeline_revisions', closure['internal_timeline_revisions'][0]
    payload = copy.deepcopy(row['payload'])
    payload['opaque_changed'] = True
    mutate(s, 'UPDATE ' + table + ' SET payload_json=?, content_digest=? WHERE id=?',
           (json.dumps(payload), digest(payload), row['revision_id']))
    before = snapshot(s)
    original = s._commit_revision_closure
    def checked(*args):
        assert s.store.conn.in_transaction
        return original(*args)
    monkeypatch.setattr(s, '_commit_revision_closure', checked)
    with pytest.raises(ConflictError, match='changed before acceptance'):
        port.accept(value)
    assert snapshot(s) == before
    assert s.lookup_request(p, 'main', request['request_id']) is None


def test_declared_source_success_replay_and_accepted_revision_read(fixture, monkeypatch):
    s, p = fixture
    request = request_for(p)
    port = s._request_commit_port(request, IDENTITY)
    port.revision_closure('parent-1')
    value = acceptance(s, p, request=request)
    accepted = port.accept(value)
    assert port.revision_closure(accepted['revision_id'])['parent_revision']['revision_id'] == accepted['revision_id']
    monkeypatch.setattr(s, '_commit_revision_closure', lambda *a: pytest.fail('durable replay reopened dependencies'))
    assert port.accept(value)['stored_result'] == accepted['stored_result']


def test_direct_shot_read_scoped_pins_and_acceptance_recheck(fixture):
    s, p = fixture
    ref = dict(shot_id='shot-1', shot_revision_id='shot-rev-1', internal_revision_id='timeline-rev-1')
    request = request_for(p)
    request['change']['commands'][0]['args']['replacement'] = copy.deepcopy(ref)
    port = s._request_commit_port(request, IDENTITY)
    port.revision_closure('parent-1')
    read = port.revision_closure(ref)
    assert set(read) == {'shot_revision', 'internal_timeline_revision'}
    assert read['internal_timeline_revision']['timeline_id'] == 'main'
    with pytest.raises(AuthorizationError):
        port.revision_closure({**ref, 'internal_revision_id':'other'})
    value = acceptance(s, p, request=request)
    payload = copy.deepcopy(read['shot_revision']['payload']); payload['opaque'] = True
    mutate(s, 'UPDATE shot_revisions SET payload_json=?, content_digest=? WHERE id=?',
           (json.dumps(payload), digest(payload), ref['shot_revision_id']))
    before = snapshot(s)
    with pytest.raises(ConflictError, match='changed before acceptance'):
        port.accept(value)
    assert snapshot(s) == before


def test_direct_shot_stale_internal_pin_is_refused_without_mutation(fixture):
    s, p = fixture
    ref = dict(shot_id='shot-1', shot_revision_id='shot-rev-1', internal_revision_id='stale-internal')
    request = request_for(p)
    request['change']['commands'][0]['args']['replacement'] = ref
    port = s._request_commit_port(request, IDENTITY)
    before = snapshot(s)
    with pytest.raises(ConflictError, match='pin mismatch'):
        port.revision_closure(ref)
    assert snapshot(s) == before


def duplicate_request(s, p, *, batch=False):
    from test_timeline_retention import duplicate
    pin = duplicate(s, p)
    initial = dict(project_id=p, timeline_id='dup', expected_head=None,
                   parent_composition=dict(config={}, registry={}, clips=[], occurrences=[]),
                   shot_revisions=[], internal_timeline_revisions=[])
    s.publish_parent_composition(p, 'dup', initial, idempotency_key='bootstrap')
    head = s.head(p, 'dup')
    request = wire(p)
    request.update(timeline_id='dup', base_revision_id=head['revision_id'], base_publication_id=head['publication_id'])
    ref = dict(timeline_id='main', parent_revision_id=pin['expected_revision_id'], publication_id=pin['expected_publication_id'])
    operation = dict(op='timeline.duplicate', args=dict(source=ref, bootstrap_revision_id=head['revision_id'], identities=[]))
    request['change']['commands'] = [dict(op='timeline.batch', args=dict(commands=[operation]))] if batch else [operation]
    return request, ref


@pytest.mark.parametrize('batch', [False, True])
def test_duplicate_parent_capability_exact_declared_and_consumed(fixture, batch):  # noqa: F811 - shared fixture
    s, p = fixture
    request, ref = duplicate_request(s, p, batch=batch)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure(ref)
    assert closure['parent_revision']['timeline_id'] == 'main'
    assert len(closure['shot_revisions']) == len(closure['internal_timeline_revisions']) == 1
    with pytest.raises(AuthorizationError):
        port.revision_closure('parent-1')  # foreign parent never becomes a destination read
    with pytest.raises(AuthorizationError):
        port.revision_closure(dict(ref, publication_id='other'))
    # A newer source head does not change the captured exact selection.
    s.accept(acceptance(s, p, key='source-moves'), identity=IDENTITY)
    assert port.revision_closure(ref) == closure
    # Destination head is still independent of source head movement.
    assert s.head(p, 'dup')['revision_id'] == request['base_revision_id']


@pytest.mark.parametrize('damage', ['parent', 'shot', 'internal', 'publication', 'provenance', 'project'])
def test_duplicate_parent_capability_refuses_changed_dependencies(fixture, damage):  # noqa: F811 - shared fixture
    s, p = fixture
    request, ref = duplicate_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure(ref)
    if damage in {'parent', 'shot', 'internal'}:
        table, row = {'parent': ('parent_composition_revisions', closure['parent_revision']),
                      'shot': ('shot_revisions', closure['shot_revisions'][0]),
                      'internal': ('internal_timeline_revisions', closure['internal_timeline_revisions'][0])}[damage]
        payload = dict(row['payload'], opaque_changed=True)
        mutate(s, 'UPDATE '+table+' SET payload_json=?, content_digest=? WHERE id=?',
               (json.dumps(payload), digest(payload), row['revision_id']))
    elif damage == 'publication':
        mutate(s, 'UPDATE parent_composition_publications SET publication_id=? WHERE publication_id=?', ('changed', ref['publication_id']))
    elif damage == 'provenance':
        mutate(s, "UPDATE timeline_events SET payload_json='{}' WHERE timeline_id='dup' AND kind='timeline.duplicate_created'", ())
    else:
        other = s.create_project(dict(slug='other', name='Other'), idempotency_key='other')['id']
        mutate(s, "UPDATE timelines SET project_id=? WHERE id='main'", (other,))
    before = snapshot(s)
    with pytest.raises((ConflictError, AuthorizationError)):
        port.revision_closure(ref)
    assert snapshot(s) == before


def duplicate_acceptance(s, p, request):
    value = acceptance(s, p, request=request)
    value.update(timeline_id='dup', expected_head_revision_id=request['base_revision_id'])
    value['result']['rebased_onto'] = request['base_revision_id']
    return value


def test_duplicate_source_must_be_consumed_before_accept(fixture):  # noqa: F811 - shared fixture
    s, p = fixture
    request, ref = duplicate_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    before = snapshot(s)
    with pytest.raises(ValidationError, match='must be read'):
        port.accept(duplicate_acceptance(s, p, request))
    assert snapshot(s) == before


@pytest.mark.parametrize('damage', ['parent', 'shot', 'internal'])
def test_duplicate_source_rechecked_atomically_at_accept(fixture, monkeypatch, damage):  # noqa: F811 - shared fixture
    s, p = fixture
    request, ref = duplicate_request(s, p)
    port = s._request_commit_port(request, IDENTITY)
    closure = port.revision_closure(ref)
    prepared = duplicate_acceptance(s, p, request)
    table, row = {'parent': ('parent_composition_revisions', closure['parent_revision']),
                  'shot': ('shot_revisions', closure['shot_revisions'][0]),
                  'internal': ('internal_timeline_revisions', closure['internal_timeline_revisions'][0])}[damage]
    payload = dict(row['payload'], changed_after_capture=True)
    mutate(s, 'UPDATE '+table+' SET payload_json=?, content_digest=? WHERE id=?',
           (json.dumps(payload), digest(payload), row['revision_id']))
    before = snapshot(s)
    original = s._commit_revision_closure
    def checked(*args, **kwargs):
        assert s.store.conn.in_transaction
        return original(*args, **kwargs)
    monkeypatch.setattr(s, '_commit_revision_closure', checked)
    with pytest.raises(ConflictError, match='changed before acceptance'):
        port.accept(prepared)
    assert snapshot(s) == before
    assert s.lookup_request(p, 'dup', request['request_id']) is None
