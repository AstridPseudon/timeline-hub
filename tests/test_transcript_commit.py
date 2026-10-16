"""Actual Runtime/installed Astrid boundary on disposable synthetic sources.

Run with the exact Astrid source on PYTHONPATH. Scene answers are synthetic;
document/CAS, request port, provider, transaction and ledger are production code.
"""
import copy
import hashlib
import time

import pytest

from runtime_protocol.errors import AuthorizationError, ConflictError, NotFoundError, ValidationError
from test_timeline_accept import fixture, wire  # noqa: F401
from test_selected_media_commit import snapshot, mutate


IDENTITY = dict(actor="fixture-writer", scopes=["projects:write", "projects:read", "objects:read"])


@pytest.fixture(autouse=True)
def synthetic_scene(monkeypatch):
    from astrid.core.timeline import scene_answers
    from astrid.sdk.timeline.checkout import Checkout
    class Client:
        def query_scene(self, *, revision_digest, scene, frames):
            return [dict(frame=f, coverage="COVERED", content="CONTENT", findings=[], layers=[]) for f in frames]
    monkeypatch.setattr(scene_answers, "_client", lambda: Client())
    monkeypatch.setattr(Checkout, "_native_outline_integrity", lambda *a: None)


def source(s, p, *, version=1, old=None):
    from astrid.sdk.managed_transcript import canonical_transcript_json, transcript_document_id
    media = s.ingest(p, b"synthetic media", idempotency_key="media")["data"]["object_id"]
    record = dict(schema_version=1,
        subject=dict(media_object_id=media, media_sha256=media[7:]),
        source=dict(producer_id="media.transcript_publish", source_id="take", lineage_id="lineage",
                    revision_id=f"revision-{version}", producer_digest="a" * 64),
        clock=dict(kind="media", unit="seconds", origin_seconds=0),
        words=[dict(id="word:1", text="Hello", start_s=0, end_s=.4)],
        segments=[dict(id="segment:1", word_ids=["word:1"])])
    raw = canonical_transcript_json(record).encode()
    oid = s.ingest(p, raw, media_type="application/json", idempotency_key=f"snapshot-{version}")["data"]["object_id"]
    docid = transcript_document_id(p, record["subject"], record["source"])
    if old is None:
        s.create_document(p, dict(document_id=docid, kind="media.transcript/v1", content=record), idempotency_key="doc-1")
    else:
        s.update_document(p, docid, dict(expected_version=version-1, content=record), idempotency_key=f"doc-{version}")
    return dict(schema_version=1, document=dict(id=docid, version=version, content_digest=oid),
                snapshot=dict(object_id=oid, sha256=hashlib.sha256(raw).hexdigest()),
                **{k: copy.deepcopy(record[k]) for k in ("subject", "source", "clock")})


def reference(d, *, expect=None):
    return dict(op="transcript.reference", select=None, args=dict(subject=d["subject"],
        source_key={k: d["source"][k] for k in ("producer_id", "source_id")},
        expect=expect or {"state": "absent"}, next=copy.deepcopy(d)))


def request(s, p, *calls, key="bind-1"):
    value = wire(p, key=key)
    head = s.head(p, "main")
    value.update(base_revision_id=head["revision_id"], base_publication_id=head["publication_id"])
    value["change"]["commands"] = list(calls)
    return value


def commit(s, p, body):
    return s.commit_timeline(p, "main", body, idempotency_key=body["request_id"], identity=IDENTITY)


def provider(s):
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    s.register_timeline_commit_provider(create_runtime_commit_service())


def test_actual_occurrence_bind_persists_exact_source(fixture):
    from test_shot_composition_runtime import _publication
    from astrid.sdk.timeline.commit import RuntimeCommitService
    from astrid.sdk.timeline.source_hydration import hydrate_transcript_sources
    s, p = fixture
    d = source(s, p)
    pub = _publication(p, expected_head=s.head(p, "main")["revision_id"],
                       parent_revision_id="bind-bootstrap", shot_revision_id="bind-shot")
    pub["internal_timeline_revisions"][0]["revision_id"] = "bind-internal"
    pub["shot_revisions"][0]["internal_timeline_revision_id"] = "bind-internal"
    pub["internal_timeline_revisions"][0]["payload"]["clips"][0]["object_id"] = d["subject"]["media_object_id"]
    s.publish_parent_composition(p, "main", pub, idempotency_key="bind-bootstrap")
    binding = dict(copy.deepcopy(d), occurrence_id="occurrence-1", word_ids=["word:1"])
    call = dict(op="transcript.bind", select=None, args=dict(
        target=dict(clip_id="picture", occurrence_id="occurrence-1"),
        expect=dict(binding={"state": "absent"}), next=binding, correspondence=[]))
    body = request(s, p, call)
    provider(s)
    result = commit(s, p, body)
    assert result["status"] == "accepted", result
    reload_body = request(s, p, key="reload")
    port = s._request_commit_port(reload_body, IDENTITY)
    base = RuntimeCommitService._load_revision(port, reload_body, reload_body["base_revision_id"])
    hydrate_transcript_sources(port, reload_body, base, [])
    clips = [clip for shot in base["shots"].values() for clip in shot["internal_timeline"]["clips"]]
    assert next(c for c in clips if c["id"] == "picture")["app"]["transcript"]["binding"] == binding


def test_actual_capture_accept_reload_inverse_redo_and_retained_history(fixture, monkeypatch):
    from astrid.sdk.timeline.commit import RuntimeCommitService
    from astrid.sdk.timeline.inverse import inverse_command
    s, p = fixture
    old = source(s, p)
    provider(s)
    body = request(s, p, reference(old))
    first = commit(s, p, body)
    assert first["status"] == "accepted", first
    assert first["canonical_document"]["source_mapping"]["pinned_transcripts"]
    new = source(s, p, version=2, old=old)
    before = snapshot(s)
    assert commit(s, p, body) == first  # retry does not reopen moved source
    assert snapshot(s) == before
    second_body = request(s, p, reference(new, expect=dict(state="present", value=old)), key="rebind")
    second = commit(s, p, second_body)
    assert second["status"] == "accepted", second
    assert len(second["canonical_document"]["source_mapping"]["pinned_transcripts"]) == 2
    old_base = first["canonical_document"]
    inverse = inverse_command(second["change"]["commands"], old_base, second["canonical_document"], second["accepted_publication_id"])
    def no_document(*a):
        pytest.fail("accepted old source must not read mutable document")
    monkeypatch.setattr(s, "get_document", no_document)
    undo_body = request(s, p, inverse, key="undo")
    port = s._request_commit_port(undo_body, IDENTITY)
    reloaded = RuntimeCommitService._load_revision(port, undo_body, undo_body["base_revision_id"])
    assert reloaded["parent"]["config"] == second["canonical_document"]["parent"]["config"]
    undone = commit(s, p, undo_body)
    assert undone["status"] == "accepted", undone
    redo = inverse_command(undone["change"]["commands"], second["canonical_document"], undone["canonical_document"], undone["accepted_publication_id"])
    redone = commit(s, p, request(s, p, redo, key="redo"))
    assert redone["status"] == "accepted", redone
    assert redone["canonical_document"]["parent"]["config"] == second["canonical_document"]["parent"]["config"]
    deps = {row[0] for row in s.store.conn.execute("SELECT dependency_id FROM composition_revision_dependencies WHERE dependency_kind='media'")}
    assert {old["snapshot"]["object_id"], new["snapshot"]["object_id"]} <= deps
    s.cas.path_for(old["snapshot"]["sha256"]).unlink()
    before = snapshot(s)
    failed = commit(s, p, request(s, p, inverse, key="missing-offline"))
    assert failed["status"] not in {"accepted", "no_change"}
    assert snapshot(s) == before


@pytest.mark.parametrize("mode", ["version", "digest", "clock", "source", "project", "actor", "read-scope", "object-scope", "unowned", "missing", "changed", "unselected", "request", "dict"])
def test_capture_refusals_do_not_mutate(fixture, mode):
    from astrid.sdk.timeline.transcripts import TranscriptSourceSelection
    s, p = fixture
    d = source(s, p)
    body = request(s, p, reference(d))
    identity = copy.deepcopy(IDENTITY)
    selected = copy.deepcopy(d)
    project = p
    if mode == "version": selected["document"]["version"] = 2
    if mode == "digest":
        selected["document"]["content_digest"] = "sha256:" + "f" * 64
        selected["snapshot"] = dict(object_id="sha256:" + "f" * 64, sha256="f" * 64)
    if mode == "clock": selected["clock"]["origin_seconds"] = 1
    if mode == "source": selected["source"]["revision_id"] = "foreign"
    if mode == "project": project = "wrong-project"
    if mode == "actor": identity["actor"] = "foreign"
    if mode == "read-scope": identity["scopes"].remove("projects:read")
    if mode == "object-scope": identity["scopes"].remove("objects:read")
    if mode == "unowned": mutate(s, "DELETE FROM project_objects WHERE digest=?", (d["snapshot"]["sha256"],))
    if mode == "missing": s.cas.path_for(d["snapshot"]["sha256"]).unlink()
    if mode == "changed": s.cas.path_for(d["snapshot"]["sha256"]).write_bytes(b"changed")
    if mode == "unselected": body["change"]["commands"] = []
    # Selection itself remains only a locator, including valid forged pins.
    if mode in {"version", "digest", "clock", "source"}: body["change"]["commands"] = [reference(selected)]
    before = snapshot(s)
    with pytest.raises((ValueError, AuthorizationError, ConflictError, NotFoundError, ValidationError)):
        port = s._request_commit_port(body, identity)
        if mode == "request": body = dict(body, session_id="foreign")
        selection = selected if mode == "dict" else TranscriptSourceSelection.from_reference(project, selected)
        port.resolve_transcript_source(body, selection)
    assert snapshot(s) == before
    assert s.lookup_request(p, "main", body["request_id"]) is None


@pytest.mark.parametrize("mode", ["moved", "changed", "missing", "revoked", "forged-evidence"])
def test_source_rechecked_in_atomic_acceptance(fixture, monkeypatch, mode):
    s, p = fixture
    d = source(s, p)
    body = request(s, p, reference(d))
    original = s.accept
    baseline = []
    def accept(prepared, **kwargs):
        if mode == "moved": source(s, p, version=2, old=d)
        elif mode == "changed": s.cas.path_for(d["snapshot"]["sha256"]).write_bytes(b"changed")
        elif mode == "missing": s.cas.path_for(d["snapshot"]["sha256"]).unlink()
        elif mode == "revoked":
            def denied(*a): raise AuthorizationError("revoked")
            monkeypatch.setattr(s, "_assert_commit_authority", denied)
        else: prepared["evidence"]["transcripts"] = {}
        baseline.append(snapshot(s))
        return original(prepared, **kwargs)
    monkeypatch.setattr(s, "accept", accept)
    provider(s)
    if mode == "revoked":
        with pytest.raises(AuthorizationError):
            commit(s, p, body)
    else:
        result = commit(s, p, body)
        assert result["status"] not in {"accepted", "no_change"}, result
    assert len(baseline) == 1 and snapshot(s) == baseline[0]
    assert s.lookup_request(p, "main", body["request_id"]) is None


@pytest.mark.parametrize("mode", ["accept", "revoke", "rotate", "scope", "expiry"])
def test_authenticated_generated_route_rechecks_credential_at_accept(fixture, tmp_path, monkeypatch, mode):
    from banodoco_workspace_client import WorkspaceClient, ApiError
    from test_timeline_accept import http_server
    s, p = fixture
    d = source(s, p)
    body = request(s, p, reference(d))
    provider(s)
    server, thread, api = http_server(s, tmp_path)
    token, _ = server.credentials.provision(IDENTITY["actor"], IDENTITY["scopes"], rotate=True)
    client = WorkspaceClient(api.endpoint, token)
    original = s.accept
    baselines = []
    def accept(prepared, **kwargs):
        if mode == "revoke": server.credentials.revoke(IDENTITY["actor"])
        elif mode == "rotate": server.credentials.provision(IDENTITY["actor"], IDENTITY["scopes"], rotate=True)
        elif mode in {"scope", "expiry"}:
            meta = server.credentials.actor_metadata(IDENTITY["actor"])
            if mode == "scope": meta["scopes"] = ["projects:write", "objects:read"]
            else: meta["expires_at"] = time.time() - 1
            server.credentials._publish(IDENTITY["actor"], token, meta)
        baselines.append(snapshot(s))
        return original(prepared, **kwargs)
    monkeypatch.setattr(s, "accept", accept)
    try:
        if mode == "accept":
            result = client.commit_timeline(body)
            assert result["status"] == "accepted", result
            before = snapshot(s)
            assert client.commit_timeline(body) == result and snapshot(s) == before
        else:
            with pytest.raises(ApiError) as error:
                client.commit_timeline(body)
            assert error.value.status in {401, 403}
            assert snapshot(s) == baselines[0]
            assert s.lookup_request(p, "main", body["request_id"]) is None
        assert len(baselines) == 1
    finally:
        server.credentials.revoke(IDENTITY["actor"])
        server.shutdown()
        server.server_close()
        thread.join()
