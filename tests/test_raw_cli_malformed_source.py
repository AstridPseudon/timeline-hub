"""Real CLI refusal for the original malformed historical raw-audio fixture."""
from __future__ import annotations

import copy
import json

import pytest

from precut_realm_fixture import readonly_tree_digest
from test_timeline_commit_film_fixture import read_object_from_realm
from test_timeline_commit_integration import _start_door, film  # noqa: F401

pytestmark = pytest.mark.integration


def _cli(client, fixture, capsys, *args):
    from astrid.packs.timeline.cli import build_parser

    parsed = build_parser(client).parse_args([
        *args, "--project", fixture.project_id, "--json",
    ])
    code = parsed.handler(parsed)
    output = capsys.readouterr()
    return code, json.loads(output.out)


def test_original_malformed_raw_cli_trim_refuses_without_acceptance(
    film, astrid_importable, tmp_path, monkeypatch, capsys,
):
    """A 19-byte raw source cannot acquire duration through the CLI path."""
    _ = astrid_importable
    from runtime_protocol.server import RuntimeHandler
    from astrid.sdk.client import AstridClient
    from astrid.sdk.timeline.sync import TimelineSession
    from runtime_protocol.service import RuntimeService

    fixture = film.fixture
    before_source = readonly_tree_digest(fixture.source_root)
    before_service = RuntimeService(fixture.duplicate_root)
    try:
        before_document = before_service._timeline_commits()[0].revision_closure(
            fixture.project_id, fixture.timeline_id, fixture.parent_revision_id,
        )
        asset = before_document["parent_revision"]["payload"]["registry"]["assets"]["music-bed"]
        malformed_id = asset["object_id"]
        malformed = read_object_from_realm(fixture.duplicate_root, malformed_id)
        assert malformed == b"synthetic-music-bed"
        assert len(malformed) == 19
        assert "duration" not in asset
    finally:
        before_service.close()

    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "client-data"))
    observed = []
    original_send = RuntimeHandler._send

    def send(handler, status, payload=None, **kwargs):
        if handler._is_timeline_commit() and not getattr(handler, "_defer_response", False):
            error = kwargs.get("error")
            observed.append({
                "path": handler.path,
                "status": status,
                "body": handler._prefetched_body,
                "response": copy.deepcopy(payload if error is None else error),
            })
        return original_send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, "_send", send)
    world = _start_door(film, tmp_path)
    try:
        client = AstridClient.open(
            endpoint=world.daemon.endpoint,
            credential=world.daemon.credential_path,
            realm_id=world.daemon.service.realm["id"],
            actor_id="owner",
            client_name="malformed-raw-cli-control",
            client_version="1",
            protocol_version="workspace.v1",
        )
        before_head = world.daemon.service.get_project_timeline(
            fixture.project_id, fixture.timeline_id,
        )
        before_rows = tuple(world.daemon.service.store.conn.iterdump())
        before_cas = {
            path.relative_to(world.daemon.service.store.cas_root).as_posix(): path.read_bytes()
            for path in world.daemon.service.store.cas_root.rglob("*") if path.is_file()
        }
        session = TimelineSession.open(
            fixture.project_id, fixture.timeline_id, client=client,
        )
        outbox_bytes = session.outbox.path.read_bytes()
        outbox_state = session.outbox.read()
        assert outbox_state["pending"] == []
        assert outbox_state["flight"] is None

        code, result = _cli(
            client, fixture, capsys,
            "edit", fixture.timeline_id,
            "--clip", "parent/clip:music-bed",
            "--trim-out", "4",
            "--idempotency-key", "malformed-raw-cli-refusal",
        )

        assert code == 1
        assert result["ok"] is False
        assert result["data"] is None
        assert result["receipt"] is None
        error = result["error"]
        assert error["code"] == "timeline_edit_error"
        assert "metadata" in error["message"].lower()
        assert "duration" in error["message"].lower()

        # The normal CLI stopped during capture: it did not invent a draft or
        # turn the local capture refusal into a successful HTTP commit.
        assert observed == []
        assert session.outbox.path.read_bytes() == outbox_bytes
        assert session.outbox.read() == outbox_state
        assert world.daemon.service.get_project_timeline(
            fixture.project_id, fixture.timeline_id,
        ) == before_head
        assert world.daemon.service._timeline_commits()[0].revision_closure(
            fixture.project_id, fixture.timeline_id, fixture.parent_revision_id,
        ) == before_document
        assert tuple(world.daemon.service.store.conn.iterdump()) == before_rows
        assert read_object_from_realm(fixture.duplicate_root, malformed_id) == malformed
        after_cas = {
            path.relative_to(world.daemon.service.store.cas_root).as_posix(): path.read_bytes()
            for path in world.daemon.service.store.cas_root.rglob("*") if path.is_file()
        }
        assert after_cas == before_cas
    finally:
        world.stop()
    assert readonly_tree_digest(fixture.source_root) == before_source
