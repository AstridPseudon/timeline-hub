from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from runtime_protocol import timeline_commit as abi
from runtime_protocol.errors import ProtocolError, ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit import CommitRejected, StaleHead
from runtime_protocol.timeline_commit_store import TimelineCommitStore, digest, request_identity
from runtime_protocol.util import canonical_json


def validate_prepared(prepared):
    # Consume the wire owner's actual schema; never mirror its DTOs in fixtures.
    root = Path(abi.__file__).resolve().parents[1] / "contract/schemas"
    schemas = {p.name: json.loads(p.read_text()) for p in root.glob("*.json")}
    base = "https://astrid.haus/workspace/v1/schemas/"
    registry = Registry().with_resources((base + name, Resource.from_contents(value, default_specification=DRAFT202012))
                                         for name, value in schemas.items())
    schema = {**schemas["timeline-commit.json"], "$ref": "#/$defs/PreparedCommit"}
    Draft202012Validator(schema, registry=registry).validate(prepared)


@pytest.fixture
def realm(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "acceptance", "name": "Acceptance"}, idempotency_key="project")["id"]
    service.create_timeline_document(project, {"timeline_id": "main", "slug": "main", "name": "Main", "config": {}, "registry": {}},
                                     idempotency_key="timeline")
    commits = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
    head = commits.bootstrap(project, "main", authorize=lambda: None)
    yield service, commits, project, head, root
    service.close()


def context(service, project, head, key="move", *, dry_run=False, op="clip.move"):
    command = {"schema_version": 1, "op": op, "version": "1", "select": "parent/clip:clip", "args": {"on": 2}}
    request = {"api_version": 1, "project_id": project, "timeline_id": "main", "base_revision_id": head["revision_id"],
               "base_publication_id": head["publication_id"], "commands": [command], "rationale": "Move clip"}
    if dry_run:
        request["dry_run"] = True
    value = {"request": request, "invocation": {"operation": "commitTimeline", "path": f"/v1/projects/{project}/timelines/main/commit", "body": copy.deepcopy(request)},
             "idempotency_key": key, "realm_id": service.realm["id"], "publisher": "author"}
    value["request_hash"] = request_identity(value)
    return value


def prepared(commits, ctx, *, expected=None, revision="parent-moved", on=2, reuse=False):
    request = ctx["request"]
    expected = expected or commits.head(request["project_id"], "main")
    document = commits.revision_closure(request["project_id"], "main", expected["revision_id"])
    if not reuse:
        parent = document["parent_revision"]
        parent["revision_id"] = revision
        parent["payload"]["config"] = {"clips": [], "tracks": []}
        parent["payload"]["clips"] = [{"id": "clip", "at": on, "hold": 1, "track": "picture", "clipType": "hold", "opaque": {"clear": None}}]
        parent["content_digest"] = digest(parent["payload"])
    command = copy.deepcopy(request["commands"][0])
    command["args"]["on"] = on
    record = {"ordinal": 0, "command": command,
              "writes": [{"ref": "parent/clip:clip", "path": ["at"], "before": {"state": "present", "value": on},
                          "after": {"state": "present", "value": on}}],
              "reads": [], "selections": [], "bindings": [], "created": [], "dependencies": [], "derived_writes": []}
    return {"expected_head": expected, "canonical_document": document, "document_digest": digest(document),
            "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None},
            "id_map": {"clip": "clip"}, "semantic_events": [], "provider_version": "fixture-1", "compiler_version": "fixture-1"}


def counts(service):
    result = {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in
            ("parent_composition_revisions", "internal_timeline_revisions", "shot_revisions", "timeline_commit_history", "timeline_events", "command_idempotency", "project_sequences")}
    result["project_next_seq"] = service.store.conn.execute("SELECT COALESCE(SUM(next_seq), 0) FROM project_sequences").fetchone()[0]
    result["timeline_versions"] = service.store.conn.execute("SELECT COALESCE(SUM(version), 0) FROM timelines").fetchone()[0]
    return result


def accept(commits, ctx, value):
    return commits.accept(ctx, value, authorize=lambda: None)


def test_atomic_acceptance_exact_recorder_projection_and_same_content_edge(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    value["records"]["commands"][0]["command"]["rationale"] = "Recorded move"
    first = accept(commits, ctx, value)
    assert first["data"]["commands"] == [value["records"]["commands"][0]["command"]]
    assert first["data"]["commands"] != ctx["request"]["commands"]
    receipt = first["receipt"]
    assert receipt["result"] == first["data"]
    assert receipt["command_kind"] == "timeline.commit"
    assert receipt["request_hash"] == ctx["request_hash"]
    event = service.store.conn.execute("SELECT * FROM timeline_events WHERE id=?", (receipt["event_ids"][0],)).fetchone()
    assert event["kind"] == "timeline.commit.accepted"
    assert json.loads(event["payload_json"])["previous"] == head
    next_head = commits.head(project, "main")
    second_ctx = context(service, project, next_head, "unchanged")
    second = accept(commits, second_ctx, prepared(commits, second_ctx, reuse=True))
    assert second["data"]["accepted_revision_id"] == first["data"]["accepted_revision_id"]
    assert second["receipt"]["receipt_id"] != receipt["receipt_id"]
    page = commits.history(project, "main", commits.head(project, "main"))
    assert len(page["items"]) == 3
    assert page["items"][-1]["previous"] == next_head
    assert page["items"][-1]["records"]["commands"][0]["writes"][0]["before"] == {"state": "present", "value": 2}
    assert service.store.integrity_report()["ok"]


def test_identical_retry_after_restart_and_head_advance(realm):
    service, commits, project, head, root = realm
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    original = accept(commits, ctx, value)
    advanced = context(service, project, commits.head(project, "main"), "advance")
    accept(commits, advanced, prepared(commits, advanced, revision="parent-next", on=3))
    before = counts(service)
    service.close()
    restarted = RuntimeService(root)
    try:
        replay = TimelineCommitStore(restarted.store, validate_prepared=validate_prepared)
        assert canonical_json(replay.lookup(ctx, authorize=lambda: None)) == canonical_json(original)
        assert replay.accept(ctx, value, authorize=lambda: None) == original
        assert counts(restarted) == before
    finally:
        restarted.close()


def test_changed_payload_and_publication_only_cas_refuse_without_writes(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    accept(commits, ctx, value)
    current = commits.head(project, "main")
    other = context(service, project, current, "same-content")
    accept(commits, other, prepared(commits, other, reuse=True))
    before = counts(service)
    changed = copy.deepcopy(ctx)
    changed["request"]["rationale"] = "different"
    changed["invocation"]["body"] = copy.deepcopy(changed["request"])
    changed["request_hash"] = request_identity(changed)
    with pytest.raises(CommitRejected) as mismatch:
        commits.lookup(changed, authorize=lambda: None)
    assert mismatch.value.failure["details"]["reason"] == "idempotency_mismatch"
    stale = context(service, project, current, "stale")
    stale_value = prepared(commits, stale, expected=current, revision="never-written")
    with pytest.raises(StaleHead) as race:
        accept(commits, stale, stale_value)
    assert race.value.current_head["revision_id"] == current["revision_id"]
    assert race.value.current_head["publication_id"] != current["publication_id"]
    assert counts(service) == before


@pytest.mark.parametrize("bad", ["digest", "manifest", "ordinal", "id_map", "unknown_field", "nonfinite", "event", "base_pair"])
def test_invalid_prepared_values_are_atomic(realm, bad):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    if bad == "digest":
        value["document_digest"] = "sha256:" + "0" * 64
    elif bad == "manifest":
        value["canonical_document"]["dependency_manifest"]["shots"] = [{"shot_id": "foreign", "revision_id": "foreign", "internal_timeline_revision_id": "foreign", "content_digest": "sha256:" + "0" * 64}]
        value["document_digest"] = digest(value["canonical_document"])
    elif bad == "ordinal":
        value["records"]["commands"][0]["ordinal"] = 2
    elif bad == "id_map":
        value["id_map"] = {"clip": "replacement"}
    elif bad == "unknown_field":
        value["receipt"] = {}
    elif bad == "nonfinite":
        value["records"]["commands"][0]["command"]["args"]["on"] = float("nan")
    elif bad == "event":
        value["semantic_events"] = [{"command_ordinal": 0, "kind": "unregistered", "subject_ref": None, "payload": {}}]
    elif bad == "base_pair":
        ctx["request"]["base_revision_id"] = "wrong"
        ctx["invocation"]["body"] = copy.deepcopy(ctx["request"])
        ctx["request_hash"] = request_identity(ctx)
    before = counts(service)
    with pytest.raises((CommitRejected, ValidationError)):
        accept(commits, ctx, value)
    assert counts(service) == before
    assert commits.head(project, "main") == head


def test_failure_after_receipt_rolls_back_every_row(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    class Inputs:
        def validate(self, prepared):
            pass
        def persist(self, *args):
            raise RuntimeError("crash before COMMIT")
    before = counts(service)
    with pytest.raises(RuntimeError, match="crash before COMMIT"):
        commits.accept(ctx, prepared(commits, ctx), authorize=lambda: None, inputs=Inputs())
    assert counts(service) == before
    assert commits.head(project, "main") == head
    assert commits.lookup(ctx, authorize=lambda: None) is None


def test_preview_is_validated_and_reserves_nothing(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head, dry_run=True)
    value = prepared(commits, ctx)
    before = counts(service)
    preview = commits.preview(ctx, value, authorize=lambda: None)
    assert preview["receipt"] is None
    assert preview["data"]["evaluated_head"] == head
    assert preview["data"]["commands"] == [r["command"] for r in value["records"]["commands"]]
    with pytest.raises(CommitRejected) as error:
        accept(commits, ctx, value)
    assert error.value.failure["details"]["reason"] == "dry_run_accept"
    assert counts(service) == before


def test_history_pages_keep_fixed_bounds_and_reject_foreign_cursor(realm):
    service, commits, project, head, _ = realm
    for i in range(3):
        ctx = context(service, project, commits.head(project, "main"), f"move-{i}")
        accept(commits, ctx, prepared(commits, ctx, revision=f"parent-{i}", on=i))
    through = commits.head(project, "main")
    page = commits.history(project, "main", through, limit=2)
    ctx = context(service, project, through, "advance")
    accept(commits, ctx, prepared(commits, ctx, revision="past-bound"))
    rest = commits.history(project, "main", through, cursor=page["next_cursor"], limit=2)
    assert len(page["items"] + rest["items"]) == 4
    assert rest["head"] == through
    assert rest["items"][-1]["publication_id"] == through["publication_id"]
    with pytest.raises(ValidationError):
        commits.history(project, "main", commits.head(project, "main"), cursor=page["next_cursor"])
    with pytest.raises(ValidationError):
        commits.history(project, "main", through, limit=201)


def test_nested_acceptance_is_refused(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    with service.store._mutex, service.store._transaction():
        with pytest.raises(ProtocolError, match="outer transaction"):
            accept(commits, ctx, prepared(commits, ctx))


def test_timeline_commit_retention_survives_online_and_offline_compaction(realm):
    from datetime import datetime, timedelta, timezone
    from runtime_protocol.idempotency import command_result
    from runtime_protocol.upgrade import compact_idempotency_ledger

    service, commits, project, head, root = realm
    ctx = context(service, project, head)
    result = accept(commits, ctx, prepared(commits, ctx))
    old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat(timespec="milliseconds")
    # Age the real accepted row, then capture its exact bytes/facts. This is
    # retention coverage, not a synthetic replacement for receipt acceptance.
    service.store.conn.execute("UPDATE command_idempotency SET created_at=? WHERE txn_id=?", (old, result["receipt"]["receipt_id"]))
    row = service.store.conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (result["receipt"]["receipt_id"],)).fetchone()
    assert command_result(row["result_json"], kind="timeline.commit", created_at=old) == result["data"]
    expected = commits.lookup(ctx, authorize=lambda: None)
    encoded = row["result_json"]
    service.store._last_idempotency_prune = 0
    service._command_record("test.trigger-prune", "test", "trigger", "hash", {"ok": True}, project_id=project)
    assert commits.lookup(ctx, authorize=lambda: None) == expected
    realm_id = service.realm["id"]
    service.close()
    compact_idempotency_ledger(root, confirmation=f"COMPACT IDEMPOTENCY {realm_id}")
    reopened = RuntimeService(root)
    try:
        replay = TimelineCommitStore(reopened.store, validate_prepared=validate_prepared)
        assert canonical_json(replay.lookup(ctx, authorize=lambda: None)) == canonical_json(expected)
        assert reopened.store.conn.execute("SELECT result_json FROM command_idempotency WHERE txn_id=?", (result["receipt"]["receipt_id"],)).fetchone()[0] == encoded
        assert reopened.store.integrity_report()["ok"]
    finally:
        reopened.close()


def test_verified_baseline_keeps_main_receipt_event_and_unknown_intent(tmp_path):
    from test_timeline_cutover import _service

    service, project, _ = _service(tmp_path)
    try:
        commits = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
        receipt = service.committed_receipt("parent_composition.publish", "main", "publish", project_id=project)
        before = counts(service)
        head = commits.install_verified_baseline(project, "main", authorize=lambda: None)
        assert head == {"revision_id": "parent-1", "publication_id": receipt["receipt_id"]}
        entry = commits.history_entry(project, "main", head["publication_id"])
        assert entry["receipt"] == receipt
        assert entry["intent"] == "legacy_unknown"
        assert entry["records"] is None
        assert entry["publisher"] is None
        assert counts(service) == {**before, "timeline_commit_history": 1}
        assert commits.install_verified_baseline(project, "main", authorize=lambda: None) == head
        assert commits.revision_closure(project, "main", "parent-1")["shot_revisions"][0]["shot_id"] == "shot-1"
        assert service.store.integrity_report()["ok"]
    finally:
        service.close()


def test_unproven_baseline_and_same_content_legacy_write_fail_closed(realm):
    service, commits, project, head, _ = realm
    # A later untracked write with unchanged revision bytes invalidates the
    # editable publication pair. Exact-key replay still precedes head reads.
    ctx = context(service, project, head)
    accepted = accept(commits, ctx, prepared(commits, ctx))
    service.store._append_timeline_event("main", "timeline.updated", {"project_id": project, "version": 99})
    with pytest.raises(CommitRejected) as unavailable:
        commits.head(project, "main")
    assert unavailable.value.failure["details"]["reason"] == "history_unavailable"
    assert commits.lookup(ctx, authorize=lambda: None) == accepted


def test_commit_integrity_detects_missing_history_and_corrupt_record(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head)
    result = accept(commits, ctx, prepared(commits, ctx))
    service.store.conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?",
                               ('{"commands":[]}', result["receipt"]["receipt_id"]))
    with pytest.raises(ProtocolError, match="corrupt"):
        commits.lookup(ctx, authorize=lambda: None)
    report = service.store.integrity_report()
    assert not report["ok"]
    assert any(error["table"] == "timeline_commit_history" for error in report["checks"]["revisions"]["errors"])


def test_v30_schema_migration_installs_empty_history_without_invented_baselines(tmp_path):
    import sqlite3
    from runtime_protocol.upgrade import _apply_v30_to_v31, _canonical_schema_identity, migrate_canonical_to_current

    root = tmp_path / "old-realm"
    initial = RealmStore.initialize(root)
    realm_id = initial.realm["id"]
    initial.close()
    connection = sqlite3.connect(root / "realm.sqlite3", isolation_level=None)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("ALTER TABLE parent_composition_heads DROP COLUMN publication_id")
        connection.execute("ALTER TABLE parent_composition_revisions DROP COLUMN commit_manifest_json")
        for table in ("timeline_commit_history", "timeline_document_input_links", "timeline_document_input_bindings", "timeline_document_input_contents"):
            connection.execute(f"DROP TABLE {table}")
        connection.execute("UPDATE runtime_schema SET version=30 WHERE id=1")
        assert _canonical_schema_identity(connection)["version"] == 30
        connection.execute("BEGIN IMMEDIATE")
        assert _apply_v30_to_v31(connection)["target_schema_version"] == 31
        assert connection.in_transaction
        assert _canonical_schema_identity(connection)["version"] == 31
        assert connection.execute("SELECT COUNT(*) FROM timeline_commit_history").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM timeline_document_input_contents").fetchone()[0] == 0
        connection.rollback()
        assert _canonical_schema_identity(connection)["version"] == 30
    finally:
        connection.close()
    result = migrate_canonical_to_current(root, confirmation=f"MIGRATE CANONICAL {realm_id}")
    assert result["target_schema_version"] == 31
    assert len(result["steps"]) == 1
    reopened = RealmStore(root)
    try:
        assert reopened.integrity_report()["ok"]
        assert reopened.conn.execute("SELECT COUNT(*) FROM timeline_commit_history").fetchone()[0] == 0
    finally:
        reopened.close()


@pytest.mark.parametrize("kind", ["config", "transcript"])
def test_real_acceptance_links_consumed_inputs_and_keeps_old_bytes_after_restart(realm, kind):
    from runtime_protocol.timeline_commit_inputs import (
        DocumentInputLink, capture_document_input, persist_document_input_links, validate_captured_document_inputs,
    )
    service, commits, project, head, root = realm
    if kind == "transcript":
        media_id = service.ingest(project, b"source-media", media_type="video/mp4", idempotency_key="media")["data"]["object_id"]
        document_id = RuntimeService._transcript_document_id(project, media_id, "default")
        content = {"schema": "media.transcript/v1", "media_id": media_id, "source_id": "default",
                   "segments": [{"id": "segment-1", "start": 0, "end": 1, "text": "hello",
                                 "words": [{"id": "word-1", "start": 0, "end": 1, "text": "hello"}]}]}
        document_kind = "media.transcript"
    else:
        document_id, document_kind = "editing-config", "fixture.config"
        content = {"schema": "fixture.config/v1", "value": 1, "opaque": {"clear": None}}
    document = service.create_document(project, {"document_id": document_id, "kind": document_kind, "content": content}, idempotency_key="source")["data"]
    pin = {"document_id": document_id, "version": document["version"], "content_digest": digest(content)}
    capture = capture_document_input(service.store.conn, project, pin, expected_kind=document_kind, expected_schema=content["schema"])
    class Inputs:
        def validate(self, candidate):
            assert candidate["canonical_document"]["dependency_manifest"]["documents"] == [pin]
            validate_captured_document_inputs(service.store.conn, [capture])
        def persist(self, candidate, publication_id, revision_id):
            persist_document_input_links(service.store.conn, project_id=project, timeline_id="main", publication_id=publication_id,
                                         revision_id=revision_id, links=[DocumentInputLink(capture, "transcript" if kind == "transcript" else "source", 0)])
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    value["canonical_document"]["dependency_manifest"]["documents"] = [pin]
    if kind == "transcript":
        value["canonical_document"]["dependency_manifest"]["media"] = [{"media_id": media_id, "content_digest": media_id}]
    value["document_digest"] = digest(value["canonical_document"])
    value["records"]["commands"][0]["dependencies"] = [{"key": "input", "kind": "transcript" if kind == "transcript" else "source", "pin": pin, "policy": "exact"}]
    result = commits.accept(ctx, value, authorize=lambda: None, inputs=Inputs())
    links = service.store.conn.execute("SELECT * FROM timeline_document_input_links WHERE publication_id=?", (result["receipt"]["receipt_id"],)).fetchall()
    assert len(links) == 1
    replacement = copy.deepcopy(content)
    if kind == "transcript":
        replacement["segments"][0]["words"][0]["text"] = "changed"
    else:
        replacement["value"] = 2
    service.update_document(project, document_id, {"expected_version": 1, "content": replacement}, idempotency_key="replace-input")
    service.close()
    reopened = RuntimeService(root)
    try:
        persisted = TimelineCommitStore(reopened.store, validate_prepared=validate_prepared)
        assert persisted.lookup(ctx, authorize=lambda: None) == result
        closure = persisted.revision_closure(project, "main", result["data"]["accepted_revision_id"])
        retained = capture_document_input(reopened.store.conn, project, pin, reachable_pins=closure["dependency_manifest"]["documents"],
                                          expected_kind=document_kind, expected_schema=content["schema"])
        assert retained.retained
        assert retained.document == document
        assert reopened.store.integrity_report()["ok"]
    finally:
        reopened.close()


def test_live_capture_accept_race_rolls_back_history_receipt_and_input_links(realm):
    from runtime_protocol.errors import ConflictError
    from runtime_protocol.timeline_commit_inputs import capture_document_input, validate_captured_document_inputs
    service, commits, project, head, _ = realm
    content = {"schema": "fixture.config/v1", "value": 1}
    service.create_document(project, {"document_id": "config", "kind": "fixture.config", "content": content}, idempotency_key="config")
    pin = {"document_id": "config", "version": 1, "content_digest": digest(content)}
    capture = capture_document_input(service.store.conn, project, pin, expected_kind="fixture.config", expected_schema=content["schema"])
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    value["canonical_document"]["dependency_manifest"]["documents"] = [pin]
    value["document_digest"] = digest(value["canonical_document"])
    class Inputs:
        def validate(self, prepared):
            validate_captured_document_inputs(service.store.conn, [capture])
        def persist(self, *args):
            pytest.fail("changed capture reached persistence")
    service.update_document(project, "config", {"expected_version": 1, "content": {**content, "value": 2}}, idempotency_key="update-config")
    before = counts(service)
    with pytest.raises(ConflictError):
        commits.accept(ctx, value, authorize=lambda: None, inputs=Inputs())
    assert counts(service) == before
    assert service.store.conn.execute("SELECT COUNT(*) FROM timeline_document_input_links").fetchone()[0] == 0
    assert service.store.conn.execute("SELECT COUNT(*) FROM timeline_document_input_contents").fetchone()[0] == 0


def test_complete_detached_child_closure_projects_and_reuses_exact_rows(realm):
    service, commits, project, head, _ = realm
    ctx = context(service, project, head, op="fixture.add-shot")
    value = prepared(commits, ctx)
    internal_payload = {"clips": [], "tracks": [], "app": {"opaque": None}}
    internal = {"timeline_id": "shot:shot-1", "revision_id": "internal-1", "payload": internal_payload, "content_digest": digest(internal_payload)}
    shot_payload = {"name": "Opening", "metadata": {"opaque": {"keep": None}}, "items": [], "internal_timeline_revision_id": "internal-1"}
    shot = {"shot_id": "shot-1", "revision_id": "shot-1-r1", "internal_timeline_revision_id": "internal-1", "payload": shot_payload, "content_digest": digest(shot_payload)}
    occurrence = {"occurrence_id": "occ-1", "shot_id": "shot-1", "shot_revision_id": "shot-1-r1", "placement": {"start_ms": 0},
                  "duration_ms": 1000, "source_offset": 0, "speed": {"numerator": 1, "denominator": 1}, "track": "picture",
                  "transform": {}, "gain": 1, "muted": False, "provenance": {}, "opaque": {"preserve": None}}
    document = value["canonical_document"]
    document["shot_revisions"], document["internal_timeline_revisions"] = [shot], [internal]
    document["parent_revision"]["payload"]["occurrences"] = [occurrence]
    document["parent_revision"]["content_digest"] = digest(document["parent_revision"]["payload"])
    document["dependency_manifest"]["shots"] = [{k: shot[k] for k in ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest")}]
    document["dependency_manifest"]["internal_timelines"] = [{k: internal[k] for k in ("timeline_id", "revision_id", "content_digest")}]
    value["document_digest"] = digest(document)
    value["records"]["commands"][0]["created"] = [{"ref": "parent/occurrence:occ-1", "kind": "occurrence", "owner": "parent"}]
    result = accept(commits, ctx, value)
    assert commits.revision_closure(project, "main", result["data"]["accepted_revision_id"]) == document
    child = commits.shot_closure(project, "shot-1", "shot-1-r1")
    assert child["shot_revision"] == shot
    assert child["internal_timeline_revision"] == internal
    row = service.store.conn.execute("SELECT * FROM project_shots WHERE id='shot-1'").fetchone()
    assert row["name"] == "Opening"
    assert json.loads(row["metadata_json"]) == shot_payload["metadata"]
    before = counts(service)
    new_ctx = context(service, project, commits.head(project, "main"), "reuse-child")
    accept(commits, new_ctx, prepared(commits, new_ctx, reuse=True))
    assert counts(service)["shot_revisions"] == before["shot_revisions"]
    assert counts(service)["internal_timeline_revisions"] == before["internal_timeline_revisions"]
    assert service.store.integrity_report()["ok"]


def test_nonmanaged_project_media_relation_cannot_authorize_commit(realm):
    service, commits, project, head, _ = realm
    media_id = service.ingest(project, b"same-object", media_type="video/mp4", idempotency_key="import")["data"]["object_id"]
    service.store.conn.execute("UPDATE project_objects SET relation='referenced' WHERE project_id=? AND digest=?", (project, media_id.removeprefix("sha256:")))
    ctx = context(service, project, head)
    value = prepared(commits, ctx)
    value["canonical_document"]["dependency_manifest"]["media"] = [{"media_id": media_id, "content_digest": media_id}]
    value["document_digest"] = digest(value["canonical_document"])
    before = counts(service)
    with pytest.raises(CommitRejected) as error:
        accept(commits, ctx, value)
    assert error.value.failure["details"]["reason"] == "dependency_unavailable"
    assert counts(service) == before
    assert commits.head(project, "main") == head
