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


def without_opacity(schema):
    """Remove only the proposed opacity additions from a copied schema."""
    candidate = copy.deepcopy(schema)
    args = candidate['$defs']['ClipSetArgs']
    values = args['properties']['values']['properties']
    assert values.pop('opacity') == {
        'type': 'number',
        'minimum': 0,
        'maximum': 1,
        'description': 'Raw visual opacity fraction in the inclusive range 0..1.',
    }
    clear = args['properties']['clear']['items']['enum']
    assert clear.pop() == 'opacity'
    assert args['description'].startswith(
        'Bounded raw clip fields. Set hold in source seconds or opacity as a raw 0..1 fraction;')
    args['description'] = (
        'Bounded raw clip fields. Set hold in source seconds; explicitly remove hold, asset or incoming '
        'transition. Clear removes presence, never sets null/empty. Asset assignment requires the scoped '
        'clip.swap-media or occurrence.swap-media; transition authoring is outside v1.')
    return candidate


def ordinary_schema():
    """Remove opacity and the reviewed carrier additions, checking each complete branch."""
    candidate = without_opacity(_SCHEMA)
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
    assert len(_SCHEMA['$defs']) == 56
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 30
    assert compatibility_errors(ordinary, _SCHEMA) == []


def test_removing_only_project_data_addition_reconstructs_private_carrier_bytes():
    candidate = without_opacity(_SCHEMA)
    del candidate['$defs']['ProjectDataWriteArgs']
    candidate['$defs']['EditCommand']['allOf'] = [
        clause for clause in candidate['$defs']['EditCommand']['allOf']
        if clause['if']['properties']['op']['const'] != 'project-data.write'
    ]
    raw = (json.dumps(candidate, indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_CARRIER_SHA256
    assert len(candidate['$defs']) == 55
    assert len(candidate['$defs']['EditCommand']['allOf']) == 29


def test_removing_only_opacity_addition_reconstructs_project_data_bytes():
    raw = (json.dumps(without_opacity(_SCHEMA), indent=2) + '\n').encode()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_PROJECT_DATA_SHA256


def test_complete_reviewed_private_s2_is_preserved_without_a_copied_frozen_schema():
    from tests.sdk.test_timeline_current_union_schema import FIXTURES, baseline

    previous = baseline('agent-frozen-s2-26ef2bbb')
    raw = (FIXTURES / 'agent-frozen-s2-26ef2bbb.json').read_bytes()
    for name in (*REFERENCES, 'AnchorIdentity'):
        addition = copy.deepcopy(
            _SCHEMA['$defs'][name]['anyOf'][-1] if name in REFERENCES else _SCHEMA['$defs'][name])
        old = json.dumps(previous['$defs'][name]['pattern']).encode()
        assert raw.count(old) == 1
        raw = raw.replace(old, json.dumps(addition['pattern']).encode(), 1)
        previous['$defs'][name] = addition
    current = {clause['if']['properties']['op']['const']: clause
               for clause in _SCHEMA['$defs']['EditCommand']['allOf']}
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
