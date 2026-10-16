"""Opt-in real Astrid whole-row semantics against this Runtime producer.

Select an admitted, read-only Astrid tests/sdk directory explicitly. No semantic
consumer implementation is copied into Runtime and no speech backend is invoked.
"""
import copy
import os
import sys

import pytest

consumer_tests = os.environ.get('ASTRID_NARRATION_CONSUMER_TESTS')
if not consumer_tests:
    pytest.skip('requires an explicitly admitted narration consumer test source', allow_module_level=True)
sys.path.append(consumer_tests)

from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command
from test_selected_media_commit import snapshot
from test_timeline_accept import IDENTITY, wire
from test_timeline_narration_runtime import (commit, managed_take, runtime, script,
                                             synthetic_scene_answers, valid)

pytestmark = pytest.mark.usefixtures('synthetic_scene_answers')


def test_whole_row_delete_conflict_and_exact_inverse(runtime, monkeypatch):
    s, p = runtime
    refs, _, _ = managed_take(s, p)
    request = wire(p)
    request['change']['commands'] = [script(refs)]
    first = commit(s, p, request)
    assert first['status'] == 'accepted', first
    valid(first, 'CommitResult')
    sid = 'occurrence:occurrence-1/clip:voice'
    assert any(w['id'] == sid and w['path'] == '' for w in first['change']['direct_writes'])
    delete = wire(p, key='delete-whole-row')
    delete.update(base_revision_id=first['accepted_revision_id'], base_publication_id=first['accepted_publication_id'])
    delete['change']['commands'] = [{'op': 'timeline.apply-script', 'select': None,
        'args': {'spec': {'version': 1, 'lines': [], 'remove': [sid]}}}]
    concurrent = copy.deepcopy(delete)
    concurrent['request_id'] = 'concurrent-opaque-edit'
    concurrent['change']['commands'] = [{'op': 'clip.set', 'select': sid,
        'args': {'caption': {'opaque': [None, False, 'concurrent']}, '_allow_new': True}}]
    other = commit(s, p, concurrent)
    assert other['status'] == 'accepted', other.get('error')
    before = snapshot(s)
    conflict = commit(s, p, delete)
    assert conflict['status'] == 'conflict', conflict
    valid(conflict, 'CommitResult')
    assert any(c['id'] == sid and c['path'] == '' and c['base'] != c['theirs']
               for c in conflict['conflicts'])
    assert snapshot(s) == before
    # Retry as a new edit pinned to the actual row, then undo the whole row.
    delete['request_id'] = 'delete-current-whole-row'
    delete.update(base_revision_id=other['accepted_revision_id'], base_publication_id=other['accepted_publication_id'])
    base = RuntimeCommitService._load_revision(s._request_commit_port(delete, IDENTITY), delete, delete['base_revision_id'])
    empty = commit(s, p, delete)
    assert empty['status'] == 'accepted', empty
    valid(empty, 'CommitResult')
    writes = [w for w in empty['change']['direct_writes'] if w['id'] == sid and w['path'] == '']
    assert len(writes) == 1 and writes[0]['after'] == {'state': 'absent'}
    assert writes[0]['before']['value']['params']['caption']['opaque'] == [None, False, 'concurrent']
    inverse = inverse_command(empty['change']['commands'], base, empty['canonical_document'],
                              empty['accepted_publication_id'], consequences=empty['change']['consequences'])
    undo = wire(p, key='undo-whole-row')
    undo.update(base_revision_id=empty['accepted_revision_id'], base_publication_id=empty['accepted_publication_id'])
    undo['change']['commands'] = [inverse]
    monkeypatch.setattr('astrid.sdk.invocation.invoke', lambda *_a, **_k: pytest.fail('undo generated speech'))
    restored = commit(s, p, undo)
    assert restored['status'] == 'accepted', restored
    valid(restored, 'CommitResult')
    restored_row = next(w for w in restored['change']['direct_writes'] if w['id'] == sid and w['path'] == '')
    assert restored_row['after'] == writes[0]['before']
