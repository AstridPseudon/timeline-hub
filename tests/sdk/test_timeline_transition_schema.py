"""The existing clip.set carrier accepts only guarded incoming transitions."""
from __future__ import annotations

import copy

import pytest
import yaml

from astrid.core.element import project_packs
from astrid.core.element.catalog import list_element_descriptors
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest
from tests.core import test_project_packs
from tests.editing_conformance.test_recipe_clip_scalar_fields import (
    PARENT,
    adjacent_transition_bundle,
    clip,
)
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_recipe_scalar_commands import schema_options
from tests.sdk.test_timeline_clip_scalar_provider import app_document, current
from tests.sdk.test_timeline_commit_provider import DetachedRealm
from tests.sdk.test_timeline_selected_schema import configured_project_pack  # noqa: F401


def builtin_transition():
    descriptor = next(item for item in list_element_descriptors('transitions')
                      if item['id'] == 'cross-fade')
    return {key: descriptor[key] for key in ('id', 'kind', 'revision', 'packId')}


def transition_pack():
    root, directory, manifest = test_project_packs.seed('project-1')
    definition_path = directory / 'element.yaml'
    definition = yaml.safe_load(definition_path.read_text())
    definition.update(id='pack-cross-fade', kind='transition')
    definition['schema']['properties']['seed']['maximum'] = 10
    definition_path.write_text(yaml.safe_dump(definition))
    declaration = manifest['rendering'].pop('effects/reveal')
    declaration['path'] = declaration['path'].replace('effects/reveal', 'transitions/pack-cross-fade')
    for resource in declaration['resources']:
        resource['path'] = resource['path'].replace('effects/reveal', 'transitions/pack-cross-fade')
    manifest['rendering']['transitions/pack-cross-fade'] = declaration
    transition_dir = root / 'rendering/elements/transitions/pack-cross-fade'
    transition_dir.mkdir(parents=True)
    for path in directory.iterdir():
        path.rename(transition_dir / path.name)
    directory.rmdir()
    (root / 'pack.yaml').write_text(yaml.safe_dump(manifest))
    return transition_dir


def adjacent_app_document():
    document = app_document()
    rows = document['parent_revision']['payload']['clips']
    rows[1]['at'] = 3
    document['parent_revision']['payload']['config']['clips'] = copy.deepcopy(rows)
    document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
    return document


def provider_commit(realm, commands):
    context = realm.context(commands)
    context['realm_id'] = 'realm'
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    from tests.sdk.test_timeline_commit_provider import DetachedPort
    return create_runtime_commit_service().commit(context, DetachedPort(realm, context))


def test_builtin_transition_set_preserves_raw_params_and_explicit_pair_clear():
    element = builtin_transition()
    original = adjacent_transition_bundle()
    clip(original, PARENT)['element_ref'] = {
        'id': 'legacy', 'kind': 'transition', 'revision': 'old'}
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    values = {
        'elementRef': element,
        'transition': {
            'type': element['id'], 'duration': .75, 'revision': element['revision'],
            'params': {'opaque': [None, False, 0]}, 'future': {'literal': 'kept'},
        },
    }
    plan = execute(original, [capture_clip_set(original, PARENT, values=values)])
    assert clip(plan.bundle, PARENT)['transition'] == values['transition']
    assert clip(plan.bundle, PARENT)['elementRef'] == element
    assert 'element_ref' not in clip(plan.bundle, PARENT)
    assert inverse(plan.bundle, plan.records).bundle == original

    removed = execute(plan.bundle, [capture_clip_set(
        plan.bundle, PARENT, clear=['transition', 'elementRef'])])
    assert all(key not in clip(removed.bundle, PARENT)
               for key in ('transition', 'elementRef', 'element_ref'))
    assert inverse(removed.bundle, removed.records).bundle == plan.bundle


@pytest.mark.parametrize('params', [None, {'keep': [None, False]}])
def test_transition_set_preserves_parameter_presence_and_rejects_destructive_null(params):
    original = adjacent_transition_bundle()
    target = clip(original, PARENT)
    target['transition'] = {
        'type': 'cross-fade', 'duration': .5, 'revision': 'r1', 'future': {'keep': True},
    }
    if params is not None:
        target['transition']['params'] = copy.deepcopy(params)
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    values = {'transition': {'type': 'cross-fade', 'duration': .75, 'revision': 'r1'}}
    plan = execute(original, [capture_clip_set(original, PARENT, values=values)])
    expected = copy.deepcopy(target['transition'])
    expected['duration'] = .75
    if params is not None:
        expected['params'] = params
    assert clip(plan.bundle, PARENT)['transition'] == expected

    if params:
        with pytest.raises(CommandError, match='remove existing parameters'):
            capture_clip_set(plan.bundle, PARENT, values={
                'transition': {
                    'type': 'cross-fade', 'duration': .75, 'revision': 'r1', 'params': None,
                },
            })


@pytest.mark.parametrize('field', ['elementRef', 'element_ref'])
def test_transition_only_clear_preserves_unrelated_reference(field):
    original = adjacent_transition_bundle()
    selected = {'id': 'rocket', 'kind': 'effect', 'revision': 'r1'}
    clip(original, PARENT)['transition'] = {'type': 'cross-fade', 'duration': .5}
    clip(original, PARENT)[field] = copy.deepcopy(selected)
    plan = execute(original, [capture_clip_set(original, PARENT, clear=['transition'])])
    assert clip(plan.bundle, PARENT)[field] == selected
    assert 'transition' not in clip(plan.bundle, PARENT)


@pytest.mark.parametrize('change', ['gap', 'track', 'oversize'])
def test_transition_set_enforces_adjacency_and_shortest_fit(change):
    element = builtin_transition()
    original = adjacent_transition_bundle()
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


@pytest.mark.parametrize('field', ['elementRef', 'element_ref'])
def test_no_ref_transition_update_requires_both_reference_keys_absent(field):
    original = adjacent_transition_bundle()
    target = clip(original, PARENT)
    target['transition'] = {'type': 'cross-fade', 'duration': .5, 'revision': 'r1'}
    target[field] = None
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    with pytest.raises(CommandError, match='existing raw identity'):
        capture_clip_set(original, PARENT, values={
            'transition': {'type': 'cross-fade', 'duration': .75, 'revision': 'r1'},
        })


def test_no_ref_transition_update_requires_exact_revision_presence():
    original = adjacent_transition_bundle()
    target = clip(original, PARENT)
    target['transition'] = {'type': 'cross-fade', 'duration': .5, 'revision': 'r1'}
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    with pytest.raises(CommandError, match='existing raw identity'):
        capture_clip_set(original, PARENT, values={
            'transition': {'type': 'cross-fade', 'duration': .75},
        })


def test_selected_transition_retains_first_p1_authority(configured_project_pack):  # noqa: F811
    from runtime_protocol.timeline_commit import CommitRejected as RuntimeCommitRejected

    transition_dir = transition_pack()
    first_result = project_packs.admit_project_pack('realm', 'project-1')
    first_descriptor = next(item['descriptor'] for item in first_result['elements']
                            if item['descriptor']['kind'] == 'transition')
    definition_path = transition_dir / 'element.yaml'
    definition = yaml.safe_load(definition_path.read_text())
    definition['schema']['properties']['seed']['maximum'] = 20
    definition_path.write_text(yaml.safe_dump(definition))
    second_result = project_packs.admit_project_pack('realm', 'project-1')
    second_descriptor = next(item['descriptor'] for item in second_result['elements']
                             if item['descriptor']['kind'] == 'transition')
    first = {key: first_descriptor[key] for key in ('id', 'kind', 'revision', 'packId')}
    second = {key: second_descriptor[key] for key in ('id', 'kind', 'revision', 'packId')}
    p1 = schema_options(configured_project_pack, first)
    p2 = schema_options(configured_project_pack, second)
    realm = DetachedRealm(adjacent_app_document())
    for options in (p1, p2):
        verified, objects = options['schema_inputs'][0]
        realm.live_sources[_digest(verified['pin'])] = verified
        realm.snapshot_objects.update(objects)

    def values(element, seed):
        return {'elementRef': element, 'transition': {
            'type': element['id'], 'duration': .5, 'revision': element['revision'],
            'params': {'seed': seed}}}

    provider_commit(realm, [capture_clip_set(current(realm), PARENT,
                                             values=values(first, 8), **p1)])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    later = capture_clip_set(current(realm), PARENT, values=values(second, 16), **p2)
    with pytest.raises(RuntimeCommitRejected, match='source changed|authority|selected'):
        provider_commit(realm, [later])
    assert (realm.head, realm.entries, realm.documents) == before
