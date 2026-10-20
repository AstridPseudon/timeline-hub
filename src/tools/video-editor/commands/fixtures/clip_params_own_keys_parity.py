"""Check/regenerate own-key PARAM goldens with frozen Agent 027bd16 on PYTHONPATH."""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import execute

path = Path(__file__).with_name('recipe_m2_clip_params_own_keys.json')
update = sys.argv[1:] == ['--update']
if sys.argv[1:] and not update:
    raise SystemExit('usage: clip_params_own_keys_parity.py [--update]')

seeds = json.loads(path.with_name('recipe_m2_clip_params_bundle2.json').read_text())['cases']
values = json.loads('''{"__proto__":{"keep":[1,null,false,{},[]]},"constructor":null,
    "toString":false,"literal.key":{"__proto__":"nested"},"a::b":[],"[0]":"literal","":0}''')
cases = []
for owner, seed in [('parent', seeds[4]), ('occurrence', seeds[0])]:
    for mode in ['absent', 'null', 'empty', 'overwrite', 'unchanged', 'clear']:
        bundle = copy.deepcopy(seed['bundle'])
        clip = State(bundle).entity(seed['select'])
        clip.pop('params', None)
        if mode != 'absent':
            clip['params'] = (None if mode == 'null' else
                              {**copy.deepcopy(values), 'opaque': {'keep': [False, None, {}, []]}}
                              if mode in ('unchanged', 'clear') else
                              {'__proto__': 'old', 'constructor': {}, 'toString': []}
                              if mode == 'overwrite' else {})
        if owner == 'parent':
            bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
        args = ({'values': {}, 'clear': [*values, 'missing']} if mode == 'clear' else
                {'values': copy.deepcopy(values), 'clear': []})
        command = capture_clip_set_params(bundle, seed['select'], **args)
        plan = execute(bundle, [command])
        cases.append({'name': f'{owner}_{mode}', 'bundle': bundle, 'select': seed['select'],
                      'args': args, 'command': command, 'after_bundle': plan.bundle,
                      'records': plan.records})

data = {'native_agent': '027bd16d96010544331c953c0e1014e161786e71', 'cases': cases}
if update:
    path.write_text(json.dumps(data, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n')
else:
    assert json.loads(path.read_text()) == data
print(f'{len(cases)} exact native own-key commands, after bundles and full records ' +
      ('regenerated' if update else 'verified'))
