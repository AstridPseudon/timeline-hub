"""Future-cohort proof for the original owned-raw, unplaced reference case.

This module is intentionally collected on current Runtime but only executed
with the matched private Agent/Runtime source pair named in the handoff.
"""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from test_timeline_commit_integration import agent  # noqa: F401 (shared fixture)


pytestmark = pytest.mark.integration


def _head(service, project):
    value = service.get_project_timeline(project, "main")
    return {"revision_id": value["head_revision_id"],
            "publication_id": value["head_publication_id"]}


def _document(service, project, revision=None):
    return service._timeline_commits()[0].revision_closure(
        project, "main", revision or _head(service, project)["revision_id"]
    )


def _body(project, base, command):
    return {
        "api_version": 1,
        "project_id": project,
        "timeline_id": "main",
        "base_revision_id": base["revision_id"],
        "base_publication_id": base["publication_id"],
        "commands": [copy.deepcopy(command)],
        "source": {"via": "python"},
    }


def _commit(service, project, body, key):
    return service.commit_timeline(
        project, "main", body, idempotency_key=key,
        publisher="rt03-native-proof",
        invocation_path=route_path(project, "main"), authorize=lambda: None,
    )


def _media(service, project, content, name):
    value = service.ingest(
        project, content, media_type="application/octet-stream",
        original_name=name, idempotency_key=name,
    )["data"]
    pin = {"media_id": value["object_id"], "content_digest": value["object_id"]}
    return pin


def _reference_command(service, project, agent, reference_id, pin, *, read_project=None, document=None):
    # Both the command capture and Runtime acceptance use the real raw custody
    # descriptor; no test-authored media metadata enters this case.
    from runtime_protocol.timeline_commit_port import MediaReads
    from astrid.sdk.timeline.native_parent_reference_commands import capture_timeline_reference

    read_project = project if read_project is None else read_project
    info = MediaReads(service).raw_media_info(read_project, pin)
    return capture_timeline_reference(
        agent.bundle(document or _document(service, project)), reference_id, pin,
        verified_media=[{"raw_pin": copy.deepcopy(pin), "media_info": info}],
    )


def _projection(service):
    rows = [dict(row) for row in service.store.conn.execute(
        "SELECT id, object_id, role FROM timeline_references "
        "WHERE timeline_id='main' ORDER BY id"
    )]
    row = service.store.conn.execute(
        "SELECT shots_json, references_json FROM timeline_revisions "
        "WHERE timeline_id='main' ORDER BY version DESC LIMIT 1"
    ).fetchone()
    return rows, {"shots": json.loads(row[0]), "references": json.loads(row[1])}


def test_actual_provider_preserves_original_owned_unplaced_reference_contract(
        tmp_path, agent, monkeypatch):
    """Exercise Agent1022 timeline.reference through the normal Runtime door."""
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        service.register_timeline_commit_provider(agent.provider())
        project = service.create_project({"slug": "rt03-native", "name": "RT03 native"})["id"]
        service.create_timeline(project, "main", idempotency_key="rt03-main")
        unrelated_pin = _media(service, project, b"unrelated-owned-raw", "unrelated.raw")
        unrelated = _reference_command(service, project, agent, "unrelated-reference", unrelated_pin)
        unrelated_result = _commit(service, project, _body(project, _head(service, project), unrelated),
                                   "unrelated-reference-key")

        before_exact = copy.deepcopy(_document(service, project))
        exact_pin = _media(service, project, b"exact-owned-raw", "exact.raw")
        exact = _reference_command(service, project, agent, "exact-reference", exact_pin)
        exact_body = _body(project, _head(service, project), exact)
        accepted = _commit(service, project, exact_body, "exact-reference-key")
        assert accepted["data"]["status"] == "accepted"
        assert accepted["receipt"]["idempotency_key"] == "exact-reference-key"
        assert accepted["receipt"]["result"] == accepted["data"]
        rows, snapshot = _projection(service)
        assert {row["id"]: row for row in rows}["exact-reference"] == {
            "id": "exact-reference", "object_id": exact_pin["media_id"], "role": "source"
        }
        assert {row["reference_id"]: row for row in snapshot["references"]}["exact-reference"] == {
            "reference_id": "exact-reference", "object_id": exact_pin["media_id"], "role": "source"
        }
        document = accepted["data"]["canonical_document"]
        assert document["parent_revision"]["payload"]["occurrences"] == []
        assert document["parent_revision"]["payload"]["clips"] == []
        assert document["dependency_manifest"]["media"] == [unrelated_pin, exact_pin]

        service.close()
        restarted = RuntimeService(root)
        try:
            provider = agent.provider()
            restarted.register_timeline_commit_provider(provider)
            before_retry = tuple(restarted.store.conn.iterdump())
            with monkeypatch.context() as retry:
                retry.setattr(type(provider), "commit",
                              lambda *_args: pytest.fail("exact retry re-executed Agent provider"))
                assert _commit(restarted, project, exact_body, "exact-reference-key") == accepted
            assert tuple(restarted.store.conn.iterdump()) == before_retry
            assert _projection(restarted)[0].count({
                "id": "exact-reference", "object_id": exact_pin["media_id"], "role": "source"
            }) == 1
            changed = copy.deepcopy(exact_body)
            changed["commands"][0]["args"]["role"] = "target"
            before_changed = tuple(restarted.store.conn.iterdump())
            with pytest.raises(RuntimeErrorBase) as changed_error:
                _commit(restarted, project, changed, "exact-reference-key")
            assert changed_error.value.status == 409
            assert tuple(restarted.store.conn.iterdump()) == before_changed

            foreign = restarted.create_project({"slug": "foreign", "name": "Foreign"})["id"]
            foreign_pin = _media(restarted, foreign, b"foreign-owned-raw", "foreign.raw")
            unowned = _reference_command(restarted, project, agent, "unowned-reference", foreign_pin,
                                          read_project=foreign)
            before = tuple(restarted.store.conn.iterdump())
            with pytest.raises(RuntimeErrorBase) as refused:
                _commit(restarted, project, _body(project, _head(restarted, project), unowned),
                        "unowned-reference-key")
            assert refused.value.status == 409
            assert "raw media" in str(refused.value).lower()
            assert tuple(restarted.store.conn.iterdump()) == before

            replacement_pin = _media(restarted, project, b"replacement-owned-raw", "replacement.raw")
            replacement = _reference_command(
                restarted, project, agent, "exact-reference", replacement_pin,
                read_project=project,
                document=before_exact,
            )
            before_occupied = tuple(restarted.store.conn.iterdump())
            head_before_occupied = _head(restarted, project)
            history_before_occupied = restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"]
            with pytest.raises(RuntimeErrorBase) as occupied:
                _commit(restarted, project, _body(project, head_before_occupied, replacement),
                        "occupied-reference-key")
            assert occupied.value.status == 409
            assert "occupied" in str(occupied.value).lower()
            assert tuple(restarted.store.conn.iterdump()) == before_occupied
            assert _head(restarted, project) == head_before_occupied
            assert restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"] == history_before_occupied

            inverse = {
                "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
                "args": {"publications": [accepted["receipt"]["receipt_id"]]},
            }
            undone = _commit(restarted, project, _body(project, _head(restarted, project), inverse),
                             "exact-reference-inverse-key")
            rows, snapshot = _projection(restarted)
            assert {row["id"] for row in rows} == {"unrelated-reference"}
            assert {row["reference_id"] for row in snapshot["references"]} == {"unrelated-reference"}
            restored = undone["data"]["canonical_document"]
            assert restored["parent_revision"]["payload"] == before_exact["parent_revision"]["payload"]
            assert restarted._timeline_commits()[0].revision_closure(
                project, "main", restored["parent_revision"]["revision_id"]
            ) == restored
            assert unrelated_result["data"]["canonical_document"]["parent_revision"]["payload"] == restored[
                "parent_revision"]["payload"]
        finally:
            restarted.close()
    except Exception:
        service.close()
        raise
