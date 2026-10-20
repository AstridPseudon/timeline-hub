"""Check/regenerate label + hold batches with frozen Agent 027bd16d on PYTHONPATH."""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.commands import execute

FIXTURES = Path(__file__).parent
TARGET = FIXTURES / 'recipe_m2_generic_patch.json'
SOURCE = '027bd16d96010544331c953c0e1014e161786e71'


def main():
    if sys.argv[1:] not in ([], ['--update']):
        raise SystemExit('usage: generic_patch_parity.py [--update]')
    bundle = json.loads((FIXTURES / 'recipe_m2_app_clip_scalar_fields.json').read_text())['bundle']
    cases = []
    for select in ['parent/clip:f2-transition-clip', 'occurrence:f2-occurrence/clip:f2-agent-clip']:
        original = copy.deepcopy(bundle)
        track = original['parent']['config']['tracks'][0]['id']
        inputs = [
            {'op': 'track.update', 'target': track, 'payload': {'label': 'Picture α'}, 'order': -2},
            {'op': 'clip.update', 'target': select.rsplit('clip:', 1)[1], 'payload': {'hold': 4.123456789}, 'order': -1},
            {'op': 'track.update', 'target': track, 'payload': {'label': ''}},
            {'op': 'clip.update', 'target': select.rsplit('clip:', 1)[1], 'payload': {'hold': 3.987654321}},
        ]
        commands = []
        current = copy.deepcopy(original)
        owners = [f'parent/track:{track}', select, f'parent/track:{track}', select]
        for operation, owner in zip(inputs, owners):
            if operation['op'] == 'track.update':
                command = capture_track_set(current, owner, values=operation['payload'])
            else:
                command = capture_clip_set(current, owner, values=operation['payload'])
            commands.append(command)
            current = execute(current, [command]).bundle
        plan = execute(original, commands)
        assert original == bundle
        independent = capture_clip_set(plan.bundle, 'parent/clip:f2-app-clip', values={'hold': 2.5})
        intervening = execute(plan.bundle, [independent])
        inverse = {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
                   'args': {'publications': ['label-hold-batch']}}
        undone = execute(intervening.bundle, [inverse], inverse_records=plan.records,
                         intervening_records=intervening.records)
        assert len(undone.records) == 1
        assert undone.bundle == execute(original, [independent]).bundle
        cases.append({'patch': {'version': 1, 'operations': inputs}, 'owners': owners,
                      'bundle': original, 'commands': commands, 'records': plan.records,
                      'after_bundle': plan.bundle})
    expected = {'agent_source': SOURCE, 'cases': cases}
    encoded = json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n'
    if sys.argv[1:] == ['--update']:
        TARGET.write_text(encoded)
    else:
        assert TARGET.read_text() == encoded, 'native generic patch golden changed'
    print('Agent 027bd16d: 2 exact sequential label/hold command, record and full-bundle cases; '
          'one guarded inverse per batch preserves an intervening independent hold')


if __name__ == '__main__':
    main()
