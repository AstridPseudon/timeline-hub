"""Shared provenance through real managed-media reads and Runtime acceptance.

The test-only recipe/provider adapter admits its declared selection using ABI 1.
This qualifies manifest subset acceptance, not any production popup operation.
The historical fixture keeps numeric 24 fps and its original window scope.
"""
from __future__ import annotations

import copy
import hashlib
import io
from types import SimpleNamespace

import pytest
from PIL import Image

from tests.helpers.runtime import use_runtime
from tests.helpers.trusted_seed import seed_trusted_parent

pytestmark = pytest.mark.integration


@pytest.fixture
def manifest_media(tmp_path):
    """Build a complete native closure in a fresh realm through trusted setup.

    The archived 7f6dd89 film is read only for its canonical 55/29-shaped
    source. The test realm is new, so the setup crosses Runtime's current
    bootstrap/commit-store boundary instead of calling retired shot or parent
    writers.
    """
    runtime = use_runtime(commit='7f6dd89')
    import sys
    sys.path.insert(0, str(runtime / 'tests'))
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from timeline_commit_film_fixture import build_film_fixture, read_object_from_realm

    source_root = tmp_path / 'source'
    source_root.mkdir()
    source_fixture = build_film_fixture(source_root)
    source = RuntimeService(source_fixture.duplicate_root)
    try:
        source_document = source._timeline_commits()[0].revision_closure(
            source_fixture.project_id, source_fixture.timeline_id,
            source_fixture.parent_revision_id,
        )
        source_objects = [
            (row['digest'], row['media_type'], row['original_name'])
            for row in source.store.conn.execute(
                'SELECT digest, media_type, original_name FROM objects'
            )
        ]
    finally:
        source.close()

    root = tmp_path / 'manifest-realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project(
        {'slug': 'manifest-fixture', 'name': 'Manifest fixture'},
        idempotency_key='manifest-project',
    )['id']
    service.create_timeline(project, 'film', idempotency_key='manifest-timeline')
    authorize = lambda: None  # noqa: E731 - trusted test setup only

    for digest, media_type, original_name in source_objects:
        # Preserve the canonical fixture's complete dependency closure in the
        # fresh realm without using a retired timeline writer.
        data = read_object_from_realm(source_fixture.duplicate_root, 'sha256:' + digest)
        service.ingest(
            project, data, media_type=media_type, original_name=original_name,
            idempotency_key='manifest-source-' + digest,
        )

    def imported(name, colour):
        payload = io.BytesIO()
        Image.new('RGB', (16, 12), colour).save(payload, format='PNG')
        data = payload.getvalue()
        digest = 'sha256:' + hashlib.sha256(data).hexdigest()
        result = service.import_media(
            project, data, media_type='image/png', original_name=name + '.png',
            expected_digest=digest, actor_id='trusted-test-setup', width=16,
            height=12, idempotency_key='manifest-' + name,
        )['data']
        return service.get_project_media_selection(
            project,
            {'asset': 'picture-1', 'generation_id': result['generation_id'],
             'variant_id': result['variant_id']},
            authorize=authorize,
        )

    old, new = imported('old', 'red'), imported('new', 'blue')
    parent = copy.deepcopy(source_document['parent_revision']['payload'])
    shots = copy.deepcopy(source_document['shot_revisions'])
    internals = copy.deepcopy(source_document['internal_timeline_revisions'])
    first = next(row for row in shots if row['shot_id'] == 'shot-1')
    internal_id = first['internal_timeline_revision_id']
    internal = next(row for row in internals if row['revision_id'] == internal_id)
    entry = internal['payload']['registry']['assets']['picture-1']
    entry.update(
        media_id=old['object_id'], type='image',
        generationId=old['generation_id'], variantId=old['variant_id'],
        opaque={'keep': True},
    )
    first_occurrence = next(row for row in parent['occurrences'] if row['shot_id'] == 'shot-1')
    owner = 'occurrence:' + first_occurrence['occurrence_id']
    clip = internal['payload']['clips'][0]['id']
    first['payload']['internal_timeline_revision_id'] = internal_id
    baseline_head = service.get_project_timeline(project, 'film')['head_revision_id']
    seed_trusted_parent(
        service,
        {
            'project_id': project, 'timeline_id': 'film', 'expected_head': baseline_head,
            'parent_revision_id': 'media-baseline', 'parent_composition': parent,
            'shot_revisions': shots, 'internal_timeline_revisions': internals,
        },
        idempotency_key='media-baseline',
    )
    commits, _ = service._timeline_commits()
    baseline = commits.revision_closure(project, 'film', 'media-baseline')
    return SimpleNamespace(
        root=root, service=service, project=project, authorize=authorize,
        old=old, new=new, owner=owner, clip=clip, baseline=baseline,
    )


@pytest.mark.parametrize('operation', ['add', 'swap'])
def test_real_media_manifest_inverse_retry_restart_and_history(monkeypatch, operation, manifest_media):
    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort, route_path

    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.commit import RuntimeCommitService, create_runtime_commit_service

    service, project, authorize = manifest_media.service, manifest_media.project, manifest_media.authorize
    old, new = manifest_media.old, manifest_media.new

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
            ctx.read(owner + '/clip:' + manifest_media.clip)
            ctx.write(owner + '/clip:' + manifest_media.clip, ['asset'], 'new')

    installed = commands.operations()
    installed['test.media-provenance'] = commands.Operation({'type': 'object'}, introduce, {})
    monkeypatch.setattr(commands, 'operations', lambda: installed)

    class RecipeProvider(RuntimeCommitService):
        def commit(self, context, port):
            # Test-only recipe ABI adapter, not a production popup operation.
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
        register()
        request = body([{'schema_version': 1, 'op': 'test.media-provenance', 'version': '1',
                         'select': manifest_media.owner, 'args': {'media': new}}])
        created = submit(request, 'introduce')
        baseline = next(row for row in captured if row['parent_revision']['revision_id'] == 'media-baseline')
        assert baseline == manifest_media.baseline
        assert old['object_id'] in {pin['media_id'] for pin in baseline['dependency_manifest']['media']}
        assert new['object_id'] not in {pin['media_id'] for pin in baseline['dependency_manifest']['media']}
        assert new['object_id'] in {pin['media_id'] for pin in created['data']['canonical_document']['dependency_manifest']['media']}
        assert ({pin['media_id'] for pin in created['data']['canonical_document']['dependency_manifest']['media']}
                - {pin['media_id'] for pin in baseline['dependency_manifest']['media']}) == {new['object_id']}
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
        root = manifest_media.root
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
