"""The text successor preserves complete S2 and the published schema floors."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline.commands import _SCHEMA
from tests.sdk.command_schema_compatibility import compatibility_errors

FIXTURES = Path(__file__).parents[1] / 'fixtures' / 'current-union-command-schemas'
SOURCES = {
    'runtime-0.2.9-94114269': '472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9',
    'agent-current-c456b328': '40ce6d81487f39236fbfb3adf13e6e0c3f43cfcc375b39b7badc32d65531fd4b',
    'agent-current-df2739f9': '83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224',
    'agent-frozen-s1-0a0ac7ba': '30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd',
    'runtime-0.2.10-6023cfb': '472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9',
}


def baseline(name):
    raw = (FIXTURES / (name + '.json')).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCES[name]
    return json.loads(raw)


def without_text(schema):
    candidate = copy.deepcopy(schema)
    for name in ('ScopedId', 'EntityRef', 'TargetKey'):
        branches = candidate['$defs'][name]['anyOf']
        assert len(branches) == 3
        legacy = json.loads((FIXTURES / 'runtime-0.2.2-6be97063.json').read_text())
        assert branches[0] == legacy['$defs'][name]
        candidate['$defs'][name] = branches[1]
    del candidate['$defs']['TextBindingSetArgs']
    conditions = candidate['$defs']['EditCommand']['allOf']
    assert len([item for item in conditions if item['if']['properties']['op']['const'] == 'text-binding.set']) == 1
    candidate['$defs']['EditCommand']['allOf'] = [
        item for item in conditions if item['if']['properties']['op']['const'] != 'text-binding.set']
    return candidate


@pytest.mark.parametrize('name', SOURCES)
def test_full_current_candidate_preserves_every_definition_and_registered_operation(name):
    assert compatibility_errors(baseline(name), _SCHEMA) == []


@pytest.mark.parametrize('name', SOURCES)
def test_every_dropped_definition_is_reported_even_when_not_referenced(name):
    previous = baseline(name)
    for definition in previous['$defs']:
        candidate = copy.deepcopy(_SCHEMA)
        del candidate['$defs'][definition]
        assert f'$/$defs/{definition}: missing definition' in compatibility_errors(previous, candidate)


@pytest.mark.parametrize('name', SOURCES)
def test_every_dropped_operation_is_reported_despite_the_open_generic_envelope(name):
    previous = baseline(name)
    for condition in previous['$defs']['EditCommand']['allOf']:
        op = condition['if']['properties']['op']['const']
        candidate = copy.deepcopy(_SCHEMA)
        candidate['$defs']['EditCommand']['allOf'] = [
            item for item in candidate['$defs']['EditCommand']['allOf']
            if item['if']['properties']['op']['const'] != op]
        assert (f'$/$defs/EditCommand/allOf/{op}: missing supported operation'
                in compatibility_errors(previous, candidate))


def test_only_reviewed_producer_and_consumed_additions_change_current_schema():
    previous = baseline('agent-current-c456b328')
    candidate = without_text(_SCHEMA)
    for definition in ('ProducerAdmittedTarget', 'ProducerIdentity', 'ProducerAttemptPin',
                       'ProducerGuardArgs', 'SettledProducerProposal'):
        del candidate['$defs'][definition]
    candidate['$defs']['EditCommand']['allOf'] = [
        item for item in candidate['$defs']['EditCommand']['allOf']
        if item['if']['properties']['op']['const'] != 'producer.guard']
    for definition in ('OccurrenceAddMediaArgs', 'PlacementCreateArgs'):
        del candidate['$defs'][definition]['properties']['consumed']
    candidate['$defs']['ClipSetElementArgs'] = previous['$defs']['ClipSetElementArgs']
    assert candidate == previous


def test_s2_only_adds_the_reviewed_optional_element_source_to_frozen_s1():
    previous = baseline('agent-frozen-s1-0a0ac7ba')
    candidate = without_text(_SCHEMA)
    assert len(candidate['$defs']) == 48
    assert len(candidate['$defs']['EditCommand']['allOf']) == 22
    element = candidate['$defs']['ClipSetElementArgs']
    assert element['properties'].pop('schema_source') == {'$ref': '#/$defs/DocumentPin'}
    assert element['required'] == ['elementRef'] and element['additionalProperties'] is False
    assert element['description'] == (
        'Replace an existing clip elementRef with another revision of the same element id, '
        'kind and selected pack owner. Admitted revisions require the exact retained '
        'schema_source declaration pin. The retired element_ref alias is removed. '
        'There is no clear: a clip keeps its element.')
    element['description'] = previous['$defs']['ClipSetElementArgs']['description']
    assert candidate == previous
    assert len(_SCHEMA['$defs']) == 49
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 23


@pytest.mark.parametrize('name', SOURCES)
def test_existing_argument_narrowing_still_fails(name):
    candidate = copy.deepcopy(_SCHEMA)
    candidate['$defs']['ClipMoveArgs']['properties']['on']['type'] = 'integer'
    assert compatibility_errors(baseline(name), candidate)


def test_text_delta_preserves_complete_approved_s2():
    raw = json.dumps(without_text(_SCHEMA), sort_keys=True).encode()
    assert hashlib.sha256(raw).hexdigest() == (
        'f2d4d026a8605ed312fd48b6d6eaa9c14f03168c669c729501a728df5c4e4d07')


def test_all_published_floors_preserve_every_field_with_only_historical_pattern_widening():
    sources = json.loads((FIXTURES / 'published-sources.json').read_text())
    assert set(sources) == {'0.2.1', '0.2.2', '0.2.3', '0.2.8', '0.2.9', '0.2.10'}
    for version, source in sources.items():
        raw = (FIXTURES / source['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
        previous, candidate = json.loads(raw), without_text(_SCHEMA)
        if version in ('0.2.1', '0.2.2'):
            # The conservative checker cannot prove regex inclusion. Verify
            # these exact additive alternatives, then check every other field.
            for definition in ('AnchorIdentity', 'EntityRef', 'ScopedId', 'TargetKey'):
                old = previous['$defs'][definition]['pattern']
                widened = old.replace('(?:clip|track)', '(?:clip|track|asset)').replace(
                    '|occurrence:[^/]+(?:/shot)?|cut:',
                    '|shot:(?:(?!::)[^/])+|occurrence:[^/]+(?:/shot)?|cut:')
                assert candidate['$defs'][definition]['pattern'] == widened
                candidate['$defs'][definition]['pattern'] = old
            if version == '0.2.2':
                old = next(item for item in previous['$defs']['EditCommand']['allOf']
                           if item['if']['properties']['op']['const'] == 'track.set')
                new = next(item for item in candidate['$defs']['EditCommand']['allOf']
                           if item['if']['properties']['op']['const'] == 'track.set')
                pattern = old['then']['properties']['select']['pattern']
                assert new['then']['properties']['select']['pattern'] == pattern.replace(
                    'parent/track:', '(?:parent|occurrence:[^/]+)/track:')
                new['then']['properties']['select']['pattern'] = pattern
        assert compatibility_errors(previous, candidate) == [], version
