"""Integrated D gesture writes use the existing publication inverse producer."""

import copy

import pytest
import test_timeline_gesture_producers as gesture_fixtures
from test_timeline_gesture_producers import gesture
from test_timeline_track_gestures import track_fixture

from astrid.sdk.timeline import commands, inverse
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.identity import retain_cut_reservations
from astrid.sdk.timeline.rebase import rebase

source = gesture_fixtures.source


@pytest.mark.parametrize("op", ["timeline.add", "timeline.split", "timeline.remove"])
def test_gesture_inverse_redo_and_stale_guard_preserve_exact_owners(source, op):
    before, sid = source
    if op == "timeline.remove":
        before, sid = track_fixture(source)
        call = dict(op=op, select=sid, args={})
    else:
        call = gesture(op, sid, at=1.5)
    before = copy.deepcopy(before)
    retain_cut_reservations(before)  # identity reservations survive undo by design
    original = commands.entity_states(Checkout(copy.deepcopy(before)))
    after, forward, _ = RuntimeCommitService._apply(before, [call])
    undo = inverse.inverse_command(
        forward.calls, before, after, "gesture-publication", consequences=forward.consequences
    )
    restored, backward, _ = RuntimeCommitService._apply(after, [undo])
    assert commands.entity_states(Checkout(restored)) == original
    redo = inverse.inverse_command(
        backward.calls, after, restored, "undo-publication", consequences=backward.consequences
    )
    redone, _, _ = RuntimeCommitService._apply(restored, [redo])
    assert commands.entity_states(Checkout(redone)) == commands.entity_states(Checkout(after))

    # A later disjoint edit survives semantic rebase of the recorded inverse.
    later = copy.deepcopy(after)
    later["parent"]["config"]["opaque-later"] = None
    replay = rebase(backward.calls, later)
    assert not replay.conflicts, replay.conflicts
    assert replay.document["parent"]["config"]["opaque-later"] is None

    # A later change to a member being removed/restored refuses atomically.
    stale = copy.deepcopy(after if op != "timeline.remove" else restored)
    target = forward.calls[0].created[0] if op != "timeline.remove" else sid
    scope, local = target.rsplit("/", 1)
    kind, identity = local.split(":", 1)
    internal = stale["parent"] if scope == "parent" else stale["shots"]["A"]["internal_timeline"]
    next(row for row in internal[kind + "s"] if row["id"] == identity)["opaque-later"] = None
    unchanged = copy.deepcopy(stale)
    result = rebase(backward.calls if op != "timeline.remove" else [redo], stale)
    assert result.conflicts and result.document is None
    assert stale == unchanged
