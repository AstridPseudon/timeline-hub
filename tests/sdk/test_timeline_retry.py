from __future__ import annotations

import copy
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

from astrid.sdk.timeline import retry as retry_module


BASE = {"revision_id": "r1", "publication_id": "p1"}
HEAD = {"revision_id": "r2", "publication_id": "p2"}


def _record():
    return {"id": "pc_saved", "state": "pending", "key": "recut", "label": "Recut",
            "origin": "list", "part": 0, "attempts": 2,
            "parts": [{"base": BASE, "commands": [{"op": "clip.move", "select": "clip:a",
                                                       "args": {"on": 4}}],
                       "commit_options": {"label": "Recut", "steps": [{"id": "s1"}],
                                          "merge": "fields"},
                       "rationale": "Keep this edit", "evaluation": None}],
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
        return {"status": "accepted"}


class FakeTimeline:
    def __init__(self, path):
        self.session = FakeSession(path)

    def _pending_records_with_paths(self, actors):
        return [(self.session.outbox.path, copy.deepcopy(record))
                for record in self.session.state["pending_changes"].values()]


def test_list_retry_previews_original_base_with_saved_options(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    calls = []

    def probe(session, request, merge, reads):
        calls.append((copy.deepcopy(request), merge, copy.deepcopy(reads)))
        return {"would_status": "merged", "head": HEAD,
                "diff": [{"ref": "parent/clip:a", "path": ["at"]}]}

    monkeypatch.setattr(retry_module.clash, "_probe", probe)
    preview = retry_module.retry(timeline, "recut")

    assert preview["status"] == "preview"
    assert preview["next"] == "tl.commit(r)"
    assert calls == [({"base_revision_id": "r1", "base_publication_id": "p1",
                       "commands": [{"op": "clip.move", "select": "clip:a", "args": {"on": 4}}],
                       "label": "Recut", "steps": [{"id": "s1"}], "merge": "fields",
                       "reads": [], "rationale": "Keep this edit", "source": {"via": "python"}},
                      "fields", [])]


def test_commit_preview_submits_identical_base_and_closes_pending(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module.clash, "_probe", lambda *args: {
        "would_status": "accepted", "head": HEAD, "diff": []})
    preview = retry_module.retry(timeline, "pc_saved")

    result = retry_module.commit_preview(timeline, preview)

    assert result["status"] == "accepted"
    args, kwargs = timeline.session.submissions[0]
    assert args[0] == _record()["parts"][0]["commands"]
    assert kwargs["base"] == BASE
    assert kwargs["pending_id"] == "pc_saved"
    assert kwargs["pending_path"] == str(timeline.session.outbox.path)
    assert kwargs["pending_how"] == "retry"
    assert kwargs["idempotency_key"].startswith("timeline-retry-")


def test_retry_returns_redrive_state_for_conflict(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    monkeypatch.setattr(retry_module.clash, "_probe", lambda *args: {
        "status": "conflict", "details": {"status": "conflict", "conflicts": []}})
    monkeypatch.setattr(retry_module.clash, "explain", lambda *args: {"receipts": []})

    result = retry_module.retry(timeline, "pc_saved")

    assert result["status"] == "re_derive"
    assert 'pending="pc_saved"' in result["summary"]
    assert "tl.commit(make_edit" in result["next"]


def test_retry_detects_prior_group_id_and_closes_cross_actor_record(monkeypatch, tmp_path):
    timeline = FakeTimeline(tmp_path / "outbox.json")
    entry = {"group_id": "pc_saved", "publication_id": "pub-retry", "publisher": "actor-2"}
    monkeypatch.setattr(retry_module.clash, "_history", lambda *args: (HEAD, [entry]))

    result = retry_module.retry(timeline, "pc_saved")

    saved = timeline.session.state["pending_changes"]["pc_saved"]
    assert result["status"] == "landed"
    assert saved["state"] == "landed"
    assert saved["closed_by"] == {"actor_id": "actor-1", "publication_id": "pub-retry", "how": "retry"}
