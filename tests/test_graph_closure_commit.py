"""Request-owned immutable closure reads and the atomic acceptance fence."""
import copy
import json

import pytest

from runtime_protocol.errors import AuthorizationError, ConflictError, ValidationError
from runtime_protocol.timeline_commit import digest
from test_timeline_accept import IDENTITY, acceptance, fixture, wire  # noqa: F401
from test_selected_media_commit import mutate, snapshot


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
