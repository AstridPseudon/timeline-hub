"""Implicit checkout checks must not launch a scene query or Node during save."""
import subprocess

import pytest

from astrid.core.timeline import scene_answers
from astrid.sdk import timeline_transcripts
from astrid.sdk.timeline import store
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk.test_coverage_empty_cut import _empty_cut_bundle


@pytest.fixture
def no_scene_or_process(monkeypatch, tmp_path):
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "data"))
    def forbidden(*args, **kwargs):
        pytest.fail("save attempted scene evaluation or a child process")

    monkeypatch.setattr(scene_answers, "host_frames_at", forbidden)
    monkeypatch.setattr(scene_answers, "frames_at", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)


def test_transaction_check_save_reload_and_undo_without_scene(no_scene_or_process):
    checkout = Checkout(_empty_cut_bundle())
    path = store.draft_path("p", "t", "scene-boundary")
    checkout.save(path, quiet=True)
    before = checkout.document()
    with checkout.edit("change background") as edit:
        checkout.clip("b-plate").set(fill="#123456")
    assert edit.report.valid
    assert any("EMPTY" in line and "c02" in line for line in edit.report.problems)
    loaded = Checkout.load(path)
    assert loaded.clip("b-plate").params["fill"] == "#123456"
    assert loaded.undo(1) == ["change background"]
    assert loaded.document() == before


def test_publish_keeps_actual_check_without_scene(no_scene_or_process, monkeypatch):
    checkout = Checkout(_empty_cut_bundle())
    published = []

    def publish(candidate, key, **kwargs):
        published.append((candidate, key))
        return {"new_head": "accepted"}

    monkeypatch.setattr(store, "publish_bundle", publish)
    monkeypatch.setattr(timeline_transcripts, "plan_narration_transcripts", lambda _: [])
    # This fixture changes the shots as well as the parent; narration IO is
    # separate from the real check preceding publication.
    monkeypatch.setattr(checkout, "_publish_narration", lambda *a, **k: {})
    checked = []
    check = checkout.check

    def observe_check():
        report = check()
        checked.append(report)
        return report

    monkeypatch.setattr(checkout, "check", observe_check)
    assert checkout.publish("background", idempotency_key="save-boundary")["new_head"] == "accepted"
    assert len(checked) == len(published) == 1
    assert checked[0].valid
    assert any("EMPTY" in line and "c02" in line for line in checked[0].problems)
    assert published[0][1] == "save-boundary"
