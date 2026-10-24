"""Legacy occupancy properties exercised through the authenticated v2 commit path."""
from __future__ import annotations

import base64
import copy
from typing import Any

import pytest

from astrid_runtime_client import ApiError, WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import RetiredRouteError, RuntimeErrorBase
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_store import TimelineCommitStore
from test_shot_composition_runtime import (
    _publication, _service, _validation_no_writes,
    restore_provider as _restore_provider,  # noqa: F401 (register the existing provider fixture)
)
from test_timeline_commit_acceptance import validate_prepared  # noqa: F401 (provider schema)


PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


@pytest.fixture
def occupancy_provider(request):
    return request.getfixturevalue("_restore_provider")


def publish(service, project, body, key):
    """The retired route is kept as a direct-authority probe only."""
    return service.publish_parent_composition(project, "main", body, idempotency_key=key)


def _commits(service):
    return TimelineCommitStore(service.store, validate_prepared=validate_prepared)


def _conn(service) -> Any:
    return service.store.conn


def _head(service, project, timeline):
    resource = service.get_project_timeline(project, timeline)
    return {"revision_id": resource["head_revision_id"],
            "publication_id": resource["head_publication_id"]}


def _document(commits, project, timeline, service):
    return commits.revision_closure(project, timeline, _head(service, project, timeline)["revision_id"])


def _body(service, project, timeline, commands, key, *, steps=None, reads=(), label=None) -> Any:
    label = label or key
    steps = steps or [{"id": "edit", "label": label, "intent": "Occupancy proof",
                       "tags": ["occupancy"], "command_ordinals": list(range(len(commands))),
                       "patch": [], "reads": list(reads)}]
    return {
        "api_version": 1, "project_id": project, "timeline_id": timeline,
        "base_revision_id": _head(service, project, timeline)["revision_id"],
        "base_publication_id": _head(service, project, timeline)["publication_id"],
        "commands": copy.deepcopy(commands), "label": label, "steps": copy.deepcopy(steps),
        "merge": "fields", "reads": copy.deepcopy(list(reads)), "dry_run": False,
        "source": {"via": "python", "detail": "legacy occupancy"},
        "rationale": "Preserve legacy occupancy safety through v2",
        "group_id": "legacy-occupancy",
    }


def _submit(service, project, timeline, commands, key, *, steps=None, reads=(), label=None):
    body = _body(service, project, timeline, commands, key, steps=steps, reads=reads, label=label)
    result = service.commit_timeline(
        project, timeline, body, idempotency_key=key, publisher="occupancy-test",
        invocation_path=route_path(project, timeline), authorize=lambda: None,
    )
    return result, body


def _bundle(commits, service, project, timeline):
    from astrid.sdk.timeline.commit import bundle_from_document

    return bundle_from_document(_document(commits, project, timeline, service))


def _prepare_timeline(service, commits, project, timeline):
    row = _conn(service).execute(
        "SELECT revision_id, publication_id FROM parent_composition_heads WHERE project_id=? AND timeline_id=?",
        (project, timeline),
    ).fetchone()
    if row is None:
        service.create_timeline(project, timeline, name=timeline, idempotency_key=f"timeline-{timeline}")
        commits.bootstrap(project, timeline, authorize=lambda: None)
    document = _document(commits, project, timeline, service)
    config = document["parent_revision"]["payload"].setdefault("config", {})
    if "output" not in config:
        from astrid.sdk.timeline.native_initialize import capture_initialize

        command = capture_initialize(
            _bundle(commits, service, project, timeline), name=timeline, slug=timeline,
            output={"resolution": "1280x720", "fps": 30, "file": "output.mp4",
                    "background": None, "background_scale": None},
        )
        _submit(service, project, timeline, [command], f"{timeline}-init")
        document = _document(commits, project, timeline, service)
    tracks = document["parent_revision"]["payload"].get("config", {}).get("tracks", [])
    if not any(row.get("id") == "picture" for row in tracks):
        from astrid.sdk.timeline.capture import capture_track_create

        _submit(service, project, timeline, [capture_track_create(
            _bundle(commits, service, project, timeline), "parent",
            {"id": "picture", "kind": "visual", "role": "output"},
        )], f"{timeline}-track")


def _seed_occupied(service, commits, project, timeline, *, archived=False):
    _prepare_timeline(service, commits, project, timeline)
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    _submit(service, project, timeline, [capture_occurrence_create(
        _bundle(commits, service, project, timeline), "occ-1", "shot-1",
        name="KEEP OWNER NAME", track="picture", on=0, duration=1,
    )], f"{timeline}-occurrence")
    _submit(service, project, timeline, [capture_track_create(
        _bundle(commits, service, project, timeline), "occurrence:occ-1",
        {"id": "picture", "kind": "visual"},
    )], f"{timeline}-child-track")

    imported = service.import_media(
        project, PNG, media_type="image/png", original_name="occupancy.png",
        actor_id="occupancy-test", idempotency_key=f"{timeline}-media",
    )["data"]
    pin = service.get_project_media_selection(project, {
        "asset": imported["variant_id"], "generation_id": imported["generation_id"],
        "variant_id": imported["variant_id"],
    }, authorize=lambda: None)
    verified = service.get_project_verified_media(project, pin, authorize=lambda: None)
    from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media

    bundle = _bundle(commits, service, project, timeline)
    media_command = capture_occurrence_add_media(
        bundle, "occurrence:occ-1",
        {"id": "keep-owner-item", "clipType": "image", "asset": pin["asset"],
         "track": "picture", "at": 0, "hold": 1},
        pin, verified_media=[verified],
    )
    shot = next(row for row in _document(commits, project, timeline, service)["shot_revisions"]
                if row["shot_id"] == "shot-1")
    payload = shot["payload"]
    changes = [
        {"op": "set", "ref": "shot:shot-1", "path": ["items"],
         "before": {"state": "present", "value": payload["items"]},
         "value": [{"item_id": "keep-owner-item", "media_id": pin["object_id"],
                    "metadata": {"opaque": None}}]},
        {"op": "set", "ref": "shot:shot-1", "path": ["metadata"],
         "before": {"state": "absent"}, "value": {"opaque": [None]}},
        {"op": "set", "ref": "shot:shot-1", "path": ["archived"],
         "before": {"state": "absent"}, "value": archived},
    ]
    patch = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
             "args": {"changes": changes}}
    reads = [{"kind": "field", "ref": change["ref"], "path": change["path"],
              "state": change["before"]} for change in changes]
    steps = [
        {"id": "media", "label": "Attach occupancy media", "intent": "Attach media",
         "tags": ["occupancy"], "command_ordinals": [0], "patch": [], "reads": []},
        {"id": "shot", "label": "Record occupied shot", "intent": "Preserve shot facts",
         "tags": ["occupancy"], "command_ordinals": [1], "patch": changes, "reads": reads},
    ]
    result, _ = _submit(service, project, timeline, [media_command, patch],
                        f"{timeline}-occupied", steps=steps, reads=reads)
    assert result["data"]["status"] == "accepted"
    return result


def _candidate(service, commits, project, timeline, *, occupied_name="Intruder"):
    _prepare_timeline(service, commits, project, timeline)
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    bundle = _bundle(commits, service, project, timeline)
    free = capture_occurrence_create(bundle, "free-occurrence", "free", name="Free",
                                      track="picture", on=0, duration=1)
    from astrid.sdk.timeline.commands import execute

    bundle = execute(bundle, [free]).bundle
    occupied = capture_occurrence_create(bundle, "occupied-occurrence", "shot-1",
                                         name=occupied_name, track="picture", on=1, duration=1)
    steps = [
        {"id": "free", "label": "Free first", "intent": "Exercise ordering", "tags": ["occupancy"],
         "command_ordinals": [0], "patch": [], "reads": []},
        {"id": "occupied", "label": "Occupied second", "intent": "Reject occupied destination",
         "tags": ["occupancy"], "command_ordinals": [1], "patch": [], "reads": []},
    ]
    return _body(service, project, timeline, [free, occupied], "intruder", steps=steps)


def _patch_shot_body(service, commits, project, timeline, *, name, key):
    shot = next(row for row in _document(commits, project, timeline, service)["shot_revisions"]
                if row["shot_id"] == "shot-1")
    change = {"op": "set", "ref": "shot:shot-1", "path": ["name"],
              "before": {"state": "present", "value": shot["payload"]["name"]}, "value": name}
    command = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
               "args": {"changes": [change]}}
    read = {"kind": "field", "ref": change["ref"], "path": change["path"], "state": change["before"]}
    steps = [{"id": "shot", "label": "Update current shot", "intent": "Update closure",
              "tags": ["occupancy"], "command_ordinals": [0], "patch": [change], "reads": [read]}]
    return _body(service, project, timeline, [command], key, steps=steps, reads=[read])


def _patch_shot(service, commits, project, timeline, *, name, key):
    body = _patch_shot_body(service, commits, project, timeline, name=name, key=key)
    return service.commit_timeline(
        project, timeline, body, idempotency_key=key, publisher="occupancy-test",
        invocation_path=route_path(project, timeline), authorize=lambda: None,
    ), body


def _assert_refusal(error, *, reason=None, status=409):
    assert error.value.status == status
    assert error.value.details["status"] in {"conflict", "refused"}
    if reason is not None:
        assert error.value.details["reason"] == reason


def _seed_collision(service, commits, project, *, foreign=False, archived=False):
    owner = service.create_project({"slug": "private", "name": "Private film"})["id"] if foreign else project
    _seed_occupied(service, commits, owner, "owner", archived=archived)
    _prepare_timeline(service, commits, project, "target")


@pytest.mark.parametrize("foreign", [False, True])
@pytest.mark.parametrize("archived", [False, True])
def test_legacy_publication_refuses_unrelated_destination_before_any_write(
        tmp_path, occupancy_provider, foreign, archived):
    service, project = _service(tmp_path)
    try:
        service.register_timeline_commit_provider(occupancy_provider)
        commits = _commits(service)
        commits.bootstrap(project, "main", authorize=lambda: None)
        _seed_collision(service, commits, project, foreign=foreign, archived=archived)
        body = _candidate(service, commits, project, "target")
        before = tuple(_conn(service).iterdump())
        with _validation_no_writes(service), pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(project, "target", body, idempotency_key="intruder",
                                    publisher="occupancy-test", invocation_path=route_path(project, "target"),
                                    authorize=lambda: None)
        _assert_refusal(error, reason="destination_occupied")
        assert tuple(_conn(service).iterdump()) == before
        assert _conn(service).execute("SELECT name FROM project_shots WHERE id='shot-1'").fetchone()[0] == "KEEP OWNER NAME"
        assert _conn(service).execute("SELECT COUNT(*) FROM shot_items WHERE id='keep-owner-item'").fetchone()[0] == 1
    finally:
        service.close()


def test_exact_f1_over_http(tmp_path, occupancy_provider):
    service, project = _service(tmp_path)
    service.register_timeline_commit_provider(occupancy_provider)
    commits = _commits(service)
    commits.bootstrap(project, "main", authorize=lambda: None)
    _seed_collision(service, commits, project)
    root = service.store.root
    service.close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support", authoring_profile="astrid").start()
    try:
        commits = _commits(daemon.service)
        body = _candidate(daemon.service, commits, project, "target")
        assert daemon.endpoint is not None
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        with _validation_no_writes(daemon.service), pytest.raises(ApiError) as error:
            client.commit_timeline(project, "target", body, idempotency_key="intruder")
        assert error.value.status == 409
        assert error.value.details["reason"] == "destination_occupied"
    finally:
        daemon.stop()


def test_legacy_publication_route_is_directly_retired_without_write(tmp_path):
    service, project = _service(tmp_path)
    try:
        body = _publication(project)
        before = tuple(_conn(service).iterdump())
        with _validation_no_writes(service), pytest.raises(RetiredRouteError) as error:
            publish(service, project, body, "legacy")
        assert error.value.status == 410
        assert error.value.code == "retired_route"
        assert error.value.details is not None
        assert error.value.details["reason"] == "timeline_commit_required"
        assert tuple(_conn(service).iterdump()) == before
    finally:
        service.close()


@pytest.mark.parametrize("existing", [False, True])
def test_legacy_occupied_destination_without_shot_head_is_not_adopted(
        tmp_path, occupancy_provider, existing):
    service, project = _service(tmp_path)
    try:
        service.register_timeline_commit_provider(occupancy_provider)
        commits = _commits(service)
        commits.bootstrap(project, "main", authorize=lambda: None)
        _seed_occupied(service, commits, project, "main")
        _conn(service).execute("DELETE FROM shot_revision_heads WHERE shot_id='shot-1'")
        body = _patch_shot_body(
            service, commits, project, "main",
            name="Existing head" if existing else "New head", key="missing-head",
        )
        assert body["commands"][0]["args"]["changes"][0]["value"] == (
            "Existing head" if existing else "New head"
        )
        before = tuple(_conn(service).iterdump())
        with _validation_no_writes(service), pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(project, "main", body, idempotency_key="missing-head",
                                    publisher="occupancy-test", invocation_path=route_path(project, "main"),
                                    authorize=lambda: None)
        _assert_refusal(error, reason="destination_occupied")
        assert tuple(_conn(service).iterdump()) == before
    finally:
        service.close()


def test_legacy_current_closure_update_and_exact_retry_precede_live_checks(tmp_path, occupancy_provider):
    service, project = _service(tmp_path)
    try:
        service.register_timeline_commit_provider(occupancy_provider)
        commits = _commits(service)
        commits.bootstrap(project, "main", authorize=lambda: None)
        _seed_occupied(service, commits, project, "main")
        accepted, body = _patch_shot(service, commits, project, "main", name="Updated own shot", key="second")
        assert accepted["data"]["status"] == "accepted"
        revision = next(row["revision_id"] for row in accepted["data"]["canonical_document"]["shot_revisions"]
                        if row["shot_id"] == "shot-1")
        assert service.get_project_shot_revision(project, "shot-1", revision)["payload"]["name"] == "Updated own shot"
        newer, _ = _patch_shot(service, commits, project, "main", name="Newest shot", key="third")
        assert newer["data"]["status"] == "accepted"
        _conn(service).execute("UPDATE project_shots SET name='changed after receipt' WHERE id='shot-1'")
        with _validation_no_writes(service):
            assert service.commit_timeline(project, "main", body, idempotency_key="second",
                                           publisher="occupancy-test", invocation_path=route_path(project, "main"),
                                           authorize=lambda: None) == accepted
        with _validation_no_writes(service), pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(project, "main", body, idempotency_key="different-key",
                                    publisher="occupancy-test", invocation_path=route_path(project, "main"),
                                    authorize=lambda: None)
        _assert_refusal(error, reason="value_conflict")
    finally:
        service.close()


@pytest.mark.parametrize("tamper", ["receipt", "occurrence", "digest", "projection", "removed"])
def test_legacy_current_destination_requires_verified_current_closure(tmp_path, occupancy_provider, tamper):
    service, project = _service(tmp_path)
    try:
        service.register_timeline_commit_provider(occupancy_provider)
        commits = _commits(service)
        commits.bootstrap(project, "main", authorize=lambda: None)
        _seed_occupied(service, commits, project, "main")
        if tamper == "receipt":
            body = _patch_shot_body(service, commits, project, "main", name="Unverified", key="tampered")
            _conn(service).execute("DELETE FROM command_idempotency WHERE command_kind='timeline.commit'")
        elif tamper == "occurrence":
            body = _patch_shot_body(service, commits, project, "main", name="Unverified", key="tampered")
            _conn(service).execute("DELETE FROM composition_revision_occurrences WHERE parent_revision_id=(SELECT revision_id FROM parent_composition_heads WHERE timeline_id='main')")
        elif tamper == "digest":
            body = _patch_shot_body(service, commits, project, "main", name="Unverified", key="tampered")
            revision = _head(service, project, "main")["revision_id"]
            _conn(service).execute("UPDATE parent_composition_revisions SET content_digest=? WHERE id=?", ("sha256:" + "0" * 64, revision))
        elif tamper == "projection":
            _conn(service).execute("UPDATE project_shots SET name='unaccounted' WHERE id='shot-1'")
            body = _candidate(service, commits, project, "target")
        else:
            from astrid.sdk.timeline.native_occurrence_delete import capture_occurrence_delete

            _submit(service, project, "main", [capture_occurrence_delete(
                _bundle(commits, service, project, "main"), "occurrence:occ-1")], "removed")
            body = _candidate(service, commits, project, "target")
        before = tuple(_conn(service).iterdump())
        with _validation_no_writes(service), pytest.raises(RuntimeErrorBase) as error:
            timeline = "target" if tamper in {"projection", "removed"} else "main"
            service.commit_timeline(project, timeline, body, idempotency_key="tampered",
                                    publisher="occupancy-test", invocation_path=route_path(project, timeline),
                                    authorize=lambda: None)
        _assert_refusal(
            error,
            reason=("destination_occupied" if tamper in {"projection", "removed"} else "invalid_closure" if tamper == "digest" else None),
            status=422 if tamper == "digest" else 409,
        )
        assert tuple(_conn(service).iterdump()) == before
    finally:
        service.close()


@pytest.mark.parametrize("inline", [False, True])
def test_legacy_historical_reuse_keeps_newer_global_shot_head(tmp_path, occupancy_provider, inline):
    service, project = _service(tmp_path)
    try:
        service.register_timeline_commit_provider(occupancy_provider)
        commits = _commits(service)
        commits.bootstrap(project, "main", authorize=lambda: None)
        _seed_occupied(service, commits, project, "main")
        source_head = _head(service, project, "main")
        source_document = _document(commits, project, "main", service)
        assert source_document is not None
        source_parent = source_document["parent_revision"]
        assert source_parent is not None
        _prepare_timeline(service, commits, project, "other")
        from astrid.sdk.timeline.native_timeline_duplicate import copy_command

        duplicate = copy_command({
            "project_id": project, "timeline_id": "main", "revision_id": source_head["revision_id"],
            "publication_id": source_head["publication_id"],
            "content_digest": source_parent["content_digest"],
        }, {"shot-1": "linked-shot"}, {"occ-1": "linked-occurrence"})
        copied, _ = _submit(service, project, "other", [duplicate], "historical-copy")
        assert copied["data"]["status"] == "accepted"
        _patch_shot(service, commits, project, "main", name="NEWER GLOBAL SHOT", key="newer")
        newer_head_row = _conn(service).execute(
            "SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'"
        ).fetchone()
        assert newer_head_row is not None
        newer_head = newer_head_row[0]
        _prepare_timeline(service, commits, project, "historical")
        historical = copy_command({
            "project_id": project, "timeline_id": "main", "revision_id": source_head["revision_id"],
            "publication_id": source_head["publication_id"],
            "content_digest": source_parent["content_digest"],
        }, {"shot-1": "historical-shot"}, {"occ-1": "historical-occurrence"})
        # Both legacy forms now resolve through the same authenticated source_ref;
        # keep them as separate commits so each retained scenario exercises it.
        result, _ = _submit(service, project, "historical", [historical],
                            "historical-reuse-" + str(inline),
                            label="historical inline" if inline else "historical referenced")
        assert result["data"]["status"] == "accepted"
        assert _conn(service).execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == newer_head
        assert result["data"]["canonical_document"]["shot_revisions"][0]["shot_id"] == "historical-shot"
    finally:
        service.close()
