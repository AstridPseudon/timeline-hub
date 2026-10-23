"""Bounded real-Runtime qualification for restructure's guarded inverse."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.sync import CommitConflict
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk.test_timeline_restructure import restructure_runtime  # noqa: F401


@pytest.fixture
def restructure_inverse_runtime(restructure_runtime, monkeypatch):  # noqa: F811
    """Use the production authenticated revision/publication-pair reader for this test."""
    from astrid.sdk.remote import RemoteTimelines

    env = restructure_runtime
    monkeypatch.setattr(
        env.generated,
        "get_project_parent_composition_revision",
        lambda project, timeline_id, revision: env.service.get_project_parent_composition_revision(
            project, timeline_id, revision
        ),
        raising=False,
    )
    monkeypatch.setattr(
        env.generated,
        "get_project_shot_revision",
        lambda project, shot_id, revision: env.service.get_project_shot_revision(project, shot_id, revision),
        raising=False,
    )
    monkeypatch.setattr(
        env.generated,
        "get_project_timeline_revision",
        lambda project, timeline_id, revision: env.service.get_project_timeline_revision(
            project, timeline_id, revision
        ),
        raising=False,
    )
    monkeypatch.setattr(
        env.client.timelines,
        "open_bundle",
        RemoteTimelines.open_bundle.__get__(env.client.timelines),
    )

    def document():
        head = env.service.get_project_timeline(env.project, "t")
        opened = env.client.timelines.open_bundle(
            env.project,
            "t",
            revision_id=head["head_revision_id"],
            publication_id=head["head_publication_id"],
        )
        assert opened.ok, opened.as_dict()
        return copy.deepcopy(opened.data["bundle"]["source_mapping"]["_runtime_document"])

    env.document = document
    return env


def test_restructure_whole_inverse_redo_and_intervening_overlap_refusal(
    restructure_inverse_runtime, tmp_path, monkeypatch
):  # noqa: F811
    env = restructure_inverse_runtime

    source = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "name.json")
    source.bundle["shots"][source._shot_ids()[0]]["payload"]["name"] = "02 TWO"
    source.commit("Name source chapter", idempotency_key="inverse-name")
    env.calls.clear()
    env.replies.clear()
    before = copy.deepcopy(env.document())
    before_head = env.client.timelines.history(env.project, "t", limit=1).data["head"]

    def no_narration_media(**_kwargs):
        raise TimelineEditError("qualification keeps the restructure as one publication")

    monkeypatch.setattr(env.client.media, "import_bytes", no_narration_media)
    cut = Checkout.open(env.project, "t", client=env.client).publish(
        "Restructure", restructure=True, client=env.client, idempotency_key="inverse-cut"
    )
    after = copy.deepcopy(env.document())
    restructure_reply = env.replies[0]
    assert cut["narration_error"]
    request = env.calls[0][0]
    assert {key: request[key] for key in (
        "api_version", "project_id", "timeline_id", "base_revision_id", "base_publication_id",
        "commands", "label", "steps", "merge", "reads", "dry_run", "source",
    )} == {
        "api_version": 1, "project_id": env.project, "timeline_id": "t",
        "base_revision_id": before_head["revision_id"], "base_publication_id": before_head["publication_id"],
        "commands": request["commands"], "label": "Restructure", "steps": request["steps"],
        "merge": "atomic", "reads": [{"kind": "scope", "ref": "timeline", "path": []},
                                    ], "dry_run": False, "source": {"via": "python"},
    }
    assert request["commands"][0]["op"] == "timeline.restructure"
    assert "rationale" not in request and "group_id" not in request
    assert request["steps"][-1] == {
        "id": request["steps"][-1]["id"], "label": "Restructure", "intent": "Store chapters as shots",
        "tags": ["restructure"], "command_ordinals": [len(request["commands"]) - 1], "patch": [],
    }
    assert len(after["shot_revisions"]) == len(after["internal_timeline_revisions"]) == 3
    assert len(after["parent_revision"]["payload"]["occurrences"]) == 3
    assert before["parent_revision"]["payload"]["opaque"] == {"null": None, "ordered": [None, False, 0]}
    assert after["parent_revision"]["payload"]["opaque"] == before["parent_revision"]["payload"]["opaque"]
    accepted = restructure_reply["data"]
    assert accepted["status"] == "accepted"
    assert accepted["canonical_document"] == after
    assert accepted["accepted_revision_id"] == after["parent_revision"]["revision_id"]
    assert accepted["merge_mode"] == "atomic"
    assert accepted["document_digest"]
    assert restructure_reply["receipt"]["receipt_id"]
    stored = next(item for item in env.client.timelines.history(env.project, "t", limit=200).data["items"]
                  if item["publication_id"] == restructure_reply["receipt"]["receipt_id"])
    assert stored["records"]["undo_of"] == [] and stored["records"]["undo_steps"] is None

    reopened = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "inverse.json")
    try:
        undone = reopened.session.undo(
            [restructure_reply["receipt"]["receipt_id"]], idempotency_key="inverse-undo"
        )
    except WorkspaceClientError as exc:
        import runtime_protocol

        from astrid.sdk.timeline import publish as publish_module

        print(json.dumps({
            "kind": "g5-runtime-inverse-failure",
            "error": {"type": type(exc).__name__, "message": str(exc),
                      "code": getattr(exc, "code", None), "details": getattr(exc, "details", None)},
            "request": env.calls[-1][0],
            "prepared_input_history": env.client.timelines.history(env.project, "t", limit=200).data,
            "canonical_before": before,
            "canonical_after": after,
            "origins": {
                "agent_publish": publish_module.__file__,
                "agent_test": __file__,
                "runtime_protocol": runtime_protocol.__file__,
            },
        }, sort_keys=True))
        raise
    undo_document = undone["data"]["canonical_document"]
    assert undo_document["parent_revision"]["payload"] == before["parent_revision"]["payload"]
    assert [row["payload"] for row in undo_document["shot_revisions"]] == [
        row["payload"] for row in before["shot_revisions"]
    ]
    assert [row["payload"] for row in undo_document["internal_timeline_revisions"]] == [
        row["payload"] for row in before["internal_timeline_revisions"]
    ]
    assert undo_document["dependency_manifest"] == before["dependency_manifest"]

    redone = reopened.session.undo([undone["receipt"]["receipt_id"]], idempotency_key="inverse-redo")
    redo_document = redone["data"]["canonical_document"]
    assert redo_document["parent_revision"]["payload"] == after["parent_revision"]["payload"]
    assert [row["payload"] for row in redo_document["shot_revisions"]] == [
        row["payload"] for row in after["shot_revisions"]
    ]
    assert [row["payload"] for row in redo_document["internal_timeline_revisions"]] == [
        row["payload"] for row in after["internal_timeline_revisions"]
    ]
    assert redo_document["dependency_manifest"] == after["dependency_manifest"]

    later = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "later.json")
    bed = next(clip for clip in later.bundle["parent"]["clips"] if clip["id"] == "bed")
    bed["volume"] = 0.25
    overlap = later.commit("Later authored overlap", merge="fields", reads=[], idempotency_key="inverse-overlap")
    assert overlap["data"]["status"] == "accepted"

    refusing = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "refusing.json")
    head_before_refusal = env.client.timelines.history(env.project, "t", limit=1).data["head"]
    history_before_refusal = copy.deepcopy(env.client.timelines.history(env.project, "t", limit=200).data)
    canonical_before_refusal = copy.deepcopy(env.document())
    try:
        refusing.session.undo([redone["receipt"]["receipt_id"]], idempotency_key="inverse-refuse")
    except CommitConflict as exc:
        assert "intervening" in str(exc)
    else:
        raise AssertionError("the overlapping authored write must refuse the guarded inverse")
    assert env.client.timelines.history(env.project, "t", limit=1).data["head"] == head_before_refusal
    assert env.client.timelines.history(env.project, "t", limit=200).data == history_before_refusal
    assert env.document() == canonical_before_refusal
