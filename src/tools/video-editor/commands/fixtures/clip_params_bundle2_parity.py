"""Check/regenerate params fixtures with frozen d4743e2 Agent on PYTHONPATH.

Use a separate git-archive source snapshot and the shared Agent venv; never
modify the live Agent checkout. Only native execute() supplies expected output.
"""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline_address import element_schema

path = Path(__file__).with_name('recipe_m2_clip_params_bundle2.json')
data = json.loads(path.read_text())
update = sys.argv[1:] == ['--update']
if sys.argv[1:] and not update:
    raise SystemExit('usage: clip_params_bundle2_parity.py [--update]')


def check(case, expected):
    if update:
        case.update(expected)
    else:
        for key, value in expected.items():
            assert case[key] == value, (case.get('name'), key)


for case in data['cases']:
    bundle = copy.deepcopy(case['bundle'])
    command = capture_clip_set_params(bundle, case['select'], **case['args'])
    plan = execute(bundle, [command])
    check(case, {'command': command, 'after_bundle': plan.bundle, 'records': plan.records})
    assert bundle == case['bundle'], case['name']
    if 'head_bundle' in case:
        replayed = execute(case['head_bundle'], [command])
        assert replayed.commands == [command], (case['name'], 'original claims')
        check(case, {'rebased_bundle': replayed.bundle, 'rebased_records': replayed.records})

for case in [*data['refusals'], *data['replay_refusals']]:
    try:
        if 'basis' in case:
            execute(case['basis']['bundle'], [case['basis']['command']])
        else:
            capture_clip_set_params(case['bundle'], case['select'], **case['args'])
    except CommandError as exc:
        check(case, {'error': {'kind': exc.kind, 'message': str(exc)}})
    else:
        raise AssertionError(('native accepted invalid input', case['name']))

check(data, {'builtin_properties': {
    element: element_schema(element).get('properties', {})
    for element in data['builtin_properties']
}})
if update:
    path.write_text(json.dumps(data, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n')
print(f"{len(data['cases'])} full native successes, {len(data['refusals'])} native refusals, "
      f"{len(data['replay_refusals'])} replay refusals, "
      f"{len(data['builtin_properties'])} builtin schema comparisons verified")
