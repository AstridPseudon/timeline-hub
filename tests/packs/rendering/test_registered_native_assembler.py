"""Normal admission, actual registered action and native managed-output settlement."""
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
def test_registered_host_settles_native_original_proposal(
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
                           client=worker, executor_id=worker.executor_id, attempt_root=tmp_path / 'host-attempt')
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
            prior = {'id': 'prior', 'clipType': 'text', 'track': 'visual', 'at': 0.0, 'hold': 1.0,
                     'params': {'text': 'Original'}, 'opaque': [1.0, -0.0, False, None]}
            track = {'id': 'visual', 'kind': 'visual', 'label': 'Original lane', 'opaque': [False, 1.0]}
            if duplicate_cas:
                session.commit_many([
                    {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
                     'args': {'row': track}},
                    {'schema_version': 1, 'op': 'clip.add', 'version': '1', 'select': 'parent',
                     'args': {'row': prior}},
                ], idempotency_key='original-content')
            replace_clips = ['parent/clip:prior'] if duplicate_cas else []
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
            result = session.admit_assembly(selectors, replace_clips=replace_clips, assembler_digest=record.capability_digest,
                                            idempotency_key='assembly', rationale='Ordered café visuals 1.0')
            author = result['data']['task_id']
            task = service.task(author)['task']
            public = task['spec']['spec']
            capture = public['inputs']['resolved_children']
            assert capture['admitted_target'] == {
                'project_id': project, 'timeline_id': 'main',
                'base_revision_id': original['revision_id'], 'base_publication_id': original['publication_id']}
            assert capture['bundle']['base_parent']['revision_id'] == original['revision_id']
            assert capture['bundle']['parent']['config']['tracks'] == ([track] if duplicate_cas else [])
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
            before = service.list_timeline_commits(project, 'main', authorize=lambda: None)
            calls = []

            def observe(target, name):
                operation = getattr(target, name)

                def delegated(*args, **kwargs):
                    calls.append(name)
                    return operation(*args, **kwargs)

                monkeypatch.setattr(target, name, delegated)

            for name in ('publish_timeline_render', 'upload_object', 'settle'):
                observe(worker, name)
            observe(host, '_upload_outputs')
            host.run_task({'task': {**task, 'project_id': project, 'run_id': claim.run_id,
                                    'runtime_epoch': claim.runtime_epoch}},
                          lease_token=claim.lease_id, attempt_id=claim.attempt_id,
                          fence=claim.fence, keep_attempt=True)
            attempt = tmp_path / 'host-attempt'
            assembled_input = json.loads((attempt / 'inputs/resolved-children.json').read_bytes())
            proposal = json.loads((attempt / 'outputs/authoring-proposal.json').read_bytes())
            from astrid.packs.rendering.actions.assemble_timeline.run import (
                TimelineAuthoringError,
                build_authoring_proposal,
                build_native_proposal,
                derive_asset_key,
                derive_clip_id,
            )
            from astrid.sdk.timeline.commands import _VALIDATOR, execute
            from astrid.sdk.timeline.commit import _digest
            assert not list(_VALIDATOR.evolve(schema={'$ref': '#/$defs/SettledProducerProposal'}).iter_errors(proposal))
            assert proposal['admitted_target'] == capture['admitted_target']
            assert proposal['producer'] == {'task_id': author, 'attempt_id': claim.attempt_id,
                'executor_id': worker.executor_id, 'fence': claim.fence, 'runtime_epoch': claim.runtime_epoch}
            assert proposal['rationale'] == 'Ordered café visuals 1.0'
            assert proposal['proposal_digest'] == _digest({key: value for key, value in proposal.items()
                                                          if key != 'proposal_digest'})
            commands = proposal['commands']
            assert commands[0]['op'] == 'timeline.assembled-target'
            assert commands[0]['args'] == {'replace_clips': replace_clips}
            assert commands[0]['selections']
            if duplicate_cas:
                assert any(read['ref'] == 'parent/clip:prior' and read['path'] == []
                           and read['state']['value'] == prior for read in commands[0]['reads'])
                assert [call['select'] for call in commands if call['op'] == 'clip.delete'] == replace_clips
            additions = [call for call in commands if call['op'] == 'clip.add-media']
            assert [call['args']['row']['id'] for call in additions] == [derive_clip_id(author, i) for i in range(2)]
            assert [call['args']['row']['asset'] for call in additions] == [derive_asset_key(author, i) for i in range(2)]
            assert [call['args']['media'] for call in additions] == [row['media'] for row in capture['children']]
            assert [call['args']['row']['at'] for call in additions] == [0.0, 2.0]
            assert all(call['args']['row']['hold'] == 2.0 and call['reads'] and call['bindings']
                       and call['created'] and call['selections'] for call in additions)
            replay = execute(capture['bundle'], commands,
                             verified_media=[row['verified_media'] for row in capture['children']])
            assert replay.commands == commands
            if duplicate_cas:
                assert replay.bundle['parent']['config']['tracks'] == [track]
            # Captured inputs stay exact, including reversed completion and duplicate CAS.
            import copy
            for change in ('association', 'version', 'order', 'selection', 'duration'):
                wrong = copy.deepcopy(assembled_input)
                if change == 'association':
                    wrong['associations'][0]['association_id'] = 'other'
                elif change == 'version':
                    wrong['associations'][0]['lifecycle']['version'] += 1
                elif change == 'order':
                    wrong['capture']['children'].reverse()
                elif change == 'selection':
                    wrong['capture']['children'][0]['verified_media']['selection']['variant_id'] = 'other'
                else:
                    wrong['capture']['children'][0]['verified_media']['duration_seconds'] = True
                with pytest.raises(TimelineAuthoringError, match='exact ordered verified'):
                    build_native_proposal(wrong, build_authoring_proposal(wrong))
            assert service.list_timeline_commits(project, 'main', authorize=lambda: None) == before
            assert 'publish_timeline_render' not in calls
            # Small JSON files use the normal inline settlement transport;
            # larger files use upload_object inside the same host output path.
            assert calls[0] == '_upload_outputs' and calls[-1] == 'settle'
            settled = service.task(author)['task']
            assert settled['status'] == 'completed'
            output, = [row for row in settled['result']['outputs'] if row['name'] == 'authoring_proposal']
            raw = service.object(output['digest'])[1]
            assert json.loads(raw) == proposal
            assert output['digest'] == 'sha256:' + hashlib.sha256(raw).hexdigest()
            associations = service.managed_outputs(author)
            managed, = [row for row in associations if row['output_port'] == 'authoring_proposal']
            assert managed['attempt_id'] == claim.attempt_id and managed['object_id'] == output['digest']
            assert managed['durability'] == 'durable' and managed['media_type'] == 'application/json'
            assert managed['lifecycle']['state'] == 'available'
            assert service.list_timeline_commits(project, 'main', authorize=lambda: None) == before

    finally:
        host.shutdown()
        daemon.stop()
