"""Verify a duplicate against its authenticated source, without compiling it.

The ordinary compiler remains the producer. This reader compares complete
payloads and ordered pins at the saved receipt boundary, independently of its
parent projections. Local draft or journal snapshots are never source authority.
"""

from __future__ import annotations

import copy

from astrid.core.timeline.authoring_bundle import (
    _copy_shot_for_placement,
    _remap_known_item_references,
)
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest


def _leaves(calls):
    for call in calls:
        if call["op"] == "timeline.batch":
            yield from _leaves(call["args"]["commands"])
        else:
            yield call


def verify_duplicate(workspace, body, canonical, persisted):
    """Bind a lone duplicate initializer to exact persisted source/output bytes."""
    from astrid.sdk.timeline.checkout import Checkout
    from astrid.sdk.timeline.saved_publish import _ClosurePort

    calls = list(_leaves(body["change"]["commands"]))
    copies = [call for call in calls if call["op"] == "timeline.duplicate"]
    if not copies:
        return
    if len(calls) != 1:
        raise TimelineEditError("duplicate fidelity requires its isolated initialization command")
    args = copies[0]["args"]
    source = Checkout(
        RuntimeCommitService._load_duplicate_source(
            _ClosurePort(workspace, body["project_id"], body["timeline_id"]), body, args["source"]
        )
    ).document()
    ids = args["identities"]
    rows = source["placements"]
    if len(ids) != len(rows):
        raise TimelineEditError(
            "duplicate source occurrence count differs from reserved identities"
        )
    parent = copy.deepcopy(source["parent"])
    mapping = {row["occurrence_id"]: out["occurrence_id"] for row, out in zip(rows, ids)}
    mapping.update({row["shot_id"]: out["shot_id"] for row, out in zip(rows, ids)})
    parent["clips"] = _remap_known_item_references(parent.get("clips", []), mapping)
    placements, shots, internals = [], {}, {}
    for row, out in zip(rows, ids):
        original = source["shots"][row["shot_id"]]
        pin = source["source_mapping"]["shots"][row["shot_id"]]
        payload, items = _copy_shot_for_placement(
            original["base_payload"],
            project_id=body["project_id"],
            timeline_id=body["timeline_id"],
            occurrence_id=out["occurrence_id"],
            authoring_shot_id=out["shot_id"],
            source_shot_id=pin["shot_id"],
        )
        payload.pop("internal_timeline_revision_id", None)
        payload["text_bindings"] = []  # explicit duplicate policy; never reuse source bindings
        internal = _remap_known_item_references(original["base_internal_timeline"], items)
        placement = dict(
            copy.deepcopy(row), occurrence_id=out["occurrence_id"], shot_id=out["shot_id"]
        )
        placements.append(placement)
        shots[out["shot_id"]] = payload
        internals[out["shot_id"]] = internal

    def same(actual, expected, label):
        if _digest(actual) != _digest(expected):
            raise TimelineEditError(
                f"duplicate fidelity mismatch: {label}; saved publish remains pending"
            )

    same(canonical["parent"], parent, "canonical parent")
    same(canonical["placements"], placements, "canonical ordered placements")
    same(sorted(canonical["shots"]), sorted(shots), "canonical shot identities")
    for sid in shots:
        same(canonical["shots"][sid]["payload"], shots[sid], "canonical shot payload")
        same(
            canonical["shots"][sid]["internal_timeline"],
            internals[sid],
            "canonical internal payload",
        )
    closure = persisted["immutable_closure"]
    expected = dict(
        copy.deepcopy(parent),
        occurrences=[
            dict(row, shot_revision_id=out["shot_revision_id"]) for row, out in zip(placements, ids)
        ],
    )
    same(closure["parent"]["payload"], expected, "persisted parent and ordered pins")
    same(
        sorted(closure["shots"]),
        sorted(out["shot_revision_id"] for out in ids),
        "persisted shot revision identities",
    )
    same(
        sorted(closure["internal_timelines"]),
        sorted(out["internal_revision_id"] for out in ids),
        "persisted internal revision identities",
    )
    for out in ids:
        sid, srid, irid = out["shot_id"], out["shot_revision_id"], out["internal_revision_id"]
        shot, internal = closure["shots"][srid], closure["internal_timelines"][irid]
        same(
            [shot["shot_id"], shot["revision_id"], shot["internal_timeline_revision_id"]],
            [sid, srid, irid],
            "persisted shot pins",
        )
        same(
            [internal["timeline_id"], internal["revision_id"]],
            [body["timeline_id"], irid],
            "persisted internal pins",
        )
        same(
            shot["payload"],
            dict(shots[sid], internal_timeline_revision_id=irid),
            "persisted shot payload",
        )
        same(internal["payload"], internals[sid], "persisted internal payload")
