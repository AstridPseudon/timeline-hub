from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline import cli as timeline_cli
from astrid.sdk.contracts import DomainResult, ErrorObject
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


def _runtime_idempotency(client, monkeypatch, *, history_limits=None):
    """Model Runtime's exact-key replay at the existing authenticated port."""
    original = client.timelines._typed
    calls = []
    accepted = {}

    def typed(operation, project, *args, **kwargs):
        if operation != "commit_timeline":
            result = original(operation, project, *args, **kwargs)
            if operation == "list_timeline_commits" and history_limits is not None:
                history_limits.append(kwargs.get("limit"))
                if result.ok and isinstance(result.data, dict):
                    rows = result.data.get("items")
                    if isinstance(rows, list) and rows:
                        result.data["items"] = [copy.deepcopy(rows[0]) for _ in range(201)]
            return result
        key = kwargs["idempotency_key"]
        body = copy.deepcopy(args[1])
        fingerprint = json.dumps(body, sort_keys=True, separators=(",", ":"))
        calls.append(key)
        prior = accepted.get(key)
        if prior is not None:
            old_fingerprint, result = prior
            if old_fingerprint != fingerprint:
                return DomainResult.failure(
                    ErrorObject("idempotency_conflict", "idempotency key was reused for a different request", {
                        "status": "refused", "path": "/idempotency_key",
                    }),
                    idempotency_key=key,
                )
            return copy.deepcopy(result)
        result = original(operation, project, *args, **kwargs)
        if result.ok:
            accepted[key] = (fingerprint, copy.deepcopy(result))
        return result

    monkeypatch.setattr(client.timelines, "_typed", typed)
    return calls


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


def test_document_commit_retry_uses_runtime_idempotency_without_history_scan(
    public_session, tmp_path, capsys, monkeypatch,
):
    _opened, realm, sent, client, _outbox = public_session
    calls = _runtime_idempotency(client, monkeypatch)
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
    assert len(sent) == 1  # Runtime replay returns the original accepted result.
    assert calls == ["retry-document", "retry-document"]


def test_document_commit_retry_does_not_scan_a_long_history_page(
    public_session, tmp_path, capsys, monkeypatch,
):
    _opened, realm, sent, client, _outbox = public_session
    history_limits = []
    calls = _runtime_idempotency(client, monkeypatch, history_limits=history_limits)
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Long history retry"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="long-history") == 0
    capsys.readouterr()
    assert _run(client, path, key="long-history") == 0
    capsys.readouterr()
    assert len(realm.entries) == 2 and len(sent) == 1
    assert calls == ["long-history", "long-history"]
    assert history_limits and 200 not in history_limits


def test_document_commit_empty_key_refuses_before_outbox_flight(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)

    assert _run(client, path, key="   ") == 1
    output = json.loads(capsys.readouterr().out)
    assert output["error"]["code"] == "validation_error"
    assert sent == [] and len(realm.entries) == 1
    assert path.with_suffix(".outbox.json").exists() is False


def test_document_commit_clean_raw_empty_app_is_a_noop(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["config"]["app"] = {}
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="clean-empty-app") == 0
    output = json.loads(capsys.readouterr().out)
    assert output["data"]["status"] == "unchanged"
    assert output["receipt"] is None
    assert sent == [] and len(realm.entries) == 1


def test_document_commit_preserves_unknown_parent_app_data(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["config"]["app"] = {"vendor": {"keep": None, "order": ["a", "b"]}}
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="unknown-app") == 0
    json.loads(capsys.readouterr().out)
    document = realm.documents[realm.head["revision_id"]]
    assert document["parent_revision"]["payload"]["config"]["app"] == {
        "vendor": {"keep": None, "order": ["a", "b"]}
    }
    assert sent[-1]["label"] == "Rename film"


def test_document_commit_human_output_keeps_label_and_receipt(public_session, tmp_path, capsys):
    _opened, realm, sent, client, _outbox = public_session
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Human Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    parsed = timeline_cli.build_parser(client).parse_args([
        "commit", "film", "--project", "project-1", "--file", str(path),
        "-m", "Human Film", "--idempotency-key", "human-output",
    ])

    assert parsed.handler(parsed) == 0
    output = capsys.readouterr().out
    assert "accepted revision" in output and "Human Film" in output
    assert realm.entries[-1]["receipt"]["receipt_id"] in output
    assert "canonical_document" not in output and len(output) < 1000
    assert sent[-1]["label"] == "Human Film"


def test_document_commit_changed_body_with_same_key_is_runtime_refusal(
    public_session, tmp_path, capsys, monkeypatch,
):
    _opened, realm, sent, client, _outbox = public_session
    calls = _runtime_idempotency(client, monkeypatch)
    path = _document_file(tmp_path, realm)
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "First body"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert _run(client, path, key="same-key") == 0
    capsys.readouterr()
    candidate["parent"]["name"] = "Changed body"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    assert _run(client, path, key="same-key") == 1
    output = json.loads(capsys.readouterr().out)
    assert output["error"]["code"] == "idempotency_conflict"
    assert len(realm.entries) == 2 and len(sent) == 1
    assert calls == ["same-key", "same-key"]


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
