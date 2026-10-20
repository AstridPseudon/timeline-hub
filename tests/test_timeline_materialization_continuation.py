"""Original source provenance across real M1 acceptance and recovery.

The added new-form facts exercise the private checker only. They are not an
Agent capture implementation or evidence of native new-map admission.
"""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import ProtocolError, RuntimeErrorBase, ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import RequestCommitPort, route_path
from runtime_protocol.timeline_commit_store import digest, request_identity
from runtime_protocol.timeline_materialization import has_materialization
from test_timeline_commit_integration import Editing, agent, film, rows  # noqa: F401

pytestmark = pytest.mark.integration
OWNER = "occurrence-3"
TARGET = "occurrence:" + OWNER + "/clip:clip-3"


def image_at(document, owner=OWNER):
    occurrence = next(o for o in document["parent_revision"]["payload"]["occurrences"]
                      if o["occurrence_id"] == owner)
    shot = next(s for s in document["shot_revisions"] if s["revision_id"] == occurrence["shot_revision_id"])
    internal = next(i for i in document["internal_timeline_revisions"]
                    if i["revision_id"] == shot["internal_timeline_revision_id"])
    return occurrence, shot, internal


@pytest.fixture
def continuation(film, request):
    service = RuntimeService(film.fixture.duplicate_root)
    try:
        # Main's publication API establishes the shared source before Agent and
        # the renderer-disabled fixture are loaded. No accepted SQL is invented.
        original = service._timeline_commits()[0].revision_closure(
            film.fixture.project_id, film.fixture.timeline_id, film.publication["data"]["revision_id"])
        parent = copy.deepcopy(original["parent_revision"]["payload"])
        occurrence, source, _ = image_at(original)
        shot = {k: copy.deepcopy(source[k]) for k in
                ("shot_id", "revision_id", "internal_timeline_revision_id", "payload")}
        shot["revision_id"] = "continuation-source-with-items"
        media = shot["payload"]["provenance"]["source_media"]
        shot["payload"]["items"] = [{"item_id": raw, "media_id": media, "metadata": {"opaque": [None, raw]}}
                                    for raw in ("original-item-one", "original-item-two")]
        for row in parent["occurrences"]:
            if row["occurrence_id"] == OWNER:
                row["shot_revision_id"] = shot["revision_id"]
        parent["occurrences"].append(dict(occurrence, occurrence_id="shared-sibling",
                                           shot_revision_id=shot["revision_id"],
                                           placement={"start_ms": 6000, "track": "picture"}))
        service.publish_parent_composition(film.fixture.project_id, film.fixture.timeline_id, {
            "project_id": film.fixture.project_id, "timeline_id": film.fixture.timeline_id,
            "expected_head": film.publication["data"]["revision_id"],
            "parent_revision_id": "continuation-shared-source", "parent_composition": parent,
            "shot_revisions": [shot],
        }, idempotency_key="continuation-shared-source")
        actual_agent = request.getfixturevalue("agent")
        service.register_timeline_commit_provider(actual_agent.provider())
        editing = Editing(service, film, actual_agent)
        yield editing
    finally:
        # Tests reopen this same realm and replace Editing.service.
        (editing.service if "editing" in locals() else service).close()


def context(editing, body, key):
    value = {"request": copy.deepcopy(body), "invocation": {
        "operation": "commitTimeline", "path": route_path(editing.project, editing.timeline),
        "body": copy.deepcopy(body)}, "realm_id": editing.service.realm["id"],
        "publisher": "integration-editor", "idempotency_key": key}
    value["request_hash"] = request_identity(value)
    return value


def new_form(editing, original, accepted, command):
    """Keep real M1 B execution; add the proposed source-bound carrier facts."""
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.commit import document_from_bundle

    plan = execute(editing.agent.bundle(accepted["data"]["canonical_document"]), [command])
    document = document_from_bundle(plan.bundle)
    _, source, internal = image_at(original)
    _, destination, _ = image_at(accepted["data"]["canonical_document"])
    items = dict(zip((i["item_id"] for i in source["payload"]["items"]),
                     (i["item_id"] for i in destination["payload"]["items"]), strict=True))
    root = "shot:" + destination["shot_id"]
    key = "materialization.source:" + root
    pin = {"parent": {k: original["parent_revision"][k] for k in ("revision_id", "content_digest")},
           "source": {"shot_id": source["shot_id"], "revision_id": source["revision_id"],
                      "content_digest": source["content_digest"], "internal_timeline_id": internal["timeline_id"],
                      "internal_timeline_revision_id": internal["revision_id"],
                      "internal_timeline_content_digest": internal["content_digest"], "item_id_map": items}}
    record = plan.records[0]
    bindings = {root: "shot:" + source["shot_id"],
                **{root + "/item:" + j: "shot:" + source["shot_id"] + "/item:" + i for i, j in items.items()},
                "materialization.owner:" + root: "occurrence:" + OWNER}
    record["command"].setdefault("bindings", {}).update(bindings)
    record["bindings"].extend({"key": k, "ref": v, "policy": "fixed", "dependencies": [key]}
                              for k, v in bindings.items())
    record["dependencies"].append({"key": key, "kind": "entity", "policy": "exact", "pin": pin})
    value = {"expected_head": editing.head(), "canonical_document": document, "document_digest": digest(document),
             "records": {"schema_version": 1, "commands": plan.records, "undo_of": [], "restored_from": None},
             "id_map": {root: destination["shot_id"], **{root + "/item:" + j: j for j in items.values()}},
             "semantic_events": plan.semantic_events, "provider_version": "checker-only", "compiler_version": "checker-only"}
    body = editing.body([record["command"]])
    return [context(editing, body, "dependent-new-form"), value]


def advance(editing, pair, *, touching=False):
    """C uses the installed provider; B retains its original base and carrier."""
    command = (editing.agent.move(editing.agent.bundle(editing.document()), TARGET, 3.7) if touching
               else editing.move("music-other", 2))
    accepted = editing.commit(editing.body([command]), "intervening-c")
    assert accepted["data"]["status"] == "accepted"
    # Obtain the rebased output through normal M1 preview. The new-form map
    # remains checker-only, while every output image comes from actual replay.
    if not touching:
        body = copy.deepcopy(pair[0]["request"])
        body.update(commands=[copy.deepcopy(editing.pending_b)], dry_run=True)
        before = rows(editing.service)
        preview = editing.commit(body, "legacy-b-disjoint-preview")
        assert preview["data"]["status"] == "preview"
        assert rows(editing.service) == before
        pair[1]["canonical_document"] = preview["data"]["canonical_document"]
        pair[1]["document_digest"] = digest(pair[1]["canonical_document"])
    pair[1]["expected_head"] = editing.head()
    return accepted


def captured_port(editing, pair, original, *, source=True):
    commits = editing.service._timeline_commits()[0]
    port = RequestCommitPort(editing.service, commits, pair[0], lambda: None)
    port.head()
    current = port.revision_closure(pair[1]["expected_head"]["revision_id"])
    if source:
        port.revision_closure(original["parent_revision"]["revision_id"])
    for pin in current["dependency_manifest"]["documents"]:
        port.transcript_source(pin)
    return port


def accepted_slot(editing, port, publication, destination, allocation):
    """Authenticate receipt/event/records before using the legacy slot facts."""
    entry = port.history_entry(publication)
    assert entry["intent"] == "recorded"
    assert not has_materialization({**entry["receipt"]["result"], "records": entry["records"]})
    before = port.revision_closure(entry["previous"]["revision_id"])
    after = port.revision_closure(entry["revision_id"])
    record = entry["records"]["commands"][0]
    assert any(b["ref"] == "occurrence:" + OWNER for b in record["bindings"])
    assert any(r["ref"] == "occurrence:" + OWNER + "/shot" and r["path"] == ["shot_id"]
               and r["state"] == {"state": "present", "value": allocation[1]["source"]["shot_id"]}
               for r in record["reads"])
    return editing.service._timeline_commits()[0]._same_materialization_slot(
        destination, OWNER, allocation, None, before, after)


def begin(editing):
    original = editing.document()
    body = editing.body([editing.agent.move(editing.agent.bundle(original), TARGET, 3.5)])
    accepted = editing.commit(body, "a-lost-ack")
    assert accepted["data"]["status"] == "accepted"
    editing.assert_readback(accepted)
    local = accepted["data"]["canonical_document"]
    command = editing.agent.move(editing.agent.bundle(local), TARGET, 3.6)
    editing.pending_b = copy.deepcopy(command)
    pair = new_form(editing, original, accepted, command)
    return original, body, accepted, pair


def test_original_source_map_survives_ack_disjoint_c_and_reopen(continuation, monkeypatch):
    editing = continuation
    original, body, accepted, pair = begin(editing)
    sealed = json.dumps(pair)
    destination, allocation = next(iter(captured_allocation(editing, pair, original).items()))
    assert allocation[1]["source"]["item_id_map"]
    assert set(allocation[1]["source"]["item_id_map"]) == {"original-item-one", "original-item-two"}
    assert all(i != j for i, j in allocation[1]["source"]["item_id_map"].items())
    advance(editing, pair)
    history = editing.history()
    editing.service.close()
    editing.service = RuntimeService(editing.film.fixture.duplicate_root)
    editing.service.register_timeline_commit_provider(editing.agent.provider())
    before = rows(editing.service)
    with monkeypatch.context() as retry:
        retry.setattr(type(editing.service._timeline_commit_provider), "commit",
                      lambda *_: pytest.fail("exact A retry ran the provider"))
        assert editing.commit(json.loads(json.dumps(body)), "a-lost-ack") == accepted
    assert rows(editing.service) == before
    assert editing.history() == history
    recovered = json.loads(sealed)
    assert pair[0] == recovered[0]  # B's base, guards, bindings and source pin stay sealed.
    assert pair[1]["id_map"] == recovered[1]["id_map"]
    assert pair[1]["records"] == recovered[1]["records"]
    record = pair[1]["records"]["commands"][0]
    assert record["created"] == []
    assert record["command"].get("created", []) == []
    assert any(r["ref"] == "occurrence:" + OWNER + "/shot" and r["path"] == ["shot_id"]
               and r["state"] == {"state": "present", "value": destination} for r in record["reads"])
    assert record["command"]["bindings"]["shot:" + destination] == "shot:" + allocation[1]["source"]["shot_id"]
    assert image_at(editing.document())[1:] == image_at(accepted["data"]["canonical_document"])[1:]
    assert editing.document(original["parent_revision"]["revision_id"]) == original
    port = captured_port(editing, pair, original)
    try:
        assert port.validate(pair[1]) == {destination: allocation}
        assert accepted_slot(editing, port, accepted["receipt"]["receipt_id"], destination, allocation)
    finally:
        port.close()
    assert rows(editing.service) == before


def captured_allocation(editing, pair, original):
    port = captured_port(editing, pair, original)
    try:
        return port.validate(pair[1])
    finally:
        port.close()


@pytest.mark.parametrize("damage", ["current-source-pin", "missing-source-capture", "owner-replacement",
                                          "source-membership", "destination-membership", "recapture-current-binding",
                                          "fresh-birth", "source-digest"])
def test_continuation_refuses_changed_provenance_without_writes(continuation, damage):
    editing = continuation
    original, _, _, pair = begin(editing)
    advance(editing, pair)
    value = pair[1]
    record = value["records"]["commands"][0]
    dependency = record["dependencies"][-1]
    source = dependency["pin"]["source"]
    destination = image_at(value["canonical_document"])[1]
    if damage == "current-source-pin":
        dependency["pin"]["parent"] = {k: editing.document()["parent_revision"][k]
                                        for k in ("revision_id", "content_digest")}
    elif damage == "owner-replacement":
        record["bindings"][-1]["ref"] = "occurrence:shared-sibling"
        record["command"]["bindings"][record["bindings"][-1]["key"]] = "occurrence:shared-sibling"
    elif damage == "source-membership":
        source["item_id_map"].pop("original-item-one")
    elif damage == "destination-membership":
        destination["payload"]["items"].pop()
        destination["content_digest"] = digest(destination["payload"])
    elif damage == "recapture-current-binding":
        record["bindings"][-4]["ref"] = "shot:" + destination["shot_id"]
    elif damage == "fresh-birth":
        record["created"].append({"kind": "shot", "ref": "shot:" + destination["shot_id"], "owner": None})
    elif damage == "source-digest":
        source["content_digest"] = "sha256:" + "0" * 64
    pair[0]["request"]["commands"] = [copy.deepcopy(record["command"])]
    pair[0] = context(editing, pair[0]["request"], "damaged-b")
    before = rows(editing.service)
    port = captured_port(editing, pair, original, source=damage != "missing-source-capture")
    try:
        with pytest.raises((ValidationError, CommitRejected)):
            port.validate(value)
    finally:
        port.close()
    assert rows(editing.service) == before


@pytest.mark.parametrize("damage", ["missing-accepted-edge", "corrupt-records", "corrupt-event", "wrong-owner", "wrong-parent"])
def test_own_slot_requires_authenticated_accepted_edge(continuation, damage):
    editing = continuation
    original, _, accepted, pair = begin(editing)
    destination, allocation = next(iter(captured_allocation(editing, pair, original).items()))
    advance(editing, pair)
    conn = editing.service.store.conn
    publication = accepted["receipt"]["receipt_id"]
    if damage == "missing-accepted-edge":
        # Deliberate damage to genuine acceptance, including retained inputs
        # which otherwise prevent deleting the edge through the SQL FK.
        conn.execute("PRAGMA foreign_keys=OFF")
        conn.execute("DELETE FROM timeline_commit_history WHERE publication_id=?", (publication,))
        conn.execute("PRAGMA foreign_keys=ON")
    elif damage == "corrupt-records":
        entry = conn.execute("SELECT records_json FROM timeline_commit_history WHERE publication_id=?", (publication,)).fetchone()
        records = json.loads(entry[0])
        records["commands"][0]["reads"] = []
        conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?", (json.dumps(records), publication))
    elif damage == "corrupt-event":
        conn.execute("UPDATE timeline_events SET event_hash=? WHERE id=?",
                     ("0" * 64, accepted["receipt"]["event_ids"][-1]))
    elif damage == "wrong-owner":
        allocation = ("shared-sibling", allocation[1])
    else:
        allocation[1]["parent"]["revision_id"] = editing.head()["revision_id"]
    before = rows(editing.service)
    if damage.startswith("wrong-"):
        port = captured_port(editing, pair, original)
        try:
            assert not accepted_slot(editing, port, publication, destination, allocation)
        finally:
            port.close()
    else:
        # The map remains valid in isolation; durable authentication refuses
        # before any slot comparison can treat it as acceptance authority.
        port = RequestCommitPort(editing.service, editing.service._timeline_commits()[0], pair[0], lambda: None)
        try:
            with pytest.raises((ProtocolError, CommitRejected)):
                port.history_entry(publication)
        finally:
            port.close()
    assert rows(editing.service) == before


def test_original_b_value_guards_refuse_touching_c(continuation):
    editing = continuation
    original, _, _, pair = begin(editing)
    body = copy.deepcopy(pair[0]["request"])
    # Use the ACTUAL captured M1 command, without the checker-only facts.
    body["commands"] = [copy.deepcopy(editing.pending_b)]
    advance(editing, pair, touching=True)
    before = rows(editing.service)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(body, "original-b-after-touching-c")
    assert error.value.details["status"] == "conflict"
    # Current Agent checks the captured source dependency before write history.
    assert error.value.details["reason"] == "dependency_changed"
    assert rows(editing.service) == before


@pytest.mark.parametrize("retired", [False, True])
def test_actual_m1_allocation_refuses_global_raw_item_occupancy(continuation, retired):
    editing = continuation
    original = editing.document()
    command = editing.agent.move(editing.agent.bundle(original), TARGET, 3.5)
    body = editing.body([command])
    preview_body = dict(body, dry_run=True)
    before = rows(editing.service)
    preview = editing.commit(preview_body, "inspect-m1-allocation")
    assert preview["data"]["status"] == "preview"
    assert rows(editing.service) == before
    raw = image_at(preview["data"]["canonical_document"])[1]["payload"]["items"][0]["item_id"]
    # Use the observed raw ID; no assumption about deterministic ID spelling.
    service = editing.service
    foreign = service.create_project({"slug": "foreign", "name": "Foreign"}, idempotency_key="foreign")["id"]
    media = service.ingest(foreign, b"foreign-item", media_type="image/png",
                           idempotency_key="foreign-media")["data"]["object_id"]
    from test_timeline_projection_occupancy import accept, image, new_timeline, proposal, with_media

    # Direct shot writers are retired. Establish the foreign occupant through
    # genuine host acceptance; only the tested allocation uses native Agent code.
    commits = service._timeline_commits()[0]
    new_timeline(service, commits, foreign, "foreign-timeline")
    item = {"item_id": raw, "media_id": media}
    accept(commits, with_media(proposal(service, commits, foreign, "foreign-timeline", "foreign-item",
        shots=[image("foreign-owner", "foreign-item-v1", items=[item])]), item))
    if retired:
        accept(commits, proposal(service, commits, foreign, "foreign-timeline", "retire-foreign-item",
            shots=[image("foreign-owner", "foreign-item-v2")]))
    before = rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(body, "m1-occupied-allocation")
    assert error.value.details["status"] == "refused"
    assert error.value.details["reason"] == "identity_collision"
    assert rows(service) == before
