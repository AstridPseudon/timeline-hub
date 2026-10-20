"""Native registry commands share the M1 outbox without recapturing claims."""
from __future__ import annotations

import copy
import io
import json
import wave
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline._track_commands import capture_track_set
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.sync import CommitConflict
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk import test_timeline_sync
from tests.sdk.test_timeline_sync import initial_bundle, open_session

connected = test_timeline_sync.connected
REF = 'parent/track:picture'


@pytest.mark.parametrize('damage', [None, 'project_id', 'timeline_id', 'revision_id',
                                  'content_digest', 'membership'])
def test_raw_trim_reads_original_manifest_after_peer_head_advances(connected, monkeypatch, damage):
    client, generated, path = connected
    bundle = generated.bundles['r0']
    media = 'sha256:' + '3' * 64
    bundle['parent']['registry'] = {'assets': {'voice': {'object_id': media, 'type': 'audio'}}}
    bundle['parent']['config']['tracks'][0]['kind'] = 'audio'
    bundle['parent']['clips'][0].update(clipType='audio', asset='voice', params={})
    original = {**bundle['base_parent'], 'project_id': 'p', 'timeline_id': 't',
                'dependency_manifest': {'media': [{'media_id': media, 'content_digest': media}]}}
    original['revision_id'] = 'r0'
    if damage == 'membership':
        original['dependency_manifest']['media'] = []
    elif damage is not None:
        original[damage] = 'peer-value'
    audio = io.BytesIO()
    with wave.open(audio, 'wb') as output:
        output.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
        output.writeframes(b'\x00\x00' * 48000)
    reads = []

    def revision(project, timeline, identity):
        reads.append((project, timeline, identity))
        return copy.deepcopy(original)

    monkeypatch.setattr(client._remote._transport, 'get_project_parent_composition_revision', revision)
    client.media = SimpleNamespace(read_bytes=lambda identity: audio.getvalue()
        if identity == media else pytest.fail('read another media object'))
    session = open_session(connected)
    monkeypatch.setattr(session, 'flush', lambda **options: session.outbox.read()['pending'])
    generated.head = {'revision_id': 'peer', 'publication_id': 'peer-publication'}
    persisted = path.read_bytes()
    if damage is None:
        command, = session.trim('parent/clip:a', out_s=4)
        assert {'ref': 'media:' + media, 'path': ['duration_seconds'],
                'state': {'state': 'present', 'value': 6}} in command['reads']
        assert session.outbox.read()['base'] == {'revision_id': 'r0', 'publication_id': 'pub0'}
    else:
        with pytest.raises(TimelineEditError):
            session.trim('parent/clip:a', out_s=4)
        assert path.read_bytes() == persisted
    assert reads == [('p', 't', 'r0')]
    assert generated.calls == []


def label(value='', *, clear=False):
    return {'schema_version': 1, 'op': 'track.set', 'version': '1', 'select': REF,
            'args': {'values': {} if clear else {'label': value},
                     'clear': ['label'] if clear else []}}


@pytest.mark.parametrize('captured', [False, True])
def test_native_queue_and_commit_match_full_portable_golden(connected, captured):
    _, generated, _ = connected
    fixture = json.loads((Path(__file__).parents[1] / 'editing_conformance/fixtures/'
                         'recipe_m2_app_track_label.json').read_text())
    generated.bundles['r0'] = copy.deepcopy(fixture['bundle'])
    session = open_session(connected)
    supplied = copy.deepcopy(fixture['command'] if captured else fixture['request'])
    assert session.queue(supplied) == fixture['command']
    assert session.commit(supplied)['data']['commands'] == [fixture['command']]
    assert generated.bundles['r1'] == fixture['after_bundle']
    assert supplied == (fixture['command'] if captured else fixture['request'])


@pytest.mark.parametrize('before', [None, '', 'Old'])
@pytest.mark.parametrize('clear', [False, True])
def test_native_session_preserves_presence_clear_and_unchanged_history(connected, before, clear):
    _, generated, _ = connected
    if before is not None:
        State(generated.bundles['r0']).entity(REF)['label'] = before
    original = copy.deepcopy(generated.bundles['r0'])
    session = open_session(connected)
    result = session.commit(label(clear=clear))
    track = State(generated.bundles['r1']).entity(REF)
    assert ('label' not in track) if clear else track['label'] == ''
    writes = generated.records['pub1'][0]['writes']
    assert any(row['path'] == ['label'] for row in writes)
    if (clear and before is None) or (not clear and before == ''):
        assert any(row['before'] == row['after'] for row in writes)
    session.undo([result['receipt']['receipt_id']])
    assert generated.bundles['r2'] == original


def test_native_queue_uses_prior_pending_commands_and_stable_created_identity(connected):
    _, generated, _ = connected
    session = open_session(connected)
    create = {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
              'args': {'row': {'id': 'new', 'kind': 'visual'}}}
    first = session.queue(create)
    second = label('New')
    second['select'] = 'parent/track:new'
    captured = session.queue(second)
    session.flush()
    assert json.loads(generated.calls[0][0])['commands'] == [first, captured]
    assert State(generated.bundles['r1']).entity('parent/track:new')['label'] == 'New'


def test_native_move_ingress_matches_existing_move_capture(connected):
    from astrid.sdk.timeline.capture import capture_move

    command = capture_move(initial_bundle(), 'parent/clip:a', 5)
    assert open_session(connected).commit(command)['data']['commands'] == [command]


@pytest.mark.parametrize('intent', [{}, {'ripple': 'none'},
                                 {'ripple': 'none', 'anchor': 'fixed', 'position': 'absolute'}])
def test_native_move_with_default_intent_retries_without_recapture(connected, intent):
    client, generated, _ = connected
    raw = {'schema_version': 1, 'op': 'clip.move', 'version': '1', 'select': 'parent/clip:a',
           'args': {'on': 5}, 'intent': intent}
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        open_session(connected).commit(raw)
    open_session(connected).commit(raw)
    assert generated.calls[0] == generated.calls[1]
    assert client.reads == ['r0']


@pytest.mark.parametrize('value,changed', [(True, 1), (False, 0)])
@pytest.mark.parametrize('nested', [False, True])
def test_native_lost_ack_refuses_changed_json_type_before_send(connected, value, changed, nested):
    client, generated, path = connected
    raw = {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
           'args': {'row': {'id': 'new', 'kind': 'visual',
                            'opaque': {'items': [value]} if nested else value}}}
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        open_session(connected).commit(raw, idempotency_key='original')
    persisted = path.read_bytes()
    accepted = copy.deepcopy(generated.accepted['original'][1])
    changed_command = copy.deepcopy(raw)
    changed_command['args']['row']['opaque'] = {'items': [changed]} if nested else changed
    session = open_session(connected)
    with pytest.raises(TimelineEditError, match='pending intent differs'):
        session.commit(changed_command)
    assert len(generated.calls) == 1
    assert path.read_bytes() == persisted
    retried = session.commit(raw)
    assert retried['receipt'] == accepted['receipt']
    assert generated.calls == [(json.loads(persisted)['flight']['body'].encode(), 'original')] * 2
    assert client.reads == ['r0']


@pytest.mark.parametrize('field', ['reads', 'expect'])
def test_native_lost_ack_refuses_changed_boolean_capture_claim(connected, field):
    client, generated, path = connected
    clip = State(generated.bundles['r0']).entity('parent/clip:a')
    clip.update(enabled=True, app={'astrid': {'fixed_start': True}})
    raw = {'schema_version': 1, 'op': 'clip.move', 'version': '1', 'select': 'parent/clip:a',
           'args': {'on': 5}}
    captured = execute(generated.bundles['r0'], [raw]).commands[0]
    changed = copy.deepcopy(captured)
    if field == 'reads':
        claim = next(read['state'] for read in changed['reads']
                     if read['ref'] == 'parent/clip:a' and read['path'] == ['enabled'])
    else:
        claim = changed['expect']['parent/clip:a::app.astrid.fixed_start']
    assert claim['value'] is True
    claim['value'] = 1
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        open_session(connected).commit(captured, idempotency_key='captured')
    persisted = path.read_bytes()
    accepted = copy.deepcopy(generated.accepted['captured'][1])
    session = open_session(connected)
    with pytest.raises(TimelineEditError, match='pending intent differs'):
        session.commit(changed)
    assert len(generated.calls) == 1
    assert path.read_bytes() == persisted
    assert session.commit(captured)['receipt'] == accepted['receipt']
    assert generated.calls[0] == generated.calls[1]
    assert client.reads == ['r0']


def test_native_lost_ack_numeric_equivalence_retries_original_bytes(connected):
    client, generated, _ = connected
    raw = {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
           'args': {'row': {'id': 'new', 'kind': 'visual', 'opaque': 2}}}
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        open_session(connected).commit(raw, idempotency_key='numeric')
    accepted = copy.deepcopy(generated.accepted['numeric'][1])
    raw['args']['row']['opaque'] = 2.0
    assert open_session(connected).commit(raw)['receipt'] == accepted['receipt']
    assert generated.calls[0] == generated.calls[1]
    assert b'"opaque":2}' in generated.calls[1][0]
    assert client.reads == ['r0']


@pytest.mark.parametrize('peer', ['disjoint', 'label', 'aba'])
def test_native_lost_ack_retry_precedes_original_suffix_with_fresh_key(connected, peer):
    client, generated, path = connected
    session = open_session(connected)
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        session.commit(label('A'), idempotency_key='A')
    original_flight = json.loads(path.read_bytes())['flight']
    accepted = copy.deepcopy(generated.accepted['A'][1])
    session = open_session(connected)
    suffix = session.queue(label('B'))
    assert suffix == capture_track_set(generated.bundles['r1'], REF, values={'label': 'B'})
    changed = copy.deepcopy(generated.bundles['r1'])
    if peer == 'disjoint':
        State(changed).entity('parent/clip:b')['params']['text'] = 'Peer'
    else:
        changed = execute(changed, [label('Peer')]).bundle
        if peer == 'aba':
            changed = execute(changed, [label('A')]).bundle
    generated.bundles['peer'] = changed
    generated.head = {'revision_id': 'peer', 'publication_id': 'peer-publication'}
    retried = open_session(connected).flush()
    assert retried['receipt'] == accepted['receipt']
    assert generated.calls[:2] == [(original_flight['body'].encode(), 'A')] * 2
    state = json.loads(path.read_bytes())
    assert state['base'] == {'revision_id': 'r1', 'publication_id': 'pub1'}
    assert state['pending'] == [suffix] and state['flight'] is None
    session = open_session(connected)
    if peer == 'label':
        with pytest.raises(CommitConflict):
            session.flush()
        assert json.loads(path.read_bytes())['pending'] == [suffix]
    else:
        session.flush()
        assert State(generated.bundles['r2']).entity(REF)['label'] == 'B'
        if peer == 'disjoint':
            assert State(generated.bundles['r2']).entity('parent/clip:b')['params']['text'] == 'Peer'
    body, key = generated.calls[-1]
    body = json.loads(body)
    assert body['commands'] == [suffix]
    assert body['base_revision_id'] == 'r1' and body['base_publication_id'] == 'pub1'
    assert key != 'A'
    assert client.reads == ['r0', 'r0']


def test_native_one_shot_retry_never_reads_or_recaptures(connected):
    client, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        open_session(connected).commit(label('Original'), idempotency_key='original')
    persisted = path.read_bytes()
    session = open_session(connected)
    with pytest.raises(TimelineEditError, match='pending intent differs'):
        session.commit(label('Changed'))
    assert path.read_bytes() == persisted
    session.commit(label('Original'))
    assert generated.calls[0] == generated.calls[1]
    assert client.reads == ['r0']


def test_stale_captured_claims_are_refused_without_refresh_or_persistence(connected):
    _, generated, path = connected
    session = open_session(connected)
    command = capture_track_set(initial_bundle(), REF, values={'label': 'B'})
    session.queue(label('A'))
    persisted = path.read_bytes()
    with pytest.raises(CommandError):
        session.queue(command)
    assert path.read_bytes() == persisted
    assert generated.calls == []


@pytest.mark.parametrize('damage', ['unknown-op', 'patch', 'inverse', 'restore', 'null', 'overlap'])
def test_native_ingress_rejects_unsupported_operations_and_open_patches(connected, damage):
    _, generated, path = connected
    session = open_session(connected)
    command = label('Picture')
    if damage in ('unknown-op', 'inverse', 'restore'):
        command['op'] = {'unknown-op': 'track.patch', 'inverse': 'timeline.inverse',
                         'restore': 'timeline.restore'}[damage]
        if damage == 'inverse':
            command.update(select=None, args={'publications': ['pub0']})
    elif damage == 'patch':
        command['args']['values']['opaque'] = 'overwrite'
    elif damage == 'null':
        command['args']['values']['label'] = None
    else:
        command['args']['clear'] = ['label']
    persisted = path.read_bytes()
    with pytest.raises(TimelineEditError):
        session.commit(command)
    assert path.read_bytes() == persisted
    assert generated.calls == []
