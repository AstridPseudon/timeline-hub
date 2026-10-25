"""Exact authored-time coverage for the registered clip.move producer."""
from __future__ import annotations

from fractions import Fraction

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_m1_commands import bundle

REF = 'occurrence:occ-1/clip:picture-1'


def exact_fit_bundle(codec):
    original = bundle()
    original['placements'][0]['placement']['start_ms'] = 3300
    original['placements'][1]['placement']['start_ms'] = 5300
    target = State(original).entity(REF)
    target['hold'] = 1.8
    if codec == 'at_ms':
        target['at_ms'] = 0
        del target['at']
    elif codec == 'both':
        target['at_ms'] = 0
    return original


@pytest.mark.parametrize('codec', ['at', 'at_ms', 'both'])
def test_capture_execute_exact_fit_keeps_local_time_and_interval(codec):
    original = exact_fit_bundle(codec)
    command = capture_move(original, REF, 3.5)
    plan = execute(original, [command])
    moved = State(plan.bundle).entity(REF)

    local = Fraction(str(moved['at'] if 'at' in moved else moved['at_ms'] / 1000))
    duration = Fraction(str(moved['app']['astrid']['for']))
    assert local == Fraction(1, 5)
    assert duration == Fraction(9, 5)
    assert local + duration == Fraction(2)
    if codec == 'at_ms':
        assert moved['at_ms'] == 200.0
    elif codec == 'both':
        assert moved['at'] == 0.2
        assert moved['at_ms'] == 200.0
    else:
        assert moved['at'] == 0.2


def test_capture_move_refuses_real_out_of_bounds_interval():
    original = exact_fit_bundle('at')
    with pytest.raises(CommandError, match='next occurrence') as error:
        capture_move(original, REF, 3.6)
    assert error.value.kind == 'occurrence_boundary'
