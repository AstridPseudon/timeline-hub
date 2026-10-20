"""Native sheet CLI keeps the original export in the existing scoped outbox."""
from __future__ import annotations

import hashlib
import json

import pytest

from astrid.packs.timeline import cli
from astrid.sdk import storage_root
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.outbox import request_bytes
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk.test_timeline_sheet_native import edit_cell
from tests.sdk.test_timeline_sync import connected, initial_bundle  # noqa: F401


@pytest.fixture
def native_cli(connected, monkeypatch):  # noqa: F811
    client, generated, path = connected
    monkeypatch.setattr(storage_root, "resolve_runtime_data_root", lambda: path.parent)
    scope = {"realm_id": "realm", "actor_id": "actor", "project_id": "p", "timeline_id": "t"}
    generated.path = path.parent / "timeline-outbox" / (hashlib.sha256(request_bytes(scope)).hexdigest() + ".json")

    def forbidden(*args, **kwargs):
        pytest.fail("legacy checkout/write called")

    monkeypatch.setattr(Checkout, "__init__", forbidden)
    monkeypatch.setattr(Checkout, "save", forbidden)
    monkeypatch.setattr(cli, "_edit_checkout", forbidden)

    def run(*args):
        parsed = cli.build_parser(client).parse_args([*args, "--project", "p"])
        return parsed.handler(parsed)

    return run, client, generated


def export(native_cli, capsys):
    run, _, _ = native_cli
    assert run("show", "t", "--as", "sheet", "--native") == 0
    return capsys.readouterr().out


def test_export_preview_apply_and_undo(native_cli, tmp_path, capsys):
    run, _, generated = native_cli
    text = export(native_cli, capsys)
    state = json.loads(generated.path.read_bytes())
    assert state["sheet"] == {"bundle": initial_bundle(), "basis": generated.head}
    edited = edit_cell(text, "parent/clip:a", "5")
    edited = edit_cell(edited, "parent/track:picture", '"Picture"', label=True)
    path = tmp_path / "edited.txt"
    path.write_text(edited)
    before = generated.path.read_bytes()
    assert run("apply", "t", str(path), "--native", "--dry-run", "--json") == 0
    preview = json.loads(capsys.readouterr().out)
    assert len(preview["data"]["commands"]) == 2 and preview["receipt"] is None
    assert generated.calls == [] and generated.path.read_bytes() == before
    assert run("apply", "t", str(path), "--native", "--json") == 0
    output = json.loads(capsys.readouterr().out)
    assert output["data"]["accepted_publication_id"] == "pub1"
    body = json.loads(generated.calls[0][0])
    assert len(body["commands"]) == 2 and body["base_revision_id"] == "r0"
    assert body["base_publication_id"] == "pub0" and body["source"] == {"via": "sheet"}
    assert generated.bundles["r1"]["parent"]["clips"][0]["at"] == 5
    assert run("undo", "t", "--publication", "pub1", "--json") == 0
    capsys.readouterr()
    assert generated.bundles["r2"]["parent"] == initial_bundle()["parent"]
    assert path.read_text() == edited


@pytest.mark.parametrize("relevant", [False, True])
def test_stale_export_refuses_without_recapturing(native_cli, tmp_path, capsys, relevant):
    run, client, generated = native_cli
    text = export(native_cli, capsys)
    original = json.loads(generated.path.read_bytes())["sheet"]
    path = tmp_path / "edited.txt"
    path.write_text(edit_cell(text, "parent/clip:a", "5"))
    generated.bundles["peer"] = execute(initial_bundle(), [capture_move(
        initial_bundle(), "parent/clip:a" if relevant else "parent/clip:b", 7)]).bundle
    generated.head = {"revision_id": "peer", "publication_id": "peer-pub"}
    reads = list(client.reads)
    assert run("apply", "t", str(path), "--native", "--json") == 1
    output = json.loads(capsys.readouterr().out)
    assert "original project, timeline and basis" in output["error"]["message"]
    assert "edited sheet kept" in output["error"]["message"]
    assert generated.calls == [] and client.reads == reads
    assert json.loads(generated.path.read_bytes())["sheet"] == original
    assert path.read_text() == edit_cell(text, "parent/clip:a", "5")


def test_lost_ack_immutable_retry_and_pending_export_refusal(native_cli, tmp_path, capsys, monkeypatch):
    run, _, generated = native_cli
    text = export(native_cli, capsys)
    path = tmp_path / "edited.txt"
    edited = edit_cell(text, "parent/clip:a", "5")
    path.write_text(edited)
    args = ("apply", "t", str(path), "--native", "--json")
    generated.lose_ack = True
    assert run(*args, "--idempotency-key", "sheet-once") == 1
    capsys.readouterr()
    before = generated.path.read_bytes()
    assert run("show", "t", "--as", "sheet", "--native", "--json") == 1
    assert "pending intent" in capsys.readouterr().out
    assert generated.path.read_bytes() == before
    assert run(*args, "--idempotency-key", "different") == 1
    assert "immutable" in capsys.readouterr().out
    path.write_text(edit_cell(text, "parent/clip:a", "6"))
    assert run(*args) == 1
    assert "pending intent" in capsys.readouterr().out
    assert generated.path.read_bytes() == before and len(generated.calls) == 1
    path.write_text(edited)

    def forbidden(*args, **kwargs):
        pytest.fail("retry fetched a bundle")

    monkeypatch.setattr(TimelineSession, "_bundle", forbidden)
    assert run(*args) == 0
    capsys.readouterr()
    assert generated.calls[0] == generated.calls[1]
    assert len(generated.accepted) == 1 and path.read_text() == edited


@pytest.mark.parametrize("change", [
    lambda text: text.replace("  type", "  other", 1),
    lambda text: text.replace('"parent/clip:a"', '"parent/clip:b"', 1),
    lambda text: text.replace('"publication_id": "pub0"', '"publication_id": "other"'),
])
def test_unsupported_edits_leave_text_and_outbox_intact(native_cli, tmp_path, capsys, change):
    run, _, generated = native_cli
    text = change(export(native_cli, capsys))
    path = tmp_path / "edited.txt"
    path.write_text(text)
    before = generated.path.read_bytes()
    assert run("apply", "t", str(path), "--native", "--json") == 1
    assert "edited sheet kept" in capsys.readouterr().out
    assert generated.path.read_bytes() == before and generated.calls == []
    assert path.read_text() == text


@pytest.mark.parametrize("identity", ["realm_id", "actor_id"])
def test_export_artifact_is_scoped_to_connection(native_cli, tmp_path, capsys, identity):
    run, client, generated = native_cli
    text = export(native_cli, capsys)
    path = tmp_path / "edited.txt"
    path.write_text(edit_cell(text, "parent/clip:a", "5"))
    original = generated.path.read_bytes()
    client._remote._transport._last_handshake[identity] = "other"
    assert run("apply", "t", str(path), "--native", "--json") == 1
    assert "no original native sheet export" in capsys.readouterr().out
    assert generated.path.read_bytes() == original and generated.calls == []


@pytest.mark.parametrize("options", [
    ("--as", "sheet", "--range", "0..2"),
    ("--as", "sheet", "--clip", "a"),
    ("--as", "sheet", "--draft", "main"),
    ("--as", "sheet", "--revision-id", "r0"),
    (),
])
def test_native_export_rejects_incompatible_views(native_cli, capsys, options):
    run, _, generated = native_cli
    assert run("show", "t", "--native", "--json", *options) == 1
    assert not json.loads(capsys.readouterr().out)["ok"]
    assert not generated.path.exists() and generated.calls == []


def test_unchanged_export_has_no_commit(native_cli, tmp_path, capsys):
    run, _, generated = native_cli
    path = tmp_path / "edited.txt"
    path.write_text(export(native_cli, capsys))
    assert run("apply", "t", str(path), "--native", "--json") == 0
    output = json.loads(capsys.readouterr().out)
    assert output["data"] == {"status": "unchanged", "commands": []}
    assert output["receipt"] is None and generated.calls == []


@pytest.mark.parametrize("changed", ["pending", "bundle"])
def test_original_identity_never_coerces_boolean_to_number(native_cli, tmp_path, capsys, changed):
    run, _, generated = native_cli
    generated.bundles["r0"]["parent"]["clips"][0]["opaque"] = 1
    text = export(native_cli, capsys)
    path = tmp_path / "edited.txt"
    path.write_text(edit_cell(text, "parent/clip:a", "1"))
    state = json.loads(generated.path.read_bytes())
    if changed == "pending":
        command = capture_move(generated.bundles["r0"], "parent/clip:a", 1)
        command["args"]["on"] = True
        state["pending"] = [command]
    else:
        state["sheet"]["bundle"]["parent"]["clips"][0]["opaque"] = True
    generated.path.write_bytes(request_bytes(state))
    before = generated.path.read_bytes()
    assert run("apply", "t", str(path), "--native", "--json") == 1
    assert "edited sheet kept" in capsys.readouterr().out
    assert generated.path.read_bytes() == before and generated.calls == []
