"""Public checkout history against the Runtime paired with the generated client."""
from __future__ import annotations

import copy
import os

import pytest

from tests.editing_conformance.test_commit_runtime_m1 import (
    assert_readback,
    cli,
    film,
    open_client,
    parent_of,
    renderer_off,
)
from tests.helpers.runtime import use_runtime, vendored_runtime_commit

pytestmark = pytest.mark.integration
# Like the client cutover suite, read the existing lock; never change or bypass
# either side of the public handshake to test a different Runtime contract.
os.environ.setdefault('ASTRID_RUNTIME_CHECKOUT', '/home/user/work/runtime')
RUNTIME = use_runtime(vendored_runtime_commit())


def test_checkout_reload_undo_cli_redo_uses_retained_history(
    tmp_path, monkeypatch, capsys, film, renderer_off, real_runtime,
):
    from astrid.sdk.timeline.sync import TimelineSession
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import find_version, sheet_version

    fixture, original_parent, _ = film
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(tmp_path / 'client-data'))
    daemon = real_runtime(fixture.duplicate_root, support_root=tmp_path / 'support', authoring_profile='astrid')
    with open_client(daemon) as client:
        original = Checkout.open(fixture.project_id, fixture.timeline_id, client=client)
        version = sheet_version(original)
        session = TimelineSession.open(fixture.project_id, fixture.timeline_id, client=client)
        accepted = session.move('parent/clip:music-bed', 2)
        disjoint = session.move('parent/clip:music-other', 3)
        reopened = Checkout.open(fixture.project_id, fixture.timeline_id, client=client)
        # No local history exists: an older sheet's exact basis comes from the
        # Runtime's retained revision path, including its original source pins.
        restored_basis = find_version(reopened, version, client=client)
        assert restored_basis is not None
        assert restored_basis.document() == original.document()
        undone = reopened.undo(publications=[accepted['receipt']['receipt_id']], client=client)
        expected = copy.deepcopy(parent_of(disjoint))
        expected['clips'][0] = copy.deepcopy(original_parent['clips'][0])
        expected['config']['clips'] = copy.deepcopy(expected['clips'])
        assert parent_of(undone) == expected
        assert_readback(client, fixture, undone)
        redone = cli(client, fixture, capsys, 'redo', fixture.timeline_id,
                     '--publication', undone['receipt']['receipt_id'])
        assert parent_of(redone) == parent_of(disjoint)
        assert_readback(client, fixture, redone)
        assert Checkout.open(fixture.project_id, fixture.timeline_id, client=client).base_revision == redone['data']['accepted_revision_id']


def test_retained_restore_does_not_reopen_consumed_draft_steps(
    tmp_path, monkeypatch, film, renderer_off, real_runtime,
):
    from astrid.sdk.timeline import store
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.sync import TimelineSession
    from astrid.sdk.timeline_checkout import Checkout

    fixture, _, _ = film
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(tmp_path / 'client-data'))
    daemon = real_runtime(fixture.duplicate_root, support_root=tmp_path / 'support', authoring_profile='astrid')
    with open_client(daemon) as client:
        draft = Checkout.draft(fixture.project_id, fixture.timeline_id, client=client)
        original = copy.deepcopy(draft.bundle)

        def local_move(on):
            with draft.step('move music'):
                draft.bundle['parent']['clips'][0]['at'] = on
                draft.bundle['parent']['config']['clips'] = copy.deepcopy(draft.bundle['parent']['clips'])
            draft.save(quiet=True)

        local_move(1)
        local_move(2)
        assert len(list(store._history_dir(draft.path).glob('*.json'))) == 2
        session = TimelineSession.open(fixture.project_id, fixture.timeline_id, client=client)
        accepted = session.move('parent/clip:music-bed', 2)
        draft._reset_base(client=client)
        assert draft.base_revision == accepted['data']['accepted_revision_id']
        restored = client._remote._transport._generated.restore_project_parent_composition_revision(
            fixture.project_id, fixture.timeline_id, original['base_parent']['revision_id'],
            expected_head=accepted['data']['accepted_revision_id'],
            expected_publication_id=accepted['receipt']['receipt_id'],
            idempotency_key='restore-retained-draft-base',
        )
        assert restored['data']['accepted_revision_id'] == original['base_parent']['revision_id']
        assert restored['receipt']['receipt_id'] != accepted['receipt']['receipt_id']
        draft._reset_base(client=client)
        draft = Checkout.load(draft.path)
        assert draft.document() == Checkout(original).document()
        for operation in (draft.undo, draft.redo):
            with pytest.raises(TimelineEditError, match='no unsent draft edit'):
                operation()
        base = draft.document()
        local_move(3)
        edited = draft.document()
        assert len(draft.undo(100)) == 1
        assert draft.document() == base
        draft.redo()
        assert draft.document() == edited
