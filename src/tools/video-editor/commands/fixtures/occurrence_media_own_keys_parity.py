"""Export/check asset-key parity using frozen Agent 027bd16 on PYTHONPATH.

Only native capture and execute supply the commands, records and after bundles.
The original media golden is read without changing its bytes or cases.
"""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_occurrence_media_commands import (
    capture_occurrence_add_media,
    capture_occurrence_swap_media,
)
from astrid.sdk.timeline.rebase import replay

path = Path(__file__).with_name('recipe_m2_occurrence_media_own_keys.json')
original = json.loads(path.with_name('recipe_m2_occurrence_media.json').read_text())
owner = 'occurrence:occ-a'
target = owner + '/clip:clip-a'
keys = ('__proto__', 'constructor', 'toString')
update = sys.argv[1:] == ['--update']
if sys.argv[1:] and not update:
    raise SystemExit('usage: occurrence_media_own_keys_parity.py [--update]')


def inverse(bundle, records):
    return execute(bundle, [{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                            'select': None, 'args': {'publications': ['accepted-publication']}}],
                   inverse_records=records)


def capture(case):
    call = case['plain']
    if call['op'] == 'occurrence.add-media':
        return capture_occurrence_add_media(case['bundle'], call['select'], call['args']['row'],
                                            call['args']['media'], verified_media=case['verified_media'])
    return capture_occurrence_swap_media(case['bundle'], call['select'], call['args']['old_media'],
                                         call['args']['media'], verified_media=case['verified_media'])


data = {'cases': [], 'refusals': [], 'replay_refusals': []}
for operation, golden in original.items():
    baseline = bundle_from_document(golden['input'])
    # Preserve and verify every field of both original goldens against native.
    plan = execute(baseline, golden['commands'], verified_media=golden['verified_media'])
    assert plan.records == golden['records']
    assert document_from_bundle(plan.bundle) == golden['output']
    for key in keys:
        modes = ('birth', 'existing', 'old') if operation == 'swap' else ('birth', 'existing')
        for mode in modes:
            bundle = copy.deepcopy(baseline)
            plain = {field: copy.deepcopy(golden['commands'][0][field]) for field in
                     ('schema_version', 'op', 'version', 'select', 'args', 'intent')}
            verified = copy.deepcopy(golden['verified_media'])
            assets = State(bundle).config(owner)['registry']['assets']
            assets['untouched'] = {'opaque': [None, False, {}], 'nullable': None}
            if mode == 'old':
                assets[key] = assets.pop('picture')
                State(bundle).entity(target)['asset'] = key
                plain['args']['old_media']['asset'] = key
                verified[0]['selection']['asset'] = key
            else:
                plain['args']['media']['asset'] = key
                verified[1]['selection']['asset'] = key
                if operation == 'add':
                    plain['args']['row']['asset'] = key
            pin = plain['args']['media']
            binding = {'media_id': pin['object_id'], 'type': 'video',
                       'generationId': pin['generation_id'], 'variantId': pin['variant_id']}
            if mode == 'existing':
                assets[key] = binding
            case = {'name': f'{operation}_{mode}_{key}', 'operation': operation, 'mode': mode,
                    'key': key, 'bundle': bundle, 'plain': plain, 'verified_media': verified}
            before = copy.deepcopy(case)
            command = capture(case)
            plan = execute(bundle, [command], verified_media=verified)
            assert execute(bundle, [plain], verified_media=verified).records == plan.records
            assert replay(plan, bundle, verified_media=verified).records == plan.records
            assert inverse(plan.bundle, plan.records).bundle == bundle
            assert case == before
            case.update(command=command, after_bundle=plan.bundle, records=plan.records)
            data['cases'].append(case)
            if mode != 'birth':
                continue
            for label, entry in (('null', None), ('opaque', {**binding, 'opaque': None})):
                refused = copy.deepcopy(before)
                refused['name'] += '_' + label
                State(refused['bundle']).config(owner)['registry']['assets'][key] = entry
                snapshot = copy.deepcopy(refused)
                try:
                    capture(refused)
                except CommandError as exc:
                    assert refused == snapshot
                    refused['error'] = {'kind': exc.kind, 'message': str(exc)}
                else:
                    raise AssertionError(('native accepted occupied alias', refused['name']))
                data['refusals'].append(refused)
            for damage in ('membership', 'reservation'):
                head = copy.deepcopy(bundle)
                if damage == 'membership':
                    State(head).config(owner)['clips'].append({'id': 'other'})
                else:
                    State(head).config(owner)['registry']['assets'][key] = copy.deepcopy(binding)
                refused = {'name': before['name'] + '_' + damage, 'bundle': head,
                           'command': command, 'verified_media': verified}
                snapshot = copy.deepcopy(refused)
                try:
                    execute(head, [command], verified_media=verified)
                except CommandError as exc:
                    assert refused == snapshot
                    refused['error'] = {'kind': exc.kind, 'message': str(exc)}
                else:
                    raise AssertionError(('native accepted stale capture', refused['name']))
                data['replay_refusals'].append(refused)

if update:
    path.write_text(json.dumps(data, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n')
else:
    assert json.loads(path.read_text()) == data
print(f"2 original media goldens; {len(data['cases'])} full native capture/execute/replay/inverse cases; "
      f"{len(data['refusals'])} occupied-alias refusals; {len(data['replay_refusals'])} stale-capture refusals "
      + ('regenerated' if update else 'verified'))
