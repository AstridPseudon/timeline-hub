"""Real requester admission and claim; child media settlements are input fixtures."""
from __future__ import annotations

import copy
import hashlib
import json
from contextlib import ExitStack
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.helpers.runtime import use_runtime


@pytest.mark.integration
@pytest.mark.parametrize('duplicate_cas', [False, True])
@pytest.mark.parametrize('recovery', [None, 'lost-ack', 'cleanup'])
def test_authorized_session_admits_registered_assembler_with_original_capture(
    tmp_path, monkeypatch, real_runtime, duplicate_cas, recovery,
):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from runtime_protocol.server import RuntimeHandler
    from test_generation_publish_v1_settlement import _effect, _output, _settle

    observed = []
    send = RuntimeHandler._send

    def observe(handler, status, payload=None, **kwargs):
        if (handler.command == 'POST' and handler.path == '/v1/tasks'
                and handler.headers.get('Idempotency-Key') == 'assembly'
                and getattr(handler, '_defer_response', False)):
            flight = json.loads((tmp_path / 'requester.json').read_bytes())['flight']
            assert flight['body'].encode() == handler._prefetched_body
            assert flight['key'] == handler.headers['Idempotency-Key']
            observed.append((handler._prefetched_body, copy.deepcopy(payload)))
            if recovery == 'lost-ack' and len(observed) == 1 and status == 201:
                raise ConnectionError('lost task admission ACK after durable acceptance')
        return send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, '_send', observe)

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
        with ExitStack() as clients:
            client = clients.enter_context(open_client(daemon))
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
            def admit():
                return session.admit_assembly(selectors, replace_clips=[], assembler_digest=record.capability_digest,
                                              idempotency_key='assembly', rationale='Ordered café visuals 1.0')

            if recovery:
                before = session.outbox.read()
                write = session.outbox.write

                def fail_cleanup(state):
                    if state['flight'] is None:
                        raise OSError('crash after admission ACK before cleanup')
                    write(state)

                with monkeypatch.context() as patch:
                    if recovery == 'cleanup':
                        patch.setattr(session.outbox, 'write', fail_cleanup)
                    with pytest.raises(WorkspaceClientError if recovery == 'lost-ack' else OSError):
                        admit()
                assert len(observed) == 1
                persisted = session.outbox.path.read_bytes()
                accepted = observed[0][1]
                author = accepted['data']['task_id']
                accepted_task = service.task(author)
                # Advance actual accepted history to C and lifecycle to V2 after
                # original admission. Retry must still send the V1 closure.
                peer.commit({'schema_version': 1, 'op': 'track.set', 'version': '1',
                             'select': 'parent/track:peer',
                             'args': {'values': {'label': 'Head C'}, 'clear': []}},
                            idempotency_key='head-c')
                changed = service.update_managed_output_lifecycle(selectors[0]['association_id'],
                    {'operation': 'pin', 'expected_version': 1}, idempotency_key='child-v2')
                assert changed['data']['version'] == 2
                accepted_history = client.timelines.history(project, 'main', limit=100).as_dict()
                instance, realm, port = daemon.instance_id, daemon.root, daemon.httpd.server_port
                daemon.stop()
                daemon = real_runtime(realm, support_root=tmp_path / 'support', port=port,
                                      authoring_profile='astrid')
                assert daemon.instance_id != instance
                service = daemon.service
                _, credential = daemon.credentials.provision('owner', [
                    'handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write',
                    'tasks:read', 'tasks:write'])
                client = clients.enter_context(open_client(daemon, credential=credential))

                def no_recapture(*args, **kwargs):
                    raise AssertionError('admission recovery reread the head or child media')

                with monkeypatch.context() as patch:
                    patch.setattr(client.timelines, 'open_composition', no_recapture)
                    patch.setattr(client.timelines, 'history', no_recapture)
                    session = TimelineSession.open(project, 'main', client=client, outbox_path=session.outbox.path)
                assert session.outbox.path.read_bytes() == persisted
                _, foreign_credential = daemon.credentials.provision('other-editor', [
                    'handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write',
                    'tasks:read', 'tasks:write'])
                foreign = clients.enter_context(open_client(daemon, actor='other-editor', credential=foreign_credential))
                with pytest.raises(TimelineEditError, match='different realm, actor, project or timeline'):
                    TimelineSession.open(project, 'main', client=foreign, outbox_path=session.outbox.path)
                assert session.outbox.path.read_bytes() == persisted
                transport = client._remote._transport
                assert transport.get_managed_output(selectors[0]['association_id'])['lifecycle']['version'] == 2
                for mutation in ('key', 'child', 'rationale', 'digest', 'replacement', 'order'):
                    changed_selectors = copy.deepcopy(selectors)
                    args = {'replace_clips': [], 'assembler_digest': record.capability_digest,
                            'idempotency_key': 'assembly', 'rationale': 'Ordered café visuals 1.0'}
                    if mutation == 'key':
                        args['idempotency_key'] = 'other'
                    elif mutation == 'child':
                        changed_selectors[0]['version'] = 2
                    elif mutation == 'rationale':
                        args['rationale'] = 'Changed'
                    elif mutation == 'digest':
                        args['assembler_digest'] = 'sha256:' + 'f' * 64
                    elif mutation == 'replacement':
                        args['replace_clips'] = ['parent/clip:other']
                    else:
                        changed_selectors.reverse()
                    with pytest.raises(TimelineEditError, match='immutable'):
                        session.admit_assembly(changed_selectors, **args)
                    assert session.outbox.path.read_bytes() == persisted and len(observed) == 1

                if recovery == 'cleanup':
                    pending = session.queue({'schema_version': 1, 'op': 'track.create', 'version': '1',
                        'select': 'parent', 'args': {'row': {'id': 'local-unsent', 'kind': 'visual'}}})
                    before = {**before, 'pending': [pending]}

                with monkeypatch.context() as patch:
                    patch.setattr(session, '_bundle', no_recapture)
                    patch.setattr(client.tasks, 'prepare_admission', no_recapture)
                    for name in ('get_managed_output', 'get_project_media_selection', 'get_project_verified_media'):
                        patch.setattr(transport, name, no_recapture)
                    result = admit()
                assert len(observed) == 2 and observed[0][0] == observed[1][0]
                assert result['receipt'] == accepted['receipt']
                assert result['data']['task_id'] == author
                assert session.outbox.read() == before
                assert service.task(author) == accepted_task
                tasks, cursor = transport.list_project_tasks(project, limit=100)
                assert cursor is None and len(tasks) == 3
                assert [row['task_id'] for row in tasks if row['capability_id'] == record.id] == [author]
                assert client.timelines.history(project, 'main', limit=100).as_dict() == accepted_history
            else:
                result = admit()
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
            if recovery:
                assert capture['rationale'] == 'Ordered café visuals 1.0'
                assert [row['association'] for row in capture['children']] == selectors
                # Leave the admitted task intact; its V1 request is not a new
                # authoring publication or permission to refresh child inputs.
                return
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
