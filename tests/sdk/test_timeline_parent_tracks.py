"""Canonical parent track layout; frozen refusal inputs, no Runtime writes."""

import copy
import json
from pathlib import Path

import pytest
from test_timeline_commit import call, core, request
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import open_authoring_bundle, compile_authoring_candidate
from astrid.sdk.timeline import commands, store
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def frozen():
    return json.loads((Path(__file__).parents[1] / "fixtures/timeline_editing/parent_r1_tracks.json").read_text())


def opened(frozen):
    return Checkout(open_authoring_bundle(frozen["parent_revision"], shot_revisions=[],
                                         internal_timeline_revisions=[])).document()


def test_frozen_parent_r1_exact_command_compiles_and_reopens(frozen):
    before = opened(frozen)
    pins = copy.deepcopy({k: before[k] for k in ("base_parent", "base_parent_payload", "source_mapping")})
    after, plan, _ = RuntimeCommitService._apply(before, [frozen["command"]])
    expected = copy.deepcopy(before["parent"])
    expected["config"]["tracks"][1]["muted"] = True
    assert after["parent"] == expected
    assert "tracks" not in after["parent"]
    assert {k: after[k] for k in pins} == pins
    record = plan.calls[0].to_json()
    direct = {commands.write_target(key, record["resolved"]) for key, kind in record["authorship"].items() if kind == "direct"}
    assert direct == {("parent/track:A1", "muted")}
    assert all(kind == "consequence" for key, kind in record["authorship"].items()
               if commands.write_target(key, record["resolved"]) != ("parent/track:A1", "muted"))
    assert store.checkout_change_units(Checkout(after)) == (True, [["parent-config", "tracks"]])
    publication = compile_authoring_candidate(after).publication
    assert publication["shot_revisions"] == publication["internal_timeline_revisions"] == []
    reopened = open_authoring_bundle({
        "project_id": publication["project_id"], "timeline_id": publication["timeline_id"],
        "revision_id": publication["parent_revision_id"], "content_digest": publication["content_digest"],
        "payload": publication["parent_composition"],
    }, shot_revisions=[], internal_timeline_revisions=[])
    assert reopened["parent"] == expected
    inverse = inverse_command(plan.calls, before, after, "offline-parent-track-proof")
    restored, _, _ = RuntimeCommitService._apply(after, [inverse])
    assert restored["parent"] == before["parent"]


@pytest.mark.parametrize("layout", ["missing-config", "missing-tracks", "empty-canonical", "flat-only"])
def test_track_accessor_reads_are_pure_and_writes_use_backing_collection(frozen, layout):
    tl = Checkout(opened(frozen))
    parent = tl.bundle["parent"]
    row = parent["config"].pop("tracks")[1]
    if layout == "missing-config":
        parent.pop("config")
    elif layout == "empty-canonical":
        parent["config"]["tracks"] = []
    elif layout == "flat-only":
        parent["tracks"] = [row]
    before = copy.deepcopy(parent)
    rows = tl._tracks(None)
    assert parent == before and tl._internal(None) is parent
    target = tl._tracks(None, create=True)
    if layout == "flat-only":
        assert target is parent["tracks"] and rows == [row]
        assert "tracks" not in parent["config"]
    else:
        assert rows == [] and target is parent["config"]["tracks"]
        assert "tracks" not in parent


@pytest.mark.parametrize("bad", ["dual", "empty-dual", "equal-dual", "null-config", "null-tracks", "object-tracks", "bad-row", "missing-id", "duplicate"])
def test_parent_track_layout_refuses_before_mutation(frozen, bad):
    data = opened(frozen)
    parent = data["parent"]
    if bad in {"dual", "empty-dual", "equal-dual"}:
        parent["tracks"] = copy.deepcopy(parent["config"]["tracks"])
        if bad == "empty-dual":
            parent["config"]["tracks"] = []
        elif bad == "dual":
            parent["tracks"][1]["muted"] = True
    elif bad == "null-config":
        parent["config"] = None
    elif bad in {"null-tracks", "object-tracks", "bad-row", "missing-id"}:
        parent["config"]["tracks"] = {"null-tracks": None, "object-tracks": {}, "bad-row": [None], "missing-id": [{}]}[bad]
    else:
        parent["config"]["tracks"].append(copy.deepcopy(parent["config"]["tracks"][1]))
    before = copy.deepcopy(data)
    body = request(frozen["command"])
    service, port = core(body, data)
    result = service.commit(body, port)
    if bad == "null-config":
        # Track access rejects the malformed container as an ordinary edit
        # refusal; it must still fail before any durable acceptance.
        assert result["status"] == "refused" and result["error"]["code"] == "bad_request"
        assert result["error"]["message"] == "Parent track config must be an object"
    else:
        assert result["status"] == "refused"
    assert not port.accepts and port.saved is None
    assert data == before


@pytest.mark.parametrize("internal", [None, {}])
def test_child_track_accessor_reads_create_no_containers(frozen, internal):
    tl = Checkout(opened(frozen))
    shot = {} if internal is None else {"internal_timeline": internal}
    tl.bundle["shots"]["child"] = shot
    before = copy.deepcopy(shot)
    assert tl._tracks("child") == []
    assert shot == before
    assert tl._tracks("child", create=True) is shot["internal_timeline"]["tracks"]
    assert "clips" not in shot["internal_timeline"]


def test_parent_track_rebase_preserves_property_guards(frozen):
    data = opened(frozen)
    after, plan, _ = RuntimeCommitService._apply(data, [frozen["command"]])
    head = copy.deepcopy(data)
    head["parent"]["config"]["tracks"][1]["label"] = "Concurrent label"
    replay = rebase(plan.calls, head)
    assert not replay.conflicts
    assert replay.document["parent"]["config"]["tracks"][1]["label"] == "Concurrent label"
    assert rebase(plan.calls, after).conflicts
    head["parent"]["config"]["tracks"].pop()
    assert rebase(plan.calls, head).conflicts


def test_parent_track_add_inverse_restores_collection_absence(frozen):
    data = opened(frozen)
    del data["parent"]["config"]["tracks"]
    sid = "parent/track:new"
    add = {**call("timeline.add", sid, track={"id": "new", "kind": "audio", "label": "New"}),
           "expect": {sid + "::": {"state": "absent"}}}
    after, plan, _ = RuntimeCommitService._apply(data, [add])
    assert "tracks" not in after["parent"]
    inverse = inverse_command(plan.calls, data, after, "offline-new-track-collection")
    restored, _, _ = RuntimeCommitService._apply(after, [inverse])
    assert restored["parent"] == data["parent"]


def test_parent_track_failed_second_command_rolls_back_without_acceptance(frozen):
    data = opened(frozen)
    bad = {**call("timeline.set", "parent/track:A1", values={"volume": None}),
           "expect": {"volume": {"state": "present", "value": 1}}}
    before = copy.deepcopy(data)
    body = request(frozen["command"], bad)
    service, port = core(body, data)
    result = service.commit(body, port)
    assert result["status"] == "refused" and not port.accepts and port.saved is None
    assert data == before


@pytest.mark.parametrize("scope", ["parent", "occurrence:occ-A"])
def test_same_local_track_id_conflict_after_authoring_change_refuses_atomically(frozen, scope):
    data = Checkout(json.loads((Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json").read_text())).document()
    data["parent"]["config"]["tracks"] = copy.deepcopy(frozen["parent_revision"]["payload"]["config"]["tracks"])
    child_track = copy.deepcopy(data["parent"]["config"]["tracks"][1])
    child_track.setdefault("app", {})["child"] = None
    data["shots"]["A"]["internal_timeline"]["tracks"].append(child_track)
    before = copy.deepcopy(data)
    cmd = copy.deepcopy(frozen["command"])
    cmd["select"] = scope + "/track:A1"
    cmd["expect"] = {scope + "/track:A1::muted": {"state": "present", "value": False}}
    with pytest.raises(commands.TimelineEditError, match="conflicts"):
        RuntimeCommitService._apply(data, [cmd])
    assert data == before


def test_parent_clip_track_kind_move_duplicate_and_detach_use_config(frozen):
    data = Checkout(json.loads((Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json").read_text())).document()
    parent = data["parent"]
    parent["config"]["tracks"] = copy.deepcopy(frozen["parent_revision"]["payload"]["config"]["tracks"])
    parent["registry"] = {"assets": {}}
    parent["registry"]["assets"]["movie"] = {"media_id": "sha256:" + "a" * 64, "type": "video/mp4"}
    parent["clips"] = [{"id": "movie", "clipType": "media", "asset": "movie", "track": "V1",
                        "at": 0, "from": 0, "to": 1}]
    tl = Checkout(data)
    assert tl._track_kind(None, "A1") == "audio"
    original = copy.deepcopy(parent["config"]["tracks"])
    after, _, _ = RuntimeCommitService._apply(data, [
        call("clip.set-track", "parent/clip:movie", track="A1"),
        call("timeline.add", None, **{"from": "parent/clip:movie", "at": 2, "track": "V1", "clip_id": "copy"}),
        call("clip.detach-audio", "parent/clip:copy", track="A1"),
    ])
    clips = {row["id"]: row for row in after["parent"]["clips"]}
    assert clips["movie"]["track"] == "A1"
    assert clips["copy"]["track"] == "V1" and clips["copy"]["volume"] == 0
    assert any(row["track"] == "A1" and row["id"] != "movie" for row in clips.values())
    assert after["parent"]["config"]["tracks"] == original
    assert "tracks" not in after["parent"]
    with pytest.raises(commands.TimelineEditError, match="existing track"):
        RuntimeCommitService._apply(data, [call("timeline.add", None, **{
            "from": "parent/clip:movie", "at": 2, "track": "missing", "clip_id": "bad"})])


def test_child_track_kind_resolves_parent_tracks_and_maps_definition_conflicts(frozen):
    data = Checkout(json.loads((Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json").read_text())).document()
    data["parent"]["config"]["tracks"] = copy.deepcopy(frozen["parent_revision"]["payload"]["config"]["tracks"])
    tl = Checkout(data)
    child = tl.bundle["shots"]["A"]["internal_timeline"]
    before = copy.deepcopy(tl.bundle)

    assert tl._track_kind("A", "A1") == "audio"
    assert tl._is_audio("A", {"track": "A1"})
    assert tl.bundle == before

    child["tracks"].append({"id": "A1", "kind": "visual", "label": "Conflicting child"})
    conflict_before = copy.deepcopy(tl.bundle)
    with pytest.raises(commands.TimelineEditError, match="conflicts"):
        tl._track_kind("A", "A1")
    # The film lookup reconciles every child as well: a true initial conflict
    # cannot silently fall back to the parent definition.
    with pytest.raises(commands.TimelineEditError, match="conflicts"):
        tl._track_kind(None, "A1")
    assert tl.bundle == conflict_before

    child["tracks"].pop()
    child["clips"].append({"id": "broken", "track": "missing"})
    lookup_before = copy.deepcopy(tl.bundle)
    assert tl._track_kind("A", "A1") == "audio"
    assert tl.bundle == lookup_before

    child["tracks"].append({"id": "bad", "kind": "audio", "app": None})
    invalid_before = copy.deepcopy(tl.bundle)
    with pytest.raises(commands.TimelineEditError, match="app must be an object"):
        tl._track_kind("A", "A1")
    assert tl.bundle == invalid_before
