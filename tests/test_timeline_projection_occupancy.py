"""Occupied mutable shot destinations refuse before any persistence.

Host-boundary candidates use the frozen schema and API-built accepted history.
Real Agent move/restore behavior is also covered by the integration neighbours.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_store import TimelineCommitStore, digest, request_identity
from test_timeline_commit_acceptance import (
    context, realm, validate_prepared,  # noqa: F401 (shared API-built fixture)
)


def snapshot(service):
    return tuple(service.store.conn.iterdump())


def new_timeline(service, commits, project, timeline):
    service.create_timeline(project, timeline, name=timeline, idempotency_key=timeline)
    return commits.bootstrap(project, timeline, authorize=lambda: None)


def proposal(service, commits, project, timeline, key, *, shots=None):
    head = commits.head(project, timeline)
    ctx = context(service, project, head, key, op="fixture.projection")
    ctx["request"]["timeline_id"] = timeline
    ctx["invocation"]["body"] = copy.deepcopy(ctx["request"])
    ctx["request_hash"] = request_identity(ctx)
    record = {"ordinal": 0, "command": copy.deepcopy(ctx["request"]["commands"][0]),
              "writes": [], "reads": [], "selections": [], "bindings": [], "created": [],
              "dependencies": [], "derived_writes": []}
    value = {"expected_head": head, "records": {"schema_version": 1, "commands": [record],
             "undo_of": [], "restored_from": None}, "id_map": {}, "semantic_events": [],
             "provider_version": "projection-fixture", "compiler_version": "projection-fixture"}
    document = commits.revision_closure(project, timeline, head["revision_id"])
    document["parent_revision"]["revision_id"] = key
    document["parent_revision"]["payload"]["fixture_label"] = key
    if shots is not None:
        document["shot_revisions"] = [copy.deepcopy(s) for s, _ in shots]
        document["internal_timeline_revisions"] = [copy.deepcopy(i) for _, i in shots]
        document["parent_revision"]["payload"]["occurrences"] = [{
            "occurrence_id": "occ-" + str(n), "shot_id": s["shot_id"], "shot_revision_id": s["revision_id"],
            "placement": {"start_ms": n * 1000}, "duration_ms": 1000, "track": "picture",
            "source_offset": 0, "speed": 1, "transform": {}, "gain": 1, "muted": False, "provenance": {},
        } for n, (s, _) in enumerate(shots)]
        document["dependency_manifest"]["shots"] = [
            {k: s[k] for k in ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest")}
            for s, _ in shots]
        document["dependency_manifest"]["internal_timelines"] = [
            {k: i[k] for k in ("timeline_id", "revision_id", "content_digest")} for _, i in shots]
    value["canonical_document"] = document
    refresh(value)
    return ctx, value


def refresh(value):
    document = value["canonical_document"]
    document["parent_revision"]["content_digest"] = digest(document["parent_revision"]["payload"])
    value["document_digest"] = digest(document)


def publish_source_items(service, film):
    """Publish real source items through the normal parent-composition API."""
    project, timeline = film.fixture.project_id, film.fixture.timeline_id
    head = service.get_project_timeline(project, timeline)["head_revision_id"]
    document = service._timeline_commits()[0].revision_closure(project, timeline, head)
    shot_revisions, internal_revisions = [], []
    parent = copy.deepcopy(document["parent_revision"]["payload"])
    for shot_id in ("shot-2", "shot-3"):
        source = next(row for row in document["shot_revisions"] if row["shot_id"] == shot_id)
        internal = next(row for row in document["internal_timeline_revisions"]
                        if row["revision_id"] == source["internal_timeline_revision_id"])
        item_id = "rt08-source-item-" + shot_id.removeprefix("shot-")
        item = {"item_id": item_id, "media_id": film.fixture.media_ids[0],
                "source_frame": 7, "metadata": {"opaque": [None, {"keep": True}],
                                                    "source_item_id": item_id}}
        payload = copy.deepcopy(source["payload"])
        payload["items"] = [item]
        internal_revision_id = "rt08-source-internal-" + shot_id.removeprefix("shot-")
        shot_revision_id = "rt08-source-revision-" + shot_id.removeprefix("shot-")
        payload["internal_timeline_revision_id"] = internal_revision_id
        shot_revisions.append({"shot_id": shot_id, "revision_id": shot_revision_id,
                               "internal_timeline_revision_id": internal_revision_id,
                               "payload": payload})
        internal_revisions.append({"timeline_id": internal["timeline_id"],
                                   "revision_id": internal_revision_id,
                                   "payload": copy.deepcopy(internal["payload"])})
        for occurrence in parent["occurrences"]:
            if occurrence["shot_id"] == shot_id:
                occurrence["shot_revision_id"] = shot_revision_id
    return service.publish_parent_composition(
        project, timeline,
        {"project_id": project, "timeline_id": timeline, "expected_head": head,
         "parent_revision_id": "rt08-source-items-parent", "parent_composition": parent,
         "shot_revisions": shot_revisions, "internal_timeline_revisions": internal_revisions},
        idempotency_key="rt08-source-items",
    )


def image(shot, revision, *, items=(), archived=False):
    internal_payload = {"clips": [], "tracks": []}
    internal = {"timeline_id": "shot:" + shot, "revision_id": revision + "-internal",
                "payload": internal_payload, "content_digest": digest(internal_payload)}
    payload = {"name": shot, "items": list(items), "archived": archived,
               "metadata": {"opaque": [None]}, "internal_timeline_revision_id": internal["revision_id"]}
    return ({"shot_id": shot, "revision_id": revision, "payload": payload, "content_digest": digest(payload),
             "internal_timeline_revision_id": internal["revision_id"]}, internal)


def accept(commits, pair):
    return commits.accept(*pair, authorize=lambda: None)


def refuses(service, commits, pair, monkeypatch, *, reason="destination_occupied", preview=False):
    before = snapshot(service)
    with monkeypatch.context() as patch:
        patch.setattr(commits, "_persist_closure", lambda *_: pytest.fail("projection preflight wrote a revision"))
        with pytest.raises(CommitRejected) as error:
            (commits.preview if preview else commits.accept)(*pair, authorize=lambda: None)
    assert error.value.failure["details"]["reason"] == reason
    assert error.value.failure["http_status"] == 409
    assert error.value.failure["message"] == reason
    assert error.value.failure["details"] == {"status": "refused", "reason": reason,
                                             "base": None, "current": None, "conflicts": []}
    assert snapshot(service) == before  # projections, heads, history, receipts, events and sequences


def media_item(service, project, identity):
    media = service.ingest(project, b"projection-media", media_type="video/mp4",
                           idempotency_key="projection-media")["data"]["object_id"]
    return {"item_id": identity, "media_id": media, "metadata": {"opaque": None}}


def with_media(pair, item):
    document = pair[1]["canonical_document"]
    document["dependency_manifest"]["media"] = [{"media_id": item["media_id"], "content_digest": item["media_id"]}]
    refresh(pair[1])
    return pair


@pytest.mark.parametrize("archived", [False, True])
@pytest.mark.parametrize("foreign", [False, True])
@pytest.mark.parametrize("preview", [False, True])
def test_occupied_destination_refuses_before_any_write(realm, monkeypatch, archived, foreign, preview):
    service, commits, project, _, _ = realm
    owner = service.create_project({"slug": "foreign", "name": "Private owner"})["id"] if foreign else project
    new_timeline(service, commits, owner, "other")
    item = media_item(service, owner, "occupant-item")
    accept(commits, with_media(proposal(service, commits, owner, "other", "owner-parent",
                                      shots=[image("occupied", "owner-shot", items=[item], archived=archived)]), item))
    candidate = proposal(service, commits, project, "main", "intruder-parent",
                         shots=[image("free-first", "free-shot"), image("occupied", "intruder-shot")])
    # A free earlier image must not be persisted before the occupied one is checked.
    if preview:
        candidate[0]["request"]["dry_run"] = True
        candidate[0]["invocation"]["body"] = copy.deepcopy(candidate[0]["request"])
        candidate[0]["request_hash"] = request_identity(candidate[0])
    refuses(service, commits, candidate, monkeypatch, preview=preview)


def test_free_destination_preview_and_current_input_updates_remain_legal(realm):
    service, commits, project, _, _ = realm
    pair = proposal(service, commits, project, "main", "preview-parent", shots=[image("own", "preview-shot")])
    pair[0]["request"]["dry_run"] = True
    pair[0]["invocation"]["body"] = copy.deepcopy(pair[0]["request"])
    pair[0]["request_hash"] = request_identity(pair[0])
    before = snapshot(service)
    assert commits.preview(*pair, authorize=lambda: None)["receipt"] is None
    assert snapshot(service) == before
    first = accept(commits, proposal(service, commits, project, "main", "first", shots=[image("own", "first-shot")]))
    second = accept(commits, proposal(service, commits, project, "main", "second", shots=[image("own", "second-shot")]))
    assert first["data"]["status"] == second["data"]["status"] == "accepted"
    assert service.store.integrity_report()["ok"]


def test_two_acceptors_race_for_one_destination(realm):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    pairs = [proposal(service, commits, project, timeline, "race-" + timeline,
                      shots=[image("raced-shot", "shot-" + timeline)]) for timeline in ("main", "other")]
    barrier = Barrier(2)

    def run(pair):
        barrier.wait(timeout=10)
        with service.store._mutex:
            before = snapshot(service)
            try:
                return accept(commits, pair)["data"]["status"]
            except CommitRejected as error:
                assert snapshot(service) == before
                return error.failure["details"]["reason"]

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(run, pairs)) == ["accepted", "destination_occupied"]
    assert service.store.conn.execute("SELECT COUNT(*) FROM shot_revisions").fetchone()[0] == 1
    assert commits.integrity_errors() == []


def test_retry_precedes_guard_after_restart_and_head_advance(realm, monkeypatch):
    service, commits, project, _, root = realm
    pair = proposal(service, commits, project, "main", "first", shots=[image("own", "first-shot")])
    first = accept(commits, pair)
    accept(commits, proposal(service, commits, project, "main", "advance"))
    service.close()
    restarted = RuntimeService(root)
    try:
        store = TimelineCommitStore(restarted.store, validate_prepared=validate_prepared)

        def tripwire(*_):
            pytest.fail("exact retry inspected the candidate")

        monkeypatch.setattr(store, "_check_shot_destinations", tripwire)
        monkeypatch.setattr(store, "_validate", tripwire)
        before = snapshot(restarted)
        assert accept(store, pair) == first
        changed = copy.deepcopy(pair)
        changed[0]["request"]["label"] = "changed payload"
        changed[0]["invocation"]["body"] = copy.deepcopy(changed[0]["request"])
        changed[0]["request_hash"] = request_identity(changed[0])
        with pytest.raises(CommitRejected) as error:
            accept(store, changed)
        assert error.value.failure["details"]["reason"] == "idempotency_mismatch"
        assert snapshot(restarted) == before
    finally:
        restarted.close()


def inverse_request(pair, publications):
    command = {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
               "args": {"publications": publications}}
    pair[0]["request"]["commands"] = [command]
    pair[0]["invocation"]["body"] = copy.deepcopy(pair[0]["request"])
    pair[0]["request_hash"] = request_identity(pair[0])
    pair[1]["records"]["commands"][0]["command"] = copy.deepcopy(command)
    pair[1]["records"]["undo_of"] = publications
    return pair


def seed_slot(service, commits, project, *, proof=True):
    source = image("source", "source-v1")
    accept(commits, proposal(service, commits, project, "main", "source-parent", shots=[source]))
    slot = proposal(service, commits, project, "main", "slot-parent", shots=[image("slot", "slot-v1")])
    slot[1]["records"]["commands"][0]["writes"] = [{
        "ref": "occurrence:occ-0/clip:clip", "path": ["at"],
        "before": {"state": "present", "value": 0}, "after": {"state": "present", "value": 1},
    }]
    if proof:
        record = slot[1]["records"]["commands"][0]
        record["bindings"] = [{"key": "move.owner", "ref": "occurrence:occ-0", "policy": "fixed", "dependencies": []}]
        record["reads"] = [{"ref": "occurrence:occ-0/shot", "path": ["shot_id"],
                            "state": {"state": "present", "value": "source"}}]
    result = accept(commits, slot)
    return source, result


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
        refuses(service, commits, pair, monkeypatch)


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
    refuses(service, commits, attack, monkeypatch)


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


def test_external_source_read_does_not_authorize_mutable_overwrite(realm, monkeypatch):
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


def test_exact_immutable_reuse_does_not_write_occupied_projection(realm):
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    source = image("source", "source-v1")
    accept(commits, proposal(service, commits, project, "other", "external-source-parent", shots=[source]))
    before = [tuple(r) for r in service.store.conn.execute("SELECT * FROM project_shots")]
    accepted = accept(commits, proposal(service, commits, project, "main", "exact-source-reuse", shots=[source]))
    assert accepted["data"]["canonical_document"]["shot_revisions"] == [source[0]]
    assert [tuple(r) for r in service.store.conn.execute("SELECT * FROM project_shots")] == before
    assert service.store.conn.execute("SELECT COUNT(*) FROM shot_revisions").fetchone()[0] == 1


@pytest.fixture
def shared_editing(film, request):
    from test_timeline_commit_integration import Editing

    service = RuntimeService(film.fixture.duplicate_root)
    try:
        # HOST-BOUNDARY source acceptance only: preserve the full raw closure
        # and persist the repeated occurrence before installing Agent tripwires.
        # All measured moves/restores/rematerialization use the real Agent.
        project, timeline = film.fixture.project_id, film.fixture.timeline_id
        commits = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
        commits.install_verified_baseline(project, timeline, authorize=lambda: None)
        document = commits.revision_closure(project, timeline, film.publication["data"]["revision_id"])
        pair = proposal(service, commits, project, timeline, "shared-shot-baseline")
        pair[1]["canonical_document"] = document
        document["parent_revision"]["revision_id"] = "shared-shot-baseline"
        parent = document["parent_revision"]["payload"]
        before = copy.deepcopy(parent["occurrences"])
        repeated = copy.deepcopy(parent["occurrences"][-1])
        repeated.update(occurrence_id="repeated-third", placement={"start_ms": 6000, "track": "picture"})
        parent["occurrences"].append(repeated)
        pair[1]["records"]["commands"][0]["writes"] = [{
            "ref": "parent", "path": ["occurrences"],
            "before": {"state": "present", "value": before},
            "after": {"state": "present", "value": copy.deepcopy(parent["occurrences"])},
        }]
        refresh(pair[1])
        accept(commits, pair)
        agent = request.getfixturevalue("agent")  # Disable rendering after source acceptance.
        service.register_timeline_commit_provider(agent.provider())
        yield Editing(service, film, agent)
    finally:
        service.close()


# Reuse renderer-disabled actual-provider fixtures; Agent imports remain inside
# their explicitly selected integration fixtures.
from test_timeline_commit_integration import (  # noqa: E402,F401
    Editing, _start_door, agent, film, inverse, rows,
)


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


@pytest.mark.integration
def test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy(
    film, agent, tmp_path,
):
    from runtime_protocol.errors import RuntimeErrorBase

    setup = RuntimeService(film.fixture.duplicate_root)
    try:
        publish_source_items(setup, film)
    finally:
        setup.close()

    world = _start_door(film, tmp_path)
    try:
        editing = Editing(world.daemon.service, film, agent)
        owner = "occurrence:occurrence-3/clip:clip-3"
        original = editing.document()
        source_item = next(
            item for shot in original["shot_revisions"] if shot["shot_id"] == "shot-3"
            for item in shot["payload"]["items"]
        )
        first_command = editing.agent.move(editing.agent.bundle(original), owner, 3.5)
        first = editing.commit(editing.body([first_command]), "rt08-item-first")
        record = editing.history()[-1]["records"]["commands"][0]
        source_pin = next(dep["pin"] for dep in record["dependencies"]
                          if dep["key"].startswith("materialization.source:"))
        owner_binding = next(binding for binding in record["bindings"]
                             if binding["key"].startswith("materialization.owner:"))
        physical_items = source_pin["source"]["item_id_map"]
        assert source_pin["source"]["shot_id"] == "shot-3"
        assert owner_binding["ref"] == "occurrence:occurrence-3"
        assert set(physical_items) == {source_item["item_id"]}
        physical_shot = next(
            occurrence["shot_id"]
            for occurrence in first["data"]["canonical_document"]["parent_revision"]["payload"]["occurrences"]
            if occurrence["occurrence_id"] == "occurrence-3"
        )
        physical = next(shot for shot in first["data"]["canonical_document"]["shot_revisions"]
                        if shot["shot_id"] == physical_shot)
        assert physical_shot != source_pin["source"]["shot_id"]
        assert {item["item_id"] for item in physical["payload"]["items"]} == set(physical_items.values())
        assert physical["payload"]["items"][0]["metadata"]["opaque"] == [None, {"keep": True}]

        world.stop()
        world = _start_door(film, tmp_path)
        editing = Editing(world.daemon.service, film, agent)
        restored = editing.commit(editing.body([inverse(first["receipt"]["receipt_id"])]), "rt08-item-restore")
        assert next(occurrence["shot_id"] for occurrence in
                    restored["data"]["canonical_document"]["parent_revision"]["payload"]["occurrences"]
                    if occurrence["occurrence_id"] == "occurrence-3") == "shot-3"
        second_command = editing.agent.move(editing.agent.bundle(editing.document()), owner, 3.6)
        second = editing.commit(editing.body([second_command]), "rt08-item-reuse")
        second_record = editing.history()[-1]["records"]["commands"][0]
        second_pin = next(dep["pin"] for dep in second_record["dependencies"]
                          if dep["key"].startswith("materialization.source:"))
        assert second_pin["source"] == source_pin["source"]
        assert second["data"]["id_map"] == first["data"]["id_map"]

        candidate_bundle = editing.agent.bundle(editing.document())
        candidate_command = editing.agent.move(
            candidate_bundle, "occurrence:occurrence-2/clip:clip-2", 2.5,
        )
        from astrid.sdk.timeline.commands import execute

        candidate = execute(candidate_bundle, [candidate_command])
        occupied_item = next(ref.rsplit("/item:", 1)[1] for ref in candidate.id_map
                             if "/item:" in ref)
        project, occupier = film.fixture.project_id, "rt08-unrelated-item-occupier"
        world.daemon.service.create_project_shot(
            project, {"shot_id": occupier, "name": "Unrelated item owner"},
            idempotency_key="rt08-occupier-shot",
        )
        world.daemon.service.add_shot_item(
            project, occupier,
            {"item_id": occupied_item, "media_id": film.fixture.media_ids[0],
             "metadata": {"unrelated": True}},
            idempotency_key="rt08-occupier-item",
        )
        before = rows(world.daemon.service)
        with pytest.raises(RuntimeErrorBase) as error:
            editing.commit(editing.body([candidate_command]), "rt08-global-item-conflict")
        assert error.value.details["reason"] == "identity_collision"
        assert rows(world.daemon.service) == before
    finally:
        world.stop()

