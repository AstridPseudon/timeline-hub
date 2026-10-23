"""Reconstructed 1232 combined undo regression; diagnostic artifact, not a suite rewrite.

Setup and acceptance body: exact bfcf78db test. Undo call: retained red log.
Post-call positive assertions: restoration requirement, not previously captured facts.
"""
import copy

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.emitter import emit_document_commands
from astrid.sdk.timeline.native_occurrence_fork import capture_occurrence_fork
from tests.editing_conformance.test_occurrence_fork_source_baseline import OWNER, TARGET


def test_current_runtime_retained_fork_then_emitter_and_guarded_undo(tmp_path):
    from types import SimpleNamespace

    from tests.helpers.runtime import use_runtime

    use_runtime()
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from tests.editing_conformance.test_native_sheet_current_runtime import (
        seed_document_diff_parent,
    )

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('fork-editor', ['projects:read', 'projects:write'])

    def document():
        head = service.get_project_timeline(project, 'film')
        return service._timeline_commits()[0].revision_closure(project, 'film', head['head_revision_id'])

    def commit(calls, key, *, dry_run=False):
        head = service.get_project_timeline(project, 'film')
        body = {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': head['head_revision_id'],
                'base_publication_id': head['head_publication_id'], 'commands': calls,
                'label': key, 'steps': [{'id': f'{key}-{ordinal}', 'label': key,
                    'intent': 'Selected occurrence', 'tags': [], 'command_ordinals': [ordinal],
                    'patch': call['args']['changes'] if call['op'] == 'doc.patch' else [], 'reads': []}
                    for ordinal, call in enumerate(calls)],
                'merge': 'fields', 'reads': [], 'dry_run': dry_run, 'source': {'via': 'app'},
                'rationale': 'Preserve the copied source baseline', 'group_id': 'fork-gesture'}
        validate_commit_value(body, 'CommitRequest')
        return service.commit_timeline(project, 'film', body, idempotency_key=key,
            publisher='fork-editor', invocation_path=f'/v1/projects/{project}/timelines/film/commit',
            authorize=lambda: credentials.require(token, 'projects:write'))

    try:
        project = service.create_project({'slug': 'fork', 'name': 'Fork'}, idempotency_key='project')['id']
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        service.create_timeline(project, 'film', idempotency_key='bootstrap')
        seed_document_diff_parent(SimpleNamespace(project=project, service=lambda: service))
        original = document()
        before = bundle_from_document(original)
        call = capture_occurrence_fork(before, OWNER, 'selected-shot')
        projected = bundle_from_document(document_from_bundle(execute(before, [call]).bundle))
        after = copy.deepcopy(projected)
        State(after).entity(TARGET)['params'] = {}
        patches = emit_document_commands(projected, after)
        calls = [call, *patches]
        preview = commit(calls, 'preview', dry_run=True)
        assert preview['receipt'] is None
        assert preview['data']['status'] == 'preview'
        assert preview['data']['would_status'] == 'accepted'
        assert document() == original
        result = commit(calls, 'fork-edit')
        validate_commit_value(result['data'], 'CommitAccepted')
        assert result['data']['status'] == 'accepted'
        landed = document()
        assert landed == result['data']['canonical_document'] == preview['data']['canonical_document']
        assert landed['parent_revision']['payload']['occurrences'][1:] == original[
            'parent_revision']['payload']['occurrences'][1:]
        assert original['shot_revisions'][0] in landed['shot_revisions']
        assert original['internal_timeline_revisions'][0] in landed['internal_timeline_revisions']
        assert State(bundle_from_document(landed)).entity(TARGET)['params'] == {}
        assert result['data']['steps'][0]['patch']
        undone = commit([{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                          'select': None, 'args': {'publications': [result['receipt']['receipt_id']]}}], 'undo')
        # Positive restoration requirement; the retained traceback ends at the call above.
        assert undone['data']['status'] == 'accepted'
        assert document() == original
    finally:
        service.close()
