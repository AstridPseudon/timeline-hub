"""Required M1 lane: real CLI/SDK outbox, Runtime restart, readback and inverse.

Run with ``pytest -m integration tests/editing_conformance/test_commit_runtime_m1.py``
against the paired Runtime checkout selected by tests.helpers.runtime.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.fixture
def film(tmp_path, monkeypatch):
    runtime = use_runtime()
    # Reuse Runtime's API-built duplicate realm/CAS fixture, as its own real
    # provider lane does. Never create a second bootstrap or DB model here.
    monkeypatch.syspath_prepend(str(runtime / "tests"))
    from runtime_protocol.service import RuntimeService
    from timeline_commit_film_fixture import build_film_fixture

    fixture = build_film_fixture(tmp_path)
    service = RuntimeService(fixture.duplicate_root)
    try:
        original = service.get_project_parent_composition_revision(
            fixture.project_id, fixture.timeline_id, fixture.parent_revision_id,
        )
        parent = copy.deepcopy(original["payload"])
        parent["config"]["tracks"].append({"id": "music-other", "kind": "audio"})
        parent["clips"][0]["app"] = {
            "on": "word:word-1", "until": None, "until_film_end": True,
            "astrid": {"on": "word:word-1", "until": None, "until_film_end": True,
                       "fixed_start": False, "for": 5.5, "opaque": [None, {"keep": True}]},
        }
        parent["clips"].append({
            "id": "music-other", "clipType": "audio", "asset": "music-bed",
            "track": "music-other", "at": 0, "hold": 5.5,
            "extension": {"opaque": [None, {"keep": True}]},
        })
        parent["config"]["clips"] = copy.deepcopy(parent["clips"])
        publication = service.publish_parent_composition(
            fixture.project_id, fixture.timeline_id,
            {"project_id": fixture.project_id, "timeline_id": fixture.timeline_id,
             "expected_head": fixture.parent_revision_id,
             "parent_revision_id": "m1-journey-baseline", "parent_composition": parent},
            idempotency_key="m1-journey-baseline",
        )
    finally:
        service.close()
    return fixture, parent, publication


@pytest.fixture
def renderer_off(film, monkeypatch):
    class NoSceneImports:
        def find_spec(self, fullname, path=None, target=None):
            if (fullname.startswith(("composition", "remotion",
                                     "astrid.sdk.authoring_render_preview",
                                     "astrid.core.timeline.compatibility"))
                    or ".scene" in fullname):
                raise AssertionError("commit imported scene evaluation: " + fullname)

    monkeypatch.setattr(sys, "meta_path", [NoSceneImports(), *sys.meta_path])

    def unavailable(*args, **kwargs):
        raise AssertionError("commit evaluated a scene with the renderer off")

    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    # The neutral film seed predates this tripwire. Actual commits, all exact
    # reads and inverse stay under it, including the restarted provider.
    monkeypatch.setattr(service_module, "evaluate_closure", unavailable)
    monkeypatch.setattr(visual_seam, "evaluate_closure", unavailable)


@pytest.fixture
def wire(renderer_off, monkeypatch):
    from runtime_protocol.server import RuntimeHandler

    original = RuntimeHandler._send
    observed = []
    lose = set()

    def send(handler, status, payload=None, **kwargs):
        if (handler.command == "POST" and handler.path.endswith("/commit")
                and getattr(handler, "_defer_response", False)):
            key = handler.headers["Idempotency-Key"]
            observed.append({"path": handler.path, "key": key,
                             "body": handler._prefetched_body,
                             "status": status, "response": copy.deepcopy(payload)})
            if status == 200 and key in lose:
                # commit_timeline has returned its durable real acceptance.
                # Close before any HTTP response bytes; the generated transport
                # must report ambiguity and the actual SDK must retain flight.
                lose.remove(key)
                raise ConnectionError("M1 injected lost ACK after durable acceptance")
        return original(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, "_send", send)
    return observed, lose


def open_client(daemon, *, actor="owner", credential=None, realm=None):
    from astrid.sdk.client import AstridClient

    return AstridClient.open(
        endpoint=daemon.endpoint, credential=credential or daemon.credential_path,
        realm_id=realm or daemon.service.realm["id"], actor_id=actor,
        client_name="m1-commit-journey", client_version="1", protocol_version="workspace.v1",
    )


def history(client, fixture):
    result = client.timelines.history(fixture.project_id, fixture.timeline_id, limit=100)
    assert result.ok, result.as_dict()
    return result.data


def cli(client, fixture, capsys, *args):
    from astrid.packs.timeline.cli import build_parser

    parsed = build_parser(client).parse_args([
        *args, "--project", fixture.project_id, "--json",
    ])
    code = parsed.handler(parsed)
    output = capsys.readouterr()
    value = json.loads(output.out)
    assert code == 0, (code, value, output.err)
    assert value["ok"], value
    return value


def parent_of(result):
    return result["data"]["canonical_document"]["parent_revision"]["payload"]


def assert_move(before, after, clip_id, on):
    expected = copy.deepcopy(before)
    clip = next(row for row in expected["clips"] if row["id"] == clip_id)
    clip["at"] = on
    app = clip.setdefault("app", {})
    authored = app.setdefault("astrid", {})
    for container in (app, authored):
        for key in ("on", "until", "until_film_end"):
            container.pop(key, None)
    authored.update(fixed_start=True, **{"for": 5.5})
    expected["config"]["clips"] = copy.deepcopy(expected["clips"])
    assert after == expected


def assert_readback(client, fixture, accepted):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle

    data, receipt = accepted["data"], accepted["receipt"]
    revision = data["accepted_revision_id"]
    document = data["canonical_document"]
    assert receipt["result"] == {key: value for key, value in data.items()
                                  if key not in {"accepted_publication_id", "show_command"}}
    assert revision == document["parent_revision"]["revision_id"]
    stored = client._remote._transport.get_project_parent_composition_revision(
        fixture.project_id, fixture.timeline_id, revision,
    )
    assert stored["project_id"] == document["project_id"] == fixture.project_id
    assert stored["timeline_id"] == document["timeline_id"] == fixture.timeline_id
    for key, value in document["parent_revision"].items():
        assert stored[key] == value
    assert stored["dependency_manifest"] == document["dependency_manifest"]
    # Main's lossless authoring codec represents occurrences as placements,
    # with exact shot/internal pins and any identity remapping in source_mapping.
    expected_bundle = open_authoring_bundle(
        {**document["parent_revision"], "project_id": fixture.project_id,
         "timeline_id": fixture.timeline_id},
        shot_revisions=[{**row, "project_id": fixture.project_id}
                        for row in document["shot_revisions"]],
        internal_timeline_revisions=[{**row, "project_id": fixture.project_id}
                                     for row in document["internal_timeline_revisions"]],
    )
    opened = client.timelines.open_bundle(fixture.project_id, fixture.timeline_id, revision_id=revision)
    assert opened.ok, opened.as_dict()
    assert opened.data["revision_id"] == revision
    assert opened.data["bundle"] == expected_bundle
    entry = next(row for row in history(client, fixture)["items"]
                 if row["publication_id"] == receipt["receipt_id"])
    assert entry["revision_id"] == revision
    assert entry["receipt"] == receipt
    assert [row["command"] for row in entry["records"]["commands"]] == data["commands"]
    assert entry["publisher"] == "owner"


@pytest.mark.parametrize("touched_basis", [False, True], ids=["disjoint-rebase-undo", "touched-basis-conflict"])
def test_cli_python_outbox_restart_and_guarded_inverse(
    tmp_path: Path, monkeypatch, capsys, film, wire, real_runtime, touched_basis,
):
    from astrid.sdk.exceptions import ServiceUnavailableError
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
    from astrid.sdk.workspace_client import WorkspaceClientError

    fixture, original_parent, baseline = film
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "client-data"))
    observed, lose = wire
    support = tmp_path / "support"

    def start(port=0):
        return real_runtime(fixture.duplicate_root, support_root=support,
                            port=port, authoring_profile="astrid")

    daemon = start()
    client = open_client(daemon)
    base_history = history(client, fixture)
    assert len(base_history["items"]) == 2
    assert base_history["items"][-1]["receipt"] == baseline["receipt"]
    assert all(row["intent"] == "legacy_unknown" and row["records"] is None
               for row in base_history["items"])

    moved = cli(client, fixture, capsys, "edit", "move", fixture.timeline_id,
                "--clip", "parent/clip:music-bed", "--on", "1")
    assert_move(original_parent, parent_of(moved), "music-bed", 1)
    assert observed[-1]["response"]["data"]["canonical_document"] == moved["data"]["canonical_document"]
    assert json.loads(observed[-1]["body"])["source"] == {"via": "cli"}
    assert_readback(client, fixture, moved)

    outbox = tmp_path / "python-outbox.json"
    session = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                   client=client, outbox_path=outbox)
    a = session.queue_move("parent/clip:music-bed", 2)
    lose.add("python-flight-a")
    with pytest.raises(WorkspaceClientError):
        session.flush(idempotency_key="python-flight-a")
    first_wire = copy.deepcopy(observed[-1])
    assert first_wire["status"] == 200
    accepted_a = first_wire["response"]
    persisted = json.loads(outbox.read_bytes())
    flight_a = copy.deepcopy(persisted["flight"])
    assert flight_a["path"] == first_wire["path"]
    assert flight_a["body"].encode() == first_wire["body"]
    assert flight_a["key"] == first_wire["key"]
    assert persisted["pending"] == [a]
    assert_readback(client, fixture, accepted_a)
    assert_move(parent_of(moved), parent_of(accepted_a), "music-bed", 2)

    # B is authored while A is still unacknowledged, against local A, then
    # retained verbatim. Another author's disjoint edit advances the real head.
    b = session.queue_move("parent/clip:music-bed", 3)
    assert b["expect"]["parent/clip:music-bed::at"] == {"state": "present", "value": 2}
    guard_b = json.dumps(b, sort_keys=True)
    assert json.loads(outbox.read_bytes())["pending"] == [a, b]
    other = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                client=client, outbox_path=tmp_path / "other-outbox.json")
    disjoint = other.move("parent/clip:music-other", 2)
    assert_move(parent_of(accepted_a), parent_of(disjoint), "music-other", 2)
    if touched_basis:
        other.move("parent/clip:music-bed", 4)
    before_restart = copy.deepcopy(history(client, fixture))
    assert len(before_restart["items"]) == (6 if touched_basis else 5)
    port, instance = daemon.httpd.server_port, daemon.instance_id
    epoch = client._remote._transport.health()["runtime_epoch"]
    daemon.stop()
    del session, client

    # Same realm and support root, actual startup provider/credentials and new
    # validated public connection. No replacement of private client internals.
    daemon = start(port)
    assert daemon.instance_id != instance
    with pytest.raises(ServiceUnavailableError):
        open_client(daemon, realm="foreign-realm")
    with pytest.raises(ServiceUnavailableError):
        open_client(daemon, actor="foreign-actor")
    client = open_client(daemon)
    assert client._remote._transport.health()["runtime_epoch"] > epoch
    session = TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                   client=client, outbox_path=outbox)
    assert json.loads(outbox.read_bytes())["flight"] == flight_a
    assert history(client, fixture) == before_restart
    retried = session.flush()
    retry_wire = observed[-1]
    assert {key: retry_wire[key] for key in ("path", "key", "body")} == {
        key: first_wire[key] for key in ("path", "key", "body")}
    assert retry_wire["response"] == accepted_a
    assert retried["receipt"] == accepted_a["receipt"]
    assert history(client, fixture) == before_restart
    pending = json.loads(outbox.read_bytes())
    accepted_pair = {"revision_id": accepted_a["data"]["accepted_revision_id"],
                     "publication_id": accepted_a["receipt"]["receipt_id"]}
    assert pending["base"] == accepted_pair
    assert pending["pending"] == [b] and pending["flight"] is None
    assert json.dumps(pending["pending"][0], sort_keys=True) == guard_b
    with pytest.raises(TimelineEditError, match="different realm, actor, project or timeline"):
        _wrong_scope(daemon, fixture, outbox)

    if touched_basis:
        with pytest.raises(CommitConflict) as error:
            session.flush()
        assert error.value.failure["details"]["status"] == "conflict"
        refused = json.loads(outbox.read_bytes())
        assert refused["pending"] == [b]
        assert refused["conflict"] == error.value.failure
        assert refused["flight"]["key"] != flight_a["key"]
        body_b = json.loads(refused["flight"]["body"])
        assert body_b["commands"] == [b]
        assert (body_b["base_revision_id"], body_b["base_publication_id"]) == (
            accepted_pair["revision_id"], accepted_pair["publication_id"])
        assert history(client, fixture) == before_restart
        return

    accepted_b = session.flush()
    body_b = json.loads(observed[-1]["body"])
    assert observed[-1]["key"] != flight_a["key"]
    assert (body_b["base_revision_id"], body_b["base_publication_id"]) == (
        accepted_pair["revision_id"], accepted_pair["publication_id"])
    assert body_b["commands"] == [b]
    assert json.dumps(body_b["commands"][0], sort_keys=True) == guard_b
    assert accepted_b["data"]["status"] == "rebased"
    assert_move(parent_of(disjoint), parent_of(accepted_b), "music-bed", 3)
    assert json.loads(outbox.read_bytes())["pending"] == []
    assert_readback(client, fixture, accepted_b)
    after_b = history(client, fixture)["items"]
    assert len(after_b) == 6
    assert after_b[:-1] == before_restart["items"]

    undone = cli(client, fixture, capsys, "undo", fixture.timeline_id,
                 "--publication", accepted_b["receipt"]["receipt_id"])
    assert json.loads(observed[-1]["body"])["commands"] == [{
        "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
        "args": {"publications": [accepted_b["receipt"]["receipt_id"]]},
    }]
    assert parent_of(undone) == parent_of(disjoint)
    assert_readback(client, fixture, undone)
    revision = undone["data"]["accepted_revision_id"]
    shown = cli(client, fixture, capsys, "show", fixture.timeline_id,
                "--published", "--revision-id", revision)
    assert shown["data"]["revision_id"] == revision
    assert shown["data"]["working_copy"] is None
    layers = cli(client, fixture, capsys, "show", fixture.timeline_id,
                 "--published", "--revision-id", revision, "--layers", "--clip", "music-bed")
    inspection = layers["data"]["native_inspection"]
    assert inspection["revision_id"] == revision
    clip = inspection["selected_parent_clips"][0]
    assert clip["clip_id"] == "music-bed"
    assert clip["start"] == [2, 1]
    visualized = cli(client, fixture, capsys, "visualize", fixture.timeline_id,
                     "--published", "--revision-id", revision, "--mode", "inputs", "--format", "md")
    assert visualized["data"]["outputs"]["inspection"]["revision_id"] == revision
    after_undo = history(client, fixture)["items"]
    assert len(after_undo) == 7
    assert after_undo[:-1] == after_b
    assert after_undo[-1]["records"]["undo_of"] == [accepted_b["receipt"]["receipt_id"]]
    # After undo, the former accepted revision is still the exact immutable film.
    assert_readback(client, fixture, accepted_b)


def _wrong_scope(daemon, fixture, outbox):
    from astrid.sdk.timeline.sync import TimelineSession

    _, credential = daemon.credentials.provision("second-editor", [
        "handshake", "projects:read", "projects:write", "objects:read", "objects:write",
        "tasks:read", "tasks:write",
    ])
    other = open_client(daemon, actor="second-editor", credential=credential)
    return TimelineSession.open(fixture.project_id, fixture.timeline_id,
                                client=other, outbox_path=outbox)
