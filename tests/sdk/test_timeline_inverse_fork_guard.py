"""A retained shared source does not hide consumers of its authored fork."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import ABSENT
from tests.editing_conformance.test_doc_patch_v2 import change, patch, step, submit
from tests.sdk.test_timeline_clip_scalar_provider import CLEAR, app_document, current
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedRealm, inverse
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


def land(realm, command, *, dry_run=False):
    return submit(realm, command, label='Guard fork output', merge='fields', reads=[],
                  steps=[step('edit', 0, command, reads=[])], dry_run=dry_run)


@pytest.mark.parametrize('selected', [False, True], ids=['whole', 'step'])
@pytest.mark.parametrize('consumer', [False, True], ids=['equal-clear', 'declared-read'])
def test_fork_output_guard_survives_reachable_shared_source(selected, consumer):
    realm = DetachedRealm(app_document())
    first = land(realm, capture_clip_set(current(realm), CLEAR, clear=['asset']))
    source = copy.deepcopy(realm.entries[-1])
    materialization = next(binding for binding in source['records']['commands'][0]['bindings']
                           if binding['key'] == 'commit.materialization'
                           and binding['physical_ref'].startswith('internal-revision:'))
    document = first['data']['canonical_document']
    roots = {'internal-revision:' + row['revision_id']
             for row in document['internal_timeline_revisions']}
    assert {materialization['physical_ref'], materialization['successor']} <= roots
    assert first['receipt']['result'] == first['data']
    if consumer:
        command = patch(change(['meta'], ABSENT, {'guard': {'note': 'kept'}}))
        submit(realm, command, label='Consume fork', merge='fields', steps=[step('note', 0, command)],
               reads=[{'kind': 'field', 'ref': materialization['successor'],
                       'path': ['clips', 'id:f2-agent-clear-clip', 'asset'], 'state': ABSENT}])
    else:
        last = land(realm, capture_clip_set(current(realm), CLEAR, clear=['asset']))
        record = realm.entries[-1]['records']['commands'][0]
        assert record['writes'] == [{'ref': CLEAR, 'path': ['asset'],
                                     'before': ABSENT, 'after': ABSENT}]
        assert realm.entries[-1]['records']['steps'][0]['patch'] == []
        assert first['receipt']['receipt_id'] != last['receipt']['receipt_id']
    command = inverse([first['receipt']['receipt_id']])
    if selected:
        command['args']['steps'] = {first['receipt']['receipt_id']: ['edit']}
    before = copy.deepcopy((realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared))
    for dry_run in (True, False):
        with pytest.raises(CommitRejected) as error:
            land(realm, command, dry_run=dry_run)
        details = error.value.failure['details']
        assert details['reason'] == ('inverse_conflict' if consumer else 'intervening_write')
        assert details['code'] == details['reason']
        assert details['hint'] and details['suggested_command']
        assert isinstance(details['path'], list)
        assert before == (realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared)
    assert realm.entries[1] == source


def test_fork_output_guard_allows_independent_parent_edit_and_preview_redo():
    realm = DetachedRealm(app_document())
    first = land(realm, capture_clip_set(current(realm), CLEAR, clear=['asset']))
    note = patch(change(['meta'], ABSENT, {'guard': {'note': 'kept'}}))
    land(realm, note)
    command = inverse([first['receipt']['receipt_id']])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared))
    preview = land(realm, command, dry_run=True)
    assert preview['receipt'] is None
    assert preview['data']['would_status'] == 'accepted'
    assert before == (realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared)
    undone = land(realm, command)
    assert undone['data']['canonical_document'] == preview['data']['canonical_document']
    assert undone['receipt']['result'] == undone['data']
    assert undone['data']['canonical_document']['parent_revision']['payload']['meta'] == {'guard': {'note': 'kept'}}
    redone = land(realm, inverse([undone['receipt']['receipt_id']]))
    assert redone['receipt']['result'] == redone['data']
    assert redone['data']['canonical_document']['internal_timeline_revisions'] == (
        first['data']['canonical_document']['internal_timeline_revisions'])
