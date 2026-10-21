"""The ordinary clip.set carrier preserves guarded incoming transitions."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from astrid.core.element.catalog import list_element_descriptors
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_clip_scalar_fields import PARENT, app_bundle, clip


def adjacent_bundle():
    original = app_bundle()
    rows = original['parent']['clips']
    rows[1]['at'] = 3
    original['parent']['config']['clips'] = copy.deepcopy(rows)
    return original


def selected_transition():
    descriptor = next(item for item in list_element_descriptors('transitions')
                      if item['id'] == 'cross-fade')
    return {key: descriptor[key] for key in ('id', 'kind', 'revision', 'packId')}


def test_transition_set_preserves_raw_values_and_paired_clear_inverse():
    original = adjacent_bundle()
    target = clip(original, PARENT)
    target['element_ref'] = {'id': 'legacy', 'kind': 'transition', 'revision': 'old'}
    original['parent']['clips'] = copy.deepcopy(original['parent']['config']['clips'])
    element = selected_transition()
    transition = {'type': element['id'], 'duration': .75, 'revision': element['revision'],
                  'params': {'opaque': [None, False, 0]}, 'future': {'literal': 'kept'}}

    plan = execute(original, [capture_clip_set(original, PARENT,
                                               values={'elementRef': element,
                                                       'transition': transition})])
    assert clip(plan.bundle, PARENT)['transition'] == transition
    assert clip(plan.bundle, PARENT)['elementRef'] == element
    assert 'element_ref' not in clip(plan.bundle, PARENT)
    assert execute(plan.bundle, [capture_clip_set(plan.bundle, PARENT,
                                                  values={'elementRef': element,
                                                          'transition': dict(transition,
                                                                             duration=1.25,
                                                                             params={'opaque': [None, False, 0],
                                                                                     'new': ''})})]).bundle[
        'parent']['clips'][1]['transition']['future'] == {'literal': 'kept'}

    changed = execute(plan.bundle, [capture_clip_set(plan.bundle, PARENT,
                                                     clear=['transition', 'elementRef'])])
    assert all(key not in clip(changed.bundle, PARENT)
               for key in ('transition', 'elementRef', 'element_ref'))


@pytest.mark.parametrize('field', ['elementRef', 'element_ref'])
def test_transition_only_clear_preserves_unrelated_reference(field):
    original = adjacent_bundle()
    selected = {'id': 'rocket', 'kind': 'effect', 'revision': 'r1'}
    clip(original, PARENT).update(transition={'type': 'cross-fade', 'duration': .5}, **{field: selected})
    plan = execute(original, [capture_clip_set(original, PARENT, clear=['transition'])])
    assert clip(plan.bundle, PARENT)[field] == selected
    assert 'transition' not in clip(plan.bundle, PARENT)


@pytest.mark.parametrize('change', ['gap', 'track', 'oversize'])
def test_transition_set_enforces_main_adjacency_and_shortest_fit(change):
    original = adjacent_bundle()
    element = selected_transition()
    target = clip(original, PARENT)
    if change == 'gap':
        target['at'] = 3.002
    elif change == 'track':
        target['track'] = 'S1'
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    duration = 3.1 if change == 'oversize' else .5
    with pytest.raises(CommandError, match='adjacent|shorter'):
        capture_clip_set(original, PARENT, values={
            'elementRef': element,
            'transition': {'type': element['id'], 'duration': duration,
                           'revision': element['revision']},
        })


@pytest.mark.parametrize('params', [None, {}, {'known': 1}])
def test_transition_params_presence_and_destructive_null_refusal(params):
    original = adjacent_bundle()
    element = selected_transition()
    initial = {'type': element['id'], 'duration': .5, 'revision': element['revision'],
               'params': params}
    first = execute(original, [capture_clip_set(original, PARENT,
                                                values={'elementRef': element,
                                                        'transition': initial})])
    update = {'elementRef': element,
              'transition': {'type': element['id'], 'duration': .75,
                             'revision': element['revision'], 'params': None}}
    if params:
        with pytest.raises(CommandError, match='remove existing parameters'):
            capture_clip_set(first.bundle, PARENT, values=update)
    else:
        changed = execute(first.bundle, [capture_clip_set(first.bundle, PARENT, values=update)])
        assert changed.bundle['parent']['clips'][1]['transition']['params'] is None


@pytest.mark.parametrize('params', [ABSENT, present(None), present({'opaque': [None, False]})])
def test_unreferenced_transition_update_preserves_params_presence(params):
    original = adjacent_bundle()
    target = clip(original, PARENT)
    target['transition'] = {'type': 'cross-fade', 'duration': .5, 'revision': 'r1',
                            'future': {'keep': True}}
    State(original).set(PARENT, ['transition', 'params'], params)
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    command = capture_clip_set(original, PARENT, values={
        'transition': {'type': 'cross-fade', 'duration': .75, 'revision': 'r1'}})
    changed = execute(original, [command])
    result = clip(changed.bundle, PARENT)['transition']
    expected = {'type': 'cross-fade', 'duration': .75, 'revision': 'r1',
                'future': {'keep': True}}
    if params['state'] == 'present':
        expected['params'] = copy.deepcopy(params['value'])
    assert result == expected


@pytest.mark.parametrize('field', ['elementRef', 'element_ref'])
def test_unreferenced_transition_update_refuses_present_reference(field):
    original = adjacent_bundle()
    target = clip(original, PARENT)
    target['transition'] = {'type': 'cross-fade', 'duration': .5, 'revision': 'r1'}
    target[field] = None
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    with pytest.raises(CommandError, match='existing raw identity'):
        capture_clip_set(original, PARENT, values={
            'transition': {'type': 'cross-fade', 'duration': .75, 'revision': 'r1'}})


@pytest.mark.parametrize('value', [
    {'id': 'rocket', 'kind': 'effect', 'revision': 'r1'},
    {'id': 'cross-fade', 'kind': 'transition', 'revision': 'wrong'},
    'opaque legacy reference',
])
def test_paired_transition_clear_refuses_mismatched_identity(value):
    original = adjacent_bundle()
    target = clip(original, PARENT)
    target['transition'] = {'type': 'cross-fade', 'duration': .5, 'revision': 'r1'}
    target['element_ref'] = copy.deepcopy(value)
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    with pytest.raises(CommandError):
        capture_clip_set(original, PARENT, clear=['transition', 'elementRef'])


def test_ordinary_schema_floor_is_exact_after_stripping_transition_additions():
    path = 'astrid/core/timeline/schema/edit-command.schema.json'
    schema = json.loads(open(path).read())
    args = schema['$defs']['ClipSetArgs']
    args['properties']['values']['properties'].pop('transition')
    args['properties']['values']['properties'].pop('elementRef')
    args['properties']['clear']['items']['enum'].remove('elementRef')
    args['properties'].pop('schema_source')
    args['description'] = ('Bounded raw clip fields. Set hold in source seconds; explicitly remove '
                           'hold, asset or incoming transition. Clear removes presence, never sets '
                           'null/empty. Asset assignment requires the scoped clip.swap-media or '
                           'occurrence.swap-media; transition authoring is outside v1.')
    assert len(schema['$defs']) == 55
    assert len(schema['$defs']['EditCommand']['allOf']) == 29
    assert hashlib.sha256((json.dumps(schema, indent=2) + '\n').encode()).hexdigest() == (
        '6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d')
