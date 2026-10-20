from __future__ import annotations

import copy
from contextlib import contextmanager

import pytest
from test_shot_composition_runtime import _publication, _service
from test_timeline_projection_occupancy import proposal, refresh

from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import digest, route_path
from runtime_protocol.timeline_commit_store import request_identity
from runtime_protocol.util import canonical_json


def _validation_baseline(service, project_id, timeline_id="main"):
    commits, _ = service._timeline_commits()
    head = commits.bootstrap(project_id, timeline_id, authorize=lambda: None)
    source = commits.revision_closure(project_id, timeline_id, head["revision_id"])
    assert source["parent_revision"]["payload"] == {
        "config": {"clips": [], "tracks": []}, "registry": {}, "clips": [], "occurrences": [],
    }
    assert source["shot_revisions"] == source["internal_timeline_revisions"] == []
    assert source["dependency_manifest"] == {"shots": [], "internal_timelines": [], "media": [], "documents": []}
    public = service.get_project_timeline(project_id, timeline_id)
    assert (public["head_revision_id"], public["head_publication_id"]) == (head["revision_id"], head["publication_id"])
    assert commits.history_entry(project_id, timeline_id, head["publication_id"])["revision_id"] == head["revision_id"]
    return commits


def _validation_candidate(service, commits, body, key):
    # Trusted host preparation isolates validation; it is not Agent authoring.
    shots, internals = copy.deepcopy(body["shot_revisions"]), copy.deepcopy(body["internal_timeline_revisions"])
    for shot in shots:
        shot["payload"]["internal_timeline_revision_id"] = shot["internal_timeline_revision_id"]
        shot["content_digest"] = digest(shot["payload"])
    for internal in internals:
        internal["content_digest"] = digest(internal["payload"])
    pair = proposal(service, commits, body["project_id"], body["timeline_id"], key,
                    shots=[(shot, next(i for i in internals if i["revision_id"] == shot["internal_timeline_revision_id"]))
                           for shot in shots])
    context, prepared = pair
    document = prepared["canonical_document"]
    document["parent_revision"] = {"revision_id": body["parent_revision_id"], "payload": copy.deepcopy(body["parent_composition"])}
    document["dependency_manifest"]["media"] = copy.deepcopy(body.get("dependency_manifest", {}).get("media", []))
    context["invocation"]["path"] = route_path(body["project_id"], body["timeline_id"])
    context["request_hash"] = request_identity(context)
    refresh(prepared)
    return pair


@contextmanager
def _validation_no_writes(service):
    before = tuple(service.store.conn.iterdump())
    changes = service.store.conn.total_changes
    roots = (service.store.cas_root, service.store.staging_root)

    def files():
        return {str(path.relative_to(service.store.root)): path.read_bytes() if path.is_file() else None
                for root in roots for path in root.rglob("*")}

    stored = files()
    try:
        yield
    finally:
        assert tuple(service.store.conn.iterdump()) == before, "validation changed the accepted baseline/database"
        assert service.store.conn.total_changes == changes, "validation attempted database writes"
        assert files() == stored, "validation changed CAS/staging"


@pytest.mark.parametrize("location", ["root", "clip"])
@pytest.mark.parametrize("field,value", [
    ("occurrences", []), ("occurrence_records", []), ("parent_composition", {}),
    ("nested_composition", {}), ("occurrence_id", "nested-occurrence"),
    ("shot_revision_id", "nested-shot"), ("parent_revision_id", "nested-parent"),
    ("composition_revision_id", "nested-composition"),
])
def test_internal_nested_structure_refuses_before_any_write(tmp_path, location, field, value):
    service, project = _service(tmp_path)
    try:
        commits = _validation_baseline(service, project)
        body = _publication(project)
        payload = body["internal_timeline_revisions"][0]["payload"]
        target = payload if location == "root" else payload["clips"][0]
        target[field] = value
        pair = _validation_candidate(service, commits, body, "nested")
        commits.validate_prepared(pair[1])
        with _validation_no_writes(service):
            with pytest.raises(CommitRejected, match="nested") as caught:
                commits.accept(*pair, authorize=lambda: None)
            assert caught.value.failure["http_status"] == 422
            assert caught.value.failure["details"]["reason"] == "invalid_closure"
    finally:
        service.close()


def test_internal_opaque_graph_names_roundtrip_after_restart_and_retry(tmp_path):
    service, project = _service(tmp_path)
    root = service.store.root
    try:
        commits = _validation_baseline(service, project)
        body = _publication(project)
        payload = body["internal_timeline_revisions"][0]["payload"]
        opaque = {"occurrences": [], "occurrence_records": [], "parent_composition": {},
                  "nested_composition": {"shot_revision_id": "opaque-shot"},
                  "occurrence_id": "opaque-occurrence", "parent_revision_id": None,
                  "composition_revision_id": "opaque-composition"}
        for target in (payload, payload["clips"][0]):
            target["params"] = copy.deepcopy(opaque)
            target["provenance"] = {"history": [copy.deepcopy(opaque)]}
        payload["future_extension"] = {"clips": [copy.deepcopy(opaque)]}
        pair = _validation_candidate(service, commits, body, "opaque")
        expected = copy.deepcopy(pair[1]["canonical_document"])
        encoded = canonical_json(payload)
        accepted = commits.accept(*pair, authorize=lambda: None)
        revision = accepted["data"]["accepted_revision_id"]
        assert commits.revision_closure(project, "main", revision) == expected
        stored = service.store.conn.execute(
            "SELECT payload_json FROM internal_timeline_revisions WHERE id='timeline-rev-1'",
        ).fetchone()[0]
        assert stored == encoded
        service.close()
        service = RuntimeService(root)
        commits, _ = service._timeline_commits()
        assert commits.revision_closure(project, "main", revision) == expected
        with _validation_no_writes(service):
            assert commits.accept(*pair, authorize=lambda: None) == accepted
    finally:
        service.close()
