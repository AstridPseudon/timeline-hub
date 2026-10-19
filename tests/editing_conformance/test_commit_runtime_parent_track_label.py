"""Real Runtime door coverage for the parent-track label handoff.

Run centrally with ``commit-integration --files
tests/editing_conformance/test_commit_runtime_parent_track_label.py``.
"""
from __future__ import annotations

import json

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._track_commands import capture_track_set
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance import test_commit_runtime_m1 as m1

pytestmark = pytest.mark.integration


@pytest.mark.xfail(
    strict=True,
    reason='Runtime official command-artifact refresh is required before M2 integration qualification',
)
def test_move_then_parent_label_reload_inverse_preserves_newer_disjoint_move(
    tmp_path, monkeypatch, film, real_runtime,
):
    from astrid.sdk.timeline.sync import TimelineSession

    fixture, _, _ = film
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(tmp_path / 'client-data'))
    support = tmp_path / 'support'
    daemon = real_runtime(fixture.duplicate_root, support_root=support, authoring_profile='astrid')
    client = m1.open_client(daemon)
    outbox = tmp_path / 'parent-label-outbox.json'
    session = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                   client=client, outbox_path=outbox)

    moved = session.move('parent/clip:music-bed', 1)
    moved_bundle = bundle_from_document(moved['data']['canonical_document'])
    assert State(moved_bundle).entity('parent/clip:music-bed')['at'] == 1
    label = session._queue(lambda state: capture_track_set(
        session._bundle(state), 'parent/track:music', values={'label': 'Music'}))
    accepted = session.flush()
    assert json.loads(outbox.read_bytes())['pending'] == []
    assert accepted['data']['commands'] == [label]
    m1.assert_readback(client, fixture, accepted)
    accepted_bundle = bundle_from_document(accepted['data']['canonical_document'])
    assert State(accepted_bundle).entity('parent/track:music')['label'] == 'Music'
    assert State(accepted_bundle).entity('parent/clip:music-bed')['at'] == 1

    reloaded = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                    client=client, outbox_path=tmp_path / 'reload-outbox.json')
    other = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                 client=client, outbox_path=tmp_path / 'other-outbox.json')
    disjoint = other.move('parent/clip:music-other', 2)
    undone = reloaded.undo([accepted['receipt']['receipt_id']])
    m1.assert_readback(client, fixture, undone)
    document = undone['data']['canonical_document']
    restored = bundle_from_document(document)
    assert State(restored).entity('parent/clip:music-bed')['at'] == 1
    assert State(restored).entity('parent/clip:music-other')['at'] == 2
    assert 'label' not in State(restored).entity('parent/track:music')
    assert State(bundle_from_document(disjoint['data']['canonical_document'])).entity(
        'parent/clip:music-other')['at'] == 2
