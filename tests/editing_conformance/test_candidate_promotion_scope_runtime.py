"""Executable RT02 scope counterexample from a native provider-backed bootstrap.

This does not replace the original promotion positives or construct candidate
history. The ordinary generated Runtime fixture is shared with shot birth tests;
no candidate schema, provider override, SQL or legacy writer participates.
"""
from __future__ import annotations

import copy
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.editing_conformance.test_commit_runtime_occurrence_create import (
    generated_runtime as generated_runtime,
)

pytestmark = pytest.mark.integration


def test_native_unplacement_retains_project_shot_outside_canonical_carrier(
    request, tmp_path,
):
    runtime = request.getfixturevalue('generated_runtime')
    script = '''
import sys
from pathlib import Path
from tests.helpers.runtime import use_runtime
use_runtime()
from tests.editing_conformance.test_candidate_promotion_scope_runtime import prove_scope_gap
prove_scope_gap(Path(sys.argv[1]))
'''
    environment = {**os.environ, 'ASTRID_RUNTIME_CHECKOUT': str(runtime),
                   'PYTHONDONTWRITEBYTECODE': '1',
                   'PYTHONPATH': str(Path(__file__).parents[2])}
    result = subprocess.run([sys.executable, '-B', '-c', script, str(tmp_path)],
                            env=environment, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def prove_scope_gap(tmp_path):
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    from astrid.core.timeline.authoring_bundle import AuthoringBundleError
    from astrid.sdk.timeline._command_state import CommandError, State
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_delete import capture_occurrence_delete

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('scope-editor', ['projects:read', 'projects:write'])

    def authorize():
        return credentials.require(token, 'projects:write')

    try:
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        project = service.create_project({'slug': 'promotion-scope', 'name': 'Promotion scope'},
                                         idempotency_key='project')['id']
        service.create_timeline(project, 'film', idempotency_key='bootstrap')

        def closure():
            head = service.get_project_timeline(project, 'film')
            return service._timeline_commits()[0].revision_closure(
                project, 'film', head['head_revision_id'])

        def commit(command, key):
            head = service.get_project_timeline(project, 'film')
            request = {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                       'base_revision_id': head['head_revision_id'],
                       'base_publication_id': head['head_publication_id'], 'commands': [command]}
            return service.commit_timeline(project, 'film', request, idempotency_key=key,
                publisher='scope-editor', authorize=authorize,
                invocation_path=f'/v1/projects/{project}/timelines/film/commit')

        empty = bundle_from_document(closure())
        commit(capture_track_create(empty, 'parent', {'id': 'picture', 'kind': 'visual'}), 'track')
        commit(capture_occurrence_create(bundle_from_document(closure()), 'occ', 'project-shot',
            name='Project shot', track='picture', on=0, duration=1), 'birth')
        born = closure()
        shot = copy.deepcopy(born['shot_revisions'][0])
        internal = copy.deepcopy(born['internal_timeline_revisions'][0])
        catalog = service.get_project_shot(project, 'project-shot')
        commit(capture_occurrence_delete(bundle_from_document(born), 'occurrence:occ'), 'unplace')
        unplaced = closure()
        assert unplaced['parent_revision']['payload']['occurrences'] == []
        assert unplaced['shot_revisions'] == unplaced['internal_timeline_revisions'] == []
        assert service.get_project_shot(project, 'project-shot') == catalog
        # The smallest existing source carrier still reads the exact source.
        retained = service._timeline_commits()[0].shot_closure(
            project, 'project-shot', shot['revision_id'])
        assert retained['shot_revision'] == shot
        assert retained['internal_timeline_revision'] == internal
        with pytest.raises(CommandError, match='missing shot root'):
            State(bundle_from_document(unplaced)).entity('shot:project-shot')
        # Reattaching the source as an orphan does not turn it into an
        # accepted writable project aggregate: the canonical verifier refuses.
        orphan = copy.deepcopy(unplaced)
        orphan['shot_revisions'] = [shot]
        orphan['internal_timeline_revisions'] = [internal]
        with pytest.raises(AuthoringBundleError, match='orphans'):
            bundle_from_document(orphan)
        assert closure() == unplaced
        assert service.get_project_shot(project, 'project-shot') == catalog
        print('native birth -> unplace: catalog retained; exact source readable; '
              'project shot absent from writable canonical closure')
    finally:
        service.close()
