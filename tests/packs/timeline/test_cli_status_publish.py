from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline import cli as timeline_cli
from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.timeline import store as timeline_store
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk.test_timeline_commit_provider import runtime_abi  # noqa: F401
from tests.sdk.test_timeline_public_command import public_session  # noqa: F401


def _json_result(capsys):
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def normal_commit(public_session, tmp_path):  # noqa: F811 - imported fixture
    """Run the normal timeline CLI commit against the public fixture closure."""
    opened, realm, sent, client, _ = public_session
    document = copy.deepcopy(realm.documents[realm.head["revision_id"]])
    candidate = bundle_from_document(document)
    candidate["base_parent"]["publication_id"] = realm.head["publication_id"]
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    parser = timeline_cli.build_parser(client)

    def run(*args, message="Timeline edit", as_json=True):
        argv = ["commit", "film", "--project", "project-1", "--file", str(path), "-m", message, *args]
        if as_json:
            argv.append("--json")
        parsed = parser.parse_args(argv)
        return parsed.handler(parsed)

    return run, path, realm, sent, opened, client


def test_status_absent_draft_reports_head_without_creating(tmp_path, monkeypatch, capsys) -> None:
    client = object()
    parser = timeline_cli.build_parser(client)
    path = tmp_path / "absent.json"
    monkeypatch.setattr(timeline_store, "resolve_ids", lambda *_args, **_kwargs: ("p1", "t1", "head-2"))
    monkeypatch.setattr(timeline_store, "current_draft", lambda *_args: "main")
    monkeypatch.setattr(timeline_store, "draft_path", lambda *_args: path)
    monkeypatch.setattr(Checkout, "load", classmethod(lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("must not load an absent draft"))))

    parsed = parser.parse_args(["status", "main", "--project", "p1"])

    assert parsed.handler(parsed) == 0
    payload = _json_result(capsys)
    assert payload["ok"] is True
    assert payload["data"] == {
        "timeline_id": "t1",
        "current_head": "head-2",
        "draft": "main",
        "working_copy": "absent",
    }
    assert not path.exists()


def test_status_existing_draft_reports_base_head_changes_and_check(tmp_path, monkeypatch, capsys) -> None:
    client = object()
    parser = timeline_cli.build_parser(client)
    path = tmp_path / "draft.json"
    path.write_text("present", encoding="utf-8")
    monkeypatch.setattr(timeline_store, "resolve_ids", lambda *_args, **_kwargs: ("p1", "t1", "head-3"))
    monkeypatch.setattr(timeline_store, "current_draft", lambda *_args: "working")
    monkeypatch.setattr(timeline_store, "draft_path", lambda *_args: path)

    class Report:
        valid = False
        problems = ("missing media",)
        changed_cuts = ("c2",)

    class FakeCheckout:
        base_revision = "head-1"

        def changes(self):
            return ["cut c2 changed"]

        def edits(self):
            return {
                "changes": [{"kind": "changed", "clip_id": "c2", "fields": ["app"]}],
                "placement_changes": [],
                "cut_points": {"moved": [], "added": [], "removed": []},
            }

        def check(self):
            return Report()

    monkeypatch.setattr(Checkout, "load", classmethod(lambda *_args, **_kwargs: FakeCheckout()))
    monkeypatch.setattr(
        timeline_cli,
        "_checkout_change_units",
        lambda _checkout: (True, [["clip", "s1", "c2"]]),
    )
    parsed = parser.parse_args(["status", "main", "--project", "p1"])

    assert parsed.handler(parsed) == 0
    payload = _json_result(capsys)
    assert payload["ok"] is True
    assert payload["data"] == {
        "timeline_id": "t1",
        "current_head": "head-3",
        "draft": "working",
        "working_copy": "present",
        "base_revision": "head-1",
        "head_moved": True,
        "changed": True,
        "change_state": "changed",
        "changed_units": [["clip", "s1", "c2"]],
        "changes": ["cut c2 changed"],
        "change_details": [{"kind": "changed", "clip_id": "c2", "fields": ["app"]}],
        "placement_changes": [],
        "cut_points": {"moved": [], "added": [], "removed": []},
        "check": {"valid": False, "problems": ["missing media"], "changed_cuts": ["c2"]},
    }


def test_checkout_fresh_keeps_dirty_draft_and_allows_named_fresh(tmp_path, monkeypatch, capsys) -> None:
    parser = timeline_cli.build_parser(object())
    dirty = tmp_path / "main.json"
    dirty.write_text("keep me", encoding="utf-8")
    monkeypatch.setattr(timeline_store, "resolve_ids", lambda *_args, **_kwargs: ("p1", "t1", "head-2"))
    monkeypatch.setattr(timeline_store, "current_draft", lambda *_args: "main")
    monkeypatch.setattr(timeline_store, "draft_path", lambda _p, _t, name: dirty if name == "main" else tmp_path / f"{name}.json")

    class DirtyCheckout:
        base_revision = "head-1"

        @staticmethod
        def load(_path):
            return DirtyCheckout()

        def changes(self):
            # Structured changes catch narration/app edits even if the
            # human-facing clip summary has no line to display.
            return []

        def edits(self):
            return {
                "changes": [{"kind": "changed", "clip_id": "vo-1", "fields": ["app"]}],
                "placement_changes": [],
                "cut_points": {"moved": [], "added": [], "removed": []},
            }

    calls = []
    monkeypatch.setattr(Checkout, "load", classmethod(lambda _cls, _path: DirtyCheckout()))
    monkeypatch.setattr(
        timeline_cli,
        "_checkout_change_units",
        lambda _checkout: (True, [["clip", "s1", "vo-1"]]),
    )
    monkeypatch.setattr(Checkout, "draft", classmethod(lambda _cls, *args, **kwargs: calls.append((args, kwargs)) or object()))

    refused = parser.parse_args(["checkout", "main", "--project", "p1", "--fresh"])
    assert refused.handler(refused) == 1
    payload = _json_result(capsys)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "conflict"
    assert dirty.read_text(encoding="utf-8") == "keep me"
    assert calls == []

    fresh = parser.parse_args(["checkout", "main", "--project", "p1", "--draft", "recovered", "--fresh"])
    assert fresh.handler(fresh) == 0
    assert calls == [(("p1", "main"), {"name": "recovered", "client": fresh.client, "fresh": True})]
    assert dirty.read_text(encoding="utf-8") == "keep me"


def test_checkout_fresh_refuses_parent_config_edit_when_clip_diff_is_empty(tmp_path, monkeypatch, capsys) -> None:
    from tests.packs.timeline.test_edit_verbs import bundle as editing_bundle

    parser = timeline_cli.build_parser(object())
    draft = tmp_path / "main.json"
    source = editing_bundle()
    Checkout._pin_initial_base(source)
    working = Checkout(source)
    working.bundle["parent"]["config"]["chapters"] = [{"id": "intro", "title": "Intro"}]
    draft.write_text(json.dumps(working.document(), sort_keys=True), encoding="utf-8")
    original_bytes = draft.read_bytes()
    previous = Checkout.load(draft)

    # The ordinary clip/cut diff omits this edited parent config unit.
    assert previous.edits()["changes"] == []
    assert previous.edits()["placement_changes"] == []
    base_known, changed_units = timeline_cli._checkout_change_units(previous)
    assert base_known is True
    assert any(path[-1] == "chapters" for path in changed_units)

    monkeypatch.setattr(timeline_store, "resolve_ids", lambda *_args, **_kwargs: ("p1", "t1", "head-2"))
    monkeypatch.setattr(timeline_store, "current_draft", lambda *_args: "main")
    monkeypatch.setattr(timeline_store, "draft_path", lambda *_args: draft)
    calls = []
    monkeypatch.setattr(Checkout, "draft", classmethod(lambda _cls, *args, **kwargs: calls.append((args, kwargs)) or object()))

    parsed = parser.parse_args(["checkout", "main", "--project", "p1", "--fresh"])
    assert parsed.handler(parsed) == 1
    payload = _json_result(capsys)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "conflict"
    details = payload["error"]["details"]
    assert details["change_state"] == "changed"
    assert any(path[-1] == "chapters" for path in details["changed_units"])
    assert draft.read_bytes() == original_bytes
    assert calls == []


def test_normal_commit_forwards_key_through_the_authenticated_closure(normal_commit, capsys) -> None:
    run, path, realm, sent, _, _ = normal_commit
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Committed Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert run("--idempotency-key", "edit-42", message="Committed Film") == 0
    payload = _json_result(capsys)
    assert payload["ok"] is True
    assert payload["data"]["status"] == "accepted"
    assert payload["receipt"]["idempotency_key"] == "edit-42"
    assert sent[-1]["base_revision_id"] == realm.entries[0]["revision_id"]
    assert sent[-1]["base_publication_id"] == "bootstrap"
    assert realm.entries[-1]["receipt"]["idempotency_key"] == "edit-42"
    assert sent[-1]["label"] == "Committed Film"


@pytest.mark.parametrize("as_json", [False, True])
def test_normal_commit_partial_publication_error_preserves_receipt_and_does_not_retry(
    normal_commit, monkeypatch, capsys, as_json,
) -> None:
    run, path, realm, _, _, client = normal_commit
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Partial Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    receipt = {
        "old_head": "head-1",
        "new_head": "head-2",
        "narration_pinned": [],
        "narration_error": "binding CAS conflict",
    }
    calls = []
    original = client.timelines._typed

    def refusal(operation, *args, **kwargs):
        if operation == "commit_timeline":
            calls.append((args, kwargs))
            return DomainResult.failure(
                ErrorObject("partial_publication", "binding CAS conflict", {"receipt": receipt}),
                idempotency_key=kwargs["idempotency_key"],
            )
        return original(operation, *args, **kwargs)

    monkeypatch.setattr(client.timelines, "_typed", refusal)
    assert run("--idempotency-key", "edit-43", message="Partial Film", as_json=as_json) == 1
    captured = capsys.readouterr()
    if as_json:
        payload = json.loads(captured.out)
        assert payload["ok"] is False
        assert payload["error"]["code"] == "partial_publication"
        assert payload["error"]["details"]["receipt"] == receipt
        assert payload["idempotency_key"] == "edit-43"
    else:
        assert captured.out == ""
        assert "error partial_publication:" in captured.err
    assert calls and len(calls) == 1
    assert len(realm.entries) == 1


@pytest.mark.parametrize("as_json", [False, True])
def test_normal_commit_retry_reuses_the_same_receipt_without_a_second_write(normal_commit, capsys, as_json) -> None:
    run, path, realm, _, _, _ = normal_commit
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Retryable Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    key = "edit-43-json" if as_json else "edit-43"
    assert run("--idempotency-key", key, as_json=as_json) == 0
    first = capsys.readouterr()
    assert len(realm.entries) == 2
    assert run("--idempotency-key", key, as_json=as_json) == 0
    second = capsys.readouterr()
    if as_json:
        assert json.loads(second.out) == json.loads(first.out)
    else:
        assert second.out == first.out
    assert len(realm.entries) == 2




def test_normal_commit_output_keeps_summary_and_receipt(normal_commit, capsys) -> None:
    run, path, realm, sent, _, _ = normal_commit
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Summary Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    assert run("--idempotency-key", "edit-44", message="Summary Film", as_json=False) == 0
    output = capsys.readouterr().out
    assert "accepted revision" in output
    assert len(output) < 1000 and "canonical_document" not in output
    assert sent[-1]["label"] == "Summary Film"
    assert realm.entries[-1]["receipt"]["idempotency_key"] == "edit-44"


@pytest.mark.parametrize("as_json", [False, True])
def test_normal_commit_cas_refusal_preserves_file_and_does_not_retry(normal_commit, capsys, as_json) -> None:
    from tests.sdk.test_timeline_public_command import rename

    run, path, realm, _, opened, _ = normal_commit
    candidate = json.loads(path.read_text(encoding="utf-8"))
    candidate["parent"]["name"] = "Local Film"
    path.write_text(json.dumps(candidate), encoding="utf-8")
    before = path.read_bytes()
    opened.command(rename(value="Peer Film"), reads=[])
    opened.commit("Peer edit", reads=[])
    capsys.readouterr()

    key = "cas-key-json" if as_json else "cas-key"
    assert run("--idempotency-key", key, as_json=as_json) == 1
    captured = capsys.readouterr()
    if as_json:
        payload = json.loads(captured.out)
        assert payload["ok"] is False
        assert payload["error"]["code"] == "conflict"
    else:
        assert captured.out == ""
        assert "error conflict:" in captured.err
    assert path.read_bytes() == before
    assert len(realm.entries) == 2


def test_normal_commit_of_a_clean_working_copy_writes_nothing(normal_commit, capsys) -> None:
    run, path, realm, _, _, _ = normal_commit
    before = path.read_bytes()
    assert run("--idempotency-key", "clean-key") == 0
    payload = _json_result(capsys)
    assert payload["ok"] is True
    assert payload["receipt"] is None
    assert len(realm.entries) == 1
    assert path.read_bytes() == before


def test_list_follows_every_cursor_page(monkeypatch, capsys) -> None:
    from astrid.sdk.contracts import DomainResult

    pages = {
        None: [[{"timeline_id": "film", "archived": False, "version": 1}], "c1"],
        "c1": [[], "c2"],
        "c2": [[{"timeline_id": "trial-a", "archived": False, "version": 1}], None],
    }

    class FakeTimelines:
        def list(self, _project, *, cursor=None, include_archived=False):
            return DomainResult.success(pages[cursor])

    class FakeClient:
        timelines = FakeTimelines()

    parser = timeline_cli.build_parser(object())
    parsed = parser.parse_args(["list", "--project", "p1", "--json"])
    parsed.client = FakeClient()

    assert parsed.handler(parsed) == 0
    payload = _json_result(capsys)
    assert [row["timeline_id"] for row in payload["data"][0]] == ["film", "trial-a"]
    assert payload["data"][1] is None


def test_checkout_and_status_hints_use_the_existing_document_commit(tmp_path, monkeypatch, capsys):
    from types import SimpleNamespace

    from astrid.packs.timeline.cli_common import checkout_summary, status_text

    path = tmp_path / "working copy.json"
    local = SimpleNamespace(
        path=path, base_revision="head-1", _cut_groups=lambda: ["cut"],
        cut_count=lambda: "1 cut", clips=lambda: [], words=lambda: [],
        changes=lambda: ["name changed"], edits=lambda: {"changes": []},
        check=lambda: SimpleNamespace(valid=True, brief=lambda **_kwargs: ["valid"]),
    )
    parsed = timeline_cli.build_parser(object()).parse_args([
        "status", "main", "--project", "p1", "--draft", "working", "--text",
    ])
    summary = "\n".join(checkout_summary(parsed, local, existed=True))
    monkeypatch.setattr(Checkout, "load", classmethod(lambda *_args: local))
    assert status_text(parsed, "p1", "t1", "head-2", "working", path) == 0
    output = summary + capsys.readouterr().out
    expected = timeline_cli._document_edit_commands(str(path))["commit"]
    assert output.count(expected) == 2
    assert "timelines publish" not in output and "three-way" not in output
