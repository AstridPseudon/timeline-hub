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
from runtime_protocol.timeline_commit_port import route_path, validate_request
from test_timeline_commit_integration import agent, film  # noqa: F401 (shared fixtures)


pytestmark = pytest.mark.integration

_ORDERED_TARGET = "com.example.compiler-canary"
_ORDERED_BEFORE = "a-before"
_ORDERED_AFTER = "z-after"


def _head(service, project):
    value = service.get_project_timeline(project, "main")
    return {"revision_id": value["head_revision_id"],
            "publication_id": value["head_publication_id"]}


def _document(service, project, revision=None):
    return service._timeline_commits()[0].revision_closure(
        project, "main", revision or _head(service, project)["revision_id"]
    )


def _body(project, base, command):
    commands = command if isinstance(command, list) else [command]
    return {
        "api_version": 1,
        "project_id": project,
        "timeline_id": "main",
        "base_revision_id": base["revision_id"],
        "base_publication_id": base["publication_id"],
        "commands": copy.deepcopy(commands),
        "source": {"via": "python"},
    }


def _project_data_write(key, value, *, target):
    return {
        "schema_version": 1,
        "op": "project-data.write",
        "version": "1",
        "select": "parent",
        "args": {"target": target, "key": key, "value": copy.deepcopy(value), "mode": "replace"},
    }


def _project_data_remove(key, *, target):
    return {
        "schema_version": 1,
        "op": "project-data.write",
        "version": "1",
        "select": "parent",
        "args": {"target": target, "key": key, "mode": "remove"},
    }


def _inverse(publication):
    return {
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": [publication]},
    }


def _project_app(document):
    return document["parent_revision"]["payload"]["config"].get("app")


def _authoritative_recorded_command(agent, document, command):
    """Capture the complete command from the normal Agent recorder."""
    from astrid.sdk.timeline.commands import execute

    plan = execute(agent.bundle(document), [copy.deepcopy(command)])
    return plan.records[0]["command"]


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
        # Agent's canonical manifest enumerates media pins by media_id; the
        # exact fixture digest therefore precedes the unrelated fixture digest.
        assert document["dependency_manifest"]["media"] == [exact_pin, unrelated_pin]

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
            # Rationale is the existing schema-valid request-level mutation;
            # keep the closed source-only role mutation as its own 422 case.
            changed["rationale"] = "changed request rationale"
            validate_request(changed)
            assert changed["commands"] == exact_body["commands"]
            before_changed = tuple(restarted.store.conn.iterdump())
            head_before_changed = _head(restarted, project)
            history_before_changed = restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"]
            with pytest.raises(RuntimeErrorBase) as changed_error:
                _commit(restarted, project, changed, "exact-reference-key")
            assert changed_error.value.status == 409
            assert tuple(restarted.store.conn.iterdump()) == before_changed
            assert _head(restarted, project) == head_before_changed
            assert restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"] == history_before_changed

            invalid_role = copy.deepcopy(exact_body)
            invalid_role["commands"][0]["args"]["role"] = "target"
            before_invalid_role = tuple(restarted.store.conn.iterdump())
            head_before_invalid_role = _head(restarted, project)
            history_before_invalid_role = restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"]
            with pytest.raises(RuntimeErrorBase) as invalid_role_error:
                _commit(restarted, project, invalid_role, "exact-reference-key")
            assert invalid_role_error.value.status == 422
            assert tuple(restarted.store.conn.iterdump()) == before_invalid_role
            assert _head(restarted, project) == head_before_invalid_role
            assert restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"] == history_before_invalid_role

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


def test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo(
        tmp_path, agent, monkeypatch):
    """Exercise one ordered project-data remove through the normal Runtime API."""
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = None
    try:
        provider = agent.provider()
        service.register_timeline_commit_provider(provider)
        project = service.create_project({"slug": "ordered-data", "name": "Ordered data"})["id"]
        service.create_timeline(project, "main", idempotency_key="ordered-data-main")

        opaque_before = {"literal": [None, False, 0], "future": {"kept": True}}
        opaque_after = {"literal": {"nested": [None, "opaque"]}}
        seed = [
            _project_data_write("keep", opaque_before, target=_ORDERED_BEFORE),
            _project_data_write("gone", None, target=_ORDERED_TARGET),
            _project_data_write("keep", opaque_after, target=_ORDERED_AFTER),
        ]
        seed_body = _body(project, _head(service, project), seed)
        seeded = _commit(service, project, seed_body, "ordered-data-seed")
        original = copy.deepcopy(seeded["data"]["canonical_document"])
        original_app = _project_app(original)
        assert list(original_app) == [_ORDERED_BEFORE, _ORDERED_TARGET, _ORDERED_AFTER]
        assert original_app == {
            _ORDERED_BEFORE: {"keep": opaque_before},
            _ORDERED_TARGET: {"gone": None},
            _ORDERED_AFTER: {"keep": opaque_after},
        }

        remove = _project_data_remove("gone", target=_ORDERED_TARGET)
        remove_body = _body(project, _head(service, project), remove)
        accepted = _commit(service, project, remove_body, "ordered-data-remove")
        removed = accepted["data"]["canonical_document"]
        assert accepted["receipt"]["result"] == accepted["data"]
        assert _project_app(removed) == {
            _ORDERED_BEFORE: {"keep": opaque_before},
            _ORDERED_AFTER: {"keep": opaque_after},
        }
        assert list(_project_app(removed)) == [_ORDERED_BEFORE, _ORDERED_AFTER]
        record = service.list_timeline_commits(
            project, "main", authorize=lambda: None)["items"][-1]["records"]["commands"][0]
        assert record["command"] == _authoritative_recorded_command(agent, original, remove)
        assert record["writes"] == [
            {
                "ref": "parent",
                "path": ["config", "app", _ORDERED_TARGET, "gone"],
                "before": {"state": "present", "value": None},
                "after": {"state": "absent"},
            },
            {
                "ref": "parent",
                "path": ["config", "app", _ORDERED_TARGET],
                "before": {"state": "present", "value": {}},
                "after": {"state": "absent"},
                "insertion_order": [_ORDERED_BEFORE, _ORDERED_TARGET, _ORDERED_AFTER],
            },
        ]

        service.close()
        service = None
        restarted = RuntimeService(root)
        try:
            retry_provider = agent.provider()
            restarted.register_timeline_commit_provider(retry_provider)
            before_retry = tuple(restarted.store.conn.iterdump())
            before_history = restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"]
            with monkeypatch.context() as retry:
                retry.setattr(type(retry_provider), "commit",
                              lambda *_args: pytest.fail("exact retry re-executed Agent provider"))
                assert _commit(restarted, project, remove_body, "ordered-data-remove") == accepted
            assert tuple(restarted.store.conn.iterdump()) == before_retry
            assert restarted.list_timeline_commits(
                project, "main", authorize=lambda: None)["items"] == before_history

            undone = _commit(
                restarted, project,
                _body(project, _head(restarted, project), _inverse(accepted["receipt"]["receipt_id"])),
                "ordered-data-undo",
            )
            restored = undone["data"]["canonical_document"]
            assert _project_app(restored) == original_app
            assert list(_project_app(restored)) == [_ORDERED_BEFORE, _ORDERED_TARGET, _ORDERED_AFTER]
            assert restored["parent_revision"]["payload"] == original["parent_revision"]["payload"]

            redone = _commit(
                restarted, project,
                _body(project, _head(restarted, project), _inverse(undone["receipt"]["receipt_id"])),
                "ordered-data-redo",
            )
            redone_app = _project_app(redone["data"]["canonical_document"])
            assert redone_app == _project_app(removed)
            assert list(redone_app) == [_ORDERED_BEFORE, _ORDERED_AFTER]
            assert redone["data"]["canonical_document"]["parent_revision"]["payload"] == \
                removed["parent_revision"]["payload"]
        finally:
            restarted.close()
    finally:
        if service is not None:
            service.close()
