"""The Runtime generator consumes the same closed args as the native registry."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from astrid.sdk.timeline._materialization import SOURCE_BOUND_OPERATIONS
from astrid.sdk.timeline.commands import _SCHEMA, operations


def fixture_commands(value):
    if isinstance(value, dict):
        if value.get('schema_version') == 1 and 'op' in value and 'args' in value:
            yield value
        for child in value.values():
            yield from fixture_commands(child)
    elif isinstance(value, list):
        for child in value:
            yield from fixture_commands(child)


def test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden():
    Draft202012Validator.check_schema(_SCHEMA)
    validator = Draft202012Validator(_SCHEMA)
    fixtures = Path(__file__).parents[1] / 'editing_conformance' / 'fixtures'
    commands = {command['op']: command for path in sorted(fixtures.glob('*.json'))
                for command in fixture_commands(json.loads(path.read_text()))}
    conditions = {condition['if']['properties']['op']['const']: condition['then'].get('anyOf', [condition['then']])[0]['properties']
                  for condition in _SCHEMA['$defs']['EditCommand']['allOf']}
    assert set(conditions) == set(operations()) | {'timeline.inverse', 'timeline.restore'}
    for op, operation in operations().items():
        ref = conditions[op]['args']['$ref'].removeprefix('#/$defs/')
        assert _SCHEMA['$defs'][ref] == operation.parameters
        assert operation.parameters['additionalProperties'] is False
        for version in (('1', '2') if op in SOURCE_BOUND_OPERATIONS else ('1',)):
            command = {**commands[op], 'version': version}
            validator.validate(command)
            unknown = copy.deepcopy(command)
            unknown['args']['unsupported_argument'] = None
            with pytest.raises(ValidationError):
                validator.validate(unknown)


@pytest.mark.parametrize('ref', ['shot:raw-shot', 'occurrence:raw-occurrence',
                                'parent/asset:alias', 'occurrence:raw-occurrence/asset:alias',
                                'shot:raw-shot/item:raw-item'])
def test_root_and_scoped_references_share_the_canonical_patterns(ref):
    for name in ('ScopedId', 'EntityRef', 'AnchorIdentity'):
        Draft202012Validator(_SCHEMA).evolve(
            schema={'$ref': '#/$defs/' + name}).validate(ref)
    Draft202012Validator(_SCHEMA).evolve(
        schema={'$ref': '#/$defs/TargetKey'}).validate(ref + '::')
