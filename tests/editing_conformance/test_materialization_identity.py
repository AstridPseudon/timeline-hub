"""Scoped compiler slots and the ratified derived-allocation requirements."""
from __future__ import annotations

import copy

import pytest
from jsonschema import Draft202012Validator, ValidationError

from astrid.sdk.timeline._command_state import State, present
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import _SCHEMA, execute
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.rebase import replay
from tests.sdk.test_timeline_commit_provider_document import document_fixture


def source(*, project='project-1', timeline='film', shot='chapter-shot'):
    document = document_fixture()
    document.update(project_id=project, timeline_id=timeline)
    document['shot_revisions'][0]['shot_id'] = shot
    for occurrence in document['parent_revision']['payload']['occurrences']:
        occurrence.update(shot_id=shot, source_offset=0, speed=1)
    document['dependency_manifest'] = _manifest(
        document['shot_revisions'], document['internal_timeline_revisions'],
        document['dependency_manifest']['media'], [])
    document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
    return document


def slots(bundle, index=0):
    shot_id = bundle['placements'][index]['shot_id']
    return shot_id, {item['item_id'] for item in bundle['shots'][shot_id]['payload']['items']}


@pytest.mark.parametrize('changed', [
    {'timeline': 'duplicate-film'}, {'project': 'project-2'}, {'shot': 'other-source'},
])
def test_same_raw_occurrence_and_item_ids_have_disjoint_scoped_slots(changed):
    original = source()
    duplicate = source(**changed)
    # Both inputs retain the same occurrence and raw item IDs.
    assert original['shot_revisions'][0]['payload']['items'] == duplicate['shot_revisions'][0]['payload']['items']
    assert [row['occurrence_id'] for row in original['parent_revision']['payload']['occurrences']] == [
        row['occurrence_id'] for row in duplicate['parent_revision']['payload']['occurrences']]
    first, second = bundle_from_document(original), bundle_from_document(duplicate)
    shot_a, items_a = slots(first)
    shot_b, items_b = slots(second)
    assert shot_a != shot_b
    assert items_a.isdisjoint(items_b)
    assert slots(first) == slots(bundle_from_document(original))


def test_sibling_slots_differ_and_changed_raw_source_is_not_an_identity_alias():
    original = bundle_from_document(source())
    sibling_a, items_a = slots(original)
    sibling_b, items_b = slots(original, 1)
    assert sibling_a != sibling_b
    assert items_a.isdisjoint(items_b)
    changed = State(bundle_from_document(source(shot='other-source')))
    assert not changed.matches('occurrence:occ-a/shot', ['shot_id'], present('chapter-shot'))


def test_exact_replay_keeps_compiled_slot_ids_without_mutating_source():
    original = bundle_from_document(source())
    before = copy.deepcopy(original)
    command = capture_move(original, 'occurrence:occ-a/clip:clip-a', 3.003)
    plan = execute(original, [command])
    repeated = replay(plan, original)
    assert repeated.records == plan.records
    assert document_from_bundle(repeated.bundle) == document_from_bundle(plan.bundle)
    assert slots(repeated.bundle) == slots(plan.bundle) == slots(original)
    assert original == before


# The physical-birth expectation was superseded by the ratified allocation map:
# these authored virtual roots already exist; only semantic births use created.
@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason='M2 must retain source-bound derived id_map after paired carrier freeze')
def test_materialization_retains_derived_map_without_false_semantic_births():
    original = bundle_from_document(source())
    plan = execute(original, [capture_move(original, 'occurrence:occ-a/clip:clip-a', 3.003)])
    output = document_from_bundle(plan.bundle)
    shot_id = output['parent_revision']['payload']['occurrences'][0]['shot_id']
    shot = next(row for row in output['shot_revisions'] if row['shot_id'] == shot_id)
    assert shot_id != 'chapter-shot'
    assert State(original).entity('shot:' + shot_id) is not None
    assert [fact for record in plan.records for fact in record['created']] == []
    expected = {'shot:' + shot_id: shot_id,
                **{'shot:' + shot_id + '/item:' + item['item_id']: item['item_id']
                   for item in shot['payload']['items']}}
    assert getattr(plan, 'id_map', {}) == expected


# Canonical item refs serve source bindings and separate semantic item births.
@pytest.mark.parametrize('definition,value', [
    ('ScopedId', 'shot:allocated/item:allocated-item'),
    ('EntityRef', 'shot:allocated/item:allocated-item'),
    ('TargetKey', 'shot:allocated/item:allocated-item::'),
    ('AnchorIdentity', 'shot:allocated/item:allocated-item'),
])
@pytest.mark.xfail(strict=True, raises=ValidationError,
                   reason='M2 shot-owned item refs require paired canonical source/normal generation')
def test_required_shot_owned_item_address_has_a_command_carrier(definition, value):
    Draft202012Validator({'$defs': _SCHEMA['$defs'], '$ref': '#/$defs/' + definition}).validate(value)
