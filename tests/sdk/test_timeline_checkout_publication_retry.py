"""Publication undo and redo reuse their exact persisted request after lost ACK."""
import copy
import json

import pytest
from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance.test_recipe_clip_scalar_fields import app_closure
from tests.sdk.test_timeline_checkout_history import native  # noqa: F401
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


def test_detached_numeric_move_publish_uses_native_commit_and_retry(native, tmp_path):
    """The existing Checkout edit/publish consumer uses clip.move, not whole publication."""
    client, generated = native
    parent, shots, internals = app_closure()
    parent["project_id"], parent["timeline_id"] = "p", "t"
    for shot in shots:
        shot["project_id"] = "p"
    for internal in internals:
        internal["project_id"], internal["timeline_id"] = "p", "t"
    bundle = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    bundle["base_parent"]["revision_id"] = "r0"
    generated.bundles["r0"] = copy.deepcopy(bundle)

    checkout = Checkout.open("p", "t", revision_id="r0", client=client)
    checkout.clips[2].on(7)
    accepted = checkout.publish("move the clear clip", client=client, idempotency_key="checkout-move")
    assert accepted["new_head"] == "r1"
    assert json.loads(generated.calls[0][0])["commands"][0]["op"] == "clip.move"

    reloaded = Checkout.open("p", "t", revision_id="r1", client=client)
    assert reloaded.clips[2].start == pytest.approx(7)
    undone = reloaded.undo(publications=[accepted["receipt"]["receipt_id"]], client=client,
                           idempotency_key="checkout-undo")
    assert generated.bundles[undone["data"]["accepted_revision_id"]] == generated.bundles["r0"]

    draft = Checkout.open("p", "t", revision_id=generated.head["revision_id"], client=client)
    # The generated transport fake keeps the command-engine bundle while the
    # real Runtime read returns a fresh base-parent revision.
    draft.bundle["base_parent"]["revision_id"] = generated.head["revision_id"]
    draft.clips[2].on(8)
    path = tmp_path / "move.json"
    draft.save(path, quiet=True)
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        draft.publish("move after undo", client=client, idempotency_key="checkout-lost")
    flight = json.loads(generated.path.read_text())["flight"]
    retried = Checkout.load(path).publish("move after undo", client=client, idempotency_key="checkout-lost")
    assert retried["receipt"] == generated.accepted["checkout-lost"][1]["receipt"]
    assert generated.calls[-1] == generated.calls[-2] == (flight["body"].encode(), "checkout-lost")
    assert [json.loads(body)["commands"][0]["op"] for body, _key in generated.calls] == [
        "clip.move", "timeline.inverse", "clip.move", "clip.move"]
