"""Public CLI trim versus independent SDK label, on the retained music film.

Run in the explicit integration lane with the current Astrid checkout. Keep
unsupported frontend capture as a failing acceptance assertion, rather than
rewriting the historical film or relaxing the native command's guards.
"""
from __future__ import annotations

import copy
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from time import monotonic

import pytest

from test_timeline_commit_integration import (
    Editing,
    _start_door,
    assert_json_equal,
    film,  # noqa: F401 (verified historical music-film duplicate)
    rows,
)

pytestmark = pytest.mark.integration


@pytest.fixture
def renderer_off(film, astrid_importable, monkeypatch):
    class NoSceneImports:
        def find_spec(self, fullname, path=None, target=None):
            if (fullname.startswith(("composition", "remotion", "node",
                                     "astrid.sdk.authoring_render_preview",
                                     "astrid.core.timeline.compatibility"))
                    or ".scene" in fullname):
                raise AssertionError("journey imported scene evaluation: " + fullname)

    # As in the public M1 journey, permit the pure readable timing helper
    # under packs.rendering; scene evaluation remains unavailable throughout.
    monkeypatch.setattr(sys, "meta_path", [NoSceneImports(), *sys.meta_path])

    def unavailable(*args, **kwargs):
        raise AssertionError("journey evaluated a scene with renderer unavailable")

    monkeypatch.setattr("runtime_protocol.service.evaluate_closure", unavailable)
    monkeypatch.setattr("runtime_protocol.visual_seam.evaluate_closure", unavailable)


def _client(daemon, *, actor="owner", credential=None):
    from astrid.sdk.client import AstridClient

    return AstridClient.open(
        endpoint=daemon.endpoint, credential=credential or daemon.credential_path,
        realm_id=daemon.service.realm["id"], actor_id=actor,
        client_name="public-s2-mixed-journey", client_version="1",
        protocol_version="workspace.v1",
    )


def _cli(client, fixture, capsys, *args):
    from astrid.packs.timeline.cli import build_parser

    parsed = build_parser(client).parse_args([
        *args, "--project", fixture.project_id, "--json",
    ])
    code = parsed.handler(parsed)
    output = capsys.readouterr()
    return code, json.loads(output.out)


def _ok_cli(client, fixture, capsys, *args):
    code, result = _cli(client, fixture, capsys, *args)
    assert code == 0 and result["ok"], (code, result)
    return result


def _views(client, fixture, capsys, revision):
    shown = _ok_cli(client, fixture, capsys, "show", fixture.timeline_id,
                    "--published", "--revision-id", revision)
    assert shown["data"]["revision_id"] == revision
    assert shown["data"]["working_copy"] is None
    layers = _ok_cli(client, fixture, capsys, "show", fixture.timeline_id,
                     "--published", "--revision-id", revision,
                     "--layers", "--clip", "music-bed")
    inspection = layers["data"]["native_inspection"]
    assert inspection["revision_id"] == revision
    assert [row["clip_id"] for row in inspection["selected_parent_clips"]] == ["music-bed"]
    inputs = _ok_cli(client, fixture, capsys, "visualize", fixture.timeline_id,
                     "--published", "--revision-id", revision,
                     "--mode", "inputs", "--format", "md")
    assert inputs["data"]["outputs"]["inspection"]["revision_id"] == revision


def test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo(
    film, renderer_off, tmp_path, monkeypatch, capsys,
):
    from astrid.sdk.timeline._scalar_commands import capture_track_set
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import TimelineSession
    from runtime_protocol.server import RuntimeHandler

    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "client-data"))
    fixture = film.fixture
    key = "public-s2-cli-trim"
    args = ("edit", fixture.timeline_id, "--clip", "parent/clip:music-bed",
            "--trim-out", "4", "--idempotency-key", key)
    paused, release = Event(), Event()
    observed = []
    lose = {key}
    original_route, original_send = RuntimeHandler._route, RuntimeHandler._send

    def route(handler):
        if (handler._is_timeline_commit() and handler.headers.get("Idempotency-Key") == key
                and not paused.is_set()):
            # _dispatch has prefetched the real POST bytes, outside the SQLite
            # mutex. Nothing has reached acceptance, so another author can win.
            paused.set()
            if not release.wait(30):
                raise TimeoutError("mixed journey did not release CLI trim")
        return original_route(handler)

    def send(handler, status, payload=None, **kwargs):
        if (handler._is_timeline_commit() and getattr(handler, "_defer_response", False)):
            request_key = handler.headers["Idempotency-Key"]
            observed.append({"path": handler.path, "key": request_key,
                             "body": handler._prefetched_body,
                             "status": status, "response": copy.deepcopy(payload)})
            if status == 200 and request_key in lose:
                lose.remove(request_key)
                # Existing M1 seam: acceptance is durable; no response bytes
                # reach the real SDK transport or acknowledge its disk outbox.
                raise ConnectionError("mixed journey lost durable trim ACK")
        return original_send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, "_route", route)
    monkeypatch.setattr(RuntimeHandler, "_send", send)
    world = _start_door(film, tmp_path)
    try:
        client = _client(world.daemon)
        edit = Editing(world.daemon.service, film, None)
        edit.assert_baseline()
        h0, original = edit.head(), edit.document()
        assert original["shot_revisions"] and original["internal_timeline_revisions"]
        assert original["dependency_manifest"]["media"]
        cli_session = TimelineSession.open(fixture.project_id, fixture.timeline_id, client=client)
        _, credential = world.daemon.credentials.provision("python-label-editor", [
            "handshake", "projects:read", "projects:write", "objects:read", "objects:write",
            "tasks:read", "tasks:write",
        ])
        peer = TimelineSession.open(
            fixture.project_id, fixture.timeline_id,
            client=_client(world.daemon, actor="python-label-editor", credential=credential),
            outbox_path=tmp_path / "peer.json",
        )
        label = capture_track_set(bundle_from_document(original), "parent/track:music",
                                  values={"label": "Independent Python label"})
        before = rows(edit.service)
        with ThreadPoolExecutor(max_workers=1) as executor:
            pending = executor.submit(_cli, client, fixture, capsys, *args)
            try:
                deadline = monotonic() + 15
                while not paused.wait(0.01) and not pending.done() and monotonic() < deadline:
                    pass
                if not paused.is_set():
                    result = pending.result(timeout=5)
                    assert rows(edit.service) == before
                    assert cli_session.outbox.read()["flight"] is None
                    pytest.fail(
                        "public_s2_cli_trim_must_capture_original_music_film_before_POST: "
                        f"CLI exited without submitting native trim: {result!r}"
                    )
                assert edit.head() == h0
                flight = copy.deepcopy(cli_session.outbox.read()["flight"])
                body = json.loads(flight["body"])
                assert flight["key"] == key and flight["path"] == edit.path
                assert body["source"] == {"via": "cli"}
                assert (body["base_revision_id"], body["base_publication_id"]) == (
                    h0["revision_id"], h0["publication_id"],
                )
                command, = body["commands"]
                assert command["op"] == "clip.trim" and command["select"] == "parent/clip:music-bed"
                assert command["reads"] and command["bindings"] and command["expect"]
                labelled = peer.commit(label, idempotency_key="public-s2-python-label")
                assert labelled["data"]["status"] == "accepted"
                assert labelled["data"]["publisher"] == "python-label-editor"
                release.set()
                code, ambiguous = pending.result(timeout=30)
                assert code == 1 and not ambiguous["ok"], (code, ambiguous)
            finally:
                release.set()

        trim_wire = next(row for row in observed if row["key"] == key)
        assert trim_wire["status"] == 200
        assert (trim_wire["path"], trim_wire["body"], trim_wire["key"]) == (
            flight["path"], flight["body"].encode(), flight["key"],
        )
        accepted = trim_wire["response"]
        assert accepted["data"]["status"] == "rebased"
        assert accepted["data"]["publisher"] == "owner"
        assert accepted["data"]["commands"] == [command]
        assert accepted["data"]["rebased_onto"] == {
            "revision_id": labelled["data"]["accepted_revision_id"],
            "publication_id": labelled["receipt"]["receipt_id"],
        }
        expected_trim = copy.deepcopy(labelled["data"]["canonical_document"]["parent_revision"]["payload"])
        target = next(row for row in expected_trim["clips"] if row["id"] == "music-bed")
        target.update({"from": 0, "to": 4, "hold": 4})
        expected_trim["config"]["clips"] = copy.deepcopy(expected_trim["clips"])
        assert_json_equal(accepted["data"]["canonical_document"]["parent_revision"]["payload"], expected_trim)
        assert cli_session.outbox.read()["flight"] == flight
        saved_history = copy.deepcopy(edit.history())
        assert len(saved_history) == 4  # Two retained legacy entries, label, trim.
        instance = world.daemon.instance_id
        edit.assert_readback(accepted)
        edit.assert_readback(labelled)
    finally:
        release.set()
        world.stop()

    world = _start_door(film, tmp_path)
    try:
        assert world.daemon.instance_id != instance
        client = _client(world.daemon)
        edit = Editing(world.daemon.service, film, None)
        session = TimelineSession.open(fixture.project_id, fixture.timeline_id, client=client)
        assert session.outbox.read()["flight"] == flight
        before = rows(edit.service)

        def forbidden(*args, **kwargs):
            raise AssertionError("exact outbox retry executed the semantic provider")

        with monkeypatch.context() as retry:
            retry.setattr(type(edit.service._timeline_commit_provider), "commit", forbidden)
            retried = _ok_cli(client, fixture, capsys, *args)
        assert retried["receipt"] == accepted["receipt"]
        assert observed[-1] == trim_wire
        assert rows(edit.service) == before
        assert edit.history() == saved_history
        state = session.outbox.read()
        assert state["flight"] is None and state["pending"] == []
        assert state["base"] == {
            "revision_id": accepted["data"]["accepted_revision_id"],
            "publication_id": accepted["receipt"]["receipt_id"],
        }
        _views(client, fixture, capsys, accepted["data"]["accepted_revision_id"])
        undone = _ok_cli(client, fixture, capsys, "undo", fixture.timeline_id,
                         "--publication", accepted["receipt"]["receipt_id"])
        restored = undone["data"]["canonical_document"]
        labelled_document = labelled["data"]["canonical_document"]
        assert_json_equal(restored, labelled_document)
        expected_parent = copy.deepcopy(original["parent_revision"]["payload"])
        next(row for row in expected_parent["config"]["tracks"] if row["id"] == "music")["label"] = (
            "Independent Python label"
        )
        assert_json_equal(restored["parent_revision"]["payload"], expected_parent)
        for family in ("shot_revisions", "internal_timeline_revisions", "dependency_manifest"):
            assert restored[family] == original[family]
            assert accepted["data"]["canonical_document"][family] == original[family]
        for media in restored["dependency_manifest"]["media"]:
            assert edit.service.object_location(fixture.project_id, media["media_id"])["verified"]
        edit.assert_readback(accepted)
        edit.assert_readback(undone)
        edit.assert_baseline()
        _views(client, fixture, capsys, undone["data"]["accepted_revision_id"])
        # The old accepted film remains inspectable after undo advances HEAD.
        _views(client, fixture, capsys, accepted["data"]["accepted_revision_id"])
        final = edit.history()
        assert len(final) == len(saved_history) + 1
        assert final[:-1] == saved_history
        assert final[-1]["records"]["undo_of"] == [accepted["receipt"]["receipt_id"]]
    finally:
        world.stop()
