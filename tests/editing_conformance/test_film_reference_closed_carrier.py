"""Private source proposal for the bounded occurrence film-reference carrier."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import _SCHEMA, execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_recipe_occurrence_create import empty_bundle
from tests.editing_conformance.test_recipe_occurrence_media import inputs

OWNER = 'occurrence:occ-a'
REFERENCE = {
    'version': 1,
    'reference_id': 'exact-reference',
    'role': 'source',
    'asset': 'reserved-new',
}
FROZEN_EXTENT_SHA256 = '84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5'


def _without_reference(schema):
    del schema['$defs']['OccurrenceAddMediaArgs']['properties']['timeline_reference']
    del schema['$defs']['TimelineReferenceBinding']
    return schema


def _birth_with_reference():
    return {
        'schema_version': 1,
        'op': 'occurrence.create',
        'version': '1',
        'select': 'parent',
        'args': {
            'occurrence_id': 'unplaced-occurrence',
            'shot_id': 'unplaced-shot',
            'name': 'Reference only',
            'track': 'picture',
            'on': 0,
            'duration': 1,
            'timeline_reference': REFERENCE,
        },
        'intent': {'ownership': 'occurrence'},
    }


def test_unplaced_reference_cannot_be_reclassified_as_an_occurrence_birth():
    original = empty_bundle()
    with pytest.raises(CommandError):
        validate_command(_birth_with_reference())

    birth = copy.deepcopy(_birth_with_reference())
    birth['args'].pop('timeline_reference')
    plan = execute(original, [birth])
    assert State(plan.bundle).occurrence('occurrence:unplaced-occurrence')['shot_id'] == 'unplaced-shot'
    assert plan.bundle['placements'][0]['occurrence_id'] == 'unplaced-occurrence'


def test_placed_reference_carrier_derives_from_local_media_and_inverts_exactly():
    document, bundle, ordinary, verified = _captured_add()
    occurrence = State(bundle).occurrence(OWNER)
    occurrence['provenance'] = {
        'opaque': {'keep': [None, False, 0]},
        'astrid': {'opaque': {'keep': True}},
    }
    before = copy.deepcopy(bundle)
    row = ordinary['args']['row']
    pin = ordinary['args']['media']
    command = capture_occurrence_add_media(
        bundle, OWNER, row, pin, verified_media=verified, timeline_reference=REFERENCE,
    )
    plan = execute(bundle, [command], verified_media=verified)
    stored = State(plan.bundle).occurrence(OWNER)
    assert stored['provenance'] == {
        'opaque': {'keep': [None, False, 0]},
        'astrid': {
            'opaque': {'keep': True},
            'timeline_reference': REFERENCE,
        },
    }
    assert State(plan.bundle).entity(OWNER + '/asset:' + REFERENCE['asset'])['media_id'] == pin['object_id']
    assert State(plan.bundle).entity(OWNER + '/clip:' + row['id']) == row
    assert inverse(plan.bundle, plan.records).bundle == before
    assert document['project_id'] == 'project-1'


def test_reference_identity_and_selected_asset_are_closed_and_occupied():
    _, bundle, ordinary, verified = _captured_add()
    row, pin = ordinary['args']['row'], ordinary['args']['media']
    State(bundle).occurrence('occurrence:occ-b')['provenance'] = {
        'astrid': {'timeline_reference': copy.deepcopy(REFERENCE)},
    }
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='occupied'):
        capture_occurrence_add_media(
            bundle, OWNER, row, pin, verified_media=verified, timeline_reference=REFERENCE,
        )
    assert bundle == before

    _, bundle, ordinary, verified = _captured_add()
    row, pin = ordinary['args']['row'], ordinary['args']['media']
    command = capture_occurrence_add_media(bundle, OWNER, row, pin, verified_media=verified)
    command['args']['timeline_reference'] = copy.deepcopy(REFERENCE)
    changed = copy.deepcopy(command)
    changed['args']['timeline_reference']['asset'] = 'other-asset'
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        execute(bundle, [changed], verified_media=verified)
    assert bundle == before


def _captured_add():
    document, old, new, verified = inputs('image')
    bundle = bundle_from_document(document)
    row = {
        'id': 'reference-child', 'clipType': 'image', 'asset': new['asset'],
        'track': 'picture', 'at': .125, 'hold': 1, 'params': None,
    }
    command = capture_occurrence_add_media(bundle, OWNER, row, new, verified_media=verified)
    return document, bundle, command, verified


def test_reference_descendant_reconstructs_the_frozen_extent_schema():
    raw = (json.dumps(_without_reference(copy.deepcopy(_SCHEMA)), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == FROZEN_EXTENT_SHA256
    assert len(_SCHEMA['$defs']) == 60
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 33
