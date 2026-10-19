"""Current Runtime public-seed and official commit-boundary qualification only."""
from __future__ import annotations

import json

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_public_seed_refuses_exact_rational_fps_legacy_input_atomically(tmp_path):
    use_runtime()
    from runtime_protocol.errors import NotFoundError, ValidationError
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    from astrid.sdk.timeline.commit import _digest
    from tests.editing_conformance.test_recipe_m2_group_migration import legacy_document
    from tests.sdk.test_timeline_commit_provider_document import MEDIA

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({'slug': 'migration', 'name': 'Migration'})['id']
        service.create_timeline(project, 'film', idempotency_key='timeline')
        media = service.ingest(project, b'migration-image', media_type='image/png',
                               original_name='image.png', idempotency_key='image')['data']['object_id']
        document = json.loads(json.dumps(legacy_document()).replace(MEDIA, media))
        document['project_id'] = project
        parent = document['parent_revision']
        parent['content_digest'] = _digest(parent['payload'])
        before = service.get_project_timeline(project, 'film')
        publication = {
            'project_id': project, 'timeline_id': 'film', 'expected_head': None,
            'parent_revision_id': parent['revision_id'], 'parent_composition': parent['payload'],
            'shot_revisions': [], 'internal_timeline_revisions': [],
            'dependency_manifest': document['dependency_manifest'],
        }
        # Neutral legacy publication has no DocumentPin field. Removing it
        # for the second probe exposes the independent rational-fps refusal.
        with pytest.raises(ValidationError, match='dependency_manifest contains unsupported fields') as error:
            service.publish_parent_composition(project, 'film', publication, idempotency_key='legacy-pins')
        assert error.value.details == {'field': 'documents'}
        del publication['dependency_manifest']['documents']
        with pytest.raises(ValidationError, match='visual timing fps must be finite and positive'):
            service.publish_parent_composition(project, 'film', publication, idempotency_key='legacy-seed')
        assert service.get_project_timeline(project, 'film') == before
        with pytest.raises(NotFoundError):
            service.get_project_parent_composition_revision(project, 'film', parent['revision_id'])
    finally:
        service.close()


def test_official_runtime_schema_admits_compiled_canonical_candidate():
    use_runtime()
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from tests.editing_conformance.test_recipe_m2_group_migration import FIXTURE

    validate_commit_value(json.loads(FIXTURE.read_text())['output'], 'CanonicalDocument')


@pytest.mark.xfail(strict=True, reason='Official Runtime commit schema must admit the shot root TargetKey guards supplied by recorded root creation')
def test_official_runtime_schema_admits_recorded_migration_command():
    use_runtime()
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from tests.editing_conformance.test_recipe_m2_group_migration import FIXTURE

    validate_commit_value(json.loads(FIXTURE.read_text())['commands'][0], 'EditCommand')
