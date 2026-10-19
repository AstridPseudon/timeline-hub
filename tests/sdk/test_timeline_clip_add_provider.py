"""The actual native provider accepts and reserves literal clip identities."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document, literal_row
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
    runtime_abi,  # noqa: F401 (shared autouse Runtime ABI fixture)
    track_create,
)


def test_first_clip_provider_closed_reload_reservations_inverse_redo():
    realm = DetachedRealm(empty_document())
    empty = copy.deepcopy(realm.documents[realm.head['revision_id']])
    realm.call([track_create('first-track')])
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    captured = capture_clip_add(bundle_from_document(before), 'parent', literal_row())
    created = realm.call([captured])
    document = created['data']['canonical_document']
    assert document['parent_revision']['payload']['clips'] == [literal_row()]
    assert document['parent_revision']['payload']['config']['clips'] == [literal_row()]
    assert realm.documents[realm.head['revision_id']] == document
    for key in ('shot_revisions', 'internal_timeline_revisions', 'dependency_manifest'):
        assert document[key] == empty[key]
    occupied = copy.deepcopy(realm.head)
    raw = {key: captured[key] for key in ('schema_version', 'op', 'version', 'select', 'args')}
    with pytest.raises(CommitRejected) as error:
        realm.call([raw])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    assert realm.head == occupied
    undone = realm.call([inverse([created['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == before
    retired, history = copy.deepcopy(realm.head), copy.deepcopy(realm.entries)
    with pytest.raises(CommitRejected) as error:
        realm.call([raw])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    assert realm.head == retired and realm.entries == history
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == document
    assert redone['data']['commands'][0]['created'] == ['parent/clip:first-clip']
    assert realm.call([inverse([redone['receipt']['receipt_id']])])['data']['canonical_document'] == before


def test_empty_to_nonempty_one_explicit_command_batch_has_no_hidden_lane_or_id():
    realm = DetachedRealm(empty_document())
    add = {'schema_version': 1, 'op': 'clip.add', 'version': '1', 'select': 'parent',
           'args': {'row': literal_row()}}
    accepted = realm.call([track_create('first-track'), add])
    records = realm.entries[-1]['records']['commands']
    assert [r['created'] for r in records] == [
        [{'ref': 'parent/track:first-track', 'kind': 'track', 'owner': 'parent'}],
        [{'ref': 'parent/clip:first-clip', 'kind': 'clip', 'owner': 'parent'}]]
    payload = accepted['data']['canonical_document']['parent_revision']['payload']
    assert [t['id'] for t in payload['config']['tracks']] == ['first-track']
    assert payload['clips'] == [literal_row()]


@pytest.mark.parametrize('changes', [{'track': 'missing'}, {'asset': 'x'}, {'from': 0}, {'at': -1}, {'hold': 0}])
def test_invalid_first_clip_batch_cannot_partially_create_the_track(changes):
    realm = DetachedRealm(empty_document())
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    add = {'schema_version': 1, 'op': 'clip.add', 'version': '1', 'select': 'parent',
           'args': {'row': literal_row(**changes)}}
    with pytest.raises(CommitRejected):
        realm.call([track_create('first-track'), add])
    assert (realm.head, realm.entries, realm.documents) == before
    assert realm.prepared == realm.accepted == []
