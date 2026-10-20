"""Check full parent-add goldens against frozen Agent 027bd16d on PYTHONPATH."""
import copy
import json
from pathlib import Path

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute


data = json.loads(Path(__file__).with_name('recipe_m2_parent_clip_add.json').read_text())
cases = {case['name']: case for case in data['cases']}
for case in cases.values():
    bundle = copy.deepcopy(case['bundle'])
    command = capture_clip_add(bundle, case['select'], case['row'])
    plan = execute(bundle, [command])
    for key, actual in {'command': command, 'record': plan.records[0], 'after_bundle': plan.bundle}.items():
        assert case[key] == actual, (case['name'], key)
    replayed = execute(bundle, [case['command']])
    assert replayed.commands == [command], case['name']
    assert replayed.records == plan.records, case['name']
    assert replayed.bundle == plan.bundle, case['name']
    assert bundle == case['bundle'], case['name']

for refusal in data['refusals']:
    bundle = copy.deepcopy(refusal.get('bundle', cases[refusal['case']]['bundle']))
    original = copy.deepcopy(bundle)
    command = copy.deepcopy(refusal['command'])
    try:
        execute(bundle, [command])
    except CommandError as error:
        assert error.kind == refusal['kind'], (refusal['name'], error.kind)
    else:
        raise AssertionError(('native accepted invalid input', refusal['name']))
    assert bundle == original, refusal['name']
    assert command == refusal['command'], refusal['name']

print(f"{len(cases)} exact native commands/records/after-bundles and "
      f"{len(data['refusals'])} native refusal kinds verified")
