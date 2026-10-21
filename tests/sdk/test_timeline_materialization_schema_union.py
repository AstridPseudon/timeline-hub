"""The private carrier is additive to the complete ordinary source schema."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest
from jsonschema import Draft202012Validator, ValidationError

from astrid.sdk.timeline._materialization import SOURCE_BOUND_OPERATIONS
from astrid.sdk.timeline.commands import _SCHEMA
from tests.sdk.command_schema_compatibility import compatibility_errors

REFERENCES = ('ScopedId', 'EntityRef', 'TargetKey')
ORDINARY_SHA256 = '6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d'
PRIVATE_S2_SHA256 = 'f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f'
PRIVATE_CARRIER_SHA256 = '613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3'
PRIVATE_PROJECT_DATA_SHA256 = '39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d'
PRIVATE_GROUP_SHA256 = '27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb'
PRIVATE_VOICEOVER_SHA256 = '65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e'
PRIVATE_EXTENT_SHA256 = '84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5'
PRIVATE_REMOVE_SHA256 = 'c49a6058cfb49fec3dd12e8d93868de6433f121b07a56a943257e34b239f9b7c'
PRIVATE_MUTE_SHA256 = '0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890'
PRIVATE_OPACITY_SHA256 = '9b4f16f87fffc00da010e2dbea469ca6bfc021695c5b453c821d1d4553336708'
PRIVATE_FULL_MOVE_SET_SHA256 = 'ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7'
PRIVATE_LITERAL_UNION_SHA256 = 'da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068'
PRIVATE_REFERENCE_ORDER_SHA256 = 'c47a00135a2beb9df35cbbf201ef6b7f900904f4afeb74efe3cf12871271598e'
RAW_OLD_CANONICAL_SHA256 = 'd3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2'
FROZEN_10226_CANONICAL_SHA256 = '322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc'


def without_insertion_order(schema):
    """Reconstruct the frozen 10226 AgentWrite carrier exactly."""
    assert schema['$defs']['AgentWrite']['properties'].pop('insertion_order') == {
        'type': 'array',
        'items': {'type': 'string'},
    }
    return schema


def without_move_set(schema):
    """Remove only the reviewed free multi-clip move operation."""
    del schema['$defs']['ClipMoveSetArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'clip.move-set']
    return schema


def without_reference(schema):
    """Remove only the reviewed raw parent reference operation."""
    del schema['$defs']['TimelineReferenceArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'timeline.reference'
    ]
    return schema


def without_track_reorder(schema):
    """Remove only the reviewed parent track order operation."""
    del schema['$defs']['TrackReorderArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'track.reorder'
    ]
    return schema


def without_raw_old_swap(schema):
    """Remove the additive raw-OLD successor from an earlier schema floor."""
    for clause in schema['$defs']['EditCommand']['allOf']:
        op = clause['if']['properties']['op']['const']
        if op not in {'clip.swap-media', 'occurrence.swap-media'}:
            continue
        branches = clause['then'].get('anyOf', [clause['then']])
        branches[:] = [branch for branch in branches
                       if branch['properties']['args'].get('$ref') != '#/$defs/RawOldSwapMediaArgs']
        if op == 'clip.swap-media':
            clause['then'] = branches[0]
    for name in ('RawOldSwapMediaArgs', 'MediaManifestEntry'):
        schema['$defs'].pop(name, None)
    return schema


def without_transcript(schema):
    """Remove only the reviewed transcript successor from the raw-OLD union."""
    del schema['$defs']['TranscriptAssociateArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'transcript.associate'
    ]
    return schema


def without_new_sources(schema):
    """Reconstruct the pre-movement/reference/order schema without fixtures."""
    return without_insertion_order(without_track_reorder(without_reference(without_move_set(
        without_raw_old_swap(without_transcript(schema))))))


def without_reference_and_order(schema):
    return without_insertion_order(without_track_reorder(without_reference(without_raw_old_swap(
        without_transcript(schema)))))


def without_mute(schema):
    """Remove only the reviewed raw track mute leaf from a copied schema."""
    args = schema['$defs']['TrackSetArgs']
    assert args['properties']['values']['properties'].pop('muted') == {
        'type': 'boolean',
        'description': 'Raw authored track mute flag; absent remains absent until explicitly set.',
    }
    clear = args['properties']['clear']['items']
    assert clear['enum'] == ['label', 'muted']
    clear.clear()
    clear['const'] = 'label'
    args['description'] = (
        'Set raw track.label or explicitly remove it. Null is not a label. Unmentioned fields survive.')
    return schema


def without_opacity(schema):
    """Remove only the reviewed raw clip opacity leaf from a copied schema."""
    args = schema['$defs']['ClipSetArgs']
    assert args['properties']['values']['properties'].pop('opacity') == {
        'type': 'number',
        'minimum': 0,
        'maximum': 1,
        'description': 'Raw visual opacity fraction in the inclusive range 0..1.',
    }
    assert args['properties']['clear']['items']['enum'].pop() == 'opacity'
    args['description'] = (
        'Bounded raw clip fields. Set hold in source seconds; explicitly remove hold, asset or incoming '
        'transition. Clear removes presence, never sets null/empty. Asset assignment requires the scoped '
        'clip.swap-media or occurrence.swap-media; transition authoring is outside v1.')
    return schema


def without_literal_fields(schema):
    """Remove only mute and opacity; all ordered-remove content remains."""
    return without_opacity(without_mute(schema))


def without_groups(schema):
    for name in ('MigrateGroupsArgs', 'OccurrenceMoveArgs'):
        del schema['$defs'][name]
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] not in
        ('timeline.migrate-groups', 'occurrence.move')]
    return schema


def without_voiceover(schema):
    shot = schema['$defs']['ShotSetArgs']
    del shot['properties']['values']['properties']['metadata']
    shot['properties']['clear']['items']['enum'].remove('metadata.draft_voiceover')
    shot['description'] = (
        'Occurrence-owned raw shot payload fields: canonical root name and bounded scalar settings roots. '
        'Null is a value; clear removes presence. Unmentioned fields survive. Compound settings roots '
        '(steerableMotionSettings, phaseConfig, pairConfigs, shotImageIds, loras, structureVideo, '
        'modelSettingsByModel) are unsupported.')
    return schema


def without_remove(schema):
    """Reconstruct the reviewed private voiceover/extent source."""
    args = schema['$defs']['ProjectDataWriteArgs']
    assert args['properties']['mode']['enum'] == ['replace', 'remove']
    args['properties']['mode'] = {'const': 'replace'}
    schema['$defs']['ProjectDataWriteArgs'] = {
        'type': args['type'],
        'required': ['target', 'key', 'value', 'mode'],
        'additionalProperties': args['additionalProperties'],
        'properties': args['properties'],
        'description': (
            'Replace one opaque extension-owned project-data value in the parent authored '
            'timeline. The project catalog is a separate scoped operation.'),
    }
    return schema


def without_extent(schema):
    del schema['$defs']['OccurrenceResizeArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'occurrence.resize']
    move = schema['$defs']['OccurrenceMoveArgs']
    schema['$defs']['OccurrenceMoveArgs'] = {
        'type': move['type'],
        'required': ['on', 'track', 'child_track'],
        'additionalProperties': move['additionalProperties'],
        'properties': {key: value for key, value in move['properties'].items()
                       if key != 'start_ms'},
    }
    return schema


def ordinary_schema():
    """Remove only the reviewed carrier additions, checking each complete branch."""
    candidate = without_new_sources(without_groups(without_extent(without_voiceover(
        without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))))))
    del candidate['$defs']['ProjectDataWriteArgs']
    candidate['$defs']['EditCommand']['allOf'] = [
        clause for clause in candidate['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'project-data.write'
    ]
    for name in REFERENCES:
        branches = candidate['$defs'][name]['anyOf']
        assert len(branches) == 4
        addition = branches.pop()
        old = branches[1]
        assert addition.keys() == old.keys()
        assert addition == {**old, 'pattern': addition['pattern']}
        assert addition['pattern'].startswith(f"(?:{old['pattern']})|(?:^shot:")
        assert addition['pattern'].endswith('$)')
    definition = candidate['$defs']['AnchorIdentity']
    old, item = definition['pattern'].removeprefix('(?:').split(')|(?:^shot:', 1)
    assert item == '(?:(?!::)[^/])+/item:(?:(?!::)[^/])+$)'
    definition['pattern'] = old
    affected = set()
    for clause in candidate['$defs']['EditCommand']['allOf']:
        if 'anyOf' not in clause['then']:
            continue
        old, new = clause['then']['anyOf']
        expected = copy.deepcopy(old)
        expected['properties']['version']['const'] = '2'
        assert new == expected
        clause['then'] = old
        affected.add(clause['if']['properties']['op']['const'])
    assert affected | {'track.create'} == SOURCE_BOUND_OPERATIONS
    return candidate


def test_only_carrier_additions_separate_union_from_exact_complete_ordinary_source():
    ordinary = ordinary_schema()
    raw = (json.dumps(ordinary, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == ORDINARY_SHA256
    assert len(ordinary['$defs']) == 55
    assert len(ordinary['$defs']['EditCommand']['allOf']) == 29
    assert len(_SCHEMA['$defs']) == 65
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 37
    assert compatibility_errors(ordinary, without_new_sources(without_literal_fields(copy.deepcopy(_SCHEMA)))) == []


def test_write_order_successor_preserves_frozen_10226_schema_bytes():
    predecessor = without_insertion_order(copy.deepcopy(_SCHEMA))
    raw = (json.dumps(predecessor, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == FROZEN_10226_CANONICAL_SHA256
    assert compatibility_errors(predecessor, _SCHEMA) == []
    assert _SCHEMA['$defs']['AgentWrite']['properties']['insertion_order'] == {
        'type': 'array',
        'items': {'type': 'string'},
    }
    assert 'insertion_order' not in predecessor['$defs']['AgentWrite']['properties']


def test_removing_only_group_additions_reconstructs_project_data_bytes():
    candidate = without_new_sources(without_groups(without_extent(without_voiceover(
        without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))))))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_PROJECT_DATA_SHA256
    assert len(candidate['$defs']) == 56
    assert len(candidate['$defs']['EditCommand']['allOf']) == 30


def test_removing_group_and_project_data_additions_reconstructs_private_carrier_bytes():
    candidate = without_new_sources(without_groups(without_extent(without_voiceover(
        without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))))))
    del candidate['$defs']['ProjectDataWriteArgs']
    candidate['$defs']['EditCommand']['allOf'] = [
        clause for clause in candidate['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'project-data.write'
    ]
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_CARRIER_SHA256
    assert len(candidate['$defs']) == 55
    assert len(candidate['$defs']['EditCommand']['allOf']) == 29


def test_project_data_proposal_has_a_new_closed_schema_hash():
    candidate = without_new_sources(without_groups(without_extent(without_voiceover(
        without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))))))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_PROJECT_DATA_SHA256


def test_private_remove_proposal_is_one_addition_on_extent_floor():
    raw = (json.dumps(without_new_sources(without_literal_fields(copy.deepcopy(_SCHEMA))), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_REMOVE_SHA256
    assert len(without_new_sources(copy.deepcopy(_SCHEMA))['$defs']) == 59
    assert len(without_new_sources(copy.deepcopy(_SCHEMA))['$defs']['EditCommand']['allOf']) == 33


def test_private_extent_floor_is_preserved_when_remove_is_stripped():
    raw = (json.dumps(without_new_sources(without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_EXTENT_SHA256
    assert len(without_new_sources(copy.deepcopy(_SCHEMA))['$defs']) == 59
    assert len(without_new_sources(copy.deepcopy(_SCHEMA))['$defs']['EditCommand']['allOf']) == 33


def test_full_move_set_schema_reconstructs_its_exact_source_floor():
    candidate = without_reference_and_order(without_remove(without_literal_fields(copy.deepcopy(_SCHEMA))))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_FULL_MOVE_SET_SHA256
    assert len(candidate['$defs']) == 60
    assert len(candidate['$defs']['EditCommand']['allOf']) == 34


def test_literal_three_union_reconstructs_each_reviewed_source_floor():
    candidates = {
        'literal-union-f448': without_new_sources(copy.deepcopy(_SCHEMA)),
        'movement3b320': without_reference_and_order(
            without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))),
            'reference-order-85c': without_insertion_order(without_raw_old_swap(
            without_transcript(
                without_move_set(
                    without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))
                )
                )
            )),
        'ordered-remove': without_new_sources(without_opacity(without_mute(copy.deepcopy(_SCHEMA)))),
        'track-mute': without_new_sources(without_opacity(without_remove(copy.deepcopy(_SCHEMA)))),
        'opacity': without_new_sources(without_mute(without_remove(copy.deepcopy(_SCHEMA)))),
        'exact84fc': without_new_sources(without_remove(without_literal_fields(copy.deepcopy(_SCHEMA)))),
    }
    expected = {
        'literal-union-f448': PRIVATE_LITERAL_UNION_SHA256,
        'movement3b320': PRIVATE_FULL_MOVE_SET_SHA256,
        'reference-order-85c': PRIVATE_REFERENCE_ORDER_SHA256,
        'ordered-remove': PRIVATE_REMOVE_SHA256,
        'track-mute': PRIVATE_MUTE_SHA256,
        'opacity': PRIVATE_OPACITY_SHA256,
        'exact84fc': PRIVATE_EXTENT_SHA256,
    }
    for name, candidate in candidates.items():
        raw = (json.dumps(candidate, indent=2) + '\n').encode()
        assert hashlib.sha256(raw).hexdigest() == expected[name], name
def test_transcript_successor_strips_to_exact_raw_old_schema():
    candidate = without_insertion_order(without_transcript(copy.deepcopy(_SCHEMA)))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == RAW_OLD_CANONICAL_SHA256
    assert len(candidate['$defs']) == 64
    assert len(candidate['$defs']['EditCommand']['allOf']) == 36


def test_extent_proposal_preserves_the_prior_voiceover_schema_hash():
    candidate = without_new_sources(without_literal_fields(without_extent(without_remove(copy.deepcopy(_SCHEMA)))))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_VOICEOVER_SHA256
    assert len(candidate['$defs']) == 58
    assert len(candidate['$defs']['EditCommand']['allOf']) == 32


def test_voiceover_property_preserves_the_prior_group_schema_hash():
    raw = (json.dumps(without_new_sources(without_literal_fields(without_extent(
        without_voiceover(without_remove(copy.deepcopy(_SCHEMA)))))), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_GROUP_SHA256


def test_complete_reviewed_private_s2_is_preserved_without_a_copied_frozen_schema():
    from tests.sdk.test_timeline_current_union_schema import FIXTURES, baseline

    previous = baseline('agent-frozen-s2-26ef2bbb')
    current = without_new_sources(without_literal_fields(without_extent(
        without_voiceover(without_remove(copy.deepcopy(_SCHEMA))))))
    raw = (FIXTURES / 'agent-frozen-s2-26ef2bbb.json').read_bytes()
    for name in (*REFERENCES, 'AnchorIdentity'):
        addition = copy.deepcopy(
            current['$defs'][name]['anyOf'][-1] if name in REFERENCES else current['$defs'][name])
        old = json.dumps(previous['$defs'][name]['pattern']).encode()
        assert raw.count(old) == 1
        raw = raw.replace(old, json.dumps(addition['pattern']).encode(), 1)
        previous['$defs'][name] = addition
    current = {clause['if']['properties']['op']['const']: clause
               for clause in current['$defs']['EditCommand']['allOf']}
    for clause in previous['$defs']['EditCommand']['allOf']:
        op = clause['if']['properties']['op']['const']
        if op in SOURCE_BOUND_OPERATIONS - {'track.create'}:
            old = json.dumps(clause['then'], indent=2).replace('\n', '\n          ').encode()
            addition = copy.deepcopy(current[op]['then'])
            new = json.dumps(addition, indent=2).replace('\n', '\n          ').encode()
            assert raw.count(old) == 1
            raw = raw.replace(old, new, 1)
            clause['then'] = addition
    assert json.loads(raw) == previous
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_S2_SHA256
    assert compatibility_errors(previous, without_new_sources(without_literal_fields(copy.deepcopy(_SCHEMA)))) == []


@pytest.mark.parametrize('name', (*REFERENCES, 'AnchorIdentity'))
@pytest.mark.parametrize('ref', ['shot:source/item:item', 'shot:雪 !/item:123'])
def test_typed_item_references_are_additive(name, ref):
    value = ref + '::' if name == 'TargetKey' else ref
    with pytest.raises(ValidationError):
        Draft202012Validator(ordinary_schema()).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)
    Draft202012Validator(_SCHEMA).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)


@pytest.mark.parametrize('ref', ['shot:/item:item', 'shot:shot/item:', 'shot:shot/item:item/extra',
                                'shot:shot/item:item::ambiguous', 'shot:shot::ambiguous/item:item'])
def test_typed_item_references_keep_scope_constraints(ref):
    for name in (*REFERENCES, 'AnchorIdentity'):
        value = ref + '::' if name == 'TargetKey' else ref
        with pytest.raises(ValidationError):
            Draft202012Validator(_SCHEMA).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)


def test_operation_versions_remain_limited_to_the_reviewed_thirteen_operations():
    assert SOURCE_BOUND_OPERATIONS == {
        'clip.move', 'placement.move', 'track.create', 'clip.set', 'clip.set-element',
        'track.set', 'shot.set', 'clip.set-params', 'occurrence.add-media',
        'occurrence.swap-media', 'placement.create', 'placement.unplace', 'shot.pool',
    }
