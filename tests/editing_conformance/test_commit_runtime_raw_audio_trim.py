"""Public Session trim probes only retained original-base audio over HTTP."""
from __future__ import annotations

import copy
import io
import wave

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.sync import TimelineSession
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.mark.parametrize('malformed', [False, True], ids=['wav', 'malformed'])
def test_public_raw_audio_trim_and_undo_without_authored_duration(
        tmp_path, real_runtime, malformed):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    audio = io.BytesIO()
    with wave.open(audio, 'wb') as output:
        output.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
        output.writeframes(b'\x00\x00' * 48000)
    data = b'synthetic-music-bed' if malformed else audio.getvalue()
    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({'slug': 'raw-trim', 'name': 'Raw trim'})['id']
        media = service.ingest(project, data, media_type='audio/wav',
            original_name='music.wav', idempotency_key='audio')['data']['object_id']
        clips = [{'id': 'music', 'track': 'music', 'clipType': 'audio', 'asset': 'music',
                  'at': 0, 'from': 0, 'to': 6, 'hold': 2, 'speed': 2,
                  'extension': {'opaque': [None, False]}}]
        parent = {'clips': clips, 'registry': {'assets': {'music': {
            'object_id': media, 'type': 'audio'}}}, 'occurrences': [],
            'config': {'clips': copy.deepcopy(clips), 'tracks': [{'id': 'music', 'kind': 'audio'}],
                       'output': {'fps': 30}}}
        service.publish_parent_composition(project, 'film', {
            'project_id': project, 'timeline_id': 'film', 'expected_head': None,
            'parent_revision_id': 'raw-baseline', 'parent_composition': parent,
            'dependency_manifest': {'media': [{'media_id': media, 'content_digest': media}]}},
            idempotency_key='raw-baseline')
    finally:
        service.close()

    daemon = real_runtime(root, support_root=tmp_path / 'support', authoring_profile='astrid')
    client = open_client(daemon)
    session = TimelineSession.open(project, 'film', client=client, outbox_path=tmp_path / 'outbox.json')
    transport = client._remote._transport
    original = transport.get_project_parent_composition_revision(project, 'film', 'raw-baseline')
    history = client.timelines.history(project, 'film', limit=100).data
    assert 'duration' not in original['payload']['registry']['assets']['music']
    bundle = session._bundle(session.outbox.read())
    assert '_runtime_document' not in bundle['source_mapping']
    assert client.media.read_bytes(media) == data
    persisted = session.outbox.path.read_bytes()

    if malformed:
        with pytest.raises(CommandError, match='exact Runtime-verified media metadata'):
            session.trim('parent/clip:music', in_s=1, out_s=4)
        assert session.outbox.path.read_bytes() == persisted
        assert client.timelines.history(project, 'film', limit=100).data == history
        assert transport.get_project_parent_composition_revision(project, 'film', 'raw-baseline') == original
        return

    accepted = session.trim('parent/clip:music', in_s=1, out_s=4)
    document = accepted['data']['canonical_document']
    row, = document['parent_revision']['payload']['clips']
    assert (row['from'], row['to'], row['hold'], row['speed']) == (1, 4, 3, 2)
    assert row['extension'] == {'opaque': [None, False]}
    assert 'duration' not in document['parent_revision']['payload']['registry']['assets']['music']
    command, = accepted['data']['commands']
    assert [read for read in command['reads'] if read['ref'] == 'media:' + media
            and read['path'] == ['duration_seconds']] == [{
                'ref': 'media:' + media, 'path': ['duration_seconds'],
                'state': {'state': 'present', 'value': 6},
            }]
    assert len(client.timelines.history(project, 'film', limit=100).data['items']) == len(history['items']) + 1
    assert transport.get_project_parent_composition_revision(project, 'film',
        accepted['data']['accepted_revision_id'])['payload'] == document['parent_revision']['payload']
    undone = session.undo([accepted['receipt']['receipt_id']])
    assert undone['data']['canonical_document']['parent_revision']['payload'] == original['payload']
    assert undone['data']['canonical_document']['dependency_manifest'] == original['dependency_manifest']
