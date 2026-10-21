"""Design spike over real compiler closures, not Runtime admission or new ports.

The join below uses existing map/binding/dependency envelopes. It models source
verification only; physical occupancy and historical own-slot proof are Runtime's.
"""
from __future__ import annotations

import copy
import json

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import _SCHEMA, execute
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_materialization_identity import source
from tests.editing_conformance.test_recipe_m1_commands import inverse


def physical(document, occurrence):
    owner = next(row for row in document['parent_revision']['payload']['occurrences']
                 if row['occurrence_id'] == occurrence)
    shot = next(row for row in document['shot_revisions']
                if row['revision_id'] == owner['shot_revision_id'])
    return owner['shot_id'], {item.get('item_id', item.get('id')) for item in shot['payload']['items']}


def allocation(original, output):
    """Derive the proposed join from verified ORIGINAL source and output closures."""
    mapping, bindings, dependencies = {}, [], []
    for occurrence in original['placements']:
        destination = occurrence['shot_id']
        origin = original['source_mapping']['shots'][destination]
        actual, items = physical(output, occurrence['occurrence_id'])
        if actual == origin['shot_id']:
            continue  # Parent-only edits preserve source images, not virtual slots.
        assert actual == destination
        assert items == set(origin['item_id_map'].values())
        source_shot = 'shot:' + origin['shot_id']
        shot = 'shot:' + destination
        key = 'materialization.source:' + shot
        dependencies.append({'key': key, 'kind': 'entity', 'policy': 'exact', 'pin': {
            'parent': copy.deepcopy(original['base_parent']), 'source': copy.deepcopy(origin)}})
        pairs = [(shot, source_shot, destination), *(
            (shot + '/item:' + target, source_shot + '/item:' + raw, target)
            for raw, target in origin['item_id_map'].items())]
        for ref, source_ref, identity in pairs:
            mapping[ref] = identity
            bindings.append({'key': ref, 'ref': source_ref, 'policy': 'fixed', 'dependencies': [key]})
        bindings.append({'key': 'materialization.owner:' + shot,
                         'ref': 'occurrence:' + occurrence['occurrence_id'],
                         'policy': 'fixed', 'dependencies': [key]})
    return mapping, bindings, dependencies


def verify(original, output, captured):
    mapping, bindings, dependencies = captured
    expected = allocation(original, output)
    # Existing legacy identity pairs remain gated as before; no suffix rewriting.
    assert {key: value for key, value in mapping.items() if key != value} == expected[0]
    assert (bindings, dependencies) == expected[1:]
    assert all(isinstance(key, str) and isinstance(value, str) and key and value
               for key, value in mapping.items())
    for definition, values in [('AgentBinding', bindings), ('AgentDependency', dependencies)]:
        validator = Draft202012Validator({'$defs': _SCHEMA['$defs'], '$ref': '#/$defs/' + definition})
        for value in values:
            validator.validate(value)


def moved(original, occurrence='occ-a', on=3.003):
    return execute(original, [capture_move(original, 'occurrence:' + occurrence + '/clip:clip-a', on)])


def test_capture_join_explicit_source_output_edges_and_json_recovery():
    original = bundle_from_document(source())
    plan = moved(original)
    output = document_from_bundle(plan.bundle)
    captured = json.loads(json.dumps(allocation(original, output)))
    verify(original, output, captured)
    before = physical(source(), 'occ-a')
    after = physical(output, 'occ-a')
    assert before[0] == 'chapter-shot' and before[1] == {'item-1'}
    assert before[0] != after[0] and before[1].isdisjoint(after[1])
    assert len(captured[0]) == 2
    assert all(record['created'] == [] for record in plan.records)
    assert document_from_bundle(original) == source()


def test_replay_stale_parent_undo_redo_restore_and_second_materialization():
    original = bundle_from_document(source())
    plan = moved(original)
    output = document_from_bundle(plan.bundle)
    captured = allocation(original, output)
    saved = copy.deepcopy(captured)
    head = copy.deepcopy(original)
    head['parent']['name'] = 'Disjoint later edit'
    for replayed in (replay(plan, original), replay(plan, head)):
        verify(original, document_from_bundle(replayed.bundle), captured)
    undone = inverse(plan.bundle, plan.records)
    assert document_from_bundle(undone.bundle) == source()
    assert allocation(original, document_from_bundle(undone.bundle))[0] == {}
    redone = inverse(undone.bundle, undone.records)
    verify(original, document_from_bundle(redone.bundle), captured)
    restored = bundle_from_document(source())  # Revision restore, not physical-row deletion.
    verify(original, document_from_bundle(moved(restored).bundle), captured)
    sibling = moved(original, 'occ-b', 12.012)
    sibling_map = allocation(original, document_from_bundle(sibling.bundle))
    assert len({**captured[0], **sibling_map[0]}) == 4
    assert set(captured[0].values()).isdisjoint(sibling_map[0].values())
    assert captured == saved


@pytest.mark.parametrize('damage', ['missing', 'extra', 'fake', 'binding', 'owner', 'source', 'scope'])
def test_unverified_map_or_source_pair_refuses(damage):
    original = bundle_from_document(source())
    output = document_from_bundle(moved(original).bundle)
    captured = allocation(original, output)
    mapping, bindings, dependencies = captured
    if damage == 'missing':
        mapping.pop(next(iter(mapping)))
    elif damage == 'extra':
        mapping['shot:unrelated'] = 'unrelated'
    elif damage == 'fake':
        mapping[next(iter(mapping))] = 'arbitrary-overwrite'
    elif damage == 'binding':
        bindings[1]['ref'] = 'shot:chapter-shot/item:wrong-source'
    elif damage == 'owner':
        bindings[-1]['ref'] = 'occurrence:occ-b'
    elif damage == 'source':
        dependencies[0]['pin']['source']['revision_id'] = 'new-head-is-not-original'
    else:
        original = bundle_from_document(source(project='other-project'))
    before = copy.deepcopy(output)
    with pytest.raises(AssertionError):
        verify(original, output, captured)
    assert output == before


def test_parent_only_map_and_legacy_identity_pairs():
    original = bundle_from_document(source())
    output = document_from_bundle(original)
    verify(original, output, ({}, [], []))
    verify(original, output, ({'existing': 'existing'}, [], []))


def test_native_replay_after_sibling_materialization_keeps_original_destination():
    original = bundle_from_document(source())
    plan = moved(original)
    captured = allocation(original, document_from_bundle(plan.bundle))
    sibling = moved(original, 'occ-b', 12.012)
    head = bundle_from_document(document_from_bundle(sibling.bundle))
    output = document_from_bundle(replay(plan, head).bundle)
    assert physical(output, 'occ-a') == physical(document_from_bundle(plan.bundle), 'occ-a')
    # Validate this occurrence's original join, preserving the sibling's own join.
    assert set(captured[0].values()).issubset({physical(output, 'occ-a')[0], *physical(output, 'occ-a')[1]})


def test_raw_id_item_codec_materializes_without_collision():
    document = source()
    shot = document['shot_revisions'][0]
    item = shot['payload']['items'][0]
    item['id'] = item.pop('item_id')
    shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest([shot], document['internal_timeline_revisions'],
                                               document['dependency_manifest']['media'], [])
    original = bundle_from_document(document)
    output = document_from_bundle(moved(original).bundle)
    verify(original, output, allocation(original, output))
