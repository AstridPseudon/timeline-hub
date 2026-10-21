"""One source-only spike for the occurrence source-window trim boundary."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline._trim_commands import (
    _capture_clip_trim_v2,
    _record_clip_trim_v2,
    capture_clip_trim,
)
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_recipe_m2_clip_trim import REF, media_document
from tests.editing_conformance.test_recipe_occurrence_media import OWNER, TARGET, inputs


def _exclusive_bundle(kind='video'):
    """Keep the source recipe positive on one occurrence of the shared fixture."""
    bundle = bundle_from_document(inputs(kind)[0])
    bundle['placements'] = bundle['placements'][:1]
    return bundle


def _shared_bundle(kind='video'):
    """Make the canonical bundle's two occurrences share one shot identity."""
    bundle = bundle_from_document(inputs(kind)[0])
    bundle['placements'][1]['shot_id'] = bundle['placements'][0]['shot_id']
    return bundle


def _proposed_record(bundle, *, source_duration):
    """Record the proposed v2 writes without registering a production operation."""
    command = {
        'schema_version': 1,
        'op': 'clip.trim',
        'version': '2',
        'select': TARGET,
        'args': {'in_s': 3, 'out_s': 5},
        'intent': {},
    }
    recorder = Recording(bundle, command, 0)
    for field in ('id', 'clipType', 'asset', 'at', 'from', 'to', 'hold', 'speed', 'app'):
        recorder.read(TARGET, [field])
    recorder.select('collection.clips', OWNER)
    asset = recorder.read(TARGET, ['asset'])
    source = {
        key: recorder.read(OWNER + '/registry', ['assets', asset, key])
        for key in ('media_id', 'object_id', 'digest', 'content_digest', 'type')
    }
    source['duration_seconds'] = source_duration
    recorder.read(OWNER + '/source', ['source_window'])
    recorder.read('parent', ['config', 'output', 'fps'])
    recorder.read(OWNER + '/source', ['output', 'fps'])
    recorder.dependency('trim.source', 'entity', {
        'owner': OWNER,
        'asset': asset,
        'source': source,
    })
    recorder.bind('trim.target', TARGET, dependencies=['trim.source'])
    for key, value in (('from', 3), ('to', 5), ('hold', 2)):
        recorder.write(TARGET, [key], value)
    return recorder.finish(capture=True)


def test_occurrence_trim_gap_and_existing_recorder_source_footprint():
    parent_command = capture_clip_trim(bundle_from_document(media_document()), REF, in_s=1, out_s=5)
    assert parent_command['select'] == REF
    assert parent_command['version'] == '1'

    document, _old, _new, verified = inputs('video')
    bundle = bundle_from_document(document)

    # Existing occurrence.add-media already carries raw [from, to) and source-second hold;
    # it is the supported occurrence source-window carrier, but only for a birth.
    row = {
        'id': 'reserved-child', 'clipType': 'video', 'asset': 'reserved-new',
        'track': 'picture', 'at': .125, 'hold': 4, 'from': 2, 'to': 6, 'speed': 2,
        'params': None, 'opaque': [None, False, {}],
    }
    from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media

    add = capture_occurrence_add_media(bundle, OWNER, row, _new, verified_media=verified)
    assert add['select'] == OWNER
    assert (add['args']['row']['from'], add['args']['row']['to']) == (2, 6)
    assert add['args']['row']['hold'] == 4

    # Existing trim capture keeps its live parent-only positive and refuses the raw
    # occurrence child instead of inferring a display ID or silently remapping ownership.
    with pytest.raises(CommandError, match=r"does not match .*parent/clip"):
        capture_clip_trim(bundle, TARGET, in_s=3, out_s=5)

    before = copy.deepcopy(bundle)
    record = _proposed_record(copy.deepcopy(bundle), source_duration=verified[0]['duration_seconds'])
    writes = record['writes']
    assert [(write['ref'], write['path'], write['after']['value']) for write in writes] == [
        (TARGET, ['from'], 3), (TARGET, ['to'], 5), (TARGET, ['hold'], 2),
    ]
    assert all(write['ref'] != 'occurrence:occ-b/clip:clip-a' for write in writes)
    assert record['bindings'][-1] == {
        'key': 'trim.target', 'ref': TARGET, 'policy': 'fixed',
        'dependencies': ['trim.source'],
    }
    assert record['dependencies'][0]['key'] == 'trim.source'
    assert record['dependencies'][0]['pin']['owner'] == OWNER
    assert record['dependencies'][0]['pin']['asset'] == 'picture'
    assert record['dependencies'][0]['pin']['source']['media_id'].endswith('1' * 64)
    assert record['dependencies'][0]['pin']['source']['duration_seconds'] == 6
    assert bundle == before
    assert record['command']['select'] == TARGET
    assert record['command']['version'] == '2'


def test_dormant_v2_schema_keeps_v1_parent_boundary_and_is_not_registered():
    schema = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
    validator = Draft202012Validator(schema)
    command = {'schema_version': 1, 'op': 'clip.trim', 'version': '2', 'select': TARGET,
               'args': {'in_s': 3, 'out_s': 5}, 'intent': {}}
    validator.validate(command)
    assert list(validator.iter_errors({**command, 'version': '1'}))

    from astrid.sdk.timeline._trim_commands import clip_trim
    from astrid.sdk.timeline.commands import operations

    assert operations()['clip.trim'].handler is clip_trim


def test_dormant_occurrence_trim_writes_source_seconds_only_and_inverse_is_exact():
    _document, _old, _new, verified = inputs('video')
    original = _exclusive_bundle()
    State(original).entity(TARGET)['app'] = None
    original = copy.deepcopy(original)
    sibling = next(OWNER + '/clip:' + row['id'] for row in State(original).collection(OWNER, 'clip')
                   if OWNER + '/clip:' + row['id'] != TARGET)
    capture_input = copy.deepcopy(original)
    assert _capture_clip_trim_v2(capture_input, TARGET, in_s=3, out_s=5,
                                 verified_media=verified)['version'] == '2'
    assert capture_input == original
    candidate, record = _record_clip_trim_v2(copy.deepcopy(original), TARGET,
                                             in_s=3.0000004, out_s=5.0000004,
                                             verified_media=verified)
    assert [(write['ref'], write['path'], write['after']['value']) for write in record['writes']] == [
        (TARGET, ['from'], 3.0), (TARGET, ['to'], 5.0), (TARGET, ['hold'], 2.0),
    ]
    assert candidate['parent'] == original['parent']
    assert State(candidate).entity(sibling) == State(original).entity(sibling)
    assert inverse(candidate, [record]).bundle == original
    assert record['dependencies'][0]['pin']['source']['duration_seconds'] == 6.0
    assert record['command']['bindings']['trim.target'] == TARGET


def test_dormant_occurrence_trim_refuses_shared_owner_atomically():
    bundle = _shared_bundle()
    _document, _old, _new, verified = inputs('video')
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError) as error:
        _capture_clip_trim_v2(bundle, TARGET, in_s=3, out_s=5, verified_media=verified)
    assert error.value.kind == 'unsupported_ownership'
    assert error.value.ref == OWNER
    assert bundle == before


@pytest.mark.parametrize('damage', ['missing', 'wrong-object', 'wrong-type', 'source-map'])
def test_dormant_occurrence_trim_refuses_unverified_or_mapped_source_without_mutation(damage):
    _document, _old, _new, verified = inputs('video')
    bundle = _exclusive_bundle()
    if damage == 'missing':
        verified = []
    elif damage == 'wrong-object':
        verified[0]['selection']['object_id'] = 'sha256:' + '9' * 64
    elif damage == 'wrong-type':
        verified[0]['media_type'] = 'audio/fixture'
    else:
        bundle['placements'][0]['source_offset'] = 1
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        _capture_clip_trim_v2(bundle, TARGET, in_s=3, out_s=5, verified_media=verified)
    assert bundle == before
