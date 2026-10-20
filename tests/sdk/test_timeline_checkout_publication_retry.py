"""Publication undo and redo reuse their exact persisted request after lost ACK."""
import json

import pytest
from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.sdk.timeline import store
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk.test_timeline_checkout_history import native  # noqa: F401
from tests.editing_conformance.test_recipe_clip_scalar_fields import app_closure
from tests.sdk.test_timeline_sync import connected  # noqa: F401


@pytest.mark.parametrize("operation", ["undo", "redo"])
def test_publication_retry_survives_handle_reload(operation, native, tmp_path):
    client, generated = native
    accepted = TimelineSession.open("p", "t", client=client).move("parent/clip:a", 5)
    checkout = Checkout.open("p", "t", revision_id=generated.head["revision_id"], client=client)
    publication = accepted["receipt"]["receipt_id"]
    expected = "r0"
    if operation == "redo":
        undone = checkout.undo(publications=[publication], client=client)
        publication = undone["receipt"]["receipt_id"]
        expected = "r1"
    checkout.save(tmp_path / "detached.json", quiet=True)
    saved = checkout.path.read_bytes()
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        getattr(checkout, operation)(publications=[publication], client=client,
                                     idempotency_key="review-" + operation)
    flight = json.loads(generated.path.read_text())["flight"]
    reloaded = Checkout.load(checkout.path)
    result = getattr(reloaded, operation)(publications=[publication], client=client)
    assert generated.calls[-1] == generated.calls[-2]
    assert generated.calls[-1][0].decode() == flight["body"]
    assert generated.calls[-1][1] == flight["key"] == "review-" + operation
    assert generated.bundles[result["data"]["accepted_revision_id"]] == generated.bundles[expected]
    assert checkout.path.read_bytes() == saved
    state = json.loads(generated.path.read_text())
    assert state["flight"] is None and state["pending"] == []


def test_detached_numeric_move_uses_original_command_and_rebases_without_legacy_writer(native, monkeypatch, tmp_path):
    client, generated = native
    parent, shots, internals = app_closure()
    parent.update(project_id="p", timeline_id="t")
    for row in [*shots, *internals]:
        row["project_id"] = "p"
    generated.bundles["r0"] = open_authoring_bundle(parent, shot_revisions=shots,
                                                       internal_timeline_revisions=internals)
    generated.bundles["r0"]["base_parent"]["revision_id"] = "r0"
    checkout = Checkout.open("p", "t", revision_id="r0", client=client)
    checkout.clips[2].on(7)
    queued = json.loads(generated.path.read_text())
    command = queued["pending"][0]
    assert command["op"] == "clip.move"
    assert command["select"] == "occurrence:f2-occurrence/clip:f2-agent-clear-clip"
    assert command["expect"]["occurrence:f2-occurrence/clip:f2-agent-clear-clip::at"] == {
        "state": "present", "value": 6}

    peer = execute(generated.bundles["r0"], [capture_move(
        generated.bundles["r0"], "occurrence:shared-sibling/clip:f2-agent-clear-clip", 23)]).bundle
    generated.bundles["peer"] = peer
    generated.head = {"revision_id": "peer", "publication_id": "peer-publication"}
    monkeypatch.setattr(store, "publish_bundle", lambda *args, **kwargs: pytest.fail("legacy writer called"))

    result = checkout.publish("move a", client=client, idempotency_key="move-a")
    assert result["receipt"]["result"]["rationale"] == "move a"
    assert json.loads(generated.calls[0][0])["commands"] == [command]
    assert result["new_head"] == "r1"
    assert generated.bundles["r1"]["shots"][
        generated.bundles["r1"]["placements"][0]["shot_id"]]["internal_timeline"]["clips"][2]["at"] == 7
    assert generated.bundles["r1"]["shots"][
        generated.bundles["r1"]["placements"][1]["shot_id"]]["internal_timeline"]["clips"][2]["at"] == 3

    generated.lose_ack = True
    generated.bundles["r1"]["base_parent"]["revision_id"] = "r1"
    next_checkout = Checkout.open("p", "t", revision_id="r1", client=client)
    next_checkout.clips[2].on(9)
    path = tmp_path / "move.json"
    next_checkout.save(path, quiet=True)
    with pytest.raises(WorkspaceClientError):
        next_checkout.publish("move a again", client=client, idempotency_key="move-a-again")
    flight = json.loads(generated.path.read_text())["flight"]

    restarted = Checkout.load(path)
    retried = restarted.publish("ignored after restart", client=client, idempotency_key="move-a-again")
    assert retried["receipt"] == generated.accepted["move-a-again"][1]["receipt"]
    assert generated.calls[-1] == generated.calls[-2] == (flight["body"].encode(), "move-a-again")

    undone = restarted.undo(publications=[retried["receipt"]["receipt_id"]], client=client,
                            idempotency_key="undo-move-a")
    assert generated.bundles[undone["data"]["accepted_revision_id"]] == generated.bundles["r1"]
