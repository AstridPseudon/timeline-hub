"""Check sequential parent deletes against frozen Agent 027bd16d on PYTHONPATH."""
import copy
import json
import subprocess
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.capture import capture_clip_delete
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_clip_delete import delete_document

TARGET = Path(__file__).with_name('recipe_m2_clip_delete_batch.json')
AGENT_SOURCE = '027bd16d96010544331c953c0e1014e161786e71'


def capture(bundle, members):
    commands = []
    current = copy.deepcopy(bundle)
    for member in members:
        command = capture_clip_delete(current, 'parent/clip:' + member['clipId'])
        commands.append(command)
        current = execute(current, [command]).bundle
    plan = execute(bundle, commands)
    assert plan.bundle == current
    return plan


def reload(bundle):
    return bundle_from_document(json.loads(json.dumps(document_from_bundle(bundle))))


def refused(action):
    try:
        action()
    except CommandError as error:
        return error.kind
    raise AssertionError('unsupported batch accepted')


def main():
    assert sys.argv[1:] in ([], ['--update'])
    seed = json.loads(TARGET.with_name('recipe_m2_app_clip_delete.json').read_text())['bundle']
    members = [dict(clipId=key, ownerRef='parent') for key in ['clip-b', 'clip-a']]
    cases = []

    def add(name, original, targets=members):
        before = copy.deepcopy(original)
        plan = capture(original, targets)
        assert original == before
        assert replay(plan, original).records == plan.records
        removed = reload(plan.bundle)
        undone = inverse(removed, plan.records)
        restored = reload(undone.bundle)
        assert restored['parent'] == original['parent']
        redo = inverse(restored, accepted_boundaries(undone.records, removed, restored))
        assert document_from_bundle(redo.bundle) == document_from_bundle(removed)
        cases.append(dict(name=name, bundle=original, members=targets, commands=plan.commands,
                          records=plan.records, after_bundle=plan.bundle,
                          output=document_from_bundle(plan.bundle), inverse_output=document_from_bundle(restored),
                          redo_output=document_from_bundle(redo.bundle)))
        return plan

    plan = add('ordered-subset', copy.deepcopy(seed))
    add('all-rows-final-mirror', copy.deepcopy(seed), members + [dict(clipId='clip-c', ownerRef='parent')])
    add('retained-occurrence-closure', bundle_from_document(delete_document()))
    for name, key, value in [('config-only', 'clips', 'absent'), ('payload-only', 'config', 'absent'),
                             ('null-payload', 'clips', None), ('null-mirror', 'config', None)]:
        bundle = copy.deepcopy(seed)
        container = bundle['parent'] if key == 'clips' else bundle['parent']['config']
        if value == 'absent':
            del container['clips']
        else:
            container['clips'] = value
        add(name, bundle)

    refusals = []
    for name in ['order', 'membership', 'dependency', 'second-row']:
        bundle = copy.deepcopy(seed)
        rows = bundle['parent']['clips']
        if name == 'order':
            rows.reverse()
        elif name == 'membership':
            rows.append({**rows[-1], 'id': 'new'})
        elif name == 'dependency':
            rows[-1]['app'] = {'astrid': {'on': 'clip-a'}}
        else:
            rows[0]['opaque'] = {'changed': None}
        bundle['parent']['config']['clips'] = copy.deepcopy(rows)
        before = copy.deepcopy(bundle)
        kind = refused(lambda: execute(bundle, plan.commands))
        assert bundle == before
        refusals.append(dict(name=name, bundle=bundle, commands=plan.commands, kind=kind))

    unsupported = copy.deepcopy(seed)
    unsupported['parent']['clips'][0]['children'] = []
    unsupported['parent']['config']['clips'] = copy.deepcopy(unsupported['parent']['clips'])
    first = capture_clip_delete(unsupported, 'parent/clip:clip-b')
    intermediate = execute(unsupported, [first]).bundle
    assert refused(lambda: capture_clip_delete(intermediate, 'parent/clip:clip-a')) == 'unsupported_ownership'
    before = copy.deepcopy(unsupported)
    assert refused(lambda: capture(unsupported, members)) == 'unsupported_ownership'
    assert unsupported == before

    disjoint = copy.deepcopy(seed)
    disjoint['parent']['clips'][-1]['opaque'] = {'accepted': [None, False]}
    disjoint['parent']['config']['clips'] = copy.deepcopy(disjoint['parent']['clips'])
    intervening = [later('parent/clip:clip-c', ['opaque'], {'accepted': [None, False]})]
    rebased = replay(plan, disjoint, intervening_records=intervening)
    undone = inverse(reload(rebased.bundle), plan.records, intervening)
    assert undone.bundle['parent'] == disjoint['parent']
    for ref, path, value in [('parent/clip:clip-a', ['id'], 'clip-a'), ('parent', ['clips'], []),
                             ('parent/clip:clip-b', ['asset'], 'picture')]:
        writes = [later(ref, path, value)]
        assert refused(lambda: inverse(plan.bundle, plan.records, writes)) == 'intervening_write'
        if path == ['id'] or ref == 'parent':
            assert refused(lambda: replay(plan, seed, intervening_records=writes)) == 'intervening_write'

    expected = dict(agent_source=AGENT_SOURCE, input=document_from_bundle(seed), cases=cases,
                    second_member_refusal=unsupported, refusals=refusals,
                    disjoint=dict(bundle=disjoint, after_bundle=rebased.bundle, inverse_bundle=undone.bundle))
    encoded = json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n'
    if sys.argv[1:] == ['--update']:
        TARGET.write_text(encoded)
    else:
        assert TARGET.read_text() == encoded, 'native delete batch changed; review before regenerating'
    js = """
import assert from 'node:assert/strict';
import { captureClipDeleteBatch, finishClipDeleteBatch, executeClipDeleteBatch } from './src/tools/video-editor/commands/clipDeleteBatchCapture.ts';
const golden = GOLDEN;
for (const entry of golden.cases) {
  const basis = captureClipDeleteBatch(entry.bundle, entry.members);
  const result = finishClipDeleteBatch(JSON.parse(JSON.stringify(basis)));
  assert.deepEqual(result.commands, entry.commands);
  assert.deepEqual(result.records, entry.records);
  assert.deepEqual(result.bundle, entry.after_bundle);
  assert.deepEqual(executeClipDeleteBatch(entry.bundle, entry.commands), result);
}
console.log('Agent 027: 7 exact sequential command/record/full-result cases; native reload inverse/redo, atomic second-member/order/dependency refusals, disjoint replay/inverse and strict ABA PASS');
""".replace('GOLDEN', encoded)
    subprocess.run(['node', '--import', 'tsx', '--input-type=module'], input=js, text=True, check=True)


if __name__ == '__main__':
    main()
