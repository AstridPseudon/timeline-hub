"""The ordinary provider resolves and retains the exact transition declaration."""
from __future__ import annotations

import copy

import pytest
import yaml

from astrid.core.element import project_packs
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.commit import _digest
from tests.core import test_project_packs
from tests.editing_conformance.test_recipe_clip_scalar_fields import PARENT
from tests.editing_conformance.test_recipe_scalar_commands import schema_options
from tests.sdk.test_timeline_clip_scalar_provider import app_document, current
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedRealm, inverse
from tests.sdk.test_timeline_selected_schema import (  # noqa: F401
    commit,
    configured_project_pack,
    runtime_abi,
)


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


def admitted_transition(configured):
    transition_pack()
    result = project_packs.admit_project_pack('realm', 'project-1')
    selected = next(item['descriptor'] for item in result['elements']
                    if item['descriptor']['kind'] == 'transition')
    return result, {key: selected[key] for key in ('id', 'kind', 'revision', 'packId')}


def adjacent_app_document():
    document = app_document()
    rows = document['parent_revision']['payload']['clips']
    rows[1]['at'] = 3
    document['parent_revision']['payload']['config']['clips'] = copy.deepcopy(rows)
    document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
    return document


def test_provider_selected_transition_validates_exact_schema_and_redoes(configured_project_pack):  # noqa: F811
    _, selected = admitted_transition(configured_project_pack)
    realm = DetachedRealm(adjacent_app_document())
    options = schema_options(configured_project_pack, selected)
    verified, realm.snapshot_objects = options['schema_inputs'][0]
    realm.live_sources[_digest(verified['pin'])] = verified
    values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': .5,
              'revision': selected['revision'], 'params': {'seed': 8}}}
    accepted = commit(realm, [capture_clip_set(current(realm), PARENT, values=values, **options)])
    document = accepted['data']['canonical_document']
    assert document['dependency_manifest']['documents'] == [options['schema_source']]
    invalid = copy.deepcopy(values)
    invalid['transition']['params']['seed'] = 16
    raw = {'schema_version': 1, 'op': 'clip.set', 'version': '1', 'select': PARENT,
           'args': {'values': invalid, 'clear': [], 'schema_source': options['schema_source']}}
    snapshot = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected):
        commit(realm, [raw])
    assert snapshot == (realm.head, realm.entries, realm.documents)
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document']['dependency_manifest']['documents'] == []
    redone = commit(realm, [inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == document


def test_first_selected_transition_exact_document_inverse(configured_project_pack):  # noqa: F811
    _, selected = admitted_transition(configured_project_pack)
    realm = DetachedRealm(adjacent_app_document())
    options = schema_options(configured_project_pack, selected)
    verified, realm.snapshot_objects = options['schema_inputs'][0]
    realm.live_sources[_digest(verified['pin'])] = verified
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': .5,
              'revision': selected['revision'], 'params': {'seed': 8}}}
    accepted = commit(realm, [capture_clip_set(current(realm), PARENT, values=values, **options)])
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == before


def test_selected_transition_update_retains_first_pin_for_same_reference(configured_project_pack):  # noqa: F811
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

    first_command = capture_clip_set(current(realm), PARENT, values=values(first, 8), **p1)
    commit(realm, [first_command])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    later = capture_clip_set(current(realm), PARENT, values=values(second, 16), **p2)
    with pytest.raises(CommitRejected, match='source changed|authority|selected'):
        commit(realm, [later])
    assert (realm.head, realm.entries, realm.documents) == before
