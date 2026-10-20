"""Product CLI native sheets through actual authenticated Runtime memory HTTP."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline import cli
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from tests.editing_conformance.test_sheet_runtime import (
    bundle,
    film,  # noqa: F401 - shared actual Runtime fixture and legacy/renderer tripwires
    gesture,
    history,
    readback,
    submit,
)
from tests.sdk.test_timeline_sheet_native import edit_cell

pytestmark = pytest.mark.integration


def run(film, *args):  # noqa: F811
    parsed = cli.build_parser(film.client).parse_args([*args, "--project", film.project])
    return parsed.handler(parsed)


def export(film, capsys):  # noqa: F811
    assert run(film, "show", film.timeline, "--as", "sheet", "--native") == 0
    text = capsys.readouterr().out
    session = TimelineSession.open(film.project, film.timeline, client=film.client)
    sheet = NativeSheet.load(session)
    assert sheet.text == text
    path = film.tmp / "sheet.txt"
    path.write_text(gesture(sheet))
    return session, sheet, path


def apply(film, path, *options):  # noqa: F811
    return run(film, "apply", film.timeline, str(path), "--native", "--json", *options)


def test_cli_native_batch_readback_and_undo(film, capsys):  # noqa: F811
    session, sheet, path = export(film, capsys)
    before, original = history(film), bundle(film)
    stored = session.outbox.path.read_bytes()
    assert apply(film, path, "--dry-run") == 0
    preview = json.loads(capsys.readouterr().out)
    assert preview["data"]["commands"] == sheet.preview(path.read_text()).commands
    assert preview["receipt"] is None
    assert session.outbox.path.read_bytes() == stored and history(film) == before
    assert apply(film, path, "--idempotency-key", "cli-sheet") == 0
    accepted = json.loads(capsys.readouterr().out)
    sent = json.loads(film.wire.commits()[-1]["body"])
    assert sent["commands"] == preview["data"]["commands"] and len(sent["commands"]) == 2
    assert sent["base_revision_id"] == before["head"]["revision_id"]
    assert sent["base_publication_id"] == before["head"]["publication_id"]
    assert len(history(film)["items"]) == len(before["items"]) + 1
    actual = readback(film, accepted)
    assert actual["parent"] == sheet.preview(path.read_text()).bundle["parent"]
    assert run(film, "undo", film.timeline, "--publication", accepted["receipt"]["receipt_id"], "--json") == 0
    undone = json.loads(capsys.readouterr().out)
    assert readback(film, undone)["parent"] == original["parent"]
    assert path.read_text() == gesture(sheet)


def test_cli_lost_ack_service_restart_exact_body_key_and_changed_payload_refusal(film, capsys, monkeypatch):  # noqa: F811
    session, sheet, path = export(film, capsys)
    film.wire.lose.add("cli-sheet-lost")
    assert apply(film, path, "--idempotency-key", "cli-sheet-lost") == 1
    assert "edited sheet kept" in capsys.readouterr().out
    first = copy.deepcopy(film.wire.commits()[-1])
    accepted_history, durable = history(film), session.outbox.path.read_bytes()
    film.wire.restart()
    film.client = film.connect()
    changed = json.loads(first["body"])
    changed["commands"][0]["args"]["on"] = 3
    refused = film.client.timelines.commit(film.project, film.timeline, changed,
                                           idempotency_key="cli-sheet-lost")
    assert not refused.ok and history(film) == accepted_history
    assert apply(film, path, "--idempotency-key", "different") == 1
    assert "immutable" in capsys.readouterr().out
    path.write_text(edit_cell(sheet.text, "parent/clip:a", "3"))
    assert apply(film, path) == 1
    assert "pending intent" in capsys.readouterr().out
    assert session.outbox.path.read_bytes() == durable
    path.write_text(gesture(sheet))

    def forbidden(*args, **kwargs):
        raise AssertionError("retry must not fetch a fresh bundle")

    with monkeypatch.context() as retry:
        retry.setattr(TimelineSession, "_bundle", forbidden)
        assert apply(film, path) == 0
    accepted = json.loads(capsys.readouterr().out)
    last = film.wire.commits()[-1]
    assert {key: last[key] for key in ("path", "body", "key", "response")} == {
        key: first[key] for key in ("path", "body", "key", "response")}
    assert accepted["receipt"] == first["response"]["receipt"]
    assert history(film) == accepted_history and path.read_text() == gesture(sheet)
    assert json.loads(session.outbox.path.read_bytes())["pending"] == []
    readback(film, accepted)


@pytest.mark.parametrize("relevant", [False, True])
def test_cli_stale_original_refuses_after_reload(film, capsys, monkeypatch, relevant):  # noqa: F811
    session, sheet, path = export(film, capsys)
    original = json.loads(session.outbox.path.read_bytes())["sheet"]
    submit(film, [capture_move(bundle(film), "parent/clip:a" if relevant else "parent/clip:b", 4)], "peer")
    film.wire.restart()
    film.client = film.connect()
    before, commits = history(film), len(film.wire.commits())

    def forbidden(*args, **kwargs):
        raise AssertionError("stale sheet must not recapture current guards")

    monkeypatch.setattr(TimelineSession, "_bundle", forbidden)
    assert apply(film, path) == 1
    error = json.loads(capsys.readouterr().out)["error"]
    assert "original project, timeline and basis" in error["message"]
    assert "edited sheet kept" in error["message"]
    assert len(film.wire.commits()) == commits and history(film) == before
    assert json.loads(session.outbox.path.read_bytes())["sheet"] == original
    assert path.read_text() == gesture(sheet)


@pytest.mark.parametrize("relevant", [False, True])
def test_cli_peer_between_open_and_commit_rebases_or_conflicts_atomically(film, capsys, monkeypatch, relevant):  # noqa: F811
    session, sheet, path = export(film, capsys)
    original, before = bundle(film), history(film)
    load = NativeSheet.load

    def race(cls, session):
        submit(film, [capture_move(original, "parent/clip:a" if relevant else "parent/clip:b", 4)], "peer")
        return load(session)

    monkeypatch.setattr(NativeSheet, "load", classmethod(race))
    assert apply(film, path) == (1 if relevant else 0)
    output = json.loads(capsys.readouterr().out)
    sent = json.loads(film.wire.commits()[-1]["body"])
    assert sent["base_revision_id"] == before["head"]["revision_id"]
    assert sent["base_publication_id"] == before["head"]["publication_id"]
    assert sent["commands"] == sheet.preview(path.read_text()).commands
    actual = bundle(film)
    if relevant:
        assert "edited sheet kept" in output["error"]["message"]
        assert State(actual).entity("parent/clip:a")["at"] == 4
        assert "label" not in State(actual).entity("parent/track:picture")
        durable = json.loads(session.outbox.path.read_bytes())
        assert durable["conflict"] and durable["flight"] is not None
        assert durable["pending"] == sent["commands"]
    else:
        assert output["data"]["status"] == "rebased"
        assert State(actual).entity("parent/clip:a")["at"] == 2
        assert State(actual).entity("parent/clip:b")["at"] == 4
        assert State(actual).entity("parent/track:picture")["label"] == "Picture"
    assert len(history(film)["items"]) == len(before["items"]) + (1 if relevant else 2)
    assert path.read_text() == gesture(sheet)


def test_cli_sheet_pending_suffix_requires_sdk_flush_of_exact_flight_first(film, capsys):  # noqa: F811
    session, sheet, path = export(film, capsys)
    film.wire.lose.add("cli-prefix")
    assert apply(film, path, "--idempotency-key", "cli-prefix") == 1
    capsys.readouterr()
    first = copy.deepcopy(film.wire.commits()[-1])
    session = TimelineSession.open(film.project, film.timeline, client=film.client)
    suffix = session.queue_move("parent/clip:b", 6)
    durable = session.outbox.path.read_bytes()
    assert apply(film, path) == 1
    assert "pending intent" in capsys.readouterr().out
    assert session.outbox.path.read_bytes() == durable
    session.flush()
    retried = film.wire.commits()[-1]
    assert (retried["path"], retried["body"], retried["key"]) == (first["path"], first["body"], first["key"])
    state = json.loads(session.outbox.path.read_bytes())
    assert state["pending"] == [suffix] and state["flight"] is None
    session.flush()
    suffix_body = json.loads(film.wire.commits()[-1]["body"])
    assert suffix_body["commands"] == [suffix]
    assert suffix_body["base_revision_id"] == first["response"]["data"]["accepted_revision_id"]
    assert suffix_body["base_publication_id"] == first["response"]["receipt"]["receipt_id"]
    assert State(bundle(film)).entity("parent/clip:b")["at"] == 6
    assert path.read_text() == gesture(sheet)
