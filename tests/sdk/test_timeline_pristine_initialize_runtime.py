"""Real in-process Runtime create → init → restart/reload → undo → exact retry."""
from __future__ import annotations

import copy

import pytest

from tests.editing_conformance.test_pristine_initialize import GOLDEN
from tests.helpers.runtime import use_runtime, vendored_runtime_commit

pytestmark = pytest.mark.integration


def test_pristine_init_crash_resume_reload_undo_retry_and_redo(tmp_path, monkeypatch):
    use_runtime(commit=vendored_runtime_commit())
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline import commands, commit
    from astrid.sdk.timeline.outbox import Outbox

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({'slug': 'initialize', 'name': 'Initialize'})['id']

    def head():
        row = service.get_project_timeline(project, 'film')
        return {'revision_id': row['head_revision_id'], 'publication_id': row['head_publication_id']}

    def request(calls):
        current = head()
        return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': current['revision_id'],
                'base_publication_id': current['publication_id'], 'commands': calls, 'dry_run': False}

    def submit(body, key):
        return service.commit_timeline(project, 'film', body, idempotency_key=key, publisher='author',
                                       invocation_path=route_path(project, 'film'), authorize=lambda: None)

    def inverse(result):
        return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
                'args': {'publications': [result['receipt']['receipt_id']]}}

    def reopen():
        service.close()
        reopened = RuntimeService(root)
        reopened.register_timeline_commit_provider(commit.create_runtime_commit_service())
        return reopened

    try:
        # This models a client persisting its original create/init intent before
        # either call. App must wire its own recovery store to the same sequence.
        outbox = Outbox(tmp_path / 'initialize-outbox.json')
        with outbox.locked():
            outbox.write({'create_key': 'create-film', 'init_key': 'init-film',
                          'commands': copy.deepcopy(GOLDEN['commands'])})
        created = service.create_timeline(project, 'film', idempotency_key='create-film', name='Main')
        initial = head()
        # Persisted caller intent already includes the name/slug/defaults; a
        # restart between legal create and init must retain the empty basis.
        service = reopen()
        recovered = Outbox(outbox.path).read()
        intent = recovered['commands']
        assert head() == initial
        assert service.create_timeline(project, 'film', idempotency_key='create-film', name='Main') == created
        original = request(intent)
        with outbox.locked():
            outbox.write({**recovered, 'in_flight': original})
        initialized = submit(original, 'init-film')
        document = initialized['data']['canonical_document']
        assert document['parent_revision']['payload'] == GOLDEN['app_parent']
        # Independent immutable read, then process restart after a lost ACK.
        revision = head()['revision_id']
        assert service.get_project_parent_composition_revision(project, 'film', revision)['payload'] == GOLDEN['app_parent']
        service = reopen()
        assert submit(Outbox(outbox.path).read()['in_flight'], recovered['init_key']) == initialized
        undone = submit(request([inverse(initialized)]), 'undo-init')
        assert undone['data']['canonical_document']['parent_revision']['payload'] == {
            'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': [], 'occurrences': []}
        retired = head()
        assert retired['revision_id'] == initial['revision_id'] and retired != initial
        service = reopen()

        def forbidden(*args, **kwargs):
            raise AssertionError('exact accepted retry reapplied initializer or checked new semantics')

        with monkeypatch.context() as retry:
            retry.setattr(commands, 'execute', forbidden)
            retry.setattr(commit.RuntimeCommitService, 'commit', forbidden)
            assert submit(original, 'init-film') == initialized
        assert head() == retired
        for body in (request(intent), original):
            with pytest.raises(RuntimeErrorBase) as error:
                submit(body, 'new-init-' + body['base_publication_id'])
            assert error.value.details['reason'] == 'not_pristine' and head() == retired
        changed_payload = copy.deepcopy(original)
        changed_payload['commands'][0]['args']['name'] = 'Changed'
        with pytest.raises(RuntimeErrorBase):
            submit(changed_payload, 'init-film')
        assert head() == retired
        redone = submit(request([inverse(undone)]), 'redo-init')
        assert redone['data']['canonical_document'] == document
        assert len(service.list_timeline_commits(project, 'film', authorize=lambda: None)['items']) == 4
    finally:
        service.close()


def test_pristine_init_real_provider_preserves_disjoint_opaque_row_after_reload_undo_redo(
        tmp_path,
):
    """A real accepted init must ignore a later disjoint opaque track row."""
    use_runtime(commit=vendored_runtime_commit())
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline import commit
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.native_initialize import capture_initialize

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({'slug': 'opaque-init', 'name': 'Opaque Init'})['id']
    service.create_timeline(project, 'film', idempotency_key='create-film')

    def head():
        row = service.get_project_timeline(project, 'film')
        return {'revision_id': row['head_revision_id'],
                'publication_id': row['head_publication_id']}

    def document():
        current = head()
        return service._timeline_commits()[0].revision_closure(
            project, 'film', current['revision_id'])

    def submit(calls, key):
        current = head()
        body = {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': current['revision_id'],
                'base_publication_id': current['publication_id'],
                'commands': calls, 'dry_run': False}
        return service.commit_timeline(
            project, 'film', body, idempotency_key=key, publisher='author',
            invocation_path=route_path(project, 'film'), authorize=lambda: None)

    def inverse(publication):
        return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                'select': None, 'args': {'publications': [publication]}}

    def reopen():
        service.close()
        reopened = RuntimeService(root)
        reopened.register_timeline_commit_provider(commit.create_runtime_commit_service())
        return reopened

    try:
        bootstrap = bundle_from_document(document())
        init = submit([capture_initialize(
            bootstrap, name=GOLDEN['app_parent']['name'],
            slug=GOLDEN['app_parent']['slug'],
            output=GOLDEN['app_parent']['config']['output'])], 'init-film')
        initialized = init['data']['canonical_document']

        # This row deliberately uses one opaque array for the four original
        # values. Its absent label and array order are part of the proof.
        opaque_row = {
            'id': 'opaque-holder', 'kind': 'visual',
            'opaque': [None, False, [], {}],
        }
        opaque_command = capture_track_create(
            bundle_from_document(initialized), 'parent', opaque_row)
        added = submit([opaque_command], 'unrelated-opaque')
        after_add = added['data']['canonical_document']
        assert after_add['parent_revision']['payload']['config']['tracks'] == [opaque_row]

        # Compile/reload through the actual Runtime store before reversing the
        # initializer publication; this is not a detached provider replay.
        service = reopen()
        assert document() == after_add
        undone = submit([inverse(init['receipt']['receipt_id'])], 'undo-init')
        undo_payload = undone['data']['canonical_document']['parent_revision']['payload']
        assert undo_payload == {
            'config': {'clips': [], 'tracks': [opaque_row]},
            'registry': {}, 'clips': [], 'occurrences': [],
        }
        holder = undo_payload['config']['tracks'][0]
        assert list(holder) == ['id', 'kind', 'opaque']
        assert holder['opaque'] == opaque_row['opaque']

        redone = submit([inverse(undone['receipt']['receipt_id'])], 'redo-init')
        assert redone['data']['canonical_document'] == after_add
        assert head() == {
            'revision_id': redone['data']['accepted_revision_id'],
            'publication_id': redone['receipt']['receipt_id'],
        }
        history = service.list_timeline_commits(
            project, 'film', authorize=lambda: None)['items']
        assert len(history) == 5  # create, init, opaque row, undo, redo
        assert history[-1]['publication_id'] == head()['publication_id']
        assert history[-1]['previous'] == {
            'revision_id': undone['data']['accepted_revision_id'],
            'publication_id': undone['receipt']['receipt_id'],
        }
    finally:
        service.close()
