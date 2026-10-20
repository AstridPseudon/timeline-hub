"""Accepted occurrence reference provenance projects through the old read model."""
from __future__ import annotations

import json

import pytest
from test_timeline_commit_acceptance import (
    realm,  # noqa: F401 (shared acceptance fixture)
)
from test_timeline_projection_occupancy import (
    accept,
    image,
    proposal,
    refresh,
    snapshot,
)

from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_store import digest


def reference_pair(commits, project, key, media_id, *, reference_id="reference-1"):
    pair = proposal(commits.store, commits, project, "main", key,
                    shots=[image("reference-shot", "reference-shot-" + key)])
    document = pair[1]["canonical_document"]
    internal = document["internal_timeline_revisions"][0]["payload"]
    internal["registry"] = {"assets": {
        "reference-asset": {"media_id": media_id, "content_sha256": media_id.removeprefix("sha256:")},
    }}
    document["parent_revision"]["payload"]["occurrences"][0]["provenance"] = {
        "astrid": {"timeline_reference": {
            "version": 1, "reference_id": reference_id, "role": "source", "asset": "reference-asset",
        }},
    }
    document["dependency_manifest"]["media"] = [{"media_id": media_id, "content_digest": media_id}]
    refresh_reference(pair[1])
    return pair


def refresh_reference(value):
    internal_digests = {}
    for internal in value["canonical_document"]["internal_timeline_revisions"]:
        internal["content_digest"] = digest(internal["payload"])
        internal_digests[internal["revision_id"]] = internal["content_digest"]
    for pin in value["canonical_document"]["dependency_manifest"]["internal_timelines"]:
        pin["content_digest"] = internal_digests[pin["revision_id"]]
    refresh(value)


def test_accepted_occurrence_reference_projects_row_and_revision_snapshot(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"reference", media_type="image/png", idempotency_key="reference-media")["data"]["object_id"]

    accepted = accept(commits, reference_pair(commits, project, "reference", media))
    assert tuple(service.store.conn.execute(
        "SELECT timeline_id, object_id, role FROM timeline_references WHERE id=?", ("reference-1",)
    ).fetchone()) == ("main", media, "source")
    snapshot_row = service.store.conn.execute(
        "SELECT version, references_json FROM timeline_revisions WHERE timeline_id=? ORDER BY version DESC LIMIT 1",
        ("main",),
    ).fetchone()
    assert snapshot_row["version"] == 2
    assert json.loads(snapshot_row["references_json"]) == [{
        "reference_id": "reference-1", "object_id": media, "role": "source",
    }]
    assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["occurrences"][0]["provenance"]


def test_reference_projection_refuses_missing_asset_before_any_write(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"reference", media_type="image/png", idempotency_key="missing-media")["data"]["object_id"]
    pair = reference_pair(commits, project, "missing", media)
    del pair[1]["canonical_document"]["internal_timeline_revisions"][0]["payload"]["registry"]["assets"]["reference-asset"]
    refresh_reference(pair[1])
    before = snapshot(service)
    with pytest.raises(CommitRejected) as error:
        accept(commits, pair)
    assert error.value.failure["details"]["reason"] == "reference_binding_missing"
    assert snapshot(service) == before


def test_reference_projection_refuses_conflicting_asset_identity_before_any_write(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"reference", media_type="image/png", idempotency_key="ambiguous-media")["data"]["object_id"]
    pair = reference_pair(commits, project, "ambiguous", media)
    pair[1]["canonical_document"]["internal_timeline_revisions"][0]["payload"]["registry"]["assets"]["reference-asset"]["content_sha256"] = "f" * 64
    refresh_reference(pair[1])
    before = snapshot(service)
    with pytest.raises(CommitRejected) as error:
        accept(commits, pair)
    assert error.value.failure["details"]["reason"] == "reference_binding_ambiguous"
    assert snapshot(service) == before


def test_reference_projection_refuses_occupied_identity_before_any_write(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    first_media = service.ingest(project, b"first-reference", media_type="image/png", idempotency_key="first-media")["data"]["object_id"]
    second_media = service.ingest(project, b"second-reference", media_type="image/png", idempotency_key="second-media")["data"]["object_id"]
    accept(commits, reference_pair(commits, project, "first", first_media))
    pair = reference_pair(commits, project, "second", second_media)
    pair[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"][0]["provenance"]["astrid"]["timeline_reference"]["reference_id"] = "reference-1"
    refresh_reference(pair[1])
    before = snapshot(service)
    with pytest.raises(CommitRejected) as error:
        accept(commits, pair)
    assert error.value.failure["details"]["reason"] == "reference_projection_occupied"
    assert snapshot(service) == before


def test_reference_projection_follows_restore_shape_and_removes_owned_row(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"reference", media_type="image/png", idempotency_key="restore-media")["data"]["object_id"]
    accept(commits, reference_pair(commits, project, "restore-source", media))
    cleared = proposal(commits.store, commits, project, "main", "restore-clear",
                       shots=[image("reference-shot", "reference-shot-restore-clear")])
    document = cleared[1]["canonical_document"]
    document["parent_revision"]["payload"]["occurrences"][0]["provenance"] = {}
    refresh_reference(cleared[1])
    accept(commits, cleared)
    assert service.store.conn.execute(
        "SELECT 1 FROM timeline_references WHERE id=?", ("reference-1",)
    ).fetchone() is None
    snapshots = [json.loads(row[0]) for row in service.store.conn.execute(
        "SELECT references_json FROM timeline_revisions WHERE timeline_id=? ORDER BY version", ("main",)
    )]
    assert snapshots[-2:] == [[{"reference_id": "reference-1", "object_id": media, "role": "source"}], []]
