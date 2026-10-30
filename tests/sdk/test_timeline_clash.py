"""Clash ownership, ancestry, dependency and ripple regression tests."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.timeline._command_state import ABSENT, present
from astrid.sdk.timeline._doc_patch import Closure
from astrid.sdk.timeline.clash import (
    _base_records,
    _dependents,
    _owners,
    _ripples,
    classify,
)
from astrid.sdk.timeline.commit import _digest, bundle_from_document, create_runtime_commit_service
from tests.editing_conformance.test_doc_patch_v2 import change, patch
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedPort, DetachedRealm
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


class ClassifierSession:
    """Public client facade over the existing real provider's detached test port."""

    project_id, timeline_id = 'project-1', 'film'

    def __init__(self, realm):
        self.realm, self.probes = realm, []
        self.page_size = 100
        self.client = SimpleNamespace(timelines=self)

    def history(self, project, timeline, *, cursor=None, limit=100):
        offset = int(cursor or 0)
        end = min(len(self.realm.entries), offset + min(limit, self.page_size))
        return DomainResult.success({'head': copy.deepcopy(self.realm.head),
                                     'items': copy.deepcopy(self.realm.entries[offset:end]),
                                     'next_cursor': str(end) if end < len(self.realm.entries) else None})

    def _capture_bundle(self, state, extra_commands=()):
        return bundle_from_document(self.realm.documents[state['base']['revision_id']])

    def commit(self, project, timeline, body, *, idempotency_key):
        self.probes.append((copy.deepcopy(body), idempotency_key))
        context = self.realm.context(body['commands'])
        context['request'] = copy.deepcopy(body)
        context['idempotency_key'] = idempotency_key
        context['invocation']['body'] = copy.deepcopy(body)
        context['request_hash'] = _digest(context['invocation'])

        class Port(DetachedPort):
            def selected_media(self, pin):
                return next(copy.deepcopy(value) for value in self.realm.verified
                            if value['selection'] == pin)

        try:
            response = create_runtime_commit_service().commit(context, Port(self.realm, context))
            return DomainResult.success(response['data'])
        except CommitRejected as exc:
            failure = exc.failure
            return DomainResult.failure(ErrorObject(failure['code'], failure['message'], failure['details']))


def request(base, commands):
    return {'api_version': 1, 'project_id': 'project-1', 'timeline_id': 'film',
            'base_revision_id': base['revision_id'], 'base_publication_id': base['publication_id'],
            'commands': commands, 'label': 'Our list', 'merge': 'atomic', 'reads': [],
            'rationale': 'Keep this intent', 'source': {'via': 'python'}}


def test_packet_runtime_probe_loop_preserves_exact_commands_and_attribution():
    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    ours = [realm.move(on=6.006), patch(change(['unknown', 'new'], ABSENT, None))]
    first = realm.call([realm.move(on=3.003)])
    latest = realm.call([realm.move(on=4.004)])
    session = ClassifierSession(realm)
    session.page_size = 1
    failure = {'details': {'reason': 'atomic_scope_changed', 'conflicts': [{'opaque': [None]}]}}
    packet = classify(session, request(base, ours), key='ours', pending_id='pc_1', failure=failure)
    assert packet['classified'], packet
    assert [row['verdict'] for row in packet['commands']] == ['overlaps', 'applies']
    overlap = packet['commands'][0]['overlaps'][0]
    assert (overlap['ref'], overlap['path']) == ('parent', ['config', 'clips', 'id:clip-a', 'at'])
    assert (overlap['base'], overlap['theirs'], overlap['yours']) == (1, 4.004, 6.006)
    assert overlap['receipt'] == latest['receipt']['receipt_id']
    assert [row['publication_id'] for row in packet['receipts']] == [
        first['receipt']['receipt_id'], latest['receipt']['receipt_id']]
    assert all(row['clashes_with'] == [0] for row in packet['receipts'])
    assert packet['runtime'] == failure['details']
    assert packet['commands'][0]['choices'] == ['ours', 'theirs', 'shift']
    assert packet['next'] == "tl.rebase('pc_1')"
    assert [row['command'] for row in packet['commands']] == ours
    assert [body['commands'] for body, _ in session.probes] == [ours, ours[1:]]
    assert all(body['dry_run'] and body['merge'] == 'fields' and body['reads'] == []
               and body['base_publication_id'] == base['publication_id']
               for body, _ in session.probes)
    assert len({key for _, key in session.probes}) == 2
    assert all(key.startswith('clash-probe-') for _, key in session.probes)
    assert len(realm.accepted) == 2  # The probes never accept or persist a commit.


def test_owner_mapping_alias_prefix_multiple_owners_and_unknown_fallback():
    realm = DetachedRealm()
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    calls = [patch(change(['clips', 'id:clip-a', 'hold'], present(2), 3)),
             patch(change(['unknown', 'new'], ABSENT, True))]
    records, closure = _base_records(bundle, calls), Closure(bundle)
    assert _owners(calls, records, [0, 1], {'ref': 'parent/clip:clip-a', 'path': []}, closure) == [0]
    assert _owners(calls, records, [0, 1], {'ref': 'parent', 'path': ['clips']}, closure) == [0]
    records[1]['unknown'] = True
    assert _owners(calls, records, [0, 1], {'ref': 'no-such-ref', 'path': ['x']}, closure) == [1]
    records[1]['unknown'] = False
    assert _owners(calls, records, [0, 1], {'ref': 'no-such-ref', 'path': ['x']}, closure) == [0]
    records.append(copy.deepcopy(records[0]))
    assert _owners(calls + [calls[0]], records, [0, 1, 2], {
        'ref': 'parent/clip:clip-a', 'path': ['hold']}, closure) == [0, 2]


def test_blocked_dependencies_propagate_forward_with_direct_needs():
    records = [
        {'writes': [('parent', ['clips', 'id:new'])], 'reads': []},
        {'writes': [('parent', ['clips', 'id:b', 'hold'])],
         'reads': [('parent', ['clips', 'id:new', 'hold'])]},
        {'writes': [], 'reads': [('parent', ['clips', 'id:b'])]},
        {'writes': [], 'reads': [('parent', ['clips', 'id:other'])]},
    ]
    assert _dependents(records, [0, 1, 2, 3], [0]) == {1: [0], 2: [1]}
    assert _dependents(records, [0, 1, 2, 3], [2]) == {}


def test_probe_loop_blocks_later_command_that_consumed_another_write_of_owner():
    from astrid.sdk.timeline.capture import capture_move
    from astrid.sdk.timeline.commands import execute

    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    first = patch(change(['clips', 'id:clip-a', 'at'], present(1), 2.002),
                  change(['clips', 'id:clip-b', 'hold'], present(2), 3))
    bundle = bundle_from_document(realm.documents[base['revision_id']])
    second = capture_move(execute(bundle, [first]).bundle, 'parent/clip:clip-b', 8.008)
    third = patch(change(['unknown', 'independent'], ABSENT, True))
    realm.call([realm.move(on=4.004)])
    session = ClassifierSession(realm)
    packet = classify(session, request(base, [first, second, third]))
    assert packet['classified'], packet
    assert [row['verdict'] for row in packet['commands']] == ['overlaps', 'blocked', 'applies']
    assert packet['commands'][1]['needs'] == [0]
    assert session.probes[-1][0]['commands'] == [third]


def test_absent_target_and_present_null_have_distinct_values():
    from astrid.sdk.timeline.capture import capture_clip_delete

    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    ours = [realm.move(on=6.006)]
    realm.call([capture_clip_delete(bundle_from_document(realm.documents[base['revision_id']]),
                                   'parent/clip:clip-a')])
    packet = classify(ClassifierSession(realm), request(base, ours))
    assert packet['classified'], packet
    assert packet['commands'][0]['verdict'] == 'target_missing'
    assert packet['commands'][0]['choices'] == ['theirs']

    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    ours = [patch(change(['unknown', 'opaque'], present(['parent-1', None]), None))]
    realm.call([patch(change(['unknown', 'opaque'], present(['parent-1', None]), True))])
    packet = classify(ClassifierSession(realm), request(base, ours))
    assert packet['classified'], packet
    assert packet['commands'][0]['overlaps'][0]['yours'] is None


@pytest.mark.parametrize('op,args', [('timeline.inverse', {'publications': ['p']}),
                                    ('timeline.restore', {}), ('producer.guard', {'pin': {}}),
                                    ('assembly-admission', {}),
                                    ('occurrence.place-shared', {'source_ref': {}})])
def test_unsupported_commands_never_reach_a_probe(op, args):
    realm = DetachedRealm()
    command = {'schema_version': 1, 'version': '1', 'op': op, 'select': None, 'args': args}
    session = ClassifierSession(realm)
    packet = classify(session, request(realm.head, [command]))
    assert packet['classified'], packet
    assert packet['commands'][0]['verdict'] == 'unsupported'
    assert session.probes == []


@pytest.mark.parametrize('damage', ['previous', 'duplicate', 'missing', 'cursor', 'no_records'])
def test_unverified_history_never_classifies(damage):
    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    ours = [realm.move(on=6.006)]
    realm.call([realm.move()])
    session = ClassifierSession(realm)
    if damage == 'previous':
        realm.entries[-1]['previous'] = {'revision_id': 'wrong', 'publication_id': 'wrong'}
    elif damage == 'duplicate':
        realm.entries.append(copy.deepcopy(realm.entries[-1]))
    elif damage == 'missing':
        realm.entries.pop()
    elif damage == 'no_records':
        realm.entries[-1]['records'] = None
    else:
        original = session.history

        def bad_history(*args, **kwargs):
            result = original(*args, **kwargs)
            result.data['next_cursor'] = '0'
            return result

        session.history = bad_history
    packet = classify(session, request(base, ours))
    assert not packet['classified'] and packet['error']
    assert session.probes == []


@pytest.mark.parametrize('status', ['refused', 'invalid'])
def test_probe_refusal_and_invalid_are_not_safe_to_apply(status):
    realm = DetachedRealm()
    session = ClassifierSession(realm)
    session.commit = lambda *args, **kwargs: DomainResult.failure(ErrorObject('conflict', 'stop', {
        'status': status, 'current': realm.head, 'reason': 'not_safe'}))
    packet = classify(session, request(realm.head, [realm.move()]))
    assert not packet['classified'] and 'not_safe' in packet['error']
    assert packet['commands'][0]['verdict'] == 'unknown'


def test_network_failure_returns_exact_intent_as_unclassified():
    realm = DetachedRealm()
    session = ClassifierSession(realm)

    def disconnected(*args, **kwargs):
        raise ConnectionError('offline')

    session.commit = disconnected
    ours = [realm.move()]
    packet = classify(session, request(realm.head, ours), pending_id='pc_saved')
    assert not packet['classified'] and packet['error'] == 'offline'
    assert packet['commands'][0]['command'] == ours[0]
    assert packet['pending_id'] == 'pc_saved'


@pytest.mark.parametrize('continuous', [False, True])
def test_head_moving_restarts_and_is_bounded(continuous):
    realm = DetachedRealm()
    base, ours = copy.deepcopy(realm.head), [realm.move('parent/clip:clip-b', 8.008)]
    session = ClassifierSession(realm)
    original, calls = session.commit, []

    def race(*args, **kwargs):
        if continuous or not calls:
            realm.call([realm.move(on=3.003 + len(calls) * 1.001)])
        calls.append(True)
        return original(*args, **kwargs)

    session.commit = race
    packet = classify(session, request(base, ours))
    if continuous:
        assert not packet['classified'] and packet['head_moving']
        assert len(calls) == 4
    else:
        assert packet['classified'], packet
        assert packet['head'] == realm.head
        assert packet['commands'][0]['verdict'] == 'applies'
        assert len(calls) == 2


def test_ripple_requires_two_distinct_clips_with_same_nonzero_delta():
    times = {('parent/clip:a', ('at',)): (10, 12), ('parent/clip:b', ('at',)): (15, 17),
             ('parent/clip:c', ('at',)): (30, 31), ('parent/clip:d', ('at',)): (40, 40)}
    ripple, = _ripples(times)
    assert (ripple['by'], ripple['after']) == (2, 10)
    assert len(ripple['sites']) == 2
    assert _ripples({('parent/clip:a', ('at',)): (10, 12)}) == []


def test_ripple_uses_net_delta_across_sequential_writes_to_a_clip():
    from astrid.sdk.timeline.clash import _clip_times

    writes = [{'ref': 'parent/clip:' + identity, 'path': ['at'],
               'before': present(before), 'after': present(after)}
              for identity, before, after in [('a', 10, 11), ('a', 11, 12), ('b', 15, 17)]]
    ripple, = _ripples(_clip_times(writes))
    assert (ripple['by'], ripple['after']) == (2, 10)


def test_literal_times_include_ancestor_and_birth_writes_but_ignore_extension_at_fields():
    from astrid.sdk.timeline.clash import _clip_times, _literal_times

    row = {'id': 'new', 'at': 12}
    command = patch(change(['config', 'clips'], ABSENT, row, op='list.insert', id='new',
                            order_before=[], after_id=None),
                    change(['clips', 'id:old'], present({'id': 'old', 'at': 10}), {'id': 'old', 'at': 13}),
                    change(['unknown'], present({}), {'at': 99}))
    assert list(_literal_times(command)) == [
        ('parent', ['config', 'clips', 'id:new', 'at'], 12),
        ('parent', ['config', 'clips', 'id:old', 'at'], 13)]
    before = {'clips': [{'id': 'a', 'at': 10}], 'config': {'clips': [{'id': 'a', 'at': 10}]}}
    after = {'clips': [{'id': 'a', 'at': 12}], 'config': {'clips': [{'id': 'a', 'at': 12}]}}
    times = _clip_times([{'ref': 'parent', 'path': [], 'before': present(before), 'after': present(after)}])
    assert _ripples(times) == []  # Two physical mirrors are still one clip.


@pytest.mark.parametrize('moment', ['word:hello', 'beat:4', 'clip:other+1'])
def test_numeric_compiler_position_of_a_moment_does_not_get_a_time_shift(moment):
    from astrid.sdk.timeline.clash import _ripple_flags
    from tests.editing_conformance.test_recipe_clip_delete import delete_document

    realm = DetachedRealm(delete_document())
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
        rows[2]['app'] = {'astrid': {'on': moment}}
    closure = Closure(bundle)
    command = patch(change(['clips', 'id:clip-c', 'at'], present(8), 12))
    packet = {'commands': [{'ordinal': 0, 'command': command, 'verdict': 'applies'}], 'ripple_gap': None}
    writes = [{'ref': 'parent/clip:' + identity, 'path': ['at'], 'before': present(at),
               'after': present(at + 2)} for identity, at in [('clip-a', 1), ('clip-b', 5)]]
    _ripple_flags(packet, [], closure, closure, [{'publication_id': 'ripple', 'writes': writes}])
    assert 'time_shift' not in packet['commands'][0]


def test_their_ripple_flags_literal_times_but_not_moments_or_moved_targets():
    from astrid.sdk.timeline.clash import _literal_times, _ripple_flags
    from tests.editing_conformance.test_recipe_clip_delete import delete_document

    realm = DetachedRealm(delete_document())
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    closure = Closure(bundle)
    writes = [{'ref': 'parent/clip:' + ref, 'path': ['at'], 'before': present(at),
               'after': present(at + 2)} for ref, at in [('clip-a', 1), ('clip-b', 5)]]
    commands = [realm.move('parent/clip:clip-c', 12.012), realm.move(on=6.006)]
    packet = {'commands': [{'ordinal': i, 'command': command, 'verdict': 'applies'}
                           for i, command in enumerate(commands)], 'ripple_gap': None}
    _ripple_flags(packet, [], closure, closure, [{'publication_id': 'p1', 'writes': writes}])
    assert packet['commands'][0]['time_shift'] == {'by': 2, 'after': 1, 'receipt': 'p1'}
    assert packet['commands'][0]['choices'] == ['keep', 'shift']
    assert 'time_shift' not in packet['commands'][1]
    assert list(_literal_times({'op': 'clip.move', 'select': 'parent/clip:c',
                                'args': {'on': 'word:hello'}})) == []


def test_our_ripple_detects_uncovered_created_clip():
    from astrid.sdk.timeline.clash import _ripple_flags

    realm = DetachedRealm()
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    closure = Closure(bundle)
    ours = [patch(*(change(['clips', 'id:' + identity, 'at'], present(at), at + 2)
                    for identity, at in [('clip-a', 1), ('clip-b', 5)]))]
    packet = {'commands': [], 'ripple_gap': None}
    records = _base_records(bundle, ours)
    writes = [{'ref': 'parent/clip:new', 'path': [], 'before': ABSENT,
               'after': present({'id': 'new', 'at': 15})}]
    head_bundle = copy.deepcopy(bundle)
    for rows in (head_bundle['parent']['clips'], head_bundle['parent']['config']['clips']):
        rows.append(dict(copy.deepcopy(rows[0]), id='new', at=15))
    head = Closure(head_bundle)
    _ripple_flags(packet, records, closure, head, [{'publication_id': 'birth', 'writes': writes}])
    assert packet['ripple_gap'] == {'by': 2, 'after': 1, 'choices': ['keep', 'extend'],
                                    'clips': [{'ref': 'parent/clip:new', 'path': ['at'],
                                               'at': 15, 'receipt': 'birth'}]}
