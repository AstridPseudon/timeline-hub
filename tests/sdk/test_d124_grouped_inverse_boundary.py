"""Grouped birth inverses retain custody of child writes before root removal."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, create_runtime_commit_service
from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration
OWNER = 'occurrence:child'


@pytest.fixture
def film(tmp_path):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(create_runtime_commit_service())
    project = service.create_project({'slug': 'inverse-boundary', 'name': 'Inverse boundary'})['id']
    service.create_timeline(project, 'film', idempotency_key='bootstrap')

    def document():
        head = service.get_project_timeline(project, 'film')
        return service._timeline_commits()[0].revision_closure(project, 'film', head['head_revision_id'])

    def submit(calls, key):
        head = service.get_project_timeline(project, 'film')
        body = {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': head['head_revision_id'],
                'base_publication_id': head['head_publication_id'], 'commands': calls}
        original = copy.deepcopy(body)
        result = service.commit_timeline(project, 'film', body, idempotency_key=key,
            publisher='author', invocation_path=route_path(project, 'film'), authorize=lambda: None)
        assert body == original
        assert result['data']['status'] == 'accepted'
        assert result['receipt']['result'] == result['data']
        return result

    try:
        submit([capture_track_create(bundle_from_document(document()), 'parent',
                {'id': 'picture', 'kind': 'visual'})], 'parent-track')
        yield service, document, submit
    finally:
        service.close()


def birth_commands(document):
    bundle = bundle_from_document(document)
    birth = capture_occurrence_create(bundle, 'child', 'child-shot', name='Child',
                                      track='picture', on=0, duration=10)
    born = execute(bundle, [birth]).bundle
    track = capture_track_create(born, OWNER, {'id': 'one', 'kind': 'visual'})
    return [birth, track]


def inverse(result):
    return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
            'args': {'publications': [result['receipt']['receipt_id']]}}


def test_grouped_birth_keeps_exact_step_and_child_write(film):
    service, document, submit = film
    created = submit(birth_commands(document()), 'birth')
    accepted = document()
    assert created['data']['canonical_document'] == accepted
    assert accepted['internal_timeline_revisions'][0]['payload']['tracks'] == [
        {'id': 'one', 'kind': 'visual'}]
    history = service.list_timeline_commits(accepted['project_id'], 'film', authorize=lambda: None)
    records = history['items'][-1]['records']
    step, = records['steps']
    assert step['command_ordinals'] == [0, 1]
    assert [[(write['ref'], write['path']) for write in command['writes']]
            for command in records['commands']] == [
        [('shot:child-shot', []), (OWNER, [])], [(OWNER + '/track:one', [])]]
    assert records['commands'][0]['created'] == [
        {'ref': 'shot:child-shot', 'kind': 'shot', 'owner': None},
        {'ref': OWNER, 'kind': 'occurrence', 'owner': 'parent'}]
    assert records['commands'][1]['writes'] == [
        {'ref': OWNER + '/track:one', 'path': [], 'before': {'state': 'absent'},
         'after': {'state': 'present', 'value': {'id': 'one', 'kind': 'visual'}}}]
    shot, = accepted['shot_revisions']
    child, = accepted['internal_timeline_revisions']
    assert shot['internal_timeline_revision_id'] == child['revision_id']
    for prefix, image in [('shot-revision:', shot), ('internal-revision:', child)]:
        physical = prefix + image['revision_id']
        effect, = [effect for effect in step['patch'] if effect['ref'] == physical]
        assert effect == {'op': 'set', 'ref': physical, 'path': [],
                          'before': {'state': 'absent'}, 'value': image['payload']}
        pin, = [binding for command in records['commands'] for binding in command['bindings']
                if binding['key'] == 'commit.effect' and binding['boundary']['side'] == 'after'
                and binding['physical_ref'] == physical]
        assert pin['revision_id'] == image['revision_id']
        assert pin['content_digest'] == image['content_digest']
        assert pin['owners'] == [OWNER + '/shot']


def test_grouped_birth_inverse_restores_exact_boundary(film):
    _, document, submit = film
    before = document()
    created = submit(birth_commands(before), 'birth')
    # C0 section 5 requires reversing the complete step, including its child
    # write, before removing the created occurrence and physical shot roots.
    undone = submit([inverse(created)], 'undo-birth')
    assert undone['data']['canonical_document'] == before
    assert document() == before
    redone = submit([inverse(undone)], 'redo-birth')
    assert redone['data']['canonical_document'] == created['data']['canonical_document']


def test_ungrouped_birth_and_child_inverses_restore_exact_boundaries(film):
    _, document, submit = film
    before = document()
    birth, _ = birth_commands(before)
    created = submit([birth], 'birth')
    undone = submit([inverse(created)], 'undo-birth')
    assert undone['data']['canonical_document'] == before
    assert document() == before
    redone = submit([inverse(undone)], 'redo-birth')
    assert redone['data']['canonical_document'] == created['data']['canonical_document']
    track = capture_track_create(bundle_from_document(document()), OWNER,
                                 {'id': 'one', 'kind': 'visual'})
    child = submit([track], 'child-track')
    assert submit([inverse(child)], 'undo-track')['data']['canonical_document'] == (
        created['data']['canonical_document'])
    assert document() == created['data']['canonical_document']
