"""The Runtime generator consumes the same closed args as the native registry."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

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
    commands.update({
        'timeline.migrate-groups': {
            'schema_version': 1, 'op': 'timeline.migrate-groups', 'version': '1',
            'select': 'parent', 'args': {'groups': [
                {'legacy_shot_id': 'legacy', 'shot_id': 'shot', 'occurrence_id': 'occ'}]},
        },
        'occurrence.move': {
            'schema_version': 1, 'op': 'occurrence.move', 'version': '1',
            'select': 'occurrence:occ', 'args': {
                'on': 1, 'track': 'parent/track:V1',
                'child_track': 'occurrence:occ/track:V1'},
        },
        'occurrence.resize': {
            'schema_version': 1, 'op': 'occurrence.resize', 'version': '1',
            'select': 'occurrence:occ', 'args': {'duration_ms': 1000},
        },
        'project-data.write': {
            'schema_version': 1, 'op': 'project-data.write', 'version': '1',
            'select': 'parent', 'args': {
                'target': 'example', 'key': 'value', 'value': None, 'mode': 'replace'},
        },
        'timeline.reference': {
            'schema_version': 1, 'op': 'timeline.reference', 'version': '1',
            'select': 'parent', 'args': {
                'reference_id': 'exact-reference', 'role': 'source', 'media': {
                    'media_id': 'sha256:' + 'a' * 64,
                    'content_digest': 'sha256:' + 'a' * 64,
                }},
        },
        'track.reorder': {
            'schema_version': 1, 'op': 'track.reorder', 'version': '1',
            'select': 'parent', 'args': {
                'order': ['parent/track:overlay', 'parent/track:picture'],
                'expected_order': ['parent/track:picture', 'parent/track:overlay']},
        },
        'transcript.associate': {
            'schema_version': 1, 'op': 'transcript.associate', 'version': '1',
            'select': 'parent/asset:asset-a', 'args': {
                'asset_id': 'asset-a',
                'media_id': 'sha256:' + 'a' * 64,
                'source_id': 'source-1',
                'document': {
                    'document_id': 'transcript:sample', 'version': 1,
                    'content_digest': 'sha256:' + 'b' * 64,
                },
                'previous_document': None,
                'source_schema_ref': 'astrid.transcript_segment/v1',
            },
        },
    })
    conditions = {condition['if']['properties']['op']['const']: condition['then']
                  for condition in _SCHEMA['$defs']['EditCommand']['allOf']}
    for op, operation in operations().items():
        branches = conditions[op].get('anyOf', [conditions[op]])
        for branch in branches:
            if op in {'clip.swap-media', 'occurrence.swap-media'}:
                assert branch['properties']['args'] in (
                    {'$ref': '#/$defs/OccurrenceSwapMediaArgs'},
                    {'$ref': '#/$defs/RawOldSwapMediaArgs'},
                )
            else:
                assert branch['properties']['args'] == branches[0]['properties']['args']
            version = branch['properties'].get('version', {}).get('const', '1')
            sample = copy.deepcopy(commands[op])
            if branch['properties']['args'].get('$ref') == '#/$defs/RawOldSwapMediaArgs':
                sample['args']['old_media'] = {
                    'media_id': 'sha256:' + 'a' * 64,
                    'content_digest': 'sha256:' + 'a' * 64,
                }
            validator.validate({**sample, 'version': version})
            unknown = copy.deepcopy(sample)
            unknown['version'] = version
            unknown['args']['unsupported_argument'] = None
            with pytest.raises(ValidationError):
                validator.validate(unknown)
        ref = branches[0]['properties']['args']['$ref'].removeprefix('#/$defs/')
        assert _SCHEMA['$defs'][ref] == operation.parameters
        assert operation.parameters['additionalProperties'] is False
        validator.validate(commands[op])
        unknown = copy.deepcopy(commands[op])
        unknown['args']['unsupported_argument'] = None
        with pytest.raises(ValidationError):
            validator.validate(unknown)


@pytest.mark.parametrize('ref', ['shot:raw-shot', 'occurrence:raw-occurrence',
                                'parent/asset:alias', 'occurrence:raw-occurrence/asset:alias'])
def test_root_and_scoped_asset_references_share_the_canonical_patterns(ref):
    for name in ('ScopedId', 'EntityRef', 'AnchorIdentity'):
        Draft202012Validator(_SCHEMA).evolve(
            schema={'$ref': '#/$defs/' + name}).validate(ref)
    Draft202012Validator(_SCHEMA).evolve(
        schema={'$ref': '#/$defs/TargetKey'}).validate(ref + '::')
