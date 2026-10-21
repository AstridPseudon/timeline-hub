"""SOURCE-ONLY semantic spike for the missing film transcript carrier.

This deliberately does not register an EditCommand or alter the current
closed union.  It makes the proposed read/write boundary executable while the
paired Agent/Runtime carrier is reviewed.  The source document is the exact
verified input; no parser, normalization, whole-parent replacement, or
catalog mutation is part of this spike.
"""
from __future__ import annotations

import copy

import pytest

from astrid.core.timeline.authoring_bundle import _digest


SCHEMA_REF = "astrid.transcript_segment/v1"
ASSET_ID = "asset-a"
MEDIA_ID = "sha256:" + "a" * 64
DOCUMENT_ID = "transcript:" + "b" * 64
SOURCE_ID = "source-1"
OLD_DOCUMENT_ID = "transcript:" + "c" * 64
PIN = {
    "document_id": DOCUMENT_ID,
    "version": 2,
    "content_digest": "",
}
CONTENT = {
    "schema": "media.transcript/v1",
    "media_id": MEDIA_ID,
    "source_id": SOURCE_ID,
    "segments": [
        {
            "id": "seg-a",
            "start": 0,
            "end": 1,
            "text": "Hello world",
            "words": [
                {"id": "word-a-1", "start": 0, "end": 0.4, "text": "Hello"},
                {"id": "word-a-2", "start": 0.4, "end": 1, "text": "world"},
            ],
        },
        {
            "id": "seg-b",
            "start": 1,
            "end": 2,
            "text": "Again",
            "speaker": "narrator",
            "words": [{"id": "word-b-1", "start": 1, "end": 2, "text": "Again"}],
        },
    ],
}
PIN["content_digest"] = _digest(CONTENT)
OLD_CONTENT = {
    "schema": "media.transcript/v1",
    "media_id": MEDIA_ID,
    "source_id": "old-source",
    "segments": [{
        "id": "seg-a",
        "start": 0,
        "end": 1,
        "text": "Old",
        "words": [{"id": "word-old", "start": 0, "end": 1, "text": "Old"}],
    }],
}
OLD_PIN = {"document_id": OLD_DOCUMENT_ID, "version": 1, "content_digest": _digest(OLD_CONTENT)}


class AssociationRefusal(ValueError):
    """A named refusal from the test-only closed semantic boundary."""


def _item(segment, *, asset_id=ASSET_ID, source_id=SOURCE_ID, adapter="astrid.projectTranscript",
          document_id=DOCUMENT_ID, document_version=2):
    return {
        "id": segment["id"],
        "shape": "interval",
        "domain": "source_seconds",
        "extent": {"start": segment["start"], "end": segment["end"]},
        "schemaRef": SCHEMA_REF,
        "payload": {
            "sourceId": source_id,
            "segmentId": segment["id"],
            "text": segment["text"],
            **({"speaker": segment["speaker"]} if "speaker" in segment else {}),
            "words": copy.deepcopy(segment["words"]),
            "documentId": document_id,
            "documentVersion": document_version,
            "opaque": {"future": [None, False, {"literal": segment["id"]}]},
        },
        "sourceArtifactRef": {"assetId": asset_id},
        "provenance": {"adapterId": adapter, "adapterVersion": "1"},
    }


def _document(content=CONTENT, pin=PIN):
    return {"pin": copy.deepcopy(pin), "content": copy.deepcopy(content)}


def _base():
    old_segment = {"id": "seg-old", "start": 0, "end": 1, "text": "Old", "words": [
        {"id": "word-old", "start": 0, "end": 1, "text": "Old"},
    ]}
    retained = _item(old_segment, asset_id=ASSET_ID, source_id="other-source", adapter="other.adapter")
    old_a = _item(old_segment, source_id="old-source", document_id=OLD_DOCUMENT_ID, document_version=1)
    old_a["id"] = "seg-a"
    old_a["payload"]["segmentId"] = "seg-a"
    old_a["payload"]["opaque"]["keep"] = "old-a"
    old_b = _item({"id": "seg-b", "start": 1, "end": 2, "text": "Old again", "words": [
        {"id": "word-b-1", "start": 1, "end": 2, "text": "again"},
    ]}, source_id="old-source", document_id=OLD_DOCUMENT_ID, document_version=1)
    return {
        "assets": {ASSET_ID: {"media_id": MEDIA_ID, "opaque": {"keep": "asset"}}},
        "transcriptReferences": {
            "schema": "media.transcript.references/v1",
            "associations": [
                {"assetId": "other-asset", "documentId": "transcript:" + "c" * 64},
                {"assetId": ASSET_ID, "documentId": OLD_DOCUMENT_ID},
            ],
        },
        "sourceItemsBySchemaRef": {SCHEMA_REF: [retained, old_a, old_b]},
        "config": {
            "clips": [{
                "id": "caption-a",
                "track": "transcript-caption-foundry-track",
                "asset": ASSET_ID,
                "app": {"__generated__": {
                    "extensionId": "haus.astrid.transcript-lane",
                    "contributionId": "transcript-caption-foundry",
                    "provenance": {
                        "sourceSchemaRef": SCHEMA_REF,
                        "contractVersion": "1",
                        "sourceItemId": "seg-a",
                        "opaque": {"caption": "keep"},
                    },
                }},
            }],
            "app": {"haus.astrid.transcript-lane": {
                "transcript-source-review:seg-a": {
                    "schemaVersion": 1,
                    "sourceSchemaRef": SCHEMA_REF,
                    "sourceItemId": "seg-a",
                    "opaque": {"review": "keep"},
                },
            }},
        },
        "opaque_root": {"keep": [None, False]},
        "prior_document_pin": copy.deepcopy(OLD_PIN),
    }


def _validate_source(document, state, asset_id):
    pin = document.get("pin")
    content = document.get("content")
    if set(pin or {}) != {"document_id", "version", "content_digest"}:
        raise AssociationRefusal("exact DocumentPin required")
    if pin["version"] < 1 or _digest(content) != pin["content_digest"]:
        raise AssociationRefusal("corrupt or mismatched source pin")
    if state["assets"].get(asset_id, {}).get("media_id") != content.get("media_id"):
        raise AssociationRefusal("selected transcript belongs to different source media")
    segments = content.get("segments")
    if not isinstance(segments, list) or len({row.get("id") for row in segments}) != len(segments):
        raise AssociationRefusal("ambiguous transcript segment identity")
    for segment in segments:
        words = segment.get("words", [])
        if len({word.get("id") for word in words}) != len(words):
            raise AssociationRefusal("ambiguous transcript word identity")
        if any(word["start"] < segment["start"] or word["end"] > segment["end"]
               for word in words):
            raise AssociationRefusal("word falls outside its segment")


def capture_association(state, document, asset_id=ASSET_ID, previous_document=None):
    """Capture the proposed command/readback without mutating ``state``."""
    _validate_source(document, state, asset_id)
    content, pin = document["content"], document["pin"]
    source_id = content["source_id"]
    previous_association = next((row for row in state["transcriptReferences"]["associations"]
                                 if row["assetId"] == asset_id), None)
    if previous_association is not None:
        if (previous_document is None
                or previous_document["pin"]["document_id"] != previous_association["documentId"]):
            raise AssociationRefusal("exact prior DocumentPin is required for replacement")
        _validate_source(previous_document, state, asset_id)
    old_items = state["sourceItemsBySchemaRef"][SCHEMA_REF]
    keys = [(row["sourceArtifactRef"]["assetId"], row["payload"].get("sourceId"), row["id"])
            for row in old_items]
    if len(keys) != len(set(keys)):
        raise AssociationRefusal("ambiguous existing source-item identity")
    projected = [_item(segment, asset_id=asset_id, source_id=source_id) for segment in content["segments"]]
    retained = [row for row in old_items if not (
        row["sourceArtifactRef"]["assetId"] == asset_id
        and (row["provenance"]["adapterId"] == "astrid.projectTranscript"
             or row["payload"].get("sourceId") == source_id)
    )]
    associations = [row for row in state["transcriptReferences"]["associations"]
                    if row["assetId"] != asset_id]
    associations.append({"assetId": asset_id, "documentId": pin["document_id"]})
    after = copy.deepcopy(state)
    after["transcriptReferences"]["associations"] = associations
    after["sourceItemsBySchemaRef"][SCHEMA_REF] = retained + projected
    return {
        "command": {
            "schema_version": 1,
            "op": "transcript.associate",  # proposal only; not a registered Main op
            "version": "1",
            "select": f"parent/asset:{asset_id}",
            "args": {
                "asset_id": asset_id,
                "media_id": content["media_id"],
                "source_id": source_id,
                "document": copy.deepcopy(pin),
                "previous_document": (copy.deepcopy(previous_document["pin"])
                                       if previous_document is not None else None),
                "source_schema_ref": SCHEMA_REF,
            },
        },
        "dependency": {
            "kind": "transcript",
            "pin": copy.deepcopy(pin),
            "content": copy.deepcopy(content),
            "previous": (copy.deepcopy(previous_document)
                          if previous_document is not None else None),
        },
        "owner": {"asset_id": asset_id, "media_id": content["media_id"], "source_id": source_id},
        "source_items": [
            {"asset_id": asset_id, "schema_ref": SCHEMA_REF, "segment_id": segment["id"],
             "word_ids": [word["id"] for word in segment.get("words", [])]}
            for segment in content["segments"]
        ],
        "selection": {
            "owner": "parent",
            "key": "source-items:" + SCHEMA_REF,
            "members": [
                (row["sourceArtifactRef"]["assetId"], row["payload"].get("sourceId"), row["id"])
                for row in old_items
            ],
        },
        "caption_provenance": {
            "clips": copy.deepcopy(after["config"]["clips"]),
            "reviews": copy.deepcopy(after["config"]["app"]),
        },
        "before": copy.deepcopy(state),
        "after": after,
    }


def inverse(plan, head, intervening=()):
    if "source-items" in intervening or "transcriptReferences" in intervening:
        raise AssociationRefusal("accepted inverse refuses intervening or ABA source writes")
    if (head["transcriptReferences"] != plan["after"]["transcriptReferences"]
            or head["sourceItemsBySchemaRef"][SCHEMA_REF] != plan["after"]["sourceItemsBySchemaRef"][SCHEMA_REF]):
        raise AssociationRefusal("accepted inverse guard changed")
    restored = copy.deepcopy(head)
    restored["transcriptReferences"] = copy.deepcopy(plan["before"]["transcriptReferences"])
    restored["sourceItemsBySchemaRef"][SCHEMA_REF] = copy.deepcopy(
        plan["before"]["sourceItemsBySchemaRef"][SCHEMA_REF])
    return restored


def replay(plan, head):
    candidate = capture_association(
        head,
        {"pin": plan["dependency"]["pin"], "content": plan["dependency"]["content"]},
        previous_document=plan["dependency"]["previous"],
    )
    assert candidate["command"] == plan["command"]
    return candidate


def test_source_only_association_captures_exact_pin_owner_membership_and_opaque_readback():
    before = _base()
    plan = capture_association(before, _document(), previous_document=_document(OLD_CONTENT, OLD_PIN))
    assert before == _base()
    assert plan["command"]["args"]["document"] == PIN
    assert plan["command"]["args"]["previous_document"] == OLD_PIN
    assert plan["owner"] == {"asset_id": ASSET_ID, "media_id": MEDIA_ID, "source_id": SOURCE_ID}
    assert plan["source_items"] == [
        {"asset_id": ASSET_ID, "schema_ref": SCHEMA_REF, "segment_id": "seg-a",
         "word_ids": ["word-a-1", "word-a-2"]},
        {"asset_id": ASSET_ID, "schema_ref": SCHEMA_REF, "segment_id": "seg-b",
         "word_ids": ["word-b-1"]},
    ]
    after_items = plan["after"]["sourceItemsBySchemaRef"][SCHEMA_REF]
    assert [row["id"] for row in after_items] == ["seg-old", "seg-a", "seg-b"]
    assert after_items[0]["payload"]["opaque"] == {"future": [None, False, {"literal": "seg-old"}]}
    assert plan["after"]["config"] == before["config"]
    assert plan["caption_provenance"]["clips"] == before["config"]["clips"]
    assert plan["caption_provenance"]["reviews"] == before["config"]["app"]
    assert plan["after"]["opaque_root"] == before["opaque_root"]


def test_source_only_inverse_rebase_retry_and_restart_pin_retention():
    before = _base()
    plan = capture_association(before, _document(), previous_document=_document(OLD_CONTENT, OLD_PIN))
    independent = copy.deepcopy(plan["after"])
    independent["opaque_root"]["later"] = True
    restored = inverse(plan, independent)
    assert restored["opaque_root"] == {"keep": [None, False], "later": True}
    redo = replay(plan, restored)
    assert redo["after"] == plan["after"] | {"opaque_root": {"keep": [None, False], "later": True}}
    rebased = replay(plan, before | {"opaque_root": {"other": "author"}})
    assert rebased["after"]["opaque_root"] == {"other": "author"}
    assert rebased["dependency"]["pin"] == PIN
    assert rebased["dependency"]["previous"]["pin"] == OLD_PIN
    assert replay(plan, before)["command"] == plan["command"]
    restarted = copy.deepcopy(plan["after"])
    restarted["live_document_cache"] = None
    assert plan["dependency"]["pin"] == PIN
    assert plan["dependency"]["previous"]["pin"] == OLD_PIN
    assert restarted["sourceItemsBySchemaRef"] == plan["after"]["sourceItemsBySchemaRef"]
    with pytest.raises(AssociationRefusal, match="ABA"):
        inverse(plan, plan["after"], intervening=("source-items",))


@pytest.mark.parametrize("damage", ["digest", "media", "segments", "words", "duplicate-old"])
def test_source_only_boundary_refuses_corrupt_ambiguous_or_mismatched_input(damage):
    before = _base()
    document = _document()
    if damage == "digest":
        document["pin"]["content_digest"] = "sha256:" + "f" * 64
    elif damage == "media":
        document["content"]["media_id"] = "sha256:" + "e" * 64
        document["pin"]["content_digest"] = _digest(document["content"])
    elif damage == "segments":
        document["content"]["segments"].append(copy.deepcopy(document["content"]["segments"][0]))
        document["pin"]["content_digest"] = _digest(document["content"])
    elif damage == "words":
        document["content"]["segments"][0]["words"].append(
            copy.deepcopy(document["content"]["segments"][0]["words"][0]))
        document["pin"]["content_digest"] = _digest(document["content"])
    else:
        before["sourceItemsBySchemaRef"][SCHEMA_REF].append(
            copy.deepcopy(before["sourceItemsBySchemaRef"][SCHEMA_REF][1]))
    original = copy.deepcopy(before)
    with pytest.raises(AssociationRefusal):
        capture_association(before, document, previous_document=_document(OLD_CONTENT, OLD_PIN))
    assert before == original


def test_source_only_replacement_refuses_without_exact_prior_pin():
    before = _base()
    with pytest.raises(AssociationRefusal, match="prior DocumentPin"):
        capture_association(before, _document())
    assert before == _base()
