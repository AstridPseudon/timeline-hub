"""Materialization adds typed item refs without changing the published ordinary schema."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from astrid.sdk.timeline.commands import _SCHEMA
from tests.sdk.command_schema_compatibility import compatibility_errors
from tests.sdk.test_timeline_schema_superset import FIXTURES, baseline

REFERENCES = ('ScopedId', 'EntityRef', 'AnchorIdentity', 'TargetKey')


def ordinary_schema_bytes():
    """Reverse only the exact additive branches; preserve original formatting."""
    path = Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json'
    raw = path.read_bytes()
    for clause in _SCHEMA['$defs']['EditCommand']['allOf']:
        if 'anyOf' in clause['then']:
            old, new = clause['then']['anyOf']
            expected = copy.deepcopy(old)
            expected['properties']['version']['const'] = '2'
            assert new == expected
            wrapped = json.dumps(clause['then'], indent=2).replace('\n', '\n          ').encode()
            original = json.dumps(old, indent=2).replace('\n', '\n          ').encode()
            assert raw.count(wrapped) == 1
            raw = raw.replace(wrapped, original, 1)
    for name in REFERENCES:
        old = baseline('runtime-0.2.13')['$defs'][name]['pattern']
        new = _SCHEMA['$defs'][name]['pattern']
        assert new.startswith(f'(?:{old})|(?:^') and new.endswith('$)')
        assert raw.count(json.dumps(new).encode()) == 1
        raw = raw.replace(json.dumps(new).encode(), json.dumps(old).encode(), 1)
    return raw


def test_reversing_only_the_four_patterns_recovers_exact_ordinary_schema_bytes():
    raw = ordinary_schema_bytes()
    assert raw == (FIXTURES / 'runtime-0.2.13.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        'a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef')


@pytest.mark.parametrize('name', REFERENCES)
def test_each_current_union_branch_is_proved_without_a_definition_name_exception(name):
    previous = baseline('runtime-0.2.13')
    current = copy.deepcopy(previous)
    # An unrelated definition name must get the same explicit branch proof.
    previous['$defs']['ArbitraryReference'] = copy.deepcopy(previous['$defs'][name])
    current['$defs']['ArbitraryReference'] = copy.deepcopy(_SCHEMA['$defs'][name])
    assert compatibility_errors(previous, current) == []
    old = previous['$defs']['ArbitraryReference']['pattern']
    current['$defs']['ArbitraryReference']['pattern'] = (
        _SCHEMA['$defs'][name]['pattern'].removeprefix(f'(?:{old})|'))
    assert compatibility_errors(previous, current) == [
        '$/$defs/ArbitraryReference/pattern: narrowing or unsupported change; review required']


@pytest.mark.parametrize('name', REFERENCES)
@pytest.mark.parametrize('damage', ['old-branch', 'sibling', 'unknown'])
def test_current_union_cannot_hide_a_changed_old_branch_or_added_constraint(name, damage):
    current = copy.deepcopy(_SCHEMA)
    definition = current['$defs'][name]
    if damage == 'old-branch':
        old = baseline('runtime-0.2.13')['$defs'][name]['pattern']
        definition['pattern'] = definition['pattern'].replace(old, '^parent$', 1)
    elif damage == 'sibling':
        definition['maxLength'] = 1
    else:
        definition['unrecognizedValidationKeyword'] = None
    assert compatibility_errors(baseline('runtime-0.2.13'), current)


@pytest.mark.parametrize('value', [None, False, {'limit': 1}])
def test_unknown_keyword_addition_removal_or_change_always_requires_review(value):
    ordinary = baseline('runtime-0.2.13')
    changed = copy.deepcopy(ordinary)
    changed['$defs']['ID']['unrecognizedValidationKeyword'] = value
    assert compatibility_errors(ordinary, changed)
    assert compatibility_errors(changed, ordinary)
    other = copy.deepcopy(changed)
    other['$defs']['ID']['unrecognizedValidationKeyword'] = ['different']
    assert compatibility_errors(changed, other)


@pytest.mark.parametrize('ref', [
    'shot:raw shot:雪!@#', 'shot:raw shot:雪!@#/clip:clip::arbitrary',
    'parent/asset:asset::arbitrary', 'occurrence:occ::arbitrary',
    'occurrence:occ::arbitrary/track:track::arbitrary', 'cut:cut 雪!@#',
])
def test_arbitrary_published_ids_are_still_accepted(ref):
    for name in REFERENCES:
        value = ref + '::' if name == 'TargetKey' else ref
        for schema in (baseline('runtime-0.2.13'), _SCHEMA):
            Draft202012Validator(schema).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)


@pytest.mark.parametrize('shot,item', [
    ('source-shot', 'source-item'), ('shot:雪! @#', 'item:雪! @#'), ('123', '456'),
])
def test_new_typed_shot_item_refs_are_additive(shot, item):
    ref = f'shot:{shot}/item:{item}'
    for name in REFERENCES:
        value = ref + '::' if name == 'TargetKey' else ref
        with pytest.raises(ValidationError):
            Draft202012Validator(baseline('runtime-0.2.13')).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)
        Draft202012Validator(_SCHEMA).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)


@pytest.mark.parametrize('ref', [
    'shot:/item:item', 'shot:shot/item:', 'shot:shot/item:item/extra',
    'shot:shot/item:item::ambiguous', 'shot:shot::ambiguous/item:item',
])
def test_new_item_branch_retains_typed_id_and_scope_constraints(ref):
    for name in REFERENCES:
        value = ref + '::' if name == 'TargetKey' else ref
        with pytest.raises(ValidationError):
            Draft202012Validator(_SCHEMA).evolve(schema={'$ref': '#/$defs/' + name}).validate(value)
