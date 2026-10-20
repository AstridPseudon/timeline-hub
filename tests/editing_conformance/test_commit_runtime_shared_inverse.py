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


def test_shared_inverse_preserves_newer_disjoint_sibling_edit(shared_editing):
    from test_timeline_commit_integration import inverse

    edit, index = shared_editing
    original = edit.document()
    owner = f"occurrence:occurrence-{index}/clip:clip-{index}"
    moved = edit.commit(edit.body([edit.agent.move(edit.agent.bundle(original), owner, 3.5)]), "shared-move")
    sibling = f"occurrence:repeated-third/clip:clip-{index}"
    disjoint = edit.commit(edit.body([edit.agent.move(edit.agent.bundle(edit.document()), sibling, 14)]),
                           "disjoint-sibling-move")
    before = copy.deepcopy(edit.history())
    undone = edit.commit(edit.body([inverse(moved["receipt"]["receipt_id"])]), "shared-sibling-undo")
    document = undone["data"]["canonical_document"]
    assert occurrence_image(document, f"occurrence-{index}") == occurrence_image(original, f"occurrence-{index}")
    assert occurrence_image(document, "repeated-third") == occurrence_image(
        disjoint["data"]["canonical_document"], "repeated-third")
    assert edit.history()[:-1] == before
    for accepted in (moved, disjoint, undone):
        edit.assert_readback(accepted)


def test_shared_inverse_refuses_touching_aba_atomically(shared_editing):
    from runtime_protocol.errors import RuntimeErrorBase
    from test_timeline_commit_integration import inverse, rows

    edit, index = shared_editing
    owner = f"occurrence:occurrence-{index}/clip:clip-{index}"
    moved = edit.commit(edit.body([edit.agent.move(edit.agent.bundle(edit.document()), owner, 3.5)]), "shared-move")
    for ordinal, on in enumerate((4, 3.5)):
        edit.commit(edit.body([edit.agent.move(edit.agent.bundle(edit.document()), owner, on)]), f"aba-{ordinal}")
    document, history, stored = edit.document(), edit.history(), rows(edit.service)
    with pytest.raises(RuntimeErrorBase) as error:
        edit.commit(edit.body([inverse(moved["receipt"]["receipt_id"])]), "shared-aba-undo")
    assert error.value.details["reason"] == "intervening_write"
    assert edit.document() == document
    assert edit.history() == history
    assert rows(edit.service) == stored
