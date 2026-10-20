"""The private owner-pinned overlay successor uses only retained source authority."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params, capture_track_set
from astrid.sdk.timeline.capture import capture_clip_delete
from astrid.sdk.timeline.commit import _digest, create_runtime_commit_service
from tests.editing_conformance import test_recipe_scalar_commands as scalar_recipes
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedPort,
    DetachedRealm,
    inverse,
    track_create,
)
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi
from tests.sdk.test_timeline_commit_provider_scalar import current

admitted_param_revisions = scalar_recipes.admitted_param_revisions
configured_project_pack = scalar_recipes.configured_project_pack


def commit(realm, calls, *, base=None):
    context = realm.context(calls, base=base)
    context['realm_id'] = 'realm'
    return create_runtime_commit_service().commit(context, DetachedPort(realm, context))


def source_options(realm, options):
    verified, objects = copy.deepcopy(options['schema_inputs'][0])
    realm.live_sources[_digest(verified['pin'])] = verified
    realm.snapshot_objects.update(objects)


def overlay_row(element, **changes):
    return {
        'id': 'overlay', 'clipType': element['id'], 'elementRef': copy.deepcopy(element),
        'track': 'picture', 'at': 0, 'hold': 2,
        'params': {'seed': 4, 'opaque': {'literal': [None, False]}, 'nullable': None},
        'opaque': {'keep': [None, False, 0]},
        **changes,
    }


@pytest.fixture
def admitted_overlay(admitted_param_revisions, configured_project_pack):
    _, element = admitted_param_revisions
    options = scalar_recipes.schema_options(configured_project_pack, element)
    realm = DetachedRealm(empty_document())
    source_options(realm, options)
    commit(realm, [track_create('picture')])
    row = overlay_row(element)
    add = capture_clip_add(
        current(realm), 'parent', row,
        schema_source=options['schema_source'], schema_inputs=options['schema_inputs'], realm_id='realm')
    accepted = commit(realm, [add])
    return realm, element, options, row, accepted


def test_owner_pinned_add_records_exact_source_and_preserves_opaque_row(admitted_overlay):
    realm, element, options, row, accepted = admitted_overlay
    actual = State(current(realm)).entity('parent/clip:overlay')
    assert actual == row
    record = realm.entries[-1]['records']['commands'][0]
    assert record['command']['args']['schema_source'] == options['schema_source']
    assert record['dependencies'] == [
        {'key': 'params.schema', 'kind': 'source', 'pin': options['schema_source'], 'policy': 'exact'},
        {'key': 'params.snapshot', 'kind': 'entity', 'pin': {
            'source': options['schema_source'], 'element': element,
            'object': record['dependencies'][1]['pin']['object']}, 'policy': 'exact'},
    ]
    assert next(binding for binding in record['bindings'] if binding['key'] == 'params.element') == {
        'key': 'params.element', 'ref': 'parent/clip:overlay', 'policy': 'fixed',
        'dependencies': ['params.schema', 'params.snapshot'],
    }
    assert accepted['data']['canonical_document']['dependency_manifest']['documents'] == [
        options['schema_source']]
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    assert State(current(realm)).entity('parent/clip:overlay', optional=True) is None
    redone = commit(realm, [inverse([undone['receipt']['receipt_id']])])
    assert State(current(realm)).entity('parent/clip:overlay') == row
    assert redone['data']['canonical_document']['dependency_manifest']['documents'] == [
        options['schema_source']]


def test_owner_pinned_set_clear_delete_and_inverse_keep_original_authority(admitted_overlay):
    realm, element, options, row, accepted = admitted_overlay
    changed = capture_clip_set_params(
        current(realm), 'parent/clip:overlay', values={'seed': 8, 'new': None},
        clear=['opaque'], **options)
    changed_result = commit(realm, [changed])
    changed_row = State(current(realm)).entity('parent/clip:overlay')
    assert changed_row == {
        **row, 'params': {'seed': 8, 'new': None, 'nullable': None},
    }
    assert changed_result['data']['commands'] == [changed]

    deleted = commit(realm, [capture_clip_delete(current(realm), 'parent/clip:overlay')])
    assert State(current(realm)).entity('parent/clip:overlay', optional=True) is None
    restored = commit(realm, [inverse([deleted['receipt']['receipt_id']])])
    assert State(current(realm)).entity('parent/clip:overlay') == changed_row
    assert restored['data']['canonical_document']['dependency_manifest']['documents'] == [
        options['schema_source']]
    removed_again = commit(realm, [inverse([restored['receipt']['receipt_id']])])
    assert State(current(realm)).entity('parent/clip:overlay', optional=True) is None
    assert removed_again['data']['canonical_document']['dependency_manifest']['documents'] == [
        options['schema_source']]


def test_owner_pinned_add_rebases_over_disjoint_track_write(admitted_overlay):
    realm, element, options, row, _ = admitted_overlay
    base = copy.deepcopy(realm.head)
    add = capture_clip_add(
        current(realm), 'parent', {**row, 'id': 'rebased-overlay'},
        schema_source=options['schema_source'], schema_inputs=options['schema_inputs'], realm_id='realm')
    commit(realm, [capture_track_set(current(realm), 'parent/track:picture', values={'label': 'peer'})])
    result = commit(realm, [add], base=base)
    assert result['data']['status'] == 'rebased'
    assert State(current(realm)).entity('parent/clip:rebased-overlay')['elementRef'] == element
    assert State(current(realm)).entity('parent/track:picture')['label'] == 'peer'


@pytest.mark.parametrize('damage', ['owner', 'revision', 'pin'])
def test_owner_pinned_add_refuses_wrong_authority_before_writes(admitted_overlay, damage):
    realm, element, options, row, _ = admitted_overlay
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    raw = capture_clip_add(
        current(realm), 'parent', {**row, 'id': 'bad-overlay'},
        schema_source=options['schema_source'], schema_inputs=options['schema_inputs'], realm_id='realm')
    if damage in {'owner', 'revision'}:
        raw['args']['row']['elementRef'][damage if damage == 'revision' else 'packId'] = 'wrong'
    else:
        raw['args']['schema_source']['version'] += 1
    with pytest.raises(CommitRejected):
        commit(realm, [raw])
    assert (realm.head, realm.entries, realm.documents) == before
