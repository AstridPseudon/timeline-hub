"""Ordinary attached verbs capture intent before exposing a local preview."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.sync import CommitConflict
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance.test_recipe_clip_scalar_fields import app_closure
from tests.editing_conformance.test_recipe_m2_clip_trim import media_document
from tests.editing_conformance.test_native_word_anchor_vectors import fixture as word_anchor_fixture
from tests.sdk import test_timeline_sync as sync

connected = sync.connected
open_session = sync.open_session


def attached(connected, bundle=None):
    _, generated, _ = connected
    if bundle is not None:
        generated.bundles['r0'] = copy.deepcopy(bundle)
        generated.bundles['r0'].update(project_id='p', timeline_id='t')
        for capture in bundle.get('source_mapping', {}).get('pinned_documents', []):
            generated.verified_documents[('p', tuple(sorted(capture['pin'].items())))] = capture
    return Checkout.attach(open_session(connected))


def pending(connected):
    return json.loads(connected[2].read_bytes())


def anchored_bundle():
    bundle, pin, content = word_anchor_fixture()
    pin['document_id'] = transcript_document_id('p', content['media_id'], content['source_id'])
    for capture in bundle['source_mapping']['pinned_documents']:
        capture['pin'] = pin
        capture['document']['document_id'] = pin['document_id']
        capture['document']['project_id'] = 'p'
    word = content['segments'][0]['words'][0]
    choice = {
        'source': 'occurrence:occ-a/clip:voice',
        'document': pin,
        'word_ids': [word['id']],
    }
    return bundle, {'field': 'on', 'declaration': f'"{word["text"]}"', 'choice': choice}


@pytest.mark.parametrize('type_key', ['clipType', 'clip_type'])
def test_raw_element_alias_keeps_canvas_units_after_acceptance(connected, type_key):
    row = State(connected[1].bundles['r0']).entity('parent/clip:a')
    row.pop('clipType')
    row[type_key] = 'am-sprite'
    row['params'] = {'x': 27, 'scale': 6, 'opaque': [None, False, 1, 1.0]}
    tl = attached(connected)
    tl.clip('a').set(x=600)
    command = pending(connected)['pending'][0]
    assert command['expect']['parent/clip:a::params.x'] == {'state': 'present', 'value': 27}
    assert {'ref': 'parent/clip:a', 'path': [type_key],
            'state': {'state': 'present', 'value': 'am-sprite'}} in command['reads']
    accepted = tl.flush()
    stored = State(bundle_from_document(accepted['data']['canonical_document'])).entity('parent/clip:a')
    assert stored['params'] == {'x': 100, 'scale': 6, 'opaque': [None, False, 1, 1.0]}
    assert stored[type_key] == 'am-sprite'
    assert ('clip_type' if type_key == 'clipType' else 'clipType') not in stored
    assert accepted['data']['commands'] == [command]


def test_move_is_durable_before_preview_and_unchanged_write_is_captured(connected, monkeypatch):
    tl = attached(connected)
    clip = tl.clip('a')
    before = copy.deepcopy(tl.bundle)
    write = tl.session.outbox.write

    def observe(state):
        assert tl.bundle == before
        assert state['pending'][0]['op'] == 'clip.move'
        write(state)

    monkeypatch.setattr(tl.session.outbox, 'write', observe)
    assert clip.on(0) is clip
    first = pending(connected)['pending'][0]
    assert first['expect']['parent/clip:a::at'] == {'state': 'present', 'value': 0}
    monkeypatch.setattr(tl.session.outbox, 'write', write)
    assert clip.on(2) is clip
    assert clip.start == 2
    assert len(pending(connected)['pending']) == 2
    assert tl._journal == []


def test_failed_durable_write_keeps_preview_unchanged(connected, monkeypatch):
    tl = attached(connected)
    before = copy.deepcopy(tl.bundle)
    state = pending(connected)

    def fail(state):
        raise OSError('disk full')

    monkeypatch.setattr(tl.session.outbox, 'write', fail)
    with pytest.raises(OSError, match='disk full'):
        tl.clip('a').on(2)
    assert tl.bundle == before
    assert pending(connected) == state


def test_literal_params_clear_and_opaque_values_use_one_captured_command(connected):
    tl = attached(connected)
    clip = tl.clip('a')
    clip.set(text='next', opaque={'array': [None, False, 0]}, _allow_new=True)
    clip.set_param('text', None)
    assert clip.params == {'opaque': {'array': [None, False, 0]}}
    calls = pending(connected)['pending']
    assert [call['op'] for call in calls] == ['clip.set-params', 'clip.set-params']
    assert calls[1]['args'] == {'values': {}, 'clear': ['text']}
    accepted = tl.flush()
    assert accepted['data']['commands'] == calls
    loaded = Checkout.attach(open_session(connected))
    assert loaded.clip('a').params == clip.params
    loaded.undo([accepted['receipt']['receipt_id']])
    assert loaded.clip('a').params == {'text': 'café'}


def test_move_then_trim_then_reload_preserves_source_hold_and_opaque_fields(connected):
    tl = attached(connected, bundle_from_document(media_document()))
    clip = tl.clip('parent/clip:clip-a')
    original = copy.deepcopy(clip.data)
    assert clip.on(3.003).trim(1, 5) is clip
    assert clip.start == 3.003
    assert clip.duration == 2
    assert clip.data['hold'] == 4
    assert clip.data['app']['astrid']['opaque'] == [None, False]
    assert original['from'] == 2
    reloaded = Checkout.attach(open_session(connected))
    assert reloaded.clip('parent/clip:clip-a').data == clip.data
    assert [call['op'] for call in pending(connected)['pending']] == ['clip.move', 'clip.trim']
    accepted = reloaded.flush()
    reloaded.undo([accepted['receipt']['receipt_id']])
    assert reloaded.clip('parent/clip:clip-a').data == original


def test_source_window_duration_follows_hold_and_windowless_stays_windowless(connected):
    original = bundle_from_document(media_document(hold=4, app={}))
    tl = attached(connected, original)
    clip = tl.clip('parent/clip:clip-a')
    clip.hold_for('18f')
    assert clip.duration == pytest.approx(.6006)
    assert clip.data['to'] - clip.data['from'] == pytest.approx(clip.data['hold'])
    assert pending(connected)['pending'][-1]['op'] == 'clip.trim'
    tl = attached(connected)
    # The other parent clip is windowless. Raw source hold never fabricates one.
    other = tl.clip('parent/clip:clip-b')
    other.hold_for(3)
    assert other.data['hold'] == 3.003
    assert 'from' not in other.data and 'to' not in other.data


def test_attached_word_anchor_reuses_clip_anchor_carrier_and_pinned_capture(connected):
    bundle, value = anchored_bundle()
    tl = attached(connected, bundle)
    clip = tl.clip('parent/clip:clip-a')
    before_at = clip.data['at']

    clip.set(on=value)

    command = pending(connected)['pending'][0]
    assert command['op'] == 'clip.anchor'
    assert command['intent'] == {'anchor': 'follow'}
    assert command['args'] == value
    assert clip.data['app']['astrid']['word_anchors']['on'] == value['choice']
    assert clip.data['at'] != before_at

    accepted = tl.publish('attach one stable word')
    assert accepted['new_head'] == 'r1'
    assert accepted['message'] == 'attach one stable word'
    assert pending(connected)['pending'] == []


def test_attached_word_anchor_refuses_without_exact_capture_or_on_text(connected):
    bundle, value = anchored_bundle()
    bundle['source_mapping']['pinned_documents'] = []
    tl = attached(connected, bundle)
    before, state = copy.deepcopy(tl.bundle), pending(connected)

    with pytest.raises(TimelineEditError, match='exact transcript pin is missing'):
        tl.clip('parent/clip:clip-a').set(on=value)
    with pytest.raises(TimelineEditError, match='text-only or mixed values are unsupported'):
        tl.clip('parent/clip:clip-a').set(on='again')
    with pytest.raises(TimelineEditError, match='cannot be mixed'):
        tl.clip('parent/clip:clip-a').set(on=value, text='also')

    assert tl.bundle == before
    assert pending(connected) == state


def test_attached_word_anchor_hydrates_exact_pin_after_fresh_open_and_restart(connected):
    bundle, value = anchored_bundle()
    capture = copy.deepcopy(bundle['source_mapping']['pinned_documents'][0])
    bundle['source_mapping']['pinned_documents'] = []
    generated = connected[1]
    generated.verified_documents[('p', tuple(sorted(capture['pin'].items())))] = capture

    tl = attached(connected, bundle)
    tl.clip('parent/clip:clip-a').set(on=value)
    assert generated.verified_document_calls == [('p', capture['pin'])]
    assert tl.bundle['source_mapping']['pinned_documents'] == [capture]

    reloaded = Checkout.attach(open_session(connected))
    assert generated.verified_document_calls == [('p', capture['pin']), ('p', capture['pin'])]
    assert reloaded.bundle['source_mapping']['pinned_documents'] == [capture]
    assert reloaded._pending == tl._pending
    assert reloaded._basis == tl._basis


@pytest.mark.parametrize('mismatch', ['foreign', 'version', 'hash'])
def test_attached_word_anchor_refuses_verified_pin_mismatch_without_mutation(connected, mismatch):
    bundle, value = anchored_bundle()
    capture = copy.deepcopy(bundle['source_mapping']['pinned_documents'][0])
    bundle['source_mapping']['pinned_documents'] = []
    document = capture['document']
    if mismatch == 'foreign':
        document['project_id'] = 'foreign-project'
    elif mismatch == 'version':
        document['version'] = 2
    else:
        document['content']['segments'][0]['text'] = 'changed'
    generated = connected[1]
    generated.verified_documents[('p', tuple(sorted(capture['pin'].items())))] = capture
    tl = attached(connected, bundle)
    before, state = copy.deepcopy(tl.bundle), pending(connected)

    message = {
        'foreign': 'scope or version', 'version': 'scope or version',
        'hash': 'content bytes',
    }[mismatch]
    with pytest.raises(TimelineEditError, match=message):
        tl.clip('parent/clip:clip-a').set(on=value)
    assert tl.bundle == before
    assert pending(connected) == state


def test_attached_word_anchor_clear_uses_existing_clip_anchor_command(connected):
    bundle, value = anchored_bundle()
    tl = attached(connected, bundle)
    clip = tl.clip('parent/clip:clip-a')
    clip.set(on=value)
    clip.set(on=None)

    commands = pending(connected)['pending']
    assert [command['op'] for command in commands] == ['clip.anchor', 'clip.anchor']
    assert commands[1]['args'] == {'field': 'on', 'declaration': None, 'choice': None}
    assert 'on' not in clip.data['app']['astrid'].get('word_anchors', {})


@pytest.mark.parametrize('verb', [lambda clip: clip.on('word:later'), lambda clip: clip.until('end'),
                                  lambda clip: clip.slip(1), lambda clip: clip.set_track('other'),
                                  lambda clip: clip.set_look(opacity=.5),
                                  lambda clip: clip.set(opacity=.5, _allow_new=True),
                                  lambda clip: clip.set(text='ok', **{'states[0].at': 1})])
def test_unsupported_clip_families_leave_preview_and_outbox_intact(connected, verb):
    tl = attached(connected)
    before, state = copy.deepcopy(tl.bundle), pending(connected)
    with pytest.raises(TimelineEditError):
        verb(tl.clip('a'))
    assert tl.bundle == before
    assert pending(connected) == state


def test_selected_pack_params_never_consult_local_schema(connected, monkeypatch):
    bundle = connected[1].bundles['r0']
    State(bundle).entity('parent/clip:a')['elementRef'] = {'packId': 'selected', 'id': 'a', 'kind': 'element', 'revision': 'v1'}
    tl = attached(connected)
    before = pending(connected)
    from astrid.sdk import timeline_address

    def forbidden(*args):
        pytest.fail('selected pack edit used a local schema')

    monkeypatch.setattr(timeline_address, 'element_schema', forbidden)
    with pytest.raises(TimelineEditError, match='exact schema inputs'):
        tl.clip('a').set(text='next')
    assert pending(connected) == before


def test_raw_scope_isolates_shared_occurrence_even_with_colons_in_clip_id(connected):
    parent, shots, internals = app_closure()
    parent.update(project_id='p', timeline_id='t')
    for image in [*shots, *internals]:
        image['project_id'] = 'p'
    bundle = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    for owner in ('parent', 'occurrence:f2-occurrence', 'occurrence:shared-sibling'):
        State(bundle).collection(owner, 'clip')[0]['id'] = 'literal:colon'
    tl = attached(connected, bundle)
    with pytest.raises(TimelineEditError, match='one exact clip'):
        tl.clip('literal:colon')
    child = tl.clip('occurrence:f2-occurrence/clip:literal:colon')
    child.on(1)
    assert pending(connected)['pending'][0]['select'] == 'occurrence:f2-occurrence/clip:literal:colon'
    assert child.start == 1
    child.hold_for(11)
    assert child.data['hold'] == 11
    assert tl.clip('occurrence:shared-sibling/clip:literal:colon').data['hold'] == 12
    assert tl.clip('parent/clip:literal:colon').start == 0
    assert tl.clip('occurrence:shared-sibling/clip:literal:colon').start == 20


@pytest.mark.parametrize('conflicting', [False, True])
def test_lost_ack_reload_retains_dependent_trim_and_fresh_suffix_key(connected, conflicting):
    original = bundle_from_document(media_document(hold=4, app={}))
    tl = attached(connected, original)
    clip = tl.clip('parent/clip:clip-a')
    clip.on(3.003)
    generated = connected[1]
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        tl.flush(idempotency_key='A')
    flight = pending(connected)['flight']
    clip.trim(1, 5)
    suffix = pending(connected)['pending'][1]
    assert suffix['reads']
    # C advances the accepted head independently. A relevant original basis
    # change conflicts; an unrelated label permits the original B unchanged.
    generated.bundles['peer'] = copy.deepcopy(generated.bundles['r1'])
    if conflicting:
        State(generated.bundles['peer']).entity('parent/clip:clip-a')['from'] = 0
    else:
        State(generated.bundles['peer']).entity('parent/track:picture')['label'] = 'C'
    generated.head = {'revision_id': 'peer', 'publication_id': 'peer-publication'}
    tl = Checkout.attach(open_session(connected))
    assert pending(connected)['flight'] == flight
    assert tl.clip('parent/clip:clip-a').data['hold'] == 4
    tl.flush()
    assert generated.calls[0] == generated.calls[1] == (flight['body'].encode(), 'A')
    assert pending(connected)['pending'] == [suffix]
    if conflicting:
        with pytest.raises(CommitConflict):
            tl.flush()
        assert pending(connected)['pending'] == [suffix]
    else:
        result = tl.flush()
        assert result['data']['commands'] == [suffix]
        assert tl.clip('parent/clip:clip-a').start == 3.003
    assert generated.calls[-1][1] != 'A'


def test_attached_writers_and_unqueued_local_mutations_cannot_fallback(connected, monkeypatch):
    tl = attached(connected)
    for verb in (lambda: tl.publish(), lambda: tl.save(), lambda: tl.add('text', at=1),
                 lambda: tl.edit('group'), lambda: tl.retime()):
        with pytest.raises(TimelineEditError, match='held'):
            verb()
    tl.clip('a').params['text'] = 'uncaptured'
    with pytest.raises(TimelineEditError, match='unqueued local changes'):
        tl.clip('a').on(1)
    with pytest.raises(TimelineEditError, match='unqueued local changes'):
        tl.flush()
    assert pending(connected)['pending'] == []
    assert connected[1].calls == []


def test_stale_handle_does_not_recapture_another_outbox_writer(connected):
    tl = attached(connected)
    other = Checkout.attach(open_session(connected))
    other.clip('b').on(2)
    state = pending(connected)
    with pytest.raises(TimelineEditError, match='basis changed'):
        tl.clip('a').on(1)
    assert pending(connected) == state
