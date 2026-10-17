"""Retained W13 App inputs; actual SDK, in-memory Runtime acceptance only."""
import copy
import json
from pathlib import Path

import pytest
from test_timeline_commit import CoreService, Port
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")
FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/w13_fade_history.json"
SID = "occurrence:occ-A/clip:clip-1"


def literal(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


@pytest.fixture
def case():
    return json.loads(FIXTURE.read_text())


class FadePort(Port):
    def accept(self, prepared):
        value = super().accept(prepared)
        result = value["stored_result"]
        index = int(self.current.rsplit("r", 1)[1]) + 1
        result.update(accepted_revision_id=f"parent-r{index}",
                      accepted_publication_id=f"pub-parent-r{index}")
        self.saved["result"] = copy.deepcopy(result)
        return value


def port_for(document, body):
    port = FadePort(body, {body["base_revision_id"]: document})
    port.current = body["base_revision_id"]
    return port


def accept(document, body):
    snapshot = literal(document), literal(body)
    port = port_for(document, body)
    service = CoreService()
    result = service.commit(body, port)
    assert result["status"] == "accepted", result
    assert len(port.accepts) == 1
    assert result == service.commit(body, port)  # exact request replay
    assert len(port.accepts) == 1
    assert (literal(document), literal(body)) == snapshot
    assert port.accepts[0]["evidence"]["direct_writes"] == result["change"]["direct_writes"]
    replay, plan, _ = RuntimeCommitService._apply(document, result["change"]["commands"])
    assert literal(replay) == literal(result["canonical_document"])
    assert list(plan.direct_writes) == result["change"]["direct_writes"]
    return result


def reverse_receipt(result):
    """App history uses only the accepted direct receipt, never a document diff."""
    return dict(op="timeline.inverse", select=None, args=dict(
        publication=result["accepted_publication_id"], writes=[
            {**copy.deepcopy(write), "before": copy.deepcopy(write["after"]),
             "after": copy.deepcopy(write["before"])}
            for write in result["change"]["direct_writes"]]))


def test_w13_exact_publication_undo_receipt_arms_lossless_redo(case, tmp_path):
    before = case["before"]
    forward = accept(before, case["requests"][0])
    forward_writes = forward["change"]["direct_writes"]
    assert {(w["id"], w["path"]) for w in forward_writes} == {
        (SID, "effects.fade_in"), (SID, "entrance")}
    # These are the retained App-authored Undo bytes, bound to this publication.
    undo_body = case["requests"][1]
    assert undo_body["change"]["commands"] == [reverse_receipt(forward)]
    undone = accept(forward["canonical_document"], undo_body)
    assert literal(undone["canonical_document"]) == literal(before)
    assert undone["change"]["direct_writes"] == reverse_receipt(forward)["args"]["writes"]
    entrance = next(w for w in undone["change"]["direct_writes"] if w["path"] == "entrance")
    assert entrance["id"] == SID
    assert entrance["after"] == dict(state="present", value={
        "type": "fade", "duration": 0.4, "opaque": {"keep": None}})

    redo_body = copy.deepcopy(undo_body)
    redo_body.update(request_id="w13-receipt-only-redo", session_sequence=3,
                     base_revision_id=undone["accepted_revision_id"])
    redo_body["change"]["commands"] = [reverse_receipt(undone)]
    redone = accept(undone["canonical_document"], redo_body)
    assert literal(redone["canonical_document"]) == literal(forward["canonical_document"])
    clip = redone["canonical_document"]["shots"]["A"]["internal_timeline"]["clips"][0]
    assert clip["entrance"]["duration"] == 0.37
    (tmp_path / "w13-publication-proof.json").write_text(json.dumps(dict(
        before=before, requests=[case["requests"][0], undo_body, redo_body],
        results=[forward, undone, redone]), indent=2) + "\n")


@pytest.mark.parametrize("bad", ["stale", "malformed", "duplicate", "out-of-scope"])
def test_w13_inverse_refuses_bad_entrance_write_atomically(case, bad):
    forward = accept(case["before"], case["requests"][0])
    document = copy.deepcopy(forward["canonical_document"])
    body = copy.deepcopy(case["requests"][1])
    writes = body["change"]["commands"][0]["args"]["writes"]
    entrance = writes[1]
    assert entrance["path"] == "entrance" and writes[0]["path"] == "effects.fade_in"
    if bad == "stale":
        entrance["before"]["value"]["duration"] = 0.9
    elif bad == "malformed":
        entrance["after"] = dict(state="absent", value=None)
    elif bad == "duplicate":
        writes.append(copy.deepcopy(entrance))
    else:
        # Valid guarded foreign write: scope must reject the entire candidate,
        # including the preceding valid fade write, after inverse execution.
        foreign = copy.deepcopy(document["shots"]["A"]["internal_timeline"]["clips"][0])
        foreign["id"] = "outside"
        document["parent"]["clips"].append(foreign)
        entrance["id"] = "parent/clip:outside"
        body["scope"] = copy.deepcopy(case["requests"][0]["scope"])
    snapshot = literal(document)
    port = port_for(document, body)
    result = CoreService().commit(body, port)
    assert result["status"] in {"refused", "conflict"}, result
    assert not port.accepts and port.saved is None
    assert result["canonical_document"] is None
    assert not result["change"]["direct_writes"]
    assert literal(document) == snapshot
    assert literal(port.bundles[body["base_revision_id"]]) == snapshot
    if bad == "out-of-scope":
        # The raw inverse can execute, so this refusal proves publication scope.
        applied, _, _ = RuntimeCommitService._apply(document, body["change"]["commands"])
        assert literal(applied) != snapshot
        assert "scope" in result["error"]["message"].lower()
    else:
        tl = Checkout(copy.deepcopy(document))
        with pytest.raises(commands.TimelineEditError):
            commands.run(tl, body["change"]["commands"][0])
        assert literal(tl.document()) == snapshot
