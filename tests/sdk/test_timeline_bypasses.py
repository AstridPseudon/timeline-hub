"""Write/history/publication boundaries, using only disposable local fixtures."""
from __future__ import annotations

import copy
import json
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline import journal, store
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline._common import TimelineEditError

FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json"


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setenv("ASTRID_ACTOR", "agent:bypasses-test")
    return Checkout(json.loads(FIXTURE.read_text()))


@pytest.mark.parametrize("origin", ["memory", "save-as"])
def test_non_draft_first_save_keeps_pending_journal_and_undo(checkout, tmp_path, origin):
    # Current history retains cut-ID high-water marks across undo. Seed the
    # synthetic input so exact content restoration still compares like for like.
    from astrid.sdk.timeline.identity import retain_cut_reservations
    checkout = Checkout(retain_cut_reservations(checkout.document()))
    if origin == "save-as":
        checkout.save(tmp_path / "source.json", quiet=True)
    before = checkout.document()
    checkout.clip("c1.rocket").set(x=120)
    target = checkout.save(tmp_path / "local.json", quiet=True)
    records = checkout.log()
    assert len(records) == 1 and records[0].kind == "save"
    assert records[0].calls[0]["op"] == "clip.set"
    assert records[0].actor["id"] == "bypasses-test"
    reopened = Checkout.load(target)
    after = reopened.document()
    assert reopened.undo() and reopened.document() == before
    assert reopened.redo() and reopened.document() == after
    assert journal.verify(target.with_suffix(".json.journal.jsonl")) == []


def test_save_without_path_refuses_before_writing_cwd(checkout, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    checkout.clip("c1.rocket").set(x=120)
    entries = sorted(str(p) for p in tmp_path.rglob("*"))
    before = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    pending = copy.deepcopy((checkout.bundle, checkout._journal, checkout._pending_calls))
    with pytest.raises(TimelineEditError, match="path|draft"):
        checkout.save(quiet=True)
    assert {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before
    assert sorted(str(p) for p in tmp_path.rglob("*")) == entries
    assert (checkout.bundle, checkout._journal, checkout._pending_calls) == pending
    assert not (tmp_path / "timeline.checkout.json").exists()
    assert checkout.path is None and checkout._journal


@pytest.mark.parametrize("verb", ["undo", "redo"])
@pytest.mark.parametrize("guard", ["lock", "stale", "unsaved"])
def test_history_uses_lock_and_refuses_unmerged_state(checkout, tmp_path, monkeypatch, verb, guard):
    target = checkout.save(tmp_path / "local.json", quiet=True)
    checkout.clip("c1.rocket").set(x=120)
    checkout.save(quiet=True)
    checkout.clip("c1.rocket").set(x=180)
    checkout.save(quiet=True)
    checkout.undo()
    assert list(store._history_dir(target).glob("*.json"))
    assert list(store._redo_dir(target).glob("*.json"))
    held = []
    active = []
    original_lock = store._file_lock
    read_step = store._read_step

    @contextmanager
    def locked(path):
        with original_lock(path):
            held.append(path)
            active.append(path)
            try:
                yield
            finally:
                active.pop()

    def locked_read_step(path):
        if guard == "lock":
            assert active == [target], "history must be read while the checkout lock is held"
        return read_step(path)

    monkeypatch.setattr(store, "_file_lock", locked)
    monkeypatch.setattr(store, "_read_step", locked_read_step)
    if guard == "stale":
        other = Checkout.load(target)
        other.clip("c2.card").set(text="another writer")
        other.save(quiet=True)
    elif guard == "unsaved":
        checkout.clip("c2.card").set(text="pending")
    # Current publication undo consults its journal before the snapshot guard.
    # Materialize that existing read lock before comparing refusal bytes.
    from astrid.sdk.timeline.inverse import publications
    publications(checkout.bundle["project_id"], checkout.bundle["timeline_id"])
    held.clear()
    before = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    if guard == "lock":
        assert getattr(checkout, verb)()
    else:
        with pytest.raises(TimelineEditError, match="another writer|unsaved"):
            getattr(checkout, verb)()
        assert {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before
    assert held == [target]


@pytest.mark.parametrize("when", ["fresh", "loaded", "after-command", "before-command", "inside-edit", "inside-before-command", "inside-after-command"])
def test_save_digest_refuses_raw_bundle_mutation(checkout, tmp_path, when):
    target = tmp_path / "local.json"
    if when != "fresh":
        checkout.save(target, quiet=True)
        checkout = Checkout.load(target)
    if when == "after-command":
        checkout.clip("c1.rocket").set(x=120)
    before = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    with pytest.raises(TimelineEditError, match="outside.*runner|raw.*mutation|Compiler prefix evidence does not match"):
        if when.startswith("inside-"):
            with checkout.edit("raw", quiet=True):
                if when == "inside-after-command":
                    checkout.clip("c1.rocket").set(x=120)
                checkout.bundle["parent"]["bypass"] = True
                if when == "inside-before-command":
                    checkout.clip("c1.rocket").set(x=120)
        else:
            checkout.bundle["parent"]["bypass"] = True
            if when == "before-command":
                checkout.clip("c1.rocket").set(x=120)
            checkout.save(target, quiet=True, force=True)
    # Refusal may have an audit record, but never writes document/history.
    for path, data in before.items():
        if not path.endswith(".journal.jsonl"):
            assert Path(path).read_bytes() == data
    assert not list(store._history_dir(target).glob("*.json"))
    if when == "fresh":
        assert not target.exists()


@pytest.mark.parametrize("dry_run", [False, True])
def test_pathless_publish_keeps_typed_refusal_without_effects(checkout, tmp_path, monkeypatch, dry_run):
    from astrid.sdk import AstridClient
    from astrid.sdk.timeline.saved_intent import SavedIntentError

    def forbidden(*args, **kwargs):
        pytest.fail("pathless publication must refuse before opening a transport")

    monkeypatch.setattr(AstridClient, "open_from_launcher", forbidden)
    monkeypatch.setattr(store, "publish_bundle", forbidden)
    checkout.clip("c1.rocket").set(x=120)
    before = copy.deepcopy(checkout.__dict__)
    files = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    with pytest.raises(SavedIntentError, match="exact saved canonical draft path"):
        checkout.publish("disposable publication", dry_run=dry_run)
    assert checkout.document() == before["bundle"]
    assert checkout._journal == before["_journal"]
    assert checkout._pending_calls == before["_pending_calls"]
    assert checkout.path is None
    assert {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == files


def test_narration_binding_remains_saveable_with_digest_backstop(checkout, tmp_path, monkeypatch):
    target = checkout.save(tmp_path / "local.json", quiet=True)
    monkeypatch.setattr(checkout, "narration_changes", lambda: {"A": "disposable narration\n"})
    client = SimpleNamespace(shots=SimpleNamespace(set_text_binding=lambda *a, **kw:
        {"kind": "voiceover_script", "head": kw["expected_head"] + 1, "content_hash": "fixture"}))
    assert checkout.pin_narration(client, idempotency_key="fixture") == ["A"]
    checkout.save(quiet=True)
    reopened = Checkout.load(target)
    assert reopened.bundle["shots"]["A"]["payload"]["text_bindings"][0]["content_hash"] == "fixture"
    assert reopened.undo()


@pytest.mark.parametrize("dry_run", [False, True])
def test_runner_rollback_restores_pending_state_and_digest(checkout, tmp_path, dry_run):
    from astrid.sdk.timeline import commands
    target = checkout.save(tmp_path / "local.json", quiet=True)
    checkout.clip("c1.rocket").set(x=120)
    before = copy.deepcopy((checkout.bundle, checkout._journal, checkout._pending_calls))
    if dry_run:
        commands.run(checkout, {"op": "clip.set", "select": "c2.card", "args": {"text": "preview"}}, dry_run=True)
    else:
        with pytest.raises(TimelineEditError, match="zzbogus") as caught:
            with checkout.edit("typed refusal", quiet=True):
                checkout.clip("c2.card").set(text="rolled back")
                checkout.clip("c2.card").set(zzbogus=2)
        assert type(caught.value) is TimelineEditError
    assert (checkout.bundle, checkout._journal, checkout._pending_calls) == before
    checkout.save(quiet=True)
    assert Checkout.load(target).document() == checkout.document()
    assert checkout.undo() and checkout.redo()


def test_saved_publication_and_refresh_remain_editable(tmp_path, monkeypatch):
    from tests.sdk.test_timeline_agent_sync import SharedRuntime
    from tests.sdk.test_timeline_saved_publish import edit
    from astrid.core.timeline import scene_answers
    from astrid.sdk.timeline import saved_publish
    from astrid.sdk.timeline.saved_intent import read_saved_calls

    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(Checkout, "_native_outline_integrity", lambda *a: None)
    monkeypatch.setattr(scene_answers, "_client", lambda: SimpleNamespace(query_scene=lambda **kw: [
        dict(frame=f, coverage="COVERED", content="CONTENT", findings=[], layers=[]) for f in kw["frames"]]))
    runtime = SharedRuntime()
    client = runtime.facade()
    monkeypatch.setattr(store, "resolve_ids", lambda *a, **k: ("p", "t", runtime.current))
    monkeypatch.setattr(store, "fetch_bundle", lambda *a, **k: saved_publish._exact(
        client._transport, dict(project_id="p", timeline_id="t"), k.get("revision_id") or runtime.current))
    checkout = Checkout.draft("p", "t", "supported", client=client)
    edit(checkout, x=90)
    receipt = checkout.publish(client=client)
    assert receipt["status"] == "accepted" and receipt["local_state"] == "finalized"
    assert read_saved_calls(checkout) == ()
    edit(checkout, y=180)
    checkout.refresh(client=client)
    edit(checkout, x=120)
    assert checkout.undo() and checkout.redo()
    checkout.save(quiet=True)
    assert Checkout.load(checkout.path).document() == checkout.document()
