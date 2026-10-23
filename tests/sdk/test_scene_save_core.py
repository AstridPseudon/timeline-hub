"""Save keeps core validity under real renderer import and process-launch fences."""
from __future__ import annotations

import builtins
import copy
import os
import subprocess
import sys
from types import SimpleNamespace

import pytest

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline_checkout import Checkout, TimelineEditError
from tests.sdk import test_timeline_transaction as transactions
from tests.sdk.test_timeline_sync import bundle_connection

draft = transactions.draft
tiny = transactions.tiny


@pytest.fixture
def no_renderer(monkeypatch):
    original_import = builtins.__import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        names = [name, *(f"{name}.{item}" for item in fromlist or ())]
        if any(item.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                "astrid.sdk.authoring_bundle", "astrid.sdk.authoring_render_preview",
                                "composition", "remotion"))
               or item.endswith(".onscreen") or ".scene" in item for item in names):
            raise AssertionError("save imported renderer/scene: " + name)
        return original_import(name, globals, locals, fromlist, level)

    def forbidden(*args, **kwargs):
        raise AssertionError("save launched a process or evaluated diagnostics")

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)
    for method in ("check", "_on_screen", "lint", "_sprite_problems", "_text_overflow"):
        monkeypatch.setattr(Checkout, method, forbidden)


@pytest.fixture
def client_for(tmp_path, monkeypatch):
    from astrid.sdk.timeline_cuts import base_bundle

    def connect(checkout, writes):
        client, generated = bundle_connection(tmp_path, monkeypatch, base_bundle(checkout.document()))
        send = generated.commit_timeline

        def commit(*args, **kwargs):
            result = send(*args, **kwargs)
            writes.append(copy.deepcopy(result["data"]["canonical_document"]))
            return result

        generated.commit_timeline = commit
        return client

    return connect


def commit_checkout(checkout, client):
    from astrid.sdk.timeline_duplicate import _commit_bundle

    return _commit_bundle(checkout.bundle["project_id"], checkout.bundle["timeline_id"],
                          checkout.stored_document(), label="Save fixture", client=client,
                          idempotency_key="save-fixture")


@pytest.mark.parametrize("operation", ["core", "publish", "transaction", "dry-run"])
def test_real_save_paths_need_neither_scene_imports_nor_node(draft, no_renderer, operation, client_for):
    checkout = draft
    before = checkout.document()
    writes = []
    if operation in {"transaction", "dry-run"}:
        with checkout.edit("move", dry_run=operation == "dry-run", quiet=True) as tx:
            checkout.clip("c1.rocket").set(x=90)
        assert tx.report.valid and tx.report.lint == []
        if operation == "dry-run":
            assert checkout.document() == before
        else:
            assert Checkout.load(checkout.path).clip("c1.rocket").get("x") == 90
            checkout.undo()
            assert Checkout.load(checkout.path).document() == before
    else:
        checkout.clip("c1.rocket").set(x=90)
        report = checkout._check_core()
        assert report.valid and not report.blocking and report.lint == []
        if operation == "publish":
            # An in-memory candidate avoids a follow-up head read; the publisher/compiler are real.
            checkout.path = None
            receipt = commit_checkout(checkout, client_for(checkout, writes))
            assert receipt["new_head"] == "r1" and len(writes) == 1


@pytest.mark.parametrize("damage", ["schema", "reference", "type", "length", "outside", "shot-length", "orphan"])
def test_publish_still_refuses_core_invalidity_before_writing(no_renderer, damage, client_for):
    checkout = Checkout(tiny())
    if damage == "schema":
        checkout.bundle["schema_version"] = 999
    elif damage == "reference":
        checkout.clip("c1.rocket").data["asset"] = "missing-asset"
    elif damage == "type":
        checkout.clip("c1.rocket").data["params"]["scale"] = "large"
    elif damage == "length":
        card = checkout.clip("c2.card")
        intent.set_for(card.data, None)
        intent.set_cut(card.data, None)
        card.data["hold"] = 0
    elif damage == "shot-length":
        card = checkout.clip("c2.card")
        intent.set_for(card.data, 10)
        card.data["hold"] = 10
    else:
        intent.set_formula(checkout.clip("c1.rocket").data, "params.allAt",
                           {"moment": '"now"' if damage == "outside" else '"gone"', "as": "clip_frame"})
    writes = []
    report = checkout._check_core()
    assert not report.valid and report.problems
    with pytest.raises(TimelineEditError, match="not committing"):
        commit_checkout(checkout, client_for(checkout, writes))
    assert writes == []


def test_private_check_override_still_fences_publication(monkeypatch, client_for):
    checkout = Checkout(tiny())
    writes = []
    monkeypatch.setattr(Checkout, "_check_core", lambda self: SimpleNamespace(valid=False, problems=["guard refused"]))
    with pytest.raises(TimelineEditError, match="not committing: guard refused"):
        commit_checkout(checkout, client_for(checkout, writes))
    assert writes == []


def test_offcanvas_stays_explicitly_invalid_but_saves_and_publishes_exactly(tmp_path, request, client_for):
    # PLAN §§2.5/4.2: visual checks advise; only core validity blocks publication.
    draft = Checkout(tiny())
    draft.clip("c1.rocket").data["params"]["x"] = 10000
    explicit = draft.check()
    assert explicit.validation["valid"] and not explicit.valid
    assert len(explicit.blocking) == 1 and explicit.blocking[0].startswith("OFFCANVAS c1.rocket:")
    request.getfixturevalue("no_renderer")
    core = draft._check_core()
    assert core.valid and core.blocking == [] and core.lint == []
    draft.save(tmp_path / "draft.json", quiet=True)
    assert Checkout.load(draft.path).clip("c1.rocket").data["params"]["x"] == 10000
    writes = []
    receipt = commit_checkout(draft, client_for(draft, writes))
    assert receipt["new_head"] == "r1" and len(writes) == 1
    rocket = next(clip for row in writes[0]["internal_timeline_revisions"]
                  for clip in row["payload"]["clips"] if clip["id"] == "a-rocket")
    assert rocket["params"]["x"] == 10000
    assert draft.clip("c1.rocket").data["params"]["x"] == 10000


def test_duplicate_preflights_and_publication_are_core_only(monkeypatch, no_renderer, client_for):
    from astrid.sdk import timeline_duplicate as duplicate

    source, target = Checkout(tiny()), Checkout(tiny())
    source.clip("c1.rocket").data["params"]["x"] = 10000
    target.bundle["timeline_id"] = "copy"
    monkeypatch.setattr(Checkout, "open", classmethod(
        lambda cls, project, timeline, **kw: source if timeline == "t" else target))
    writes = []
    client = client_for(target, writes)
    client.timelines.create_empty = lambda **kw: SimpleNamespace(ok=True, data={"timeline_id": "copy"})
    client.timelines.archive = lambda *a: pytest.fail("core-valid duplicate was archived")
    result = duplicate.duplicate_timeline("p", "t", client=client)
    assert result["timeline_id"] == "copy" and result["new_head"] == "r2" and len(writes) == 2


def test_implicit_cli_edit_report_and_save_are_core_only(tmp_path, request):
    from astrid.packs.timeline import cli

    path = Checkout(tiny()).save(tmp_path / "draft.json", quiet=True)
    parsed = cli.build_parser(None).parse_args(["edit", "--file", str(path),
                                               "--clip", "c1.rocket", "--set", "x=90"])
    request.getfixturevalue("no_renderer")
    assert parsed.handler(parsed) == 0
    assert Checkout.load(path).clip("c1.rocket").get("x") == 90


def test_fresh_check_import_and_core_validation_do_not_import_renderer():
    script = '''
import sys
class Blocked:
    def find_spec(self, fullname, *args):
        if (fullname.startswith(('astrid.packs.rendering', 'astrid.core.rendering',
                                 'astrid.sdk.authoring_bundle', 'astrid.sdk.authoring_render_preview',
                                 'composition', 'remotion'))
                or fullname.endswith('.onscreen') or '.scene' in fullname):
            raise AssertionError('renderer dependency: ' + fullname)
sys.meta_path.insert(0, Blocked())
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk.test_timeline_transaction import tiny
assert Checkout(tiny())._check_core().valid
'''
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    assert result.returncode == 0, result.stderr
