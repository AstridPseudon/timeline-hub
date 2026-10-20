"""Bounded NativeSheet through authenticated Runtime dispatch, without sockets.

Only the generated client's byte transport is replaced. Authentication, routing,
provider loading, SQLite/CAS acceptance and the SDK outbox are the real products.
Run with ASTRID_RUNTIME_CHECKOUT set and pytest -m integration.
"""
from __future__ import annotations

import copy
import io
import json
import sys
import uuid
from email.message import Message
from types import SimpleNamespace

import pytest

from astrid.sdk.client import AstridClient
from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline.capture import capture_move, capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet, SheetError
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.helpers.runtime import use_runtime
from tests.sdk.test_timeline_sheet_native import edit_cell

pytestmark = pytest.mark.integration


class RuntimeWire:
    """Memory HTTP streams around the actual handler; never fake semantics."""

    def __init__(self, root, credentials):
        self.root, self.credentials = root, credentials
        self.calls, self.lose = [], set()
        self.start()

    def start(self):
        from runtime_protocol.service import RuntimeService
        from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

        self.service = RuntimeService(self.root)
        self.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        self.instance_id = uuid.uuid4().hex

    def restart(self):
        self.service.close()
        self.start()

    def transport(self, method, path, headers, body):
        from runtime_protocol.server import RuntimeHandler

        handler = object.__new__(RuntimeHandler)
        handler.server = SimpleNamespace(runtime=self.service, credentials=self.credentials,
                                         daemon_runtime=self)
        handler.command, handler.path = method, path
        handler.headers = Message()
        for key, value in headers.items():
            handler.headers[key] = value
        raw = body or b""
        handler.headers["Content-Length"] = str(len(raw))
        handler.rfile, handler.wfile = io.BytesIO(raw), io.BytesIO()
        response = {}
        handler.send_response = lambda status: response.update(status=status)
        handler.send_header = lambda key, value: response.setdefault("headers", {}).update({key: value})
        handler.end_headers = lambda: None
        handler._dispatch()
        status, data = response["status"], handler.wfile.getvalue()
        call = {"method": method, "path": path, "body": raw,
                "key": headers.get("Idempotency-Key"), "status": status,
                "response": json.loads(data)}
        self.calls.append(call)
        if path.endswith("/commit") and status == 200 and call["key"] in self.lose:
            self.lose.remove(call["key"])
            raise ConnectionError("lost ACK after real durable acceptance")
        return status, response["headers"], data

    def commits(self):
        return [call for call in self.calls if call["path"].endswith("/commit")]


@pytest.fixture
def film(tmp_path, monkeypatch):
    use_runtime()
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.store import RealmStore

    from astrid.sdk import workspace_client

    def forbidden(*args, **kwargs):
        raise AssertionError("sheet must not use renderer or legacy writer")

    class NoSceneImports:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("composition", "remotion", "astrid.sdk.authoring_render_preview")):
                raise AssertionError("sheet imported renderer: " + fullname)

    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    from astrid.sdk.timeline import store
    from astrid.sdk.timeline_checkout import Checkout

    monkeypatch.setattr(sys, "meta_path", [NoSceneImports(), *sys.meta_path])
    monkeypatch.setattr(service_module, "evaluate_closure", forbidden)
    monkeypatch.setattr(visual_seam, "evaluate_closure", forbidden)
    monkeypatch.setattr(service_module.RuntimeService, "publish_parent_composition", forbidden)
    monkeypatch.setattr(store, "publish_bundle", forbidden)
    monkeypatch.setattr(Checkout, "save", forbidden)
    monkeypatch.setattr(Checkout, "__init__", forbidden)
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "client-data"))
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    credentials = CredentialStore(tmp_path / "credentials")
    _, credential = credentials.provision("owner", [
        "handshake", "projects:read", "projects:write", "objects:read", "objects:write",
        "tasks:read", "tasks:write",
    ])
    wire = RuntimeWire(root, credentials)
    generated = workspace_client.GeneratedWorkspaceClient
    monkeypatch.setattr(workspace_client, "GeneratedWorkspaceClient",
                        lambda endpoint, token: generated(endpoint, token, transport=wire.transport))

    def connect():
        return AstridClient.open(
            endpoint="http://127.0.0.1:1", credential=credential,
            realm_id=wire.service.realm["id"], actor_id="owner",
            client_name="sheet-runtime-proof", client_version="1", protocol_version="workspace.v1",
        )

    try:
        client = connect()
        project = client.projects.create(slug="sheet", name="Sheet")
        assert project.ok, project.as_dict()
        project_id = project.data["project_id"]
        # Runtime's public create now bootstraps a verified empty head itself.
        client._remote._transport.create_timeline(project_id, "film", idempotency_key="create-film")
        realm = SimpleNamespace(wire=wire, client=client, connect=connect,
                                project=project_id, timeline="film", tmp=tmp_path)
        empty = bundle(realm)
        calls = [capture_track_create(empty, "parent", {
            "id": "picture", "kind": "visual", "opaque": [None, False],
        })]
        for name in ("a", "b"):
            calls.append(capture_clip_add(execute(empty, calls).bundle, "parent", {
                "id": name, "track": "picture", "clipType": "text", "at": 0, "hold": 1,
                "params": {"text": name}, "opaque": {"keep": [None, False, {"id": name}]},
            }))
        submit(realm, calls, "seed-native")
        yield realm
    finally:
        wire.service.close()


def history(film):
    result = film.client.timelines.history(film.project, film.timeline, limit=100)
    assert result.ok, result.as_dict()
    return result.data


def bundle(film, revision=None):
    result = film.client.timelines.open_bundle(film.project, film.timeline, revision_id=revision)
    assert result.ok, result.as_dict()
    return result.data["bundle"]


def submit(film, commands, key, *, base=None):
    base = base or history(film)["head"]
    result = film.client.timelines.commit(film.project, film.timeline, {
        "api_version": 1, "project_id": film.project, "timeline_id": film.timeline,
        "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
        "commands": commands,
    }, idempotency_key=key)
    assert result.ok, result.as_dict()
    return result.as_dict()


def open_sheet(film, name="sheet"):
    session = TimelineSession.open(film.project, film.timeline, client=film.client,
                                   outbox_path=film.tmp / (name + ".json"))
    basis = json.loads(session.outbox.path.read_bytes())["base"]
    original = bundle(film, basis["revision_id"])
    return session, NativeSheet(original, basis=basis), original, basis


def gesture(sheet):
    text = edit_cell(sheet.text, "parent/clip:a", "2")
    return edit_cell(text, "parent/track:picture", '"Picture"', label=True)


def readback(film, result):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle

    data = result["data"]
    document = data["canonical_document"]
    stored = film.client._remote._transport.get_project_parent_composition_revision(
        film.project, film.timeline, data["accepted_revision_id"])
    for key, value in document["parent_revision"].items():
        assert stored[key] == value
    assert stored["dependency_manifest"] == document["dependency_manifest"]
    opened = bundle(film, data["accepted_revision_id"])
    assert opened == open_authoring_bundle(
        {**document["parent_revision"], "project_id": film.project, "timeline_id": film.timeline},
        shot_revisions=[{**row, "project_id": film.project} for row in document["shot_revisions"]],
        internal_timeline_revisions=[{**row, "project_id": film.project}
                                     for row in document["internal_timeline_revisions"]],
    )
    entry = next(row for row in history(film)["items"]
                 if row["publication_id"] == result["receipt"]["receipt_id"])
    assert entry["receipt"] == result["receipt"] and entry["publisher"] == "owner"
    assert [row["command"] for row in entry["records"]["commands"]] == data["commands"]
    return opened


def test_preview_batch_acceptance_readback_and_inverse(film):
    session, sheet, original, basis = open_sheet(film)
    text = gesture(sheet)
    before, outbox, calls = history(film), session.outbox.path.read_bytes(), len(film.wire.calls)
    plan = sheet.preview(text)
    assert sheet.apply(text, session=session).commands == plan.commands
    assert sheet.apply(sheet.text, session=session, dry_run=False).commands == []
    assert sheet.preview(sheet.text).commands == []
    assert session.outbox.path.read_bytes() == outbox and len(film.wire.calls) == calls
    expected = [capture_move(original, "parent/clip:a", 2)]
    expected.append(capture_track_set(execute(original, expected).bundle,
                                     "parent/track:picture", values={"label": "Picture"}))
    assert plan.commands == expected
    accepted = sheet.apply(text, session=session, dry_run=False, idempotency_key="sheet-gesture")
    sent = json.loads(film.wire.commits()[-1]["body"])
    assert sent["commands"] == expected and sent["source"] == {"via": "sheet"}
    assert (sent["base_revision_id"], sent["base_publication_id"]) == (
        basis["revision_id"], basis["publication_id"])
    after = history(film)
    assert len(after["items"]) == len(before["items"]) + 1
    assert len(after["items"][-1]["records"]["commands"]) == 2
    actual = readback(film, accepted)
    # Revision identity changes; all authored fields must equal the preview.
    assert actual["parent"] == plan.bundle["parent"]
    assert State(actual).entity("parent/clip:b") == State(original).entity("parent/clip:b")
    undone = session.undo([accepted["receipt"]["receipt_id"]])
    assert readback(film, undone)["parent"] == original["parent"]
    redone = session.undo([undone["receipt"]["receipt_id"]])
    assert readback(film, redone)["parent"] == actual["parent"]
    assert sheet.preview(text).commands == expected  # original claims never refreshed


@pytest.mark.parametrize("relevant", [False, True], ids=["disjoint", "relevant"])
def test_original_sheet_basis_rebases_or_conflicts_atomically(film, relevant):
    session, sheet, original, basis = open_sheet(film)
    text = gesture(sheet)
    expected = sheet.preview(text).commands
    peer = capture_move(original, "parent/clip:a" if relevant else "parent/clip:b", 7)
    submit(film, [peer], "peer")
    before = history(film)
    if relevant:
        with pytest.raises(CommitConflict):
            sheet.apply(text, session=session, dry_run=False)
        state = json.loads(session.outbox.path.read_bytes())
        assert state["pending"] == expected and state["base"] == basis and state["conflict"]
        assert json.loads(state["flight"]["body"])["commands"] == expected
        assert history(film) == before
        assert "label" not in State(bundle(film)).entity("parent/track:picture")
        assert sheet.preview(text).commands == expected
    else:
        result = sheet.apply(text, session=session, dry_run=False)
        assert result["data"]["status"] == "rebased"
        assert result["data"]["commands"] == expected
        assert State(readback(film, result)).entity("parent/clip:b")["at"] == 7
        assert len(history(film)["items"]) == len(before["items"]) + 1
        undone = session.undo([result["receipt"]["receipt_id"]])
        assert readback(film, undone)["parent"] == execute(original, [peer]).bundle["parent"]
    sent = json.loads(film.wire.commits()[-1 if relevant else -2]["body"])
    assert (sent["base_revision_id"], sent["base_publication_id"]) == (
        basis["revision_id"], basis["publication_id"])
    assert sent["commands"] == expected


@pytest.mark.parametrize("relevant", [False, True], ids=["disjoint", "relevant"])
@pytest.mark.parametrize("outbox_name", ["fresh", "sheet"], ids=["new-outbox", "reopened-empty-outbox"])
def test_fresh_session_stale_sheet_refuses_without_recapturing(film, relevant, outbox_name, monkeypatch):
    _, sheet, original, _ = open_sheet(film)
    text = gesture(sheet)
    draft = film.tmp / "edited.sheet"
    draft.write_text(text)
    submit(film, [capture_move(original, "parent/clip:a" if relevant else "parent/clip:b", 7)], "peer")
    fresh, _, _, _ = open_sheet(film, outbox_name)
    before, outbox = history(film), fresh.outbox.path.read_bytes()
    calls = len(film.wire.calls)

    def forbidden(*args, **kwargs):
        raise AssertionError("stale sheet must never recapture from current session bundle")

    monkeypatch.setattr(fresh, "_bundle", forbidden)
    with pytest.raises(SheetError, match="original project, timeline and basis"):
        sheet.apply(text, session=fresh, dry_run=False)
    assert len(film.wire.calls) == calls and fresh.outbox.path.read_bytes() == outbox
    assert draft.read_text() == text and history(film) == before


@pytest.mark.parametrize("change", ["header", "bundle", "pending"])
def test_changed_original_basis_or_other_draft_refuses_without_writes(film, change):
    session, sheet, original, basis = open_sheet(film)
    if change == "bundle":
        original["parent"]["clips"][0]["opaque"]["keep"].append("changed")
        sheet = NativeSheet(original, basis=basis)
    if change == "pending":
        session.queue_move("parent/clip:b", 4)
    text = gesture(sheet)
    if change == "header":
        text = text.replace(basis["publication_id"], "changed-publication")
    draft = film.tmp / "edited.sheet"
    draft.write_text(text)
    before, outbox = history(film), session.outbox.path.read_bytes()
    count = len(film.wire.commits())
    with pytest.raises(SheetError):
        sheet.apply(text, session=session, dry_run=False)
    assert session.outbox.path.read_bytes() == outbox
    assert len(film.wire.commits()) == count and history(film) == before
    assert draft.read_text() == text


@pytest.mark.parametrize("touched_suffix", [False, True], ids=["suffix-rebase", "suffix-conflict"])
def test_lost_ack_restart_exact_flight_and_original_suffix(film, touched_suffix, monkeypatch):
    session, sheet, _, basis = open_sheet(film)
    text = gesture(sheet)
    expected = sheet.preview(text).commands
    film.wire.lose.add("sheet-flight")
    with pytest.raises(WorkspaceClientError):
        sheet.apply(text, session=session, dry_run=False, idempotency_key="sheet-flight")
    first = copy.deepcopy(film.wire.commits()[-1])
    accepted = first["response"]
    flight = json.loads(session.outbox.path.read_bytes())["flight"]
    assert flight["body"].encode() == first["body"] and flight["key"] == first["key"]
    assert json.loads(flight["body"])["commands"] == expected
    suffix = session.queue_move("parent/clip:a", 3)
    assert suffix["expect"]["parent/clip:a::at"] == {"state": "present", "value": 2}
    suffix_json = json.dumps(suffix, sort_keys=True)
    current = bundle(film)
    peer = submit(film, [capture_move(current, "parent/clip:a" if touched_suffix else "parent/clip:b", 7)], "peer")
    before_restart = history(film)
    film.wire.restart()
    film.client = film.connect()  # fresh authenticated public connection, same durable realm
    resumed = TimelineSession.open(film.project, film.timeline, client=film.client,
                                   outbox_path=session.outbox.path)
    assert json.loads(resumed.outbox.path.read_bytes())["flight"] == flight
    # Applying an old sheet over a newer pending suffix refuses without altering it.
    before = resumed.outbox.path.read_bytes()
    with pytest.raises(SheetError, match="flush original pending intent"):
        sheet.apply(text, session=resumed, dry_run=False)
    assert resumed.outbox.path.read_bytes() == before
    with pytest.raises(TimelineEditError, match="immutable"):
        resumed.flush(idempotency_key="changed-key")
    assert resumed.outbox.path.read_bytes() == before
    # Same key with a changed payload is rejected by the actual Runtime receipt store.
    changed = json.loads(flight["body"])
    changed["source"] = {"via": "python"}
    refused = film.client.timelines.commit(film.project, film.timeline, changed,
                                           idempotency_key=flight["key"])
    assert not refused.ok and refused.error.code == "conflict"
    assert history(film) == before_restart
    film.wire.credentials.disable_actor("owner")
    try:
        with pytest.raises(WorkspaceClientError) as denied:
            film.client._remote._transport.commit_timeline(
                film.project, film.timeline, json.loads(flight["body"]), idempotency_key=flight["key"])
        assert denied.value.status == 401
        with pytest.raises(WorkspaceClientError):
            resumed.flush()
        assert resumed.outbox.path.read_bytes() == before
    finally:
        film.wire.credentials.enable_actor("owner")

    def forbidden(*args, **kwargs):
        raise AssertionError("exact retry must not run provider execution")

    with monkeypatch.context() as retry:
        retry.setattr("astrid.sdk.timeline.commands.execute", forbidden)
        result = resumed.flush()
    retried = film.wire.commits()[-1]
    assert {key: retried[key] for key in ("path", "body", "key")} == {
        key: first[key] for key in ("path", "body", "key")}
    assert retried["response"] == accepted and result["receipt"] == accepted["receipt"]
    assert history(film) == before_restart
    state = json.loads(resumed.outbox.path.read_bytes())
    accepted_pair = {"revision_id": accepted["data"]["accepted_revision_id"],
                     "publication_id": accepted["receipt"]["receipt_id"]}
    assert state["base"] == accepted_pair and state["flight"] is None
    assert state["pending"] == [suffix]
    assert json.dumps(state["pending"][0], sort_keys=True) == suffix_json
    readback(film, accepted)
    if touched_suffix:
        with pytest.raises(CommitConflict):
            resumed.flush()
        assert history(film) == before_restart
        state = json.loads(resumed.outbox.path.read_bytes())
        assert state["pending"] == [suffix] and state["conflict"]
    else:
        result = resumed.flush()
        assert result["data"]["status"] == "rebased"
        actual = State(readback(film, result))
        assert actual.entity("parent/clip:a")["at"] == 3
        assert actual.entity("parent/clip:b")["at"] == 7
        assert json.loads(resumed.outbox.path.read_bytes())["pending"] == []
    sent = film.wire.commits()[-1]
    body = json.loads(sent["body"])
    assert sent["key"] != first["key"] and body["commands"] == [suffix]
    assert json.dumps(body["commands"][0], sort_keys=True) == suffix_json
    assert (body["base_revision_id"], body["base_publication_id"]) == (
        accepted_pair["revision_id"], accepted_pair["publication_id"])
    assert sheet.preview(text).commands == expected
    assert accepted["data"]["base_revision_id"] == basis["revision_id"]
    assert State(readback(film, peer)).entity("parent/clip:b" if not touched_suffix else "parent/clip:a")["at"] == 7


def test_sheet_apply_retries_its_original_batch_after_restart(film, monkeypatch):
    session, sheet, _, _ = open_sheet(film)
    text = gesture(sheet)
    film.wire.lose.add("sheet-only")
    with pytest.raises(WorkspaceClientError):
        sheet.apply(text, session=session, dry_run=False, idempotency_key="sheet-only")
    first = copy.deepcopy(film.wire.commits()[-1])
    before = history(film)
    film.wire.restart()
    film.client = film.connect()
    resumed = TimelineSession.open(film.project, film.timeline, client=film.client,
                                   outbox_path=session.outbox.path)

    def forbidden(*args, **kwargs):
        raise AssertionError("sheet retry must not fetch or recapture a session bundle")

    monkeypatch.setattr(resumed, "_bundle", forbidden)
    result = sheet.apply(text, session=resumed, dry_run=False)
    retried = film.wire.commits()[-1]
    assert {key: retried[key] for key in ("path", "key", "body", "response")} == {
        key: first[key] for key in ("path", "key", "body", "response")}
    assert history(film) == before and json.loads(resumed.outbox.path.read_bytes())["pending"] == []
    assert result["receipt"] == first["response"]["receipt"]
    readback(film, result)
