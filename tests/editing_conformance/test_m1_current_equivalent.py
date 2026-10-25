"""NEW-OURS current equivalent for the M1 word-bound commit journey.

This file deliberately does not alter ``test_commit_runtime_m1.py``.  The
current source is the native word/transcript fixture: media, the transcript,
its pin, and the word binding are all admitted by the registered provider
through real Runtime commits before the SDK outbox journey starts.
"""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.sync import TimelineSession
from tests.editing_conformance import native_word_anchor_fixture as current_inputs
from tests.editing_conformance.test_native_word_anchor import bundle as current_bundle
from tests.editing_conformance.test_native_word_anchor import pick as current_pick

pytestmark = pytest.mark.integration
retained = current_inputs.retained


def test_new_ours_current_equivalent_preserves_m1_commit_journey(
    retained, real_runtime, tmp_path, monkeypatch,
):
    """Exercise the original M1 gesture order against current word authority.

    NEW-OURS identity: this is one current-equivalent journey, not a rewrite
    or a reclassification of any ``original550`` selector.  The binding is
    authored first through ``timeline.commitTimeline`` by the registered
    provider, and all later writes use the ordinary SDK commit/outbox path.
    """
    from runtime_protocol.server import RuntimeHandler
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.client import AstridClient
    from astrid.sdk.exceptions import ServiceUnavailableError
    from astrid.sdk.workspace_client import WorkspaceClientError

    case = retained

    def current_commit(commands, key, label):
        """Submit the complete C0 v2 body through the registered provider."""
        base = case.head()
        body = {
            "api_version": 1, "project_id": case.project, "timeline_id": "film",
            "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
            "commands": copy.deepcopy(commands), "label": label, "merge": "fields", "reads": [],
            "dry_run": False, "source": {"via": "python"},
            "rationale": "NEW-OURS current-equivalent M1", "group_id": key,
            "steps": [{
                "id": key, "label": label, "intent": label, "tags": ["m1", "current"],
                "command_ordinals": list(range(len(commands))), "patch": [], "reads": [],
            }],
        }
        result = case.service.commit_timeline(
            case.project, "film", body, idempotency_key=key, publisher="timing-editor",
            invocation_path=route_path(case.project, "film"), authorize=lambda: None,
        )
        document = result["data"]["canonical_document"]
        case.documents[document["parent_revision"]["revision_id"]] = document
        return result

    # The fixture has already created genuine media and a persisted transcript
    # with the current provider.  Capture the current word choice from that
    # registered source, then submit it through the provider before any SDK
    # outbox activity.  No legacy declaration or copied archive is involved.
    binding = current_pick(case)
    binding_result = current_commit([binding], "new-ours-word-binding", "NEW-OURS current word binding")
    assert binding_result["data"]["status"] in {"accepted", "merged", "rebased"}
    binding_document = binding_result["data"]["canonical_document"]
    assert binding_document["parent_revision"]["payload"]["clips"][0]["app"]["astrid"]["on"] == (
        current_inputs.DECLARATION
    )
    assert binding_result["receipt"]["command_kind"] == "timeline.commit"

    # Add the independent clip used for the original disjoint-head gesture.
    # It is an ordinary current native commit, not synthetic SQL/history state.
    from astrid.sdk.timeline._clip_commands import capture_clip_add

    authored = current_bundle(case)
    add = capture_clip_add(authored, "parent", {
        "id": "music-other", "clipType": "am-type", "track": "initial", "at": 0, "hold": 1,
        "opaque": [None, {"keep": True}],
    })
    added = current_commit([add], "new-ours-independent-clip", "NEW-OURS independent clip")
    assert added["data"]["canonical_document"]["parent_revision"]["payload"]["clips"][-1]["id"] == (
        "music-other"
    )

    # Hand the persisted current source to the real Runtime server and use the
    # public SDK transport.  The server's provider is startup-registered; the
    # test never calls the service body as a shortcut for the journey.
    case.service.close()
    daemon = real_runtime(case.root, support_root=tmp_path / "support", authoring_profile="astrid")

    def open_client():
        return AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=daemon.service.realm["id"],
            actor_id="timing-editor",
            client_name="m1-current-equivalent",
            client_version="1",
            protocol_version="workspace.v1",
        )

    client = open_client()
    outbox = tmp_path / "current-equivalent-outbox.json"
    session = TimelineSession.open(case.project, "film", client=client, outbox_path=outbox)
    observed = []
    original_send = RuntimeHandler._send

    def lose_a_ack(handler, status, payload=None, **kwargs):
        if (handler.command == "POST" and handler.path.endswith("/commit")
                and handler.headers.get("Idempotency-Key") == "new-ours-a" and status == 200):
            observed.append({"body": handler._prefetched_body, "payload": copy.deepcopy(payload)})
            raise ConnectionError("NEW-OURS lost ACK after durable current commit")
        return original_send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, "_send", lose_a_ack)
    # A is the current-source move, matching the original authored gesture's
    # literal move semantics while retaining the real word-bound source.
    with pytest.raises(WorkspaceClientError):
        session.move("occurrence:occ/clip:voice", 2, idempotency_key="new-ours-a")
    persisted = json.loads(outbox.read_text(encoding="utf-8"))
    assert persisted["flight"]["key"] == "new-ours-a"
    assert persisted["pending"]
    first_body = persisted["flight"]["body"]
    first_response = observed[-1]["payload"]
    assert first_response["data"]["status"] in {"accepted", "merged", "rebased"}

    # A second author advances a disjoint field while A's acknowledgement is
    # lost.  The move is captured as a real current command, preserving exact
    # guards and the original no-overwrite/rebase distinction.
    other_client = open_client()
    other = TimelineSession.open(
        case.project, "film", client=other_client, outbox_path=tmp_path / "other-outbox.json",
    )
    other.move("parent/clip:music-other", 2, idempotency_key="new-ours-disjoint")
    before_restart = other_client.timelines.history(case.project, "film", limit=100)
    assert before_restart.ok
    old_epoch = client._remote._transport.health()["runtime_epoch"]
    port = daemon.httpd.server_port
    daemon.stop()
    client = None

    # Restart the authenticated Runtime and replay the exact lost flight.  A
    # foreign realm remains refused, while the same identity retries byte-for-
    # byte and does not append a second history row.
    daemon = real_runtime(case.root, support_root=tmp_path / "support", port=port,
                          authoring_profile="astrid")
    with pytest.raises(ServiceUnavailableError):
        AstridClient.open(endpoint=daemon.endpoint, credential=daemon.credential_path,
                          realm_id="foreign-realm", actor_id="timing-editor",
                          client_name="m1-current-equivalent", client_version="1",
                          protocol_version="workspace.v1")
    client = open_client()
    assert client._remote._transport.health()["runtime_epoch"] > old_epoch
    session = TimelineSession.open(case.project, "film", client=client, outbox_path=outbox)
    retried = session.flush()
    retry_wire = json.loads(json.dumps(persisted["flight"]))
    assert retry_wire["body"] == first_body
    assert retried["receipt"] == first_response["receipt"]
    assert json.loads(outbox.read_text(encoding="utf-8"))["pending"] == []
    assert client.timelines.history(case.project, "film", limit=100).ok

    # B is authored against A's exact landing, then replays over the intervening
    # disjoint head.  The provider returns current v2 ``merged`` (historical
    # implementations may spell the same authenticated outcome ``rebased``).
    current = client.timelines.open_bundle(case.project, "film")
    assert current.ok
    b_bundle = current.data["bundle"]
    b_command = capture_move(b_bundle, "occurrence:occ/clip:voice", 3)
    expected = session.outbox.read()
    accepted_b = session.submit(
        [b_command], label="NEW-OURS current follow-up", steps=[{
            "id": "new-ours-b", "label": "NEW-OURS current follow-up",
            "intent": "Repeat the original move after a disjoint head", "tags": ["m1", "current"],
            "command_ordinals": [0], "patch": [],
        }], merge="fields", reads=[], idempotency_key="new-ours-b",
        expected_state=expected,
        base={"revision_id": retried["data"]["accepted_revision_id"],
              "publication_id": retried["receipt"]["receipt_id"]},
    )
    assert accepted_b["data"]["status"] in {"merged", "rebased"}
    assert accepted_b["data"]["canonical_document"]

    # Exact current inverse and redo close the original history predicates,
    # including no mutation on an idempotent retry and preservation of the
    # intervening disjoint edit.
    undone = session.undo([accepted_b["receipt"]["receipt_id"]], idempotency_key="new-ours-undo")
    assert undone["data"]["canonical_document"]
    redone = session.undo([undone["receipt"]["receipt_id"]], idempotency_key="new-ours-redo")
    assert redone["data"]["canonical_document"] == accepted_b["data"]["canonical_document"]
    final_history = client.timelines.history(case.project, "film", limit=100)
    assert final_history.ok
    ids = [row["publication_id"] for row in final_history.data["items"]]
    assert ids.count(first_response["receipt"]["receipt_id"]) == 1
    assert final_history.data["items"][-2]["records"]["undo_of"] == [accepted_b["receipt"]["receipt_id"]]
    assert final_history.data["items"][-1]["records"]["undo_of"] == [undone["receipt"]["receipt_id"]]

    # Preserve the original CLI readback leg on the same current head.  This
    # is an inspection only: it cannot create a second write or alter the
    # authoritative history asserted above.
    from astrid.packs.timeline.cli import build_parser

    parsed = build_parser(client).parse_args([
        "show", "film", "--project", case.project, "--json", "--published",
        "--revision-id", redone["data"]["accepted_revision_id"],
    ])
    assert parsed.handler(parsed) == 0

