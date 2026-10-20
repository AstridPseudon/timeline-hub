"""Verify the reviewed App split golden against the native Agent recipe and inverse."""
import copy
import json
from pathlib import Path

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
