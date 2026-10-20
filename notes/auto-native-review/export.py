"""Independent vectors; import only an explicit frozen Agent archive via PYTHONPATH."""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.native_auto_placement import auto_place_completion, auto_place_shared
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance import test_recipe_m2_auto_placement as completion
from tests.editing_conformance import test_recipe_m2_shared_auto_placement as shared
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse

OWNER = completion.OWNER
vectors = []


def emit(name, bundle, approval, verified, command=None):
    before = copy.deepcopy(bundle)
    item = dict(name=name, bundle=bundle, approval=approval, media=verified[1]['selection'],
                verified=verified[1])
    try:
        if command is None:
            kwargs = dict(ownership='occurrence', verified_media=verified, anchor=approval['anchor'])
            if approval['mode'] == 'completion':
                kwargs.update(preferred_track=approval['preferredTrack'], fallback_at=approval['fallbackAt'],
                              fallback_track=approval['fallbackTrack'], duration=approval.get('duration'))
                result = auto_place_completion(bundle, OWNER, 'placed', item['media'], **kwargs)
            else:
                result = auto_place_shared(bundle, OWNER, 'placed', item['media'], frame=approval['frame'], **kwargs)
            plan = execute(bundle, result['commands'], verified_media=verified)
            assert replay(plan, bundle, verified_media=verified).records == plan.records
            undone = inverse(plan.bundle, plan.records)
            assert undone.bundle == bundle
            assert inverse(undone.bundle, accepted_boundaries(undone.records, plan.bundle, undone.bundle)).bundle == plan.bundle
            item['expected'] = dict(**result, records=plan.records, bundle=plan.bundle)
        else:
            item['command'] = command
            plan = execute(bundle, [command], verified_media=verified)
            item['expected'] = dict(command=plan.commands[0], record=plan.records[0], bundle=plan.bundle)
    except CommandError as error:
        item['refusal'] = error.kind
        if command is not None:
            item['command'] = command
    assert bundle == before
    vectors.append(item)


for module, mode in [(completion, 'completion'), (shared, 'shared')]:
    for name in module.CASES:
        _, bundle, result, verified = module.case(name)
        plan = execute(bundle, result['commands'], verified_media=verified)
        assert json.loads(module.FIXTURE.read_text())[name] == dict(
            commands=result['commands'], capture=result['capture'], child=State(plan.bundle).entity(module.CHILD))
        approval = dict(autoApprove=True, owner=OWNER, ownership='occurrence', clipId='placed',
                        mode=mode, anchor=result['capture']['anchor']['id'])
        approval.update(dict(preferredTrack=None, fallbackAt=None, fallbackTrack=None) if mode == 'completion'
                        else dict(frame=result['capture'].get('requested_frame')))
        emit(mode + '-' + name, bundle, approval, verified)


def fresh(kind, mode):
    _, bundle, _, verified = (completion.build(kind, 'clip-a', wide=True, overlay=True)
                             if mode == 'completion' else shared.build(kind, anchor='clip-c'))
    approval = dict(autoApprove=True, owner=OWNER, ownership='occurrence', clipId='placed', mode=mode,
                    anchor='clip-a' if mode == 'completion' else 'clip-c')
    approval.update(dict(preferredTrack=None, fallbackAt=None, fallbackTrack=None) if mode == 'completion'
                    else dict(frame=None))
    return bundle, approval, verified


def mutate(bundle, label, verified):
    config = State(bundle).config(OWNER)
    clip = config['clips'][0]
    if label == 'fractional-trim-speed':
        clip.pop('hold', None)
        clip.update(at=1.2345, **{'from': 0.25, 'to': 3.75, 'speed': 1.5})
    elif label == 'at-ms':
        clip['at_ms'] = clip.pop('at') * 1000
    elif label == 'opaque-consumed':
        clip['opaque'] = {'clear': None, 'nested': [1, 2]}
    elif label == 'empty':
        config['clips'].clear()
    elif label == 'source-window':
        config['source_window'] = {'from': 0, 'to': 20}
    elif label == 'non-output':
        config['tracks'][0]['role'] = 'input'
    elif label == 'shared-owner':
        bundle['placements'][1]['shot_id'] = bundle['placements'][0]['shot_id']
    elif label == 'pool':
        config['app'] = {'astrid': {'pool': ['reserved-new']}}
    elif label == 'legacy':
        bundle['parent']['config']['pinnedShotGroups'] = [{'id': 'legacy'}]
    elif label in ('exact-binding', 'opaque-binding'):
        pin = verified[1]['selection']
        binding = dict(media_id=pin['object_id'], type=verified[1]['media_type'].split('/')[0],
                       generationId=pin['generation_id'], variantId=pin['variant_id'])
        if label == 'opaque-binding':
            binding['opaque'] = True
        config['registry']['assets'][pin['asset']] = binding
    elif label == 'duplicate-member':
        config['clips'].append(copy.deepcopy(clip))
    elif label == 'reorder':
        config['clips'].reverse()
    elif label == 'new-member':
        config['clips'].append(dict(id='extra', at=2, hold=1, track='picture'))
    elif label == 'extent':
        bundle['placements'][0]['duration_ms'] += 1000
    elif label == 'parent-fps':
        bundle['parent']['config']['output']['fps'] = 25
    elif label == 'child-fps':
        config['output']['fps'] = 25
    elif label == 'inherited-lane':
        config['clips'][-1]['track'] = 'picture'
    elif label == 'irrelevant':
        bundle['parent']['name'] = 'Unrelated rename'
        State(bundle).config('occurrence:occ-b')['clips'][0]['at'] = 2


for kind in ('image', 'video'):
    for mode in ('completion', 'shared'):
        for label in ('fractional-trim-speed', 'at-ms', 'opaque-consumed', 'empty', 'source-window',
                      'non-output', 'shared-owner', 'exact-binding', 'opaque-binding', 'duplicate-member'):
            bundle, approval, verified = fresh(kind, mode)
            mutate(bundle, label, verified)
            emit(f'{mode}-{kind}-build-{label}', bundle, approval, verified)
        bundle, approval, verified = fresh(kind, mode)
        emit('seed', bundle, approval, verified)
        command = vectors.pop()['expected']['commands'][0]
        for label in ('fractional-trim-speed', 'opaque-consumed', 'source-window', 'non-output', 'shared-owner',
                      'pool', 'legacy', 'opaque-binding', 'duplicate-member', 'reorder', 'new-member', 'extent',
                      'parent-fps', 'child-fps', 'inherited-lane', 'irrelevant'):
            head = copy.deepcopy(bundle)
            mutate(head, label, verified)
            emit(f'{mode}-{kind}-replay-{label}', head, approval, verified, command)
        # Isolate the corrected pool/eligibility reads from registry creation.
        # The exact alias is already present; pool add writes no asset binding.
        for pool_state in ('absent', 'empty'):
            for eligibility in ('absent', 'null', 'empty'):
                bundle, approval, verified = fresh(kind, mode)
                mutate(bundle, 'exact-binding', verified)
                if pool_state == 'empty':
                    State(bundle).config(OWNER)['app'] = {'astrid': {'pool': []}}
                if eligibility != 'absent':
                    bundle['parent']['config']['pinnedShotGroups'] = None if eligibility == 'null' else []
                emit('seed', bundle, approval, verified)
                command = vectors.pop()['expected']['commands'][0]
                for label in ('pool', 'legacy'):
                    head = copy.deepcopy(bundle)
                    mutate(head, label, verified)
                    emit(f'{mode}-{kind}-bound-{pool_state}-{eligibility}-{label}', head, approval, verified, command)
    for label, anchor, saved in [('saved', 'gone', dict(fallback_at=22.25, fallback_track='overlay')),
                                 ('preferred', 'clip-a', dict(preferred_track='overlay'))]:
        _, bundle, _, verified = completion.build(kind, anchor, wide=True, overlay=True, **saved)
        approval = dict(autoApprove=True, owner=OWNER, ownership='occurrence', clipId='placed',
                        mode='completion', anchor=anchor, preferredTrack=saved.get('preferred_track'),
                        fallbackAt=saved.get('fallback_at'), fallbackTrack=saved.get('fallback_track'))
        emit(kind + '-' + label, bundle, approval, verified)

Path(sys.argv[1]).write_text(json.dumps(vectors, allow_nan=False))
print(f'{len(vectors)} independent vectors; original frozen fixtures, full records/bundles, replay/inverse/redo checked')
