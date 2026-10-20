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
PRIVATE_EXTENT_SHA256 = '166644a84067b4f40fe6cc4a0d0047cfe2e4fb2678ca1d7b2fc9d48c605cfa41'


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


def without_extent(schema):
    del schema['$defs']['OccurrenceResizeArgs']
    schema['$defs']['EditCommand']['allOf'] = [
        clause for clause in schema['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'occurrence.resize']
    return schema


def ordinary_schema():
    """Remove only the reviewed carrier additions, checking each complete branch."""
    candidate = without_extent(without_groups(without_voiceover(copy.deepcopy(_SCHEMA))))
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
    assert len(_SCHEMA['$defs']) == 59
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 33
    assert compatibility_errors(ordinary, _SCHEMA) == []


def test_removing_only_group_additions_reconstructs_project_data_bytes():
    candidate = without_extent(without_groups(without_voiceover(copy.deepcopy(_SCHEMA))))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_PROJECT_DATA_SHA256
    assert len(candidate['$defs']) == 56
    assert len(candidate['$defs']['EditCommand']['allOf']) == 30


def test_removing_group_and_project_data_additions_reconstructs_private_carrier_bytes():
    candidate = without_extent(without_groups(without_voiceover(copy.deepcopy(_SCHEMA))))
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
    raw = (json.dumps(without_extent(without_groups(without_voiceover(copy.deepcopy(_SCHEMA)))), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_PROJECT_DATA_SHA256


def test_private_extent_proposal_is_one_addition_on_voiceover_floor():
    raw = (json.dumps(_SCHEMA, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_EXTENT_SHA256
    assert len(_SCHEMA['$defs']) == 59
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 33


def test_extent_proposal_preserves_the_prior_voiceover_schema_hash():
    candidate = without_extent(copy.deepcopy(_SCHEMA))
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_VOICEOVER_SHA256
    assert len(candidate['$defs']) == 58
    assert len(candidate['$defs']['EditCommand']['allOf']) == 32


def test_voiceover_property_preserves_the_prior_group_schema_hash():
    raw = (json.dumps(without_extent(without_voiceover(copy.deepcopy(_SCHEMA))), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_GROUP_SHA256


def test_complete_reviewed_private_s2_is_preserved_without_a_copied_frozen_schema():
    from tests.sdk.test_timeline_current_union_schema import FIXTURES, baseline

    previous = baseline('agent-frozen-s2-26ef2bbb')
    current = without_extent(without_voiceover(copy.deepcopy(_SCHEMA)))
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
    assert compatibility_errors(previous, _SCHEMA) == []


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
