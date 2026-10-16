"""Accepted narration comes from immutable publication/receipt pins, not head."""
import copy
import json
import threading

import pytest

from runtime_protocol.errors import ConflictError, NotFoundError
from runtime_protocol.auth import CredentialStore
from runtime_protocol.narration import narration_projection
from runtime_protocol.server import RuntimeHTTPServer, RuntimeHandler
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit import digest
from http_helpers import Api
from test_narration_commit import setup
from test_selected_media_commit import snapshot
from test_timeline_accept import IDENTITY, acceptance, fixture, valid, wire


def adopt_and_delete(service, project):
    refs, request, port, take, value = setup(service, project)
    # Two occurrences prove the read preserves the complete ordered projection.
    occurrence = copy.deepcopy(value['publication']['parent_composition']['occurrences'][0])
    occurrence['occurrence_id'] = 'occurrence-2'
    value['publication']['parent_composition']['occurrences'].append(occurrence)
    publication = value['publication']
    value['narration'] = narration_projection({
        'parent_revision': {'payload': publication['parent_composition']},
        'shot_revisions': publication['shot_revisions'],
        'internal_timeline_revisions': publication['internal_timeline_revisions']})
    first = port.accept(value)
    request = wire(project, key='delete-all')
    request.update(base_revision_id=first['revision_id'], base_publication_id=first['publication_id'])
    request['change']['commands'] = [{'op': 'timeline.apply-script', 'args': {'lines': []}}]
    delete_port = service._request_commit_port(request, IDENTITY)
    deletion = acceptance(service, project, request=request)
    pub = deletion['publication']
    pub['internal_timeline_revisions'][0]['revision_id'] = 'empty-internal'
    pub['shot_revisions'][0]['revision_id'] = 'empty-shot'
    pub['shot_revisions'][0]['internal_timeline_revision_id'] = 'empty-internal'
    pub['parent_composition']['occurrences'][0]['shot_revision_id'] = 'empty-shot'
    deletion['narration'] = {'version': 1, 'lines': []}
    deletion['evidence']['commands'] = copy.deepcopy(request['change']['commands'])
    empty = delete_port.accept(deletion)
    valid(empty, 'AcceptResponse')
    return first, empty, delete_port, deletion


def test_delete_all_exact_pinned_read_reload_and_replay(fixture, monkeypatch):
    s, p = fixture
    first, empty, port, deletion = adopt_and_delete(s, p)
    old = s.get_project_timeline_revision(p, 'main', 'narrated-internal')
    current = s.get_project_timeline_revision(p, 'main', 'empty-internal')
    assert old['narration_state'] == first['receipt']['narration_state']
    assert len(old['narration_state']['projection']['lines']) == 2
    assert current['narration_state'] == empty['receipt']['narration_state']
    assert current['narration_state']['projection'] == {'version': 1, 'lines': []}
    assert current['narration_state']['parent_revision_id'] == empty['revision_id']
    assert current['narration_state']['parent_revision_id'] != current['revision_id']
    assert 'narration_state' not in s.get_project_timeline_revision(p, 'main', 'timeline-rev-1')
    # Later accepted publications referencing the same child do not replace its
    # receipt, nor adopt narration for a legacy child retroactively.
    later = acceptance(s, p, key='later')
    later['narration'] = {'version': 1, 'lines': []}
    s.accept(later, identity=IDENTITY)
    assert s.get_project_timeline_revision(p, 'main', 'empty-internal') == current
    assert s.get_project_timeline_revision(p, 'main', 'narrated-internal') == old
    assert 'narration_state' not in s.get_project_timeline_revision(p, 'main', 'timeline-rev-1')
    before = snapshot(s)
    assert port.accept(deletion)['stored_result'] == empty['stored_result']
    assert snapshot(s) == before
    root = s.store.root
    s.close()
    reloaded = RuntimeService(root)
    try:
        assert reloaded.get_project_timeline_revision(p, 'main', 'empty-internal') == current
        assert reloaded.get_project_timeline_revision(p, 'main', 'narrated-internal') == old
        assert 'narration_state' not in reloaded.get_project_timeline_revision(p, 'main', 'timeline-rev-1')
        # Stored-result replay must not consult mutable dependencies or providers.
        monkeypatch.setattr(reloaded, '_managed_narration_take', lambda *_: pytest.fail('replay reread takes'))
        assert reloaded.accept(deletion, identity=IDENTITY)['stored_result'] == empty['stored_result']
        detached = reloaded.get_project_timeline_revision(p, 'main', 'empty-internal')
        detached['narration_state']['projection']['lines'].append('caller mutation')
        assert reloaded.get_project_timeline_revision(p, 'main', 'empty-internal') == current
    finally:
        reloaded.close()


@pytest.mark.parametrize('bad', ['parent', 'digest', 'projection', 'result-revision',
                               'result-publication', 'result-request', 'result-hash',
                               'result-status', 'receipt-type', 'extra'])
def test_invalid_stored_narration_never_returns_adopted_state(fixture, bad):
    s, p = fixture
    first, empty, port, deletion = adopt_and_delete(s, p)
    row = s.store.conn.execute(
        "SELECT rowid, result_json FROM command_idempotency WHERE command_kind='timeline.commit' "
        "AND idempotency_key='delete-all'").fetchone()
    stored = json.loads(row['result_json'])
    result = stored['result']
    state = result['runtime_receipt']['narration_state']
    if bad == 'parent':
        state['parent_revision_id'] = first['revision_id']
    elif bad == 'digest':
        state['digest'] = 'sha256:' + '0' * 64
    elif bad == 'projection':
        state['projection'] = first['receipt']['narration_state']['projection']
        state['digest'] = digest(state['projection'])
    elif bad == 'result-revision':
        result['accepted_revision_id'] = first['revision_id']
    elif bad == 'result-request':
        result['request_id'] = 'forged'
    elif bad == 'result-publication':
        result['accepted_publication_id'] = 'forged'
    elif bad == 'result-hash':
        result['request_hash'] = 'sha256:' + '0' * 64
    elif bad == 'result-status':
        result['status'] = 'no_change'
    elif bad == 'receipt-type':
        result['runtime_receipt'] = []
    else:
        state['unknown'] = True
    with s.store._transaction():
        s.store.conn.execute('UPDATE command_idempotency SET result_json=? WHERE rowid=?',
                             (json.dumps(stored), row['rowid']))
    before = snapshot(s)
    with pytest.raises(ConflictError):
        s.get_project_timeline_revision(p, 'main', 'empty-internal')
    assert snapshot(s) == before


@pytest.mark.parametrize('bad', ['child-bytes', 'parent-bytes', 'shot-bytes',
                               'dependency-digest', 'membership', 'duplicate-receipt'])
def test_origin_closure_corruption_refuses_without_side_effects(fixture, bad):
    s, p = fixture
    first, empty, port, deletion = adopt_and_delete(s, p)
    with s.store._transaction():
        if bad == 'child-bytes':
            s.store.conn.execute("UPDATE internal_timeline_revisions SET payload_json='{}' WHERE id='empty-internal'")
        elif bad == 'parent-bytes':
            s.store.conn.execute("UPDATE parent_composition_revisions SET payload_json='{}' WHERE id=?",
                                 (empty['revision_id'],))
        elif bad == 'shot-bytes':
            s.store.conn.execute("UPDATE shot_revisions SET payload_json='{}' WHERE id='empty-shot'")
        elif bad == 'dependency-digest':
            s.store.conn.execute("UPDATE composition_revision_dependencies SET content_digest=? "
                                 "WHERE parent_revision_id=? AND dependency_id='empty-internal'",
                                 ('sha256:' + '0' * 64, empty['revision_id']))
        elif bad == 'membership':
            # A forged dependency edge cannot make an unrelated child part of
            # the actual immutable parent/shot/internal closure.
            s.store.conn.execute("UPDATE composition_revision_dependencies SET parent_revision_id=? "
                                 "WHERE parent_revision_id=? AND dependency_id='empty-internal'",
                                 (first['revision_id'], empty['revision_id']))
        else:
            row = s.store.conn.execute("SELECT * FROM command_idempotency WHERE command_kind='timeline.commit' "
                                       "AND idempotency_key='delete-all'").fetchone()
            s.store.conn.execute("INSERT INTO command_idempotency(command_kind,aggregate_id,idempotency_key,"
                                 "request_hash,result_json,created_at) VALUES (?,?,?,?,?,?)",
                                 (row['command_kind'], row['aggregate_id'], 'duplicate', row['request_hash'],
                                  row['result_json'], row['created_at']))
    before = snapshot(s)
    with pytest.raises(ConflictError):
        s.get_project_timeline_revision(p, 'main', 'empty-internal')
    assert snapshot(s) == before


def test_project_timeline_revision_refusals_and_real_legacy_absence(fixture):
    s, p = fixture
    assert 'narration_state' not in s.get_project_timeline_revision(p, 'main', 'timeline-rev-1')
    first, empty, port, deletion = adopt_and_delete(s, p)
    other = s.create_project({'slug': 'other', 'name': 'Other'}, idempotency_key='other')['id']
    before = snapshot(s)
    for project, timeline, revision in [(other, 'main', 'empty-internal'),
                                        (p, 'wrong', 'empty-internal'),
                                        (p, 'main', 'missing')]:
        with pytest.raises(NotFoundError):
            s.get_project_timeline_revision(project, timeline, revision)
    assert snapshot(s) == before


def test_child_timeline_identity_can_differ_from_origin_parent_timeline(fixture):
    s, p = fixture
    s.create_timeline(p, 'inside', idempotency_key='inside')
    refs, request, port, take, value = setup(s, p)
    value['publication']['internal_timeline_revisions'][0]['timeline_id'] = 'inside'
    publication = value['publication']
    value['narration'] = narration_projection({
        'parent_revision': {'payload': publication['parent_composition']},
        'shot_revisions': publication['shot_revisions'],
        'internal_timeline_revisions': publication['internal_timeline_revisions']})
    accepted = port.accept(value)
    child = s.get_project_timeline_revision(p, 'inside', 'narrated-internal')
    assert child['timeline_id'] == 'inside'
    assert child['narration_state'] == accepted['receipt']['narration_state']
    with pytest.raises(NotFoundError):
        s.get_project_timeline_revision(p, 'main', 'narrated-internal')


def test_exact_pinned_http_read_keeps_projects_read_authorization(fixture, tmp_path):
    s, p = fixture
    first, empty, port, deletion = adopt_and_delete(s, p)
    credentials = CredentialStore(tmp_path / 'credentials')
    reader, _ = credentials.provision('reader', ['projects:read'])
    writer, _ = credentials.provision('writer', ['projects:write'])
    server = RuntimeHTTPServer(('127.0.0.1', 0), RuntimeHandler)
    server.runtime, server.credentials = s, credentials
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    endpoint = f'http://127.0.0.1:{server.server_port}'
    path = f'/v1/projects/{p}/timelines/main/revisions/empty-internal'
    before = snapshot(s)
    try:
        state = Api(endpoint, reader).request('GET', path)['narration_state']
        assert state == empty['receipt']['narration_state']
        for token, status in [(None, 401), (writer, 401)]:
            with pytest.raises(RuntimeError) as refused:
                Api(endpoint, token).request('GET', path)
            assert refused.value.status == status
        assert snapshot(s) == before
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive()
