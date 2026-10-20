"""Check bootstrap goldens using the authoritative Agent 31d02d45 on PYTHONPATH.

No Runtime transport/admission is exercised here. Run with the shared Agent
interpreter; the selected Agent source must also contain editing_conformance.
"""
import copy
import json
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._init_commands import capture_timeline_init
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse

fixture = json.loads(Path(__file__).with_name('recipe_m2_app_bootstrap.json').read_text())
original = fixture['bundle']
init = capture_timeline_init(original, **fixture['commands'][0]['args'])
video = capture_track_create(execute(original, [init]).bundle, 'parent', fixture['commands'][1]['args']['row'])
audio = capture_track_create(execute(original, [init, video]).bundle, 'parent', fixture['commands'][2]['args']['row'])
assert [init, video, audio] == fixture['commands']
plan = execute(original, [init, video, audio])
assert plan.records == fixture['records'] and plan.bundle == fixture['after_bundle']
undone = inverse(plan.bundle, plan.records)
assert undone.bundle == original and undone.records == fixture['inverse_records']
redone = inverse(undone.bundle, undone.records)
assert redone.bundle == plan.bundle and redone.records == fixture['redo_records']
assert replay(plan, original).records == plan.records
try:
    replay(plan, undone.bundle, intervening_records=[*plan.records, *undone.records])
except CommandError as error:
    assert error.kind == 'intervening_write', error.kind
else:
    raise AssertionError('Init then complete undo must still prevent original init replay')
for value in [None, False, [3, 1, 2], {'constructor': None, '__proto__': [None, False]}]:
    edited = copy.deepcopy(plan.bundle)
    edited['parent']['opaque'] = value
    before = copy.deepcopy(edited)
    restored = inverse(edited, plan.records)
    assert restored.bundle['parent']['opaque'] == value and edited == before
edited = copy.deepcopy(plan.bundle)
edited['parent']['config']['output']['background'] = 'edited'
try:
    inverse(edited, plan.records)
except CommandError:
    assert edited['parent']['config']['output']['background'] == 'edited'
else:
    raise AssertionError('Guarded inverse must preserve a later authored output edit')
print('PASS: native sequential captures/records, full defaults/order/nulls, exact inverse/redo/replay, '
      'opaque inverse preservation, guarded inverse refusal, init+undo intervening-write refusal')
