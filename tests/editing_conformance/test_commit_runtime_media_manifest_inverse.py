"""Shared provenance through real managed-media reads and Runtime acceptance.

The test-only recipe/provider adapter admits its declared selection using ABI 1.
This qualifies manifest subset acceptance, not any production popup operation.
"""
from __future__ import annotations

import copy

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.mark.parametrize('operation', ['add', 'swap'])
def test_real_media_manifest_inverse_retry_restart_and_history(tmp_path, monkeypatch, operation):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort, route_path
    from test_generation_publish_v1_settlement import _effect, _fixture, _output, _settle
    from timeline_commit_film_fixture import _binding_descriptor

    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.commit import RuntimeCommitService, create_runtime_commit_service
    from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture

    def effect(project):
        return _effect(project, groups=[{'group_key': 'main', 'selectors': [
            {'selector': name, 'ordinal': index, 'variant_key': name, 'output_port': 'image'}
            for index, name in enumerate(('old', 'new'))]}])

    service, project, task, attempt, admitted = _fixture(tmp_path, effect_factory=effect)
    project = project['id']
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('media-editor', ['projects:read', 'projects:write'])

    def authorize():
        return credentials.require(token, 'projects:write')

    def introduce(ctx, command):
        pin = command['args']['media']
        owner = command['select']
        ctx.read(owner + '/source')
        ctx.write(owner + '/source', ['registry', 'assets', 'new'], {
            'media_id': pin['object_id'], 'type': 'image', 'generationId': pin['generation_id'],
            'variantId': pin['variant_id'], 'opaque': [None, False, {}]})
        ctx.dependency('fixture.media', 'media', pin)
        if operation == 'add':
            ctx.create(owner, 'clip', {'id': 'reserved-child', 'track': 'picture', 'asset': 'new',
                                       'clipType': 'image', 'at': .125, 'hold': 1.25, 'params': None})
        else:
            ctx.read(owner + '/clip:clip-a')
            ctx.write(owner + '/clip:clip-a', ['asset'], 'new')

    installed = commands.operations()
    installed['test.media-provenance'] = commands.Operation({'type': 'object'}, introduce, {})
    monkeypatch.setattr(commands, 'operations', lambda: installed)

    class RecipeProvider(RuntimeCommitService):
        def commit(self, context, port):
            # The base worker predates the held native-media admission seam.
            # Use its exact ABI read; never replace captures or prepared output.
            for call in context['request']['commands']:
                if call['op'] == 'test.media-provenance':
                    port.selected_media(call['args']['media'])
            return super().commit(context, port)

    captured = []
    real_closure = RequestCommitPort.revision_closure

    def closure(port, revision):
        result = real_closure(port, revision)
        captured.append(copy.deepcopy(result))
        return result

    monkeypatch.setattr(RequestCommitPort, 'revision_closure', closure)

    def register():
        service.register_timeline_commit_provider(RecipeProvider(create_runtime_commit_service().contract_digest))

    def body(calls, *, dry_run=False):
        head = service.get_project_timeline(project, 'film')
        return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': head['head_revision_id'], 'base_publication_id': head['head_publication_id'],
                'commands': calls, 'dry_run': dry_run, 'source': {'via': 'python'}}

    def submit(request, key):
        return service.commit_timeline(project, 'film', request, idempotency_key=key, publisher='media-editor',
                                       invocation_path=route_path(project, 'film'), authorize=authorize)

    def inverse(result):
        return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
                'args': {'publications': [result['receipt']['receipt_id']]}}

    try:
        outputs = [_output(name.encode(), output_port='image', group_key='main', variant_key=name,
                           ordinal=index, filename=name + '.png', media_type='image/png')
                   for index, name in enumerate(('old', 'new'))]
        _settle(service, attempt, outputs, effect=admitted)
        selections = {row['variant_key']: service.get_project_media_selection(project, {
            'association_id': row['association_id'], 'object_id': row['object_id'],
            'version': row['lifecycle']['version']}, authorize=authorize)
            for row in service.managed_outputs(task['task']['id'])}
        old, new = selections['old'], selections['new']

        def replace(value):
            if value == MEDIA:
                return old['object_id']
            if isinstance(value, dict):
                return {key: replace(child) for key, child in value.items()}
            if isinstance(value, list):
                return [replace(child) for child in value]
            return value

        document = replace(document_fixture())
        internal = document['internal_timeline_revisions'][0]
        internal['payload'].pop('source_window')
        internal['timeline_id'] = 'film'
        # Legacy seed publication's visual seam accepts numeric fps only.
        # Rational fps/source preservation remains in the detached proof.
        document['parent_revision']['payload']['config']['output']['fps'] = 24
        internal['payload']['output']['fps'] = 24
        for occurrence in document['parent_revision']['payload']['occurrences']:
            occurrence.update(source_offset=0, speed=1)
        document['parent_revision']['payload']['occurrences'][0]['placement']['start_ms'] = 8000
        service.create_project_shot(project, {'shot_id': 'chapter-shot', 'name': 'Chapter One'},
                                    idempotency_key='chapter-shot')
        binding = service.set_project_shot_text_binding(project, {
            'shot_id': 'chapter-shot', 'kind': 'transcript', 'text': 'A chapter', 'expected_head': 0,
        }, idempotency_key='chapter-text')['data']
        document['shot_revisions'][0]['payload']['text_bindings'] = [_binding_descriptor(binding, 'A chapter')]
        service.publish_parent_composition(project, 'film', {
            'project_id': project, 'timeline_id': 'film', 'expected_head': None,
            'parent_revision_id': 'media-baseline', 'parent_composition': document['parent_revision']['payload'],
            'shot_revisions': [{key: value for key, value in row.items() if key != 'content_digest'}
                               for row in document['shot_revisions']],
            'internal_timeline_revisions': [{key: value for key, value in internal.items()
                                             if key != 'content_digest'}],
        }, idempotency_key='media-baseline')
        register()
        request = body([{'schema_version': 1, 'op': 'test.media-provenance', 'version': '1',
                         'select': 'occurrence:occ-a', 'args': {'media': new}}])
        created = submit(request, 'introduce')
        baseline = next(row for row in captured if row['parent_revision']['revision_id'] == 'media-baseline')
        assert new['object_id'] not in {pin['media_id'] for pin in baseline['dependency_manifest']['media']}
        assert new['object_id'] in {pin['media_id'] for pin in created['data']['canonical_document']['dependency_manifest']['media']}
        undo_request = body([inverse(created)])
        preview = submit(dict(undo_request, dry_run=True), 'undo-preview')
        assert preview['data']['canonical_document'] == baseline
        captured.clear()
        undone = submit(undo_request, 'undo')
        assert undone['data']['canonical_document'] == baseline
        # Acceptance captured and validated the introduced media in the target
        # closure, while its result manifest omits it. History remains immutable.
        assert created['data']['canonical_document'] in captured
        before_restart = service.list_timeline_commits(project, 'film', authorize=authorize)
        root = tmp_path / 'publish'
        service.close()
        service = RuntimeService(root)
        register()
        with monkeypatch.context() as retry:
            retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('retry executed semantics'))
            assert submit(undo_request, 'undo') == undone
            assert submit(request, 'introduce') == created
        changed = copy.deepcopy(undo_request)
        changed['source'] = {'via': 'cli'}
        with pytest.raises(RuntimeErrorBase) as error:
            submit(changed, 'undo')
        assert error.value.status == 409
        assert service.list_timeline_commits(project, 'film', authorize=authorize) == before_restart
        assert service.get_project_media_selection(project, {key: new[key] for key in (
            'asset', 'generation_id', 'variant_id')}, authorize=authorize) == new
        redone = submit(body([inverse(undone)]), 'redo')
        assert redone['data']['canonical_document'] == created['data']['canonical_document']
        history = service.list_timeline_commits(project, 'film', authorize=authorize)['items']
        edge = next(row for row in history if row['publication_id'] == created['receipt']['receipt_id'])
        assert edge['receipt'] == created['receipt']
        assert edge['records']['commands'][0]['dependencies'][0]['pin'] == new
        stored = service.get_project_parent_composition_revision(project, 'film', created['data']['accepted_revision_id'])
        assert stored['dependency_manifest'] == created['data']['canonical_document']['dependency_manifest']
        assert service.store.integrity_report()['ok']
    finally:
        service.close()
