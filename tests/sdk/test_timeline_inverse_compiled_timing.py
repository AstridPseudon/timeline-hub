"""W42 accepted Runtime artifacts bind the command/inverse/compiler consumer."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.core.timeline.cuts import clip_duration
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/timeline_editing/w42"
HASHES = {
    "runtime-command-result.json": "ebebe93a0c0fa42d23d4107d10cae5bef360d78464b7bc1c47d8631739090d41",
    "runtime-command-wire.json": "fafbc833dee376107cf7c88e61fbab0fd23c83fc913cd5ae95402c053c334043",
    "runtime-undo-wire.json": "bec9fd727494e2f21545f085fe2f856f488ba0caa961e170b4dc1d1453520a82",
}


def w42():
    artifacts = {}
    for name, digest in HASHES.items():
        raw = (FIXTURE / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
        artifacts[name] = json.loads(raw)
    accepted = artifacts["runtime-command-result.json"]
    assert accepted["status"] == "accepted"
    before = copy.deepcopy(accepted["canonical_document"])
    before["parent"] = copy.deepcopy(before["base_parent_payload"])
    return before, accepted, artifacts["runtime-command-wire.json"], artifacts["runtime-undo-wire.json"]


def compiled_geometry(document):
    parent = compile_authoring_candidate(document).publication["parent_composition"]
    return [(c["id"], c.get("at", 0), clip_duration(c), c.get("at", 0) + clip_duration(c))
            for c in parent["clips"]]


def test_w42_accepted_duration_inverse_restores_compiled_effective_geometry():
    before, accepted, request, undo_request = w42()
    original = copy.deepcopy(before)
    # The complete captured App command is replayed, including relation choice,
    # presence-aware expectations and opaque lookalike payloads.
    after, forward, _ = RuntimeCommitService._apply(before, request["change"]["commands"])
    assert after == accepted["canonical_document"]
    undo = inverse_command(forward.calls, before, after, accepted["accepted_publication_id"],
                           consequences=forward.consequences)
    assert undo == undo_request["change"]["commands"][0]
    restored, backward, _ = RuntimeCommitService._apply(after, [undo])
    assert before == original
    assert compiled_geometry(before) == [("clip-1", 1, 0.2, 1.2), ("clip-2", 1.2, 1.0, 2.2)]
    assert compiled_geometry(after) == [("clip-1", 1, 0.5, 1.5), ("clip-2", 1.2, 1.0, 2.2)]
    assert compiled_geometry(restored) == compiled_geometry(before)
    assert restored["parent"] == before["parent"]
    assert restored["parent"]["clips"][0]["hold"] == 0.2
    # The same existing inverse producer supports redo without a geometry write.
    redo = inverse_command(backward.calls, after, restored, "w42-undo",
                           consequences=backward.consequences)
    redone, _, _ = RuntimeCommitService._apply(restored, [redo])
    assert compiled_geometry(redone) == compiled_geometry(after)


@pytest.mark.parametrize("relation", ["hold", "for", "until", "clear"])
def test_explicit_relations_and_plain_holds_keep_one_resolver(relation):
    before, _, _, _ = w42()
    clip = before["parent"]["clips"][0]
    ns = clip["app"]["astrid"]
    if relation == "for":
        ns.pop("until")
        ns["for"] = 0.2
    elif relation == "hold":
        ns.pop("until")
    if relation in {"for", "until"}:
        clip["hold"] = 0.5  # stale materialized value, never another authority
    call = {"op": "timeline.resolve", "select": None, "args": {}}
    if relation == "clear":
        call = {"op": "clip.clear", "select": "parent/clip:clip-1", "args": {
            "keys": ["until"], "relation_choices": [{
                "target": "parent/clip:clip-1", "edge": "end", "choice": "detach"}]}}
    after, _, _ = RuntimeCommitService._apply(before, [call])
    assert compiled_geometry(after)[0] == ("clip-1", 1, 0.2, 1.2)
    assert after["parent"]["clips"][1] == before["parent"]["clips"][1]
    assert after["parent"]["clips"][0]["params"] == clip["params"]
    if relation == "clear":
        assert "until" not in after["parent"]["clips"][0]["app"]["astrid"]
        after["parent"]["clips"][1]["at"] = 1.4
        resolved, _, _ = RuntimeCommitService._apply(after, [{"op": "timeline.resolve", "select": None, "args": {}}])
        assert compiled_geometry(resolved)[0] == ("clip-1", 1, 0.2, 1.2)


@pytest.mark.parametrize("kind", ["audio", "visual"])
def test_source_window_convention_is_preserved(kind):
    before, _, _, _ = w42()
    before["parent"]["config"]["tracks"][0]["kind"] = kind
    clip = before["parent"]["clips"][0]
    clip.update({"from": 0.1, "to": 0.6, "hold": 0.5})
    tl = Checkout(copy.deepcopy(before))
    tl.resolve()
    assert tl.document()["parent"]["clips"][0] == clip


def test_restored_until_remains_live_when_its_anchor_moves():
    before, accepted, request, _ = w42()
    after, forward, _ = RuntimeCommitService._apply(before, request["change"]["commands"])
    undo = inverse_command(forward.calls, before, after, accepted["accepted_publication_id"],
                           consequences=forward.consequences)
    restored, _, _ = RuntimeCommitService._apply(after, [undo])
    moved, _, _ = RuntimeCommitService._apply(restored, [{
        "op": "clip.on", "select": "parent/clip:clip-2", "args": {"moment": 1.4}}])
    assert compiled_geometry(moved)[0] == ("clip-1", 1, 0.4, 1.4)
    assert moved["parent"]["clips"][0]["app"] == before["parent"]["clips"][0]["app"]


@pytest.mark.parametrize("invalid", ["missing", "ambiguous", "cycle"])
def test_invalid_clip_anchor_refuses_without_mutating_input(invalid):
    before, _, _, _ = w42()
    clips = before["parent"]["clips"]
    if invalid == "missing":
        clips.pop()
    elif invalid == "ambiguous":
        clips.append(copy.deepcopy(clips[1]))
    else:
        clips[1]["app"] = {"astrid": {"on": 'clip-end "parent/clip:clip-1"'}}
    unchanged = copy.deepcopy(before)
    with pytest.raises(TimelineEditError, match={"missing": "(missing|No|no)",
                                                "ambiguous": "Duplicate scoped identity parent/clip:clip-2",
                                                "cycle": "CYCLE"}[invalid]):
        RuntimeCommitService._apply(before, [{"op": "timeline.resolve", "select": None, "args": {}}])
    assert before == unchanged
