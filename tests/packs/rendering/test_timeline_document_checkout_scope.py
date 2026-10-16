from __future__ import annotations

import copy
import importlib.util
import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.timeline.authoring_bundle import (
    AuthoringBundleError,
    decode_authoring_bundle_storage,
    encode_authoring_bundle_storage,
)
from tests.timeline.test_authoring_bundle import _chapter_bundle, _closure

SCRIPT = Path(__file__).resolve().parents[3] / "astrid/packs/rendering/docs/scripts/timeline_document.py"
SPEC = importlib.util.spec_from_file_location("timeline_document_checkout_scope", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TimelineReader:
    def __init__(self, result):
        self.result = result
        self.args = None

    def open_composition(self, project_id, timeline_ref):
        self.args = (project_id, timeline_ref)
        return SimpleNamespace(ok=True, data=self.result)


def test_checkout_scope_uses_canonical_inspection_and_pins_returned_id():
    timelines = TimelineReader(
        {
            "summary": {"head_revision_id": "parent-head"},
            "native_inspection": {
                "project_id": "project-id",
                "timeline_id": "timeline-id",
                "head_revision_id": "parent-head",
            },
        }
    )
    client = SimpleNamespace(timelines=timelines)

    timeline_id, inspection = MODULE.resolve_timeline_scope(client, "project-id", "timeline-slug")

    assert timelines.args == ("project-id", "timeline-slug")
    assert timeline_id == "timeline-id"
    assert inspection["summary"]["head_revision_id"] == "parent-head"


def test_checkout_scope_fails_closed_if_inspection_does_not_confirm_project():
    timelines = TimelineReader(
        {
            "summary": {"head_revision_id": "parent-head"},
            "native_inspection": {
                "project_id": "other-project",
                "timeline_id": "timeline-id",
                "head_revision_id": "parent-head",
            },
        }
    )
    client = SimpleNamespace(timelines=timelines)

    with pytest.raises(RuntimeError, match="requested project"):
        MODULE.resolve_timeline_scope(client, "project-id", "timeline-slug")


def spy_codec(monkeypatch, name):
    original = getattr(MODULE, name)
    calls = []

    def wrapped(value):
        calls.append(copy.deepcopy(value))
        return original(value)

    monkeypatch.setattr(MODULE, name, wrapped)
    return calls


def chapter_candidate():
    candidate = _chapter_bundle()
    # chapter_layout alone opts in; no second policy flag is required.
    candidate.pop("opt_in")
    return candidate


def assert_chapter_storage(storage, candidate):
    assert storage["format"] == "astrid.authoring-chapters/v1"
    assert storage["film"]["tracks"] == candidate["parent"]["config"]["tracks"]
    assert "tracks" not in storage["film"]["bundle"]["parent"]["config"]
    assert [chapter["layout"] for chapter in storage["chapters"]] == candidate["chapter_layout"]
    for chapter in storage["chapters"]:
        for placement in chapter["placements"]:
            shot_id = placement["shot_id"]
            stored = chapter["shots"][shot_id]["internal_timeline"]
            assert "tracks" not in stored
            assert stored["track_ids"] == [
                row["id"] for row in candidate["shots"][shot_id]["internal_timeline"]["tracks"]
            ]
    assert decode_authoring_bundle_storage(storage) == candidate


@pytest.mark.parametrize("explicit_layout", [False, True])
def test_checkout_candidate_save_uses_only_explicit_layout(tmp_path, monkeypatch, explicit_layout):
    parent, shots, internals = _closure(shared=True)
    expected = MODULE.open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=internals
    )
    if explicit_layout:
        # The current opener does not author a layout. Prove the save hook when
        # its producer explicitly supplies one, without adding a source contract.
        expected = chapter_candidate()
        monkeypatch.setattr(MODULE, "open_authoring_bundle", lambda *a, **kw: expected)
    client = SimpleNamespace(
        projects=SimpleNamespace(show=lambda project: SimpleNamespace(
            ok=True, data={"project_id": "project-1"}
        )),
        timelines=TimelineReader({
            "summary": {"head_revision_id": "parent-1"},
            "native_inspection": {
                "project_id": "project-1", "timeline_id": "main", "head_revision_id": "parent-1"
            },
        }),
    )
    monkeypatch.setattr(MODULE.AstridClient, "open_from_launcher", lambda **kw: nullcontext(client))
    reads = []

    def read_parent(*args):
        reads.append(args)
        return {"data": parent}

    monkeypatch.setattr(MODULE, "workspace", lambda: SimpleNamespace(
        get_project_parent_composition_revision=read_parent,
        get_project_shot_revision=lambda *args: {"data": shots[0]},
        get_project_timeline_revision=lambda *args: {"data": internals[0]},
    ))
    calls = spy_codec(monkeypatch, "encode_authoring_bundle_storage")
    path = tmp_path / "checkout.json"
    MODULE.checkout(SimpleNamespace(project="project-slug", timeline="timeline-slug", file=path))
    assert reads == [("project-1", "main", "parent-1")]
    if explicit_layout:
        assert calls == [expected]
        assert_chapter_storage(json.loads(path.read_text()), expected)
    else:
        assert calls == []
        assert path.read_text() == json.dumps(expected, indent=2) + "\n"
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        MODULE.checkout(SimpleNamespace(file=path))
    assert path.read_bytes() == original


@pytest.mark.parametrize("command", ["check", "publish", "bind-script"])
@pytest.mark.parametrize("representation", ["chapters", "flat", "flat-layout"])
def test_dispatch_loads_flat_and_chapter_candidates(
    tmp_path, monkeypatch, command, representation
):
    candidate = chapter_candidate()
    if representation == "flat":
        candidate.pop("chapter_layout")
    value = encode_authoring_bundle_storage(candidate) if representation == "chapters" else candidate
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(value))
    original = path.read_bytes()
    text = tmp_path / "narration.txt"
    text.write_text("Synthetic narration")
    shot_id = candidate["placements"][0]["shot_id"]
    pin = {"kind": "voiceover_script", "binding_id": "synthetic-binding"}
    bound = []

    def set_binding(project_id, **kwargs):
        assert project_id == candidate["project_id"]
        assert kwargs == {
            "shot_id": shot_id, "kind": "voiceover_script", "text": text.read_text(),
            "expected_head": 7, "idempotency_key": "synthetic-request",
        }
        bound.append(True)
        return SimpleNamespace(ok=True, data=pin)

    opened = []

    def open_composition(*args):
        opened.append(args)
        return SimpleNamespace(ok=True, data={"summary": {"head_revision_id": "parent-1"}})

    client = SimpleNamespace(
        timelines=SimpleNamespace(open_composition=open_composition),
        shots=SimpleNamespace(set_text_binding=set_binding),
    )
    monkeypatch.setattr(MODULE.AstridClient, "open_from_launcher", lambda **kw: nullcontext(client))
    monkeypatch.setattr(MODULE, "workspace", lambda: object())
    decoded = spy_codec(monkeypatch, "decode_authoring_bundle_storage")
    encoded = spy_codec(monkeypatch, "encode_authoring_bundle_storage")
    planned = []
    real_plan = MODULE.plan_authoring_media

    def plan(value, **kwargs):
        planned.append(copy.deepcopy(value))
        return real_plan(value, **kwargs)

    monkeypatch.setattr(MODULE, "plan_authoring_media", plan)
    published = []

    def publish(value, writer, **kwargs):
        assert value == candidate
        assert isinstance(writer, MODULE.Writer)
        assert kwargs == {"idempotency_key": "synthetic-request", "media_imports": []}
        published.append(copy.deepcopy(value))
        return {"publication": {"new_head": "saved"}, "update": "Saved", "summary": {}, "next_actions": []}

    monkeypatch.setattr(MODULE, "publish_authoring_candidate", publish)
    argv = [str(SCRIPT), command, "--file", str(path)]
    if command != "check":
        argv += ["--idempotency-key", "synthetic-request"]
    if command == "bind-script":
        argv += ["--shot", shot_id, "--text-file", str(text), "--expected-head", "7"]
    monkeypatch.setattr("sys.argv", argv)
    MODULE.main()
    assert decoded == ([value] if representation == "chapters" else [])
    admission = [candidate] if representation == "flat-layout" else []
    if command == "bind-script":
        assert bound == [True]
        expected = copy.deepcopy(candidate)
        expected["shots"][shot_id]["payload"].setdefault("text_bindings", []).append(pin)
        saved = json.loads(path.read_text())
        if representation != "flat":
            assert encoded == admission + [expected]
            assert_chapter_storage(saved, expected)
        else:
            assert encoded == []
            assert path.read_text() == json.dumps(expected, indent=2) + "\n"
        assert json.loads(path.with_suffix(".text-binding.json").read_text()) == pin
        assert planned == published == []
    else:
        assert planned == [candidate]
        assert path.read_bytes() == original
        assert json.loads(path.with_suffix(".check.json").read_text())["media_imports"] == []
        if command == "publish":
            assert published == [candidate]
            prepared = json.loads(path.with_suffix(".prepared.json").read_text())
            if representation != "flat":
                assert encoded == admission + [candidate]
                assert_chapter_storage(prepared, candidate)
            else:
                assert encoded == []
                assert prepared == candidate
            assert json.loads(path.with_suffix(".publication.json").read_text())["publication"] == {"new_head": "saved"}
        else:
            assert encoded == admission
            assert published == opened == []


@pytest.mark.parametrize("command", ["check", "publish", "bind-script"])
@pytest.mark.parametrize("fault", ["version", "conflict", "transform", "flat-layout", "flat-conflict"])
def test_storage_refuses_before_dispatch_side_effects(tmp_path, monkeypatch, command, fault):
    tmp_path = tmp_path / "documents"
    tmp_path.mkdir()
    candidate = chapter_candidate()
    storage = encode_authoring_bundle_storage(candidate)
    if fault == "flat-layout":
        storage = candidate
        storage["chapter_layout"] = None
    elif fault == "flat-conflict":
        storage = candidate
        next(iter(storage["shots"].values()))["internal_timeline"]["tracks"][0]["kind"] = "audio"
    elif fault == "version":
        storage["format"] = "astrid.authoring-chapters/v999"
    else:
        chapter = storage["chapters"][0]
        if fault == "conflict":
            internal = next(iter(chapter["shots"].values()))["internal_timeline"]
            internal.pop("track_ids")
            internal["tracks"] = copy.deepcopy(storage["film"]["tracks"])
            internal["tracks"][0]["kind"] = "audio"
        else:
            chapter["placements"][0]["transform"] = {"rotation": 45}
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(storage))
    # Existing artifacts must remain byte-identical, not just absent on failure.
    for suffix in (".check.json", ".prepared.json", ".publication.json", ".text-binding.json", ".imports.json"):
        path.with_suffix(suffix).write_text("existing artifact")
    before = {file.name: file.read_bytes() for file in tmp_path.iterdir()}

    def forbidden(*args, **kwargs):
        pytest.fail("invalid storage reached a side effect or flat preflight")

    monkeypatch.setattr(MODULE.AstridClient, "open_from_launcher", forbidden)
    for name in ("workspace", "dump", "plan_authoring_media", "publish_authoring_candidate"):
        monkeypatch.setattr(MODULE, name, forbidden)
    argv = [str(SCRIPT), command, "--file", str(path)]
    if command != "check":
        argv += ["--idempotency-key", "synthetic-request"]
    if command == "bind-script":
        argv += ["--shot", "unused", "--text-file", str(tmp_path / "absent.txt"), "--expected-head", "7"]
    monkeypatch.setattr("sys.argv", argv)
    with pytest.raises(AuthoringBundleError):
        MODULE.main()
    assert {file.name: file.read_bytes() for file in tmp_path.iterdir()} == before


@pytest.mark.parametrize("fault", ["layout", "conflict"])
def test_invalid_explicit_candidate_save_preserves_existing_file(tmp_path, fault):
    candidate = chapter_candidate()
    if fault == "layout":
        candidate["chapter_layout"] = None
    else:
        next(iter(candidate["shots"].values()))["internal_timeline"]["tracks"][0]["kind"] = "audio"
    before = copy.deepcopy(candidate)
    path = tmp_path / "candidate.json"
    path.write_text("existing candidate")
    with pytest.raises(AuthoringBundleError):
        MODULE.save_candidate(path, candidate)
    assert path.read_text() == "existing candidate"
    assert candidate == before
