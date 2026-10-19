"""Scalar acceptance/reload/inverse through the real native provider and recorder."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params, capture_track_set
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi as runtime_abi,
)


def current(realm):
    return bundle_from_document(realm.documents[realm.head['revision_id']])


@pytest.mark.xfail(strict=True, reason='M2 inverse primitives must restore the original shared source closure after occurrence materialization')
def test_committed_move_then_parent_label_and_occurrence_params_reload_undo_redo():
    realm = DetachedRealm()
    moved = realm.call([realm.move()])
    moved_document = moved['data']['canonical_document']
    bundle = current(realm)
    label = capture_track_set(bundle, 'parent/track:picture', values={'label': 'Picture'})
    local = execute(bundle, [label]).bundle
    params = capture_clip_set_params(local, 'occurrence:occ-a/clip:clip-a',
                                     values={'null': None, 'opaque': {'keep': [False, {}, '']}})
    result = realm.call([label, params])
    assert result['data']['commands'] == [label, params]
    document = result['data']['canonical_document']
    reloaded = bundle_from_document(json.loads(json.dumps(document)))
    assert State(reloaded).entity('parent/track:picture')['label'] == 'Picture'
    assert State(reloaded).entity('parent/clip:clip-a')['at'] == 3.003
    assert State(reloaded).entity('occurrence:occ-a/clip:clip-a')['params'] == {
        'null': None, 'opaque': {'keep': [False, {}, '']}}
    assert 'params' not in State(reloaded).entity('occurrence:occ-b/clip:clip-a')
    assert 'params' not in State(reloaded).entity('parent/clip:clip-a')
    assert moved_document['shot_revisions'][0] in document['shot_revisions']
    assert moved_document['internal_timeline_revisions'][0] in document['internal_timeline_revisions']
    undo = realm.call([inverse([result['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == moved_document
    redo = realm.call([inverse([undo['receipt']['receipt_id']])])
    assert redo['data']['canonical_document'] == document


def test_move_then_parent_label_reload_and_exact_inverse_redo():
    realm = DetachedRealm()
    moved = realm.call([realm.move()])
    command = capture_track_set(current(realm), 'parent/track:picture', values={'label': 'Picture'})
    accepted = realm.call([command])
    assert State(current(realm)).entity('parent/clip:clip-a')['at'] == 3.003
    assert State(current(realm)).entity('parent/track:picture')['label'] == 'Picture'
    undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == moved['data']['canonical_document']
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


def test_occurrence_scalar_inverse_restores_fields_and_redo_after_accepted_reload():
    realm = DetachedRealm()
    ref = 'occurrence:occ-a/clip:clip-a'
    original = copy.deepcopy(State(current(realm)).entity(ref))
    accepted = realm.call([capture_clip_set_params(current(realm), ref, values={'null': None})])
    undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
    assert State(current(realm)).entity(ref) == original
    assert 'params' not in State(current(realm)).entity('occurrence:occ-b/clip:clip-a')
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


def test_disjoint_param_leaf_rebase_survives_materialization_and_keeps_original_claims():
    realm = DetachedRealm()
    ref = 'occurrence:occ-a/clip:clip-a'
    realm.call([capture_clip_set_params(current(realm), ref, values={'x': 0, 'y': None})])
    base, original = copy.deepcopy(realm.head), current(realm)
    a = capture_clip_set_params(original, ref, values={'x': 1})
    b = capture_clip_set_params(original, ref, values={'y': False})
    first = realm.call([a])
    result = realm.call([b], base=base)
    assert result['data']['status'] == 'rebased'
    assert result['data']['commands'] == [b]
    assert State(current(realm)).entity(ref)['params'] == {'x': 1, 'y': False}
    undo = realm.call([inverse([result['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == first['data']['canonical_document']


def test_dependent_original_capture_handoff_after_move_ack_and_same_child_revision_change():
    realm = DetachedRealm()
    original = current(realm)
    move = realm.move()
    local = execute(original, [move]).bundle
    b = capture_track_set(local, 'parent/track:picture', values={'label': 'After move'})
    sealed = json.dumps(b, sort_keys=True)
    realm.call([move])
    accepted = realm.call([b])
    assert json.dumps(accepted['data']['commands'][0], sort_keys=True) == sealed
    assert State(current(realm)).entity('parent/clip:clip-a')['at'] == 3.003
    ref = 'occurrence:occ-a/clip:clip-a'
    # Author B over local A before A has materialized a shared source occurrence.
    a = capture_clip_set_params(current(realm), ref, values={'x': 1, 'y': None})
    local = execute(current(realm), [a]).bundle
    b = capture_clip_set_params(local, ref, values={'y': 2})
    sealed = copy.deepcopy(b)
    realm.call([a])
    realm.call([capture_clip_set_params(current(realm), ref, values={'x': 3})])
    accepted = realm.call([b])
    assert accepted['data']['commands'] == [sealed]
    assert State(current(realm)).entity(ref)['params'] == {'x': 3, 'y': 2}


@pytest.mark.parametrize('op', ['track.set', 'clip.set-params'])
@pytest.mark.parametrize('aba', [False, True])
def test_scalar_unchanged_publications_and_aba_refuse_guarded_undo(op, aba):
    realm = DetachedRealm()

    def capture(value):
        if op == 'track.set':
            return capture_track_set(current(realm), 'parent/track:picture', values={'label': value})
        return capture_clip_set_params(current(realm), 'parent/clip:clip-a', values={'literal': value})

    original = realm.call([capture('same')])
    revision = realm.head['revision_id']
    if aba:
        realm.call([capture('away')])
    last = realm.call([capture('same')])
    assert realm.head['revision_id'] == revision
    assert last['receipt']['receipt_id'] != original['receipt']['receipt_id']
    record = realm.entries[-1]['records']['commands'][0]
    if not aba:
        assert any(write['before'] == write['after'] for write in record['writes'])
    before = copy.deepcopy(realm.head)
    with pytest.raises(CommitRejected) as error:
        realm.call([inverse([original['receipt']['receipt_id']])])
    assert error.value.failure['details']['reason'] == 'intervening_write'
    assert realm.head == before


def test_null_assignment_then_explicit_clear_accepted_reload_and_exact_inverse():
    realm = DetachedRealm()
    ref = 'parent/clip:clip-a'
    first = realm.call([capture_clip_set_params(current(realm), ref,
                                              values={'null': None, 'unknown': {'literal': [None, '']}})])
    cleared = realm.call([capture_clip_set_params(current(realm), ref, clear=['null'])])
    assert State(current(realm)).entity(ref)['params'] == {'unknown': {'literal': [None, '']}}
    restored = realm.call([inverse([cleared['receipt']['receipt_id']])])
    assert restored['data']['canonical_document'] == first['data']['canonical_document']
    assert State(current(realm)).entity(ref)['params']['null'] is None


def test_original_param_claim_conflict_and_malformed_batch_do_not_accept_partially():
    realm = DetachedRealm()
    ref = 'parent/clip:clip-a'
    original = capture_clip_set_params(current(realm), ref, values={'x': 2})
    realm.call([capture_clip_set_params(current(realm), ref, values={'x': 3})])
    before, count = copy.deepcopy(realm.head), len(realm.entries)
    with pytest.raises(CommitRejected) as error:
        realm.call([original])
    assert error.value.failure['details']['reason'] == 'dependency_changed'
    label = capture_track_set(current(realm), 'parent/track:picture', values={'label': 'New'})
    malformed = dict(original, args={'values': {'x': 4}, 'clear': [], 'config': {}})
    with pytest.raises(CommitRejected):
        realm.call([label, malformed])
    assert realm.head == before and len(realm.entries) == count
