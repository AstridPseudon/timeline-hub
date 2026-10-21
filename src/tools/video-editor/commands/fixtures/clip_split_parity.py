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
print('1/1 native split command, complete record, authored after, inverse and redo verified')


def source_clock_rows(bundle):
    return [bundle['parent']['clips'][0], bundle['parent']['config']['clips'][0]]


dynamic_original = bundle_from_document(fixture['input'])
for row in source_clock_rows(dynamic_original):
    row['at'] = 0
    row['from'] = 0
    row['to'] = 4
    row['hold'] = 4
    row['speed'] = 1.3
    row['app']['astrid']['for'] = 4 / 1.3

dynamic_before = copy.deepcopy(dynamic_original)
derived_bundle = copy.deepcopy(dynamic_original)
for row in source_clock_rows(derived_bundle):
    row['hold'] = 4 / 1.3
derived_before = copy.deepcopy(derived_bundle)
try:
    capture_clip_split(derived_bundle, 'parent/clip:clip-a', on=1, right_id='right-dynamic')
except CommandError as error:
    assert str(error) == 'split requires matching hold and source window'
    assert derived_bundle == derived_before
else:
    raise AssertionError('derived timeline hold was accepted')

dynamic_command = capture_clip_split(dynamic_original, 'parent/clip:clip-a', on=1, right_id='right-dynamic')
dynamic_plan = execute(dynamic_original, [dynamic_command])
dynamic_record = dynamic_plan.records[0]
dynamic_rows = dynamic_plan.bundle['parent']['clips']
assert dynamic_command == dynamic_record['command']
assert dynamic_command['args'] == {'on': 1, 'right_id': 'right-dynamic'}
assert dynamic_command['resolved'] == ['parent/clip:clip-a']
assert dynamic_command['bindings'] == {'split.target': 'parent/clip:clip-a'}
assert dynamic_command['created'] == ['parent/clip:right-dynamic']
assert dynamic_record['ordinal'] == 0
assert dynamic_record['dependencies'] == []
assert dynamic_record['created'] == [{'ref': 'parent/clip:right-dynamic', 'kind': 'clip', 'owner': 'parent'}]
assert dynamic_record['reads'] == dynamic_command['reads']
assert dynamic_record['selections'] == dynamic_command['selections']
assert dynamic_record['bindings'] == [{
    'key': 'split.target',
    'ref': 'parent/clip:clip-a',
    'policy': 'fixed',
    'dependencies': [],
}]
assert dynamic_record['writes'][0]['ref'] == 'parent/clip:right-dynamic'
assert dynamic_record['writes'][0]['before'] == {'state': 'absent'}
assert dynamic_record['writes'][0]['after']['value']['at'] == 1
assert dynamic_record['writes'][0]['after']['value']['from'] == 1.3
assert dynamic_record['writes'][0]['after']['value']['to'] == 4
assert dynamic_record['writes'][0]['after']['value']['hold'] == 2.7
assert dynamic_record['writes'][0]['after']['value']['speed'] == 1.3
assert dynamic_record['writes'][0]['after']['value']['app']['astrid']['for'] == 2.0769230769230766
assert [(write['path'], write['before']['value'], write['after']['value']) for write in dynamic_record['writes'][1:]] == [
    (['hold'], 4, 1.3),
    (['to'], 4, 1.3),
    (['app', 'astrid', 'for'], 4 / 1.3, 1),
]
assert dynamic_record['derived_writes'] == [{
    'ref': 'parent',
    'path': ['config', 'clips'],
    'before': {'state': 'present', 'value': dynamic_before['parent']['config']['clips']},
    'after': {'state': 'present', 'value': dynamic_plan.bundle['parent']['config']['clips']},
    'cause': 0,
}]
assert dynamic_rows[0]['at'] == 0
assert dynamic_rows[0]['from'] == 0
assert dynamic_rows[0]['to'] == 1.3
assert dynamic_rows[0]['hold'] == 1.3
assert dynamic_rows[0]['speed'] == 1.3
assert dynamic_rows[0]['app']['astrid']['for'] == 1
assert dynamic_rows[1]['id'] == 'right-dynamic'
assert dynamic_rows[1]['at'] == 1
assert dynamic_rows[1]['from'] == 1.3
assert dynamic_rows[1]['to'] == 4
assert dynamic_rows[1]['hold'] == 2.7
assert dynamic_rows[1]['speed'] == 1.3
assert dynamic_rows[1]['app']['astrid']['for'] == 2.0769230769230766
assert dynamic_rows[0]['opaque'] == dynamic_before['parent']['clips'][0]['opaque']
assert dynamic_rows[1]['opaque'] == dynamic_before['parent']['clips'][0]['opaque']
assert dynamic_rows[0]['params'] == dynamic_rows[1]['params'] == dynamic_before['parent']['clips'][0]['params']
assert dynamic_original == dynamic_before
dynamic_undone = inverse(dynamic_plan.bundle, dynamic_plan.records)
assert dynamic_undone.bundle == dynamic_before
dynamic_redone = inverse(dynamic_undone.bundle, dynamic_undone.records)
assert dynamic_redone.bundle == dynamic_plan.bundle
print('2/2 exact source-clock on=1 command, full record, authored after, inverse, redo and refusal verified')
