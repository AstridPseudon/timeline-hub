"""Disposable exact-set lifecycle proofs; no historical-film/live-store input."""
import hashlib
import json
import sqlite3
from pathlib import Path
import pytest

from runtime_protocol.errors import AuthorizationError, ConflictError, ValidationError
from test_shot_composition_runtime import _service, _publication

OWNER = {"actor": "owner", "scopes": ["admin", "projects:write"], "_credential_binding": "fixture-owner"}


@pytest.fixture
def fixture(tmp_path):
    s, p = _service(tmp_path)
    s.publish_parent_composition(p, "main", _publication(p), idempotency_key="source-publish")
    yield s, p
    s.close()


def duplicate(s, p, tid="dup", publish=False, shared=False, share_internal=False):
    head = s.head(p, "main")
    source = {"timeline_id": "main", "expected_revision_id": head["revision_id"], "expected_publication_id": head["publication_id"]}
    s.create_timeline(p, tid, duplicate_source=source, identity=OWNER, idempotency_key="create-" + tid)
    if publish:
        body = _publication(p, parent_revision_id=tid + "-parent", shot_revision_id=tid + "-shotrev")
        body["timeline_id"] = tid
        body["internal_timeline_revisions"][0]["timeline_id"] = tid
        body["internal_timeline_revisions"][0]["revision_id"] = tid + "-internal"
        body["shot_revisions"][0]["shot_id"] = tid + "-shot"
        body["shot_revisions"][0]["internal_timeline_revision_id"] = tid + "-internal"
        body["parent_composition"]["occurrences"][0].update(shot_id=tid + "-shot", shot_revision_id=tid + "-shotrev")
        if shared:
            body["internal_timeline_revisions"] = []
            body["shot_revisions"] = []
            body["parent_composition"]["occurrences"][0].update(shot_id="shot-1", shot_revision_id="shot-rev-1")
        elif share_internal:
            body["internal_timeline_revisions"] = []
            body["shot_revisions"][0]["internal_timeline_revision_id"] = "timeline-rev-1"
        s.publish_parent_composition(p, tid, body, idempotency_key="publish-" + tid)
    return source


def archive(s, tid="dup", withdraw=False):
    body = {"expected_version": s._timeline_resource(tid)["version"]}
    if withdraw:
        head = s.head(s._timeline_resource(tid)["project_id"], tid)
        body["withdraw_publication"] = {"expected_revision_id": head["revision_id"], "expected_publication_id": head["publication_id"]}
    return s.archive_timeline(tid, body, identity=OWNER, idempotency_key="archive-" + tid)


def request(s, p, *tids):
    return {"targets": [{"timeline_id": tid, "expected_version": s._timeline_resource(tid)["version"],
                         "expected_revision_id": None, "expected_publication_id": None} for tid in tids]}


def execute(s, p, body, key="purge", identity=OWNER):
    plan = s.plan_timeline_purge(p, body)
    return s.execute_timeline_purge(p, {**body, "plan_digest": plan["plan_digest"]}, identity=identity, idempotency_key=key)


def test_exact_set_reclaims_history_and_exclusive_children_replays(fixture):
    s, p = fixture
    duplicate(s, p, publish=True)
    archive(s, withdraw=True)
    body = request(s, p, "dup")
    plan = s.plan_timeline_purge(p, body)
    assert plan["eligible"], plan["blockers"]
    assert plan["deletion_counts"]["shot_revisions"] == 1
    assert plan["deletion_counts"]["parent_composition_publications"] == 1
    result = execute(s, p, body)
    assert result["data"]["status"] == "purged"
    assert s.store.conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert not s.store.conn.execute("SELECT 1 FROM timelines WHERE id='dup'").fetchone()
    replay_body = {**body, "plan_digest": plan["plan_digest"]}
    assert s.execute_timeline_purge(p, replay_body, identity=OWNER, idempotency_key="purge") == result
    s.store.conn.execute("UPDATE command_idempotency SET created_at='2000-01-01T00:00:00+00:00' WHERE command_kind='timeline.purge'")
    old_replay = s.execute_timeline_purge(p, replay_body, identity=OWNER, idempotency_key="purge")
    assert old_replay["data"] == result["data"]
    assert old_replay["receipt"]["receipt_id"] == result["receipt"]["receipt_id"]
    # Target-owned create replay cannot return its reclaimed resource.
    terminal = s.create_timeline(p, "dup", duplicate_source={"timeline_id": "main", "expected_revision_id": "parent-1", "expected_publication_id": s.head(p, "main")["publication_id"]}, identity=OWNER, idempotency_key="create-dup")
    assert terminal["data"] == {"status": "purged", "terminal": True}


@pytest.mark.parametrize("identity", [None, {"actor": "owner", "scopes": ["projects:write"]},
    {"actor": "editor", "scopes": ["admin"], "_credential_binding": "x"},
    {**OWNER, "_paired_session": "grant"}, {**OWNER, "connector_assertion": {"x": "y"}}])
def test_owner_execution_required(fixture, identity):
    s, p = fixture
    duplicate(s, p)
    archive(s)
    with pytest.raises(AuthorizationError):
        execute(s, p, request(s, p, "dup"), identity=identity)
    assert s._timeline_resource("dup")


def test_ordinary_archived_and_forged_duplicate_not_admitted(fixture):
    s, p = fixture
    s.create_timeline(p, "ordinary", idempotency_key="ordinary")
    archive(s, "ordinary")
    plan = s.plan_timeline_purge(p, request(s, p, "ordinary"))
    assert "duplicate_provenance_missing" in {b["code"] for b in plan["blockers"]}
    with pytest.raises(ConflictError):
        s.create_timeline(p, "bad", duplicate_source={"timeline_id": "main", "expected_revision_id": "forged", "expected_publication_id": "forged"}, identity=OWNER)
    with pytest.raises(AuthorizationError):
        s.create_timeline(p, "bad", duplicate_source={"timeline_id": "main", "expected_revision_id": "parent-1", "expected_publication_id": s.head(p, "main")["publication_id"]})


def test_archive_current_publication_requires_explicit_withdrawal(fixture):
    s, p = fixture
    duplicate(s, p, publish=True)
    before = s.head(p, "dup")
    archive(s)
    assert s.head(p, "dup") == before
    plan = s.plan_timeline_purge(p, request(s, p, "dup"))
    assert "current_publication" in {b["code"] for b in plan["blockers"]}
    with pytest.raises(ConflictError):
        s.archive_timeline("dup", {"expected_version": s._timeline_resource("dup")["version"], "withdraw_publication": {"expected_revision_id": "stale", "expected_publication_id": before["publication_id"]}}, identity=OWNER)


def test_shared_children_survive(fixture):
    s, p = fixture
    duplicate(s, p, publish=True, shared=True)
    archive(s, withdraw=True)
    plan = s.plan_timeline_purge(p, request(s, p, "dup"))
    assert plan["eligible"], plan["blockers"]
    assert "shot_revisions" not in plan["deletion_counts"]
    execute(s, p, request(s, p, "dup"))
    assert s.store.conn.execute("SELECT 1 FROM shot_revisions WHERE id='shot-rev-1'").fetchone()
    assert s.head(p, "main")["revision_id"] == "parent-1"


def test_duplicate_owned_shot_reclaimed_while_source_internal_payload_survives(fixture):
    s, p = fixture
    duplicate(s, p, publish=True, share_internal=True)
    archive(s, withdraw=True)
    body = request(s, p, "dup")
    plan = s.plan_timeline_purge(p, body)
    assert plan["eligible"], plan["blockers"]
    assert plan["deletion_counts"]["shot_revisions"] == 1
    execute(s, p, body)
    assert not s.store.conn.execute("SELECT 1 FROM project_shots WHERE id='dup-shot'").fetchone()
    assert s.store.conn.execute("SELECT 1 FROM internal_timeline_revisions WHERE id='timeline-rev-1'").fetchone()
    assert s.get_project_parent_composition_revision(p, "main", "parent-1")


@pytest.mark.parametrize("race", ["recover", "new_reference", "new_publication"])
def test_stale_plan_races_reject_whole_set(fixture, race):
    s, p = fixture
    duplicate(s, p)
    archive(s)
    body = request(s, p, "dup")
    plan = s.plan_timeline_purge(p, body)
    if race == "recover":
        s.recover_timeline("dup", {"expected_version": 2, "version": 1}, idempotency_key="recover")
    elif race == "new_reference":
        s.create_document(p, {"document_id": "pin", "kind": "pin", "content": {"timeline_id": "dup"}}, idempotency_key="pin")
    else:
        body2 = _publication(p, parent_revision_id="dup-parent")
        body2["timeline_id"] = "dup"
        body2["internal_timeline_revisions"] = []
        body2["shot_revisions"] = []
        s.publish_parent_composition(p, "dup", body2, idempotency_key="race-publish")
    with pytest.raises(ConflictError):
        s.execute_timeline_purge(p, {**body, "plan_digest": plan["plan_digest"]}, identity=OWNER, idempotency_key="purge")
    assert s._timeline_resource("dup")


def test_mixed_set_is_atomic_and_delete_failure_rolls_back(fixture, monkeypatch):
    s, p = fixture
    duplicate(s, p)
    archive(s)
    body = request(s, p, "dup", "main")
    with pytest.raises(ConflictError):
        execute(s, p, body)
    assert s._timeline_resource("dup")
    import runtime_protocol.timeline_retention as retention
    original = retention.delete_plan
    def fail_after_delete(service, snapshot):
        original(service, snapshot)
        raise RuntimeError("fixture post-delete failure")
    monkeypatch.setattr(retention, "delete_plan", fail_after_delete)
    before = list(s.store.conn.execute("SELECT result_json FROM command_idempotency ORDER BY command_kind, aggregate_id, idempotency_key"))
    with pytest.raises(RuntimeError):
        execute(s, p, request(s, p, "dup"))
    assert s._timeline_resource("dup")
    assert list(s.store.conn.execute("SELECT result_json FROM command_idempotency ORDER BY command_kind, aggregate_id, idempotency_key")) == before


@pytest.mark.parametrize("field", ["previous_revision_id", "restored_from_revision_id", "previous_publication_id"])
def test_retained_historical_publication_pin_blocks(fixture, field):
    s, p = fixture
    duplicate(s, p, publish=True)
    pinned = s.head(p, "dup")
    archive(s, withdraw=True)
    value = pinned["publication_id"] if field == "previous_publication_id" else pinned["revision_id"]
    s.store.conn.execute(f"UPDATE parent_composition_publications SET {field}=? WHERE timeline_id='main'", (value,))
    plan = s.plan_timeline_purge(p, request(s, p, "dup"))
    assert any(b["code"] == "external_reference" and b["table"] == "parent_composition_publications" for b in plan["blockers"])
    with pytest.raises(ConflictError):
        execute(s, p, request(s, p, "dup"))


@pytest.mark.parametrize("content", [{"timeline_id": 42}, {"pin": {"unknown_extension": "dup"}}])
def test_malformed_or_unknown_resolving_data_refuses(fixture, content):
    s, p = fixture
    duplicate(s, p)
    archive(s)
    s.create_document(p, {"document_id": "pin", "kind": "pin", "content": content}, idempotency_key="pin")
    assert not s.plan_timeline_purge(p, request(s, p, "dup"))["eligible"]


def test_retained_shared_child_with_deleted_owner_timeline_blocks(fixture):
    s, p = fixture
    duplicate(s, p, publish=True)
    archive(s, withdraw=True)
    s.create_document(p, {"document_id": "child-pin", "kind": "pin", "content": {"shot_revision_id": "dup-shotrev"}}, idempotency_key="child-pin")
    plan = s.plan_timeline_purge(p, request(s, p, "dup"))
    # C011's inspection reader requires the retained internal timeline owner
    # to remain a valid timeline; retaining only the shared bytes is unsafe.
    assert any(b["table"] == "internal_timeline_revisions" for b in plan["blockers"])
    assert "shot_revisions" not in plan["deletion_counts"]


def test_execute_holds_sqlite_writer_fence_through_delete(fixture, monkeypatch):
    s, p = fixture
    duplicate(s, p)
    archive(s)
    import runtime_protocol.timeline_retention as retention
    original = retention.delete_plan
    db_path = s.store.conn.execute("PRAGMA database_list").fetchone()[2]
    def concurrent_reference_attempt(service, snapshot):
        other = sqlite3.connect(db_path, timeout=0)
        try:
            with pytest.raises(sqlite3.OperationalError, match="locked"):
                other.execute("UPDATE timelines SET archived_at=NULL WHERE id='dup'")
        finally:
            other.close()
        original(service, snapshot)
    monkeypatch.setattr(retention, "delete_plan", concurrent_reference_attempt)
    execute(s, p, request(s, p, "dup"))


def test_retained_source_history_bytes_unchanged_and_schemas_match(fixture):
    import jsonschema
    s, p = fixture
    def digest():
        tables = ("parent_composition_revisions", "parent_composition_publications", "internal_timeline_revisions", "shot_revisions")
        return hashlib.sha256(json.dumps([[dict(r) for r in s.store.conn.execute(f"SELECT * FROM {t} ORDER BY 1")] for t in tables], sort_keys=True).encode()).hexdigest()
    before = digest()
    duplicate(s, p, publish=True)
    archive(s, withdraw=True)
    body = request(s, p, "dup")
    schema = json.loads((Path(__file__).parents[1] / "contract/schemas/timeline-retention.json").read_text())
    plan = s.plan_timeline_purge(p, body)
    jsonschema.Draft202012Validator({**schema, "$ref": "#/$defs/PlanResult"}).validate(plan)
    result = execute(s, p, body)
    jsonschema.Draft202012Validator({**schema, "$ref": "#/$defs/ExecuteResult"}).validate(result["data"])
    assert digest() == before
    for history in s.list_project_parent_composition_revisions(p, "main")["items"]:
        s.get_project_parent_composition_revision(p, "main", history["revision_id"])


def test_commit_compound_ledger_replay_becomes_valid_terminal_error(fixture):
    from test_timeline_accept import acceptance, valid, wire, IDENTITY
    s, p = fixture
    duplicate(s, p, publish=True, shared=True)
    head = s.head(p, "dup")
    wire_request = wire(p, key="dup-save")
    wire_request.update(timeline_id="dup", base_revision_id=head["revision_id"], base_publication_id=head["publication_id"])
    prepared = acceptance(s, p, request=wire_request, no_change=True)
    prepared.update(timeline_id="dup", expected_head_revision_id=head["revision_id"])
    prepared["result"]["rebased_onto"] = head["revision_id"]
    s.accept(prepared, identity=IDENTITY)
    archive(s, withdraw=True)
    body = request(s, p, "dup")
    plan = s.plan_timeline_purge(p, body)
    assert plan["eligible"], plan["blockers"]
    execute(s, p, body)
    terminal = s.lookup_request(p, "dup", "dup-save")["result"]
    valid(terminal, "CommitResult")
    assert terminal["status"] == "error" and terminal["canonical_document"] is None
    assert terminal["error"]["code"] == "base_not_found"
    assert s.commit_timeline(p, "dup", wire_request, idempotency_key="dup-save", identity=IDENTITY) == terminal
    assert s.revisions(p, "dup", {}) == []


@pytest.mark.parametrize("family", ["run", "task_result", "continuation"])
def test_persisted_execution_reference_families_block(fixture, family):
    from runtime_protocol.util import now
    s, p = fixture
    duplicate(s, p)
    archive(s)
    stamp = now()
    conn = s.store.conn
    conn.execute("INSERT INTO runs(id,project_id,capability,spec_json,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
                 ("ref-run", p, "fixture", json.dumps({"timeline_ref": "dup"}) if family == "run" else "{}", "succeeded", stamp, stamp))
    conn.execute("INSERT INTO tasks(id,run_id,capability,spec_json,status,result_json,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
                 ("ref-task", "ref-run", "fixture", "{}", "succeeded", json.dumps({"timeline_id": "dup"}) if family == "task_result" else None, stamp, stamp))
    if family == "continuation":
        conn.execute("INSERT INTO continuation_admissions VALUES (?,?,?)", ("ref-task", json.dumps({"dependencies": [{"timeline_id": "dup"}]}), stamp))
    plan = s.plan_timeline_purge(p, request(s, p, "dup"))
    table = {"run": "runs", "task_result": "tasks", "continuation": "continuation_admissions"}[family]
    assert any(b["code"] == "external_reference" and b["table"] == table for b in plan["blockers"])


def test_two_target_execution_leaves_other_admitted_duplicate(fixture):
    s, p = fixture
    for tid in ("one", "two", "keep"):
        duplicate(s, p, tid=tid)
        archive(s, tid)
    result = execute(s, p, request(s, p, "one", "two"))
    assert result["data"]["target_ids"] == ["one", "two"]
    assert s._timeline_resource("keep")["archived"]
    assert s._timeline_resource("main")


def test_generated_python_client_real_owner_and_editor_http(tmp_path):
    from banodoco_workspace_client import ApiError, WorkspaceClient
    from runtime_protocol.daemon import RuntimeDaemon
    from runtime_protocol.store import RealmStore
    RealmStore.initialize(tmp_path / "realm").close()
    daemon = RuntimeDaemon(tmp_path / "realm", support_root=tmp_path / "support").start()
    try:
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        p = client.create_project("Retention HTTP", slug="retention-http", idempotency_key="project").project_id
        client.create_timeline(p, "main", idempotency_key="source")
        client.publish_parent_composition(p, "main", _publication(p), idempotency_key="source-publish")
        head = client.get_project_timeline(p, "main")
        client.create_timeline(p, "dup", duplicate_source={"timeline_id": "main", "expected_revision_id": head["head_revision_id"], "expected_publication_id": head["head_publication_id"]}, idempotency_key="duplicate")
        publication = _publication(p, parent_revision_id="dup-parent")
        publication.update(timeline_id="dup", internal_timeline_revisions=[], shot_revisions=[])
        client.publish_parent_composition(p, "dup", publication, idempotency_key="duplicate-publish")
        dup_head = client.get_project_timeline(p, "dup")
        client.archive_timeline("dup", expected_version=1, idempotency_key="archive", withdraw_publication={
            "expected_revision_id": dup_head["head_revision_id"], "expected_publication_id": dup_head["head_publication_id"]})
        targets = [{"timeline_id": "dup", "expected_version": 2, "expected_revision_id": None, "expected_publication_id": None}]
        plan = client.plan_timeline_purge(p, targets)
        assert plan["eligible"]
        editor_token, _ = daemon.credentials.provision("editor", ["projects:read", "projects:write"])
        editor = WorkspaceClient(daemon.endpoint, editor_token)
        with pytest.raises(ApiError):
            editor.execute_timeline_purge(p, targets, plan_digest=plan["plan_digest"], idempotency_key="purge")
        result = client.execute_timeline_purge(p, targets, plan_digest=plan["plan_digest"], idempotency_key="purge")
        assert result["status"] == "purged"
        assert client.execute_timeline_purge(p, targets, plan_digest=plan["plan_digest"], idempotency_key="purge").receipt == result.receipt
    finally:
        daemon.stop()
