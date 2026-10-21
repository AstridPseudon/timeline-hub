"""timeline.reference v1: raw, unplaced parent source references."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.doc import _strip_derived
from astrid.sdk.timeline.native_parent_reference_commands import capture_timeline_reference
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_recipe_occurrence_create import empty_bundle

MEDIA = {
    "media_id": "sha256:" + "a" * 64,
    "content_digest": "sha256:" + "a" * 64,
}
VERIFIED = [{
    "raw_pin": MEDIA,
    "media_info": {
        "object_id": MEDIA["media_id"],
        "media_type": "application/octet-stream",
        "size": 1,
    },
}]


def command(bundle, reference_id, media=MEDIA):
    return capture_timeline_reference(bundle, reference_id, media, verified_media=VERIFIED)


def plain(captured):
    return {
        key: copy.deepcopy(captured[key])
        for key in ("schema_version", "op", "version", "select", "args", "intent")
    }


def test_empty_parent_raw_reference_is_unplaced_and_round_trips_exactly():
    original = empty_bundle()
    before = copy.deepcopy(original)
    captured = command(original, "exact-reference")

    validate_command(captured)
    plan = execute(original, [captured], verified_media=VERIFIED)
    assert original == before
    assert captured["args"] == {
        "reference_id": "exact-reference",
        "role": "source",
        "media": MEDIA,
    }
    assert plan.records[0]["created"] == [
        {"ref": "parent/asset:exact-reference", "kind": "asset", "owner": "parent"},
    ]
    assert plan.records[0]["dependencies"] == [{
        "key": "reference.media",
        "kind": "media",
        "pin": MEDIA,
        "policy": "exact",
    }]

    parent = plan.bundle["parent"]
    reference = parent["config"]["app"]["astrid"]["timeline_references"]
    assert list(reference) == ["exact-reference"]
    assert reference["exact-reference"] == {
        "version": 1,
        "reference_id": "exact-reference",
        "role": "source",
        "media": MEDIA,
    }
    assert State(plan.bundle).entity("parent/asset:exact-reference") == MEDIA
    assert plan.bundle["placements"] == []
    assert plan.bundle["shots"] == {}
    assert State(plan.bundle).collection("parent", "clip") == []

    document = document_from_bundle(plan.bundle)
    assert document["dependency_manifest"]["media"] == [MEDIA]
    reloaded = bundle_from_document(copy.deepcopy(document))
    assert document_from_bundle(reloaded) == document
    assert _strip_derived(document) == document


def test_raw_reference_replays_in_order_and_inverse_redo_preserves_order():
    original = empty_bundle()
    first = command(original, "first")
    second = command(execute(original, [first], verified_media=VERIFIED).bundle, "second")
    plan = execute(original, [first, second], verified_media=VERIFIED)

    references = plan.bundle["parent"]["config"]["app"]["astrid"]["timeline_references"]
    assets = State(plan.bundle).registry("parent")["assets"]
    assert list(references) == ["first", "second"]
    assert list(assets) == ["first", "second"]
    assert replay(plan, original, verified_media=VERIFIED).records == plan.records

    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    redone = inverse(undone.bundle, undone.records)
    assert redone.bundle == plan.bundle


@pytest.mark.parametrize(
    "verified_media, message",
    [
        ([], "exact Runtime-verified raw media"),
        ([{"raw_pin": MEDIA, "media_info": None}], "verified raw media metadata"),
        ([{"raw_pin": MEDIA, "media_info": {
            "object_id": "sha256:" + "b" * 64,
            "media_type": "application/octet-stream",
            "size": 1,
        }}], "verified raw media metadata"),
    ],
)
def test_raw_reference_requires_exact_verified_owned_media(verified_media, message):
    original = empty_bundle()
    captured = command(original, "refused-reference")
    before = copy.deepcopy(original)
    with pytest.raises(CommandError, match=message):
        execute(original, [plain(captured)], verified_media=verified_media)
    assert original == before


def test_raw_reference_does_not_overwrite_an_occupied_stable_identity():
    original = empty_bundle()
    first = execute(original, [command(original, "occupied")], verified_media=VERIFIED)
    replacement_media = {
        "media_id": "sha256:" + "b" * 64,
        "content_digest": "sha256:" + "b" * 64,
    }
    replacement_verified = [{
        "raw_pin": replacement_media,
        "media_info": {
            "object_id": replacement_media["media_id"],
            "media_type": "application/octet-stream",
            "size": 2,
        },
    }]
    replacement = plain(command(original, "occupied"))
    replacement["args"]["media"] = replacement_media
    before = copy.deepcopy(first.bundle)
    with pytest.raises(CommandError, match="identity is already occupied"):
        execute(first.bundle, [replacement], verified_media=replacement_verified)
    assert first.bundle == before


def test_raw_reference_does_not_alias_an_ordinary_asset_with_the_same_user_id():
    original = empty_bundle()
    original["parent"]["registry"] = {"assets": {
        "same-id": {"media_id": MEDIA["media_id"], "type": "image"},
    }}
    before = copy.deepcopy(original)
    captured = command(empty_bundle(), "same-id")

    with pytest.raises(CommandError, match="identity is already occupied"):
        execute(original, [plain(captured)], verified_media=VERIFIED)
    assert original == before
