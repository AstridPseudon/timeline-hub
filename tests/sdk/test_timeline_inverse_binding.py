from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_doc_patch_v2 import change, patch, submit
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedRealm, inverse
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.mark.parametrize('mismatched', [False, True])
def test_raw_physical_scope_records_cannot_authorize_inverse(mismatched):
    realm = DetachedRealm()
    landed = submit(realm, patch(change(['name'], present('Renamed Film'), 'B')),
                    reads=[{'kind': 'scope', 'ref': 'timeline', 'path': []}])
    records = copy.deepcopy(realm.entries[-1]['records']['commands'])
    if mismatched:
        records[0]['bindings'][0]['revision_id'] = 'different-revision'
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    original = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='authenticated physical binding normalization') as error:
        execute(bundle, [inverse([landed['receipt']['receipt_id']])], inverse_records=records)
    assert error.value.kind == 'history_unavailable'
    assert bundle == original


@pytest.mark.parametrize('later_write', [False, True])
def test_provider_scope_inverse_uses_authenticated_closure_and_keeps_later_guard(monkeypatch, later_write):
    realm = DetachedRealm()
    landed = submit(realm, patch(change(['name'], present('Renamed Film'), 'B')),
                    reads=[{'kind': 'scope', 'ref': 'timeline', 'path': []}])
    record = realm.entries[-1]['records']['commands'][0]
    scopes = [binding for binding in record['bindings'] if binding['ref'] == 'timeline']
    assert {binding['physical_ref'] for binding in scopes} == {
        'parent', 'shot-revision:shot-1', 'internal-revision:internal-1'}
    assert realm.head['revision_id'] != scopes[0]['revision_id']
    if later_write:
        submit(realm, patch(change(['name'], present('B'), 'B')), reads=[])
    before = copy.deepcopy((realm.head, realm.entries))
    original_entity = State.entity

    def entity(state, ref, *, optional=False):
        assert ref != 'timeline', 'timeline scope must not dispatch through State.entity'
        return original_entity(state, ref, optional=optional)

    monkeypatch.setattr(State, 'entity', entity)
    call = inverse([landed['receipt']['receipt_id']])
    if later_write:
        with pytest.raises(CommitRejected) as error:
            submit(realm, call, reads=[])
        assert error.value.failure['details']['reason'] == 'intervening_write'
        assert (realm.head, realm.entries) == before
    else:
        undone = submit(realm, call, reads=[])
        assert undone['data']['canonical_document']['parent_revision']['payload']['name'] == 'Renamed Film'
        redone = submit(realm, inverse([undone['receipt']['receipt_id']]), reads=[])
        assert redone['data']['canonical_document']['parent_revision']['payload']['name'] == 'B'
