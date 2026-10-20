"""Incoming transition writes from the App's raw three-products fixture."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from astrid.core.element import project_packs
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.core import test_project_packs
from tests.editing_conformance.test_recipe_clip_scalar_fields import CHILD, PARENT, app_bundle
from tests.editing_conformance.test_recipe_m1_commands import clip, inverse, later
from tests.editing_conformance.test_recipe_scalar_commands import schema_options

FIXTURES = Path(__file__).parent / 'fixtures'
configured_project_pack = pytest.fixture(test_project_packs.configured.__wrapped__)


def exact(left, right):
    assert json.dumps(left, sort_keys=True, ensure_ascii=False) == json.dumps(right, sort_keys=True, ensure_ascii=False)


def test_actual_app_fixture_portable_capture_undo_redo_clear_and_original_claims():
    original = app_bundle()
    transition = {'type': 'crossfade', 'duration': 0.75,
                  'params': {'future': {'literal': [None, False, 0, '', 'ƒ(x)']}},
                  'future': [None, 2.0]}
    command = capture_clip_set(original, PARENT, values={'transition': transition})
    plan = execute(original, [command])
    exact(clip(plan.bundle, PARENT), dict(clip(original, PARENT), transition=transition))
    assert plan.records[0]['writes'] == [{'ref': PARENT, 'path': ['transition'],
        'before': present(clip(original, PARENT)['transition']), 'after': present(transition)}]
    assert plan.commands == [command]
    assert command['selections'][0]['members'] == ['parent/clip:f2-app-clip']
    exact(inverse(plan.bundle, plan.records).bundle, original)
    undone = inverse(plan.bundle, plan.records)
    exact(inverse(undone.bundle, undone.records).bundle, plan.bundle)
    exact(replay(plan, original).records, plan.records)
    cleared = execute(plan.bundle, [capture_clip_set(plan.bundle, PARENT, clear=['transition'])])
    assert 'transition' not in clip(cleared.bundle, PARENT)
    exact(inverse(cleared.bundle, cleared.records).bundle, plan.bundle)
    compile_authoring_candidate(plan.bundle)
    fixture = json.loads((FIXTURES / 'recipe_m2_app_transition_set.json').read_text())
    exact(fixture, {'bundle': original, 'commands': plan.commands, 'records': plan.records,
                    'after_bundle': plan.bundle})
    exact(execute(fixture['bundle'], fixture['commands']).bundle, fixture['after_bundle'])
    damaged = copy.deepcopy(command)
    damaged['reads'].pop()
    with pytest.raises(CommandError, match='capture'):
        execute(original, [damaged])


@pytest.mark.parametrize('fps', [30, {'numerator': 30000, 'denominator': 1001}])
@pytest.mark.parametrize('start,duration,first', [(0, .5, True), (1, .5, False),
    (15, .5, False), (3, .5, False), (3, 20, False)])
def test_ratified_first_gap_overlap_and_oversized_windows(fps, start, duration, first):
    original = app_bundle()
    original['parent']['config']['output']['fps'] = fps
    clip(original, PARENT)['at'] = start
    if first:
        original['parent']['clips'].reverse()  # Stable ties use authored collection order.
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    plan = execute(original, [capture_clip_set(original, PARENT,
        values={'transition': {'type': 'crossfade', 'duration': duration}})])
    selection = plan.commands[0]['selections'][0]
    assert selection['members'] == ([] if first else ['parent/clip:f2-app-clip'])
    assert clip(plan.bundle, PARENT)['transition']['duration'] == duration
    exact(inverse(plan.bundle, plan.records).bundle, original)
    compile_authoring_candidate(plan.bundle)


@pytest.mark.parametrize('ref', [PARENT, CHILD])
def test_unknown_opaque_transitions_and_sibling_occurrence_isolation(ref):
    original = app_bundle()
    row = clip(original, ref)
    row['transition'] = {'type': 'future-plugin', 'duration': 1, 'params': {'opaque': [True, None, 2.0]},
                         'x_future': {'do-not-normalize': 'ƒ(x)'}}
    if ref == PARENT:
        original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    changed = dict(row['transition'], duration=25)
    plan = execute(original, [capture_clip_set(original, ref, values={'transition': changed})])
    exact(clip(plan.bundle, ref), dict(row, transition=changed))
    exact(State(plan.bundle).config('occurrence:shared-sibling'),
          State(original).config('occurrence:shared-sibling'))
    exact(inverse(plan.bundle, plan.records).bundle, original)
    exact(replay(plan, original).records, plan.records)


@pytest.mark.parametrize('damage', ['predecessor-duration', 'predecessor-source', 'target-source',
    'new-predecessor', 'move-predecessor-lane', 'owner', 'selection-order', 'fps'])
def test_relevant_guards_refuse_while_disjoint_lanes_replay(damage):
    original = app_bundle()
    plan = execute(original, [capture_clip_set(original, PARENT,
        values={'transition': {'type': 'crossfade', 'duration': 1}})])
    head = copy.deepcopy(original)
    if damage == 'predecessor-duration':
        clip(head, 'parent/clip:f2-app-clip')['to'] = 2
    elif damage == 'predecessor-source':
        head['parent']['registry']['assets']['f2-app']['media_id'] = 'other'
    elif damage == 'target-source':
        head['parent']['registry']['assets']['f2-video']['content_sha256'] = 'other'
    elif damage == 'new-predecessor':
        head['parent']['clips'].append({'id': 'new', 'track': 'V1', 'at': 12, 'hold': 1})
    elif damage == 'move-predecessor-lane':
        clip(head, 'parent/clip:f2-app-clip')['track'] = 'V3'
    elif damage == 'owner':
        head['parent']['clips'].remove(clip(head, PARENT))
    elif damage == 'selection-order':
        clip(head, 'parent/clip:f2-app-clip')['at'] = 20
    else:
        head['parent']['config']['output']['fps'] = 24
    head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    with pytest.raises(CommandError):
        replay(plan, head)
    disjoint = copy.deepcopy(original)
    disjoint['parent']['clips'].append({'id': 'other', 'track': 'other-lane', 'at': 14, 'hold': 1})
    disjoint['parent']['config']['clips'] = copy.deepcopy(disjoint['parent']['clips'])
    rebased = replay(plan, disjoint)
    assert rebased.commands == plan.commands
    exact(inverse(rebased.bundle, rebased.records).bundle, disjoint)


def test_inverse_refuses_aba_and_later_transition_edits_but_replay_keeps_original_body():
    original = app_bundle()
    plan = execute(original, [capture_clip_set(original, PARENT,
        values={'transition': {'type': 'crossfade', 'duration': 1}})])
    aba = [later(PARENT, ['transition'], {'type': 'crossfade', 'duration': 2}),
           later(PARENT, ['transition'], clip(plan.bundle, PARENT)['transition'])]
    with pytest.raises(CommandError) as error:
        inverse(plan.bundle, plan.records, aba)
    assert error.value.kind == 'intervening_write'
    later_plan = execute(plan.bundle, [capture_clip_set(plan.bundle, PARENT,
        values={'transition': {'type': 'crossfade', 'duration': 2}})])
    with pytest.raises(CommandError):
        inverse(later_plan.bundle, plan.records, later_plan.records)
    # Ordinary replay permits equal-state ABA; inverse history remains stricter.
    assert replay(plan, original, intervening_records=aba).commands == plan.commands


def test_inverse_refuses_same_lane_membership_aba_allows_other_lane():
    original = app_bundle()
    plan = execute(original, [capture_clip_set(original, PARENT,
        values={'transition': {'type': 'crossfade', 'duration': 1}})])
    for track in ('V1', 'other-lane'):
        change = later('parent/clip:new', [], {'id': 'new', 'track': track, 'at': 14, 'hold': 1})
        if track == 'V1':
            with pytest.raises(CommandError):
                inverse(plan.bundle, plan.records, [change])
        else:
            exact(inverse(plan.bundle, plan.records, [change]).bundle, original)


@pytest.mark.parametrize('values,clear', [({'transition': None}, []), ({'transition': ''}, []),
    ({'transition': {}}, []), ({'transition': {'type': 'crossfade', 'duration': 0}}, []),
    ({'transition': {'type': 'crossfade', 'duration': True}}, []),
    ({'transition': {'type': 'crossfade', 'duration': float('inf')}}, []),
    ({'transition': {'type': 'crossfade', 'duration': .5}}, ['transition']),
    ({'elementRef': {'id': 'crossfade', 'kind': 'transition', 'revision': 'r'}}, []),
    ({'transition': {'type': 'crossfade', 'duration': .5},
      'elementRef': {'id': 'different', 'kind': 'transition', 'revision': 'r'}}, []),
    ({'effects': {}}, [])])
def test_closed_transition_values_and_clear_are_distinct(values, clear):
    with pytest.raises(CommandError):
        capture_clip_set(app_bundle(), PARENT, values=values, clear=clear)


def admitted_transition(configured):
    root, directory, manifest = test_project_packs.seed('project-1')
    path = directory / 'element.yaml'
    definition = yaml.safe_load(path.read_text())
    definition['kind'] = 'transition'
    manifest['rendering']['transitions/reveal'] = manifest['rendering'].pop('effects/reveal')
    (root / 'pack.yaml').write_text(yaml.safe_dump(manifest))
    definition['schema']['properties']['seed']['maximum'] = 20
    path.write_text(yaml.safe_dump(definition))
    old = project_packs.admit_project_pack('realm', 'project-1')['elements'][0]['descriptor']
    definition['schema']['properties']['seed']['maximum'] = 10
    path.write_text(yaml.safe_dump(definition))
    new = project_packs.admit_project_pack('realm', 'project-1')['elements'][0]['descriptor']
    return [{k: descriptor[k] for k in ('packId', 'id', 'kind', 'revision')} for descriptor in (old, new)]


def test_selected_schema_max_uses_exact_immutable_transition_snapshot(configured_project_pack):
    old, new = admitted_transition(configured_project_pack)
    original = app_bundle()
    original['project_id'] = 'project-1'
    for selected, accepted in [(old, True), (new, False)]:
        options = schema_options(configured_project_pack, selected)
        inputs = {key: value for key, value in options.items() if key != 'schema_source'}
        values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': .5,
                  'revision': selected['revision'], 'params': {'seed': 16, 'future': [None, 2.0]}}}
        if accepted:
            command = capture_clip_set(original, PARENT, values=values, **options)
            plan = execute(original, [command], **inputs)
            assert clip(plan.bundle, PARENT)['elementRef'] == selected
            assert options['schema_source'] in [p['pin'] for p in plan.bundle['source_mapping']['pinned_documents']]
            assert any(d['key'] == 'params.snapshot' for d in plan.records[0]['dependencies'])
            assert replay(plan, original, **inputs).commands == plan.commands
            # Undo restores authored fields; retained immutable sources stay available.
            undone = inverse(plan.bundle, plan.records)
            exact(clip(undone.bundle, PARENT), clip(original, PARENT))
            exact(inverse(undone.bundle, undone.records).bundle, plan.bundle)
        else:
            with pytest.raises(CommandError, match='maximum'):
                capture_clip_set(original, PARENT, values=values, **options)
        with pytest.raises(CommandError, match='schema_source'):
            capture_clip_set(original, PARENT, values=values)
        bad = copy.deepcopy(options)
        bad['schema_inputs'][0][1].clear()
        with pytest.raises(CommandError):
            capture_clip_set(original, PARENT, values=values, **bad)


def test_builtin_known_params_are_validated_without_coercion(monkeypatch):
    from astrid.core.element import catalog

    monkeypatch.setattr(catalog, 'list_transition_ids', lambda: ['crossfade'])
    monkeypatch.setattr(catalog, 'read_transition_schema', lambda name: {
        'type': 'object', 'properties': {'strength': {'type': 'number', 'maximum': 1}}})
    with pytest.raises(CommandError):
        capture_clip_set(app_bundle(), PARENT, values={'transition': {
            'type': 'crossfade', 'duration': .5, 'params': {'strength': '1'}}})
    capture_clip_set(app_bundle(), PARENT, values={'transition': {
        'type': 'crossfade', 'duration': .5, 'params': {'strength': .5, 'opaque': False}}})


def test_actual_app_selected_builtin_uses_exact_shipped_catalog_reference():
    from astrid.core.element.catalog import list_element_descriptors

    descriptor = next(d for d in list_element_descriptors('transitions') if d['id'] == 'cross-fade')
    selected = {key: descriptor[key] for key in ('id', 'kind', 'revision', 'packId')}
    original = app_bundle()
    values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': 8 / 30,
              'revision': selected['revision'], 'params': {'durationFrames': 8, 'opaque': 'kept'}}}
    plan = execute(original, [capture_clip_set(original, PARENT, values=values)])
    exact(clip(plan.bundle, PARENT), dict(clip(original, PARENT), **values))
    exact(inverse(plan.bundle, plan.records).bundle, original)
    exact(replay(plan, original).records, plan.records)
    for key in ('revision', 'packId'):
        bad = copy.deepcopy(values)
        bad['elementRef'][key] = 'unavailable'
        with pytest.raises(CommandError):
            capture_clip_set(original, PARENT, values=bad)
    values['transition']['params']['durationFrames'] = 0
    with pytest.raises(CommandError):
        capture_clip_set(original, PARENT, values=values)
