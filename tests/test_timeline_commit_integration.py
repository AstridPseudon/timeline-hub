"""Real Agent recipes through Runtime acceptance, independently of rendering.

Run explicitly with the integration lane and an Agent checkout/dependency stack.
Default neutral Runtime collection never imports Agent.
"""
from __future__ import annotations

import copy
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock
from types import SimpleNamespace

import pytest

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_baseline import verify_baseline
from precut_realm_fixture import load_precut_realm_fixture
from timeline_commit_film_fixture import (
    FilmFixture,
    refresh_copied_legacy_publication_receipts,
)

pytestmark = pytest.mark.integration


@pytest.fixture
def film(tmp_path):
    captured = load_precut_realm_fixture(tmp_path, variant="music-documents")
    pins = captured.pins
    fixture = FilmFixture(
        source_root=captured.copy_roots[0],
        duplicate_root=captured.copy_roots[1],
        project_id=pins["project_id"],
        timeline_id=pins["timeline_id"],
        parent_revision_id=pins["parent_revision_id"],
        media_ids=pins["media_ids"],
        transcript_document_id=pins["transcript_document_id"],
        text_binding_id=pins["text_binding_id"],
    )
    # Preserve the historical receipt bodies while keeping this copied
    # legacy baseline inside Runtime's real replay window before startup.
    refresh_copied_legacy_publication_receipts(fixture.duplicate_root, fixture.timeline_id)
    # The capture contains the original two clips, opaque data and config mirror.
    # Read its verified publication without replaying the retired writer.
    service = RuntimeService(fixture.duplicate_root)
    try:
        baseline = verify_baseline(
            service.store.conn, fixture.project_id, fixture.timeline_id,
            read_object=service.cas.read,
        )
        receipt = baseline["entries"][-1]["receipt"]
        publication = {"data": receipt["result"], "receipt": receipt}
        original_events = [tuple(row) for row in service.store.conn.execute(
            "SELECT * FROM timeline_events ORDER BY id",
        )]
    finally:
        service.close()
    return SimpleNamespace(fixture=fixture, publication=publication, original_events=original_events)


@pytest.fixture
def agent(film, astrid_importable, monkeypatch):
    class RendererUnavailable:
        def find_spec(self, fullname, path=None, target=None):
            if (fullname.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                     "astrid.sdk.authoring_render_preview",
                                     "astrid.core.timeline.compatibility", "composition",
                                     "remotion", "node")) or "scene" in fullname):
                raise AssertionError("save imported renderer: " + fullname)

    blocker = RendererUnavailable()
    monkeypatch.setattr(sys, "meta_path", [blocker, *sys.meta_path])

    def unavailable(*args, **kwargs):
        raise AssertionError("save evaluated a scene")

    # The seed publication happened before rendering became unavailable.
    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam
    monkeypatch.setattr(service_module, "evaluate_closure", unavailable)
    monkeypatch.setattr(visual_seam, "evaluate_closure", unavailable)

    from astrid.sdk.timeline.capture import capture_move, capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    return SimpleNamespace(move=capture_move, track=capture_track_create,
                           bundle=bundle_from_document,
                           provider=lambda: load_timeline_commit_provider("astrid"))


class Editing:
    def __init__(self, service, film, agent):
        self.service, self.film, self.agent = service, film, agent
        self.project = film.fixture.project_id
        self.timeline = film.fixture.timeline_id
        self.path = f"/v1/projects/{self.project}/timelines/{self.timeline}/commit"

    def head(self):
        head = self.service.get_project_timeline(self.project, self.timeline)
        return {"revision_id": head["head_revision_id"],
                "publication_id": head["head_publication_id"]}

    def document(self, revision=None):
        return self.service._timeline_commits()[0].revision_closure(
            self.project, self.timeline, revision or self.head()["revision_id"],
        )

    def body(self, commands, base=None):
        base = base or self.head()
        return {"api_version": 1, "project_id": self.project, "timeline_id": self.timeline,
                "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
                "commands": copy.deepcopy(commands), "source": {"via": "python"},
                "rationale": "real renderer-free integration"}

    def move(self, clip, on, *, document=None):
        return self.agent.move(self.agent.bundle(document or self.document()), "parent/clip:" + clip, on)

    def commit(self, body, key):
        return self.service.commit_timeline(
            self.project, self.timeline, body, idempotency_key=key, publisher="integration-editor",
            invocation_path=self.path, authorize=lambda: None,
        )

    def history(self):
        return self.service.list_timeline_commits(self.project, self.timeline, authorize=lambda: None)["items"]

    def assert_baseline(self):
        baselines = [entry for entry in self.history() if entry["intent"] == "legacy_unknown"]
        assert len(baselines) == 2
        baseline = baselines[-1]
        assert baseline["intent"] == "legacy_unknown"
        assert baseline["records"] is None
        assert baseline["publication_id"] == self.film.publication["receipt"]["receipt_id"]
        assert baseline["receipt"] == self.film.publication["receipt"]
        events = [tuple(row) for row in self.service.store.conn.execute(
            "SELECT * FROM timeline_events ORDER BY id",
        )]
        assert events[:len(self.film.original_events)] == self.film.original_events

    def assert_readback(self, accepted):
        data = accepted["data"]
        document = data["canonical_document"]
        revision = document["parent_revision"]["revision_id"]
        assert data["accepted_revision_id"] == revision
        assert accepted["receipt"]["result"] == data
        assert self.document(revision) == document
        parent = self.service.get_project_parent_composition_revision(self.project, self.timeline, revision)
        assert parent["revision_id"] == revision
        assert parent["payload"] == document["parent_revision"]["payload"]
        assert parent["content_digest"] == document["parent_revision"]["content_digest"]
        for image in document["shot_revisions"]:
            row = self.service.store.conn.execute("SELECT payload_json FROM shot_revisions WHERE id=?",
                                                  (image["revision_id"],)).fetchone()
            assert json.loads(row[0]) == image["payload"]
        for image in document["internal_timeline_revisions"]:
            row = self.service.store.conn.execute("SELECT payload_json FROM internal_timeline_revisions WHERE id=?",
                                                  (image["revision_id"],)).fetchone()
            assert json.loads(row[0]) == image["payload"]


@pytest.fixture
def editing(film, agent):
    service = RuntimeService(film.fixture.duplicate_root)
    try:
        service.register_timeline_commit_provider(agent.provider())
        result = Editing(service, film, agent)
        result.assert_baseline()
        yield result
    finally:
        service.close()


def inverse(publication):
    return {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
            "args": {"publications": [publication]}}


def positions(document):
    return {row["id"]: row["at"] for row in document["parent_revision"]["payload"]["clips"]}


def assert_json_equal(actual, expected):
    if type(actual) in (int, float) and type(expected) in (int, float):
        assert actual == expected
        return
    assert type(actual) is type(expected)
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_json_equal(actual[key], expected[key])
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for actual_item, expected_item in zip(actual, expected):
            assert_json_equal(actual_item, expected_item)
    else:
        assert actual == expected


def rows(service):
    # Rejection/retry must leave the entire durable store unchanged, including
    # projections, sequence allocation, receipts, retained inputs and history.
    return tuple(service.store.conn.iterdump())


def test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip(editing):
    base, document = editing.head(), editing.document()
    first_body = editing.body([editing.move("music-bed", 1, document=document)], base)
    disjoint = editing.body([editing.move("music-other", 2, document=document)], base)
    conflicting = editing.body([editing.move("music-bed", 3, document=document)], base)
    first = editing.commit(first_body, "move-first")
    second = editing.commit(disjoint, "move-disjoint")
    assert first["data"]["status"] == "accepted"
    assert second["data"]["status"] == "rebased"
    assert positions(second["data"]["canonical_document"]) == {"music-bed": 1, "music-other": 2}
    editing.assert_readback(first)  # Exact old accepted closure after a newer head.
    editing.assert_readback(second)
    before = rows(editing.service)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(conflicting, "move-conflict")
    assert error.value.status == 409
    assert error.value.details["status"] == "conflict"
    assert rows(editing.service) == before
    history = editing.history()
    assert len(history) == 4
    assert [entry["publication_id"] for entry in history[-2:]] == [
        first["receipt"]["receipt_id"], second["receipt"]["receipt_id"],
    ]
    original = history[-2]["records"]["commands"][0]
    assert original["command"] == first["data"]["commands"][0]
    assert original["writes"] and original["reads"] and original["bindings"]
    assert original["selections"] and original["dependencies"]
    editing.assert_baseline()


def test_real_door_concurrent_disjoint_moves_accept_and_rebase(film, agent, tmp_path, monkeypatch):
    world = _start_door(film, tmp_path)
    try:
        editing = Editing(world.daemon.service, film, agent)
        editing.assert_baseline()
        base, document = editing.head(), editing.document()
        requests = [
            (editing.body([editing.move("music-bed", 1, document=document)], base), "door-concurrent-bed"),
            (editing.body([editing.move("music-other", 2, document=document)], base), "door-concurrent-other"),
        ]

        provider_type = type(world.daemon.service._timeline_commit_provider)
        provider_commit = provider_type.commit
        preparation_barrier = Barrier(2)
        provider_keys, provider_lock = [], Lock()

        def overlap_provider(provider, context, port):
            with provider_lock:
                provider_keys.append(context["idempotency_key"])
            preparation_barrier.wait(timeout=10)
            return provider_commit(provider, context, port)

        monkeypatch.setattr(provider_type, "commit", overlap_provider)
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(_post_door, world, editing.path, body, key)
                       for body, key in requests]
            results = [future.result(timeout=30) for future in futures]

        assert sorted(provider_keys) == sorted(key for _, key in requests)
        assert sorted(result["data"]["status"] for result in results) == ["accepted", "rebased"]
        assert len({result["receipt"]["receipt_id"] for result in results}) == 2
        for result in results:
            editing.assert_readback(result)

        final = editing.document()
        assert positions(final) == {"music-bed": 1, "music-other": 2}
        history = editing.history()
        assert len(history) == 4
        concurrent_history = history[-2:]
        assert {entry["publication_id"] for entry in concurrent_history} == {
            result["receipt"]["receipt_id"] for result in results
        }
        assert len({entry["revision_id"] for entry in concurrent_history}) == 2
        ledger = world.daemon.service.store.conn.execute(
            "SELECT idempotency_key, txn_id FROM command_idempotency "
            "WHERE command_kind='timeline.commit' AND idempotency_key IN (?, ?) "
            "ORDER BY idempotency_key",
            tuple(key for _, key in requests),
        ).fetchall()
        assert [(row["idempotency_key"], row["txn_id"]) for row in ledger] == sorted(
            (key, next(result["receipt"]["receipt_id"] for result in results
                       if result["receipt"]["idempotency_key"] == key))
            for _, key in requests
        )
    finally:
        world.stop()


def test_real_inverse_preserves_newer_disjoint_work_and_original_recorders(editing):
    original = editing.document()
    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "undo-target")
    second = editing.commit(editing.body([editing.move("music-other", 2)]), "undo-disjoint")
    stored = copy.deepcopy(editing.history())
    undone = editing.commit(editing.body([inverse(first["receipt"]["receipt_id"])]), "undo-target-publication")
    assert positions(undone["data"]["canonical_document"]) == {"music-bed": 0, "music-other": 2}
    parent = undone["data"]["canonical_document"]["parent_revision"]["payload"]
    original_parent = original["parent_revision"]["payload"]
    second_parent = second["data"]["canonical_document"]["parent_revision"]["payload"]
    # Baseline plus B.at omitted B's intentional app.astrid fixed_start/for writes.
    expected = copy.deepcopy(second_parent)
    for container, baseline in ((expected, original_parent),
                                (expected["config"], original_parent["config"])):
        target = next(row for row in baseline["clips"] if row["id"] == "music-bed")
        for index, row in enumerate(container["clips"]):
            if row["id"] == "music-bed":
                container["clips"][index] = copy.deepcopy(target)
    assert_json_equal(parent, expected)
    for container, accepted in ((parent, second_parent),
                                (parent["config"], second_parent["config"])):
        assert_json_equal(next(row for row in container["clips"] if row["id"] == "music-other"),
                          next(row for row in accepted["clips"] if row["id"] == "music-other"))
    assert undone["data"]["canonical_document"]["shot_revisions"] == original["shot_revisions"]
    assert undone["data"]["canonical_document"]["internal_timeline_revisions"] == original["internal_timeline_revisions"]
    assert editing.history()[:-1] == stored
    assert editing.history()[-1]["records"]["undo_of"] == [first["receipt"]["receipt_id"]]
    editing.assert_readback(first)
    editing.assert_readback(second)
    editing.assert_readback(undone)


def test_real_same_value_publication_is_recorded_and_blocks_older_undo(editing):
    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "same-target")
    same = editing.commit(editing.body([editing.move("music-bed", 1)]), "same-value")
    assert same["data"]["accepted_revision_id"] == first["data"]["accepted_revision_id"]
    assert same["receipt"]["receipt_id"] != first["receipt"]["receipt_id"]
    records = editing.history()[-1]["records"]["commands"]
    assert any(write["ref"] == "parent/clip:music-bed" and write["path"] == ["at"]
               and write["before"] == write["after"] for write in records[0]["writes"])
    before = rows(editing.service)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(editing.body([inverse(first["receipt"]["receipt_id"])]), "same-value-undo-conflict")
    assert error.value.status == 409
    assert error.value.details["status"] == "conflict"
    assert rows(editing.service) == before
    assert len(editing.history()) == 4
    editing.assert_readback(same)


@pytest.mark.parametrize("later", ["overwritten", "returned"])
def test_real_inverse_refuses_when_target_was_overwritten_or_returned(editing, later):
    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "undo-stale-target")
    editing.commit(editing.body([editing.move("music-bed", 2)]), "undo-overwrite")
    if later == "returned":
        editing.commit(editing.body([editing.move("music-bed", 1)]), "undo-return")
    before, length = rows(editing.service), len(editing.history())
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(editing.body([inverse(first["receipt"]["receipt_id"])]), "undo-stale-conflict")
    assert error.value.status == 409
    assert error.value.details["status"] == "conflict"
    assert rows(editing.service) == before
    assert len(editing.history()) == length


def test_real_inverse_dry_run_and_exact_retry_write_only_the_undo_once(editing, monkeypatch):
    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "undo-dry-target")
    undo = editing.body([inverse(first["receipt"]["receipt_id"])])
    before = rows(editing.service)
    preview = editing.commit({**copy.deepcopy(undo), "dry_run": True}, "undo-dry-run")
    assert preview["data"]["status"] == "preview"
    assert preview["receipt"] is None
    assert rows(editing.service) == before
    undone = editing.commit(copy.deepcopy(undo), "undo-real")
    after = rows(editing.service)

    def forbidden(self, context, port):
        raise AssertionError("exact retry executed the semantic provider")

    with monkeypatch.context() as retry:
        retry.setattr(type(editing.service._timeline_commit_provider), "commit", forbidden)
        assert editing.commit(copy.deepcopy(undo), "undo-real") == undone
    assert rows(editing.service) == after
    assert editing.history()[-1]["records"]["undo_of"] == [first["receipt"]["receipt_id"]]


def test_real_track_create_and_inverse_keep_complete_film_closure(editing):
    original = editing.document()
    track = {"id": "new-audio", "kind": "audio", "extension": {"opaque": [None, "kept"]}}
    command = editing.agent.track(editing.agent.bundle(original), "parent", track)
    accepted = editing.commit(editing.body([command]), "track-create")
    assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["tracks"][-1] == track
    assert editing.history()[-1]["records"]["commands"][0]["created"]
    undone = editing.commit(editing.body([inverse(accepted["receipt"]["receipt_id"])]), "track-undo")
    restored = undone["data"]["canonical_document"]
    assert restored["parent_revision"]["payload"] == original["parent_revision"]["payload"]
    assert restored["parent_revision"]["content_digest"] == original["parent_revision"]["content_digest"]
    for family in ("shot_revisions", "internal_timeline_revisions", "dependency_manifest"):
        assert restored[family] == original[family]
    editing.assert_readback(accepted)
    editing.assert_readback(undone)


def _start_door(film, tmp_path):
    from runtime_protocol.daemon import RuntimeDaemon
    from runtime_protocol.door import DoorConfig
    from tests.door_helpers import HOSTED, DoorWorld

    credential = tmp_path / "product.json"
    daemon = RuntimeDaemon(
        film.fixture.duplicate_root, support_root=tmp_path / "support", authoring_profile="astrid",
        door=DoorConfig(origin=HOSTED, port=0, credential_file=credential),
    ).start()
    world = DoorWorld(tmp_path, daemon, credential)
    world.provision()
    handshake = world.call("/api/runtime/v1/handshake", "POST", body=b"{}",
                           headers={"Content-Type": "application/json"})
    assert handshake.status == 200, handshake.body
    return world


def _post_door(world, path, body, key):
    response = world.call("/api/runtime" + path, "POST", body=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json", "Idempotency-Key": key})
    assert response.status == 200, response.body
    return response.json()


def test_real_door_commit_admission_checks_origin_auth_and_project_scope(film, agent, tmp_path):
    world = _start_door(film, tmp_path)
    try:
        evil_origin = "https://evil.test"
        edit = Editing(world.daemon.service, film, agent)
        edit.assert_baseline()
        body = edit.body([edit.move("music-bed", 1)])
        encoded = json.dumps(body).encode()
        path = "/api/runtime" + edit.path
        headers = {"Content-Type": "application/json", "Idempotency-Key": "door-admission"}
        before = rows(edit.service)

        refused = world.call(path, "POST", origin=evil_origin, body=encoded, headers=headers)
        assert refused.status == 403
        assert refused.json() == {"error": "hosted_origin_required"}

        refused = world.call(path, "POST", body=encoded,
                             headers={**headers, "Authorization": f"Bearer {world.product_token}"})
        assert refused.status == 403
        assert refused.json() == {"error": "browser_credentials_forbidden"}

        foreign = copy.deepcopy(body)
        foreign["project_id"] = "foreign-project"
        refused = world.call(path, "POST", body=json.dumps(foreign).encode(),
                             headers={**headers, "Idempotency-Key": "door-foreign-project"})
        assert refused.status == 409
        assert refused.json()["code"] == "conflict"
        assert rows(edit.service) == before

        accepted = _post_door(world, edit.path, body, "door-admission")
        assert accepted["data"]["status"] == "accepted"
    finally:
        world.stop()


def test_real_door_lost_ack_restart_exact_retry_never_executes_provider(film, agent, tmp_path, monkeypatch):
    def start():
        return _start_door(film, tmp_path)

    post = _post_door

    world = start()
    try:
        edit = Editing(world.daemon.service, film, agent)
        edit.assert_baseline()
        body = edit.body([edit.move("music-bed", 1)])
        frozen = json.dumps(body, sort_keys=True)
        accepted = post(world, edit.path, body, "door-lost-ack")
        # No acknowledgement is applied to a client session. Its exact flight
        # survives while a different author advances the head before shutdown.
        newer = edit.commit(edit.body([edit.move("music-other", 2)]), "door-newer-disjoint")
        original_history = copy.deepcopy(edit.history())
        old_instance = world.daemon.instance_id
        provider_type = type(world.daemon.service._timeline_commit_provider)
    finally:
        world.stop()

    world = start()
    try:
        assert world.daemon.instance_id != old_instance
        edit = Editing(world.daemon.service, film, agent)
        assert edit.head()["revision_id"] == newer["data"]["accepted_revision_id"]
        before = rows(edit.service)

        def forbidden(self, context, port):
            raise AssertionError("exact retry executed the semantic provider")

        with monkeypatch.context() as retry:
            retry.setattr(provider_type, "commit", forbidden)
            replayed = post(world, edit.path, json.loads(frozen), "door-lost-ack")
        assert replayed == accepted
        assert json.dumps(body, sort_keys=True) == frozen
        assert rows(edit.service) == before
        assert edit.history() == original_history
        edit.assert_readback(replayed)
        edit.assert_readback(newer)
        # A changed request under the same identity is refused without writes.
        changed = copy.deepcopy(body)
        changed["rationale"] = "changed identity"
        refused = world.call("/api/runtime" + edit.path, "POST", body=json.dumps(changed).encode(),
                             headers={"Content-Type": "application/json", "Idempotency-Key": "door-lost-ack"})
        assert refused.status == 409, refused.body
        assert refused.json()["details"]["reason"] == "idempotency_mismatch"
        assert rows(edit.service) == before
        undone = post(world, edit.path, edit.body([inverse(accepted["receipt"]["receipt_id"])]), "door-undo")
        assert positions(undone["data"]["canonical_document"]) == {"music-bed": 0, "music-other": 2}
        assert edit.history()[:-1] == original_history
        edit.assert_readback(undone)
        edit.assert_baseline()
    finally:
        world.stop()


def test_real_restart_undo_then_recorder_tamper_fails_closed(film, agent, tmp_path):
    from runtime_protocol.errors import RealmAdmissionError
    from runtime_protocol.util import canonical_json

    world = _start_door(film, tmp_path)
    try:
        edit = Editing(world.daemon.service, film, agent)
        edit.assert_baseline()
        accepted = _post_door(world, edit.path, edit.body([edit.move("music-bed", 1)]), "restart-undo-target")
    finally:
        world.stop()

    world = _start_door(film, tmp_path)
    try:
        edit = Editing(world.daemon.service, film, agent)
        publication = accepted["receipt"]["receipt_id"]
        undone = _post_door(world, edit.path, edit.body([inverse(accepted["receipt"]["receipt_id"])]), "restart-undo")
        edit.assert_readback(undone)
        assert edit.history()[-1]["records"]["undo_of"] == [publication]
        # Tamper the durable recorder of the pre-restart edit; the live store must refuse it.
        conn = world.daemon.service.store.conn
        records = json.loads(conn.execute(
            "SELECT records_json FROM timeline_commit_history WHERE publication_id=?", (publication,),
        ).fetchone()[0])
        records["undo_of"] = ["other-publication"]
        conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?",
                     (canonical_json(records), publication))
        commits = world.daemon.service._timeline_commits()[0]
        assert any(error["id"] == publication for error in commits.integrity_errors())
    finally:
        world.stop()

    with pytest.raises(RealmAdmissionError) as error:
        RuntimeService(film.fixture.duplicate_root)
    assert not error.value.details["ok"]
    assert any(item["table"] == "timeline_commit_history" for item in error.value.details["checks"]["revisions"]["errors"])
