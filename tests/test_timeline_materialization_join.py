"""Staged source-bound allocation requirements at the prepared-provider boundary.

These fixtures do not implement Agent capture/compiler semantics. The normal
artifact and both identity-only gates remain in force pending the paired release;
negative cases currently establish only fail-closed behavior, not join validation.
"""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import RequestCommitPort
from runtime_protocol.timeline_commit_store import request_identity
from test_timeline_commit_acceptance import realm  # noqa: F401
from test_timeline_projection_occupancy import (
    accept, image, media_item, proposal, refresh, snapshot, with_media,
)


def seal(pair, *, preview=False):
    context, value = pair
    context["request"]["commands"] = [copy.deepcopy(r["command"]) for r in value["records"]["commands"]]
    if preview:
        context["request"]["dry_run"] = True
    context["invocation"]["body"] = copy.deepcopy(context["request"])
    context["request_hash"] = request_identity(context)
    refresh(value)
    return pair


def joined(realm):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "source-item")
    source = image("source", "source-v1", items=[item])
    seed = with_media(proposal(service, commits, project, "main", "shared-source", shots=[source]), item)
    occurrences = seed[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"]
    occurrences.append(dict(occurrences[0], occurrence_id="occ-1", placement={"start_ms": 1000}))
    refresh(seed[1])
    accepted = accept(commits, seed)
    original = accepted["data"]["canonical_document"]
    destination = image("destination", "destination-v1", items=[dict(item, item_id="destination-item")])
    pair = with_media(proposal(service, commits, project, "main", "materialize", shots=[destination, source]), item)
    value = pair[1]
    shot, key = "shot:destination", "materialization.source:shot:destination"
    value["id_map"] = {shot: "destination", shot + "/item:destination-item": "destination-item"}
    record = value["records"]["commands"][0]
    record["bindings"] = [
        {"key": shot, "ref": "shot:source", "policy": "fixed", "dependencies": [key]},
        {"key": shot + "/item:destination-item", "ref": "shot:source/item:source-item",
         "policy": "fixed", "dependencies": [key]},
        {"key": "materialization.owner:" + shot, "ref": "occurrence:occ-0",
         "policy": "fixed", "dependencies": [key]},
    ]
    record["command"]["bindings"] = {b["key"]: b["ref"] for b in record["bindings"]}
    record["reads"] = [{"ref": "occurrence:occ-0/shot", "path": ["shot_id"],
                        "state": {"state": "present", "value": "source"}}]
    record["dependencies"] = [{"key": key, "kind": "entity", "policy": "exact", "pin": {
        "parent": {k: original["parent_revision"][k] for k in ("revision_id", "content_digest")},
        "source": {"shot_id": source[0]["shot_id"], "revision_id": source[0]["revision_id"],
                   "content_digest": source[0]["content_digest"],
                   "internal_timeline_id": source[1]["timeline_id"],
                   "internal_timeline_revision_id": source[1]["revision_id"],
                   "internal_timeline_content_digest": source[1]["content_digest"],
                   "item_id_map": {"source-item": "destination-item"}},
    }}]
    # JSON recovery retains the original source and allocation; no physical birth.
    assert record["created"] == []
    return json.loads(json.dumps(seal(pair)))


def evaluate(realm, pair, boundary, *, capture=True):
    service, commits, _, _, _ = realm
    context, value = pair
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.head()
        if capture:
            port.revision_closure(context["request"]["base_revision_id"])
        if boundary == "port":
            return port.preview(value)
        return commits.preview(context, value, authorize=lambda: None, inputs=port)
    finally:
        port.close()


@pytest.mark.parametrize("boundary", ["port", "store"])
@pytest.mark.parametrize("mapping", [{}, {"legacy": "legacy"}])
def test_legacy_identity_maps_still_preview_without_writes(realm, boundary, mapping):
    service, commits, project, _, _ = realm
    pair = proposal(service, commits, project, "main", "legacy-map")
    pair[1]["id_map"] = mapping
    seal(pair, preview=True)
    before = snapshot(service)
    result = evaluate(realm, pair, boundary)
    assert result["data"]["id_map"] == mapping
    assert result["receipt"] is None
    assert snapshot(service) == before


# M2 source-bound materialization requires the exact manager-ACKed paired
# Agent capture/parser/compiler + normally generated Runtime item-ref artifact.
@pytest.mark.xfail(strict=True, raises=(ValidationError, CommitRejected),
                   reason="M2 joined allocation requires paired capture/item refs and Runtime join validation")
@pytest.mark.parametrize("boundary", ["port", "store"])
def test_complete_captured_join_previews_original_map_without_writes(realm, boundary):
    pair = seal(joined(realm), preview=True)
    before = snapshot(realm[0])
    result = evaluate(realm, pair, boundary)
    assert result["data"]["id_map"] == pair[1]["id_map"]
    assert result["data"]["canonical_document"] == pair[1]["canonical_document"]
    assert result["receipt"] is None
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("boundary", ["port", "store"])
@pytest.mark.parametrize("damage", [
    "missing-pair", "extra-pair", "forged-id", "raw-source-map", "missing-binding",
    "conflicting-binding", "wrong-owner", "wrong-source-item", "wrong-source-shot",
    "wrong-shot-pin", "wrong-internal-pin", "wrong-parent-pin", "nonbijective-items",
    "wrong-scope", "wrong-edge", "missing-read", "uncaptured-source",
])
def test_unverified_join_refuses_atomically(realm, monkeypatch, boundary, damage):
    pair = joined(realm)
    value = pair[1]
    record = value["records"]["commands"][0]
    source = record["dependencies"][0]["pin"]["source"]
    if damage == "missing-pair":
        value["id_map"].pop("shot:destination/item:destination-item")
    elif damage == "extra-pair":
        value["id_map"]["shot:unbound"] = "unbound"
    elif damage == "forged-id":
        value["id_map"]["shot:destination"] = "unrelated"
    elif damage == "raw-source-map":
        value["id_map"] = {"source": "destination", "source-item": "destination-item"}
    elif damage == "missing-binding":
        record["bindings"].pop(1)
    elif damage == "conflicting-binding":
        record["bindings"].append(dict(record["bindings"][0], ref="shot:other"))
    elif damage == "wrong-owner":
        record["bindings"][-1]["ref"] = "occurrence:occ-1"
    elif damage == "wrong-source-item":
        record["bindings"][1]["ref"] = "shot:source/item:other-item"
    elif damage == "wrong-source-shot":
        source["shot_id"] = "other-source"
    elif damage == "wrong-shot-pin":
        source["content_digest"] = "sha256:" + "0" * 64
    elif damage == "wrong-internal-pin":
        source["internal_timeline_content_digest"] = "sha256:" + "0" * 64
    elif damage == "wrong-parent-pin":
        record["dependencies"][0]["pin"]["parent"]["content_digest"] = "sha256:" + "0" * 64
    elif damage == "nonbijective-items":
        source["item_id_map"]["other-item"] = "destination-item"
    elif damage == "wrong-scope":
        value["canonical_document"]["timeline_id"] = "other-timeline"
    elif damage == "wrong-edge":
        value["canonical_document"]["parent_revision"]["payload"]["occurrences"][0]["occurrence_id"] = "other-owner"
    elif damage == "missing-read":
        record["reads"] = []
    seal(pair, preview=True)
    before = snapshot(realm[0])
    monkeypatch.setattr(realm[1], "_persist_closure", lambda *_: pytest.fail("unverified allocation wrote a closure"))
    with pytest.raises((ValidationError, CommitRejected)):
        evaluate(realm, pair, boundary, capture=damage != "uncaptured-source")
    assert snapshot(realm[0]) == before
