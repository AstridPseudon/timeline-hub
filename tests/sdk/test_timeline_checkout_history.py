"""Draft snapshots cannot rewind accepted history; public inverses use the outbox."""
from __future__ import annotations

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.sdk import storage_root
from astrid.sdk.timeline import store
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.outbox import request_bytes
from astrid.sdk.timeline.revisions import Revision, RuntimeRevisions
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_sheet import find_version, sheet_version
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk.test_timeline_sync import connected  # noqa: F401
from tests.sdk.test_timeline_transaction import draft  # noqa: F401


@pytest.fixture
def native(connected, monkeypatch):
    client, generated, path = connected
    monkeypatch.setattr(storage_root, 'resolve_runtime_data_root', lambda: path.parent)
    scope = {'realm_id': 'realm', 'actor_id': 'actor', 'project_id': 'p', 'timeline_id': 't'}
    generated.path = path.parent / 'timeline-outbox' / (hashlib.sha256(request_bytes(scope)).hexdigest() + '.json')
    return client, generated


@pytest.mark.parametrize('redo', [False, True])
def test_local_restore_stops_at_accepted_base_and_keeps_new_unsent_edits(draft, redo):
    old = draft.path.read_text()
    # Simulate a successful publish/reset. Old step files may survive upgrades
    # and crashes; they must not be treated as unsent edits on the new base.
    draft.bundle['base_parent']['revision_id'] = 'accepted-new-base'
    draft.save(quiet=True)
    folder = store._redo_dir if redo else store._history_dir
    store._write_step(folder(draft.path), 'before publication', old)
    published = draft.document()
    text = draft.path.read_bytes()
    with pytest.raises(TimelineEditError, match='no unsent draft edit'):
        (draft.redo if redo else draft.undo)()
    assert draft.path.read_bytes() == text
    assert draft.document() == published
    draft.clip('c1.rocket').set(x=99)
    draft.save(quiet=True)
    edited = draft.document()
    assert draft.undo()  # the new unsent edit is still useful and undoable
    assert draft.document() == published
    assert draft.redo()
    assert draft.document() == edited


def test_checkout_accepted_inverse_reload_retry_and_redo_leave_draft_untouched(native, tmp_path):
    client, generated = native
    original = copy.deepcopy(generated.bundles['r0'])
    accepted = TimelineSession.open('p', 't', client=client).move('parent/clip:a', 5)
    checkout = Checkout.open('p', 't', revision_id=generated.head['revision_id'], client=client)
    checkout.save(tmp_path / 'detached.json', quiet=True)
    draft_text = checkout.path.read_bytes()
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        checkout.undo(publications=[accepted['receipt']['receipt_id']], client=client,
                      idempotency_key='undo-accepted')
    undone = Checkout.load(checkout.path).undo(publications=['pub1'], client=client)
    assert generated.calls[-1] == generated.calls[-2]
    assert generated.bundles['r2'] == original
    assert checkout.path.read_bytes() == draft_text
    redone = Checkout.open('p', 't', revision_id=generated.head['revision_id'], client=client).redo(
        publications=[undone['receipt']['receipt_id']], client=client)
    assert generated.bundles[redone['data']['accepted_revision_id']] == generated.bundles['r1']
    state = json.loads(generated.path.read_bytes())
    assert state['pending'] == [] and state['flight'] is None
    assert set(state) == {'scope', 'base', 'pending', 'flight'}


def test_sheet_local_basis_does_not_cross_accepted_base(draft):
    old = draft.path.read_text()
    version = sheet_version(draft)
    draft._exported = {version: copy.deepcopy(draft.bundle)}
    draft.bundle['base_parent']['revision_id'] = 'accepted-new-base'
    draft.save(quiet=True)
    store._write_step(store._history_dir(draft.path), 'old accepted basis', old)
    assert find_version(draft, version) is None


def test_sheet_basis_with_client_uses_runtime_history_before_local_snapshots(draft, monkeypatch):
    draft.clip('c1.rocket').set(x=40)
    draft.save(quiet=True)
    historical = copy.deepcopy(draft.bundle)
    version = sheet_version(draft)
    draft.clip('c1.rocket').set(x=99)
    draft.save(quiet=True)
    draft._exported = {version: historical}
    retained = Checkout(copy.deepcopy(historical))
    opened = []

    monkeypatch.setattr(RuntimeRevisions, 'list', lambda self, project, timeline, limit: [
        Revision('retained-revision', 'astrid', None, None, None, 'retained-publication', None),
    ])

    def open_retained(cls, project, timeline, *, revision_id=None, client=None):
        opened.append((project, timeline, revision_id, client))
        return retained

    monkeypatch.setattr(Checkout, 'open', classmethod(open_retained))
    client = SimpleNamespace(timelines=object())
    assert find_version(draft, version, client=client) is retained
    assert opened == [('p', 't', 'retained-revision', client)]


def test_sheet_basis_follows_runtime_history_cursor_to_page_two(draft, monkeypatch):
    draft.clip('c1.rocket').set(x=40)
    draft.save(quiet=True)
    historical = copy.deepcopy(draft.bundle)
    version = sheet_version(draft)
    draft.clip('c1.rocket').set(x=99)
    draft.save(quiet=True)
    retained = Checkout(copy.deepcopy(historical))

    def history_item(publication_id, revision_id, previous=None):
        return {
            'publication_id': publication_id,
            'revision_id': revision_id,
            'previous': previous,
            'receipt': {'created_at': f'{publication_id}-time'},
            'intent': 'recorded',
            'records': {},
            'provider_version': 'astrid-v1',
            'compiler_version': 'compiler-v1',
            'publisher': 'actor-1',
        }

    pages = {
        None: {
            'items': [history_item('pub-1', 'old-revision')],
            'next_cursor': 'page-2',
            'head': {'revision_id': 'retained-revision', 'publication_id': 'pub-2'},
        },
        'page-2': {
            'items': [history_item(
                'pub-2', 'retained-revision',
                {'publication_id': 'pub-1', 'revision_id': 'old-revision'},
            )],
            'next_cursor': None,
            'head': {'revision_id': 'retained-revision', 'publication_id': 'pub-2'},
        },
    }
    calls = []

    class Timelines:
        def list_timeline_commits(self, project, timeline, *, cursor=None, limit=50):
            calls.append((project, timeline, cursor, limit))
            return pages[cursor]

    opened = []

    def open_retained(cls, project, timeline, *, revision_id=None, client=None):
        opened.append((project, timeline, revision_id, client))
        return retained

    monkeypatch.setattr(Checkout, 'open', classmethod(open_retained))
    client = SimpleNamespace(timelines=Timelines())
    assert find_version(draft, version, client=client) is retained
    assert calls == [('p', 't', None, 50), ('p', 't', 'page-2', 50)]
    assert opened == [('p', 't', 'retained-revision', client)]
