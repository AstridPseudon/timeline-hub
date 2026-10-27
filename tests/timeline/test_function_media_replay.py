"""Function media identity through real Runtime commits, undo, and restart."""
from __future__ import annotations

import copy
import json

import pytest
from PIL import Image

from astrid.sdk.timeline.commit_session import Timeline
from tests.timeline.test_audio_import_runtime import realm, session_for, wav  # noqa: F401


def opened(session):
    return Timeline.open(session.project_id, session.timeline_id, client=session.client,
                         outbox_path=session.outbox.path)


def watch_imports(session, monkeypatch):
    transport = session.client._remote._transport
    original = transport.import_project_media
    calls = []

    def imported(*args, **kwargs):
        calls.append(copy.deepcopy(kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(transport, 'import_project_media', imported)
    return calls


def test_function_content_imports_one_commit_and_exact_undo(realm, tmp_path, monkeypatch):  # noqa: F811
    service, writer, candidate = realm
    session = session_for(service, writer, candidate, tmp_path / 'outbox.json')
    tl = opened(session)
    imports = watch_imports(session, monkeypatch)
    picture = tmp_path / 'picture.png'
    Image.new('RGB', (16, 12), 'red').save(picture)
    same_content = tmp_path / 'another-name.png'
    same_content.write_bytes(picture.read_bytes())
    voice = wav(tmp_path / 'voice.wav')
    project, timeline = session.project_id, session.timeline_id
    history = writer.list_timeline_commits(project, timeline)
    before = service._timeline_commits()[0].revision_closure(
        project, timeline, history['head']['revision_id'])

    def place(t):
        t.add(voice, at=0, hold=1, id='voice')
        t.add(picture, at=0, hold=1, id='picture-1')
        t.add(same_content, at=2, hold=1, id='picture-2')

    result = tl.commit(place, idempotency_key='place-media')
    assert len(imports) == len(result['imports']) == 2
    assert all(row['catalog_write'] and row['retained_on_undo'] for row in result['imports'])
    parent = result['data']['canonical_document']['parent_revision']['payload']
    assert [row['id'] for row in parent['clips']] == ['voice', 'picture-1', 'picture-2']
    assert parent['clips'][1]['asset'] == parent['clips'][2]['asset']
    assert parent['clips'][0]['clipType'] == 'audio'
    assert parent['clips'][0]['hold'] == parent['clips'][0]['to'] == 1
    assert len(writer.list_timeline_commits(project, timeline)['items']) == len(history['items']) + 1
    undone = tl.undo(publications=[result['receipt']['receipt_id']])
    assert undone['data']['canonical_document'] == before
    assert len(writer.list_timeline_commits(project, timeline)['items']) == len(history['items']) + 2
    assert len(service.list_generations(project)['items']) == 2


def test_conflict_then_lost_ack_restart_replays_original_media_bytes(
        realm, tmp_path, monkeypatch):  # noqa: F811
    service, writer, candidate = realm
    path = tmp_path / 'outbox.json'
    session = session_for(service, writer, candidate, path)
    tl = opened(session)
    imports = watch_imports(session, monkeypatch)
    source = wav(tmp_path / 'voice.wav')
    original_send = writer.commit_timeline
    sent, evaluations = [], []

    def send(project, timeline, body, **kwargs):
        sent.append((copy.deepcopy(body), kwargs['idempotency_key']))
        if len(sent) == 1:
            peer = session_for(service, writer, candidate, tmp_path / 'peer.json')
            peer.commit({'schema_version': 1, 'op': 'track.create', 'version': '1',
                         'select': 'parent', 'args': {'row': {'id': 'peer', 'kind': 'visual'}}},
                        idempotency_key='peer-edit')
            source.write_bytes(b'changed local bytes after the verified import')
        result = original_send(project, timeline, body, **kwargs)
        if kwargs['idempotency_key'] != 'peer-edit':
            raise ConnectionError('lost function acknowledgement')
        return result

    monkeypatch.setattr(writer, 'commit_timeline', send)

    def place(t):
        evaluations.append(t.head)
        t.add(source, at=0, hold=1, id='voice')

    with pytest.raises(ConnectionError, match='lost function acknowledgement'):
        tl.commit(place, idempotency_key='logical-place')
    assert len(evaluations) == 2 and len(imports) == 1
    state = json.loads(path.read_bytes())
    frozen = copy.deepcopy(state['flight'])
    accepted_request = sent[-1]
    history = writer.list_timeline_commits(session.project_id, session.timeline_id)
    source.rename(tmp_path / 'removed.wav')
    monkeypatch.setattr(writer, 'commit_timeline', original_send)
    restarted = opened(session_for(service, writer, candidate, path))

    def forbidden(*args, **kwargs):
        pytest.fail('replay evaluated intent or selected/imported media')

    transport = restarted.session.client._remote._transport
    monkeypatch.setattr(transport, 'import_project_media', forbidden)
    monkeypatch.setattr(transport, 'get_project_media_selection', forbidden)
    monkeypatch.setattr(transport, 'get_project_verified_media', forbidden)
    result = restarted.commit(forbidden, idempotency_key='logical-place')
    assert writer.requests[-1] == accepted_request[0] == json.loads(frozen['body'])
    assert result['receipt']['idempotency_key'] == accepted_request[1] == frozen['key']
    assert result['imports'] == frozen['imports']
    assert len(evaluations) == 2 and len(imports) == 1
    assert writer.list_timeline_commits(session.project_id, session.timeline_id) == history

    restarted.undo(publications=[result['receipt']['receipt_id']])
    latest = opened(restarted.session)
    latest_head, latest_bundle = latest.head, copy.deepcopy(latest.bundle)
    replay = latest.commit(forbidden, idempotency_key='logical-place')
    assert replay['receipt'] == result['receipt']
    assert replay['imports'] == result['imports']
    assert latest.head == latest_head and latest.bundle == latest_bundle
    assert len(evaluations) == 2 and len(imports) == 1


def test_restart_at_conflict_reuses_saved_content_import(realm, tmp_path, monkeypatch):  # noqa: F811
    service, writer, candidate = realm
    path = tmp_path / 'outbox.json'
    session = session_for(service, writer, candidate, path)
    tl = opened(session)
    imports = watch_imports(session, monkeypatch)
    source = wav(tmp_path / 'voice.wav')
    original_send = writer.commit_timeline
    evaluations, sent = [], []

    def send(project, timeline, body, **kwargs):
        sent.append(kwargs['idempotency_key'])
        if len(sent) == 1:
            peer = session_for(service, writer, candidate, tmp_path / 'peer.json')
            peer.commit({'schema_version': 1, 'op': 'track.create', 'version': '1',
                         'select': 'parent', 'args': {'row': {'id': 'peer', 'kind': 'visual'}}},
                        idempotency_key='peer-edit')
        return original_send(project, timeline, body, **kwargs)

    monkeypatch.setattr(writer, 'commit_timeline', send)

    def place(t):
        evaluations.append(t.head)
        if len(evaluations) == 2:
            raise InterruptedError('interrupted reevaluation')
        t.add(source, at=0, hold=1, id='voice')

    with pytest.raises(InterruptedError, match='interrupted reevaluation'):
        tl.commit(place, idempotency_key='logical-place')
    state = json.loads(path.read_bytes())
    assert state['evaluation']['count'] == 1
    cached = next(iter(state['evaluation']['media_cache'].values()))
    assert len(imports) == 1
    source.rename(tmp_path / 'removed-before-restart.wav')
    monkeypatch.setattr(writer, 'commit_timeline', original_send)
    transport = session.client._remote._transport
    monkeypatch.setattr(transport, 'import_project_media',
                        lambda *a, **kw: pytest.fail('reimported saved content after restart'))
    monkeypatch.setattr(transport, 'get_project_media_selection',
                        lambda *a, **kw: pytest.fail('reselected saved content after restart'))
    result = opened(session).commit(place)
    assert result['imports'] == cached['imports']
    assert result['receipt']['idempotency_key'] != 'logical-place'
    assert len(evaluations) == 3
    replay = opened(session).commit(lambda t: pytest.fail('reevaluated acknowledged function'),
                                    idempotency_key='logical-place')
    assert replay['receipt'] == result['receipt']
