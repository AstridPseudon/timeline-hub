"""Physical projection ownership at Runtime's acceptance boundary.

Detached candidates intentionally exercise a trusted-provider boundary, not
Agent allocation, command execution or inverse semantics. Existing integration
neighbours exercise the actual provider; no accepted history is seeded by SQL.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_store import TimelineCommitStore, request_identity
from test_timeline_commit_acceptance import (
    realm, validate_prepared,  # noqa: F401 (shared API-built fixture)
)
from test_timeline_projection_occupancy import (
    accept, image, inverse_request, media_item, new_timeline, proposal,
    seed_slot, snapshot, with_media,
)


def refuses(service, commits, pair, monkeypatch, *, reason="identity_collision", preview=False):
    before = snapshot(service)
    with monkeypatch.context() as patch:
        patch.setattr(commits, "_persist_closure", lambda *_: pytest.fail("projection preflight wrote a revision"))
        with pytest.raises(CommitRejected) as error:
            (commits.preview if preview else commits.accept)(*pair, authorize=lambda: None)
    assert error.value.failure["details"]["reason"] == reason
    assert error.value.failure["details"]["current"] is None
    assert snapshot(service) == before  # projections, heads, history, receipts, events and sequences


@pytest.mark.parametrize("archived", [False, True])
@pytest.mark.parametrize("claim", [False, True])
def test_other_timeline_occupied_shot_and_compiler_slot_refuse_atomically(realm, monkeypatch, archived, claim):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    accept(commits, proposal(service, commits, project, "other", "owner", shots=[image("occupied", "owner-shot", archived=archived)]))
    candidate = proposal(service, commits, project, "main", "intruder", shots=[image("occupied", "intruder-shot")])
    if claim:
        # A created fact alone cannot grant authority. Agent owns consistency
        # with command.created; Runtime must still refuse the physical occupant.
        candidate[1]["records"]["commands"][0]["created"] = [{"kind": "shot", "ref": "shot:occupied", "owner": None}]
    refuses(service, commits, candidate, monkeypatch, reason="destination_occupied")


def test_foreign_global_shot_refuses_without_disclosing_owner(realm, monkeypatch):
    service, commits, project, _, _ = realm
    foreign = service.create_project({"slug": "foreign", "name": "Foreign secret"})["id"]
    new_timeline(service, commits, foreign, "foreign-timeline")
    accept(commits, proposal(service, commits, foreign, "foreign-timeline", "foreign-seed",
                             shots=[image("global-shot", "foreign-shot")]))
    candidate = proposal(service, commits, project, "main", "foreign-intruder", shots=[image("global-shot", "intruder-shot")])
    refuses(service, commits, candidate, monkeypatch, reason="destination_occupied")


@pytest.mark.parametrize("case", ["same-shot-duplicate", "two-shot-duplicate", "foreign-shot", "empty"])
def test_complete_item_write_set_refuses_before_any_revision(realm, monkeypatch, case):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "reserved-item")
    accept(commits, with_media(proposal(service, commits, project, "main", "item-owner",
                                      shots=[image("a-owner", "owner-shot", items=[item])]), item))
    shots = [image("a-owner", "updated-owner", items=[item])]
    if case == "same-shot-duplicate":
        shots = [image("a-owner", "updated-owner", items=[item, item])]
    elif case == "two-shot-duplicate":
        shots += [image("b-new", "new-shot", items=[item])]
    elif case == "foreign-shot":
        shots = [image("b-new", "new-shot", items=[item])]
    elif case == "empty":
        shots = [image("a-owner", "updated-owner", items=[dict(item, item_id="")])]
    refuses(service, commits, with_media(proposal(service, commits, project, "main", "item-intruder", shots=shots), item), monkeypatch)


def test_own_primary_update_preserves_distinct_opaque_secondary_and_its_unrelated_owner(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    item = media_item(service, project, "reserved-item")
    original = accept(commits, with_media(proposal(service, commits, project, "main", "item-owner",
        shots=[image("a-owner", "owner-shot", items=[item])]), item))["data"]["canonical_document"]
    new_timeline(service, commits, project, "other")
    unrelated = dict(item, item_id="different")
    accept(commits, with_media(proposal(service, commits, project, "other", "secondary-owner",
        shots=[image("unrelated", "unrelated-shot", items=[unrelated])]), unrelated))
    before = tuple(service.store.conn.execute("SELECT * FROM shot_items WHERE id='different'").fetchone())
    # The former conflicting-alias negative supplied only an own-primary
    # update. The stored codec treats its distinct secondary as opaque data.
    updated = dict(item, id="different")
    pair = with_media(proposal(service, commits, project, "main", "opaque-update",
        shots=[image("a-owner", "updated-owner", items=[updated])]), updated)
    accepted = accept(commits, pair)
    document = accepted["data"]["canonical_document"]
    assert document == pair[1]["canonical_document"]
    assert document["shot_revisions"][0]["payload"]["items"] == [updated]
    assert accepted["receipt"]["result"] == accepted["data"]
    assert commits.history_entry(project, "main", accepted["receipt"]["receipt_id"])["records"] == pair[1]["records"]
    assert commits.revision_closure(project, "main", document["parent_revision"]["revision_id"]) == document
    assert commits.revision_closure(project, "main", original["parent_revision"]["revision_id"]) == original
    assert [tuple(r) for r in service.store.conn.execute("SELECT id, shot_id FROM shot_items ORDER BY id")] == [
        ("different", "unrelated"), ("reserved-item", "a-owner")]
    assert tuple(service.store.conn.execute("SELECT * FROM shot_items WHERE id='different'").fetchone()) == before
    assert service.store.integrity_report()["ok"]


def test_retired_item_cannot_be_moved_to_another_owner(realm, monkeypatch):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "retired-item")
    accept(commits, with_media(proposal(service, commits, project, "main", "retired-owner",
                                      shots=[image("owner", "items-v1", items=[item])]), item))
    accept(commits, proposal(service, commits, project, "main", "remove-item", shots=[image("owner", "items-v2")]))
    assert service.store.conn.execute("SELECT 1 FROM shot_items WHERE id=?", (item["item_id"],)).fetchone() is None
    new_timeline(service, commits, project, "other")
    pair = with_media(proposal(service, commits, project, "other", "steal-retired",
                               shots=[image("new-owner", "new-owner-v1", items=[item])]), item)
    refuses(service, commits, pair, monkeypatch)


def test_unoccupied_and_same_owner_updates_and_parent_only_do_not_scan_history(realm):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "item")
    accept(commits, with_media(proposal(service, commits, project, "main", "first",
                                      shots=[image("owner", "first-shot", items=[item])]), item))
    accept(commits, with_media(proposal(service, commits, project, "main", "update",
                                      shots=[image("owner", "second-shot", items=[item])]), item))
    parent_only = proposal(service, commits, project, "main", "parent-only")
    # SQLite trace catches unbounded history enumeration; head verification's
    # exact publication reads remain necessary.
    queries = []
    service.store.conn.set_trace_callback(queries.append)
    try:
        accept(commits, parent_only)
        accept(commits, with_media(proposal(service, commits, project, "main", "third",
                                          shots=[image("owner", "third-shot", items=[item])]), item))
    finally:
        service.store.conn.set_trace_callback(None)
    assert not any("FROM timeline_commit_history h LEFT JOIN" in q for q in queries)
    assert service.store.integrity_report()["ok"]


def test_preview_refuses_collisions_and_does_not_reserve_free_ids(realm, monkeypatch):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    pair = proposal(service, commits, project, "main", "preview", shots=[image("available", "preview-shot")])
    pair[0]["request"]["dry_run"] = True
    pair[0]["invocation"]["body"] = copy.deepcopy(pair[0]["request"])
    pair[0]["request_hash"] = request_identity(pair[0])
    before = snapshot(service)
    assert commits.preview(*pair, authorize=lambda: None)["receipt"] is None
    assert snapshot(service) == before
    accept(commits, proposal(service, commits, project, "other", "claim-after-preview", shots=[image("available", "accepted-shot")]))
    refuses(service, commits, pair, monkeypatch, reason="destination_occupied", preview=True)


def test_two_acceptors_race_for_one_global_shot(realm):
    service, commits, project, _, root = realm
    new_timeline(service, commits, project, "other")
    pairs = [proposal(service, commits, project, timeline, "race-" + timeline,
                      shots=[image("raced-shot", "shot-" + timeline)]) for timeline in ("main", "other")]
    barrier = Barrier(2)
    def run(pair):
        barrier.wait(timeout=10)
        store = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
        with service.store._mutex:
            before = snapshot(service)
            try:
                return accept(store, pair)["data"]["status"]
            except CommitRejected as error:
                assert snapshot(service) == before
                return error.failure["details"]["reason"]
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(run, pairs)) == ["accepted", "destination_occupied"]
    assert service.store.conn.execute("SELECT COUNT(*) FROM shot_revisions").fetchone()[0] == 1
    assert service.store.conn.execute("SELECT COUNT(*) FROM timeline_commit_history WHERE intent='recorded'").fetchone()[0] == 1
    assert commits.integrity_errors() == []


def test_retry_returns_before_guard_after_head_advance_and_restart(realm, monkeypatch):
    service, commits, project, _, root = realm
    first = proposal(service, commits, project, "main", "original", shots=[image("shot", "original-shot")])
    accepted = accept(commits, first)
    accept(commits, proposal(service, commits, project, "main", "advance"))
    service.close()
    restarted = RuntimeService(root)
    try:
        store = TimelineCommitStore(restarted.store, validate_prepared=validate_prepared)
        def tripwire(*_):
            pytest.fail("exact retry inspected new projection or ran the provider")
        monkeypatch.setattr(store, "_check_shot_destinations", tripwire)
        monkeypatch.setattr(store, "_validate", tripwire)
        before = snapshot(restarted)
        assert accept(store, first) == accepted
        assert snapshot(restarted) == before
    finally:
        restarted.close()


@pytest.mark.parametrize("proof", [True, False])
def test_historical_slot_requires_exact_accepted_occurrence_source_proof(realm, monkeypatch, proof):
    service, commits, project, _, _ = realm
    source, result = seed_slot(service, commits, project, proof=proof)
    # Exact source-image reuse remains legal, even though the current slot has
    # another physical ID. An inverse then rematerializes the same proven slot.
    restored = accept(commits, proposal(service, commits, project, "main", "restore-source", shots=[source]))
    assert restored["data"]["canonical_document"]["shot_revisions"] == [source[0]]
    pair = proposal(service, commits, project, "main", "rematerialize-slot", shots=[image("slot", "slot-v2")])
    if proof:
        assert accept(commits, pair)["data"]["status"] == "accepted"
        assert commits.history_entry(project, "main", result["receipt"]["receipt_id"])["records"]["commands"][0]["created"] == []
    else:
        refuses(service, commits, pair, monkeypatch, reason="destination_occupied")


def test_verified_inverse_reuses_only_its_actual_historical_owner(realm, monkeypatch):
    service, commits, project, _, _ = realm
    source, result = seed_slot(service, commits, project)
    target = result["receipt"]["receipt_id"]
    # A new content revision of the actual before-owner is authorized. This
    # boundary fixture supplies it; Agent still owns reversing authored writes.
    restored = inverse_request(proposal(service, commits, project, "main", "inverse-source",
                                       shots=[image("source", "source-v2")]), [target])
    assert accept(commits, restored)["data"]["status"] == "accepted"
    new_timeline(service, commits, project, "other")
    accept(commits, proposal(service, commits, project, "other", "unrelated-parent", shots=[image("unrelated", "unrelated-v1")]))
    attack = inverse_request(proposal(service, commits, project, "main", "unrelated-inverse",
                                     shots=[image("unrelated", "unrelated-v2")]), [target])
    refuses(service, commits, attack, monkeypatch, reason="destination_occupied")


def test_tampered_historical_slot_record_is_not_owner_proof(realm):
    service, commits, project, _, _ = realm
    source, result = seed_slot(service, commits, project)
    accept(commits, proposal(service, commits, project, "main", "back-to-source", shots=[source]))
    # Deliberate corruption of a genuinely accepted edge, never fabricated
    # accepted history. Its event/receipt must authenticate the owner evidence.
    service.store.conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?",
                               ('{"commands":[]}', result["receipt"]["receipt_id"]))
    pair = proposal(service, commits, project, "main", "tampered-slot", shots=[image("slot", "slot-v2")])
    before = snapshot(service)
    from runtime_protocol.errors import ProtocolError

    with pytest.raises(ProtocolError, match="corrupt"):
        accept(commits, pair)
    assert snapshot(service) == before


def test_retired_shot_on_archived_timeline_stays_reserved(realm, monkeypatch):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    accept(commits, proposal(service, commits, project, "other", "retired-shot", shots=[image("retired", "retired-v1")]))
    accept(commits, proposal(service, commits, project, "other", "remove-shot", shots=[]))
    version = service.get_project_timeline(project, "other")["version"]
    service.archive_timeline("other", {"expected_version": version}, idempotency_key="archive-other")
    refuses(service, commits, proposal(service, commits, project, "main", "reuse-retired",
                                       shots=[image("retired", "retired-v2")]), monkeypatch, reason="destination_occupied")


def test_global_item_collision_across_projects_and_preallocated_copy(realm, monkeypatch):
    service, commits, project, _, _ = realm
    foreign = service.create_project({"slug": "item-owner", "name": "Item owner"})["id"]
    new_timeline(service, commits, foreign, "foreign")
    foreign_item = media_item(service, foreign, "global-item")
    accept(commits, with_media(proposal(service, commits, foreign, "foreign", "foreign-item-parent",
                                      shots=[image("foreign-shot", "foreign-item-shot", items=[foreign_item])]), foreign_item))
    item = media_item(service, project, "global-item")
    refuses(service, commits, with_media(proposal(service, commits, project, "main", "global-item-collision",
                                                 shots=[image("local", "local-collision", items=[item])]), item), monkeypatch)
    allocated = dict(item, item_id="preallocated-copy")
    accept(commits, with_media(proposal(service, commits, project, "main", "preallocated",
                                      shots=[image("local", "local-v1", items=[allocated])]), allocated))
    assert service.store.integrity_report()["ok"]


@pytest.mark.parametrize("kind,ref,owner", [("shot", "shot:new", None), ("item", "shot:new/item:new", "shot:new")])
def test_frozen_artifact_does_not_yet_carry_typed_physical_creation_claims(realm, monkeypatch, kind, ref, owner):
    service, commits, project, _, _ = realm
    pair = proposal(service, commits, project, "main", "typed-claim")
    record = pair[1]["records"]["commands"][0]
    record["created"] = [{"ref": ref, "kind": kind, "owner": owner}]
    record["command"]["created"] = [ref]
    # This is the explicit Agent artifact dependency. Do not widen the frozen
    # schema here or fake an accepted created-and-removed reservation by SQL.
    refuses(service, commits, pair, monkeypatch, reason="invalid_prepared")


def test_captured_external_source_does_not_authorize_mutable_overwrite(realm, monkeypatch):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.timeline_commit_port import route_path
    from test_timeline_commit_port import PreparedProvider

    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    source = image("external-source", "external-v1")
    accept(commits, proposal(service, commits, project, "other", "external-parent", shots=[source]))
    pair = proposal(service, commits, project, "main", "source-read-overwrite",
                    shots=[image("external-source", "external-v2")])
    pair[0]["request"]["commands"][0]["args"]["source"] = {"shot_id": "external-source", "revision_id": "external-v1"}
    pair[1]["records"]["commands"][0]["command"] = copy.deepcopy(pair[0]["request"]["commands"][0])
    def action(context, port):
        port.head()
        port.revision_closure(pair[1]["expected_head"]["revision_id"])
        assert port.shot_closure("external-source", "external-v1")["shot_revision"] == source[0]
        return port.accept(pair[1])
    provider = PreparedProvider(action)
    service.register_timeline_commit_provider(provider)
    before = snapshot(service)
    with monkeypatch.context() as patch:
        patch.setattr(TimelineCommitStore, "_persist_closure", lambda *_: pytest.fail("source read granted overwrite authority"))
        with pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(project, "main", pair[0]["request"], idempotency_key="source-read-overwrite",
                                    publisher="author", invocation_path=route_path(project, "main"), authorize=lambda: None)
    assert error.value.details["reason"] == "destination_occupied"
    assert provider.calls == 1
    assert snapshot(service) == before


def test_external_exact_immutable_image_reuse_does_not_write_its_projection(realm):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    source = image("source", "source-v1")
    accept(commits, proposal(service, commits, project, "other", "external-source-parent", shots=[source]))
    before = [tuple(r) for r in service.store.conn.execute("SELECT * FROM project_shots")]
    accepted = accept(commits, proposal(service, commits, project, "main", "exact-source-reuse", shots=[source]))
    assert accepted["data"]["canonical_document"]["shot_revisions"] == [source[0]]
    assert [tuple(r) for r in service.store.conn.execute("SELECT * FROM project_shots")] == before
    assert service.store.conn.execute("SELECT COUNT(*) FROM shot_revisions").fetchone()[0] == 1


def test_duplicate_mutable_shot_destinations_refuse_before_persistence(realm, monkeypatch):
    service, commits, project, _, _ = realm
    pair = proposal(service, commits, project, "main", "duplicate-shots",
                    shots=[image("same", "first"), image("same", "second")])
    refuses(service, commits, pair, monkeypatch)


def test_retired_item_can_return_to_its_current_owner(realm):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "returning-item")
    accept(commits, with_media(proposal(service, commits, project, "main", "with-item",
                                      shots=[image("owner", "with-item-shot", items=[item])]), item))
    accept(commits, proposal(service, commits, project, "main", "without-item", shots=[image("owner", "without-item-shot")]))
    result = accept(commits, with_media(proposal(service, commits, project, "main", "return-item",
                                               shots=[image("owner", "return-item-shot", items=[item])]), item))
    assert result["data"]["canonical_document"]["shot_revisions"][0]["payload"]["items"] == [item]
    assert service.store.integrity_report()["ok"]


def test_verified_inverse_rematerializes_its_historical_items(realm):
    service, commits, project, _, _ = realm
    item = media_item(service, project, "source-item")
    accept(commits, with_media(proposal(service, commits, project, "main", "source-with-item",
                                      shots=[image("source", "source-item-v1", items=[item])]), item))
    slot = proposal(service, commits, project, "main", "move-to-slot", shots=[image("slot", "slot-v1")])
    slot[1]["records"]["commands"][0]["writes"] = [{
        "ref": "occurrence:occ-0/clip:clip", "path": ["at"],
        "before": {"state": "present", "value": 0}, "after": {"state": "present", "value": 1},
    }]
    moved = accept(commits, slot)
    restored = inverse_request(with_media(proposal(service, commits, project, "main", "restore-source-items",
                                                  shots=[image("source", "source-item-v2", items=[item])]), item),
                               [moved["receipt"]["receipt_id"]])
    result = accept(commits, restored)
    assert result["data"]["canonical_document"]["shot_revisions"][0]["payload"]["items"] == [item]
    assert service.store.integrity_report()["ok"]


def creation(pair, identity="retired"):
    # A schema-supported track proves exact recorder reservation independently
    # of physical shot/item spelling, which still awaits the official artifact.
    record = pair[1]["records"]["commands"][0]
    ref = "parent/track:" + identity
    record["created"] = [{"ref": ref, "kind": "track", "owner": "parent"}]
    record["command"]["created"] = [ref]
    pair[0]["request"]["commands"] = [copy.deepcopy(record["command"])]
    pair[0]["invocation"]["body"] = copy.deepcopy(pair[0]["request"])
    pair[0]["request_hash"] = request_identity(pair[0])
    return pair


def test_accepted_creation_reserves_even_without_final_projection(realm, monkeypatch):
    service, commits, project, _, _ = realm
    first = creation(proposal(service, commits, project, "main", "create-and-remove"))
    # At this trusted-provider boundary the detached record is authoritative;
    # no SQL fabricates acceptance and the final closure contains no such track.
    accepted = accept(commits, first)
    records = commits.history_entry(project, "main", accepted["receipt"]["receipt_id"])["records"]
    assert records["commands"][0]["created"] == first[1]["records"]["commands"][0]["created"]
    accept(commits, proposal(service, commits, project, "main", "advance-after-creation"))
    refuses(service, commits, creation(proposal(service, commits, project, "main", "reclaim")), monkeypatch)
    # Timeline-local track references do not reserve another timeline's track.
    new_timeline(service, commits, project, "other")
    assert accept(commits, creation(proposal(service, commits, project, "other", "other-create")))["data"]["status"] == "accepted"
    assert accept(commits, creation(proposal(service, commits, project, "main", "fresh-create"), "fresh"))["data"]["status"] == "accepted"


def test_matching_creation_history_is_authenticated(realm):
    from runtime_protocol.errors import ProtocolError

    service, commits, project, _, _ = realm
    accepted = accept(commits, creation(proposal(service, commits, project, "main", "reserved")))
    # Advance so the matching reservation is not also the current/base edge.
    accept(commits, proposal(service, commits, project, "main", "after-reservation"))
    service.store.conn.execute("UPDATE timeline_commit_history SET publisher=? WHERE publication_id=?",
                               ("tampered", accepted["receipt"]["receipt_id"]))
    before = snapshot(service)
    with pytest.raises(ProtocolError, match="corrupt"):
        accept(commits, creation(proposal(service, commits, project, "main", "tampered-reservation")))
    assert snapshot(service) == before


@pytest.fixture
def shared_editing(film, request):
    from test_timeline_commit_integration import Editing

    service = RuntimeService(film.fixture.duplicate_root)
    try:
        # Extend the existing genuine legacy film fixture before establishing
        # its accepted baseline. All measured moves/inverses use real Agent.
        parent = service.get_project_parent_composition_revision(
            film.fixture.project_id, film.fixture.timeline_id, film.publication["data"]["revision_id"])["payload"]
        repeated = copy.deepcopy(parent["occurrences"][-1])
        repeated.update(occurrence_id="repeated-third", placement={"start_ms": 6000, "track": "picture"})
        parent["occurrences"].append(repeated)
        service.publish_parent_composition(film.fixture.project_id, film.fixture.timeline_id, {
            "project_id": film.fixture.project_id, "timeline_id": film.fixture.timeline_id,
            "expected_head": film.publication["data"]["revision_id"], "parent_revision_id": "shared-shot-baseline",
            "parent_composition": parent,
        }, idempotency_key="shared-shot-baseline")
        agent = request.getfixturevalue("agent")  # Disable rendering after the legacy seed.
        service.register_timeline_commit_provider(agent.provider())
        yield Editing(service, film, agent)
    finally:
        service.close()


# Reuse renderer-disabled actual-provider fixtures; Agent imports remain inside
# their explicitly selected integration fixtures.
from test_timeline_commit_integration import agent, film  # noqa: E402,F401


# Shared-occurrence inverse restores the exact authored/source closure.
@pytest.mark.integration
def test_actual_provider_shared_slot_move_inverse_redo_and_rematerialization(shared_editing):
    from test_timeline_commit_integration import inverse

    editing = shared_editing
    original = editing.document()
    owner = "occurrence:occurrence-3/clip:clip-3"
    command = editing.agent.move(editing.agent.bundle(original), owner, 3.5)
    first = editing.commit(editing.body([command]), "shared-first-move")
    editing.assert_readback(first)
    undone = editing.commit(editing.body([inverse(first["receipt"]["receipt_id"])]), "shared-undo")
    assert undone["data"]["canonical_document"]["shot_revisions"] == original["shot_revisions"]
    redone = editing.commit(editing.body([inverse(undone["receipt"]["receipt_id"])]), "shared-redo")
    assert redone["data"]["canonical_document"]["shot_revisions"] == first["data"]["canonical_document"]["shot_revisions"]
    editing.commit(editing.body([inverse(redone["receipt"]["receipt_id"])]), "shared-undo-again")
    next_move = editing.agent.move(editing.agent.bundle(editing.document()), owner, 3.6)
    rematerialized = editing.commit(editing.body([next_move]), "shared-rematerialize")
    editing.assert_readback(rematerialized)
    first_slots = {s["shot_id"] for s in first["data"]["canonical_document"]["shot_revisions"]}
    assert {s["shot_id"] for s in rematerialized["data"]["canonical_document"]["shot_revisions"]} == first_slots


@pytest.mark.integration
def test_actual_provider_historical_slot_rematerializes_after_verified_restore(shared_editing):
    editing = shared_editing
    original = editing.document()
    owner = "occurrence:occurrence-3/clip:clip-3"
    move = editing.agent.move(editing.agent.bundle(original), owner, 3.5)
    first = editing.commit(editing.body([move]), "shared-move-before-restore")
    pin = {k: original["parent_revision"][k] for k in ("revision_id", "content_digest")}
    restored = editing.commit(editing.body([{
        "schema_version": 1, "op": "timeline.restore", "version": "1", "select": None, "args": pin,
    }]), "shared-verified-restore")
    assert restored["data"]["canonical_document"]["shot_revisions"] == original["shot_revisions"]
    move = editing.agent.move(editing.agent.bundle(editing.document()), owner, 3.6)
    rematerialized = editing.commit(editing.body([move]), "shared-after-restore")
    editing.assert_readback(rematerialized)
    assert {s["shot_id"] for s in rematerialized["data"]["canonical_document"]["shot_revisions"]} == {
        s["shot_id"] for s in first["data"]["canonical_document"]["shot_revisions"]}


def test_missing_accepted_history_fails_closed_before_fresh_allocation(realm, monkeypatch):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    result = accept(commits, proposal(service, commits, project, "other", "proof-to-remove"))
    # Corrupt genuine accepted history; the retained receipt is not a substitute
    # for the missing allocation facts, even if its projection is empty.
    service.store.conn.execute("UPDATE parent_composition_heads SET publication_id=NULL WHERE timeline_id='other'")
    service.store.conn.execute("DELETE FROM timeline_commit_history WHERE publication_id=?", (result["receipt"]["receipt_id"],))
    pair = proposal(service, commits, project, "main", "fresh-with-missing-history", shots=[image("free", "free-v1")])
    refuses(service, commits, pair, monkeypatch)


@pytest.mark.parametrize("raw", ["raw-item", "with:colon", "with spaces"])
def test_item_reservation_identity_compares_raw_ids_across_shot_owners(raw):
    assert TimelineCommitStore._reservation_identity("item", "shot:first/item:" + raw) == raw
    assert TimelineCommitStore._reservation_identity("item", "shot:second/item:" + raw) == raw
    assert TimelineCommitStore._reservation_identity("shot", "shot:first") == "shot:first"
    assert TimelineCommitStore._reservation_identity("shot", "shot:second") == "shot:second"


@pytest.mark.parametrize("ref", ["shot:owner/item:", "shot:owner/item: ", "shot:owner/item:i/extra",
                                 "shot:owner/item:i::x", "occurrence:owner/item:i", "raw-item"])
def test_item_reservation_rejects_noncanonical_refs(ref):
    with pytest.raises(CommitRejected) as error:
        TimelineCommitStore._reservation_identity("item", ref)
    assert error.value.failure["details"]["reason"] == "invalid_records"


@pytest.mark.parametrize("kind", ["shot", "item"])
@pytest.mark.parametrize("occupant", ["live", "retired", "archived", "foreign"])
def test_detached_native_birth_checks_actual_live_and_retained_destinations(realm, kind, occupant):
    service, commits, project, _, _ = realm
    owner = service.create_project({"slug": "foreign-birth-owner", "name": "Foreign"})["id"] if occupant == "foreign" else project
    new_timeline(service, commits, owner, "birth-owner")
    item = media_item(service, owner, "reserved-raw-item")
    accept(commits, with_media(proposal(service, commits, owner, "birth-owner", "birth-physical-owner",
        shots=[image("reserved-shot", "birth-owner-v1", items=[item], archived=occupant == "archived")]), item))
    if occupant == "retired":
        accept(commits, proposal(service, commits, owner, "birth-owner", "remove-physical-item",
                                shots=[image("reserved-shot", "birth-owner-v2")]))
        accept(commits, proposal(service, commits, owner, "birth-owner", "remove-physical-shot", shots=[]))
        assert service.store.conn.execute("SELECT 1 FROM shot_items WHERE id='reserved-raw-item'").fetchone() is None
    ref = "shot:reserved-shot" if kind == "shot" else "shot:another-owner/item:reserved-raw-item"
    claim = (kind, commits._reservation_identity(kind, ref))
    before = snapshot(service)
    # Exercise the internal occupancy check directly. The frozen artifact still
    # cannot carry complete native typed root records; no schema is overridden.
    with pytest.raises(CommitRejected) as error:
        commits._check_birth_destinations([claim])
    assert error.value.failure["details"]["reason"] == ("destination_occupied" if kind == "shot" else "identity_collision")
    commits._check_birth_destinations([("shot", "shot:free"), ("item", "free-raw-item")])
    assert snapshot(service) == before
