"""Check batch capture/execute/records/undo against frozen Agent 027 on PYTHONPATH."""
import copy
import json
import subprocess
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._split_commands import capture_clip_split
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle
from tests.editing_conformance.test_recipe_m1_commands import inverse, later

FIXTURES = Path(__file__).parent
TARGET = FIXTURES / 'recipe_m2_clip_split_batch.json'
AGENT_SOURCE = '027bd16d96010544331c953c0e1014e161786e71'


def main():
    assert sys.argv[1:] in ([], ['--update'])
    document = json.loads((FIXTURES / 'recipe_m2_clip_split.json').read_text())['input']
    parent = document['parent_revision']['payload']
    parent['clips'][1] = {**copy.deepcopy(parent['clips'][0]), 'id': 'clip-b'}
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    parent['opaque_batch'] = {'keep': [None, False, {}]}
    document['parent_revision']['content_digest'] = _digest(parent)
    original = bundle_from_document(document)
    members = [{'clipId': 'clip-b', 'rightId': 'right:b'}, {'clipId': 'clip-a', 'rightId': 'right:a'}]
    commands = []
    next_bundle = copy.deepcopy(original)
    for member in members:
        command = capture_clip_split(next_bundle, 'parent/clip:' + member['clipId'], on=3, right_id=member['rightId'])
        commands.append(command)
        next_bundle = execute(next_bundle, [command]).bundle
    plan = execute(original, commands)
    assert plan.bundle == next_bundle
    assert execute(original, commands).records == plan.records
    undone = inverse(bundle_from_document(document_from_bundle(plan.bundle)), plan.records)
    assert document_from_bundle(undone.bundle)['parent_revision']['payload'] == parent
    assert document_from_bundle(inverse(undone.bundle, undone.records).bundle) == document_from_bundle(plan.bundle)
    for name, changed in [('order', list(reversed(parent['clips']))),
                          ('membership', parent['clips'] + [{**parent['clips'][0], 'id': 'inserted'}])]:
        bundle = copy.deepcopy(original)
        bundle['parent']['clips'] = copy.deepcopy(changed)
        bundle['parent']['config']['clips'] = copy.deepcopy(changed)
        try:
            execute(bundle, commands)
        except CommandError:
            pass
        else:
            raise AssertionError(name)
    refused = copy.deepcopy(original)
    refused['parent']['clips'][0]['time_map'] = {}
    refused['parent']['config']['clips'] = copy.deepcopy(refused['parent']['clips'])
    first = capture_clip_split(refused, 'parent/clip:clip-b', on=3, right_id='right:b')
    intermediate = execute(refused, [first]).bundle
    try:
        capture_clip_split(intermediate, 'parent/clip:clip-a', on=3, right_id='right:a')
    except CommandError:
        pass
    else:
        raise AssertionError('unsupported second member accepted')
    try:
        inverse(plan.bundle, plan.records, [later('parent/clip:clip-a', ['to'], 6)])
    except CommandError as error:
        assert error.kind == 'intervening_write'
    else:
        raise AssertionError('ABA undo accepted')
    expected = {'agent_source': AGENT_SOURCE, 'input': document, 'members': members, 'on': 3,
                'bundle': original, 'commands': plan.commands, 'records': plan.records,
                'after_bundle': plan.bundle, 'output': document_from_bundle(plan.bundle),
                'inverse_output': document_from_bundle(undone.bundle)}
    encoded = json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n'
    if sys.argv[1:] == ['--update']:
        TARGET.write_text(encoded)
    else:
        assert TARGET.read_text() == encoded, 'native split batch changed; review before regenerating'
    js = """
import assert from 'node:assert/strict';
import { captureClipSplitBatch, finishClipSplitBatch, executeClipSplitBatch } from './src/tools/video-editor/commands/clipSplitBatchCapture.ts';
const golden = GOLDEN;
const basis = captureClipSplitBatch(golden.bundle, golden.members, golden.on);
const result = finishClipSplitBatch(JSON.parse(JSON.stringify(basis)));
assert.deepEqual(result.commands, golden.commands);
assert.deepEqual(result.records, golden.records);
assert.deepEqual(result.bundle, golden.after_bundle);
assert.deepEqual(executeClipSplitBatch(golden.bundle, golden.commands), result);
console.log('Agent 027 batch: exact sequential capture/execute/records/full after-bundle; native reload inverse/redo, membership/order refusal, second-member refusal and guarded ABA undo PASS');
""".replace('GOLDEN', encoded)
    subprocess.run(['node', '--import', 'tsx', '--input-type=module'], input=js, text=True, check=True)


if __name__ == '__main__':
    main()
