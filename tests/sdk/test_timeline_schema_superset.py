"""Published canonical command schemas never lose existing definitions or operations."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline.commands import _SCHEMA
from tests.sdk.command_schema_compatibility import compatibility_errors

FIXTURES = Path(__file__).parents[1] / 'fixtures' / 'published-command-schemas'


def baseline(name='runtime-0.2.3'):
    filename = name + '.json'
    source = json.loads((FIXTURES / 'sources.json').read_text())[filename]
    raw = (FIXTURES / filename).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source['sha256'], source
    return json.loads(raw)


def test_current_canonical_schema_preserves_latest_ordinary_publication():
    assert compatibility_errors(baseline('runtime-0.2.13'), _SCHEMA) == []


@pytest.mark.parametrize('name', ['runtime-0.2.2', 'runtime-0.2.3'])
def test_exact_unchanged_published_artifacts_pass(name):
    assert compatibility_errors(baseline(name), baseline(name)) == []


def test_withdrawn_exact_10c_schema_reports_every_lost_definition_and_operation():
    errors = compatibility_errors(baseline(), baseline('withdrawn-10c'))
    assert {e.split('/')[2].split(':')[0] for e in errors if ': missing definition' in e} == {
        'ClipSetArgs', 'ClipSplitArgs', 'ClipTrimArgs', 'DocumentPin', 'MediaSelection',
        'OccurrenceAddMediaArgs', 'OccurrenceSwapMediaArgs', 'TrackCreateArgs'}
    assert {e.split('/allOf/')[1].split(':')[0] for e in errors
            if ': missing supported operation' in e} == {
        'occurrence.add-media', 'occurrence.swap-media', 'placement.move', 'track.create',
        'clip.set', 'clip.trim', 'clip.split'}
    assert any('/properties/schema_source' in e for e in errors)
    assert any('/ScopedId/pattern' in e for e in errors)


@pytest.mark.parametrize(('definition', 'path', 'value'), [
    ('ClipMoveArgs', ('required',), ['on', 'new_required_argument']),
    ('Intent', ('properties', 'ownership', 'enum'), ['occurrence']),
    ('ClipAddArgs', ('properties', 'row', 'properties', 'hold', 'exclusiveMinimum'), 1),
    ('ID', ('minLength',), 2),
    ('ScopedId', ('pattern',), '^parent$'),
    ('ClipMoveArgs', ('properties', 'on', 'type'), 'integer'),
    ('ClipMoveArgs', ('properties', 'on', 'maximum'), 1),
    ('ID', ('pattern',), '^x$'),
    ('ClipAddArgs', ('properties', 'row', 'additionalProperties'), False),
    ('ID', ('unrecognizedValidationKeyword',), 1),
    ('AgentState', ('oneOf',), [{'type': 'null'}]),
])
def test_narrowing_or_unsupported_changes_fail(definition, path, value):
    current = baseline()
    node = current['$defs'][definition]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    assert compatibility_errors(baseline(), current)


@pytest.mark.parametrize('drop', ['definition', 'clip.delete', 'timeline.inverse',
                                'timeline.restore', 'property'])
def test_dropping_published_structure_fails(drop):
    current = baseline()
    if drop == 'definition':
        del current['$defs']['TrackSetArgs']
    elif drop != 'property':
        current['$defs']['EditCommand']['allOf'] = [
            c for c in current['$defs']['EditCommand']['allOf']
            if c['if']['properties']['op']['const'] != drop]
    else:
        del current['$defs']['ClipSetParamsArgs']['properties']['schema_source']
    assert compatibility_errors(baseline(), current)


@pytest.mark.parametrize('name', ['ScopedId', 'EntityRef', 'TargetKey', 'AnchorIdentity'])
def test_materialization_regex_requires_the_full_old_pattern_as_an_alternative(name):
    current = baseline()
    old = current['$defs'][name]['pattern']
    new = baseline('withdrawn-10c')['$defs'][name]['pattern']
    current['$defs'][name]['pattern'] = f'(?:{old})|(?:{new})'
    assert compatibility_errors(baseline(), current) == []
    current['$defs'][name]['pattern'] = baseline('withdrawn-10c')['$defs'][name]['pattern']
    assert compatibility_errors(baseline(), current)


def test_new_refs_and_union_require_a_structurally_retained_old_branch():
    current = baseline()
    current['$defs']['MoreMoveArgs'] = {'anyOf': [
        {'$ref': '#/$defs/ClipMoveArgs'}, {'type': 'object'}]}
    condition = next(c for c in current['$defs']['EditCommand']['allOf']
                     if c['if']['properties']['op']['const'] == 'clip.move')
    condition['then']['properties']['args'] = {'$ref': '#/$defs/MoreMoveArgs'}
    assert compatibility_errors(baseline(), current) == []
    current['$defs']['MoreMoveArgs']['anyOf'] = [{'type': 'object'}, {'type': 'null'}]
    assert compatibility_errors(baseline(), current)  # Retain the actual old branch.


def test_new_definitions_and_operations_are_allowed_but_not_new_constraints_on_old_operations():
    current = baseline()
    current['$defs']['NewArgs'] = {'type': 'object'}
    condition = copy.deepcopy(current['$defs']['EditCommand']['allOf'][0])
    condition['if']['properties']['op']['const'] = 'new.operation'
    condition['then']['properties']['args'] = {'$ref': '#/$defs/NewArgs'}
    current['$defs']['EditCommand']['allOf'].append(condition)
    assert compatibility_errors(baseline(), current) == []
    condition['if']['properties']['op']['const'] = 'clip.move'
    assert compatibility_errors(baseline(), current)  # Duplicate condition can narrow an old op.


def test_widening_required_enum_ranges_and_property_schemas_is_allowed():
    current = baseline()
    current['$defs']['ClipMoveArgs']['required'] = []
    current['$defs']['Intent']['properties']['ownership']['enum'].append('new-owner')
    current['$defs']['ClipMoveArgs']['properties']['on']['minimum'] = -1
    current['$defs']['ClipMoveArgs']['additionalProperties'] = True
    current['$defs']['ClipMoveArgs']['properties']['new_optional'] = {'type': 'string'}
    assert compatibility_errors(baseline(), current) == []


def test_union_cannot_hide_sibling_constraints_and_unknown_changes_require_review():
    current = baseline()
    current['$defs']['ID'] = {'anyOf': [baseline()['$defs']['ID'], {'type': 'null'}],
                             'maxLength': 1}
    assert compatibility_errors(baseline(), current)
    previous = baseline()
    previous['$defs']['ID']['unrecognizedValidationKeyword'] = 1
    assert compatibility_errors(previous, baseline())


def test_equivalent_refs_pass_but_unproductive_ref_cycles_require_review():
    current = baseline()
    current['$defs']['Alias'] = copy.deepcopy(current['$defs']['ClipMoveArgs'])
    current['$defs']['ClipMoveArgs'] = {'$ref': '#/$defs/Alias'}
    assert compatibility_errors(baseline(), current) == []
    current['$defs']['Alias'] = {'$ref': '#/$defs/Alias'}
    assert compatibility_errors(baseline(), current)


@pytest.mark.parametrize('replacement', [True, {'type': 'object'}])
def test_widening_the_envelope_does_not_preserve_supported_operations(replacement):
    current = baseline()
    current['$defs']['EditCommand'] = replacement
    errors = compatibility_errors(baseline(), current)
    assert sum(': missing supported operation' in e for e in errors) == 14


def test_an_unconstrained_root_does_not_preserve_published_definitions():
    errors = compatibility_errors(baseline(), True)
    assert sum(': missing definition' in e for e in errors) == 35
