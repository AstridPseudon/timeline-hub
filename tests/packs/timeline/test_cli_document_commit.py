from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline import cli as timeline_cli
from astrid.sdk.timeline.commit import bundle_from_document

pytest_plugins = (
    "tests.sdk.test_timeline_commit_provider",
    "tests.sdk.test_timeline_public_command",
)


def _document_file(tmp_path, realm):
    candidate = bundle_from_document(copy.deepcopy(realm.documents[realm.head["revision_id"]]))
    candidate["base_parent"]["publication_id"] = realm.head["publication_id"]
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    return path


def _run(client, path, *, message="Rename film", key="document-1", dry_run=False):
    args = [
        "commit", "film", "--project", "project-1", "--file", str(path),
        "--message", message, "--idempotency-key", key, "--json",
    ]
    if dry_run:
        args.append("--dry-run")
    parsed = timeline_cli.build_parser(client).parse_args(args)
    return parsed.handler(parsed)


def test_document_commit_uses_the_authenticated_commit_door(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Committed Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["data"]["status"] == "accepted"
    assert sent[-1]["label"] == "Rename film"
    assert output["receipt"]["idempotency_key"] == "document-1"
    assert sent[-1]["merge"] == "atomic"
    assert sent[-1]["label"] == "Rename film"
    assert sent[-1]["steps"][0]["reads"]
    assert path.with_suffix(".publication.json").exists() is False


def test_document_commit_retry_reuses_history_without_a_second_write(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Retryable Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="retry-document") == 0
    first = json.loads(capsys.readouterr().out)
    assert _run(client, path, key="retry-document") == 0
    second = json.loads(capsys.readouterr().out)
    assert second == first
    assert len(realm.entries) == 2
    assert len(sent) == 1  # the second call reads durable history, but does not recapture a write


def test_document_commit_preview_has_no_accepted_receipt(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Preview Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    before = path.read_bytes()

    assert _run(client, path, key="preview-document", dry_run=True) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["data"]["status"] == "preview"
    assert output["data"]["would_status"] == "accepted"
    assert output["receipt"] is None
    assert len(realm.entries) == 1
    assert sent[-1]["dry_run"] is True
    assert path.read_bytes() == before


def test_document_commit_requires_a_nonempty_message_and_key(public_session, tmp_path, capsys):
    _opened, realm, _sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    parser = timeline_cli.build_parser(client)

    empty = parser.parse_args([
        "commit", "film", "--project", "project-1", "--file", str(path),
        "-m", "", "--idempotency-key", "key", "--json",
    ])
    assert empty.handler(empty) == 1
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "validation_error"
    with pytest.raises(SystemExit):
        parser.parse_args([
            "commit", "film", "--project", "project-1", "--file", str(path),
            "-m", "label", "--json",
        ])


def test_document_commit_refuses_a_stale_base_pair(public_session, tmp_path, capsys):
    _opened, realm, _sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["base_parent"]["publication_id"] = "publication-stale"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="stale-document") == 1
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is False
    assert output["error"]["details"]["path"] == "/file"
    assert len(realm.entries) == 1


def test_document_commit_parser_uses_current_project_for_file_edits():
    class Projects:
        @staticmethod
        def current():
            from astrid.sdk.contracts import DomainResult

            return DomainResult.success({"project": {"project_id": "current-project"}})

    class Client:
        projects = Projects()

    parsed = timeline_cli.build_parser(Client()).parse_args([
        "commit", "film", "--file", "timeline.json", "-m", "label", "--idempotency-key", "key",
    ])
    assert parsed.project == "current-project"

    class NoCurrentProjects:
        @staticmethod
        def current():
            from astrid.sdk.contracts import DomainResult, ErrorObject

            return DomainResult.failure(ErrorObject("no-current-project", "none", {}))

    class NoCurrentClient:
        projects = NoCurrentProjects()

    with pytest.raises(SystemExit):
        timeline_cli.build_parser(NoCurrentClient()).parse_args([
            "commit", "film", "--file", "timeline.json", "-m", "label", "--idempotency-key", "key",
        ])
