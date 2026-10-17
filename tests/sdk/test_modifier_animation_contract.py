"""Adopted144: real J029 schema through existing complete-pair/history paths.

Only the existing acceptance port and scene-answer fixture are synthetic. No
component declaration/schema is mocked; exact original pack bytes are copied
into the test's explicit trusted-extra source for mutation-negative isolation.
"""
import copy
import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest
from test_timeline_app_keyframes import clip, source, wire
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from test_timeline_writer_direct_receipts import accepted, roundtrip

from astrid.core.pack.components import component_discovery_scope, resolve_component
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline import commands, modifiers
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.rebase import rebase

pytestmark = pytest.mark.usefixtures('synthetic_scene_answers')
IDENTITY = 'timeline.component/fresh_vignette_029.vignette'
PATH = 'modifiers["shade"].params.strength'
KEYS = {
    PATH: [dict(time=0, value=0, interpolation='linear', opaque={'retain': [None, False, 1.125]}),
           dict(time=1, value=1, interpolation='linear')],
    'modifiers["other"].params.strength': [dict(time=0, value=.6, interpolation='hold')],
    'literal.key[0]': [dict(time=7.125, value=False, interpolation='hold', opaque={'old': True})],
}


@pytest.fixture
def real_source(tmp_path, monkeypatch):
    selected = os.environ.get('I_MODIFIER_TEST_PACK')
    if not selected:
        pytest.skip('explicit immutable J029 pack required for external component integration')
    original = Path(selected)
    for name, digest in [('vignette.yaml', '19c32dd2f6222d2d90204e1bbfc0afa39be677dc04e9600b0f318d5ccf8bf010'),
                         ('vignette.tsx', 'fcded70fe529fb02aa59d79d1b0845f865950a3060786d073898212e429d0c39')]:
        assert hashlib.sha256((original / 'extensions/timeline.component' / name).read_bytes()).hexdigest() == digest
    root = tmp_path / 'packs' / 'fresh_vignette_029'
    shutil.copytree(original, root)
    monkeypatch.delenv('ASTRID_PACKS_PATH', raising=False)
    from astrid.core.pack.source_setup import provision
    state = tmp_path / 'test-sources.json'
    provision(state_path=state, data_root=tmp_path / 'source-data')
    monkeypatch.setenv('ASTRID_SOURCE_STATE', str(state))
    discovery = dict(project_root=tmp_path / 'empty', extra_pack_roots=(str(root.parent),))
    with component_discovery_scope(**discovery):
        component = resolve_component(IDENTITY, **discovery)
        assert component.eligible
        assert component.implementation_digest == '1ac864cc8cf36842bc9fecddc80761f601eb88b7447eab8df6daf72a9ab98d0b'
        yield root


@pytest.fixture
def initial(real_source):
    fixture = Path(__file__).parents[1] / 'fixtures/timeline_editing/tiny_publishable.json'
    before, sid = source(Checkout(json.loads(fixture.read_text())).document(), 'parent')
    target = clip(before, sid).data
    target.update(keyframeOrigin=.25, modifiers=[
        dict(id='shade', element=IDENTITY, params=dict(strength=.2)),
        dict(id='other', element=IDENTITY, params=dict(strength=.7)),
    ])
    return before, sid


def author(initial, keys=None):
    before, sid = initial
    return wire(before, sid, keyframes=copy.deepcopy(KEYS if keys is None else keys), keyframeOrigin=.25)


def test_real_schema_command_compile_save_fresh_readback_and_receipt_undo_redo(initial, tmp_path):
    before, sid = initial
    before = copy.deepcopy(before)
    other = Checkout(before).clip('a-rocket').data
    other['modifiers'] = [dict(id='shade', element=IDENTITY, params=dict(strength=.9))]
    other['keyframeOrigin'] = .25
    after, plan, receipt = accepted(before, [author(initial)])
    row = clip(after, sid).data
    assert row['keyframes'] == KEYS
    assert row['modifiers'] == clip(before, sid).data['modifiers']
    assert after['shots'] == before['shots']  # same local instance ID in another occurrence
    recorded = plan.calls[0]
    assert recorded.expect['modifiers["shade"]']['value']['params'] == {'strength': .2}
    declaration = recorded.expect['modifierDeclarations[' + json.dumps(IDENTITY) + ']']['value']
    assert declaration['implementation_digest'] == '1ac864cc8cf36842bc9fecddc80761f601eb88b7447eab8df6daf72a9ab98d0b'
    assert declaration['descriptor']['params']['properties']['strength']['maximum'] == 1
    roundtrip(before, after, plan, receipt)
    saved = tmp_path / 'actual.checkout.json'
    Checkout(copy.deepcopy(after)).save(saved, quiet=True)
    fresh = Checkout.load(saved).document()
    assert clip(fresh, sid).data['keyframes'] == KEYS
    publication = compile_authoring_candidate(fresh).publication
    compiled = next(row for row in publication['parent_composition']['clips'] if row['id'] == 'movie')
    assert compiled['keyframes'] == KEYS and compiled['keyframeOrigin'] == .25
    if os.environ.get('I_MODIFIER_READBACK'):
        Path(os.environ['I_MODIFIER_READBACK']).write_text(json.dumps(dict(target=compiled, authoredKeys=KEYS), indent=2))


@pytest.mark.parametrize('operation', ['clear-curve', 'remove-instance'])
def test_curve_clear_and_instance_remove_have_exact_receipt_undo_redo(initial, operation):
    before, sid = initial
    authored, _, first = accepted(before, [author(initial)])
    if operation == 'clear-curve':
        keys = {key: copy.deepcopy(value) for key, value in KEYS.items() if key != PATH}
        call = wire(authored, sid, keyframes=keys, keyframeOrigin=.25)
    else:
        call = dict(op='clip.clear', select=sid, args={'keys': ['modifiers["shade"]']})
    after, plan, receipt = accepted(authored, [call], first)
    row = clip(after, sid).data
    assert PATH not in row['keyframes']
    assert row['keyframes']['literal.key[0]'] == KEYS['literal.key[0]']
    assert row['keyframes']['modifiers["other"].params.strength'] == KEYS['modifiers["other"].params.strength']
    assert row['modifiers'][-1] == clip(authored, sid).data['modifiers'][-1]
    if operation == 'clear-curve':
        assert row['modifiers'][0]['params'] == {'strength': .2}
    else:
        assert [instance['id'] for instance in row['modifiers']] == ['other']
        assert any(effect['path'] == 'keyframes' for effect in plan.consequences)
    roundtrip(authored, after, plan, receipt)


def test_instance_reorder_preserves_curves_and_rebases_pending_authoring(initial):
    before, sid = initial
    authored, plan, _ = accepted(before, [author(initial)])
    reorder = dict(op='clip.set-param', select=sid, args=dict(path='modifiers.order', value=['other', 'shade']))
    head, _, _ = RuntimeCommitService._apply(before, [reorder])
    rebased = rebase(plan.calls, head)
    assert not rebased.conflicts
    target = clip(rebased.document, sid).data
    assert [row['id'] for row in target['modifiers']] == ['other', 'shade']
    assert target['keyframes'] == clip(authored, sid).data['keyframes']


@pytest.mark.parametrize('fault', ['static-edit', 'deletion', 'identity-replacement', 'resource-change'])
def test_reserved_write_has_instance_static_and_actual_resource_read_dependencies(initial, real_source, fault):
    before, sid = initial
    _, plan, _ = accepted(before, [author(initial)])
    head = copy.deepcopy(before)
    row = clip(head, sid).data
    if fault == 'static-edit':
        row['modifiers'][0]['params']['strength'] = .3
    elif fault == 'deletion':
        row['modifiers'].pop(0)
    elif fault == 'identity-replacement':
        row['modifiers'][0]['element'] = 'timeline.component/foreign.vignette'
    else:
        resource = real_source / 'extensions/timeline.component/vignette.tsx'
        resource.write_text(resource.read_text() + '\n// changed admitted implementation resource\n')
    old = copy.deepcopy(head)
    result = rebase(plan.calls, head)
    assert result.conflicts
    assert head == old


@pytest.mark.parametrize('fault', ['path', 'index', 'ambiguous', 'instance', 'leaf', 'nested', 'nan-time',
    'infinite-value', 'bool-value', 'negative', 'range', 'easing', 'interpolation', 'missing-origin'])
def test_invalid_modifier_curves_refuse_the_actual_complete_pair_atomically(initial, fault):
    before, sid = initial
    call = author(initial)
    keys = call['args']['keyframes']
    key = keys[PATH][0]
    if fault in {'path', 'index', 'ambiguous', 'instance', 'leaf', 'nested'}:
        target = {'path': 'modifiers.shade.params.strength', 'index': 'modifiers[0].params.strength',
                  'ambiguous': 'modifiers["\\u0073hade"].params.strength', 'instance': 'modifiers["foreign"].params.strength',
                  'leaf': 'modifiers["shade"].params.radius', 'nested': 'modifiers["shade"].params.nested.x'}[fault]
        keys[target] = keys.pop(PATH)
    elif fault == 'nan-time':
        key['time'] = float('nan')
    elif fault == 'infinite-value':
        key['value'] = float('inf')
    elif fault == 'bool-value':
        key['value'] = False
    elif fault == 'negative':
        key['value'] = -.1
    elif fault == 'range':
        key['value'] = 1.1
    elif fault == 'easing':
        key['easing'] = 'bogus'
    elif fault == 'interpolation':
        key['interpolation'] = 'frames'
    else:
        call['args'].pop('keyframeOrigin')
    original = copy.deepcopy(before)
    with pytest.raises((commands.CommandError, ValueError)):
        RuntimeCommitService._apply(before, [call])
    assert before == original


def test_replacement_static_schema_and_structural_copy_refuse_without_losing_curves(initial):
    before, sid = initial
    authored, _, _ = accepted(before, [author(initial)])
    replacement = dict(id='shade', element='timeline.component/unknown.vignette', params=dict(strength=.5))
    with pytest.raises((commands.CommandError, ValueError)):
        RuntimeCommitService._apply(authored, [dict(op='clip.set-param', select=sid,
            args=dict(path='modifiers["shade"]', value=replacement))])
    assert clip(authored, sid).data['keyframes'] == KEYS
    with pytest.raises(commands.TimelineEditError, match='animation partition'):
        RuntimeCommitService._apply(authored, [dict(op='timeline.add', select=None, args={'from': sid, 'at': 0})])


def test_python_and_shared_host_use_the_same_quoted_instance_serializer():
    for mid in ['shade', 'quote"slash\\', 'é😀']:
        path = modifiers.parameter_address(mid, 'strength')
        assert modifiers.keyframe_address(path) == (mid, 'strength')


def test_modifier_curve_refuses_an_audio_target_atomically(initial):
    before, sid = initial
    clip(before, sid).data['track'] = 'A1'
    original = copy.deepcopy(before)
    with pytest.raises(commands.CommandError, match='visual clip subtree'):
        RuntimeCommitService._apply(before, [author(initial)])
    assert before == original


@pytest.mark.parametrize('mode', ['hold', 'named-easing', 'duplicate-time'])
def test_existing_complete_pair_retains_supported_authored_curve_semantics(initial, mode):
    keys = copy.deepcopy(KEYS)
    if mode == 'hold':
        keys[PATH][0]['interpolation'] = 'hold'
    elif mode == 'named-easing':
        keys[PATH][0]['easing'] = 'ease-in'
    else:
        keys[PATH].insert(1, dict(time=0, value=.9, interpolation='linear', opaque='second authored'))
    after, _, _ = RuntimeCommitService._apply(initial[0], [author(initial, keys)])
    assert clip(after, initial[1]).data['keyframes'] == keys
