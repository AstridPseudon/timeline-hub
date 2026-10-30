"""S6: packet verdicts must agree with the production commit provider.

The detached cases exercise the five existing recipe families without sockets.
The HTTP case uses editing_case and is run by the central integration service.
"""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import ABSENT, present
from astrid.sdk.timeline._shot_commands import capture_shot_set
from astrid.sdk.timeline.capture import capture_clip_delete
from astrid.sdk.timeline.clash import classify
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from tests.editing_conformance.test_doc_patch_v2 import change, patch
from tests.sdk.test_timeline_clash import ClassifierSession, request
from tests.sdk.test_timeline_commit_provider import DetachedRealm
from tests.sdk.test_timeline_commit_provider_document import document_fixture


@pytest.fixture(autouse=True)
def provider_abi(request, monkeypatch):
    if request.node.get_closest_marker('integration') is None:
        from tests.sdk.test_timeline_commit_provider import runtime_abi

        runtime_abi.__wrapped__(monkeypatch)


def scenario(family, concurrent):
    if family == 'doc.patch':
        realm = DetachedRealm()
        ours = patch(change(['name'], present('Renamed Film'), 'Ours'))
        peer = patch(change(['name'], present('Renamed Film'), 'Theirs'))
    elif family == 'shot.set':
        realm = DetachedRealm(document_fixture(shared=False))
        bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
        ours = capture_shot_set(bundle, 'occurrence:occ-a/shot', values={'name': 'Ours'})
        peer = capture_shot_set(bundle, 'occurrence:occ-a/shot', values={'name': 'Theirs'})
    elif family == 'clip.delete':
        from tests.editing_conformance.test_recipe_clip_delete import delete_document

        realm = DetachedRealm(delete_document())
        bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
        ours = capture_clip_delete(bundle, 'parent/clip:clip-b')
        peer = patch(change(['clips', 'id:clip-b', 'hold'], present(2), 3))
    elif family == 'parent.media':
        from tests.editing_conformance.test_recipe_m2_parent_media import captured
        from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm

        document, _, ours, verified = captured()
        realm = MediaRealm(document, verified)
        # The same stable identity cannot be born twice, even with equal bytes.
        peer = copy.deepcopy(ours)
    else:
        from astrid.sdk.timeline._command_state import State
        from astrid.sdk.timeline.native_auto_placement import auto_place_completion
        from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs

        document, _, media, verified = inputs('image')
        document['parent_revision']['payload']['occurrences'] = document['parent_revision']['payload']['occurrences'][:1]
        document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
        realm = MediaRealm(document, verified)
        bundle = bundle_from_document(document)
        result = auto_place_completion(bundle, 'occurrence:occ-a', 'placed', media,
                                       ownership='occurrence', verified_media=verified,
                                       anchor='clip-a', duration=1)
        ours, = result['commands']
        original = State(bundle).entity('occurrence:occ-a/clip:clip-a')['at']
        peer = patch(change(['clips', 'id:clip-a', 'at'], present(original), original + 1,
                            ref='internal:chapter-1'))
    if concurrent == 'disjoint':
        peer = patch(change(['unknown', 'peer'], ABSENT, True))
    return realm, [ours], [peer]


def assert_matches_provider(realm, base, ours):
    session = ClassifierSession(realm)
    original = request(base, ours)
    packet = classify(session, original)
    assert packet['classified'], packet
    fields = {**original, 'merge': 'fields', 'reads': [], 'dry_run': True}
    result = session.commit('project-1', 'film', fields, idempotency_key='differential-probe')
    all_apply = all(row['verdict'] == 'applies' for row in packet['commands'])
    assert all_apply == result.ok
    if result.ok:
        other = ClassifierSession(copy.deepcopy(realm))
        merged = session.commit('project-1', 'film', {**fields, 'dry_run': False},
                                idempotency_key='merged')
        rebased_body = {**fields, 'dry_run': False,
                        'base_revision_id': packet['head']['revision_id'],
                        'base_publication_id': packet['head']['publication_id']}
        rebased = other.commit('project-1', 'film', rebased_body, idempotency_key='rebased')
        assert merged.ok and rebased.ok, (merged.as_dict(), rebased.as_dict())
        assert merged.data['canonical_document'] == rebased.data['canonical_document']
    else:
        expected = result.error.details['conflicts'][0]
        row = next(row for row in packet['commands'] if row['verdict'] in ('overlaps', 'target_missing'))
        if row['verdict'] == 'overlaps':
            overlap, = row['overlaps']
            assert (overlap['ref'], overlap['path']) == (expected['ref'], expected['path'])
        else:
            assert row['verdict'] == 'target_missing'
            assert row['ref'] == expected['ref']
    return packet


@pytest.mark.parametrize('family', ['doc.patch', 'shot.set', 'clip.delete', 'parent.media', 'auto.placement'])
@pytest.mark.parametrize('concurrent', ['disjoint', 'overlap'])
def test_rebase_verdicts_match_provider(family, concurrent):
    realm, ours, peer = scenario(family, concurrent)
    base = copy.deepcopy(realm.head)
    realm.call(peer)
    packet = assert_matches_provider(realm, base, ours)
    assert (packet['commands'][0]['verdict'] == 'applies') == (concurrent == 'disjoint')


@pytest.mark.parametrize('ours_op', ['list.move', 'list.remove', 'field'])
@pytest.mark.parametrize('peer_op', ['list.move', 'list.remove', 'field', 'equal', 'sibling'])
def test_patch_collection_order_membership_and_field_sites(ours_op, peer_op):
    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    row = realm.documents[base['revision_id']]['parent_revision']['payload']['clips'][1]

    def call(operation, value):
        if operation in ('field', 'equal', 'sibling'):
            identity = 'clip-a' if operation == 'sibling' else 'clip-b'
            return patch(change(['clips', 'id:' + identity, 'hold'], present(2),
                                2 if operation == 'equal' else value))
        extra = {'after_id': None} if operation == 'list.move' else {}
        return patch(change(['clips'], present(row), op=operation, id='clip-b',
                            order_before=['clip-a', 'clip-b'], **extra))

    ours = [call(ours_op, 3)]
    realm.call([call(peer_op, 4)])
    assert_matches_provider(realm, base, ours)


@pytest.mark.parametrize('kind', ['image', 'video'])
@pytest.mark.parametrize('replace', [False, True])
@pytest.mark.parametrize('peer', ['disjoint', 'same_identity'])
def test_parent_media_birth_and_replacement_authority(kind, replace, peer):
    from astrid.sdk.timeline.native_parent_media_commands import capture_clip_replace_media
    from tests.editing_conformance.test_recipe_m2_parent_media import (
        args,
        calls,
        capture,
        parent_inputs,
    )
    from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm

    document, _, media, verified = parent_inputs(kind)
    bundle = bundle_from_document(document)
    value = args(media, kind)
    command = (capture_clip_replace_media(bundle, 'parent/clip:ov-a', value['row'], media,
                                          verified_media=verified) if replace
               else capture(bundle, value, verified))
    realm = MediaRealm(document, verified)
    base = copy.deepcopy(realm.head)
    realm.call(calls(command) if peer == 'same_identity' else [patch(change(['unknown', 'peer'], ABSENT, True))])
    assert_matches_provider(realm, base, calls(command))


@pytest.mark.parametrize('kind', ['image', 'video'])
@pytest.mark.parametrize('anchor', ['clip-a', None])
@pytest.mark.parametrize('peer', ['anchor_move', 'lane_move', 'unrelated', 'anchor_delete'])
def test_auto_placement_consumed_timing_and_selection(kind, anchor, peer):
    from astrid.sdk.timeline.native_auto_placement import auto_place_completion
    from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs

    document, _, media, verified = inputs(kind)
    payload = document['parent_revision']['payload']
    payload['occurrences'] = payload['occurrences'][:1]
    payload['occurrences'][0]['duration_ms'] = 20000
    document['parent_revision']['content_digest'] = _digest(payload)
    bundle = bundle_from_document(document)
    ours = auto_place_completion(bundle, 'occurrence:occ-a', 'placed', media,
                                ownership='occurrence', verified_media=verified,
                                anchor=anchor, duration=1)['commands']
    realm = MediaRealm(document, verified)
    base = copy.deepcopy(realm.head)
    rows = document['internal_timeline_revisions'][0]['payload']['clips']
    if peer == 'unrelated':
        command = patch(change(['unknown', 'peer'], ABSENT, True))
    elif peer == 'anchor_delete':
        command = patch(change(['clips'], present(rows[0]), op='list.remove', id='clip-a',
                               order_before=['clip-a', 'clip-b'], ref='internal:chapter-1'))
    else:
        row = rows[1] if peer == 'lane_move' else rows[0]
        command = patch(change(['clips', 'id:' + row['id'], 'at'], present(row['at']), row['at'] + 1,
                               ref='internal:chapter-1'))
    realm.call([command])
    assert_matches_provider(realm, base, ours)


@pytest.mark.parametrize('peer', ['same_leaf', 'other_leaf', 'equal', 'aba', 'container'])
def test_shot_settings_leaf_presence_and_aba(peer):
    document = document_fixture(shared=False)
    image = document['shot_revisions'][0]
    image['payload']['settings'] = {'prompt': 'Old', 'turboMode': True}
    image['content_digest'] = _digest(image['payload'])
    # Regenerate the manifest after changing a retained child image.
    from astrid.sdk.timeline.commit import _manifest

    document['dependency_manifest'] = _manifest(document['shot_revisions'], document['internal_timeline_revisions'],
                                                 document['dependency_manifest']['media'], [])
    realm = DetachedRealm(document)
    base = copy.deepcopy(realm.head)
    bundle = bundle_from_document(document)
    ours = [capture_shot_set(bundle, 'occurrence:occ-a/shot', values={'settings': {'prompt': 'Ours'}})]
    values = {'turboMode': False} if peer == 'other_leaf' else {'prompt': 'Old' if peer == 'equal' else 'Theirs'}
    command = capture_shot_set(bundle, 'occurrence:occ-a/shot', values={'settings': values})
    if peer == 'container':
        command = patch(change(['settings'], present(image['payload']['settings']), [], ref='shot:chapter-shot'))
    realm.call([command])
    if peer == 'aba':
        current = bundle_from_document(realm.documents[realm.head['revision_id']])
        realm.call([capture_shot_set(current, 'occurrence:occ-a/shot', values={'settings': {'prompt': 'Old'}})])
    assert_matches_provider(realm, base, ours)


@pytest.mark.parametrize('mode', ['equal', 'aba'])
def test_doc_patch_equal_write_and_aba_are_not_lost(mode):
    realm, ours, peer = scenario('doc.patch', 'overlap')
    base = copy.deepcopy(realm.head)
    if mode == 'equal':
        peer = [patch(change(['name'], present('Renamed Film'), 'Renamed Film'))]
    realm.call(peer)
    if mode == 'aba':
        realm.call([patch(change(['name'], present('Theirs'), 'Renamed Film'))])
    session = ClassifierSession(realm)
    packet = classify(session, request(base, ours))
    assert packet['classified'], packet
    assert packet['commands'][0]['verdict'] == 'overlaps'
    assert packet['commands'][0]['overlaps'][0]['receipt'] == realm.head['publication_id']


@pytest.mark.parametrize('overlap', [False, True])
def test_shared_physical_successor_values_and_verdict_match_provider(overlap):
    realm = DetachedRealm()
    base = copy.deepcopy(realm.head)
    ours = [patch(change(['unknown'], present([1, 2]), [4], ref='internal-revision:internal-1'))]
    peer = patch(change(['unknown'], present([1, 2]), [3], ref='internal:chapter-1')) if overlap else patch(
        change(['source_window'], present({'start': 4, 'end': 9}), {'start': 4, 'end': 8},
               ref='internal:chapter-1'))
    realm.call([peer])
    session = ClassifierSession(realm)
    packet = classify(session, request(base, ours))
    assert packet['classified'], packet
    assert packet['commands'][0]['verdict'] == ('overlaps' if overlap else 'applies')
    if overlap:
        actual, = packet['commands'][0]['overlaps']
        assert (actual['base'], actual['theirs'], actual['yours']) == ([1, 2], [3], [4])
        assert actual['receipt'] == realm.head['publication_id']


@pytest.fixture
def editing_case(tmp_path, monkeypatch, real_runtime):
    """The current paired Runtime, using the established editing-case shape."""
    from tests.editing_conformance.test_commit_runtime_m1 import open_client
    from tests.helpers.runtime import use_runtime

    use_runtime()
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(tmp_path / 'client-data'))
    daemon = real_runtime(authoring_profile='astrid')
    project = daemon.service.create_project({'slug': 'clash-differential', 'name': 'S6'})['id']
    client = open_client(daemon)
    created = client.timelines.create_empty(project=project, timeline_id='film', name='S6',
                                            idempotency_key='s6-create')
    assert created.ok, created.as_dict()
    from astrid.sdk.timeline import Timeline

    timeline = Timeline.open(project, 'film', client=client, outbox_path=tmp_path / 'outbox.json')
    return daemon, client, project, timeline


@pytest.mark.integration
@pytest.mark.parametrize('overlap', [False, True])
def test_http_rebase_verdicts_match_provider(editing_case, overlap, tmp_path):
    from astrid.sdk.timeline.sync import _response
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    daemon, client, project, timeline = editing_case
    session = timeline.session
    initial = timeline._runtime_document['parent_revision']['payload']['name']
    base = copy.deepcopy(timeline._basis)
    ours = [patch(change(['name'], present(initial), 'Our title'))]
    peer = patch(change(['name'], present(initial), 'Peer title')) if overlap else patch(
        change(['meta'], ABSENT, {'org.example': {'peer': True}}))
    _, credential = daemon.credentials.provision('s6-peer', [
        'handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write',
        'tasks:read', 'tasks:write',
    ])
    peer_client = open_client(daemon, actor='s6-peer', credential=credential)
    peer_timeline = type(timeline).open(project, 'film', client=peer_client,
                                        outbox_path=tmp_path / 'peer.json')
    peer_timeline.commit([peer], label='Peer edit', key='s6-peer')
    body = {**request(base, ours), 'project_id': project}
    before = session.outbox.path.read_bytes()
    packet = classify(session, body, key='s6-ours')
    assert session.outbox.path.read_bytes() == before
    assert packet['classified'], packet
    assert packet['receipts'][0]['publisher'] == 's6-peer'
    assert packet['receipts'][0]['label'] == 'Peer edit'
    assert [row['verdict'] for row in packet['commands']] == ['overlaps' if overlap else 'applies']
    probe = client.timelines.commit(project, 'film', {**body, 'merge': 'fields', 'dry_run': True},
                                    idempotency_key='s6-direct-probe')
    assert probe.ok == (not overlap), probe.as_dict()
    if overlap:
        conflict = probe.error.details['conflicts'][0]
        actual, = packet['commands'][0]['overlaps']
        assert (actual['ref'], actual['path']) == (conflict['ref'], conflict['path'])
        assert (actual['base'], actual['theirs'], actual['yours']) == (initial, 'Peer title', 'Our title')
    else:
        rebased = {**body, 'base_revision_id': packet['head']['revision_id'],
                   'base_publication_id': packet['head']['publication_id'], 'merge': 'fields'}
        landed = _response(client.timelines.commit(project, 'film', rebased, idempotency_key='s6-land'))
        assert landed['data']['canonical_document'] == probe.data['canonical_document']
