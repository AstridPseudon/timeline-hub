"""Bounded outer admission and the authored carrier still needed for WC5.

Admission is real; no outer action is executed or settled while its exact
authored result cannot be expressed by the installed command registry.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import astrid.sdk as sdk
from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._shot_commands import capture_shot_set
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import create_runtime_commit_service
from astrid.sdk.workspace_client import WorkspaceClient
from astrid_runtime_client import contract_metadata
from astrid_runtime_client.generated import ApiError
from tests.packs.video_editing.test_draft_voiceover import fixture, synthesis

OUTER = 'video_editing.sync_draft_voiceover'
OUTER_RUNTIME_COMMIT = 'fcf4c3d5e9444bf9e221d05aa8fa8d203fb27bd3'


class _MissingTargetCarrier(AssertionError):
    pass


def _ripple_outcome():
    candidate, scripts = fixture()
    scripts['occurrences'][0]['text'] = 'Long new narration'
    prepared = vo.prepare_draft_voiceover(candidate, scripts, synthesize=synthesis,
        timing_policy='ripple', padding_seconds=.15)
    return candidate, prepared['candidate']


def test_outer_fixture_still_requires_audio_provenance_and_ripple():
    before, after = _ripple_outcome()
    assert before['placements'][0]['duration_ms'] == 3000
    assert after['placements'][0]['duration_ms'] == 4150
    assert after['placements'][1]['placement']['start_ms'] == 4150
    assert after['shots']['s1']['internal_timeline']['clips'][0]['hold'] == 4.15
    assert after['shots']['s1']['internal_timeline']['clips'][1]['to'] == 4
    assert after['parent']['clips'][0]['hold'] == 7.15
    assert after['parent']['config']['duration'] == 7.15
    record = after['shots']['s1']['payload']['metadata'][vo.KEY]
    assert record['text'] == 'Long new narration'
    assert record['generation_task_id'] == 'task'
    assert record['audio_media_id'] == synthesis('', {})['audio_media_id']


@pytest.mark.xfail(strict=True, raises=CommandError,
    reason='WC5 requires a registered carrier for exact draft_voiceover shot metadata')
def test_outer_fixture_provenance_can_be_captured_without_a_snapshot_writer():
    before, after = _ripple_outcome()
    record = after['shots']['s1']['payload']['metadata'][vo.KEY]
    # Keep the successful authored outcome as the requirement. shot.set is
    # currently limited to name/settings; do not drop this provenance to fit it.
    command = capture_shot_set(before, 'occurrence:o1/shot',
        values={'metadata': {vo.KEY: copy.deepcopy(record)}})
    result = execute(before, [command])
    assert result.bundle['shots']['s1']['payload']['metadata'][vo.KEY] == record


@pytest.mark.integration
def test_outer_admission_records_exact_spec_and_worker_has_no_commit_authority(tmp_path, real_runtime, capsys):
    root = Path(__file__).resolve().parents[3]
    lock = json.loads((root / 'runtime.lock.json').read_text())
    assert lock['source_commit'] == 'a0dca16975dfe8f5e762703b99d9791a16cf7fd7'
    assert lock['producer_version'] == 'sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0'
    assert contract_metadata.CONTRACT_VERSION == '0.2.14'
    assert contract_metadata.SCHEMA_DIGEST == 'sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59'
    # The current ordinary014-compatible Runtime admits the publication-only
    # producer carrier; the earlier ad97 probe was before that fix.
    daemon = real_runtime(commit=OUTER_RUNTIME_COMMIT)
    host = GenericPackHost(
        pack_roots=[root / 'astrid/packs/video_editing'],
        client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
        executor_id='astrid-pack-host', attempt_root=tmp_path / 'attempts')
    transport = WorkspaceClient(daemon.endpoint, daemon.token)
    transport.handshake('outer-voiceover-admission', '1', [
        'projects:read', 'projects:write', 'objects:read', 'objects:write',
        'tasks:read', 'tasks:write'])
    client = RemoteAstridClient(transport)
    try:
        host.discover()
        host.preflight(OUTER)
        host.register()
        project = client.projects.create(slug='outer-voiceover', name='Outer voiceover',
            idempotency_key='outer-project')
        assert project.ok, project.error
        project_id = project.data.get('project_id') or project.data['id']
        daemon.service.register_timeline_commit_provider(create_runtime_commit_service())
        daemon.service.create_timeline(project_id, 'film', idempotency_key='outer-timeline')
        timeline = daemon.service.get_project_timeline(project_id, 'film')
        target = {'project_id': project_id, 'timeline_id': 'film',
            'base_revision_id': timeline['head_revision_id'],
            'base_publication_id': timeline['head_publication_id']}
        assert all(isinstance(value, str) and value for value in target.values())
        # This is ordinary project object ingestion, not a script authority pin.
        script = transport.ingest_project_object(project_id, b'Long new narration',
            media_type='text/plain', filename='script.txt', idempotency_key='outer-script')
        object_id = script['data']['object_id']
        descriptor = {'name': 'script', 'object_id': object_id, 'digest': object_id,
            'filename': 'script.txt', 'required': True}
        request = {'target': {'kind': 'default'}, 'inputs': [descriptor]}
        submissions = []
        dispatch = transport.dispatch_task_admission

        def record_dispatch(arguments):
            submissions.append(copy.deepcopy(arguments))
            return dispatch(arguments)

        transport.dispatch_task_admission = record_dispatch
        invoked = sdk.invoke(OUTER, kind='executor', project=project_id, client=client,
            inputs={'project': project_id, 'timeline_ref': 'film', 'timing_policy': 'ripple',
                'occurrence_ids': ['o1']},
            wait=False, idempotency_key='outer-normal-submit')
        assert invoked.ok, invoked.error
        ordinary = submissions[0]
        assert ordinary['capability_id'] == OUTER
        assert ordinary['input_object_ids'] == []
        ordinary_task = daemon.service.task(invoked.kernel_task_id)['task']
        with capsys.disabled():
            print('OUTER_NORMAL_TASK_ID=' + invoked.kernel_task_id)
            print('OUTER_NORMAL_SUBMIT=' + json.dumps(ordinary, sort_keys=True))
            print('OUTER_NORMAL_ADMITTED_SPEC=' + json.dumps(ordinary_task['spec'], sort_keys=True))

        # Inspect the accepted bootstrap history read-only.
        history = 'SELECT * FROM timeline_commit_history WHERE project_id=? AND timeline_id=?'
        before = daemon.service.store.conn.execute(history, (project_id, 'film')).fetchall()
        worker = WorkspaceClient(daemon.endpoint, daemon.worker_token)
        # Authorization must refuse before command validation. No substitute
        # voiceover edits or borrowed requester credential belong here.
        with pytest.raises(ApiError) as error:
            worker._generated.commit_timeline(project_id, 'film',
                {'api_version': 1, **target, 'commands': [], 'rationale': 'Worker cannot commit'},
                idempotency_key='outer-worker-denied')
        assert error.value.status == 401
        assert error.value.code == 'unauthorized'
        assert error.value.message == 'credential lacks required scope'
        assert daemon.service.store.conn.execute(history, (project_id, 'film')).fetchall() == before
        assert daemon.service.get_project_timeline(project_id, 'film') == timeline
        with capsys.disabled():
            print('OUTER_WORKER_COMMIT_DENIED=' + str(error.value.status))
        transport._generated.cancel_task(invoked.kernel_task_id, expected_version=None,
            idempotency_key='cancel-' + invoked.kernel_task_id)

        # Preserve the required successful target/script admission, but never
        # invent two continuation children to satisfy the current Runtime.
        spec = copy.deepcopy(ordinary['spec'])
        spec['runtime_dependencies'] = {'publication': {'admitted_target': target}}
        pinned = client.tasks.create(project_id=project_id, capability=OUTER, spec=spec,
            execution_request=request, input_manifest=[object_id], idempotency_key='outer-pinned-submit')
        with capsys.disabled():
            print('OUTER_PINNED_SUBMIT=' + json.dumps(submissions[1], sort_keys=True))
        if (not pinned.ok and pinned.error.code == 'validation_error'
                and pinned.error.message == 'runtime continuation requires exactly two ordered dependency edges'):
            with capsys.disabled():
                print('OUTER_PINNED_ADMISSION_BLOCKED=' + pinned.error.message)
            raise _MissingTargetCarrier(pinned.error.message)
        assert pinned.ok, pinned.error
        task = daemon.service.task(pinned.data['task_id'])['task']
        assert task['capability'] == OUTER
        assert task['spec']['spec']['runtime_dependencies']['publication']['admitted_target'] == target
        assert task['spec']['spec']['inputs']['script'] == descriptor
        assert submissions[1]['input_object_ids'] == [object_id]
        assert submissions[1]['execution_request']['inputs'] == [descriptor]
        with capsys.disabled():
            print('OUTER_PINNED_TASK_ID=' + pinned.data['task_id'])
            print('OUTER_PINNED_ADMITTED_SPEC=' + json.dumps(task['spec'], sort_keys=True))
        transport._generated.cancel_task(pinned.data['task_id'], expected_version=None,
            idempotency_key='cancel-' + pinned.data['task_id'])
    finally:
        host.shutdown()
        daemon.stop()
