from __future__ import annotations

import copy
import json
import uuid
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline import retry as retry_module
from astrid.sdk.timeline.sync import CommitConflict


BASE = {"revision_id": "r1", "publication_id": "p1"}
HEAD = {"revision_id": "r2", "publication_id": "p2"}


def _record():
    return {"id": "pc_saved", "state": "pending", "key": "recut", "label": "Recut",
            "origin": "list", "part": 0, "attempts": 2,
            "parts": [{"base": BASE, "commands": [{"op": "clip.move", "select": "clip:a",
                                                       "args": {"on": 4}}],
                       "commit_options": {"label": "Recut", "steps": [{"id": "s1"}],
                                          "merge": "fields"},
                       "group_id": "assembly-1",
                       "rationale": "Keep this edit", "imports": [{"object_id": "media-1"}],
                       "evaluation": None}],
            "failure": {"details": {"status": "conflict", "conflicts": []}},
            "head": HEAD, "closed_by": None}


class FakeSession:
    def __init__(self, path):
        self.outbox = SimpleNamespace(path=Path(path), locked=lambda: nullcontext(),
                                      read=lambda: self.state, write=lambda state: setattr(self, "state", state))
        self.identity = {"actor_id": "actor-1"}
        self.state = {"pending_changes": {"pc_saved": _record()}, "base": HEAD,
                      "pending": [], "flight": None}
        self.client = SimpleNamespace()
        self.project_id, self.timeline_id = "project", "timeline"
        self.submissions = []

    def _state(self):
        return self.state

    def submit(self, *args, **kwargs):
        self.submissions.append((args, kwargs))
        pending_id = kwargs.get("pending_id")
        if pending_id:
            from astrid.sdk.timeline.sync import _settle_pending

            record = self.state["pending_changes"][pending_id]
            _settle_pending(record, actor_id=self.identity["actor_id"],
                            publication_id="pub-accepted", how=kwargs["pending_how"],
                            base=HEAD)
        return {"status": "accepted", "receipt": {"receipt_id": "pub-accepted"}}


class FakeTimeline:
    def __init__(self, path):
        self.session = FakeSession(path)

    def _pending_records_with_paths(self, actors):
        return [(self.session.outbox.path, copy.deepcopy(record))
                for record in self.session.state["pending_changes"].values()]

    def _accepted(self, result):
        return result


def test_list_retry_previews_original_base_with_saved_options(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    calls = []

    def probe(session, request):
        calls.append(copy.deepcopy(request))
        return {"would_status": "merged", "evaluated_head": HEAD, "canonical_document": {}}

    monkeypatch.setattr(retry_module, "_probe", probe)
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": [{"ref": "parent/clip:a"}]})
    preview = retry_module.retry(timeline, "recut")

    assert preview["status"] == "preview"
    assert preview["next"] == "tl.commit(r)"
    assert calls == [{"base_revision_id": "r1", "base_publication_id": "p1",
                       "commands": [{"op": "clip.move", "select": "clip:a", "args": {"on": 4}}],
                       "label": "Recut", "steps": [{"id": "s1"}], "merge": "fields",
                       "group_id": "assembly-1", "reads": [], "rationale": "Keep this edit",
                       "imports": [{"object_id": "media-1"}], "source": {"via": "python"}}]


def test_commit_preview_submits_identical_base_and_closes_pending(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")

    result = retry_module.commit_preview(timeline, preview)

    assert result["status"] == "accepted"
    args, kwargs = timeline.session.submissions[0]
    assert args[0] == _record()["parts"][0]["commands"]
    assert kwargs["base"] == BASE
    assert kwargs["pending_id"] == "pc_saved"
    assert kwargs["pending_path"] == str(timeline.session.outbox.path)
    assert kwargs["pending_how"] == "retry"
    assert str(uuid.UUID(kwargs["idempotency_key"])) == kwargs["idempotency_key"]
    assert kwargs["logical_key"] == "recut"
    assert kwargs["group_id"] == "assembly-1"
    assert kwargs["rationale"] == "Keep this edit"
    assert kwargs["imports"] == [{"object_id": "media-1"}]


def test_commit_preview_uses_pending_id_as_default_group(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    record = timeline.session.state["pending_changes"]["pc_saved"]
    record["parts"][0].pop("group_id")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")

    retry_module.commit_preview(timeline, preview)

    assert timeline.session.submissions[0][1]["group_id"] == "pc_saved"


def test_retry_preserves_original_group_id_from_part(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    requests = []
    monkeypatch.setattr(retry_module, "_probe", lambda session, request: requests.append(request) or {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})

    preview = retry_module.retry(timeline, "pc_saved")
    retry_module.commit_preview(timeline, preview)

    assert requests[0]["group_id"] == "assembly-1"
    assert timeline.session.submissions[0][1]["group_id"] == "assembly-1"


def test_retry_returns_redrive_state_for_conflict(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "status": "conflict", "details": {"status": "conflict", "conflicts": []}})
    monkeypatch.setattr(retry_module.clash, "explain", lambda *args: {"receipts": []})

    result = retry_module.retry(timeline, "pc_saved")

    assert result["status"] == "re_derive"
    assert 'pending="pc_saved"' in result["summary"]
    assert "tl.commit(make_edit" in result["next"]


def test_function_retry_returns_commit_result_and_reuses_label_key(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    calls = []
    def function(working):
        return None

    committed = {"status": "accepted", "data": {"publication_id": "pub9"},
                 "receipt": {"receipt_id": "pub9"}}
    timeline.commit = lambda *args, **kwargs: calls.append((args, kwargs)) or committed
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, []))

    result = retry_module.retry(timeline, "pc_saved", fn=function)

    assert calls == [((function,), {"label": "Recut", "key": "recut", "pending": "pc_saved"})]
    assert result is committed


def test_function_record_probe_preserves_original_base_and_guards(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    part = timeline.session.state["pending_changes"]["pc_saved"]["parts"][0]
    part["commit_options"] = {
        "label": "Recut", "steps": [{"id": "s1", "reads": [
            {"kind": "scope", "ref": "timeline", "path": []}]}], "merge": "atomic"
    }
    request = retry_module._request(
        timeline.session.state["pending_changes"]["pc_saved"], part
    )
    captured = {}

    class Timelines:
        def commit(self, project, timeline_id, body, *, idempotency_key):
            captured.update(body)
            return SimpleNamespace(ok=True, as_dict=lambda: {
                "data": {"status": "preview", "would_status": "conflict"}})

    timeline.session.client.timelines = Timelines()
    retry_module._probe(timeline.session, request)

    assert captured["base_revision_id"] == BASE["revision_id"]
    assert captured["base_publication_id"] == BASE["publication_id"]
    assert captured["merge"] == "atomic"
    assert captured["steps"] == part["commit_options"]["steps"]
    assert "reads" not in captured

    part["rationale"] = None
    assert "rationale" not in retry_module._request(
        timeline.session.state["pending_changes"]["pc_saved"], part
    )


def test_probe_reads_conflict_preview_before_generated_dto_rejects_it(tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    captured = {}

    class Generated:
        @staticmethod
        def _json(payload):
            return json.loads(payload)

        @staticmethod
        def _request(method, path, *, body, headers):
            captured.update(method=method, path=path, body=json.loads(body), headers=headers)
            return 200, {}, json.dumps({"data": {
                "status": "preview", "would_status": "conflict", "conflicts": []
            }}).encode()

    timeline.session.client._remote = SimpleNamespace(
        _transport=SimpleNamespace(_generated=Generated)
    )
    part = timeline.session.state["pending_changes"]["pc_saved"]["parts"][0]
    result = retry_module._probe(
        timeline.session,
        retry_module._request(timeline.session.state["pending_changes"]["pc_saved"], part),
    )

    assert result["would_status"] == "conflict"
    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/projects/project/timelines/timeline/commit"


def test_atomic_probe_omits_unset_reads(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    record = timeline.session.state["pending_changes"]["pc_saved"]
    record["parts"][0]["commit_options"]["merge"] = "atomic"
    record["parts"][0]["commit_options"].pop("reads", None)
    calls = []

    class Client:
        class Timelines:
            def commit(self, project, timeline_id, body, *, idempotency_key):
                calls.append(body)
                return SimpleNamespace(ok=True, as_dict=lambda: {
                    "data": {"status": "refused", "message": "Runtime refusal"}})
        timelines = Timelines()
    timeline.session.client = Client()

    result = retry_module.retry(timeline, "pc_saved")

    assert "reads" not in calls[0]
    assert result["summary"] == "Runtime refusal"


def test_preview_rejects_stale_record_and_token(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    timeline.session.state["pending_changes"]["pc_saved"]["rev"] = 3

    with pytest.raises(ValueError, match="changed after this retry preview"):
        retry_module.commit_preview(timeline, preview)

    timeline.session.state["pending_changes"]["pc_saved"]["rev"] = preview["_retry_record_rev"]
    preview["data"]["retry"]["token"] = "stale"
    with pytest.raises(ValueError, match="token is stale or invalid"):
        retry_module.commit_preview(timeline, preview)


def test_preview_rejects_tampered_request(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    preview["_retry_request"]["commands"][0]["args"]["on"] = 999

    with pytest.raises(ValueError, match="matches its saved part"):
        retry_module.commit_preview(timeline, preview)


def test_commit_preview_adopts_successful_submit(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    accepted = {"status": "accepted", "receipt": {"receipt_id": "pub-accepted"}}
    timeline.session.submit = lambda *args, **kwargs: accepted
    adopted = []
    timeline._accepted = lambda result: adopted.append(result) or {"adopted": result}

    result = retry_module.commit_preview(timeline, preview)

    assert adopted == [accepted]
    assert result == {"adopted": accepted}


def test_preview_diff_uses_evaluated_head_and_canonical_document(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    captured = {}
    import astrid.sdk.timeline.commit as commit_module
    import astrid.sdk.timeline.emitter as emitter
    import astrid.sdk.timeline.store as store

    monkeypatch.setattr(store, "fetch_bundle", lambda *args, **kwargs: captured.update(kwargs) or "before")
    monkeypatch.setattr(commit_module, "bundle_from_document", lambda document: (captured.update(document=document) or "after"))
    monkeypatch.setattr(emitter, "_root_pairs", lambda before, after: [("parent", "old", "new")])
    monkeypatch.setattr(emitter, "_payload_for_emit", lambda ref, value: value)
    changes = []
    monkeypatch.setattr(emitter, "_diff", lambda *args: changes.append(args))

    diff = retry_module._preview_diff(timeline, {"canonical_document": {"revision": "candidate"}}, HEAD)

    assert captured["revision_id"] == HEAD["revision_id"]
    assert captured["publication_id"] == HEAD["publication_id"]
    assert captured["document"] == {"revision": "candidate"}
    assert diff == {"changes": []}
    assert changes[0][:4] == ("old", "new", "parent", ())


def test_group_id_conflict_means_this_actor_already_landed(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    timeline.session.submit = lambda *args, **kwargs: (_ for _ in ()).throw(
        CommitConflict({"details": {"status": "conflict"}}))
    entry = {"group_id": "pc_saved", "publication_id": "pub-retry", "revision_id": "r3",
             "publisher": "actor-2", "receipt": {"receipt_id": "receipt-retry"}}
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, [entry]))

    result = retry_module.commit_preview(timeline, preview)

    assert result["status"] == "landed"
    assert result["summary"].endswith("(by actor-2); pc_saved is closed. Nothing was sent.")


def test_commit_preview_resolves_history_landed_before_stale_record_check(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    timeline.session.state["pending_changes"]["pc_saved"]["rev"] = 99
    entry = {"group_id": "pc_saved", "publication_id": "pub-other", "revision_id": "r3",
             "publisher": "actor-2", "receipt": {"receipt_id": "receipt-other"}}
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, [entry]))

    result = retry_module.commit_preview(timeline, preview)

    assert result["status"] == "landed"
    assert timeline.session.submissions == []
    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert saved["state"] == "landed"
    assert saved["closed_by"]["actor_id"] == "actor-2"


def test_multi_part_history_does_not_close_whole_record(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    record = timeline.session.state["pending_changes"]["pc_saved"]
    record["parts"].append(copy.deepcopy(record["parts"][0]))
    entry = {"group_id": "pc_saved", "publication_id": "pub-part-1", "revision_id": "r3",
             "publisher": "actor-2", "receipt": {"receipt_id": "receipt-part-1"}}
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, [entry]))

    result = retry_module.retry(timeline, "pc_saved")

    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert result["status"] == "part_landed"
    assert saved["state"] == "pending"
    assert saved["part"] == 1
    assert saved["parts"][1]["base"] == {"revision_id": "r3", "publication_id": "pub-part-1"}
    assert saved["receipts"] == ["receipt-part-1"]


def test_multi_part_history_uses_current_part_order(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    record = timeline.session.state["pending_changes"]["pc_saved"]
    record["parts"].extend(copy.deepcopy(record["parts"][0]) for _ in range(2))
    record["part"] = 1
    record["receipts"] = ["receipt-part-0"]
    entries = [
        {"group_id": "pc_saved", "publication_id": "pub-part-0", "revision_id": "r2",
         "publisher": "actor-2", "receipt": {"receipt_id": "receipt-part-0"}},
        {"group_id": "pc_saved", "publication_id": "pub-part-1", "revision_id": "r3",
         "publisher": "actor-3", "receipt": {"receipt_id": "receipt-part-1"}},
    ]
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, entries))

    result = retry_module.retry(timeline, "pc_saved")

    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert result["status"] == "part_landed"
    assert saved["part"] == 2
    assert saved["parts"][2]["base"] == {"revision_id": "r3", "publication_id": "pub-part-1"}
    assert saved["receipts"] == ["receipt-part-0", "receipt-part-1"]


def test_close_ignores_stale_part_after_another_actor_advances_record(tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    saved = timeline.session.state["pending_changes"]["pc_saved"]
    saved["parts"].extend(copy.deepcopy(saved["parts"][0]) for _ in range(2))
    stale = copy.deepcopy(saved)
    saved["part"] = 1
    saved["receipts"] = ["receipt-part-0"]
    before = copy.deepcopy(saved)
    path = timeline.session.outbox.path

    duplicate = {"publication_id": "pub-part-0", "revision_id": "r3",
                 "publisher": "actor-2", "receipt": {"receipt_id": "receipt-part-0"}}
    retry_module._close(path, stale, timeline.session, duplicate, "retry")
    assert saved == before

    stale_history_entry = {"publication_id": "pub-stale", "revision_id": "r4",
                           "publisher": "actor-3", "receipt": {"receipt_id": "receipt-stale"}}
    retry_module._close(path, stale, timeline.session, stale_history_entry, "retry")
    assert saved == before


def test_multi_part_preview_ack_advances_without_closing(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    record = timeline.session.state["pending_changes"]["pc_saved"]
    record["parts"].append(copy.deepcopy(record["parts"][0]))
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")

    retry_module.commit_preview(timeline, preview)

    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert saved["state"] == "pending"
    assert saved["part"] == 1
    assert timeline.session.submissions[0][1]["pending_id"] == "pc_saved"


def test_commit_preview_accepts_records_without_saved_steps(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    timeline.session.state["pending_changes"]["pc_saved"]["parts"][0]["commit_options"].pop("steps")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})

    preview = retry_module.retry(timeline, "pc_saved")
    retry_module.commit_preview(timeline, preview)

    assert timeline.session.submissions[0][1]["steps"] == []


def test_unknown_outcome_is_not_converted_to_refusal(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module, "_probe", lambda *args: {
        "would_status": "accepted", "evaluated_head": HEAD, "canonical_document": {}})
    monkeypatch.setattr(retry_module, "_preview_diff", lambda *args: {"changes": []})
    preview = retry_module.retry(timeline, "pc_saved")
    timeline.session.submit = lambda *args, **kwargs: (_ for _ in ()).throw(TimeoutError("unknown"))

    with pytest.raises(TimeoutError, match="unknown"):
        retry_module.commit_preview(timeline, preview)


def test_retry_detects_prior_group_id_and_closes_cross_actor_record(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    entry = {"group_id": "pc_saved", "publication_id": "pub-retry", "revision_id": "r3",
             "publisher": "actor-2", "receipt": {"receipt_id": "receipt-retry"}}
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, [entry]))

    result = retry_module.retry(timeline, "pc_saved")

    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert result["status"] == "landed"
    assert saved["state"] == "landed"
    assert saved["closed_by"] == {"actor_id": "actor-2", "publication_id": "pub-retry", "how": "retry"}
    assert saved["receipts"] == ["receipt-retry"]
