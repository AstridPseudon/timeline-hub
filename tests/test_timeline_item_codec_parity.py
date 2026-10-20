"""Publicly published item codecs agree with Agent and physical projection keys."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from runtime_protocol.service import RuntimeService
from test_timeline_commit_integration import Editing, inverse, rows
from test_timeline_commit_acceptance import realm  # noqa: F401
from test_timeline_projection_occupancy import image, media_item, proposal, with_media
from timeline_commit_film_fixture import build_film_fixture


SHAPES = ["primary", "fallback", "mirrors", "opaque", "opaque-bool"]


def identity_fields(shape):
    return {
        "primary": {"item_id": "item-I"},
        "fallback": {"id": "item-I"},
        "mirrors": {"item_id": "item-I", "id": "item-I"},
        "opaque": {"item_id": "item-I", "id": "OPAQUE"},
        "opaque-bool": {"item_id": "item-I", "id": True},
    }[shape]


def occurrence_image(document, owner="occurrence-1"):
    occurrence = next(o for o in document["parent_revision"]["payload"]["occurrences"]
                      if o["occurrence_id"] == owner)
    shot = next(s for s in document["shot_revisions"] if s["revision_id"] == occurrence["shot_revision_id"])
    internal = next(i for i in document["internal_timeline_revisions"]
                    if i["revision_id"] == shot["internal_timeline_revision_id"])
    return occurrence, shot, internal


@pytest.fixture(params=SHAPES)
def codec_film(request, tmp_path):
    fixture = build_film_fixture(tmp_path)
    service = RuntimeService(fixture.duplicate_root)
    editing = Editing(service, SimpleNamespace(fixture=fixture), None)
    try:
        original = editing.document()
        parent = copy.deepcopy(original["parent_revision"]["payload"])
        _, source, internal = occurrence_image(original)
        shot = {k: copy.deepcopy(source[k]) for k in (
            "shot_id", "revision_id", "internal_timeline_revision_id", "payload")}
        shot["revision_id"] = "codec-shot"
        internal = {k: copy.deepcopy(internal[k]) for k in ("timeline_id", "revision_id", "payload")}
        internal["revision_id"] = "codec-internal"
        internal["payload"]["clips"][0]["hold"] = 0.25
        shot["internal_timeline_revision_id"] = internal["revision_id"]
        item = {**identity_fields(request.param), "media_id": fixture.media_ids[0],
                "metadata": {"opaque": [None, "item-I", True]},
                "data": {"foreign_item_id": "item-I", "literal": "OPAQUE"}}
        shot["payload"]["items"] = [item]
        _, other, _ = occurrence_image(original, "occurrence-3")
        other = {k: copy.deepcopy(other[k]) for k in (
            "shot_id", "revision_id", "internal_timeline_revision_id", "payload")}
        other["revision_id"] = "codec-unrelated-shot"
        # A distinct secondary value can coincide with another owner's actual
        # primary key. It must neither reserve that key nor modify its row.
        other["payload"]["items"] = [{"item_id": "OPAQUE", "media_id": fixture.media_ids[2]}]
        parent["occurrences"][2]["shot_revision_id"] = other["revision_id"]
        for occurrence in parent["occurrences"][:2]:
            occurrence.update(shot_id=shot["shot_id"], shot_revision_id=shot["revision_id"])
        publication = service.publish_parent_composition(editing.project, editing.timeline, {
            "project_id": editing.project, "timeline_id": editing.timeline,
            "expected_head": fixture.parent_revision_id, "parent_revision_id": "codec-parent",
            "parent_composition": parent, "shot_revisions": [shot, other],
            "internal_timeline_revisions": [internal],
        }, idempotency_key="codec-publication")
        assert publication["data"]["new_head"] == "codec-parent"
        # No SQL seeding or schema substitution: these are ordinary API bytes.
        stored = service.get_project_shot_revision(editing.project, shot["shot_id"], "codec-shot")
        assert stored["payload"]["items"] == [item]
        assert occurrence_image(editing.document())[1]["payload"]["items"] == [item]
        assert [tuple(r) for r in service.store.conn.execute(
            "SELECT id, shot_id FROM shot_items ORDER BY id")] == [("OPAQUE", "shot-3"), ("item-I", "shot-1")]
        assert service.store.integrity_report()["ok"]
        yield editing, request.param, item
    finally:
        editing.service.close()


def test_public_publication_preserves_item_codec_and_primary_sql_key(codec_film):
    editing, _, item = codec_film
    editing.service.close()
    editing.service = RuntimeService(editing.film.fixture.duplicate_root)
    assert occurrence_image(editing.document())[1]["payload"]["items"] == [item]
    assert editing.service.get_project_shot(editing.project, "shot-1")["items"][0]["item_id"] == "item-I"


@pytest.mark.integration
def test_actual_move_readback_reopen_retry_inverse_preserve_secondary(codec_film, astrid_importable, monkeypatch):
    from astrid.sdk.timeline.capture import capture_move
    from astrid.sdk.timeline.commit import bundle_from_document
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    editing, shape, item = codec_film
    editing.agent = SimpleNamespace(move=capture_move, bundle=bundle_from_document)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    original = editing.document()
    command = editing.agent.move(editing.agent.bundle(original), "occurrence:occurrence-1/clip:clip-1", 0.5)
    body = editing.body([command])
    accepted = editing.commit(body, "codec-move")
    assert accepted["data"]["status"] == "accepted"
    document = accepted["data"]["canonical_document"]
    _, shot, internal = occurrence_image(document)
    moved = shot["payload"]["items"][0]
    primary = moved.get("item_id", moved.get("id"))
    assert primary != "item-I"
    expected = copy.deepcopy(item)
    for field in ("item_id", "id"):
        if expected.get(field) == "item-I":
            expected[field] = primary
    assert moved == expected
    if shape.startswith("opaque"):
        assert type(moved["id"]) is type(item["id"])
        assert moved["id"] == item["id"]
    assert internal["payload"]["clips"][0]["at"] == 0.5
    assert occurrence_image(document, "occurrence-2") == occurrence_image(original, "occurrence-2")
    assert occurrence_image(document, "occurrence-3") == occurrence_image(original, "occurrence-3")
    assert [tuple(r) for r in editing.service.store.conn.execute(
        "SELECT id, shot_id FROM shot_items ORDER BY id")] == sorted([
            ("OPAQUE", "shot-3"), ("item-I", "shot-1"), (primary, shot["shot_id"])])
    editing.assert_readback(accepted)
    assert editing.document(original["parent_revision"]["revision_id"]) == original
    history = editing.history()
    editing.service.close()
    editing.service = RuntimeService(editing.film.fixture.duplicate_root)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))

    def forbidden(*args, **kwargs):
        pytest.fail("exact retry executed provider semantics")

    before = rows(editing.service)
    with monkeypatch.context() as retry:
        retry.setattr(type(editing.service._timeline_commit_provider), "commit", forbidden)
        assert editing.commit(copy.deepcopy(body), "codec-move") == accepted
    assert rows(editing.service) == before
    assert editing.history() == history
    editing.assert_readback(accepted)
    undone = editing.commit(editing.body([inverse(accepted["receipt"]["receipt_id"])]), "codec-inverse")
    assert undone["data"]["canonical_document"] == original
    editing.assert_readback(undone)
    assert editing.service.store.integrity_report()["ok"]


@pytest.mark.parametrize("fields", [
    {}, {"item_id": ""}, {"id": ""}, {"item_id": True}, {"id": False},
    {"item_id": 1}, {"id": 1}, {"item_id": []}, {"id": {}},
    {"item_id": None, "id": "fallback"}, {"item_id": False, "id": "fallback"},
    {"item_id": "", "id": "fallback"},
])
@pytest.mark.parametrize("preview", [False, True])
def test_invalid_primary_or_fallback_refuses_before_writes(realm, monkeypatch, fields, preview):  # noqa: F811
    # Trusted acceptance-boundary negative, not an Agent/publication positive.
    from test_timeline_projection_ownership import refuses

    service, commits, project, _, _ = realm
    media = media_item(service, project, "unused")
    item = {**fields, "media_id": media["media_id"]}
    pair = with_media(proposal(service, commits, project, "main", "invalid-codec",
                               shots=[image("new-shot", "invalid-shot", items=[item])]), media)
    if preview:
        from runtime_protocol.timeline_commit_store import request_identity

        pair[0]["request"]["dry_run"] = True
        pair[0]["invocation"]["body"] = copy.deepcopy(pair[0]["request"])
        pair[0]["request_hash"] = request_identity(pair[0])
    refuses(service, commits, pair, monkeypatch, preview=preview)
