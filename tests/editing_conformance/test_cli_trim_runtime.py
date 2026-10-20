"""Ordinary CLI literal edits through the pinned Runtime's real HTTP handlers and disk.

Uses the existing in-memory HTTP transport: no sockets or daemon substitute.
"""
from __future__ import annotations

import copy
import json

import pytest

from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.packs.timeline.cli import build_parser
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._trim_commands import capture_clip_trim
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.sync import TimelineSession
from tests.editing_conformance.test_native_batch_ingress import runtime  # noqa: F401

pytestmark = pytest.mark.integration
REF = 'parent/clip:literal'


def run(world, capsys, *args):
    parsed = build_parser(world.client()).parse_args([*args, '--project', world.project, '--json'])
    code = parsed.handler(parsed)
    output = capsys.readouterr()
    return code, json.loads(output.out)


@pytest.fixture
def film(runtime):  # noqa: F811
    client = runtime.client()
    imported = client.media.import_bytes(project=runtime.project, data=b'CLI trim fixture',
                                         filename='picture.png', media_type='image/png', idempotency_key='picture')
    assert imported.ok, imported.as_dict()
    media = imported.data['object_id']
    head = runtime.history()['head']
    opened = client.timelines.open_bundle(runtime.project, 'film', revision_id=head['revision_id'])
    assert opened.ok, opened.as_dict()
    parent = copy.deepcopy(opened.data['bundle']['parent'])
    parent['config'].update(output={'fps': 30}, tracks=[{'id': 'picture', 'kind': 'visual'}])
    parent['registry'] = {'assets': {'picture': {'media_id': media, 'type': 'image', 'duration': 10}}}
    parent['clips'] = [
        {'id': 'literal', 'track': 'picture', 'clipType': 'media', 'asset': 'picture',
         'at': 0, 'from': 1, 'to': 6, 'hold': 5, 'speed': 2,
         'app': {'astrid': {'for': 2.5, 'opaque': [None, False]}, 'extension': {'keep': True}}},
        {'id': 'title', 'track': 'picture', 'clipType': 'text', 'at': 5, 'hold': 1, 'params': {'text': 'Keep me'}},
    ]
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    client._remote._transport.publish_parent_composition(runtime.project, 'trim-film', {
        'project_id': runtime.project, 'timeline_id': 'trim-film', 'expected_head': None,
        'parent_revision_id': 'trim-baseline', 'parent_composition': parent,
    }, idempotency_key='trim-baseline')
    # A first legacy import on a new timeline is still the supported fixture
    # ingress. All subsequent edits below use the real native commit route.
    runtime.restart()  # Startup verifies and installs the initial import's baseline.
    runtime.history = lambda: client.timelines.history(runtime.project, 'trim-film', limit=100).data
    return runtime


@pytest.mark.parametrize('relevant_peer', [False, True], ids=['disjoint-rebase-undo', 'relevant-conflict'])
def test_cli_trim_exact_retry_restart_dependent_suffix_and_peer(film, tmp_path, capsys, relevant_peer):
    world = film
    client = world.client()
    session = TimelineSession.open(world.project, 'trim-film', client=client)
    original = session._bundle(session.outbox.read())
    expected_a = capture_clip_trim(original, REF, out_s=5.000001)
    args = ('edit', 'trim-film', '--clip', 'lit', '--trim-out', '5.000001', '--idempotency-key', 'cli-A')
    world.lost.add('cli-A')
    code, error = run(world, capsys, *args)
    assert code == 1 and not error['ok']
    first = copy.deepcopy(world.calls[-1])
    flight = json.loads(session.outbox.path.read_bytes())['flight']
    assert (flight['body'].encode(), flight['key']) == first[:2]
    assert json.loads(first[0])['commands'] == [expected_a]
    accepted_a = first[3]
    document_a = accepted_a['data']['canonical_document']
    actual_a = State(bundle_from_document(document_a)).entity(REF)
    assert actual_a == State(execute(original, [expected_a]).bundle).entity(REF)
    assert actual_a['to'] <= 5.000001
    b = session.queue({'schema_version': 1, 'op': 'clip.trim', 'version': '1',
                       'select': REF, 'args': {'in_s': None, 'out_s': 4}})
    assert b == capture_clip_trim(bundle_from_document(document_a), REF, out_s=4)
    assert json.loads(session.outbox.path.read_bytes())['pending'] == [expected_a, b]
    peer = TimelineSession.open(world.project, 'trim-film', client=client, outbox_path=tmp_path / 'peer.json')
    if relevant_peer:
        peer.trim(REF, out_s=3)
    else:
        peer.commit({'schema_version': 1, 'op': 'track.set', 'version': '1',
                     'select': 'parent/track:picture', 'args': {'values': {'label': 'Peer'}, 'clear': []}})
    history_before = copy.deepcopy(world.history())
    world.restart()
    code, retried = run(world, capsys, *args)
    assert code == 0 and retried['receipt'] == accepted_a['receipt']
    assert world.calls[-1][:2] == first[:2]
    assert world.calls[-1][3] == first[3]
    assert world.history() == history_before
    client = world.client()
    opened = client.timelines.open_bundle(world.project, 'trim-film', revision_id=document_a['parent_revision']['revision_id'])
    assert opened.ok and opened.data['bundle'] == open_authoring_bundle(
        {**document_a['parent_revision'], 'project_id': world.project, 'timeline_id': 'trim-film'},
        shot_revisions=document_a['shot_revisions'],
        internal_timeline_revisions=document_a['internal_timeline_revisions'])
    stored = client._remote._transport.get_project_parent_composition_revision(
        world.project, 'trim-film', document_a['parent_revision']['revision_id'])
    assert all(stored[key] == value for key, value in document_a['parent_revision'].items())
    assert stored['dependency_manifest'] == document_a['dependency_manifest']
    pending = json.loads(session.outbox.path.read_bytes())
    assert pending['pending'] == [b] and pending['flight'] is None
    assert pending['base'] == {'revision_id': accepted_a['data']['accepted_revision_id'],
                               'publication_id': accepted_a['receipt']['receipt_id']}
    code, result = run(world, capsys, 'edit', 'trim-film', '--clip', 'literal', '--trim-out', '4')
    assert json.loads(world.calls[-1][0])['commands'] == [b]
    assert world.calls[-1][1] != first[1]
    if relevant_peer:
        assert code == 1 and not result['ok']
        refused = json.loads(session.outbox.path.read_bytes())
        assert refused['pending'] == [b] and refused['conflict']['details']['status'] == 'conflict'
        assert world.history() == history_before
    else:
        assert code == 0 and result['data']['status'] == 'rebased'
        bundle_b = bundle_from_document(result['data']['canonical_document'])
        assert State(bundle_b).entity(REF)['to'] == 4
        assert State(bundle_b).entity('parent/track:picture')['label'] == 'Peer'
        assert State(bundle_b).entity('parent/clip:title') == State(original).entity('parent/clip:title')
        code, undone = run(world, capsys, 'undo', 'trim-film', '--publication', result['receipt']['receipt_id'])
        assert code == 0
        undone_bundle = bundle_from_document(undone['data']['canonical_document'])
        assert State(undone_bundle).entity(REF) == actual_a
        assert State(undone_bundle).entity('parent/track:picture')['label'] == 'Peer'


def test_cli_move_exact_retry_restart_and_undo_over_real_http(film, capsys):
    world = film
    session = TimelineSession.open(world.project, 'trim-film', client=world.client())
    original = session._bundle(session.outbox.read())
    expected = capture_move(original, REF, 3)
    args = ('edit', 'trim-film', '--clip', 'lit', '--on', '3', '--idempotency-key', 'cli-move-A')

    world.lost.add('cli-move-A')
    code, failure = run(world, capsys, *args)
    assert code == 1 and not failure['ok']
    first = copy.deepcopy(world.calls[-1])
    flight = json.loads(session.outbox.path.read_bytes())['flight']
    assert (flight['body'].encode(), flight['key']) == first[:2]
    assert json.loads(first[0])['commands'] == [expected]
    accepted = first[3]
    history_after_accept = copy.deepcopy(world.history())

    world.restart()
    code, retry = run(world, capsys, *args)
    assert code == 0 and retry['receipt'] == accepted['receipt']
    assert world.calls[-1][:2] == first[:2]
    assert world.calls[-1][3] == accepted
    assert world.history() == history_after_accept

    code, undone = run(world, capsys, 'undo', 'trim-film',
                       '--publication', accepted['receipt']['receipt_id'])
    assert code == 0
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert State(restored).entity(REF) == State(original).entity(REF)
