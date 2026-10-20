"""Compare App bootstrap goldens against Agent 487ca1e0 on PYTHONPATH.

Run with the shared Agent interpreter and an extracted source tree containing
editing_conformance. This exercises native semantics, not Runtime admission.
"""
import copy
import json
import re
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.native_initialize import capture_initialize
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_pristine_initialize import GOLDEN as native_fixture

fixture = json.loads(Path(__file__).with_name('recipe_m2_app_bootstrap.json').read_text())
original = fixture['bundle']
init = capture_initialize(original, **fixture['commands'][0]['args'])
video = capture_track_create(execute(original, [init]).bundle, 'parent', fixture['commands'][1]['args']['row'])
audio = capture_track_create(execute(original, [init, video]).bundle, 'parent', fixture['commands'][2]['args']['row'])
plan = execute(original, [init, video, audio])


def test_native_sequential_captures_records_inverse_redo_and_replay():
    assert fixture['source'] == '487ca1e0d74edf4aecdd2b4e045294ab089fc273'
    assert fixture['commands'] == native_fixture['commands']
    assert fixture['records'] == native_fixture['records']
    assert [init, video, audio] == fixture['commands']
    assert plan.records == fixture['records'] and plan.bundle == fixture['after_bundle']
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original and undone.records == fixture['inverse_records']
    redone = inverse(undone.bundle, undone.records)
    assert redone.bundle == plan.bundle and redone.records == fixture['redo_records']
    assert replay(plan, original).records == plan.records
    with pytest.raises(CommandError) as error:
        replay(plan, undone.bundle, intervening_records=[*plan.records, *undone.records])
    assert error.value.kind == 'intervening_write'


@pytest.mark.parametrize('name', ['', '   ', '  Authored Cut  ', 'x' * 121, 'Timeline 2', '!!!'])
def test_authored_names_match_native_capture_and_reverse_exactly(name):
    slug = re.sub(r'^-|-$', '', re.sub('[^a-z0-9]+', '-', name.lower())) or 'timeline'
    named = capture_initialize(original, name=name, slug=slug, output=init['args']['output'])
    expected = copy.deepcopy(init)
    expected['args'].update(name=name, slug=slug)
    assert named == expected
    named_plan = execute(original, [named])
    assert named_plan.bundle['parent']['name'] == name
    assert inverse(named_plan.bundle, named_plan.records).bundle == original


def test_inverse_preserves_a_later_authored_output_edit():
    edited = copy.deepcopy(plan.bundle)
    edited['parent']['config']['output']['background'] = 'edited'
    before = copy.deepcopy(edited)
    with pytest.raises(CommandError):
        inverse(edited, plan.records)
    assert edited == before


@pytest.mark.parametrize('value', [None, False, [3, 1, 2], {'constructor': None, '__proto__': [None, False]}])
# Requirement: bootstrap inverse must preserve unrelated opaque parent fields.
@pytest.mark.xfail(strict=True, reason='Agent 487ca1e0 raw-parent inverse read currently rejects unrelated opaque fields')
def test_inverse_preserves_unrelated_opaque_parent_fields(value):
    edited = copy.deepcopy(plan.bundle)
    edited['parent']['opaque'] = value
    before = copy.deepcopy(edited)
    restored = inverse(edited, plan.records)
    assert restored.bundle['parent']['opaque'] == value and edited == before


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q', '-p', 'no:cacheprovider']))
