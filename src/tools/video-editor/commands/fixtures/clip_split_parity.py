"""Verify the reviewed App split golden against the native Agent recipe and inverse."""
import copy
import json
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._split_commands import capture_clip_split
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from tests.editing_conformance.test_recipe_m1_commands import inverse

fixture = json.loads(Path(__file__).with_name('recipe_m2_clip_split.json').read_text())
original = bundle_from_document(fixture['input'])
before = copy.deepcopy(original)
command = capture_clip_split(original, 'parent/clip:clip-a', on=3, right_id='right')
plan = execute(original, [command])
assert [command] == fixture['commands']
assert plan.records == fixture['records']
assert document_from_bundle(plan.bundle) == fixture['output']
assert original == before
undone = inverse(plan.bundle, plan.records)
assert undone.bundle == original
assert inverse(undone.bundle, undone.records).bundle == plan.bundle


def source_clock_rows(bundle):
    return [bundle['parent']['clips'][0], bundle['parent']['config']['clips'][0]]


dynamic_original = bundle_from_document(fixture['input'])
for row in source_clock_rows(dynamic_original):
    row['from'] = 0
    row['to'] = 4
    row['hold'] = 4
    row['speed'] = 1.3
    row['app']['astrid']['for'] = 4 / 1.3

derived_bundle = copy.deepcopy(dynamic_original)
for row in source_clock_rows(derived_bundle):
    row['hold'] = 4 / 1.3
try:
    capture_clip_split(derived_bundle, 'parent/clip:clip-a', on=3, right_id='right-dynamic')
except CommandError as error:
    assert 'matching hold and source window' in str(error)
else:
    raise AssertionError('derived timeline hold was accepted')

dynamic_before = copy.deepcopy(dynamic_original)
dynamic_command = capture_clip_split(dynamic_original, 'parent/clip:clip-a', on=3, right_id='right-dynamic')
dynamic_plan = execute(dynamic_original, [dynamic_command])
dynamic_rows = dynamic_plan.bundle['parent']['clips']
assert dynamic_rows[0]['from'] == 0
assert dynamic_rows[0]['to'] == 2.6
assert dynamic_rows[0]['hold'] == 2.6
assert dynamic_rows[1]['from'] == 2.6
assert dynamic_rows[1]['to'] == 4
assert dynamic_rows[1]['hold'] == 1.4
assert dynamic_rows[0]['speed'] == dynamic_rows[1]['speed'] == 1.3
assert dynamic_rows[0]['app']['astrid']['for'] == 2
assert dynamic_rows[1]['app']['astrid']['for'] == 4 / 1.3 - 2
assert dynamic_rows[1]['opaque'] == dynamic_rows[0]['opaque']
assert dynamic_rows[1]['params'] == dynamic_rows[0]['params']
assert dynamic_original == dynamic_before
dynamic_undone = inverse(dynamic_plan.bundle, dynamic_plan.records)
assert dynamic_undone.bundle == dynamic_original
assert inverse(dynamic_undone.bundle, dynamic_undone.records).bundle == dynamic_plan.bundle
print('1/1 canonical native split command, complete record, authored after, inverse and redo verified')
print('2/2 dynamic source-clock split refusal, record, after, inverse and redo verified')
