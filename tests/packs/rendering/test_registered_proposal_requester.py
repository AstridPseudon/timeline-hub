"""Authorized requester consumes real registered artifacts through the normal outbox."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.packs.rendering.test_registered_native_assembler import registered_assembly

pytestmark = pytest.mark.integration


def history(case):
    result = case.client.timelines.history(case.project, 'main', limit=100)
    assert result.ok, result.as_dict()
    return result.data


def queue(case):
    return case.session.queue_assembly(case.author, attempt_id=case.claim.attempt_id)


@pytest.mark.parametrize('duplicate_cas', [False, True])
def test_registered_requester_lost_ack_restart_exact_retry_history_and_inverse(
    tmp_path, monkeypatch, real_runtime, duplicate_cas,
):
    from tests.helpers.runtime import use_runtime

    use_runtime()
    from runtime_protocol.server import RuntimeHandler

    observed = []
    send = RuntimeHandler._send

    def lose_ack(handler, status, payload=None, **kwargs):
        if (handler.command == 'POST' and handler.path.endswith('/commit')
                and handler.headers.get('Idempotency-Key') == 'proposal-commit' and status == 200
                and getattr(handler, '_defer_response', False)):
            observed.append((handler._prefetched_body, copy.deepcopy(payload)))
            if status == 200 and len(observed) == 1:
                raise ConnectionError('registered requester lost ACK after durable acceptance')
        return send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, '_send', lose_ack)
    with registered_assembly(tmp_path, monkeypatch, real_runtime, duplicate_cas, peer_edit='label') as case:
        before = history(case)
        transport = case.client._remote._transport
        peer_payload = transport.get_project_parent_composition_revision(
            case.project, 'main', case.peer.outbox.read()['base']['revision_id'])['payload']
        original_outbox = case.session.outbox.path.read_bytes()
        # Corrupted downloads never reach the outbox or a commit, even when the
        # decoded JSON would be equivalent. Hash the stored bytes first.
        get_object = transport.get_object
        with monkeypatch.context() as patch:
            patch.setattr(transport, 'get_object', lambda object_id: {'data': case.raw + b' '})
            with pytest.raises(TimelineEditError, match='unavailable or changed'):
                queue(case)
        assert case.session.outbox.path.read_bytes() == original_outbox
        assert get_object(case.managed['object_id'])['data'] == case.raw
        with pytest.raises(TimelineEditError, match='unavailable or changed'):
            case.session.queue_assembly(case.author, attempt_id='other-attempt')
        list_outputs = transport.list_managed_outputs
        for mutation in ('attempt', 'lifecycle', 'fence'):
            rows, cursor = copy.deepcopy(list_outputs(case.author))
            row, = [item for item in rows if item['output_port'] == 'authoring_proposal']
            if mutation == 'attempt':
                row['attempt_id'] = 'other-attempt'
            elif mutation == 'lifecycle':
                row['lifecycle']['state'] = 'superseded'
            else:
                row['provenance']['fence'] += 1
            with monkeypatch.context() as patch:
                patch.setattr(transport, 'list_managed_outputs', lambda task_id: [rows, cursor])
                with pytest.raises(TimelineEditError, match='unavailable or changed'):
                    queue(case)
            assert case.session.outbox.path.read_bytes() == original_outbox
        # A changed decoded value under the real settled producer pin is also
        # refused by Runtime, independently of the requester's byte checks.
        from astrid.sdk.timeline.producer import build_producer_batch
        for mutation in ('value', 'rationale', 'digest'):
            changed = build_producer_batch(case.proposal)
            if mutation == 'value':
                addition = next(row for row in changed['commands'] if row['op'] == 'clip.add-media')
                addition['args']['row']['hold'] = 3
            elif mutation == 'rationale':
                changed['rationale'] = 'Changed rationale'
            else:
                changed['commands'][0]['args']['pin']['proposal_digest'] = 'sha256:' + 'f' * 64
            refusal = case.client.timelines.commit(case.project, 'main', {'api_version': 1, **changed},
                                                   idempotency_key='changed-proposal-' + mutation)
            assert not refusal.ok
        assert history(case) == before
        queued = queue(case)
        assert queued[0]['op'] == 'producer.guard'
        assert queued[0]['args']['pin'] == {**case.proposal['producer'],
            'admitted_target': case.proposal['admitted_target'],
            'proposal_digest': case.proposal['proposal_digest']}
        assert queued[1:] == case.proposal['commands']
        state = case.session.outbox.read()
        assert state['base'] == case.original
        assert state['rationale'] == case.proposal['rationale']
        with pytest.raises(TimelineEditError, match='flush the producer'):
            case.session.queue_move('parent/clip:missing', 1)
        with pytest.raises(WorkspaceClientError):
            case.session.flush(idempotency_key='proposal-commit')
        assert len(observed) == 1 and observed[0][1]['data']['status'] == 'rebased'
        persisted = case.session.outbox.path.read_bytes()
        flight = case.session.outbox.read()['flight']
        assert flight['body'].encode() == observed[0][0]
        body = json.loads(flight['body'])
        assert body['commands'] == queued and body['rationale'] == case.proposal['rationale']
        assert body['base_revision_id'] == case.original['revision_id']
        assert body['base_publication_id'] == case.original['publication_id']
        accepted = observed[0][1]
        accepted_history = history(case)
        changed_flight = copy.deepcopy(body)
        changed_flight['rationale'] = 'Changed under the original retry key'
        refusal = case.client.timelines.commit(case.project, 'main', changed_flight,
                                               idempotency_key=flight['key'])
        assert not refusal.ok
        assert history(case) == accepted_history
        assert case.session.outbox.path.read_bytes() == persisted
        assert len(accepted_history['items']) == len(before['items']) + 1
        assert accepted['data']['rationale'] == case.proposal['rationale']
        entry = next(row for row in accepted_history['items']
                     if row['publication_id'] == accepted['receipt']['receipt_id'])
        assert entry['publisher'] == 'owner' and entry['receipt'] == accepted['receipt']
        assert entry['rationale'] == case.proposal['rationale']
        assert [row['command'] for row in entry['records']['commands']] == accepted['data']['commands']
        # Both requester process state and Runtime are discarded before retry.
        realm, port = case.daemon.root, case.daemon.httpd.server_port
        case.daemon.stop()
        restarted = real_runtime(realm, support_root=tmp_path / 'support', port=port, authoring_profile='astrid')
        with open_client(restarted) as client:
            session = TimelineSession.open(case.project, 'main', client=client,
                                            outbox_path=case.session.outbox.path)
            assert session.outbox.path.read_bytes() == persisted
            with pytest.raises(TimelineEditError, match='immutable'):
                session.flush(idempotency_key='different-key')
            assert session.outbox.path.read_bytes() == persisted
            retried = session.flush()
            assert retried['receipt'] == accepted['receipt']
            assert len(observed) == 2 and observed[0] == observed[1]
            case.client = client
            assert history(case) == accepted_history
            state = session.outbox.read()
            assert not state['pending'] and state['flight'] is None and 'rationale' not in state
            revision = accepted['data']['accepted_revision_id']
            stored = client._remote._transport.get_project_parent_composition_revision(case.project, 'main', revision)
            assert stored['payload'] == accepted['data']['canonical_document']['parent_revision']['payload']
            clips = stored['payload']['clips']
            assert len(clips) == 2 and [row['at'] for row in clips] == [0.0, 2.0]
            assert len({row['asset'] for row in clips}) == 2
            assert len({row['id'] for row in clips}) == 2
            undo = session.undo([accepted['receipt']['receipt_id']], idempotency_key='undo-proposal')
            payload = undo['data']['canonical_document']['parent_revision']['payload']
            assert payload == peer_payload
            assert next(row for row in payload['config']['tracks'] if row['id'] == 'peer')['label'] == 'After peer edit'
            assert client._remote._transport.get_project_parent_composition_revision(
                case.project, 'main', revision) == stored
            assert next(row for row in history(case)['items']
                        if row['publication_id'] == entry['publication_id']) == entry


def test_registered_requester_keeps_original_membership_guards_on_peer_conflict(
    tmp_path, monkeypatch, real_runtime,
):
    with registered_assembly(tmp_path, monkeypatch, real_runtime, True, peer_edit='conflict') as case:
        before = history(case)
        queued = queue(case)
        with pytest.raises(CommitConflict):
            case.session.flush(idempotency_key='conflicting-proposal')
        assert history(case) == before
        state = case.session.outbox.read()
        assert state['base'] == case.original and state['pending'] == queued
        assert json.loads(state['flight']['body'])['commands'] == queued


def test_cancelled_registered_attempt_cannot_supply_requester_authority(tmp_path, monkeypatch, real_runtime):
    with registered_assembly(tmp_path, monkeypatch, real_runtime, False, cancel=True) as case:
        before = history(case)
        persisted = case.session.outbox.path.read_bytes()
        with pytest.raises(TimelineEditError, match='unavailable or changed'):
            queue(case)
        assert case.service.managed_outputs(case.author) == []
        assert history(case) == before
        assert case.session.outbox.path.read_bytes() == persisted


def test_registered_requester_inverse_refuses_intervening_edit(tmp_path, monkeypatch, real_runtime):
    with registered_assembly(tmp_path, monkeypatch, real_runtime, True, peer_edit='label') as case:
        queue(case)
        accepted = case.session.flush(idempotency_key='accept-proposal')
        clip = accepted['data']['canonical_document']['parent_revision']['payload']['clips'][0]
        peer = TimelineSession.open(case.project, 'main', client=case.client, outbox_path=tmp_path / 'later-peer.json')
        peer.queue_move('parent/clip:' + clip['id'], 1)
        peer.flush(idempotency_key='peer-touches-born-clip')
        before = history(case)
        with pytest.raises(CommitConflict):
            case.session.undo([accepted['receipt']['receipt_id']], idempotency_key='guarded-undo')
        assert history(case) == before
