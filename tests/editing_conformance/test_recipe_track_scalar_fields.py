"""Bounded raw track fields from the current Main mute control."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse

TRACK = 'parent/track:picture'


def track(original, ref=TRACK):
    return State(original).entity(ref)


@pytest.mark.parametrize('before', [ABSENT, present(None), present(False), present(True)])
@pytest.mark.parametrize('clear', [False, True])
def test_mute_set_clear_preserves_raw_presence_and_exact_inverse(before, clear):
    original = bundle()
    if before != ABSENT:
        track(original)['muted'] = copy.deepcopy(before['value'])
    before_row = copy.deepcopy(track(original))
    command = capture_track_set(
        original,
        TRACK,
        values={} if clear else {'muted': False},
        clear=['muted'] if clear else [],
    )
    assert command['args'] == {
        'values': {} if clear else {'muted': False},
        'clear': ['muted'] if clear else [],
    }
    assert command['expect'] == {TRACK + '::muted': before}
    plan = execute(original, [command])
    expected = copy.deepcopy(before_row)
    if clear:
        expected.pop('muted', None)
    else:
        expected['muted'] = False
    assert track(plan.bundle) == expected
    assert plan.records[0]['writes'] == [{
        'ref': TRACK,
        'path': ['muted'],
        'before': before,
        'after': ABSENT if clear else present(False),
    }]
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle


def test_mute_capture_is_exact_main_shape_and_one_leaf_preserves_opaque_track():
    original = bundle()
    track(original).update(
        label='Audio',
        muted=False,
        role='source',
        opacity=0.4,
        volume=0.8,
        app={'opaque': {'keep': [None, False]}},
        opaque={'future': [1, None, False]},
    )
    before = copy.deepcopy(track(original))
    original_snapshot = copy.deepcopy(original)
    command = capture_track_set(original, TRACK, values={'muted': True})

    assert command['op'] == 'track.set'
    assert command['select'] == TRACK
    assert command['args'] == {'values': {'muted': True}, 'clear': []}
    assert command['intent'] == {}
    assert command['resolved'] == [TRACK]
    assert command['bindings'] == {'scalar.target': TRACK}
    assert command['expect'] == {TRACK + '::muted': present(False)}
    assert command['authorship'] == {TRACK + '::muted': 'direct'}

    plan = execute(original, [command])
    assert track(plan.bundle) == dict(before, muted=True)
    assert plan.records[0]['writes'] == [{
        'ref': TRACK,
        'path': ['muted'],
        'before': present(False),
        'after': present(True),
    }]
    assert original == original_snapshot


@pytest.mark.parametrize('values,clear', [
    ({'muted': None}, []),
    ({'muted': 0}, []),
    ({'muted': 'true'}, []),
    ({'muted': True}, ['muted']),
    ({'unknown': True}, []),
    ({}, ['unknown']),
])
def test_mute_contract_is_closed(values, clear):
    with pytest.raises(CommandError):
        capture_track_set(bundle(), TRACK, values=values, clear=clear)


def test_mute_stale_same_property_refuses_without_partial_write():
    original = bundle()
    command = capture_track_set(original, TRACK, values={'muted': True})
    head = execute(original, [capture_track_set(original, TRACK, values={'muted': False})]).bundle
    snapshot = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, [command])
    assert head == snapshot


def test_mute_replays_across_disjoint_label_write():
    original = bundle()
    command = capture_track_set(original, TRACK, values={'muted': True})
    plan = execute(original, [command])
    labelled = execute(original, [capture_track_set(original, TRACK, values={'label': 'Picture'})])

    rebased = replay(plan, labelled.bundle, intervening_records=labelled.records)
    assert track(rebased.bundle)['muted'] is True
    assert track(rebased.bundle)['label'] == 'Picture'
    assert inverse(rebased.bundle, rebased.records).bundle == labelled.bundle


def test_mute_owner_binding_is_explicit_for_occurrence_track():
    original = bundle()
    ref = 'occurrence:occ-1/track:picture'
    command = capture_track_set(original, ref, values={'muted': True})

    assert command['bindings']['scalar.target'] == ref
    assert command['bindings']['scalar.owner'] == 'occurrence:occ-1'
    assert command['expect'] == {ref + '::muted': ABSENT}
