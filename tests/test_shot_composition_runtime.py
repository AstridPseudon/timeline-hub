from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "packages" / "python"))
from astrid_runtime_client import ApiError, WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import ConflictError, NotFoundError, ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import digest, route_path
from runtime_protocol.timeline_commit_store import request_identity
from runtime_protocol.util import canonical_json
from baseline_fixture import load_baseline_fixture
from restore_history_fixture import load_restore_history_fixture


def _service(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "composition", "name": "Composition"}, idempotency_key="project")
    service.create_timeline(project["id"], "main", idempotency_key="timeline")
    return service, project["id"]


@pytest.fixture
def restore_provider(astrid_importable):
    # Restore semantics select the real provider explicitly via ASTRID_CHECKOUT.
    # Agent stays out of neutral Runtime startup and default collection.
    from astrid.sdk.timeline import commit as agent
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    return load_timeline_commit_provider("astrid")


def _select_restore_provider(service, project_id, provider):
    # Historical source capture or host acceptance is complete before Agent startup.
    service.register_timeline_commit_provider(provider)
    head = service.get_project_timeline(project_id, "main")
    return {"expected_head": head["head_revision_id"],
            "expected_publication_id": head["head_publication_id"]}


def _restore_history_service(tmp_path):
    fixture = load_restore_history_fixture(tmp_path)
    return RuntimeService(fixture.root), fixture


def _captured_media_service(tmp_path):
    service, project_id, (publication,) = load_baseline_fixture(tmp_path, "explicit-media")
    source = publication["data"]
    scene = source["payload"]["config"]["clips"][0]["app"]["liveScene"]["revision"]
    audio, = (pin["media_id"] for pin in source["dependency_manifest"]["media"] if pin["media_id"] != scene)
    return service, project_id, scene, audio


def _accept_composition_source(service, project_id, body, *, idempotency_key):
    """Seed source images through host acceptance, without a command provider.

    This is setup for read/integrity tests, not an authoring or legacy API
    success proof. The fixture view below contains normal source reads; the
    accepted mutation and its public head pair remain available separately.
    Every measured restore still selects the real Agent via ASTRID_CHECKOUT.
    """
    commits, _ = service._timeline_commits()
    if service.get_project_timeline(project_id, "main")["head_revision_id"] is None:
        base = commits.bootstrap(project_id, "main", authorize=lambda: None)
    else:
        base = commits.install_verified_baseline(project_id, "main", authorize=lambda: None)
    previous = commits.revision_closure(project_id, "main", base["revision_id"])
    payload = copy.deepcopy(body["parent_composition"])
    shots = copy.deepcopy(body.get("shot_revisions", previous["shot_revisions"]))
    internals = copy.deepcopy(body.get("internal_timeline_revisions", previous["internal_timeline_revisions"]))
    for shot in shots:
        shot["payload"]["internal_timeline_revision_id"] = shot["internal_timeline_revision_id"]
        shot["content_digest"] = digest(shot["payload"])
    for internal in internals:
        internal["content_digest"] = digest(internal["payload"])
    shots.sort(key=lambda image: (image["shot_id"], image["revision_id"]))
    internals.sort(key=lambda image: (image["timeline_id"], image["revision_id"]))
    document = {"schema_version": 1, "project_id": project_id, "timeline_id": "main",
                "parent_revision": {"revision_id": body["parent_revision_id"],
                                    "payload": payload, "content_digest": digest(payload)},
                "shot_revisions": shots, "internal_timeline_revisions": internals,
                "dependency_manifest": {
                    "shots": [{k: image[k] for k in ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest")}
                              for image in shots],
                    "internal_timelines": [{k: image[k] for k in ("timeline_id", "revision_id", "content_digest")}
                                           for image in internals],
                    "documents": [],
                    "media": sorted(body.get("dependency_manifest", {}).get("media", []),
                                    key=lambda pin: pin["media_id"])}}
    command = {"schema_version": 1, "op": "fixture.composition-source", "version": "1",
               "select": None, "args": {"document": copy.deepcopy(document)}}
    request = {"api_version": 1, "project_id": project_id, "timeline_id": "main",
               "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
               "commands": [command]}
    context = {"request": request, "idempotency_key": idempotency_key,
               "realm_id": service.realm["id"], "publisher": "restore-source-fixture",
               "invocation": {"operation": "commitTimeline", "path": route_path(project_id, "main"),
                              "body": copy.deepcopy(request)}}
    context["request_hash"] = request_identity(context)
    record = {"ordinal": 0, "command": command, "writes": [{
        "ref": "parent", "path": [field],
        "before": {"state": "present", "value": previous["parent_revision"]["payload"][field]},
        "after": {"state": "present", "value": payload[field]},
    } for field in ("config", "registry", "clips", "occurrences")],
        "reads": [], "selections": [], "bindings": [], "created": [], "dependencies": [], "derived_writes": []}
    prepared = {"expected_head": base, "canonical_document": document, "document_digest": digest(document),
                "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None},
                "id_map": {}, "semantic_events": [],
                "provider_version": "restore-source-fixture", "compiler_version": "restore-source-fixture"}
    accepted = commits.accept(context, prepared, authorize=lambda: None)
    source = service.get_project_parent_composition_revision(
        project_id, "main", accepted["data"]["accepted_revision_id"])
    assert commits.revision_closure(project_id, "main", source["revision_id"]) == document
    head = {"revision_id": source["revision_id"], "publication_id": accepted["receipt"]["receipt_id"]}
    public = service.get_project_timeline(project_id, "main")
    assert public["head_revision_id"] == head["revision_id"]
    assert public["head_publication_id"] == head["publication_id"]
    content_digests = {
        image["revision_id"]: service.get_project_shot_revision(
            project_id, image["shot_id"], image["revision_id"])["content_digest"]
        for image in shots
    }
    return {"data": {**source, "new_head": source["revision_id"], "content_digests": content_digests},
            "accepted": accepted, "head": head}


def _restore(service, project_id, revision, guards, *, idempotency_key):
    return service.restore_project_parent_composition_revision(
        project_id, "main", revision, guards, idempotency_key=idempotency_key,
        publisher="restore-editor", authorize=lambda: None,
        invocation_path=route_path(project_id, "main", f"composition-revisions/{revision}/restore"),
    )


def _publication(project_id, *, expected_head=None, parent_revision_id="parent-1", shot_revision_id="shot-rev-1", config=None):
    return {
        "project_id": project_id,
        "timeline_id": "main",
        "expected_head": expected_head,
        "parent_revision_id": parent_revision_id,
        "internal_timeline_revisions": [{
            "timeline_id": "main",
            "revision_id": "timeline-rev-1",
            # Integrity/CAS tests need a valid admitted picture closure. Empty
            # children are independently covered by seam rejection tests.
            "payload": {"tracks": [], "clips": [{"id": "picture", "clipType": "media", "at": 0, "hold": 1, "track": "video-1"}], "effects": [], "audio": [], "layout": {}, "registry": {}, "assets": []},
        }],
        "shot_revisions": [{
            "shot_id": "shot-1",
            "revision_id": shot_revision_id,
            "internal_timeline_revision_id": "timeline-rev-1",
            "payload": {"metadata": {"title": "opening"}, "items": [], "pools": [], "selected_variants": {}, "provenance": {}, "generation_inputs": {}, "audio_bindings": [], "text_bindings": []},
        }],
        "parent_composition": {
            "config": config or {},
            "registry": {},
            "clips": [],
            "occurrences": [{
                "occurrence_id": "occurrence-1",
                "shot_id": "shot-1",
                "shot_revision_id": shot_revision_id,
                "placement": {"start_ms": 0},
                "source_offset": 0,
                "duration_ms": 1000,
                "speed": 1,
                "track": "video-1",
                "transform": {},
                "gain": 1,
                "mute": False,
                "provenance": {},
            }],
        },
    }


def _publish_with_explicit_media(service, project_id, *, parent_revision_id="parent-media", accept_source=False):
    scene = service.ingest(
        project_id, b'{"schema":"live-scene-package/v1"}',
        media_type="application/json", original_name="scene.json",
        idempotency_key="scene-package",
    )["data"]["object_id"]
    audio = service.ingest(
        project_id, b"audio-object", media_type="audio/wav",
        original_name="tone.wav", idempotency_key="audio-object",
    )["data"]["object_id"]
    body = _explicit_media_publication(project_id, scene, audio, parent_revision_id=parent_revision_id)
    if accept_source:
        result = _accept_composition_source(
            service, project_id, body, idempotency_key=f"publish-{parent_revision_id}"
        )
    else:
        result = service.publish_parent_composition(
            project_id, "main", body, idempotency_key=f"publish-{parent_revision_id}"
        )
    return result, scene, audio


def _explicit_media_publication(project_id, scene, audio, *, parent_revision_id="parent-media"):
    body = _publication(project_id, parent_revision_id=parent_revision_id)
    body["parent_composition"]["config"]["clips"] = [{
        "clipType": "haus.astrid.liveScene",
        "app": {"liveScene": {"revision": scene, "source": {"objectId": scene, "revision": scene}}},
    }]
    body["dependency_manifest"] = {"media": [
        {"media_id": scene, "content_digest": scene},
        {"media_id": audio, "content_digest": audio},
    ]}
    return body


def _revision_errors(report):
    return report["checks"]["revisions"]["errors"]


def _rehash_timeline_events(service, timeline_id, *, replacements=None):
    replacements = replacements or {}
    previous = ""
    rows = service.store.conn.execute(
        "SELECT id, kind, payload_json, created_at FROM timeline_events WHERE timeline_id=? ORDER BY id",
        (timeline_id,),
    ).fetchall()
    for row in rows:
        payload = replacements.get(row["id"], json.loads(row["payload_json"]))
        event_hash = hashlib.sha256(canonical_json({
            "timeline_id": timeline_id,
            "kind": row["kind"],
            "payload": payload,
            "previous_hash": previous,
            "created_at": row["created_at"],
        }).encode()).hexdigest()
        service.store.conn.execute(
            "UPDATE timeline_events SET payload_json=?, previous_hash=?, event_hash=? WHERE id=?",
            (canonical_json(payload), previous, event_hash, row["id"]),
        )
        previous = event_hash


def test_historical_revision_is_exact_after_mutable_edits(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        first = _accept_composition_source(service, project_id, _publication(project_id), idempotency_key="publish-1")
        edited = _publication(project_id, parent_revision_id="parent-2", shot_revision_id="shot-rev-2")
        edited["shot_revisions"][0]["payload"]["name"] = "edited"
        _accept_composition_source(service, project_id, edited, idempotency_key="edit-shot")
        updated = {"data": service.get_project_shot_revision(project_id, "shot-1", "shot-rev-2")}
        assert updated["data"]["revision_id"] != first["data"]["revision_id"]
        assert service.store.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == updated["data"]["revision_id"]
        reread = service.get_project_shot_revision(project_id, "shot-1", "shot-rev-1")
        assert reread["content_digest"] == first["data"]["content_digests"]["shot-rev-1"]
        assert reread["payload"]["metadata"] == {"title": "opening"}
        assert service.get_project_timeline_revision(project_id, "main", "timeline-rev-1")["payload"]["layout"] == {}
    finally:
        service.close()


def test_parent_revision_and_head_reads_and_linked_reuse_do_not_regress_child_head(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        first = _accept_composition_source(service, project_id, _publication(project_id), idempotency_key="publish-1")
        parent = service.get_project_parent_composition_revision(project_id, "main", "parent-1")
        assert parent["content_digest"] == first["data"]["content_digest"]
        assert service._timeline_resource("main")["head_revision_id"] == "parent-1"

        reused = _publication(project_id, expected_head="parent-1", parent_revision_id="parent-2")
        second = _accept_composition_source(service, project_id, reused, idempotency_key="publish-2")
        assert second["data"]["new_head"] == "parent-2"
        assert service.store.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == "shot-rev-1"
    finally:
        service.close()


def test_parent_track_role_survives_immutable_publication_and_read(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id)
        body["parent_composition"]["config"]["tracks"] = [
            {"id": "output", "kind": "visual", "label": "Output", "role": "output"},
            {"id": "source", "kind": "visual", "label": "Source", "role": "source"},
        ]
        published = _accept_composition_source(
            service, project_id, body, idempotency_key="publish-track-roles"
        )

        reread = service.get_project_parent_composition_revision(
            project_id, "main", published["data"]["new_head"]
        )
        assert reread["content_digest"] == published["data"]["content_digest"]
        assert reread["payload"]["config"]["tracks"] == body["parent_composition"]["config"]["tracks"]
    finally:
        service.close()


@pytest.mark.parametrize("location", ["parent", "internal"])
def test_invalid_track_role_is_rejected_when_publishing_timeline_payload(tmp_path, location):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id, parent_revision_id=f"invalid-role-{location}")
        tracks = [{"id": "bad-role", "kind": "visual", "label": "Bad", "role": "draft"}]
        if location == "parent":
            body["parent_composition"]["config"]["tracks"] = tracks
        else:
            body["internal_timeline_revisions"][0]["payload"]["tracks"] = tracks

        with pytest.raises(ValidationError, match="track role"):
            service.publish_parent_composition(
                project_id, "main", body, idempotency_key=f"invalid-role-{location}"
            )
        assert service.store.conn.execute(
            "SELECT COUNT(*) FROM parent_composition_revisions"
        ).fetchone()[0] == 0
    finally:
        service.close()


def test_occurrence_only_linked_reuse_resolves_committed_child_closure(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        first = _accept_composition_source(service, project_id, _publication(project_id), idempotency_key="publish-1")
        reused = _publication(project_id, expected_head="parent-1", parent_revision_id="parent-2")
        reused.pop("shot_revisions")
        reused.pop("internal_timeline_revisions")
        second = _accept_composition_source(service, project_id, reused, idempotency_key="publish-2")

        assert second["data"]["dependency_manifest"] == first["data"]["dependency_manifest"]
        rows = service.store.conn.execute(
            "SELECT dependency_kind, dependency_id FROM composition_revision_dependencies WHERE parent_revision_id=? ORDER BY ordinal",
            ("parent-2",),
        ).fetchall()
        assert [(row["dependency_kind"], row["dependency_id"]) for row in rows] == [
            ("shot_revision", "shot-rev-1"),
            ("internal_timeline_revision", "timeline-rev-1"),
        ]
    finally:
        service.close()


def test_integrity_report_detects_occurrence_order_tampering(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id)
        second = copy.deepcopy(body["parent_composition"]["occurrences"][0])
        second["occurrence_id"] = "occurrence-2"
        second["placement"] = {"start_ms": 1000}
        body["parent_composition"]["occurrences"].append(second)
        _accept_composition_source(service, project_id, body, idempotency_key="publish-1")
        service.store.conn.execute(
            "UPDATE composition_revision_occurrences SET ordinal=CASE occurrence_id WHEN 'occurrence-1' THEN 1 ELSE 0 END WHERE parent_revision_id='parent-1'"
        )
        report = service.store.integrity_report()
        assert report["ok"] is False
        assert any(error["reason"] == "occurrence_sequence_mismatch" for error in report["checks"]["revisions"]["errors"])
    finally:
        service.close()


def test_integrity_report_detects_occurrence_identity_tampering(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _accept_composition_source(service, project_id, _publication(project_id), idempotency_key="publish-1")
        service.store.conn.execute(
            "UPDATE composition_revision_occurrences SET occurrence_id='tampered' WHERE parent_revision_id='parent-1'"
        )
        report = service.store.integrity_report()
        assert report["ok"] is False
        assert any(error["reason"] in {"occurrence_missing", "occurrence_extra", "occurrence_sequence_mismatch"} for error in report["checks"]["revisions"]["errors"])
    finally:
        service.close()


def test_integrity_report_detects_revision_digest_tampering(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _accept_composition_source(service, project_id, _publication(project_id), idempotency_key="publish-1")
        service.store.conn.execute("UPDATE parent_composition_revisions SET content_digest='sha256:' || printf('%064d', 0) WHERE id='parent-1'")
        report = service.store.integrity_report()
        assert report["ok"] is False
        assert "revisions" in report["issues"]
        assert any(error["reason"] == "content_digest_mismatch" for error in report["checks"]["revisions"]["errors"])
    finally:
        service.close()


def test_integrity_report_accepts_media_pinned_by_publication_evidence(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _publish_with_explicit_media(service, project_id, accept_source=True)
        report = service.store.integrity_report()
        assert report["ok"] is True, report["checks"]["revisions"]["errors"]
        assert report["checks"]["event_chain"]["ok"] is True
    finally:
        service.close()


@pytest.mark.parametrize("fault", ["healthy", "missing_cas", "missing_dependency"])
def test_doctor_preserves_cas_missing_after_parent_dependency_check(tmp_path, fault):
    service, project_id = _service(tmp_path)
    root = service.store.root
    try:
        _, _, audio = _publish_with_explicit_media(service, project_id, accept_source=True)
        if fault == "missing_cas":
            digest = audio.removeprefix('sha256:')
            (service.store.cas_root / digest[:2] / digest[2:]).unlink()
        elif fault == "missing_dependency":
            service.store.conn.execute(
                "DELETE FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_id=?",
                ("parent-media", audio),
            )
        report = service.store.integrity_report()
        expected_missing = [audio.removeprefix("sha256:")] if fault == "missing_cas" else []
        assert report["checks"]["cas_missing"] == expected_missing
        assert report["checks"]["reachable_cas"]["missing"] == expected_missing
        assert report["checks"]["reachable_cas"]["ok"] is (fault != "missing_cas")
        assert report["ok"] is (fault == "healthy")
        if fault == "missing_dependency":
            assert any(error["reason"] == "dependency_graph_mismatch" for error in _revision_errors(report))
        wire_report = json.loads(json.dumps(report))
        assert wire_report["checks"]["cas_missing"] == expected_missing
        assert wire_report["ok"] is (fault == "healthy")
    finally:
        service.close()
    completed = subprocess.run(
        [sys.executable, "-m", "runtime_protocol", "doctor", "--root", str(root), "--json", "--deep"],
        cwd=Path(__file__).parents[1], capture_output=True, text=True, timeout=20,
    )
    assert completed.returncode == (0 if fault == "healthy" else 1), completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["checks"]["cas_missing"] == expected_missing
    assert observed["ok"] is (fault == "healthy")


def test_integrity_report_rejects_undeclared_media_dependency(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _publish_with_explicit_media(service, project_id, accept_source=True)
        extra = service.ingest(
            project_id, b"undeclared-object", media_type="application/octet-stream",
            idempotency_key="undeclared-object",
        )["data"]["object_id"]
        service.store.conn.execute(
            "INSERT INTO composition_revision_dependencies(parent_revision_id, dependency_kind, dependency_id, content_digest, ordinal) VALUES (?, 'media', ?, ?, 2)",
            ("parent-media", extra, extra),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "dependency_graph_mismatch" for error in _revision_errors(report)), _revision_errors(report)
    finally:
        service.close()


def test_integrity_report_rejects_missing_manifest_media_dependency(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _, _, audio = _publish_with_explicit_media(service, project_id, accept_source=True)
        service.store.conn.execute(
            "DELETE FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_id=?",
            ("parent-media", audio),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "dependency_graph_mismatch" for error in _revision_errors(report))
    finally:
        service.close()


def test_integrity_report_rejects_wrong_project_media_dependency(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _, _, audio = _publish_with_explicit_media(service, project_id, accept_source=True)
        other = service.create_project({"slug": "other", "name": "Other"}, idempotency_key="other-project")
        foreign = service.ingest(
            other["id"], b"foreign-object", media_type="application/octet-stream",
            idempotency_key="foreign-object",
        )["data"]["object_id"]
        service.store.conn.execute(
            "UPDATE composition_revision_dependencies SET dependency_id=?, content_digest=? WHERE parent_revision_id=? AND dependency_id=?",
            (foreign, foreign, "parent-media", audio),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "dependency_closure" for error in _revision_errors(report))
    finally:
        service.close()


def test_integrity_report_rejects_dependency_digest_mismatch(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        _, scene, _ = _publish_with_explicit_media(service, project_id, accept_source=True)
        service.store.conn.execute(
            "UPDATE composition_revision_dependencies SET content_digest=? WHERE parent_revision_id=? AND dependency_id=?",
            ("sha256:" + "0" * 64, "parent-media", scene),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "dependency_closure" for error in _revision_errors(report))
    finally:
        service.close()


@pytest.mark.parametrize("tamper", ["duplicate", "noncontiguous"])
def test_integrity_report_rejects_duplicate_or_noncontiguous_dependencies(tmp_path, tamper):
    service, project_id = _service(tmp_path)
    try:
        _, scene, audio = _publish_with_explicit_media(service, project_id, accept_source=True)
        if tamper == "duplicate":
            service.store.conn.execute(
                "INSERT INTO composition_revision_dependencies(parent_revision_id, dependency_kind, dependency_id, content_digest, ordinal) VALUES (?, 'media', ?, ?, 2)",
                ("parent-media", scene, scene),
            )
        else:
            service.store.conn.execute(
                "UPDATE composition_revision_dependencies SET ordinal=4 WHERE parent_revision_id=? AND dependency_id=?",
                ("parent-media", audio),
            )
        report = service.store.integrity_report()
        assert any(error["reason"] == "dependency_graph_mismatch" for error in _revision_errors(report)), _revision_errors(report)
    finally:
        service.close()


def test_integrity_report_rejects_inconsistent_publication_evidence(tmp_path):
    service, project_id, scene, audio = _captured_media_service(tmp_path)
    try:
        event = service.store.conn.execute(
            "SELECT id, payload_json FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        ).fetchone()
        payload = json.loads(event["payload_json"])
        payload["dependency_manifest"]["media"].pop()
        _rehash_timeline_events(service, "main", replacements={event["id"]: payload})
        report = service.store.integrity_report()
        assert report["checks"]["event_chain"]["ok"] is True
        assert any(error["reason"] == "publication_evidence_mismatch" for error in _revision_errors(report))
    finally:
        service.close()


def test_integrity_report_rejects_manifest_receipt_paired_with_manifestless_event(tmp_path):
    service, project_id, scene, audio = _captured_media_service(tmp_path)
    try:
        event = service.store.conn.execute(
            "SELECT id, payload_json FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        ).fetchone()
        payload = json.loads(event["payload_json"])
        del payload["dependency_manifest"]
        _rehash_timeline_events(service, "main", replacements={event["id"]: payload})
        report = service.store.integrity_report()
        assert report["checks"]["event_chain"]["ok"] is True
        assert any(error["reason"] == "publication_evidence_mismatch" for error in _revision_errors(report)), _revision_errors(report)
    finally:
        service.close()


def test_integrity_report_does_not_trust_manifest_without_publication_event(tmp_path):
    service, project_id, scene, audio = _captured_media_service(tmp_path)
    try:
        service.store.conn.execute(
            "DELETE FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "publication_evidence_mismatch" for error in _revision_errors(report))
    finally:
        service.close()


def test_integrity_report_rejects_receipt_for_missing_event_even_without_manifest_rows(tmp_path):
    service, project_id, scene, audio = _captured_media_service(tmp_path)
    try:
        service.store.conn.execute(
            "DELETE FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        )
        service.store.conn.execute(
            "DELETE FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_id IN (?, ?)",
            ("parent-media", scene, audio),
        )
        report = service.store.integrity_report()
        assert any(error["reason"] == "publication_evidence_mismatch" for error in _revision_errors(report)), _revision_errors(report)
        assert not any(error["reason"] == "dependency_graph_mismatch" for error in _revision_errors(report)), _revision_errors(report)
    finally:
        service.close()


def test_integrity_report_keeps_payload_only_legacy_closure_without_event(tmp_path):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        service.store.conn.execute(
            "DELETE FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        )
        service.store.conn.execute(
            "DELETE FROM command_idempotency WHERE command_kind=? AND aggregate_id=?",
            ("parent_composition.publish", "main"),
        )
        report = service.store.integrity_report()
        assert report["ok"] is True, report["checks"]["revisions"]["errors"]
    finally:
        service.close()


def test_integrity_report_accepts_identical_parent_republished_with_new_key(tmp_path):
    service, project_id, scene, audio = _captured_media_service(tmp_path)
    try:
        body = _explicit_media_publication(project_id, scene, audio)
        body["expected_head"] = "parent-media"
        body["parent_composition"] = service.get_project_parent_composition_revision(
            project_id, "main", "parent-media")["payload"]
        body.pop("shot_revisions")
        body.pop("internal_timeline_revisions")
        _accept_composition_source(
            service, project_id, body, idempotency_key="publish-parent-media-again"
        )
        report = service.store.integrity_report()
        assert report["ok"] is True, report["checks"]["revisions"]["errors"]
    finally:
        service.close()


def test_integrity_report_rejects_conflicting_repeat_publication_manifests(tmp_path):
    service, project_id, publications = load_baseline_fixture(tmp_path, "repeat-media")
    source = publications[0]["data"]
    scene = source["payload"]["config"]["clips"][0]["app"]["liveScene"]["revision"]
    audio, = (pin["media_id"] for pin in source["dependency_manifest"]["media"] if pin["media_id"] != scene)
    assert [publication["receipt"]["idempotency_key"] for publication in publications] == [
        "publish-parent-media", "publish-parent-media-again",
    ]
    try:
        event = service.store.conn.execute(
            "SELECT id, payload_json FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published' ORDER BY id DESC LIMIT 1",
            ("main",),
        ).fetchone()
        event_payload = json.loads(event["payload_json"])
        event_payload["dependency_manifest"]["media"].pop()
        _rehash_timeline_events(service, "main", replacements={event["id"]: event_payload})
        receipt = service.store.conn.execute(
            "SELECT idempotency_key, result_json FROM command_idempotency WHERE command_kind=? AND idempotency_key=?",
            ("parent_composition.publish", "publish-parent-media-again"),
        ).fetchone()
        result = json.loads(receipt["result_json"])
        result["dependency_manifest"] = event_payload["dependency_manifest"]
        service.store.conn.execute(
            "UPDATE command_idempotency SET result_json=? WHERE command_kind=? AND idempotency_key=?",
            (canonical_json(result), "parent_composition.publish", receipt["idempotency_key"]),
        )
        report = service.store.integrity_report()
        assert report["checks"]["event_chain"]["ok"] is True
        assert any(error["reason"] == "publication_evidence_mismatch" for error in _revision_errors(report)), _revision_errors(report)
    finally:
        service.close()


def test_integrity_report_checks_timeline_event_hash_chain(tmp_path):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        event_id = service.store.conn.execute(
            "SELECT id FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published'",
            ("main",),
        ).fetchone()["id"]
        service.store.conn.execute("UPDATE timeline_events SET event_hash='broken' WHERE id=?", (event_id,))
        report = service.store.integrity_report()
        assert report["checks"]["event_chain"]["ok"] is False
        assert any(error.get("stream") == "timeline" and error["reason"] == "hash_mismatch" for error in report["checks"]["event_chain"]["errors"])
    finally:
        service.close()


def test_stale_publication_rolls_back_and_retry_conflicts(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        first = service.publish_parent_composition(project_id, "main", _publication(project_id), idempotency_key="publish-1")
        before = {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in ("shot_revisions", "internal_timeline_revisions", "parent_composition_revisions", "timeline_events", "command_idempotency")}
        stale = _publication(project_id, expected_head=None, parent_revision_id="parent-2", shot_revision_id="shot-rev-2", config={"changed": True})
        with pytest.raises(ConflictError, match="stale"):
            service.publish_parent_composition(project_id, "main", stale, idempotency_key="publish-2")
        after = {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in before}
        assert after == before
        assert service.store.conn.execute("SELECT revision_id FROM parent_composition_heads WHERE timeline_id='main'").fetchone()[0] == first["data"]["new_head"]
        with pytest.raises(ConflictError, match="different input"):
            service.publish_parent_composition(project_id, "main", _publication(project_id, parent_revision_id="parent-1", config={"different": True}), idempotency_key="publish-1")
    finally:
        service.close()


def test_lost_response_replay_returns_original_head_after_a_newer_publish(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        first_body = _publication(project_id)
        first = service.publish_parent_composition(
            project_id, "main", first_body, idempotency_key="publish-lost-response"
        )
        second_body = _publication(
            project_id,
            expected_head="parent-1",
            parent_revision_id="parent-2",
            shot_revision_id="shot-rev-2",
            config={"writer": 2},
        )
        service.publish_parent_composition(
            project_id, "main", second_body, idempotency_key="publish-second-writer"
        )

        replay = service.publish_parent_composition(
            project_id, "main", copy.deepcopy(first_body), idempotency_key="publish-lost-response"
        )

        assert replay == first
        assert replay["data"]["new_head"] == "parent-1"
        assert replay["receipt"]["result"]["new_head"] == "parent-1"
        assert service._timeline_resource("main")["head_revision_id"] == "parent-2"
    finally:
        service.close()


def test_same_head_concurrent_publishers_have_one_winner(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        def publish(index):
            body = _publication(project_id, parent_revision_id=f"parent-{index}", shot_revision_id=f"shot-rev-{index}")
            try:
                return service.publish_parent_composition(project_id, "main", body, idempotency_key=f"publish-{index}")
            except ConflictError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(publish, (1, 2)))
        assert sum(value is not None for value in results) == 1
        assert service.store.conn.execute("SELECT COUNT(*) FROM parent_composition_revisions").fetchone()[0] == 1
    finally:
        service.close()


def test_dependency_scope_and_nesting_are_rejected(tmp_path):
    service, project_id = _service(tmp_path)
    other_project = service.create_project({"slug": "other", "name": "Other"}, idempotency_key="other-project")["id"]
    service.create_timeline(other_project, "other", idempotency_key="other-timeline")
    try:
        missing = _publication(project_id)
        missing["parent_composition"]["occurrences"][0]["shot_revision_id"] = "does-not-exist"
        with pytest.raises(NotFoundError, match="dependency"):
            service.publish_parent_composition(project_id, "main", missing, idempotency_key="missing")

        nested = _publication(project_id, parent_revision_id="nested")
        nested["internal_timeline_revisions"][0]["payload"]["occurrences"] = []
        with pytest.raises(ValidationError, match="nested"):
            service.publish_parent_composition(project_id, "main", nested, idempotency_key="nested")

        service.publish_parent_composition(project_id, "main", _publication(project_id), idempotency_key="base")
        cross_project = _publication(other_project, parent_revision_id="cross", shot_revision_id="shot-rev-cross")
        cross_project["timeline_id"] = "other"
        cross_project["shot_revisions"][0]["shot_id"] = "shot-1"
        cross_project["parent_composition"]["occurrences"][0]["shot_id"] = "shot-1"
        with pytest.raises(ConflictError, match="different project"):
            service.publish_parent_composition(other_project, "other", cross_project, idempotency_key="cross")
    finally:
        service.close()


def test_failure_injection_rolls_back_every_publication_write(tmp_path, monkeypatch):
    service, project_id = _service(tmp_path)
    try:
        command_count = service.store.conn.execute("SELECT COUNT(*) FROM command_idempotency").fetchone()[0]
        baseline = {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in ("project_shots", "shot_items", "shot_revisions", "internal_timeline_revisions", "parent_composition_revisions", "shot_revision_heads", "parent_composition_heads", "composition_revision_occurrences", "composition_revision_dependencies")}
        monkeypatch.setattr(service.store, "_append_timeline_event", lambda *args: (_ for _ in ()).throw(RuntimeError("injected")))
        with pytest.raises(RuntimeError, match="injected"):
            service.publish_parent_composition(project_id, "main", _publication(project_id), idempotency_key="injected")
        for table in ("project_shots", "shot_items", "shot_revisions", "internal_timeline_revisions", "parent_composition_revisions", "shot_revision_heads", "parent_composition_heads", "composition_revision_occurrences", "composition_revision_dependencies"):
            assert service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == baseline[table]
        assert service.store.conn.execute("SELECT COUNT(*) FROM command_idempotency").fetchone()[0] == command_count
        assert service.store.conn.execute("SELECT COUNT(*) FROM timeline_events WHERE timeline_id='main'").fetchone()[0] == 1
    finally:
        service.close()


def test_publication_preserves_opaque_parent_and_occurrence_fields(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id)
        body["parent_composition"]["opaque_parent"] = {"future": [1, 2, 3]}
        occurrence = body["parent_composition"]["occurrences"][0]
        occurrence["placement"]["opaque_geometry"] = {"anchor": "center"}
        occurrence["opaque_occurrence"] = {"future_schema": True}

        published = _accept_composition_source(
            service, project_id, body, idempotency_key="opaque-publication"
        )
        reread = service.get_project_parent_composition_revision(
            project_id, "main", published["data"]["new_head"]
        )

        assert reread["payload"]["opaque_parent"] == {"future": [1, 2, 3]}
        stored = reread["payload"]["occurrences"][0]
        assert stored["opaque_occurrence"] == {"future_schema": True}
        assert stored["placement"]["opaque_geometry"] == {"anchor": "center"}
    finally:
        service.close()


def test_publication_preserves_open_shot_payload_without_manufacturing_legacy_audio(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id)
        payload = body["shot_revisions"][0]["payload"]
        payload["name"] = "Open payload"
        payload["metadata"]["future_nested"] = {"values": [1, {"two": True}]}
        payload["future_sibling"] = {"mode": "opaque", "value": None}
        payload.pop("audio_bindings")

        published = _accept_composition_source(
            service, project_id, body, idempotency_key="open-shot-payload"
        )
        reread = service.get_project_shot_revision(
            project_id, "shot-1", "shot-rev-1"
        )

        assert reread["content_digest"] == published["data"]["content_digests"]["shot-rev-1"]
        assert reread["payload"]["name"] == "Open payload"
        assert reread["payload"]["metadata"]["future_nested"] == {"values": [1, {"two": True}]}
        assert reread["payload"]["future_sibling"] == {"mode": "opaque", "value": None}
        assert "audio" not in reread["payload"]
    finally:
        service.close()


def test_missing_selected_media_rejects_publication_without_identity_leak(tmp_path):
    service, project_id = _service(tmp_path)
    try:
        body = _publication(project_id)
        missing = "sha256:" + "f" * 64
        body["shot_revisions"][0]["payload"]["items"] = [
            {"item_id": "missing-item", "media_id": missing, "metadata": {}}
        ]
        before = {
            table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ("project_shots", "shot_items", "shot_revisions", "internal_timeline_revisions")
        }

        with pytest.raises(NotFoundError, match="media dependency"):
            service.publish_parent_composition(
                project_id, "main", body, idempotency_key="missing-selected-media"
            )

        after = {
            table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in before
        }
        assert after == before
    finally:
        service.close()


def test_parent_composition_history_paginates_and_restores_exact_closure_over_http(tmp_path, restore_provider):
    fixture = load_restore_history_fixture(tmp_path)
    project_id = fixture.project_id
    daemon = RuntimeDaemon(fixture.root, support_root=tmp_path / "support").start()
    try:
        service = daemon.service
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        second = {"new_head": fixture.head["revision_id"]}

        page_one, cursor = client.list_project_parent_composition_revisions(
            project_id, "main", limit=1
        )
        page_two, next_cursor = client.list_project_parent_composition_revisions(
            project_id, "main", cursor=cursor, limit=1
        )
        assert cursor and next_cursor is None
        assert [page_one[0]["revision_id"], page_two[0]["revision_id"]] == ["parent-2", "parent-1"]
        assert page_one[0]["is_current_head"] is True
        assert page_two[0]["is_current_head"] is False

        guards = _select_restore_provider(service, project_id, restore_provider)
        assert guards["expected_head"] == second["new_head"]
        before = {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                  for table in ("shot_revisions", "internal_timeline_revisions", "timeline_commit_history")}
        restored = client.restore_project_parent_composition_revision(
            project_id, "main", "parent-1", **guards,
            idempotency_key="history-restore",
        )
        restored_head = restored["data"]["accepted_revision_id"]
        # Revision content may be reused; the accepted publication is always new.
        assert restored["receipt"]["result"] == restored["data"]
        assert restored["receipt"]["receipt_id"] != guards["expected_publication_id"]
        source_publication = service.list_timeline_commits(
            project_id, "main", authorize=lambda: None,
        )["items"][0]["publication_id"]
        assert restored["receipt"]["receipt_id"] != source_publication
        assert restored["data"]["canonical_document"]["parent_revision"]["revision_id"] == restored_head
        assert service.get_project_timeline(project_id, "main")["head_publication_id"] == restored["receipt"]["receipt_id"]
        assert client.get_project_parent_composition_revision(
            project_id, "main", restored_head
        )["payload"] == client.get_project_parent_composition_revision(
            project_id, "main", "parent-1"
        )["payload"]
        commits = service._timeline_commits()[0]
        source = commits.revision_closure(project_id, "main", "parent-1")
        accepted = restored["data"]["canonical_document"]
        for field in ("shot_revisions", "internal_timeline_revisions", "dependency_manifest"):
            assert accepted[field] == source[field]
        before_replay = tuple(service.store.conn.iterdump())
        replay = client.restore_project_parent_composition_revision(
            project_id, "main", "parent-1", **guards,
            idempotency_key="history-restore",
        )
        assert replay == restored
        assert tuple(service.store.conn.iterdump()) == before_replay
        assert {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in before} == {**before, "timeline_commit_history": before["timeline_commit_history"] + 1}
        with pytest.raises(ApiError) as error:
            client.restore_project_parent_composition_revision(
                project_id, "main", "parent-1", **guards,
                idempotency_key="history-restore-stale-pair",
            )
        assert error.value.status == 409
        assert error.value.details["reason"] == "stale_head"
    finally:
        daemon.stop()


def test_parent_composition_history_lists_broken_rows_but_restore_rejects_tampered_dependencies(tmp_path, restore_provider):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        guards = _select_restore_provider(service, project_id, restore_provider)
        service.store.conn.execute(
            "UPDATE shot_revisions SET content_digest=? WHERE id='shot-rev-1'",
            ("sha256:" + "0" * 64,),
        )

        page = service.list_project_parent_composition_revisions(project_id, "main")
        assert {item["revision_id"] for item in page["items"]} == {"parent-1", "parent-2"}
        before = {
            table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in (
                "parent_composition_revisions", "parent_composition_heads",
                "composition_revision_dependencies", "timeline_events",
                "command_idempotency", "runs", "tasks",
            )
        }
        before_rows = tuple(service.store.conn.iterdump())
        with pytest.raises(
            ConflictError,
            match="historical parent composition dependency closure failed immutable verification",
        ):
            _restore(
                service, project_id, "parent-1", guards,
                idempotency_key="history-restore-broken-source",
            )
        after = {
            table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in before
        }
        assert after == before
        assert tuple(service.store.conn.iterdump()) == before_rows
        assert service._timeline_resource("main")["head_revision_id"] == "parent-2"
    finally:
        service.close()


def test_parent_composition_restore_preserves_payload_and_declared_media_dependency_closure(tmp_path, restore_provider):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        payload_media = service.ingest(
            project_id, b"history-payload-media", media_type="audio/wav",
            idempotency_key="history-payload-media",
        )["data"]["object_id"]
        declared_extra = service.ingest(
            project_id, b"history-declared-extra", media_type="application/octet-stream",
            idempotency_key="history-declared-extra",
        )["data"]["object_id"]
        first_body = _publication(project_id, parent_revision_id="parent-with-media")
        first_body["internal_timeline_revisions"] = []
        first_body["shot_revisions"] = []
        first_body["parent_composition"] = {
            "config": {"clips": []},
            "registry": {"assets": {"payload": {
                "media_id": payload_media,
                "content_sha256": payload_media,
                "type": "audio",
            }}},
            "clips": [],
            "occurrences": [],
        }
        first_body["dependency_manifest"] = {"media": [
            {"media_id": payload_media, "content_digest": payload_media},
            {"media_id": declared_extra, "content_digest": declared_extra},
        ]}
        first = _accept_composition_source(
            service, project_id, first_body, idempotency_key="history-publish-media"
        )
        later = _publication(
            project_id, expected_head="parent-with-media", parent_revision_id="parent-after-media"
        )
        later["internal_timeline_revisions"] = []
        later["shot_revisions"] = []
        later["parent_composition"] = {"config": {"clips": []}, "registry": {}, "clips": [], "occurrences": []}
        _accept_composition_source(
            service, project_id, later, idempotency_key="history-publish-after-media"
        )

        guards = _select_restore_provider(service, project_id, restore_provider)
        restored = _restore(
            service, project_id, "parent-with-media", guards,
            idempotency_key="history-restore-media",
        )
        restored_head = restored["data"]["accepted_revision_id"]
        assert restored["data"]["canonical_document"]["parent_revision"]["payload"] == first["data"]["payload"]
        assert {
            item["media_id"] for item in restored["data"]["canonical_document"]["dependency_manifest"]["media"]
        } == {payload_media, declared_extra}
        dependencies = service.store.conn.execute(
            "SELECT dependency_kind, dependency_id, content_digest FROM composition_revision_dependencies "
            "WHERE parent_revision_id=? ORDER BY ordinal",
            (restored_head,),
        ).fetchall()
        assert {
            (row["dependency_kind"], row["dependency_id"], row["content_digest"])
            for row in dependencies
        } == {("media", value, value) for value in (payload_media, declared_extra)}
    finally:
        service.close()


@pytest.mark.parametrize("admission_seconds", [5.0, 120.0])
def test_parent_composition_restore_uses_selected_admission_integrity_budget(tmp_path, monkeypatch, admission_seconds, restore_provider):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        first = fixture.first
        guards = _select_restore_provider(service, project_id, restore_provider)
        service.store.admission_timeout = admission_seconds
        original = service.store.integrity_report
        observed = []

        def selected_report(*, catalog_path=None, timeout_seconds=None):
            observed.append(timeout_seconds)
            return original(catalog_path=catalog_path, timeout_seconds=timeout_seconds)

        monkeypatch.setattr(service.store, "integrity_report", selected_report)
        restored = _restore(
            service, project_id, "parent-1", guards,
            idempotency_key="restore-budget-selected",
        )
        assert observed == [admission_seconds]
        assert restored["data"]["canonical_document"]["parent_revision"]["payload"] == first["data"]["payload"]
        assert restored["data"]["canonical_document"]["parent_revision"]["content_digest"] == first["data"]["content_digest"]
        assert service._timeline_resource("main")["head_revision_id"] == restored["data"]["accepted_revision_id"]
    finally:
        service.close()


def test_parent_composition_restore_refuses_incomplete_integrity_at_selected_budget(tmp_path, monkeypatch, restore_provider):
    service, fixture = _restore_history_service(tmp_path)
    project_id = fixture.project_id
    try:
        guards = _select_restore_provider(service, project_id, restore_provider)
        service.store.admission_timeout = 120.0
        observed = []

        def incomplete_report(*, timeout_seconds):
            observed.append(timeout_seconds)
            return RealmStore._integrity_failure("timeout", "bounded inspection exhausted")

        monkeypatch.setattr(service.store, "integrity_report", incomplete_report)
        tables = ("parent_composition_revisions", "parent_composition_heads", "composition_revision_dependencies", "timeline_events", "command_idempotency", "runs", "tasks")
        def counts():
            return {table: service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in tables}
        before = counts()
        before_rows = tuple(service.store.conn.iterdump())
        with pytest.raises(ConflictError, match="dependency closure failed immutable verification") as failure:
            _restore(
                service, project_id, "parent-1", guards,
                idempotency_key="restore-incomplete-refused",
            )
        assert observed == [120.0]
        assert failure.value.details["errors"] == [{"reason": "integrity_report_unavailable"}]
        assert counts() == before
        assert tuple(service.store.conn.iterdump()) == before_rows
        assert service._timeline_resource("main")["head_revision_id"] == "parent-2"
    finally:
        service.close()


def test_stale_head_conflict_carries_machine_readable_reason_over_http(tmp_path, restore_provider):
    """Clients classify a lost head race by details.reason, never by message text."""
    fixture = load_restore_history_fixture(tmp_path)
    project_id = fixture.project_id
    daemon = RuntimeDaemon(fixture.root, support_root=tmp_path / "support").start()
    try:
        service = daemon.service
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        guards = _select_restore_provider(service, project_id, restore_provider)
        current = fixture.head
        source_publication = fixture.first["receipt"]["receipt_id"]
        # The retired publish CAS (expected_head/actual_head) is now the restore
        # head-pair CAS (base/current). Check publication-only and revision races.
        for base, key in [
            ({"revision_id": current["revision_id"], "publication_id": source_publication},
             "stale-publication"),
            ({"revision_id": "parent-1", "publication_id": source_publication}, "stale-revision"),
        ]:
            before = tuple(service.store.conn.iterdump())
            with pytest.raises(ApiError) as stale:
                client.restore_project_parent_composition_revision(
                    project_id, "main", "parent-1", expected_head=base["revision_id"],
                    expected_publication_id=base["publication_id"], idempotency_key=key,
                )
            assert (stale.value.status, stale.value.code) == (409, "conflict")
            assert stale.value.message == "restore requires the exact head pair"
            assert stale.value.details == {
                "status": "refused", "reason": "stale_head", "base": base,
                "current": current, "conflicts": [],
            }
            assert tuple(service.store.conn.iterdump()) == before

        client.restore_project_parent_composition_revision(
            project_id, "main", "parent-1", **guards, idempotency_key="restore-once",
        )
        before = tuple(service.store.conn.iterdump())
        # Changed retry payload remains a distinct 409 on the current route.
        with pytest.raises(ApiError) as reuse:
            client.restore_project_parent_composition_revision(
                project_id, "main", "parent-1", expected_head=guards["expected_head"],
                expected_publication_id=source_publication, idempotency_key="restore-once",
            )
        assert (reuse.value.status, reuse.value.code) == (409, "conflict")
        assert reuse.value.message == "idempotency_mismatch"
        assert reuse.value.details == {
            "status": "refused", "reason": "idempotency_mismatch", "base": None,
            "current": None, "conflicts": [],
        }
        assert tuple(service.store.conn.iterdump()) == before
    finally:
        daemon.stop()


def test_canonical_payload_mismatch_conflict_carries_machine_readable_reason():
    from runtime_protocol import timeline_inspection, visual_seam
    payload = {"clips": [{"id": "a"}], "config": {"clips": [{"id": "b"}]}}
    for raise_it in (lambda: visual_seam.parent_clips(payload), lambda: timeline_inspection._canonical_parent_clips(payload)):
        with pytest.raises(ConflictError) as error:
            raise_it()
        assert error.value.as_dict() == {
            "code": "conflict",
            "message": "canonical parent clips and config.clips disagree",
            "details": {"reason": "canonical_payload_mismatch"},
        }
