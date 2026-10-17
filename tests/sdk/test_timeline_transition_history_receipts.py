"""Retained W29 App requests through SDK; synthetic declaration/acceptance only."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_timeline_commit import CoreService
from test_timeline_fade_history_receipts import accept, literal, port_for, reverse_receipt
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.element import catalog
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers", "declared_transition")
FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/w29_transition_history.json"
SID = "parent/clip:after"


@pytest.fixture
def case():
    return json.loads(FIXTURE.read_text())


@pytest.fixture
def declared_transition(monkeypatch):
    """Explicit SDK declaration seam; no esbuild or installed resource claim."""
    from astrid.packs.rendering.actions.timeline_visualize.motion import element_motion
    from astrid.sdk import invocation

    component = Path(__file__).resolve()
    element = SimpleNamespace(component=component)

    def get(kind, identifier, *, pack_id):
        assert (kind, identifier, pack_id) == ("transitions", "cross-fade", "rendering")
        return element

    ref = json.loads(FIXTURE.read_text())["canonical"]["requests"][0]["change"]["commands"][0]["args"]["elementRef"]
    monkeypatch.setattr(catalog, "_registry", lambda: SimpleNamespace(get=get))
    monkeypatch.setattr(catalog, "_element_descriptor", lambda value: {
        "id": "cross-fade", "kind": "transition", "revision": ref["revision"],
        "defaults": {}, "schema": {"type": "object", "properties": {
            "durationFrames": {"type": "number", "minimum": 0}}, "additionalProperties": False}})

    def admitted(document, *, registry):
        return {row["id"]: {"declaration": {
            "pack_root": str(component.parent),
            "resources": [{"kind": "implementation", "path": component.name}]}}
            for row in document["clips"]}

    monkeypatch.setattr(invocation, "_admitted_timeline_element_resources", admitted)
    # Known renderer admission answer at its existing boundary. Producer timing,
    # track, revision, type and parameter guards above it still execute normally.
    monkeypatch.setattr(element_motion, "admit_transitions", lambda requests: {"ok": True})


def history(before, request, tmp_path, name, undo_request=None):
    forward = accept(before, request)
    undo_body = copy.deepcopy(undo_request or request)
    undo_body.update(request_id="w29-undo-" + name, session_sequence=2,
                     base_revision_id=forward["accepted_revision_id"])
    if undo_request is None:
        undo_body["change"]["commands"] = [reverse_receipt(forward)]
    else:
        # Preserve the retained App-authored Undo request exactly.
        undo_body = copy.deepcopy(undo_request)
        assert undo_body["change"]["commands"] == [reverse_receipt(forward)]
    undone = accept(forward["canonical_document"], undo_body)
    assert literal(undone["canonical_document"]) == literal(before)
    assert undone["change"]["direct_writes"] == reverse_receipt(forward)["args"]["writes"]
    transition_write = next(w for w in undone["change"]["direct_writes"] if w["path"] == "transition")
    assert transition_write["id"] == SID
    redo_body = copy.deepcopy(undo_body)
    redo_body.update(request_id="w29-receipt-only-redo-" + name, session_sequence=3,
                     base_revision_id=undone["accepted_revision_id"])
    redo_body["change"]["commands"] = [reverse_receipt(undone)]
    redone = accept(undone["canonical_document"], redo_body)
    assert literal(redone["canonical_document"]) == literal(forward["canonical_document"])
    result = redone["canonical_document"]["parent"]["clips"][1]
    assert result["transition"] == request["change"]["commands"][0]["args"]["transition"]
    assert result["transition"]["duration"] == 0.731
    assert result["transition"]["params"] is None
    assert result["elementRef"] == request["change"]["commands"][0]["args"]["elementRef"]
    (tmp_path / (name + "-proof.json")).write_text(json.dumps(dict(
        before=before, requests=[request, undo_body, redo_body],
        results=[forward, undone, redone]), indent=2) + "\n")
    return forward, undone, redone


def test_w29_pinned_update_exact_undo_receipt_arms_lossless_redo(case, tmp_path):
    retained = case["pinned"]
    assert retained["retained_result"]["status"] == "accepted"
    assert retained["retained_result"]["change"]["direct_writes"] == []
    forward, undone, _ = history(retained["before"], retained["requests"][0], tmp_path,
                                  "pinned", retained["requests"][1])
    assert literal(forward["canonical_document"]) == literal(retained["retained_results"][0]["canonical_document"])
    assert {(w["id"], w["path"]) for w in undone["change"]["direct_writes"]} == {(SID, "transition")}


def test_w29_canonical_track_assignment_uses_one_unchanged_authority(case, tmp_path):
    retained = case["canonical"]
    assert retained["retained_result"]["error"]["message"] == "transition requires an exact declared visual track"
    before = retained["before"]
    assert "tracks" not in before["parent"]
    tracks = literal(before["parent"]["config"]["tracks"])
    results = history(before, retained["requests"][0], tmp_path, "canonical")
    expected = copy.deepcopy(before)
    args = retained["requests"][0]["change"]["commands"][0]["args"]
    expected["parent"]["clips"][1].update(
        transition=copy.deepcopy(args["transition"]), elementRef=copy.deepcopy(args["elementRef"]))
    assert literal(results[0]["canonical_document"]) == literal(expected)
    for result in results:
        parent = result["canonical_document"]["parent"]
        assert "tracks" not in parent
        assert literal(parent["config"]["tracks"]) == tracks
        assert [r["id"] for r in parent["clips"]] == ["before", "after"]
        assert literal(parent["clips"][0]) == literal(before["parent"]["clips"][0])


def refuse(document, body, *, local=True):
    snapshot = literal(document), literal(body)
    port = port_for(document, body)
    result = CoreService().commit(body, port)
    assert result["status"] in {"refused", "conflict"}, result
    assert not port.accepts and port.saved is None
    assert result["canonical_document"] is None
    assert result["accepted_revision_id"] is None
    assert result["runtime_receipt"] is None
    assert result["change"]["direct_writes"] == []
    assert result["change"]["commands"] == []
    assert (literal(document), literal(body)) == snapshot
    assert literal(port.bundles[body["base_revision_id"]]) == snapshot[0]
    if local:
        tl = Checkout(copy.deepcopy(document))
        with pytest.raises(commands.TimelineEditError):
            commands.run(tl, body["change"]["commands"][0])
        assert literal(tl.document()) == snapshot[0]
    return result


@pytest.mark.parametrize("damage", [
    "absent-tracks", "missing-track", "duplicate-track", "audio-track",
    "dual-identical", "dual-contradictory", "malformed-tracks",
    "missing-predecessor", "wrong-track", "wrong-predecessor", "wrong-scope",
    "implicit-predecessor", "duplicate-predecessor", "gap", "overlap", "fit",
    "stale-transition", "stale-track", "stale-predecessor", "stale-revision",
    "type", "params",
])
def test_w29_assignment_refuses_atomically(case, damage):
    before = case["canonical"]["before"]
    body = case["canonical"]["requests"][0]
    parent = before["parent"]
    tracks = parent["config"]["tracks"]
    previous, destination = parent["clips"]
    call = body["change"]["commands"][0]
    if damage == "absent-tracks":
        del parent["config"]["tracks"]
    elif damage == "missing-track":
        tracks.pop(0)
    elif damage == "duplicate-track":
        tracks.append(copy.deepcopy(tracks[0]))
    elif damage == "audio-track":
        tracks[0]["kind"] = "audio"
    elif damage.startswith("dual-"):
        parent["tracks"] = copy.deepcopy(tracks)
        if damage == "dual-contradictory":
            parent["tracks"][0]["kind"] = "audio"
    elif damage == "malformed-tracks":
        parent["config"]["tracks"] = None
    elif damage == "missing-predecessor":
        parent["clips"].pop(0)
    elif damage == "wrong-track":
        previous["track"] = "V2"
        call["expect"]["parent/clip:before::track"]["value"] = "V2"
    elif damage == "wrong-predecessor":
        call["args"]["from_clip"] = SID
    elif damage == "wrong-scope":
        call["args"]["from_clip"] = "occurrence:occ-A/clip:before"
    elif damage == "implicit-predecessor":
        del call["args"]["from_clip"]
    elif damage == "duplicate-predecessor":
        parent["clips"].append(copy.deepcopy(previous))
    elif damage in {"gap", "overlap"}:
        previous["hold"] = 1.9 if damage == "gap" else 2.1
        call["expect"]["parent/clip:before::hold"]["value"] = previous["hold"]
    elif damage == "fit":
        call["args"]["transition"]["duration"] = 2.01
    elif damage == "stale-transition":
        destination["transition"] = None
    elif damage == "stale-track":
        call["expect"]["parent/track:V1::kind"]["value"] = "audio"
    elif damage == "stale-predecessor":
        call["expect"]["parent/clip:before::hold"]["value"] = 1.9
    elif damage == "stale-revision":
        for key in ("transition", "elementRef"):
            call["args"][key]["revision"] = "sha256:" + "0" * 64
    elif damage == "type":
        call["args"]["transition"]["type"] = "different-transition"
    else:
        call["args"]["transition"]["params"] = {"durationFrames": -1}
    refuse(before, body)


@pytest.mark.parametrize("damage", ["stale", "duplicate", "malformed", "publication"])
def test_w29_inverse_refuses_without_partial_receipt(case, damage):
    retained = case["pinned"]
    before = retained["retained_results"][0]["canonical_document"]
    body = retained["requests"][1]
    inverse = body["change"]["commands"][0]
    writes = inverse["args"]["writes"]
    if damage == "stale":
        writes[0]["before"]["value"]["duration"] = 0.732
    elif damage == "duplicate":
        writes.append(copy.deepcopy(writes[0]))
    elif damage == "malformed":
        writes[0]["after"] = dict(state="absent", value=None)
    else:
        inverse["args"]["publication"] = "unproven-publication"
    result = refuse(before, body, local=damage != "publication")
    if damage == "publication":
        assert result["status"] == "conflict"


def test_w29_late_transition_failure_rolls_back_earlier_batch_write(case):
    before = case["canonical"]["before"]
    body = case["canonical"]["requests"][0]
    invalid = copy.deepcopy(body["change"]["commands"][0])
    invalid["args"]["from_clip"] = SID
    body["change"]["commands"] = [dict(op="timeline.batch", select=None, args=dict(commands=[
        dict(op="clip.set-look", select="parent/clip:before", args=dict(opacity=0.3)), invalid]))]
    refuse(before, body)


@pytest.mark.parametrize("params", ["absent", None, {}])
def test_w29_flat_only_assignment_preserves_params_presence(case, params):
    before = case["canonical"]["before"]
    parent = before["parent"]
    parent["tracks"] = parent["config"].pop("tracks")
    body = case["canonical"]["requests"][0]
    transition = body["change"]["commands"][0]["args"]["transition"]
    if params == "absent":
        del transition["params"]
    else:
        transition["params"] = params
    result = accept(before, body)
    after = result["canonical_document"]["parent"]
    assert "tracks" not in after["config"]
    assert literal(after["tracks"]) == literal(parent["tracks"])
    assert literal(after["clips"][1]["transition"]) == literal(transition)
