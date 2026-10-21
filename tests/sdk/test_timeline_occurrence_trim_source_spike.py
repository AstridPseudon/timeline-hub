"""One source-only spike for the occurrence source-window trim boundary."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline._trim_commands import capture_clip_trim
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_m2_clip_trim import REF, media_document
from tests.editing_conformance.test_recipe_occurrence_media import OWNER, TARGET, inputs


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

    # The existing trim capture keeps its live parent-only positive and refuses the raw
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

    # The proposed source interval is half-open/source-seconds and does not mutate the input.
    assert bundle == before
    assert record['command']['select'] == TARGET
    assert record['command']['version'] == '2'
