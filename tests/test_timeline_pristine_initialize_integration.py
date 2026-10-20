"""Approved Agent init through normal generated Runtime admission, without a publisher seed."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from runtime_protocol.errors import ConflictError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
from test_timeline_empty_shell_repair import _retain_document, _shell
from test_timeline_headless_overwrite_refused import _scoped_rows

pytestmark = pytest.mark.integration

OUTPUT = {"resolution": "1280x720", "fps": 30, "file": "output.mp4",
          "background": None, "background_scale": None}
TRACKS = [{"id": identity, "kind": kind, "label": identity, "scale": 1,
           "fit": "contain", "opacity": 1, "blendMode": "normal"}
          for identity, kind in (("V1", "visual"), ("A1", "audio"))]


def head(service, project):
    row = service.get_project_timeline(project, "main")
    return {"revision_id": row["head_revision_id"], "publication_id": row["head_publication_id"]}


def document(service, project):
    return service._timeline_commits()[0].revision_closure(project, "main", head(service, project)["revision_id"])


def request(service, project, calls):
    base = head(service, project)
    return {"api_version": 1, "project_id": project, "timeline_id": "main",
            "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
            "commands": copy.deepcopy(calls), "source": {"via": "python"}}


def submit(service, project, body, key):
    return service.commit_timeline(project, "main", body, idempotency_key=key, publisher="initializer",
                                   invocation_path=route_path(project, "main"), authorize=lambda: None)


def batch(basis, name="Main", slug="main"):
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_initialize import capture_initialize

    bundle = bundle_from_document(basis)
    calls = [capture_initialize(bundle, name=name, slug=slug, output=copy.deepcopy(OUTPUT))]
    for row in TRACKS:
        calls.append(capture_track_create(execute(bundle, calls).bundle, "parent", copy.deepcopy(row)))
    return calls


def inverse(result):
    return {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
            "args": {"publications": [result["receipt"]["receipt_id"]]}}


def snapshot(service):
    return (tuple(service.store.conn.iterdump()),
            {str(p.relative_to(service.store.cas_root)): p.read_bytes()
             for p in service.store.cas_root.rglob("*") if p.is_file()})


@pytest.fixture
def approved_agent(astrid_importable, monkeypatch):
    from astrid.sdk.timeline import commit
    assert Path(commit.__file__).resolve().is_relative_to(astrid_importable)
    schema = astrid_importable / "astrid/core/timeline/schema/edit-command.schema.json"
    assert hashlib.sha256(schema.read_bytes()).hexdigest() == "e29c4542a79e5c2098251ac3ff80a47883d08878b79592aa920f1e3321274159"

    def forbidden(*args, **kwargs):
        raise AssertionError("initialization called a compatibility writer or renderer")

    for name in ("publish_parent_composition", "create_timeline_document", "update_timeline",
                 "create_document", "update_document", "replace_timeline_clip", "publish_timeline_render"):
        monkeypatch.setattr(RuntimeService, name, forbidden)
    monkeypatch.setattr("runtime_protocol.service.evaluate_closure", forbidden)
    monkeypatch.setattr("runtime_protocol.visual_seam.evaluate_closure", forbidden)
    return commit


@pytest.fixture
def actual(tmp_path, approved_agent):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    project = service.create_project({"slug": "init", "name": "Init"}, idempotency_key="project")["id"]
    try:
        yield service, project
    finally:
        service.close()


@pytest.mark.parametrize("name,slug", [("Main", "main"), ("Timeline 2", "timeline-2"), ("!!!", "timeline"), ("", "timeline")])
def test_create_init_exact_original_app_defaults(actual, name, slug):
    service, project = actual
    created = service.create_timeline(project, "main", name=name or None, idempotency_key="create")
    basis = document(service, project)
    assert head(service, project) == {"revision_id": created["data"]["head_revision_id"],
                                     "publication_id": created["data"]["head_publication_id"]}
    calls = batch(basis, name, slug)
    accepted = submit(service, project, request(service, project, calls), "init")
    expected = {"name": name, "slug": slug, "config": {"clips": [], "tracks": TRACKS, "output": OUTPUT},
                "registry": {"assets": {}}, "clips": [], "occurrences": []}
    assert document(service, project)["parent_revision"]["payload"] == expected
    assert service.get_project_parent_composition_revision(
        project, "main", head(service, project)["revision_id"])["payload"] == expected
    entry = next(item for item in service.list_timeline_commits(project, "main", authorize=lambda: None)["items"]
                 if item["publication_id"] == accepted["receipt"]["receipt_id"])
    writes = entry["records"]["commands"][0]["writes"]
    assert [(w["ref"], w["path"]) for w in writes] == [
        ("parent", ["config", "output"]), ("parent", ["name"]),
        ("parent", ["slug"]), ("parent", ["registry", "assets"])]
    assert all(w["before"] == {"state": "absent"} for w in writes)
    undone = submit(service, project, request(service, project, [inverse(accepted)]), "undo")
    assert document(service, project) == basis
    redone = submit(service, project, request(service, project, [inverse(undone)]), "redo")
    assert redone["data"]["canonical_document"] == accepted["data"]["canonical_document"]


@pytest.mark.parametrize("later_edit", [False, True])
def test_create_init_lost_ack_restart_and_late_retries_never_reapply_defaults(tmp_path, approved_agent, monkeypatch, later_edit):
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.outbox import Outbox

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()

    def reopen(service=None):
        if service is not None:
            service.close()
        result = RuntimeService(root)
        result.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        return result

    service = reopen()
    try:
        project = service.create_project({"slug": "retry", "name": "Retry"})["id"]
        outbox = Outbox(tmp_path / "outbox.json")
        intent = {"create": {"project_id": project, "timeline_id": "main", "name": "Main",
                             "idempotency_key": "create"}, "init_key": "init", "name": "Main", "slug": "main"}
        with outbox.locked():
            outbox.write(intent)
        created = service.create_timeline(**intent["create"])
        basis = document(service, project)
        service = reopen(service)
        recovered = Outbox(outbox.path).read()
        before = snapshot(service)
        assert service.create_timeline(**recovered["create"]) == created
        assert snapshot(service) == before
        original = request(service, project, batch(basis, recovered["name"], recovered["slug"]))
        with outbox.locked():
            outbox.write({**recovered, "in_flight": original})
        initialized = submit(service, project, original, "init")
        service = reopen(service)
        before = snapshot(service)
        assert submit(service, project, Outbox(outbox.path).read()["in_flight"], "init") == initialized
        assert snapshot(service) == before
        if later_edit:
            edit = {"schema_version": 1, "op": "track.set", "version": "1", "select": "parent/track:V1",
                    "args": {"values": {"label": "Later"}, "clear": []}}
            edited = submit(service, project, request(service, project, [edit]), "later-edit")
            assert document(service, project)["parent_revision"]["payload"]["config"]["tracks"][0]["label"] == "Later"
            before = snapshot(service)
            with pytest.raises(RuntimeErrorBase):
                submit(service, project, request(service, project, [inverse(initialized)]), "unsafe-inverse")
            assert snapshot(service) == before
            submit(service, project, request(service, project, [inverse(edited)]), "undo-edit")
            # The edit + inverse remains an intervening write even with equal bytes.
            before = snapshot(service)
            with pytest.raises(RuntimeErrorBase):
                submit(service, project, request(service, project, [inverse(initialized)]), "aba-inverse")
            assert snapshot(service) == before
        else:
            submit(service, project, request(service, project, [inverse(initialized)]), "undo-init")
            assert document(service, project) == basis
        retired = head(service, project)
        service = reopen(service)

        def forbidden(*args, **kwargs):
            raise AssertionError("accepted retry reran Agent semantics")

        before = snapshot(service)
        with monkeypatch.context() as retry:
            retry.setattr(commands, "execute", forbidden)
            retry.setattr(approved_agent.RuntimeCommitService, "commit", forbidden)
            assert service.create_timeline(**recovered["create"]) == created
            assert submit(service, project, original, "init") == initialized
        assert snapshot(service) == before and head(service, project) == retired
        for key, body in (("new-init-original-base", original),
                          ("new-init-current-base", request(service, project, original["commands"]))):
            with pytest.raises(RuntimeErrorBase) as error:
                submit(service, project, body, key)
            assert error.value.details["reason"] == "not_pristine"
            assert snapshot(service) == before
        changed = copy.deepcopy(original)
        changed["commands"][0]["args"]["name"] = "Changed"
        with pytest.raises(RuntimeErrorBase) as error:
            submit(service, project, changed, "init")
        assert error.value.details["reason"] == "idempotency_mismatch"
        with pytest.raises(ConflictError):
            service.create_timeline(project, "main", name="Changed", idempotency_key="create")
        assert snapshot(service) == before
    finally:
        service.close()


@pytest.mark.xfail(strict=True, raises=ConflictError,
                   reason="03:20 requirement: same-ID create must bootstrap a genuinely empty resource with no parent head")
def test_genuinely_empty_no_head_same_id_repair_then_init(tmp_path, approved_agent):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "shell", "name": "Shell"})["id"]
        original = service.create_timeline(project, "main", idempotency_key="old-create")
        assert service.get_project_timeline(project, "main")["head_revision_id"] is None
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        repaired = service.create_timeline(project, "main", idempotency_key="repair")
        assert repaired["data"]["timeline_id"] == "main"
        accepted = submit(service, project, request(service, project, batch(document(service, project))), "init")
        assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["output"] == OUTPUT
        before = snapshot(service)
        assert service.create_timeline(project, "main", idempotency_key="old-create") == original
        assert service.create_timeline(project, "main", idempotency_key="repair") == repaired
        assert snapshot(service) == before
    finally:
        service.close()


@pytest.mark.parametrize("hidden", ["document", "timeline_references", "timeline_shots", "snapshot", "dependency"])
def test_hidden_authored_bytes_scope_and_dependencies_refuse_zero_writes(tmp_path, approved_agent, hidden):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "hidden", "name": "Hidden"})["id"]
        service.create_timeline(project, "main", idempotency_key="old-create")
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        # SQL models only retained historical corrupt/hidden input, never a successful init basis.
        _shell(service, project)
        if hidden == "document":
            _retain_document(service, project, {"config": {"opaque": [None, False, {"__proto__": 1}]},
                                                "slug": "authored", "registry": {"assets": {}}})
        else:
            _scoped_rows(service, project, hidden)
        before, changes = snapshot(service), service.store.conn.total_changes
        for key in ("repair", "repair"):
            with pytest.raises(ConflictError):
                service.create_timeline(project, "main", idempotency_key=key)
            assert snapshot(service) == before and service.store.conn.total_changes == changes
    finally:
        service.close()


def test_generated_client_real_door_create_init_restart_undo_and_exact_retry(tmp_path, approved_agent, monkeypatch):
    from astrid_runtime_client import CONTRACT_VERSION, WorkspaceClient
    from astrid_runtime_client.contract_metadata import SCHEMA_DIGEST as CLIENT_DIGEST
    from astrid.sdk.timeline import commands
    from runtime_protocol.contract_metadata import SCHEMA_DIGEST
    from runtime_protocol.daemon import RuntimeDaemon
    from runtime_protocol.door import DoorConfig
    from tests.door_helpers import HOSTED, DoorWorld

    assert CONTRACT_VERSION == "0.2.14" and CLIENT_DIGEST == SCHEMA_DIGEST
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    credential = tmp_path / "credential.json"
    traffic = []

    def start():
        daemon = RuntimeDaemon(root, support_root=tmp_path / "support", authoring_profile="astrid",
                               door=DoorConfig(origin=HOSTED, port=0, credential_file=credential)).start()
        world = DoorWorld(tmp_path, daemon, credential)
        world.provision()

        def transport(method, path, headers, body):
            traffic.append((method, path))
            reply = world.call("/api/runtime" + path, method, headers=headers, body=body)
            return reply.status, reply.headers, reply.body

        client = WorkspaceClient(daemon.door_endpoint, transport=transport)
        assert client.health().schema_digest == SCHEMA_DIGEST
        assert daemon.service._timeline_commit_provider.__class__ is approved_agent.RuntimeCommitService
        return daemon, client

    daemon, client = start()
    try:
        project = client.create_project("Door init", slug="door-init", idempotency_key="project")["project_id"]
        created = client.create_timeline(project, "main", name="Main", idempotency_key="create")
        basis = document(daemon.service, project)
        initial = head(daemon.service, project)
        assert initial == {"revision_id": created["head_revision_id"], "publication_id": created["head_publication_id"]}
        daemon.stop()
        daemon, client = start()
        assert client.create_timeline(project, "main", name="Main", idempotency_key="create") == created
        original = request(daemon.service, project, batch(basis))
        accepted = client.commit_timeline(project, "main", original, idempotency_key="init")
        assert accepted["data"]["canonical_document"]["parent_revision"]["payload"] == {
            "name": "Main", "slug": "main", "config": {"clips": [], "tracks": TRACKS, "output": OUTPUT},
            "registry": {"assets": {}}, "clips": [], "occurrences": []}
        daemon.stop()
        daemon, client = start()
        assert client.commit_timeline(project, "main", original, idempotency_key="init") == accepted
        client.commit_timeline(project, "main", request(daemon.service, project, [inverse(accepted)]), idempotency_key="undo")
        assert document(daemon.service, project) == basis
        retired = head(daemon.service, project)
        assert retired["revision_id"] == initial["revision_id"] and retired != initial
        daemon.stop()
        daemon, client = start()

        def forbidden(*args, **kwargs):
            raise AssertionError("HTTP exact retry reran Agent semantics")

        before = snapshot(daemon.service)
        with monkeypatch.context() as retry:
            retry.setattr(commands, "execute", forbidden)
            retry.setattr(approved_agent.RuntimeCommitService, "commit", forbidden)
            assert client.create_timeline(project, "main", name="Main", idempotency_key="create") == created
            assert client.commit_timeline(project, "main", original, idempotency_key="init") == accepted
        assert snapshot(daemon.service) == before and head(daemon.service, project) == retired
        assert len(client.list_timeline_commits(project, "main")["items"]) == 3
        assert not any("composition-revisions" in path or "timeline-documents" in path for _, path in traffic)
    finally:
        daemon.stop()


def test_real_acceptance_race_edit_undo_cannot_reopen_pristine_init(actual, monkeypatch):
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    service, project = actual
    service.create_timeline(project, "main", idempotency_key="create")
    basis = document(service, project)
    original = request(service, project, batch(basis))
    accept = RequestCommitPort.accept
    intervened = []

    def race(port, prepared):
        if not intervened and prepared["records"]["commands"][0]["command"]["op"] == "timeline.init":
            intervened.append(True)
            call = {"schema_version": 1, "op": "track.create", "version": "1", "select": "parent",
                    "args": {"row": {"id": "later", "kind": "visual"}}}
            edited = submit(service, project, request(service, project, [call]), "race-edit")
            submit(service, project, request(service, project, [inverse(edited)]), "race-undo")
            assert document(service, project) == basis
            intervened.append(snapshot(service))
        return accept(port, prepared)

    monkeypatch.setattr(RequestCommitPort, "accept", race)
    with pytest.raises(RuntimeErrorBase) as error:
        submit(service, project, original, "racing-init")
    assert error.value.details["reason"] == "not_pristine"
    assert snapshot(service) == intervened[1]
    assert len(service.list_timeline_commits(project, "main", authorize=lambda: None)["items"]) == 3
