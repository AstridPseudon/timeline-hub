"""History authority for init uses the existing scoped read/accept port."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_initialize import capture_initialize_raw
from tests.editing_conformance.test_pristine_initialize import (
    GOLDEN,
    batch,
    empty_document,
)
from tests.editing_conformance.test_pristine_raw_initialize import RAW_CONFIG
from tests.sdk import test_timeline_commit_provider as provider

runtime_abi = provider.runtime_abi


def inverse(publication):
    return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
            'args': {'publications': [publication]}}


def test_init_undo_redo_and_reinitialization_requires_bootstrap_history():
    realm = provider.DetachedRealm(empty_document())
    calls = batch(bundle_from_document(empty_document()))
    original = copy.deepcopy(realm.head)
    accepted = realm.call(calls)
    assert accepted['data']['canonical_document']['parent_revision']['payload'] == GOLDEN['app_parent']
    undone = realm.call([inverse(accepted['receipt']['receipt_id'])])
    assert undone['data']['canonical_document'] == empty_document()
    assert realm.head['revision_id'] == original['revision_id']
    assert realm.head['publication_id'] != original['publication_id']
    for base in (None, original):
        before = copy.deepcopy(realm.head)
        with pytest.raises(provider.CommitRejected) as error:
            realm.call(calls, base=base)
        assert error.value.failure['details']['reason'] == 'not_pristine'
        assert realm.head == before
    redone = realm.call([inverse(undone['receipt']['receipt_id'])])
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


@pytest.mark.parametrize('intent,previous', [('legacy_unknown', None),
                                          ('recorded', None), ('bootstrap', {'publication_id': 'prior'})])
def test_equal_bytes_without_pristine_history_cannot_initialize(intent, previous):
    realm = provider.DetachedRealm(empty_document())
    realm.entries[0].update(intent=intent, previous=previous)
    before = copy.deepcopy(realm.head)
    with pytest.raises(provider.CommitRejected) as error:
        realm.call(batch(bundle_from_document(empty_document())))
    assert error.value.failure['details']['reason'] == 'not_pristine'
    assert realm.head == before and realm.accepted == []


def test_cas_retry_cannot_initialize_over_edit_then_undo_equal_bytes():
    realm = provider.DetachedRealm(empty_document())
    calls = batch(bundle_from_document(empty_document()))

    def edit_and_undo():
        created = realm.call([{'schema_version': 1, 'op': 'track.create', 'version': '1',
                              'select': 'parent', 'args': {'row': {'id': 'later', 'kind': 'visual'}}}])
        realm.call([inverse(created['receipt']['receipt_id'])])

    realm.before_accept = edit_and_undo
    with pytest.raises(provider.CommitRejected) as error:
        realm.call(calls)
    assert error.value.failure['details']['reason'] == 'not_pristine'
    assert realm.documents[realm.head['revision_id']] == empty_document()
    assert len(realm.accepted) == 2


def test_provider_carries_raw_config_and_keeps_init_history_boundary():
    realm = provider.DetachedRealm(empty_document())
    command = capture_initialize_raw(bundle_from_document(empty_document()),
                                     name='Custom', slug='custom', config=RAW_CONFIG)
    accepted = realm.call([command])
    payload = accepted['data']['canonical_document']['parent_revision']['payload']
    assert payload['config'] == RAW_CONFIG
    undone = realm.call([inverse(accepted['receipt']['receipt_id'])])
    assert undone['data']['canonical_document'] == empty_document()
    with pytest.raises(provider.CommitRejected) as error:
        realm.call([command])
    assert error.value.failure['details']['reason'] == 'not_pristine'
