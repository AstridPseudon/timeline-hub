import copy
import json
from pathlib import Path
from tests.helpers.runtime import use_runtime

use_runtime()
import runtime_protocol.timeline_commit_auth as auth
from runtime_protocol.timeline_commit import CommitRejected

path = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-historical-inverse-sol-0236/historical-inverse-auth-0.json')
packet = json.loads(path.read_text())
records = packet['prepared']['records']
step = records['steps'][0]
boundary = auth.images(packet['source'])
accepted = auth.images(packet['prepared']['canonical_document'])
output = auth.step_output(boundary, step, records, accepted, original=boundary)


def expect_rejection(label, callback, message):
    try:
        callback()
    except CommitRejected as exc:
        assert message in str(exc), str(exc)
        print(label + ': ' + str(exc))
    else:
        raise AssertionError(label + ': unexpectedly accepted')


assert len(auth._inverse_stage_ranges(step, records, packet['history'])) == 1
print('original source-stage native partition: VALID (1 native write, 3 effects)')
expect_rejection('exact captured full authentication', lambda: auth.validate(**packet),
                 'native writes do not cover')

extra = copy.deepcopy(records)
shot, _ = auth._inverse_stage_root(boundary, 'shot:shared')
extra['commands'][0]['writes'].append({'ref': 'shot:shared', 'path': [],
    'before': shot, 'after': {'state': 'absent'}})
next(b for b in extra['commands'][0]['bindings'] if b['key'] == 'inverse.stage')['boundary']['native_write_range'] = [0, 2]
expect_rejection('append exact shot/internal aggregate retirement',
    lambda: auth._inverse_stage_ranges(step, extra, packet['history']), 'native ranges are missing')

canonical = copy.deepcopy(records)
canonical['commands'][0]['writes'] = [
    {'ref': e['ref'], 'path': e['path'], 'before': e['before'],
     'after': {'state': 'present', 'value': e['value']} if e['op'] == 'set' else {'state': 'absent'}}
    for e in step['patch']]
next(b for b in canonical['commands'][0]['bindings'] if b['key'] == 'inverse.stage')['boundary']['native_write_range'] = [0, 3]
expect_rejection('observe all three exact canonical sites',
    lambda: auth._inverse_stage_ranges(step, canonical, packet['history']), 'native ranges are missing')


def check_bindings(candidate):
    auth.validate_bindings(packet['request'], candidate, packet['prepared']['expected_head'],
        boundary, output, step, 0, packet['continuations'], boundary, boundary)

check_bindings(records)
print('unmodified isolated physical/effect binding checks: VALID')
for owners in ([], ['occurrence:one/shot'], ['occurrence:shared-copy/shot', 'occurrence:extra/shot']):
    changed = copy.deepcopy(records)
    for binding in changed['commands'][0]['bindings']:
        if binding.get('key') == 'commit.effect' and 'owners' in binding:
            binding['owners'] = owners
    expect_rejection('retirement owner negative ' + repr(owners), lambda: check_bindings(changed),
        'owners differ from its physical edges')

for damage in ('missing-history', 'forged-publication', 'wrong-receipt'):
    history = copy.deepcopy(packet['history'])
    key = next(iter(history))
    if damage == 'missing-history':
        history = {}
    elif damage == 'forged-publication':
        history[key]['publication_id'] = 'forged'
    else:
        history[key]['receipt']['receipt_id'] = 'forged'
    expect_rejection('source stage negative ' + damage,
        lambda: auth._inverse_stage_ranges(step, records, history), 'inverse stage')
