"""Real settled, media-free producer through RuntimeService and the native provider.

This uses a generic producer, not the assembler's ordered visual continuation.
The Runtime checkout is selected through the normal integration-test locator.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline import build_producer_batch, commit
from astrid.sdk.timeline.capture import capture_track_create
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def settle_output(service, attempt, raw, name, media_type, key):
    service.settle_attempt(attempt['attempt_id'], {
        **{field: attempt[field] for field in ('lease_id', 'fence', 'runtime_epoch')},
        'outputs': [{'name': name, 'output_port': name, 'kind': 'object', 'filename': name + '.json',
                     'digest': 'sha256:' + hashlib.sha256(raw).hexdigest(), 'size': len(raw),
                     'media_type': media_type, 'durability': 'durable',
                     'data_base64': base64.b64encode(raw).decode('ascii')}]}, idempotency_key=key)


@pytest.fixture
def settled(tmp_path):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    case = SimpleNamespace(service=service, root=root)
    try:
        service.register_timeline_commit_provider(commit.create_runtime_commit_service())
        project = service.create_project({'slug': 'settled', 'name': 'Settled'})['id']
        service.create_timeline(project, 'film', idempotency_key='timeline')
        timeline = service.get_project_timeline(project, 'film')
        target = {'project_id': project, 'timeline_id': 'film',
                  'base_revision_id': timeline['head_revision_id'],
                  'base_publication_id': timeline['head_publication_id']}
        capability = 'fixture.propose-track'
        digest = commit._digest(capability)
        service.register_capability({'capability_id': capability, 'definition_digest': digest})
        child_capability = 'fixture.producer-input'
        child_digest = commit._digest(child_capability)
        service.register_capability({'capability_id': child_capability, 'definition_digest': child_digest})
        service.register_executor({'executor_id': 'worker', 'capabilities': [capability, child_capability]},
                                  idempotency_key='executor')
        children = []
        for index in range(2):
            child = service.create_task({'project': project, 'capability_id': child_capability,
                'capability_digest': child_digest, 'input_object_ids': [], 'spec': {'index': index},
                'idempotency_key': f'input-{index}'})
            claim = service.claim_next({'executor_id': 'worker', 'capability_ids': [child_capability],
                'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key=f'claim-input-{index}')
            settle_output(service, claim, commit._json({'index': index}).encode('utf-8'),
                          'data', 'application/json', f'settle-input-{index}')
            children.append(child['task']['id'])
        task = service.create_task({'project': project, 'capability_id': capability,
            'capability_digest': digest, 'input_object_ids': [], 'idempotency_key': 'task',
            'spec': {'runtime_dependencies': {'publication': {'admitted_target': target},
                'edges': [{'from_task_id': child, 'to': 'self', 'requires_event': 'task.succeeded',
                           'fence': 'runtime_task'} for child in children],
                'aggregation': {'kind': 'ordered_cas_inputs'}},
                     'outputs': {'authoring_proposal': {
                         'type': 'file', 'artifact_type': 'timeline/authoring-proposal'}}}})
        attempt = service.claim_next({'executor_id': 'worker', 'capability_ids': [capability],
            'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='claim')
        assert attempt['task_id'] == task['task']['id']
        document = service._timeline_commits()[0].revision_closure(
            project, 'film', target['base_revision_id'])
        commands = [capture_track_create(commit.bundle_from_document(document), 'parent',
            {'id': 'proposed', 'kind': 'visual', 'opaque': [1.0, -0.0, False]})]
        proposal = {'schema_version': 1, 'producer': {
            'task_id': attempt['task_id'], 'attempt_id': attempt['attempt_id'],
            'executor_id': 'worker', 'fence': attempt['fence'], 'runtime_epoch': attempt['runtime_epoch']},
            'admitted_target': target, 'rationale': 'Reviewed café', 'commands': commands}
        proposal['proposal_digest'] = commit._digest(proposal)
        raw = commit._json(proposal).encode('utf-8')
        settle_output(service, attempt, raw, 'authoring_proposal', 'application/json', 'settle')
        case.proposal, case.target = proposal, target
        yield case
    finally:
        case.service.close()


def body(case):
    return {'api_version': 1, **build_producer_batch(case.proposal)}


def submit(case, request, key):
    from runtime_protocol.timeline_commit_port import route_path

    return case.service.commit_timeline(case.target['project_id'], 'film', request,
        idempotency_key=key, publisher='requester',
        invocation_path=route_path(case.target['project_id'], 'film'), authorize=lambda: None)


# D13 qualification requires Runtime to accept the native recorder's guard
# metadata; 6023cfb compares that record to the necessarily bare request guard.
@pytest.mark.xfail(strict=True, reason='D13: Runtime must accept native captured producer.guard records')
def test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes(settled):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService

    case = settled
    original = body(case)
    forwarded = subprocess.run(['node', '-e',
        'process.stdout.write(JSON.stringify(JSON.parse(require("fs").readFileSync(0,"utf8"))))'],
        input=commit._json(original), text=True, capture_output=True, check=True, timeout=15)
    request = json.loads(forwarded.stdout)
    assert type(original['commands'][1]['args']['row']['opaque'][0]) is float
    assert type(request['commands'][1]['args']['row']['opaque'][0]) is int
    assert request['commands'][0]['args']['pin']['proposal_digest'] == case.proposal['proposal_digest']
    preview = submit(case, {**request, 'dry_run': True}, 'preview')
    assert preview['data']['status'] == 'preview' and preview['receipt'] is None
    accepted = submit(case, request, 'accept')
    assert accepted['data']['status'] == 'accepted'
    assert accepted['data']['canonical_document']['parent_revision']['payload']['config']['tracks'] == [
        request['commands'][1]['args']['row']]
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    assert submit(case, request, 'accept') == accepted
    with pytest.raises(RuntimeErrorBase) as error:
        submit(case, request, 'second-key')
    assert error.value.details['reason'] == 'producer_proposal_consumed'
    current = {'base_revision_id': accepted['data']['accepted_revision_id'],
               'base_publication_id': accepted['receipt']['receipt_id']}
    inverse = {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
               'args': {'publications': [accepted['receipt']['receipt_id']]}}
    undone = submit(case, {**request, **current, 'commands': [inverse]}, 'undo')
    assert undone['data']['canonical_document']['parent_revision']['payload']['config']['tracks'] == []


@pytest.mark.parametrize('mutation', ['number', 'boolean', 'reason', 'digest'])
def test_settled_artifact_mutation_refuses_without_history_or_head_changes(settled, mutation):
    from runtime_protocol.errors import RuntimeErrorBase

    case = settled
    request = copy.deepcopy(body(case))
    if mutation in ('number', 'boolean'):
        request['commands'][1]['args']['row']['opaque'][0] = 2 if mutation == 'number' else True
    elif mutation == 'reason':
        request['rationale'] = 'Changed'
    else:
        request['commands'][0]['args']['pin']['proposal_digest'] = 'sha256:' + 'f' * 64
    before = case.service.list_timeline_commits(case.target['project_id'], 'film', authorize=lambda: None)
    with pytest.raises(RuntimeErrorBase) as error:
        submit(case, request, 'mutated')
    assert error.value.details['reason'] in {'producer_dependency_unavailable', 'producer_attempt_mismatch'}
    assert case.service.list_timeline_commits(
        case.target['project_id'], 'film', authorize=lambda: None) == before
