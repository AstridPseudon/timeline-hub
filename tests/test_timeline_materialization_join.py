"""Source joins over actual captured revisions, plus the held native requirements.

Prepared fixtures do not implement Agent capture/compiler semantics. Direct
checker cases prove Runtime checks independently of the frozen wire artifact.
"""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import RequestCommitPort
from runtime_protocol.timeline_commit_store import digest, request_identity
from runtime_protocol.timeline_materialization import materialization_join
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
        captures = {}
        if capture:
            revision = context["request"]["base_revision_id"]
            captures[revision] = port.revision_closure(revision)
        if boundary == "checker":
            def captured(revision):
                if revision not in captures:
                    raise ValidationError("uncaptured revision")
                return captures[revision]
            return materialization_join(value, context["request"]["project_id"], context["request"]["timeline_id"], captured)
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
                   reason="M2 native positive requires reviewed Agent and normally generated matching item-ref artifact")
@pytest.mark.parametrize("boundary", ["port", "store"])
def test_complete_captured_join_previews_original_map_without_writes(realm, boundary):
    pair = seal(joined(realm), preview=True)
    before = snapshot(realm[0])
    result = evaluate(realm, pair, boundary)
    assert result["data"]["id_map"] == pair[1]["id_map"]
    assert result["data"]["canonical_document"] == pair[1]["canonical_document"]
    assert result["receipt"] is None
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("boundary", ["port", "store", "checker"])
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


def test_checker_joins_actual_captured_source_without_schema_substitution(realm):
    pair = joined(realm)
    before = snapshot(realm[0])
    expected = pair[1]["records"]["commands"][0]["dependencies"][0]["pin"]
    assert evaluate(realm, pair, "checker") == {"destination": ("occ-0", expected)}
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("damage", [
    "duplicate-binding", "duplicate-dependency", "duplicate-record-conflict", "bool-provenance", "number-provenance",
    "empty-item", "slash-item", "alias-item", "missing-source-member", "extra-source-member", "missing-output-member",
    "extra-output-member", "output-internal-edge", "output-shot-digest", "output-internal-digest",
    "sealed-missing", "sealed-wrong", "sealed-extra", "record-extra", "unbound-owner", "nonfixed", "inexact",
    "wrong-dependency-key", "wrong-binding-dependency", "fake-shot-birth", "fake-item-birth", "extra-identity-map",
    "cross-owner-birth",
])
def test_checker_rejects_each_join_concern_without_early_schema_gate(realm, damage):
    pair = joined(realm)
    value = pair[1]
    record = value["records"]["commands"][0]
    dependency = record["dependencies"][0]
    source = dependency["pin"]["source"]
    output = value["canonical_document"]
    if damage == "duplicate-binding":
        record["bindings"].append(copy.deepcopy(record["bindings"][0]))
    elif damage == "duplicate-dependency":
        record["dependencies"].append(copy.deepcopy(dependency))
    elif damage in ("duplicate-record-conflict", "bool-provenance", "number-provenance"):
        other = copy.deepcopy(record)
        other_source = other["dependencies"][0]["pin"]["source"]
        other_source["revision_id"] = {"duplicate-record-conflict": "wrong", "bool-provenance": True,
                                       "number-provenance": 1}[damage]
        value["records"]["commands"].append(other)
    elif damage in ("empty-item", "slash-item", "alias-item"):
        source["item_id_map"]["source-item"] = {"empty-item": "", "slash-item": "a/b", "alias-item": "a::b"}[damage]
    elif damage == "missing-source-member":
        source["item_id_map"] = {}
    elif damage == "extra-source-member":
        source["item_id_map"]["other"] = "other-destination"
    elif damage == "missing-output-member":
        output["shot_revisions"][0]["payload"]["items"] = []
        output["shot_revisions"][0]["content_digest"] = digest(output["shot_revisions"][0]["payload"])
    elif damage == "extra-output-member":
        output["shot_revisions"][0]["payload"]["items"].append({"item_id": "extra"})
        output["shot_revisions"][0]["content_digest"] = digest(output["shot_revisions"][0]["payload"])
    elif damage == "output-internal-edge":
        output["shot_revisions"][0]["internal_timeline_revision_id"] = "wrong"
    elif damage in ("output-shot-digest", "output-internal-digest"):
        family = "shot_revisions" if damage == "output-shot-digest" else "internal_timeline_revisions"
        output[family][0]["content_digest"] = "sha256:" + "0" * 64
    elif damage == "sealed-missing":
        record["command"]["bindings"].pop("shot:destination")
    elif damage == "sealed-wrong":
        record["command"]["bindings"]["shot:destination"] = "shot:other"
    elif damage in ("sealed-extra", "record-extra"):
        key = "shot:destination/item:extra"
        if damage == "sealed-extra":
            record["command"]["bindings"][key] = "shot:source/item:source-item"
        else:
            record["bindings"].append(dict(record["bindings"][1], key=key))
    elif damage == "unbound-owner":
        record["bindings"].append(dict(record["bindings"][-1], key="materialization.owner:shot:unbound"))
    elif damage == "nonfixed":
        record["bindings"][0]["policy"] = "follow"
    elif damage == "inexact":
        dependency["policy"] = "latest"
    elif damage == "wrong-dependency-key":
        dependency["key"] += "-wrong"
    elif damage == "wrong-binding-dependency":
        record["bindings"][0]["dependencies"] = []
    elif damage in ("fake-shot-birth", "fake-item-birth"):
        kind = "shot" if damage == "fake-shot-birth" else "item"
        ref = "shot:destination" + ("/item:destination-item" if kind == "item" else "")
        record["created"] = [{"kind": kind, "ref": ref, "owner": None}]
        record["command"]["created"] = [ref]
    elif damage == "cross-owner-birth":
        record["created"] = [{"kind": "item", "ref": "shot:other/item:destination-item", "owner": "shot:other"}]
    else:
        value["id_map"]["extra"] = "extra"
    refresh(value)
    before = snapshot(realm[0])
    with pytest.raises(ValidationError, match="materialization"):
        evaluate(realm, pair, "checker")
    assert snapshot(realm[0]) == before


def test_matching_allocations_merge_across_records_but_duplicates_within_record_refuse(realm):
    pair = joined(realm)
    expected = evaluate(realm, pair, "checker")
    pair[1]["records"]["commands"].append(copy.deepcopy(pair[1]["records"]["commands"][0]))
    assert evaluate(realm, pair, "checker") == expected


def test_private_port_validates_complete_join_and_revalidates_captured_bytes(realm):
    service, commits, _, _, _ = realm
    context, value = joined(realm)
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.head()
        port.revision_closure(context["request"]["base_revision_id"])
        assert port.validate(value) == evaluate(realm, [context, value], "checker")
        service.store.conn.execute("UPDATE shot_revisions SET payload_json='{}' WHERE id='source-v1'")
        with pytest.raises(CommitRejected):
            port.validate(value)
    finally:
        port.close()


@pytest.mark.parametrize("capture_original", [True, False])
def test_original_pin_survives_disjoint_head_and_still_requires_original_capture(realm, capture_original):
    service, commits, project, _, _ = realm
    context, value = joined(realm)
    expected = copy.deepcopy(value["records"]["commands"][0]["dependencies"][0]["pin"])
    accept(commits, proposal(service, commits, project, "main", "disjoint-parent"))
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        value["expected_head"] = port.head()
        port.revision_closure(value["expected_head"]["revision_id"])
        if capture_original:
            port.revision_closure(context["request"]["base_revision_id"])
            assert port.validate(value) == {"destination": ("occ-0", expected)}
        else:
            with pytest.raises(CommitRejected) as error:
                port.validate(value)
            assert error.value.failure["details"]["reason"] == "dependency_unavailable"
    finally:
        port.close()


def accept_legacy_projection(commits, pair):
    """Use the real legacy boundary to obtain history, never invent accepted rows."""
    legacy = copy.deepcopy(pair)
    record = legacy[1]["records"]["commands"][0]
    legacy[1]["id_map"] = {}
    record["bindings"] = [{"key": "owner", "ref": "occurrence:occ-0", "policy": "fixed", "dependencies": []}]
    record["dependencies"] = []
    record["command"]["bindings"] = {"owner": "occurrence:occ-0"}
    seal(legacy)
    return accept(commits, legacy)


@pytest.mark.parametrize("damage", [None, "owner", "source", "parent", "items", "output-owner", "output-edge", "missing"])
def test_slot_comparison_uses_genuine_authenticated_m1_boundaries(realm, damage):
    _, commits, project, _, _ = realm
    pair = joined(realm)
    allocation = evaluate(realm, pair, "checker")["destination"]
    result = accept_legacy_projection(commits, pair)
    entry = commits.history_entry(project, "main", result["receipt"]["receipt_id"])
    before = commits.revision_closure(project, "main", entry["previous"]["revision_id"])
    after = commits.revision_closure(project, "main", entry["revision_id"])
    if damage == "owner":
        allocation = ("occ-1", allocation[1])
    elif damage in ("source", "parent"):
        allocation[1]["source" if damage == "source" else "parent"]["revision_id"] = "wrong"
    elif damage == "items":
        allocation[1]["source"]["item_id_map"]["source-item"] = "other-item"
    elif damage in ("output-owner", "output-edge"):
        after["parent_revision"]["payload"]["occurrences"][0][
            "occurrence_id" if damage == "output-owner" else "shot_id"] = "other"
    elif damage == "missing":
        allocation = None
    assert commits._same_materialization_slot("destination", "occ-0", allocation, None, before, after) is (damage is None)


def test_inverse_output_can_return_to_source_but_map_cannot_invent_inverse_authority(realm):
    service, commits, project, _, _ = realm
    pair = joined(realm)
    allocation = evaluate(realm, pair, "checker")
    original = commits.revision_closure(project, "main", pair[0]["request"]["base_revision_id"])
    accepted = accept_legacy_projection(commits, pair)
    value = pair[1]
    value["expected_head"] = commits.head(project, "main")
    value["canonical_document"] = original
    record = value["records"]["commands"][0]
    record["command"]["op"] = "timeline.inverse"
    record["command"]["args"] = {"publications": [accepted["receipt"]["receipt_id"]]}
    record["reads"][0]["state"]["value"] = "destination"
    value["records"]["undo_of"] = [accepted["receipt"]["receipt_id"]]
    refresh(value)
    captures = {revision: commits.revision_closure(project, "main", revision) for revision in
                (original["parent_revision"]["revision_id"], value["expected_head"]["revision_id"])}
    before = snapshot(service)
    assert materialization_join(value, project, "main", captures.__getitem__) == allocation
    # That real M1 target has no typed allocation facts. A caller cannot claim
    # them retroactively and turn this direct checker success into undo authority.
    with pytest.raises(CommitRejected, match="authenticated provenance"):
        commits._check_inherited_allocations(project, "main", value["records"], allocation)
    assert snapshot(service) == before


@pytest.mark.parametrize("mapping", [{"shot:destination": "destination"}, {"source": "destination"}, {"a": True}, None])
def test_durable_lookup_rejects_new_result_maps_not_authenticated_by_records(realm, mapping):
    from runtime_protocol.errors import ProtocolError

    service, commits, project, _, _ = realm
    pair = proposal(service, commits, project, "main", "genuine-acceptance")
    accepted = accept(commits, pair)
    row = service.store.conn.execute("SELECT result_json FROM command_idempotency WHERE txn_id=?",
                                     (accepted["receipt"]["receipt_id"],)).fetchone()
    data = json.loads(row[0])
    data["id_map"] = mapping
    service.store.conn.execute("UPDATE command_idempotency SET result_json=? WHERE txn_id=?",
                               (json.dumps(data), accepted["receipt"]["receipt_id"]))
    before = snapshot(service)
    with pytest.raises(ProtocolError, match="corrupt"):
        commits.lookup(pair[0], authorize=lambda: None)
    assert snapshot(service) == before


@pytest.mark.parametrize("change", ["birth", "delete"])
@pytest.mark.parametrize("damage", [None, "unrecorded", "wrong-identity", "missing-created", "missing-absence"])
def test_item_membership_joins_typed_authored_roots_separately_from_allocations(realm, change, damage):
    pair = joined(realm)
    value = pair[1]
    record = value["records"]["commands"][0]
    shot = value["canonical_document"]["shot_revisions"][0]
    if change == "birth":
        row = dict(shot["payload"]["items"][0], item_id="authored-new-item")
        shot["payload"]["items"].append(row)
        before, after = {"state": "absent"}, {"state": "present", "value": row}
        created = {"kind": "item", "ref": "shot:destination/item:authored-new-item", "owner": "shot:destination"}
        record["created"] = [created]
        record["command"]["created"] = [created["ref"]]
    else:
        row = shot["payload"]["items"].pop()
        before, after = {"state": "present", "value": row}, {"state": "absent"}
    ref = "shot:destination/item:" + row["item_id"]
    record["writes"] = [{"ref": ref, "path": [], "before": copy.deepcopy(before), "after": copy.deepcopy(after)}]
    record["reads"].append({"ref": ref, "path": [], "state": copy.deepcopy(before)})
    if damage == "unrecorded":
        record["writes"] = []
    elif damage == "wrong-identity":
        record["writes"][0]["after" if change == "birth" else "before"]["value"]["item_id"] = "forged"
    elif damage == "missing-created":
        if change == "birth":
            record["created"] = []
        else:
            record["writes"][0]["before"] = {"state": "absent"}
    elif damage == "missing-absence":
        if change == "birth":
            record["reads"].pop()
        else:
            record["writes"] = []
    shot["content_digest"] = digest(shot["payload"])
    refresh(value)
    before_sql = snapshot(realm[0])
    if damage is None:
        assert evaluate(realm, pair, "checker")["destination"][0] == "occ-0"
        assert value["id_map"] == {"shot:destination": "destination", "shot:destination/item:destination-item": "destination-item"}
    else:
        with pytest.raises(ValidationError, match="materialization"):
            evaluate(realm, pair, "checker")
    assert snapshot(realm[0]) == before_sql


@pytest.mark.parametrize("damage", ["missing", "changed"])
def test_private_port_joins_record_bindings_to_the_sealed_request(realm, damage):
    service, commits, _, _, _ = realm
    context, value = joined(realm)
    if damage == "missing":
        context["request"]["commands"][0]["bindings"].pop("shot:destination")
    else:
        context["request"]["commands"][0]["bindings"]["shot:destination"] = "shot:forged-source"
    context["invocation"]["body"] = copy.deepcopy(context["request"])
    context["request_hash"] = request_identity(context)
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.head()
        port.revision_closure(context["request"]["base_revision_id"])
        before = snapshot(service)
        with pytest.raises(ValidationError, match="sealed request"):
            port.validate(value)
        assert snapshot(service) == before
    finally:
        port.close()
