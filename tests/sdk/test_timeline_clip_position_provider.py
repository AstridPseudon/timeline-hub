"""Position panel leaves through the native commit provider, without sockets."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_clip_position import FIELDS, PARENT
from tests.editing_conformance.test_recipe_clip_scalar_fields import CHILD, clip
from tests.sdk.test_timeline_clip_scalar_provider import app_document, current
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
    runtime_abi,  # noqa: F401 (shared autouse Runtime ABI fixture)
)


@pytest.mark.parametrize('ref', [PARENT, CHILD])
def test_provider_box_crop_and_full_reset_roundtrip_preserves_opaque_and_shared_occurrence(ref):
    realm = DetachedRealm(app_document())
    original = copy.deepcopy(realm.documents[realm.head['revision_id']])
    first = realm.call([capture_clip_set(current(realm), ref, values=dict(zip(
        FIELDS, [-120.5, 4000, 0, -1, .125, .25, -2, 3])))])
    positioned = copy.deepcopy(first['data']['canonical_document'])
    assert clip(current(realm), 'occurrence:shared-sibling/clip:f2-agent-clip') == clip(
        current(DetachedRealm(original)), 'occurrence:shared-sibling/clip:f2-agent-clip')
    undo_set = realm.call([inverse([first['receipt']['receipt_id']])])
    assert undo_set['data']['canonical_document'] == original
    redo_set = realm.call([inverse([undo_set['receipt']['receipt_id']])])
    assert redo_set['data']['canonical_document'] == positioned
    reset = realm.call([capture_clip_set(current(realm), ref, clear=FIELDS)])
    assert all(field not in clip(current(realm), ref) for field in FIELDS)
    # A new reset publication has new revision IDs even when raw content
    # returns to its original value. Compare every owner's complete config.
    for owner in ('parent', 'occurrence:f2-occurrence', 'occurrence:shared-sibling'):
        assert State(current(realm)).config(owner) == State(current(DetachedRealm(original))).config(owner)
    undo_reset = realm.call([inverse([reset['receipt']['receipt_id']])])
    assert undo_reset['data']['canonical_document'] == positioned
    redo_reset = realm.call([inverse([undo_reset['receipt']['receipt_id']])])
    assert redo_reset['data']['canonical_document'] == reset['data']['canonical_document']


@pytest.mark.parametrize('other', ['y', 'params'])
def test_provider_original_position_capture_rebases_independently_and_undo_keeps_later_leaf(other):
    realm = DetachedRealm(app_document())
    base = copy.deepcopy(realm.head)
    command = capture_clip_set(current(realm), CHILD, values={'x': -10})
    sealed = copy.deepcopy(command)
    changed = (capture_clip_set(current(realm), CHILD, values={'y': 123}) if other == 'y' else
               capture_clip_set_params(current(realm), CHILD, values={'vendor.position/v1': [None, False]}))
    realm.call([changed])
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    accepted = realm.call([command], base=base)
    assert accepted['data']['status'] == 'rebased'
    assert accepted['data']['commands'] == [sealed]
    assert clip(current(realm), CHILD)['x'] == -10
    undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == before
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


@pytest.mark.parametrize('field', FIELDS)
def test_provider_same_leaf_stale_capture_refuses_atomically(field):
    realm = DetachedRealm(app_document())
    base = copy.deepcopy(realm.head)
    stale = capture_clip_set(current(realm), CHILD, values={field: 100})
    realm.call([capture_clip_set(current(realm), CHILD, values={field: 200})])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected):
        realm.call([stale], base=base)
    assert (realm.head, realm.entries, realm.documents) == before


@pytest.mark.parametrize('field', FIELDS)
@pytest.mark.parametrize('aba', [False, True])
def test_provider_unchanged_position_write_and_aba_refuse_old_inverse(field, aba):
    realm = DetachedRealm(app_document())
    first = realm.call([capture_clip_set(current(realm), CHILD, values={field: 10})])
    if aba:
        realm.call([capture_clip_set(current(realm), CHILD, values={field: 20})])
    realm.call([capture_clip_set(current(realm), CHILD, values={field: 10})])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected) as error:
        realm.call([inverse([first['receipt']['receipt_id']])])
    assert error.value.failure['details']['reason'] == 'intervening_write'
    assert (realm.head, realm.entries, realm.documents) == before


def test_provider_position_captured_after_move_preserves_command_and_authored_timing():
    realm = DetachedRealm(app_document())
    move = capture_move(current(realm), CHILD, 4)
    local = execute(current(realm), [move]).bundle
    position = capture_clip_set(local, CHILD, values={'x': -10, 'y': 100})
    realm.call([move])
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    accepted = realm.call([position])
    assert accepted['data']['commands'] == [position]
    assert clip(current(realm), CHILD) == dict(clip(local, CHILD), x=-10, y=100)
    undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == before
