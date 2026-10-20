"""Direct real Runtime acceptance; no daemon, sockets or validator substitution."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    create_runtime_commit_service,
)
from tests.editing_conformance.test_recipe_clip_scalar_fields import (
    CHILD,
    CLEAR,
    PARENT,
    app_calls,
    clip,
)
from tests.helpers.runtime import use_runtime
from tests.sdk.test_timeline_clip_scalar_provider import app_document
from tests.timeline.test_authoring_bundle import AUDIO, OLD, _replace_values

pytestmark = pytest.mark.integration


def test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba(tmp_path):
    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({'slug': 'clip-scalars', 'name': 'Clip scalars'})['id']
    service.create_timeline(project, 'film', idempotency_key='create-film')
    media = service.ingest(project, b'clip scalar fixture', media_type='image/png',
                           original_name='fixture.png', idempotency_key='fixture')['data']['object_id']
    document = _replace_values(app_document(), {OLD: media, AUDIO: media})
    parent, shots, internals = document['parent_revision'], document['shot_revisions'], document['internal_timeline_revisions']
    for row in internals:
        row['timeline_id'] = 'film'
        row['payload'].update(effects=[], audio=[], layout={})
    for row in shots:
        row['payload'] = {'metadata': {'title': 'F2 agent shot'}, 'items': [], 'pools': [],
            'selected_variants': {}, 'provenance': {}, 'generation_inputs': {},
            'audio_bindings': [], 'text_bindings': [],
            'internal_timeline_revision_id': row['internal_timeline_revision_id']}
    for row in [parent, *shots, *internals]:
        row['content_digest'] = _digest(row['payload'])
    document['dependency_manifest'] = _manifest(shots, internals, [{'media_id': media, 'content_digest': media}], [])
    resource = service.get_project_timeline(project, 'film')
    service.publish_parent_composition(project, 'film', {
        'project_id': project, 'timeline_id': 'film', 'expected_head': resource['head_revision_id'],
        'parent_revision_id': 'app-scalar-baseline', 'parent_composition': parent['payload'],
        'shot_revisions': shots, 'internal_timeline_revisions': internals,
    }, idempotency_key='seed-app-scalars')
    service.register_timeline_commit_provider(create_runtime_commit_service())

    def head():
        row = service.get_project_timeline(project, 'film')
        return {'revision_id': row['head_revision_id'], 'publication_id': row['head_publication_id']}

    def current():
        return service._timeline_commits()[0].revision_closure(project, 'film', head()['revision_id'])

    def request(calls):
        pin = head()
        return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': pin['revision_id'], 'base_publication_id': pin['publication_id'],
                'commands': calls, 'dry_run': False}

    def submit(body, key):
        return service.commit_timeline(project, 'film', body, idempotency_key=key,
            publisher='scalar-author', invocation_path=route_path(project, 'film'), authorize=lambda: None)

    def undo(publication, key):
        return submit(request([{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
            'select': None, 'args': {'publications': [publication]}}]), key)

    try:
        original = current()
        calls = app_calls(bundle_from_document(original))
        body = request(calls)
        accepted = submit(body, 'app-scalars')
        assert accepted['data']['commands'] == calls
        document = accepted['data']['canonical_document']
        assert current() == document
        state = bundle_from_document(document)
        assert clip(state, CHILD)['hold'] == 4
        assert 'asset' not in clip(state, CLEAR)
        assert 'transition' not in clip(state, PARENT)
        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(create_runtime_commit_service())
        assert current() == document
        assert submit(body, 'app-scalars') == accepted
        undone = undo(accepted['receipt']['receipt_id'], 'undo-app-scalars')
        assert undone['data']['canonical_document'] == original
        redone = undo(undone['receipt']['receipt_id'], 'redo-app-scalars')
        assert redone['data']['canonical_document'] == document
        repeated = submit(request([capture_clip_set(bundle_from_document(document), CLEAR, clear=['asset'])]), 'unchanged-clear')
        assert repeated['data']['canonical_document'] == document
        before = copy.deepcopy(head())
        with pytest.raises(RuntimeErrorBase) as error:
            undo(accepted['receipt']['receipt_id'], 'refuse-aba')
        assert error.value.details['reason'] == 'intervening_write'
        assert head() == before
    finally:
        service.close()
