"""Registered attachment through the existing authenticated Runtime commit port."""
from __future__ import annotations

import copy

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_attach_normal_port_exact_sharing_steps_history_guards_inverse_redo(tmp_path):
    use_runtime()
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_attach import capture_occurrence_attach
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('attach-editor', ['projects:read', 'projects:write'])

    def authorize():
        return credentials.require(token, 'projects:write')

    try:
        project = service.create_project({'slug': 'attach', 'name': 'Attach'}, idempotency_key='project')['id']
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        service.create_timeline(project, 'film', idempotency_key='bootstrap')

        def document():
            head = service.get_project_timeline(project, 'film')
            return service._timeline_commits()[0].revision_closure(project, 'film', head['head_revision_id'])

        def request(calls):
            head = service.get_project_timeline(project, 'film')
            return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                    'base_revision_id': head['head_revision_id'],
                    'base_publication_id': head['head_publication_id'], 'commands': calls,
                    'label': 'Attach shared child', 'steps': [
                        {'id': 'edit', 'label': 'Attach shared child', 'intent': 'Retain sharing',
                         'tags': ['copy'], 'command_ordinals': list(range(len(calls))), 'patch': [], 'reads': []}],
                    'merge': 'fields', 'reads': [], 'dry_run': False, 'source': {'via': 'python'},
                    'rationale': 'Place the exact destination child again', 'group_id': 'copy'}

        def commit(body, key):
            validate_commit_value(body, 'CommitRequest')
            result = service.commit_timeline(project, 'film', body, idempotency_key=key,
                publisher='attach-editor', invocation_path=f'/v1/projects/{project}/timelines/film/commit',
                authorize=authorize)
            validate_commit_value(result['data'], 'CommitPreview' if body['dry_run'] else 'CommitAccepted')
            return result

        def bundle():
            return bundle_from_document(document())

        commit(request([capture_track_create(bundle(), 'parent', {'id': 'picture', 'kind': 'visual'})]), 'track')
        before = document()
        first = capture_occurrence_create(bundle(), 'first', 'shared', name='Shared', track='picture', on=0, duration=10)
        born = execute(bundle(), [first]).bundle
        attached = capture_occurrence_attach(born, 'occurrence:first', 'second', track='picture', on=12, duration=4)
        body = request([first, attached])
        preview_body = {**copy.deepcopy(body), 'dry_run': True}
        # G5 still needs the V2 timing adapter to materialize shared authoring
        # contexts. Keep this positive path intact until that scoped repair.
        preview = commit(preview_body, 'preview')
        assert preview['receipt'] is None
        assert preview['data']['would_status'] == 'accepted'
        assert document() == before
        result = commit(body, 'attach')
        assert result['data']['status'] == 'accepted'
        after = document()
        assert result['data']['canonical_document'] == after
        rows = after['parent_revision']['payload']['occurrences']
        assert [row['occurrence_id'] for row in rows] == ['first', 'second']
        assert rows[0]['shot_id'] == rows[1]['shot_id'] == 'shared'
        assert rows[0]['shot_revision_id'] == rows[1]['shot_revision_id']
        assert rows[1]['placement']['start_ms'] == 12000 and rows[1]['duration_ms'] == 4000
        assert len(after['shot_revisions']) == len(after['internal_timeline_revisions']) == 1
        history = service.list_timeline_commits(project, 'film', authorize=authorize)
        entry = history['items'][-1]
        record = entry['records']['commands'][1]
        assert record['created'] == [{'ref': 'occurrence:second', 'kind': 'occurrence', 'owner': 'parent'}]
        assert record['writes'][0]['after']['value']['shot_id'] == 'shared'
        assert any(read['ref'] == 'timeline' for read in record['reads'])
        assert entry['steps'] == result['data']['steps']
        assert result['data']['steps'][0]['patch']
        assert commit(body, 'attach') == result

        def inverse(accepted, key):
            return commit(request([{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                'select': None, 'args': {'publications': [accepted['receipt']['receipt_id']]}}]), key)

        # Undo only an attachment of an existing child, retaining both siblings.
        third = capture_occurrence_attach(bundle(), 'occurrence:first', 'third', track='picture', on=20, duration=2)
        third_result = commit(request([third]), 'third')
        third_document = document()
        undo = inverse(third_result, 'undo-third')
        assert document() == after
        inverse(undo, 'redo-third')
        assert document() == third_document
        assert document()['parent_revision']['payload']['occurrences'][:2] == rows

        for damage in ('outside', 'occupied', 'media', 'shot', 'created', 'reads'):
            call = capture_occurrence_attach(bundle(), 'occurrence:first', 'fourth', track='picture', on=24, duration=1)
            if damage == 'outside':
                call['select'] = 'occurrence:foreign'
            elif damage == 'occupied':
                call['args']['occurrence_id'] = 'second'
            elif damage in ('media', 'shot'):
                call['args'][damage] = 'guessed'
            elif damage == 'created':
                call['created'].append('shot:forged')
            else:
                call['reads'][0]['state'] = {'state': 'absent'}
            saved = document()
            saved_history = service.list_timeline_commits(project, 'film', authorize=authorize)
            with pytest.raises(RuntimeErrorBase):
                commit(request([call]), damage)
            assert document() == saved
            assert service.list_timeline_commits(project, 'film', authorize=authorize) == saved_history
    finally:
        service.close()
