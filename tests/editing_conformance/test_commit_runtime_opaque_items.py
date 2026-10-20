"""Unknown namespaced values survive real occurrence materialization."""
from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest

from tests.editing_conformance.test_commit_runtime_identity import occurrence_image
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration
NAMESPACE = "org.example.notes/v1"


def opaque():
    return {NAMESPACE: {
        "foreign_item_id": "item-1", "foreign_item_ids": ["item-2", None, "item-1"],
        "item_id": "item-1", "item_ids": ["item-1", "item-2"],
        "literal": "item-1", "item-1": None,
        "nested": [{"selected_item_id": "item-2", "parent_item_id": "item-1"}, None],
    }}


@pytest.fixture(params=["item_id", "id", "both"])
def opaque_film(request, tmp_path, monkeypatch):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / "tests"))
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from test_timeline_commit_integration import Editing
    from timeline_commit_film_fixture import build_film_fixture

    from astrid.sdk.timeline.capture import capture_move
    from astrid.sdk.timeline.commit import bundle_from_document

    fixture = build_film_fixture(tmp_path)
    service = RuntimeService(fixture.duplicate_root)
    edit = Editing(service, SimpleNamespace(fixture=fixture),
                   SimpleNamespace(move=capture_move, bundle=bundle_from_document))
    try:
        original = edit.document()
        parent = copy.deepcopy(original["parent_revision"]["payload"])
        _, source_shot, source_internal = occurrence_image(original, "occurrence-1")
        shot = {key: copy.deepcopy(source_shot[key]) for key in (
            "shot_id", "revision_id", "internal_timeline_revision_id", "payload")}
        internal = {key: copy.deepcopy(source_internal[key]) for key in (
            "timeline_id", "revision_id", "payload")}
        shot.update(revision_id="opaque-shot", internal_timeline_revision_id="opaque-internal")
        internal["revision_id"] = "opaque-internal"
        internal["payload"]["clips"][0]["hold"] = 0.25
        media = shot["payload"]["provenance"]["source_media"]
        shot["payload"]["items"] = [{
            "item_id": item_id, "media_id": media, "source_frame": None,
            "metadata": {"source_item_id": "item-1", "source_item": "item-2", "data": opaque()},
            "data": opaque(), "app": opaque(), "opaque": opaque(),
        } for item_id in ("item-1", "item-2")]
        for item in shot["payload"]["items"]:
            if request.param in ("id", "both"):
                item["id"] = item["item_id"]
            if request.param == "id":
                del item["item_id"]
        for row in (parent, parent["config"], parent["config"]["tracks"][0],
                    parent["clips"][0], shot["payload"], internal["payload"],
                    internal["payload"]["tracks"][0], internal["payload"]["clips"][0]):
            row.update(data=opaque(), app=opaque(), opaque=opaque())
        for occurrence in parent["occurrences"][:2]:
            occurrence.update(shot_id=shot["shot_id"], shot_revision_id=shot["revision_id"],
                              data=opaque(), app=opaque(), opaque=opaque())
        service.publish_parent_composition(edit.project, edit.timeline, {
            "project_id": edit.project, "timeline_id": edit.timeline,
            "expected_head": fixture.parent_revision_id, "parent_revision_id": "opaque-baseline",
            "parent_composition": parent, "shot_revisions": [shot],
            "internal_timeline_revisions": [internal],
        }, idempotency_key="opaque-baseline")
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        yield edit, load_timeline_commit_provider
    finally:
        edit.service.close()


def assert_opaque(row):
    for field in ("data", "app", "opaque"):
        # The moved clip's app.astrid timing fields are declared writes.
        assert {key: value for key, value in row[field].items() if key != "astrid"} == opaque()


def assert_readback(edit, document):
    assert edit.document(document["parent_revision"]["revision_id"]) == document
    for shot in document["shot_revisions"]:
        stored = edit.service.get_project_shot_revision(edit.project, shot["shot_id"], shot["revision_id"])
        assert stored["payload"] == shot["payload"]
        assert stored["content_digest"] == shot["content_digest"]
    for internal in document["internal_timeline_revisions"]:
        stored = edit.service.get_project_timeline_revision(
            edit.project, edit.timeline, internal["revision_id"])
        assert stored["payload"] == internal["payload"]
        assert stored["content_digest"] == internal["content_digest"]


def test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse(
    opaque_film, tmp_path, monkeypatch,
):
    from runtime_protocol.service import RuntimeService

    edit, provider = opaque_film
    original = edit.document()
    original_copy = copy.deepcopy(original)
    command = edit.agent.move(edit.agent.bundle(original), "occurrence:occurrence-1/clip:clip-1", 0.5)
    body = edit.body([command])
    flight = tmp_path / "flight.json"
    flight.write_text(json.dumps({"key": "opaque-lost-ack", "body": body}))
    accepted = edit.commit(body, "opaque-lost-ack")
    assert accepted["data"]["status"] == "accepted"
    document = accepted["data"]["canonical_document"]
    history = edit.history()
    writes = history[-1]["records"]["commands"][0]["writes"]
    _, _, internal = occurrence_image(document, "occurrence-1")
    assert internal["payload"]["clips"][0]["at"] == 0.5
    assert not any("data" in write["path"] or "opaque" in write["path"] for write in writes)
    assert edit.document() == document
    assert original == original_copy
    assert edit.document(original["parent_revision"]["revision_id"]) == original
    for sibling in ("occurrence-2", "occurrence-3"):
        assert occurrence_image(document, sibling) == occurrence_image(original, sibling)
    edit.service.close()
    edit.service = RuntimeService(edit.film.fixture.duplicate_root)
    edit.service.register_timeline_commit_provider(provider("astrid"))
    persisted = json.loads(flight.read_text())

    def forbidden(*args, **kwargs):
        raise AssertionError("exact retry executed the provider")

    with monkeypatch.context() as retry:
        retry.setattr(type(edit.service._timeline_commit_provider), "commit", forbidden)
        assert edit.commit(persisted["body"], persisted["key"]) == accepted
    assert edit.document() == document
    assert edit.history() == history
    inverse = {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
               "args": {"publications": [accepted["receipt"]["receipt_id"]]}}
    undone = edit.commit(edit.body([inverse]), "opaque-undo")
    for image in (document, undone["data"]["canonical_document"]):
        assert_preserved(image, materialized=image == document)
        assert_readback(edit, image)
        for sibling in ("occurrence-2", "occurrence-3"):
            assert occurrence_image(image, sibling) == occurrence_image(original, sibling)
    assert_readback(edit, original)
    assert edit.history()[:-1] == history


def assert_preserved(document, *, materialized):
    occurrence, shot, internal = occurrence_image(document, "occurrence-1")
    assert_opaque(shot["payload"])
    identities = [item.get("item_id", item.get("id")) for item in shot["payload"]["items"]]
    for item, source in zip(shot["payload"]["items"], ("item-1", "item-2")):
        if materialized:
            assert item.get("item_id", item.get("id")) != source
        if "item_id" in item and "id" in item:
            assert item["item_id"] == item["id"]
        assert item["metadata"]["source_item_id"] == identities[0]
        assert item["metadata"]["source_item"] == identities[1]
        assert item["metadata"]["data"] == opaque()
        assert_opaque(item)
    for row in (document["parent_revision"]["payload"],
                document["parent_revision"]["payload"]["config"],
                document["parent_revision"]["payload"]["config"]["tracks"][0],
                document["parent_revision"]["payload"]["clips"][0], occurrence,
                internal["payload"], internal["payload"]["tracks"][0],
                internal["payload"]["clips"][0]):
        assert_opaque(row)


@pytest.mark.xfail(strict=True, reason="M1 historical-image reuse must restore the exact original closure")
def test_occurrence_inverse_restores_exact_original_closure(opaque_film):
    edit, _ = opaque_film
    original = edit.document()
    command = edit.agent.move(edit.agent.bundle(original), "occurrence:occurrence-1/clip:clip-1", 0.5)
    accepted = edit.commit(edit.body([command]), "opaque-exact-move")
    inverse = {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
               "args": {"publications": [accepted["receipt"]["receipt_id"]]}}
    undone = edit.commit(edit.body([inverse]), "opaque-exact-undo")
    assert undone["data"]["canonical_document"] == original
    assert edit.document() == original
