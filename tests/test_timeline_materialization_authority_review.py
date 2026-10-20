"""Independent authority probes using real accepted sources and private captures.

Direct join checks bypass no validator: the normal item-ref artifact is still
pending, so these are internal boundary proofs rather than native admission.
"""
from __future__ import annotations

import copy
import json

import pytest
from test_timeline_commit_acceptance import (
    realm as realm,  # noqa: PLC0414 (pytest fixture re-export)
)
from test_timeline_materialization_join import (
    accept_legacy_projection,
    evaluate,
    joined,
    seal,
)
from test_timeline_projection_occupancy import accept, proposal, refresh, snapshot

from runtime_protocol.errors import AuthorizationError, ProtocolError, ValidationError
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import RequestCommitPort
from runtime_protocol.timeline_commit_store import digest


@pytest.fixture
def captured_join(realm):
    service, commits, _, _, _ = realm
    context, value = joined(realm)
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.head()
        port.revision_closure(context["request"]["base_revision_id"])
        yield context, value, port
    finally:
        port.close()


def test_public_inputs_cannot_delegate_private_capture_authority(realm, captured_join):
    context, value, port = captured_join
    commits = realm[1]
    assert port.validate(value)["destination"][0] == "occ-0"

    class Inputs:
        # A genuine validator/capture behind this facade still confers no
        # authority on a public custom Inputs object.
        validate = port.validate
        _provider_context = port._provider_context

    before = snapshot(realm[0])
    for inputs in (None, Inputs()):
        with pytest.raises(CommitRejected) as error:
            commits._materializations(context, value, inputs)
        assert error.value.failure["details"]["reason"] == "dependency_unavailable"
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("change", ["publisher", "idempotency_key", "request_hash"])
def test_real_private_port_is_bound_to_exact_context(realm, captured_join, change):
    context, value, port = captured_join
    other = copy.deepcopy(context)
    other[change] += "-other"
    before = snapshot(realm[0])
    with pytest.raises(CommitRejected) as error:
        realm[1]._materializations(other, value, port)
    assert error.value.failure["details"]["reason"] == "dependency_unavailable"
    assert snapshot(realm[0]) == before


def test_closed_private_port_cannot_supply_allocation_authority(realm, captured_join):
    context, value, port = captured_join
    assert realm[1]._materializations(context, value, port)["destination"][0] == "occ-0"
    port.close()
    before = snapshot(realm[0])
    with pytest.raises(AuthorizationError, match="closed"):
        realm[1]._materializations(context, value, port)
    assert snapshot(realm[0]) == before


def test_private_capture_is_reauthorized_at_allocation_validation(realm):
    service, commits, _, _, _ = realm
    context, value = joined(realm)
    allowed = True

    def authorize():
        if not allowed:
            raise AuthorizationError("authority revoked")

    port = RequestCommitPort(service, commits, context, authorize)
    try:
        port.head()
        port.revision_closure(context["request"]["base_revision_id"])
        assert commits._materializations(context, value, port)["destination"][0] == "occ-0"
        allowed = False
        before = snapshot(service)
        with pytest.raises(AuthorizationError, match="revoked"):
            commits._materializations(context, value, port)
        assert snapshot(service) == before
    finally:
        port.close()


def test_caller_mutation_of_returned_capture_cannot_repin_private_source(realm, captured_join):
    context, value, port = captured_join
    returned = port.revision_closure(context["request"]["base_revision_id"])
    returned["parent_revision"]["payload"]["forged"] = True
    returned["parent_revision"]["content_digest"] = digest(returned["parent_revision"]["payload"])
    assert port.validate(value)["destination"][0] == "occ-0"
    value["records"]["commands"][0]["dependencies"][0]["pin"]["parent"]["content_digest"] = returned["parent_revision"]["content_digest"]
    before = snapshot(realm[0])
    with pytest.raises(ValidationError, match="materialization"):
        port.validate(value)
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("drop", ["map", "map-and-bindings", "map-and-dependencies", "all-record-facts"])
def test_partial_claim_dropping_does_not_turn_allocation_into_legacy(realm, captured_join, drop):
    _, value, port = captured_join
    record = value["records"]["commands"][0]
    value["id_map"] = {}
    if drop in ("map-and-bindings", "all-record-facts"):
        record["bindings"] = []
    if drop in ("map-and-dependencies", "all-record-facts"):
        record["dependencies"] = []
    # Retain the sealed claim; public map/fact removal cannot erase it.
    before = snapshot(realm[0])
    with pytest.raises(ValidationError, match="materialization"):
        port.validate(value)
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("damage", ["bool-read", "numeric-read", "duplicate-owner", "duplicate-member", "bool-item", "numeric-item", "empty-item", "id-only"])
def test_checker_reads_and_output_membership_use_exact_identities(realm, damage):
    pair = joined(realm)
    value = pair[1]
    record = value["records"]["commands"][0]
    output = value["canonical_document"]
    if damage in ("bool-read", "numeric-read"):
        record["reads"][0]["state"]["value"] = True if damage == "bool-read" else 1
    elif damage == "duplicate-owner":
        occurrences = output["parent_revision"]["payload"]["occurrences"]
        occurrences.append(copy.deepcopy(occurrences[0]))
    else:
        shot = output["shot_revisions"][0]
        item = shot["payload"]["items"][0]
        if damage == "duplicate-member":
            shot["payload"]["items"].append(copy.deepcopy(item))
        elif damage in ("bool-item", "numeric-item", "empty-item"):
            item["item_id"] = {"bool-item": True, "numeric-item": 1, "empty-item": ""}[damage]
        else:
            item["id"] = item.pop("item_id")
        shot["content_digest"] = digest(shot["payload"])
    refresh(value)
    before = snapshot(realm[0])
    if damage == "id-only":
        assert evaluate(realm, pair, "checker")["destination"][0] == "occ-0"
    else:
        with pytest.raises(ValidationError, match="materialization"):
            evaluate(realm, pair, "checker")
    assert snapshot(realm[0]) == before


@pytest.mark.parametrize("damage", ["records", "commands-bool", "event", "receipt", "source-shot", "source-internal"])
def test_durable_m1_proof_cannot_be_reused_after_partial_authentication(realm, damage):
    service, commits, project, _, _ = realm
    pair = joined(realm)
    pair[1]["records"]["commands"][0]["command"]["args"]["on"] = 1
    seal(pair)
    accepted = accept_legacy_projection(commits, pair)
    publication = accepted["receipt"]["receipt_id"]
    # All rows originate in real acceptance. Only corruption is injected here;
    # no fabricated SQL acceptance is used to create a positive history proof.
    if damage == "records":
        row = service.store.conn.execute("SELECT records_json FROM timeline_commit_history WHERE publication_id=?", (publication,)).fetchone()
        records = json.loads(row[0])
        records["commands"][0]["reads"] = []
        service.store.conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?", (json.dumps(records), publication))
    elif damage == "commands-bool":
        row = service.store.conn.execute("SELECT result_json FROM command_idempotency WHERE txn_id=?", (publication,)).fetchone()
        result = json.loads(row[0])
        result["commands"][0]["args"]["on"] = True
        service.store.conn.execute("UPDATE command_idempotency SET result_json=? WHERE txn_id=?", (json.dumps(result), publication))
    elif damage == "event":
        service.store.conn.execute("DELETE FROM timeline_events WHERE id=?", (accepted["receipt"]["event_ids"][-1],))
    elif damage == "receipt":
        service.store.conn.execute("DELETE FROM command_idempotency WHERE txn_id=?", (publication,))
    else:
        table, revision = (("shot_revisions", "source-v1") if damage == "source-shot" else
                           ("internal_timeline_revisions", "source-v1-internal"))
        service.store.conn.execute(f"UPDATE {table} SET payload_json='{{}}' WHERE id=?", (revision,))
    before = snapshot(service)
    if damage.startswith("source-"):
        with pytest.raises(CommitRejected):
            commits.revision_closure(project, "main", pair[0]["request"]["base_revision_id"])
    else:
        with pytest.raises((ProtocolError, CommitRejected)):
            commits.history_entry(project, "main", publication)
    assert snapshot(service) == before


@pytest.mark.parametrize("target", ["self", "future", "missing"])
def test_inverse_history_sequence_rejects_cycles_before_following_target(realm, monkeypatch, target):
    service, commits, project, _, _ = realm
    pair = joined(realm)
    allocation = evaluate(realm, pair, "checker")
    first = accept_legacy_projection(commits, pair)
    later = accept(commits, proposal(service, commits, project, "main", "later-history"))
    publications = {"self": first["receipt"]["receipt_id"], "future": later["receipt"]["receipt_id"], "missing": "absent-publication"}
    records = copy.deepcopy(pair[1]["records"])
    records["commands"][0]["command"]["op"] = "timeline.inverse"
    records["undo_of"] = [publications[target]]
    before = snapshot(service)
    monkeypatch.setattr(commits, "history_entry", lambda *_: pytest.fail("followed a nonhistorical inverse target"))
    with pytest.raises(CommitRejected) as error:
        commits._check_inherited_allocations(project, "main", records, allocation, first["receipt"]["project_seq"][0])
    assert error.value.failure["details"]["reason"] == "invalid_records"
    assert snapshot(service) == before
