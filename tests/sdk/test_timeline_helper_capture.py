"""Detached helper capture survives restart and is checked by the real provider."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline import journal
from astrid.sdk.timeline import open as open_timeline
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk import test_timeline_restructure

restructure_runtime = test_timeline_restructure.restructure_runtime


def draft(env, tmp_path, monkeypatch):
    monkeypatch.setattr('astrid.sdk.timeline_checkout.drafts_root', lambda: tmp_path)
    tl = Checkout.open(env.project, 't', client=env.client)
    tl.save(tmp_path / 'helper.json', quiet=True)
    return tl


def peer_edit(env, clip='p2'):
    peer = open_timeline(env.project, 't', client=env.client)
    peer.clip(clip).data['opaque'] = {'peer': True}
    peer.commit('Peer', idempotency_key='peer')


def test_nudge_restart_merges_peer_other_clip(restructure_runtime, tmp_path, monkeypatch):
    env = restructure_runtime
    original_open = env.client.timelines.open_bundle
    opens = []

    def open_bundle(*args, **kwargs):
        result = original_open(*args, **kwargs)
        opens.append(copy.deepcopy(kwargs))
        if 'publication_id' not in kwargs:
            result.data['bundle']['source_mapping'].pop('_runtime_document')
        return result

    env.client.timelines.open_bundle = open_bundle
    tl = draft(env, tmp_path, monkeypatch)
    base = copy.deepcopy(tl.bundle['base_parent'])
    start = tl.clip('cross').start
    tl.clip('cross').nudge(0.5)
    tl.save(quiet=True)
    tl = Checkout.load(tl.path)
    assert tl.bundle['base_parent'] == base
    peer_edit(env)
    result = tl.publish('Nudge', client=env.client, idempotency_key='nudge')
    assert result['receipt']['result']['status'] == 'merged'
    body = env.calls[-2][0]
    assert body['merge'] == 'fields' and body['steps'][0]['reads']
    assert body['base_publication_id'] == base['publication_id']
    loaded = Checkout.open(env.project, 't', client=env.client)
    assert loaded.clip('cross').start == pytest.approx(start + 0.5)
    assert loaded.clip('p2').data['opaque'] == {'peer': True}
    assert any(row.get('publication_id') == base['publication_id']
               and row.get('revision_id') == base['revision_id'] for row in opens)


@pytest.mark.parametrize('mode', ['same', 'unknown', 'mixed', 'gap', 'old'])
def test_conflicts_and_uncaptured_edits_never_write(restructure_runtime, tmp_path, monkeypatch, mode):
    env = restructure_runtime
    tl = draft(env, tmp_path, monkeypatch)
    if mode not in {'unknown', 'old'}:
        tl.clip('cross').nudge(0.5)
    if mode in {'unknown', 'mixed', 'gap', 'old'}:
        tl.clip('cross').data['opaque'] = {'local': True}
    if mode == 'gap':
        tl.clip('cross').nudge(0.5)
    tl.save(quiet=True)
    tl = Checkout.load(tl.path)
    peer_edit(env, 'cross' if mode == 'same' else 'p2')
    before = tuple(env.service.store.conn.iterdump())
    with pytest.raises((TimelineEditError, WorkspaceClientError)):
        tl.publish('Refused', client=env.client, idempotency_key='refused')
    assert tuple(env.service.store.conn.iterdump()) == before
    assert env.calls[-1][0]['merge'] == ('fields' if mode == 'same' else 'atomic')


@pytest.mark.parametrize('damage', ['hash', 'commands', 'reads', 'after'])
def test_journal_tamper_and_forged_capture_refuse(restructure_runtime, tmp_path, monkeypatch, damage):
    env = restructure_runtime
    tl = draft(env, tmp_path, monkeypatch)
    tl.clip('cross').nudge(0.5)
    tl.save(quiet=True)
    path = journal.journal_path(env.project, 't')
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    row = rows[-1]
    if damage == 'hash':
        row['label'] = 'tampered'
    else:
        call = row['calls'][0]
        if damage == 'commands':
            call['commands'][0]['args']['changes'][0]['value'] = 9
        elif damage == 'reads':
            call['reads'] = []
        else:
            call['after'] = 'sha256:' + '0' * 64
        row['hash'] = journal._hash(row['prev'], {k: v for k, v in row.items() if k != 'hash'})
    path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
    before = tuple(env.service.store.conn.iterdump())
    with pytest.raises(TimelineEditError, match='helper'):
        Checkout.load(tl.path).publish('Tamper', client=env.client)
    assert tuple(env.service.store.conn.iterdump()) == before


def test_helper_lost_ack_retries_exact_request(restructure_runtime, tmp_path, monkeypatch):
    env = restructure_runtime
    tl = draft(env, tmp_path, monkeypatch)
    tl.clip('cross').nudge(0.5)
    tl.save(quiet=True)
    lost = False

    def send(*args, **kwargs):
        nonlocal lost
        result = env.send(*args, **kwargs)
        if not lost:
            lost = True
            raise WorkspaceClientError(0, 'unavailable', 'lost ACK')
        return result

    env.generated.commit_timeline = send
    with pytest.raises(WorkspaceClientError):
        tl.publish('Retry helper', client=env.client, idempotency_key='helper-retry')
    Checkout.load(tl.path).publish('Retry helper', client=env.client, idempotency_key='helper-retry')
    assert env.calls[0] == env.calls[1]
    assert env.replies[0] == env.replies[1]


def test_contiguous_helpers_keep_sequential_steps(restructure_runtime, tmp_path, monkeypatch):
    env = restructure_runtime
    tl = draft(env, tmp_path, monkeypatch)
    start = tl.clip('cross').start
    tl.clip('cross').nudge(0.5)
    tl.clip('cross').nudge(frames=3)
    tl.save(quiet=True)
    peer_edit(env)
    result = Checkout.load(tl.path).publish('Two nudges', client=env.client)
    assert result['receipt']['result']['status'] == 'merged'
    body = env.calls[-2][0]
    assert [step['command_ordinals'] for step in body['steps']] == [[0], [1]]
    assert Checkout.open(env.project, 't', client=env.client).clip('cross').start == pytest.approx(start + 0.6)


@pytest.mark.parametrize('damage', ['wrong-pair', 'ambiguous'])
def test_original_publication_pair_is_required(restructure_runtime, tmp_path, monkeypatch, damage):
    from astrid.sdk.contracts import DomainResult

    env = restructure_runtime
    tl = draft(env, tmp_path, monkeypatch)
    tl.clip('cross').nudge(0.5)
    if damage == 'wrong-pair':
        tl.bundle['base_parent']['publication_id'] = 'wrong'
    else:
        tl.bundle['base_parent'].pop('publication_id')
        original = env.client.timelines.history

        def history(*args, **kwargs):
            result = copy.deepcopy(original(*args, **kwargs).data)
            matches = [row for row in result['items'] if row['revision_id'] == tl.base_revision]
            if matches:
                row = copy.deepcopy(matches[0])
                row['publication_id'] = 'another-publication'
                result['items'].append(row)
            return DomainResult.success(result)

        env.client.timelines.history = history
    before = tuple(env.service.store.conn.iterdump())
    with pytest.raises(TimelineEditError, match='unique publication base'):
        tl.publish('Bad base', client=env.client)
    assert tuple(env.service.store.conn.iterdump()) == before
