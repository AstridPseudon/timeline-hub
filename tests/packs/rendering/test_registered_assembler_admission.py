"""Real requester admission and claim; child media settlements are input fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.sdk.timeline.sync import TimelineSession
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.helpers.runtime import use_runtime


@pytest.mark.integration
@pytest.mark.parametrize('duplicate_cas', [False, True])
def test_authorized_session_admits_registered_assembler_with_original_capture(
    tmp_path, monkeypatch, real_runtime, duplicate_cas,
):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from test_generation_publish_v1_settlement import _effect, _output, _settle

    daemon = real_runtime(authoring_profile='astrid')
    service = daemon.service
    worker = RuntimeProtocolClient(daemon.endpoint, daemon.worker_token)
    worker.executor_id = 'astrid-pack-host'
    host = GenericPackHost(pack_roots=[Path(__file__).resolve().parents[3] / 'astrid/packs/rendering'],
                           client=worker, executor_id=worker.executor_id)
    try:
        host.discover()
        host.preflight('rendering.assemble_timeline')
        record = host.capabilities['rendering.assemble_timeline']
        service.register_capability({'capability_id': record.id, 'definition_digest': record.capability_digest})
        child_capability = 'fixture.registered-visual'
        child_digest = 'sha256:' + hashlib.sha256(child_capability.encode()).hexdigest()
        service.register_capability({'capability_id': child_capability, 'definition_digest': child_digest})
        service.register_executor({'executor_id': worker.executor_id,
                                  'capabilities': [child_capability, record.id], 'max_concurrency': 3},
                                 idempotency_key='executor')
        project = service.create_project({'slug': 'assembly', 'name': 'Assembly'})['id']
        service.create_timeline(project, 'main', idempotency_key='timeline')
        with open_client(daemon) as client:
            session = TimelineSession.open(project, 'main', client=client, outbox_path=tmp_path / 'requester.json')
            original = session.outbox.read()['base']
            children, effects = [], []
            for index in range(2):
                effect = _effect(project, groups=[{'group_key': 'main', 'selectors': [
                    {'selector': 'visual', 'ordinal': 0, 'variant_key': 'visual', 'output_port': 'video'}]}])
                effect['payload']['metadata']['params'] = {'duration_seconds': 2}
                effects.append(effect)
                children.append(service.create_task({'project': project, 'capability_id': child_capability,
                    'capability_digest': child_digest, 'settlement_effect': effect,
                    'idempotency_key': f'child-{index}'})['task']['id'])
            claims = [service.claim_next({'executor_id': worker.executor_id,
                'capability_ids': [child_capability], 'runtime_epoch': service.health()['runtime_epoch']},
                idempotency_key=f'claim-child-{index}') for index in range(2)]
            by_task = {claim['task_id']: claim for claim in claims}
            for index in (1, 0):
                raw = b'shared visual fixture' if duplicate_cas else f'visual fixture {index}'.encode()
                output = _output(raw, output_port='video', group_key='main', variant_key='visual', ordinal=0,
                                 media_type='video/mp4', role='primary', is_primary=True,
                                 filename=f'visual-{index}.mp4', duration_seconds=2)
                _settle(service, by_task[children[index]], [output], effect=effects[index], key=f'settle-{index}')
            selectors = [{key: association[key] for key in ('association_id', 'object_id')} | {
                'version': association['lifecycle']['version']}
                for child in children for association in service.managed_outputs(child)]
            peer = TimelineSession.open(project, 'main', client=client, outbox_path=tmp_path / 'peer.json')
            peer.commit({'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
                         'args': {'row': {'id': 'peer', 'kind': 'visual'}}}, idempotency_key='peer-track')
            result = session.admit_assembly(selectors, replace_clips=[], assembler_digest=record.capability_digest,
                                            idempotency_key='assembly')
            author = result['data']['task_id']
            task = service.task(author)['task']
            public = task['spec']['spec']
            capture = public['inputs']['resolved_children']
            assert capture['admitted_target'] == {
                'project_id': project, 'timeline_id': 'main',
                'base_revision_id': original['revision_id'], 'base_publication_id': original['publication_id']}
            assert capture['bundle']['base_parent']['revision_id'] == original['revision_id']
            assert capture['bundle']['parent']['config']['tracks'] == []
            assert public['outputs']['authoring_proposal'] == {
                'type': 'file', 'artifact_type': 'timeline/authoring-proposal'}
            claim = worker.claim_next(executor_id=worker.executor_id, capability_ids=[record.id],
                                      idempotency_key='claim-assembler')
            assert claim.task_id == author
            task = service.task(author)['task']
            assert len(task['spec']['input_object_ids']) == (1 if duplicate_cas else 2)
            values = host._materialize_inputs(task['spec'], tmp_path / 'attempt', continuation_id=author)
            envelope = json.loads(Path(values['resolved_children']).read_text())
            assert envelope['capture'] == capture
            assert [row['task_id'] for row in capture['children']] == children
            assert [row['association'] for row in capture['children']] == selectors
            assert len(envelope['aggregation']['order']) == 2
            assert all(row['verified_media']['selection'] == row['media'] for row in capture['children'])
    finally:
        host.shutdown()
        daemon.stop()
