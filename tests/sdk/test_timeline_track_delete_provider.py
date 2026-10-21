"""Track deletion through the real provider and authenticated accepted history."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline._track_commands import capture_track_delete
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document, literal_row
from tests.editing_conformance.test_recipe_m2_track_delete import TARGET, deletion_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
    runtime_abi,  # noqa: F401 (shared autouse Runtime ABI fixture)
    track_create,
)
from tests.sdk.test_timeline_commit_provider_document import document_fixture


def capture(realm, ref=TARGET):
    return capture_track_delete(bundle_from_document(realm.documents[realm.head['revision_id']]), ref)


def test_provider_exact_order_opaque_absence_reload_inverse_redo():
    realm = DetachedRealm(deletion_document())
    original = copy.deepcopy(realm.documents[realm.head['revision_id']])
    deleted = realm.call([capture(realm)])
    document = deleted['data']['canonical_document']
    tracks = document['parent_revision']['payload']['config']['tracks']
    assert [row['id'] for row in tracks] == ['before', 'picture']
    assert realm.documents[realm.head['revision_id']] == document
    for key in ('shot_revisions', 'internal_timeline_revisions', 'dependency_manifest'):
        assert document[key] == original[key]
    undone = realm.call([inverse([deleted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == original
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == document
    assert realm.call([inverse([redone['receipt']['receipt_id']])])['data']['canonical_document'] == original


def test_stale_delete_preserves_independent_move_and_other_track_label_then_undo():
    realm = DetachedRealm(deletion_document())
    base = copy.deepcopy(realm.head)
    command = capture(realm)
    realm.call([realm.move(on=2)])
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    realm.call([capture_track_set(bundle, 'parent/track:picture', values={'label': 'New label'})])
    head_document = copy.deepcopy(realm.documents[realm.head['revision_id']])
    deleted = realm.call([command], base=base)
    payload = deleted['data']['canonical_document']['parent_revision']['payload']
    assert payload['clips'] == head_document['parent_revision']['payload']['clips']
    assert payload['config']['tracks'][-1]['label'] == 'New label'
    undone = realm.call([inverse([deleted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == head_document


def test_new_consumer_stale_delete_refuses_without_partial_publication():
    realm = DetachedRealm(empty_document())
    realm.call([track_create('first-track')])
    base = copy.deepcopy(realm.head)
    command = capture(realm, 'parent/track:first-track')
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    realm.call([capture_clip_add(bundle, 'parent', literal_row())])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected):
        realm.call([command], base=base)
    assert (realm.head, realm.entries, realm.documents) == before


def test_created_then_deleted_track_id_is_retired_and_guarded_redo_keeps_same_id():
    realm = DetachedRealm(empty_document())
    realm.call([track_create('reserved-track')])
    original = copy.deepcopy(realm.documents[realm.head['revision_id']])
    deleted = realm.call([capture(realm, 'parent/track:reserved-track')])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected) as error:
        realm.call([track_create('reserved-track')])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    assert (realm.head, realm.entries, realm.documents) == before
    restored = realm.call([inverse([deleted['receipt']['receipt_id']])])
    assert restored['data']['canonical_document'] == original
    redone = realm.call([inverse([restored['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == deleted['data']['canonical_document']


def test_deleted_bootstrap_track_id_must_also_stay_retired():
    realm = DetachedRealm(deletion_document())
    realm.call([capture(realm)])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected) as error:
        realm.call([track_create('empty')])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    assert (realm.head, realm.entries, realm.documents) == before


def test_deleted_track_own_write_aba_and_late_invalid_batch_refuse_atomically():
    realm = DetachedRealm(deletion_document())
    base = copy.deepcopy(realm.head)
    command = capture(realm)
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    realm.call([capture_track_set(bundle, TARGET, values={'label': 'Changed'})])
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    realm.call([capture_track_set(bundle, TARGET, clear=['label'])])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected) as error:
        realm.call([command], base=base)
    assert error.value.failure['details']['reason'] == 'intervening_write'
    bad = {'schema_version': 1, 'op': 'track.delete', 'version': '1',
           'select': 'parent/track:before', 'args': {'cascade': True}}
    with pytest.raises(CommitRejected):
        realm.call([capture(realm), bad])
    assert (realm.head, realm.entries, realm.documents) == before


def test_parent_delete_keeps_original_shared_shot_closure_and_provider_restores_original_pin():
    from astrid.sdk.timeline.commit import _digest

    document = document_fixture()
    parent = document['parent_revision']
    parent['payload']['config']['tracks'].insert(0, {'id': 'empty', 'kind': 'visual'})
    parent['content_digest'] = _digest(parent['payload'])
    realm = DetachedRealm(document)
    deleted = realm.call([capture(realm)])
    for key in ('shot_revisions', 'internal_timeline_revisions', 'dependency_manifest'):
        assert deleted['data']['canonical_document'][key] == document[key]
    restored = realm.call([inverse([deleted['receipt']['receipt_id']])])
    assert restored['data']['canonical_document'] == document
