"""Bounded original SDK verbs through the generated client and Runtime HTTP.

Manager-run only, using the current qualified Runtime/public Composition pair.
The first two cases inject the real HTTP handler transport; the ambiguity case
uses the existing live Runtime fixture. Neither is run by this worker.
"""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance import test_commit_runtime_m1 as m1
from tests.editing_conformance import test_native_batch_ingress as ingress
from tests.editing_conformance.test_native_sheet_current_runtime import seed

pytestmark = pytest.mark.integration
runtime = ingress.runtime
film = m1.film
REF = 'parent/clip:title'


def attach(runtime, name='owned'):
    return Checkout.attach(runtime.session(name=name))


def test_http_original_sdk_move_publish_disjoint_rebase_reload_undo(runtime):
    seed(runtime)
    tl = attach(runtime)
    original = copy.deepcopy(tl.clip(REF).data)
    base = copy.deepcopy(runtime.history()['head'])
    runtime.session(name='peer').commit(ingress.label('Peer label'))
    assert tl.clip(REF).on(3.017).start == pytest.approx(tl.quantize(3.017))
    captured = json.loads(tl.session.outbox.path.read_bytes())['pending']
    accepted = tl.publish('Make room for the opening', idempotency_key='sdk-parent-move')
    data = accepted['receipt']['result']
    body = json.loads(runtime.calls[-1][0])
    assert body['base_revision_id'] == base['revision_id']
    assert body['base_publication_id'] == base['publication_id']
    assert body['commands'] == captured == data['commands']
    assert body['rationale'] == data['rationale'] == accepted['message'] == 'Make room for the opening'
    assert data['status'] == 'rebased'
    runtime.restart()
    loaded = attach(runtime)
    assert loaded.clip(REF).start == tl.clip(REF).start
    stored = runtime.client().timelines.open_bundle(runtime.project, 'film', revision_id=accepted['new_head'])
    assert State(stored.data['bundle']).entity(REF) == loaded.clip(REF).data
    loaded.undo([accepted['receipt']['receipt_id']])
    assert loaded.clip(REF).data == original
    assert State(loaded.bundle).entity('parent/track:picture')['label'] == 'Peer label'


def test_http_lost_ack_restart_exact_retry_and_unrelated_global_nonconsumption(runtime):
    seed(runtime)
    tl = attach(runtime)
    tl.clip(REF).on(2)
    runtime.lost.add('sdk-once')
    with pytest.raises(WorkspaceClientError):
        tl.publish('Opening', idempotency_key='sdk-once')
    first = copy.deepcopy(runtime.calls[-1])
    path = tl.session.outbox.path
    durable = path.read_bytes()
    count = len(runtime.history()['items'])
    runtime.restart()
    # A CLI/global move is distinct from this explicitly selected draft.
    global_session = TimelineSession.open(runtime.project, 'film', client=runtime.client())
    global_session.queue_move(REF, 4)
    global_bytes = global_session.outbox.path.read_bytes()
    calls = len(runtime.calls)
    with pytest.raises(TimelineEditError, match='held'):
        Checkout.attach(global_session).publish()
    with pytest.raises(TimelineEditError, match='held'):
        attach(runtime, 'unrelated').publish()
    assert path.read_bytes() == durable
    assert global_session.outbox.path.read_bytes() == global_bytes
    assert len(runtime.calls) == calls and runtime.calls[-1] == first
    loaded = attach(runtime)
    with pytest.raises(TimelineEditError, match='immutable'):
        loaded.publish('Changed reason')
    with pytest.raises(TimelineEditError, match='immutable'):
        loaded.publish(idempotency_key='changed-key')
    assert path.read_bytes() == durable
    accepted = loaded.publish()
    assert runtime.calls[-1][:2] == first[:2]
    assert accepted['receipt'] == first[3]['receipt']
    assert accepted['message'] == 'Opening' and len(runtime.history()['items']) == count
    assert global_session.outbox.path.read_bytes() == global_bytes
    assert json.loads(path.read_bytes())['pending'] == []


def test_http_ambiguous_owner_and_mixed_edits_keep_original_draft(
    tmp_path, film, real_runtime,
):
    fixture, parent, _ = film
    daemon = real_runtime(fixture.duplicate_root, support_root=tmp_path / 'support', authoring_profile='astrid')
    client = m1.open_client(daemon)
    session = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                  client=client, outbox_path=tmp_path / 'owned.json')
    original = session._bundle(json.loads(session.outbox.path.read_bytes()))
    owner = 'occurrence:' + parent['occurrences'][0]['occurrence_id']
    identity = State(original).collection(owner, 'clip')[0]['id']
    # The same display ID belongs to two different owners in a real closure.
    session.commit_many([
        ingress.command('track.create', 'parent', {'row': {'id': 'titles', 'kind': 'visual'}}),
        ingress.command('clip.add', 'parent', {'row': {'id': identity, 'clipType': 'am-type',
            'track': 'titles', 'at': 0, 'hold': 1, 'params': {'text': 'Parent'}}}),
    ])
    tl = Checkout.attach(session)
    durable, draft = session.outbox.path.read_bytes(), copy.deepcopy(tl.bundle)
    with pytest.raises(TimelineEditError, match='one exact clip'):
        tl.clip(identity).on(2)
    assert session.outbox.path.read_bytes() == durable and tl.bundle == draft
    ref = 'parent/clip:' + identity
    tl.clip(ref).on(2)
    tl.clip(ref).set(text='Local mixed edit')
    durable, draft = tl.session.outbox.path.read_bytes(), copy.deepcopy(tl.bundle)
    head = copy.deepcopy(m1.history(client, fixture)['head'])
    with pytest.raises(TimelineEditError, match='held'):
        tl.publish('Mixed')
    assert tl.session.outbox.path.read_bytes() == durable and tl.bundle == draft
    assert m1.history(client, fixture)['head'] == head
