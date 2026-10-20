"""The word successor preserves complete frozen S2 and earlier command floors."""
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
    'agent-frozen-s2-26ef2bbb': 'a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef',
    'agent-word-caea687e': 'a058aa6ec55d86f84b74360f4e9c01d207ec1db86434170c5d5658b5c809130a',
    'agent-current-c456b328': '40ce6d81487f39236fbfb3adf13e6e0c3f43cfcc375b39b7badc32d65531fd4b',
    'agent-current-df2739f9': '83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224',
    'agent-frozen-s1-0a0ac7ba': '30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd',
    'runtime-0.2.10-6023cfb': '472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9',
}


def baseline(name):
    raw = (FIXTURES / (name + '.json')).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCES[name]
    return json.loads(raw)


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
    candidate = without_word_slice()
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
    candidate = without_word_slice()
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
    assert len(candidate['$defs']) == 48
    assert len(candidate['$defs']['EditCommand']['allOf']) == 22


@pytest.mark.parametrize('name', SOURCES)
def test_existing_argument_narrowing_still_fails(name):
    candidate = copy.deepcopy(_SCHEMA)
    candidate['$defs']['ClipMoveArgs']['properties']['on']['type'] = 'integer'
    assert compatibility_errors(baseline(name), candidate)


def without_word_slice():
    candidate = copy.deepcopy(_SCHEMA)
    for definition in ('WordAnchor', 'ClipAnchorArgs'):
        del candidate['$defs'][definition]
    candidate['$defs']['EditCommand']['allOf'] = [
        item for item in candidate['$defs']['EditCommand']['allOf']
        if item['if']['properties']['op']['const'] != 'clip.anchor']
    return candidate


def test_word_successor_is_exactly_complete_frozen_s2_plus_word_types_and_operation():
    assert without_word_slice() == baseline('agent-frozen-s2-26ef2bbb')
    assert len(_SCHEMA['$defs']) == 50
    assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 23
