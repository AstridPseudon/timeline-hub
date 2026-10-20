"""Accepted occurrence reference provenance projects through the old read model."""
from __future__ import annotations

import copy
import json

import pytest
from test_timeline_commit_acceptance import (
    realm,  # noqa: F401 (shared acceptance fixture)
)
from test_timeline_projection_occupancy import (
    accept,
    image,
    new_timeline,
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


def test_reference_projection_refuses_foreign_occupied_identity_before_any_write(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    first_media = service.ingest(project, b"foreign-reference", media_type="image/png", idempotency_key="foreign-occupied-media")["data"]["object_id"]
    second_media = service.ingest(project, b"candidate-reference", media_type="image/png", idempotency_key="foreign-candidate-media")["data"]["object_id"]
    service.store.conn.execute(
        "INSERT INTO timeline_references(id, timeline_id, object_id, role) VALUES (?, ?, ?, ?)",
        ("reference-1", "other", first_media, "source"),
    )
    pair = reference_pair(commits, project, "foreign-occupied", second_media)
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


def _rewrite_latest_reference_snapshot(service, timeline_id, references):
    service.store.conn.execute(
        "UPDATE timeline_revisions SET references_json=? WHERE timeline_id=? "
        "AND version=(SELECT MAX(version) FROM timeline_revisions WHERE timeline_id=?)",
        (json.dumps(references, separators=(",", ":")), timeline_id, timeline_id),
    )


def test_clear_preserves_unrelated_reference_not_proven_by_prior_closure(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"owned-reference", media_type="image/png", idempotency_key="owned-media")["data"]["object_id"]
    legacy_media = service.ingest(project, b"legacy-reference", media_type="image/png", idempotency_key="legacy-media")["data"]["object_id"]
    accept(commits, reference_pair(commits, project, "owned", media))
    service.store.conn.execute(
        "INSERT INTO timeline_references(id, timeline_id, object_id, role) VALUES (?, ?, ?, ?)",
        ("legacy-ref", "main", legacy_media, "source"),
    )
    service.store.conn.execute(
        "INSERT INTO timeline_reference_state(id, version, archived_at) VALUES (?, ?, ?)",
        ("legacy-ref", 4, None),
    )
    _rewrite_latest_reference_snapshot(service, "main", [
        {"reference_id": "reference-1", "object_id": media, "role": "source"},
        {"reference_id": "legacy-ref", "object_id": legacy_media, "role": "source"},
    ])
    cleared = proposal(commits.store, commits, project, "main", "clear-unrelated",
                       shots=[image("reference-shot", "reference-shot-clear-unrelated")])
    cleared[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"][0]["provenance"] = {}
    refresh_reference(cleared[1])

    accept(commits, cleared)
    assert tuple(service.store.conn.execute(
        "SELECT timeline_id, object_id, role FROM timeline_references WHERE id=?", ("legacy-ref",)
    ).fetchone()) == ("main", legacy_media, "source")
    assert tuple(service.store.conn.execute(
        "SELECT version, archived_at FROM timeline_reference_state WHERE id=?", ("legacy-ref",)
    ).fetchone()) == (4, None)
    assert service.store.conn.execute(
        "SELECT 1 FROM timeline_references WHERE id=?", ("reference-1",)
    ).fetchone() is None

    restored = reference_pair(commits, project, "restore-unrelated", media)
    accept(commits, restored)
    assert service.store.conn.execute(
        "SELECT 1 FROM timeline_references WHERE id=?", ("legacy-ref",)
    ).fetchone() is not None
    assert service.store.conn.execute(
        "SELECT 1 FROM timeline_reference_state WHERE id=?", ("legacy-ref",)
    ).fetchone() is not None


def test_clear_preserves_foreign_reference_state_named_by_corrupt_snapshot(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    new_timeline(service, commits, project, "other")
    media = service.ingest(project, b"owned-reference", media_type="image/png", idempotency_key="owned-foreign-media")["data"]["object_id"]
    foreign_media = service.ingest(project, b"foreign-reference", media_type="image/png", idempotency_key="foreign-media")["data"]["object_id"]
    accept(commits, reference_pair(commits, project, "owned-foreign", media))
    service.store.conn.execute(
        "INSERT INTO timeline_references(id, timeline_id, object_id, role) VALUES (?, ?, ?, ?)",
        ("foreign-ref", "other", foreign_media, "source"),
    )
    service.store.conn.execute(
        "INSERT INTO timeline_reference_state(id, version, archived_at) VALUES (?, ?, ?)",
        ("foreign-ref", 7, None),
    )
    _rewrite_latest_reference_snapshot(service, "main", [
        {"reference_id": "reference-1", "object_id": media, "role": "source"},
        {"reference_id": "foreign-ref", "object_id": foreign_media, "role": "source"},
    ])
    cleared = proposal(commits.store, commits, project, "main", "clear-foreign",
                       shots=[image("reference-shot", "reference-shot-clear-foreign")])
    cleared[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"][0]["provenance"] = {}
    refresh_reference(cleared[1])

    accept(commits, cleared)
    assert tuple(service.store.conn.execute(
        "SELECT timeline_id, object_id, role FROM timeline_references WHERE id=?", ("foreign-ref",)
    ).fetchone()) == ("other", foreign_media, "source")
    assert tuple(service.store.conn.execute(
        "SELECT version, archived_at FROM timeline_reference_state WHERE id=?", ("foreign-ref",)
    ).fetchone()) == (7, None)


def test_duplicate_occurrence_reference_identity_refuses_before_any_write(realm):  # noqa: F811
    service, commits, project, _, _ = realm
    media = service.ingest(project, b"duplicate-reference", media_type="image/png", idempotency_key="duplicate-media")["data"]["object_id"]
    pair = reference_pair(commits, project, "duplicate", media)
    occurrence = copy.deepcopy(pair[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"][0])
    occurrence.update(occurrence_id="occ-duplicate", placement={"start_ms": 1000})
    pair[1]["canonical_document"]["parent_revision"]["payload"]["occurrences"].append(occurrence)
    refresh_reference(pair[1])
    before = snapshot(service)

    with pytest.raises(CommitRejected) as error:
        accept(commits, pair)
    assert error.value.failure["details"]["reason"] == "reference_binding_ambiguous"
    assert snapshot(service) == before
