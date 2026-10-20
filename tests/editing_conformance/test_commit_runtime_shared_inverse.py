"""Exact shared-source inverses through the real Runtime commit provider."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from tests.editing_conformance.test_commit_runtime_identity import occurrence_image
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.fixture(params=[3, 1], ids=["original-third", "authored-first"])
def shared_editing(request, tmp_path, monkeypatch):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / "tests"))
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from test_timeline_commit_integration import Editing
    from timeline_commit_film_fixture import build_film_fixture

    from astrid.sdk.timeline.capture import capture_move
    from astrid.sdk.timeline.commit import bundle_from_document

    fixture = build_film_fixture(tmp_path)
    service = RuntimeService(fixture.duplicate_root)
    edit = Editing(service, SimpleNamespace(fixture=fixture),
                   SimpleNamespace(move=capture_move, bundle=bundle_from_document))
    try:
        original = edit.document()
        parent = copy.deepcopy(original["parent_revision"]["payload"])
        index = request.param
        children = {}
        if index == 1:
            _, shot, internal = copy.deepcopy(occurrence_image(original, "occurrence-1"))
            shot.update(revision_id="authored-shot", internal_timeline_revision_id="authored-internal")
            shot["payload"].update(unknown={"literal": [None, False, 0, {}, []]}, items=[{
                "item_id": "shared-source-item", "media_id": fixture.media_ids[0],
                "metadata": {"literal": "shared-source-item", "keep": [None, False]},
            }])
            internal["revision_id"] = "authored-internal"
            internal["payload"].update(source_window={"start": 4, "end": 9},
                                       unknown={"literal": [None, False, 0, {}, []]})
            internal["payload"]["clips"][0]["extension"] = {"literal": "shared-source-item", "clear": None}
            for image in (shot, internal):
                image.pop("content_digest")
            parent["occurrences"][0]["shot_revision_id"] = shot["revision_id"]
            for ordinal, occurrence in enumerate(parent["occurrences"][1:]):
                occurrence["placement"]["start_ms"] = 8000 + ordinal * 2000
            parent["unknown"] = {"literal": [None, False, 0, {}, []]}
            children = {"shot_revisions": [shot], "internal_timeline_revisions": [internal]}
        repeated = copy.deepcopy(parent["occurrences"][index - 1])
        repeated.update(occurrence_id="repeated-third",
                        placement={"start_ms": 13000 if index == 1 else 6000, "track": "picture"})
        parent["occurrences"].append(repeated)
        service.publish_parent_composition(edit.project, edit.timeline, {
            "project_id": edit.project, "timeline_id": edit.timeline,
            "expected_head": fixture.parent_revision_id,
            "parent_revision_id": "shared-inverse-baseline", "parent_composition": parent, **children,
        }, idempotency_key="shared-inverse-baseline")

        def unavailable(*args, **kwargs):
            raise AssertionError("save evaluated a scene")

        import runtime_protocol.service as service_module
        import runtime_protocol.visual_seam as visual_seam
        monkeypatch.setattr(service_module, "evaluate_closure", unavailable)
        monkeypatch.setattr(visual_seam, "evaluate_closure", unavailable)
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        yield edit, index
    finally:
        edit.service.close()


def test_shared_slot_move_inverse_redo_and_rematerialization(shared_editing):
    from test_timeline_commit_integration import inverse

    edit, index = shared_editing
    original = edit.document()
    baseline_history = copy.deepcopy(edit.history())
    baseline_closures = [edit.document(entry["revision_id"]) for entry in baseline_history]
    transcript = edit.service.get_document(edit.project, edit.film.fixture.transcript_document_id)
    binding = edit.service.get_project_shot_text_binding(edit.project, edit.film.fixture.text_binding_id)
    owner = f"occurrence:occurrence-{index}/clip:clip-{index}"
    move = edit.agent.move(edit.agent.bundle(original), owner, 3.5)
    first = edit.commit(edit.body([move]), "shared-first-move")
    edit.assert_readback(first)
    undone = edit.commit(edit.body([inverse(first["receipt"]["receipt_id"])]), "shared-undo")
    assert undone["data"]["canonical_document"] == original
    redone = edit.commit(edit.body([inverse(undone["receipt"]["receipt_id"])]), "shared-redo")
    assert redone["data"]["canonical_document"] == first["data"]["canonical_document"]
    undone_again = edit.commit(edit.body([inverse(redone["receipt"]["receipt_id"])]), "shared-undo-again")
    assert undone_again["data"]["canonical_document"] == original
    move = edit.agent.move(edit.agent.bundle(edit.document()), owner, 3.6)
    rematerialized = edit.commit(edit.body([move]), "shared-rematerialize")
    assert {s["shot_id"] for s in rematerialized["data"]["canonical_document"]["shot_revisions"]} == {
        s["shot_id"] for s in first["data"]["canonical_document"]["shot_revisions"]}
    for accepted in (first, undone, redone, undone_again, rematerialized):
        edit.assert_readback(accepted)
        for sibling in [*(f"occurrence-{n}" for n in range(1, 4) if n != index), "repeated-third"]:
            assert occurrence_image(accepted["data"]["canonical_document"], sibling) == occurrence_image(original, sibling)
    history = edit.history()
    assert history[:len(baseline_history)] == baseline_history
    assert [edit.document(entry["revision_id"]) for entry in baseline_history] == baseline_closures
    accepted_results = (first, undone, redone, undone_again, rematerialized)
    assert len(history) == len(baseline_history) + len(accepted_results)
    for entry, accepted in zip(history[len(baseline_history):], accepted_results):
        assert entry["receipt"] == accepted["receipt"]
        assert entry["revision_id"] == accepted["data"]["accepted_revision_id"]
        assert edit.document(entry["revision_id"]) == accepted["data"]["canonical_document"]
    assert edit.service.get_document(edit.project, edit.film.fixture.transcript_document_id) == transcript
    assert edit.service.get_project_shot_text_binding(edit.project, edit.film.fixture.text_binding_id) == binding


def test_shared_inverse_preserves_newer_disjoint_parent_edit(shared_editing):
    from test_timeline_commit_integration import inverse

    edit, index = shared_editing
    original = edit.document()
    owner = f"occurrence:occurrence-{index}/clip:clip-{index}"
    moved = edit.commit(edit.body([edit.agent.move(edit.agent.bundle(original), owner, 3.5)]), "shared-move")
    parent_move = edit.agent.move(edit.agent.bundle(edit.document()), "parent/clip:music-bed", 1)
    disjoint = edit.commit(edit.body([parent_move]), "disjoint-parent-move")
    before = copy.deepcopy(edit.history())
    undone = edit.commit(edit.body([inverse(moved["receipt"]["receipt_id"])]), "shared-disjoint-undo")
    document = undone["data"]["canonical_document"]
    expected_parent = copy.deepcopy(disjoint["data"]["canonical_document"]["parent_revision"]["payload"])
    expected_parent["occurrences"] = original["parent_revision"]["payload"]["occurrences"]
    assert document["parent_revision"]["payload"] == expected_parent
    for key in ("shot_revisions", "internal_timeline_revisions", "dependency_manifest"):
        assert document[key] == original[key]
    assert edit.history()[:-1] == before
    for accepted in (moved, disjoint, undone):
        edit.assert_readback(accepted)
