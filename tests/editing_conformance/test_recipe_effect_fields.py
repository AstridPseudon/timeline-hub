"""Actual named inspector slots and canonical fades; custom instances stay open."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_clip_scalar_fields import CHILD, PARENT, app_bundle
from tests.editing_conformance.test_recipe_m1_commands import clip, inverse, later

GOLDEN = Path(__file__).parent / 'fixtures/recipe_m2_app_effect_fields.json'


def inspector_requests():
    # Literal onChange shapes in ClipEntrance/Exit/ContinuousEffectField and
    # element-adapter.ts timeline.set_clip_fade. undefined becomes explicit clear.
    return [
        {'values': {'entrance': {'type': 'fade', 'duration': 0.4},
                    'effects': {'fade_in': 0.4, 'fade_out': 0.8},
                    'exit': {'type': 'fade-out', 'duration': 0.8}}},
        {'values': {'continuous': {'type': 'drift', 'intensity': 0.5}}},
        {'values': {'entrance': {'type': 'fade', 'duration': 0.6}}},
        {'clear': ['entrance', 'continuous']},
    ]


def inspector_plan():
    original = app_bundle()
    commands, current = [], original
    for request in inspector_requests():
        command = capture_clip_set(current, CHILD, **request)
        commands.append(command)
        current = execute(current, [command]).bundle
    return original, execute(original, commands)


def test_actual_inspector_shapes_capture_golden_order_roundtrip_and_compile():
    original, plan = inspector_plan()
    fixture = json.loads(GOLDEN.read_text())
    assert fixture == {'bundle': original, 'requests': inspector_requests(),
                       'commands': plan.commands, 'records': plan.records, 'after_bundle': plan.bundle}
    assert execute(fixture['bundle'], fixture['commands']).records == plan.records
    assert clip(plan.bundle, CHILD)['effects'] == {'fade_in': 0.4, 'fade_out': 0.8}
    assert clip(plan.bundle, CHILD)['exit'] == {'type': 'fade-out', 'duration': 0.8}
    assert 'entrance' not in clip(plan.bundle, CHILD)
    assert 'continuous' not in clip(plan.bundle, CHILD)
    assert State(plan.bundle).config('occurrence:shared-sibling') == State(original).config('occurrence:shared-sibling')
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    assert replay(plan, original).records == plan.records
    compile_authoring_candidate(plan.bundle)


@pytest.mark.parametrize('ref', [PARENT, CHILD])
@pytest.mark.parametrize('slot', ['entrance', 'exit', 'continuous', 'effects'])
@pytest.mark.parametrize('before', [ABSENT, present(None), present({}),
    present({'type': 'custom:resource-id', 'params': {'old': None}, 'opaque': [None, False]}),
    present([{'fade_in': 0.4}, {'fade_in': 0.4}, {'fade_out': 0.8}])])
def test_whole_field_clear_exact_null_absent_opaque_and_ordered_duplicates(ref, slot, before):
    original = app_bundle()
    State(original).set(ref, [slot], before)
    if ref == PARENT:
        original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    snapshot = copy.deepcopy(original)
    plan = execute(original, [capture_clip_set(original, ref, clear=[slot])])
    assert original == snapshot
    assert slot not in clip(plan.bundle, ref)
    assert plan.records[0]['writes'] == [{'ref': ref, 'path': [slot], 'before': before, 'after': ABSENT}]
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle


@pytest.mark.parametrize('before', [ABSENT, present(None), present({})])
def test_map_creation_and_slot_creation_restore_exact_container_presence(before):
    original = app_bundle()
    State(original).set(CHILD, ['effects'], before)
    State(original).set(CHILD, ['continuous'], before)
    command = capture_clip_set(original, CHILD, values={
        'effects': {'fade_in': 0}, 'continuous': {'type': 'drift', 'intensity': 0}})
    plan = execute(original, [command])
    assert clip(plan.bundle, CHILD)['effects'] == {'fade_in': 0}
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle


def test_same_slot_leaf_writes_preserve_opaque_params_and_disjoint_property_changes():
    original = app_bundle()
    row = clip(original, CHILD)
    row['continuous'] = {'type': 'custom:literal-id', 'intensity': 0.5,
                         'params': {'seed': None, 'opaque': [None, False]}, 'member': {'keep': None}}
    row['effects'] = {'fade_in': 0.2, 'fade_out': 0.8, 'old': None}
    plan = execute(original, [capture_clip_set(original, CHILD, values={
        'continuous': {'type': 'custom:literal-id', 'intensity': 0.7}, 'effects': {'fade_in': 0.3}})])
    assert clip(plan.bundle, CHILD)['continuous'] == dict(row['continuous'], intensity=0.7)
    assert clip(plan.bundle, CHILD)['effects'] == dict(row['effects'], fade_in=0.3)
    assert [w['path'] for w in plan.records[0]['writes']] == [
        ['continuous', 'intensity'], ['effects', 'fade_in']]
    other = execute(original, [capture_clip_set(original, CHILD, values={'hold': 4})])
    head = copy.deepcopy(other.bundle)
    clip(head, CHILD)['effects']['fade_out'] = 0.9
    rebased = replay(plan, head, intervening_records=other.records)
    assert inverse(rebased.bundle, rebased.records).bundle == head
    assert replay(plan, original).commands == plan.commands


def test_unchanged_param_echo_is_guarded_at_literal_leaves_without_schema_fallback():
    original = app_bundle()
    row = {'type': 'custom:resource-id', 'intensity': 0.5,
           'params': {'unknown': {'keep': [None, 0]}, 'null': None}}
    clip(original, CHILD)['continuous'] = row
    plan = execute(original, [capture_clip_set(original, CHILD, values={'continuous': row})])
    assert plan.bundle == original
    assert [w['path'] for w in plan.records[0]['writes']] == [
        ['continuous', 'intensity'], ['continuous', 'params', 'null'], ['continuous', 'params', 'unknown']]
    assert inverse(plan.bundle, plan.records).bundle == original


def test_same_effect_disjoint_duration_and_intensity_rebase_and_inverse():
    original = app_bundle()
    clip(original, CHILD)['entrance'] = {'type': 'fade', 'duration': 0.4, 'intensity': 0.5}
    duration = execute(original, [capture_clip_set(original, CHILD, values={
        'entrance': {'type': 'fade', 'duration': 0.6}})])
    intensity = execute(original, [capture_clip_set(original, CHILD, values={
        'entrance': {'type': 'fade', 'intensity': 0.9}})])
    rebased = replay(duration, intensity.bundle, intervening_records=intensity.records)
    assert clip(rebased.bundle, CHILD)['entrance'] == {'type': 'fade', 'duration': 0.6, 'intensity': 0.9}
    assert inverse(rebased.bundle, rebased.records).bundle == intensity.bundle


def test_selecting_new_effect_type_matches_inspector_slot_replacement_and_restores_old_params():
    original = app_bundle()
    before = {'type': 'custom:old-resource', 'duration': 0.7,
              'params': {'opaque': [None, False]}, 'opaque_member': None}
    clip(original, CHILD)['entrance'] = copy.deepcopy(before)
    replacement = {'type': 'fade', 'duration': 0.4}
    plan = execute(original, [capture_clip_set(original, CHILD, values={'entrance': replacement})])
    assert clip(plan.bundle, CHILD)['entrance'] == replacement
    assert plan.records[0]['writes'] == [{
        'ref': CHILD, 'path': ['entrance'], 'before': present(before), 'after': present(replacement)}]
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle


@pytest.mark.parametrize('params', [ABSENT, present(None), present({'opaque': [None, False]})])
def test_duration_edit_preserves_opaque_param_container_presence(params):
    original = app_bundle()
    clip(original, CHILD)['entrance'] = {'type': 'fade', 'duration': 0.4}
    State(original).set(CHILD, ['entrance', 'params'], params)
    plan = execute(original, [capture_clip_set(original, CHILD, values={
        'entrance': {'type': 'fade', 'duration': 0.6}})])
    assert State(plan.bundle).get(CHILD, ['entrance', 'params']) == params
    assert inverse(plan.bundle, plan.records).bundle == original


def test_ordered_legacy_and_opaque_instances_survive_unrelated_named_slot_edit():
    original = app_bundle()
    rows = [{'fade_in': 0.4}, {'fade_in': 0.4},
            {'type': 'unowned-opaque', 'params': {'keep': [None, False]}}, None]
    clip(original, CHILD)['effects'] = copy.deepcopy(rows)
    command = capture_clip_set(original, CHILD, values={'entrance': {'type': 'fade', 'duration': 0.4}})
    plan = execute(original, [command])
    assert clip(plan.bundle, CHILD)['effects'] == rows
    assert all(write['path'][0] != 'effects' for write in plan.records[0]['writes'])
    assert inverse(plan.bundle, plan.records).bundle == original


def test_missing_custom_descriptor_refuses_atomically_even_after_other_requested_writes():
    original = app_bundle()
    clip(original, CHILD)['continuous'] = {'type': 'custom:resource-id', 'params': {'seed': 1}}
    before = copy.deepcopy(original)
    with pytest.raises(CommandError) as error:
        capture_clip_set(original, CHILD, values={
            'hold': 4, 'continuous': {'type': 'custom:resource-id', 'params': {'seed': 16}}})
    assert error.value.kind == 'unsupported_effect_schema'
    assert original == before


@pytest.mark.parametrize('change', ['type', 'owner', 'source', 'field', 'missing'])
def test_slot_and_owner_identity_guards_refuse_atomically(change):
    original = app_bundle()
    clip(original, CHILD)['entrance'] = {'type': 'fade', 'duration': 0.4}
    command = capture_clip_set(original, CHILD, values={'entrance': {'type': 'fade', 'duration': 0.6}})
    head = copy.deepcopy(original)
    if change == 'owner':
        source = head['placements'][0]['shot_id']
        head['shots']['other-shot'] = copy.deepcopy(head['shots'][source])
        head['shots']['other-shot']['shot_id'] = 'other-shot'
        head['source_mapping']['shots']['other-shot'] = dict(
            head['source_mapping']['shots'][source], shot_id='other-shot')
        head['placements'][0]['shot_id'] = 'other-shot'
    elif change == 'source':
        shot = head['placements'][0]['shot_id']
        head['source_mapping']['shots'][shot]['shot_id'] = 'different'
    elif change == 'missing':
        State(head).config('occurrence:f2-occurrence')['clips'].remove(clip(head, CHILD))
    else:
        clip(head, CHILD)['entrance']['type' if change == 'type' else 'duration'] = 'other' if change == 'type' else 0.8
    snapshot = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, [command])
    assert head == snapshot


@pytest.mark.parametrize('path,values', [(['entrance', 'duration'], {'entrance': {'type': 'fade', 'duration': 0.4}}),
    (['effects', 'fade_in'], {'effects': {'fade_in': 0.4}})])
def test_unchanged_and_aba_history_guard_inverse_but_equal_state_rebases(path, values):
    original = app_bundle()
    clip(original, CHILD).update(entrance={'type': 'fade', 'duration': 0.4}, effects={'fade_in': 0.4})
    plan = execute(original, [capture_clip_set(original, CHILD, values=values)])
    assert plan.bundle == original
    for history in ([later(CHILD, path, 0.4)], [later(CHILD, path, 0.9), later(CHILD, path, 0.4)]):
        with pytest.raises(CommandError, match='intervening'):
            inverse(plan.bundle, plan.records, history)
        assert replay(plan, original, intervening_records=history).commands == plan.commands


@pytest.mark.parametrize('values', [{'continuous': {'type': 'x', 'duration': 1}},
    {'entrance': {'type': 'x', 'id': 'guessed'}}, {'effects': [{'fade_in': 1}]},
    {'effects': {'unknown': 1}}, {'effects': {}}, {'entrance': {'duration': 1}},
    {'entrance': None}, {'continuous': {'type': 'x', 'intensity': True}}])
def test_closed_values_refuse_unsupported_shapes(values):
    with pytest.raises(CommandError):
        capture_clip_set(app_bundle(), CHILD, values=values)


def test_raw_canonical_schema_proves_named_slots_and_legacy_array_without_ids():
    path = Path(__file__).parents[2] / 'astrid/core/timeline/schema/timeline-config.schema.json'
    schema = json.loads(path.read_text())
    validator = Draft7Validator({'$ref': '#/definitions/TimelineClip', 'definitions': schema['definitions']})
    row = {'id': 'raw', 'at': 0, 'track': 'V1', 'clipType': 'media', 'hold': 1}
    assert not list(validator.iter_errors(dict(row, effects=[{'fade_in': 0.4}, {'fade_in': 0.4}])))
    assert list(validator.iter_errors(dict(row, effects=[{'id': 'fx', 'type': 'blur', 'params': {}}])))
    assert not list(validator.iter_errors(dict(row, entrance={'type': 'fade', 'duration': 0.4})))


# Requirement: bind named-slot params to exact immutable descriptor identity
# through the existing resolver before retiring their positive App behavior.
@pytest.mark.xfail(strict=True, reason='M2 named-slot exact descriptor binding remains open')
def test_existing_custom_inspector_param_edit_positive_requirement():
    original = app_bundle()
    clip(original, CHILD)['continuous'] = {'type': 'custom:resource-id', 'params': {'seed': 1}}
    command = capture_clip_set(original, CHILD, values={
        'continuous': {'type': 'custom:resource-id', 'params': {'seed': 16}}})
    assert clip(execute(original, [command]).bundle, CHILD)['continuous']['params'] == {'seed': 16}


# Requirement: exact descriptor-bound param reset/clear must restore the
# inspector's existing behavior before its snapshot writer can be deleted.
@pytest.mark.xfail(strict=True, reason='M2 named-slot parameter reset/clear remains open')
def test_existing_custom_inspector_param_clear_positive_requirement():
    original = app_bundle()
    clip(original, CHILD)['continuous'] = {'type': 'custom:resource-id', 'params': {'seed': 1}}
    command = capture_clip_set(original, CHILD, values={
        'continuous': {'type': 'custom:resource-id', 'params': {}}})
    assert clip(execute(original, [command]).bundle, CHILD)['continuous']['params'] == {}


# Requirement: establish the actual ordered-instance producer and its declared
# identity/migration contract; never select legacy duplicate fades by position.
@pytest.mark.xfail(strict=True, reason='M2 ordered custom-instance identity contract remains open')
def test_ordered_custom_instance_add_positive_requirement():
    original = app_bundle()
    rows = [{'id': 'fx-1', 'type': 'blur', 'params': {'radius': 2}},
            {'id': 'fx-2', 'type': 'blur', 'params': {'radius': 2}}]
    command = capture_clip_set(original, CHILD, values={'effects': rows})
    assert clip(execute(original, [command]).bundle, CHILD)['effects'] == rows
