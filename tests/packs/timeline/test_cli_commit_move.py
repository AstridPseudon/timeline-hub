"""The real product parser/dispatch emits the SDK's captured move and inverse."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from astrid.packs.timeline import cli
from astrid.sdk import storage_root
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.outbox import request_bytes
from tests.sdk.test_timeline_sync import connected as sync_connection  # noqa: F401
from tests.sdk.test_timeline_sync import initial_bundle


def _install_history(generated):
    """Expose accepted fake responses through the authenticated public history shape."""
    bootstrap = copy.deepcopy(generated.head)
    generated.bundles[bootstrap["revision_id"]]["base_parent"]["publication_id"] = bootstrap["publication_id"]

    def list_timeline_commits(project, timeline, *, cursor=None, limit):
        assert (project, timeline) == ("p", "t")
        items = [{
            "publication_id": bootstrap["publication_id"], "revision_id": bootstrap["revision_id"],
            "previous": None, "receipt": {"receipt_id": bootstrap["publication_id"]},
            "intent": "bootstrap", "records": None,
            "provider_version": None, "compiler_version": None, "publisher": None,
        }]
        for _raw, response in generated.accepted.values():
            data, receipt = response["data"], response["receipt"]
            body = next(json.loads(raw) for raw, key in generated.calls
                        if key == receipt["idempotency_key"])
            label = data.get("label", body.get("label", "Timeline edit"))
            steps = copy.deepcopy(data.get("steps", body.get("steps", [])))
            merge_mode = data.get("merge_mode", body.get("merge", "fields"))
            records = generated.records[receipt["receipt_id"]]
            generated.bundles[data["accepted_revision_id"]]["base_parent"].update(
                revision_id=data["accepted_revision_id"], publication_id=receipt["receipt_id"])
            if not isinstance(records, dict):
                records = {"commands": copy.deepcopy(records)}
            else:
                records = copy.deepcopy(records)
            records.setdefault("commands", copy.deepcopy(generated.records[receipt["receipt_id"]]))
            records.update(label=copy.deepcopy(label), steps=copy.deepcopy(steps), merge_mode=merge_mode)
            command = body.get("commands", [{}])[0]
            if command.get("op") == "timeline.inverse":
                records.setdefault("undo_of", copy.deepcopy(command.get("args", {}).get("publications", [])))
                if "steps" in command.get("args", {}):
                    records.setdefault("undo_steps", copy.deepcopy(command["args"]["steps"]))
            history_data = copy.deepcopy(data)
            history_data.update(label=copy.deepcopy(label), steps=copy.deepcopy(steps), merge_mode=merge_mode)
            history_receipt = copy.deepcopy(receipt)
            history_receipt["result"] = copy.deepcopy(history_data)
            items.append({
                "publication_id": receipt["receipt_id"], "revision_id": history_data["accepted_revision_id"],
                "previous": {"revision_id": data["previous_revision_id"],
                             "publication_id": data["previous_publication_id"]},
                "receipt": history_receipt, "intent": "recorded", "records": records,
                "provider_version": history_data["provider_version"],
                "compiler_version": history_data["compiler_version"],
                "publisher": history_data["publisher"], "source": history_data.get("source"),
                "label": label, "steps": copy.deepcopy(steps), "merge_mode": merge_mode,
            })
        return {"head": copy.deepcopy(generated.head), "items": items, "next_cursor": None}

    generated.list_timeline_commits = list_timeline_commits


@pytest.fixture
def command(sync_connection, monkeypatch):  # noqa: F811 - imported pytest fixture
    client, generated, path = sync_connection
    _install_history(generated)
    monkeypatch.setattr(storage_root, "resolve_runtime_data_root", lambda: path.parent)
    scope = {"realm_id": "realm", "actor_id": "actor", "project_id": "p", "timeline_id": "t"}
    generated.path = path.parent / "timeline-outbox" / (hashlib.sha256(request_bytes(scope)).hexdigest() + ".json")
    monkeypatch.setattr(cli, "_edit_checkout", lambda *a, **kw: pytest.fail("legacy draft editor called"))
    parser = cli.build_parser(client)

    def run(*args):
        parsed = parser.parse_args(args)
        return parsed.handler(parsed)

    return run, generated


def test_move_dispatch_matches_python_capture_and_reports_immutable_revision(command, capsys):
    run, generated = command
    assert run("edit", "timeline-slug", "--project", "project-slug", "--clip", "parent/clip:a", "--on", "5", "--json") == 0
    body = json.loads(generated.calls[0][0])
    assert body["commands"] == [capture_move(initial_bundle(), "parent/clip:a", 5)]
    assert body["source"] == {"via": "cli"}
    output = json.loads(capsys.readouterr().out)
    assert output["data"]["accepted_revision_id"] == "r1"
    assert output["data"]["accepted_publication_id"] == "pub1"
    assert output["data"]["show_command"] == "astrid timelines show t --project p --published --revision-id r1"
    assert output["receipt"]["receipt_id"] == "pub1"


def test_ordinary_edit_literal_move_uses_commit_outbox(command, capsys):
    run, generated = command
    assert run("edit", "t", "--clip", "a", "--on", "5", "--json") == 0
    body = json.loads(generated.calls[0][0])
    assert body["commands"] == [capture_move(initial_bundle(), "parent/clip:a", 5.0)]
    assert body["source"] == {"via": "cli"}
    output = json.loads(capsys.readouterr().out)
    assert output["data"]["accepted_publication_id"] == "pub1"


def test_ordinary_edit_literal_move_retries_the_persisted_flight(command, capsys):
    run, generated = command
    args = ("edit", "t", "--clip", "a", "--on", "5", "--json", "--idempotency-key", "ordinary-move")
    generated.lose_ack = True
    assert run(*args) == 1
    capsys.readouterr()
    assert run(*args) == 0
    capsys.readouterr()
    assert generated.calls[0] == generated.calls[1]


def test_ordinary_edit_symbolic_move_keeps_legacy_moment_resolution(command, monkeypatch):
    run, generated = command

    def legacy(*args, **kwargs):
        raise RuntimeError("legacy moment resolution")

    monkeypatch.setattr(cli, "_edit_checkout", legacy)
    with pytest.raises(RuntimeError, match="legacy moment resolution"):
        run("edit", "t", "--clip", "a", "--on", 'after "Astrid"')
    assert generated.calls == []


def test_ordinary_edit_occurrence_move_keeps_legacy_owner_resolution(command, monkeypatch):
    run, generated = command
    from tests.editing_conformance.test_recipe_m2_clip_trim import bundle as trim_bundle

    generated.bundles['r0'] = trim_bundle()
    generated.bundles['r0']['base_parent'].update(revision_id='r0', publication_id='pub0')

    def legacy(*args, **kwargs):
        raise RuntimeError("legacy occurrence resolution")

    monkeypatch.setattr(cli, "_edit_checkout", legacy)
    with pytest.raises(RuntimeError, match="legacy occurrence resolution"):
        run("edit", "t", "--clip", "occurrence:occ-b/clip:clip-a", "--on", "5")
    assert generated.calls == []


def test_ordinary_edit_move_with_draft_keeps_legacy_draft(command, monkeypatch):
    from astrid.sdk.timeline import store
    from astrid.sdk.timeline.sync import TimelineSession

    run, generated = command
    monkeypatch.setattr(store, "find_draft", lambda *args, **kwargs: generated.path)
    monkeypatch.setattr(TimelineSession, "open",
                        lambda *args, **kwargs: pytest.fail("draft opened through native session"))

    def legacy(*args, **kwargs):
        raise RuntimeError("legacy draft resolution")

    monkeypatch.setattr(cli, "_edit_checkout", legacy)
    with pytest.raises(RuntimeError, match="legacy draft resolution"):
        run("edit", "t", "--clip", "a", "--on", "5")
    assert generated.calls == []


@pytest.mark.parametrize("extra", [("--trim-out", "4"), ("--set", "x=2"), ("--verify",)])
def test_ordinary_edit_move_with_unsupported_flags_keeps_legacy(command, monkeypatch, extra):
    run, generated = command

    def legacy(*args, **kwargs):
        raise RuntimeError("legacy mixed move")

    monkeypatch.setattr(cli, "_edit_checkout", legacy)
    with pytest.raises(RuntimeError, match="legacy mixed move"):
        run("edit", "t", "--clip", "a", "--on", "5", *extra)
    assert generated.calls == []


def test_move_preview_uses_current_project_and_does_not_claim_publication(command, capsys):
    run, generated = command
    assert run("edit", "t", "--clip", "parent/clip:a", "--on", "5", "--dry-run") == 0
    assert capsys.readouterr().out.strip() == "preview only; no publication accepted"
    assert generated.accepted == {}
    assert generated.head["revision_id"] == "r0"


def test_cli_lost_ack_retry_and_accepted_undo(command, capsys):
    run, generated = command
    args = ("edit", "t", "--project", "p", "--clip", "parent/clip:a", "--on", "5", "--json")
    generated.lose_ack = True
    assert run(*args) == 1
    assert not json.loads(capsys.readouterr().out)["ok"]
    assert run(*args) == 0
    capsys.readouterr()
    assert generated.calls[0] == generated.calls[1]
    assert run("undo", "t", "--project", "p", "--commit", "pub1", "--json") == 0
    output = json.loads(capsys.readouterr().out)
    assert output["data"]["accepted_publication_id"] == "pub2"
    inverse = json.loads(generated.calls[-1][0])["commands"][0]
    assert inverse["op"] == "timeline.inverse" and inverse["args"]["publications"] == ["pub1"]
    assert generated.bundles["r2"]["parent"] == initial_bundle()["parent"]


def test_edit_parser_refuses_retired_native_flag(command):
    run, generated = command
    with pytest.raises(SystemExit) as exc:
        run("edit", "t", "--project", "p", "--clip", "parent/clip:a", "--on", "5", "--native")
    assert exc.value.code == 2
    assert generated.calls == []


def test_preview_json_preserves_actual_bridge_request_key(command, capsys):
    run, generated = command
    assert run("edit", "t", "--clip", "parent/clip:a", "--on", "5", "--dry-run", "--json") == 0
    output = json.loads(capsys.readouterr().out)
    assert output["idempotency_key"] == generated.calls[0][1]
    assert output["idempotency_key"] and output["receipt"] is None


def test_cli_accepted_redo_inverts_undo_publication_and_preserves_disjoint_edit(command, capsys):
    run, generated = command
    for clip, on in [('a', '5'), ('b', '7')]:
        assert run('edit', 't', '--clip', 'parent/clip:' + clip, '--on', on, '--json') == 0
        capsys.readouterr()
    assert run('undo', 't', '--commit', 'pub1', '--json') == 0
    capsys.readouterr()
    assert run('redo', 't', '--commit', 'pub3', '--json') == 0
    output = json.loads(capsys.readouterr().out)
    assert output['data']['accepted_publication_id'] == 'pub4'
    assert generated.bundles['r4']['parent'] == generated.bundles['r2']['parent']
    inverse = json.loads(generated.calls[-1][0])['commands'][0]
    assert inverse['op'] == 'timeline.inverse' and inverse['args']['publications'] == ['pub3']
