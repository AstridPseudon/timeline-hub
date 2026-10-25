"""D136 preserves the upstream two-integer FPS spelling through the provider."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline import _commit_timing_validation as timing_validation
from astrid.sdk.timeline._timing_evaluators import _fps as production_fps
from astrid.sdk.timeline.commit import _digest
from tests.sdk import test_timeline_commit_provider as provider
from tests.sdk.test_p1_doc_patch_provider import _service_call
from tests.sdk.test_timeline_commit_provider_document import document_fixture

runtime_abi = provider.runtime_abi


def _document_with_upstream_fps_list() -> dict:
    document = document_fixture(shared=False)
    parent = document["parent_revision"]
    parent["payload"]["config"]["theme_overrides"] = {
        "visual": {"canvas": {"fps": [30000, 1001]}}
    }
    parent["content_digest"] = _digest(parent["payload"])
    return document


def _controls(*, dry_run: bool) -> dict:
    return {
        "label": "Unrelated track edit",
        "merge": "fields",
        "reads": [],
        "dry_run": dry_run,
        "source": {"via": "python"},
        "rationale": "Preserve upstream FPS spelling",
        "group_id": "d136-fps",
        "steps": [{
            "id": "track",
            "label": "Unrelated track edit",
            "intent": "Add an unrelated track",
            "tags": ["d136"],
            "command_ordinals": [0],
            "patch": [],
            "reads": [],
        }],
    }


def _document_with_canvas(canvas) -> dict:
    document = document_fixture(shared=False)
    parent = document["parent_revision"]
    parent["payload"]["config"]["theme_overrides"] = {"visual": {"canvas": canvas}}
    parent["content_digest"] = _digest(parent["payload"])
    return document


@pytest.mark.parametrize("dry_run", [False, True])
def test_production_caller_accepts_and_retains_upstream_fps_list(dry_run):
    realm = provider.DetachedRealm(_document_with_upstream_fps_list())
    original = copy.deepcopy(realm.documents[realm.head["revision_id"]])

    result = _service_call(
        realm,
        [provider.track_create("d136-track")],
        controls=_controls(dry_run=dry_run),
    )

    assert result["data"]["status"] == ("preview" if dry_run else "accepted")
    if dry_run:
        assert result["data"]["would_status"] == "accepted"
        assert result["receipt"] is None
    else:
        assert result["receipt"]["result"] == result["data"]
    payload = result["data"]["canonical_document"]["parent_revision"]["payload"]
    assert payload["config"]["theme_overrides"] == original["parent_revision"]["payload"]["config"]["theme_overrides"]


@pytest.mark.parametrize("fps", [[30000], [30000, 0], {"numerator": 0, "denominator": 1001}])
def test_production_caller_keeps_invalid_typed_fps_refused(fps):
    document = document_fixture(shared=False)
    parent = document["parent_revision"]
    parent["payload"]["config"]["output"]["fps"] = fps
    parent["content_digest"] = _digest(parent["payload"])
    realm = provider.DetachedRealm(document)
    before = copy.deepcopy(realm.head)

    with pytest.raises(provider.CommitRejected) as raised:
        _service_call(
            realm,
            [provider.track_create("d136-invalid-fps")],
            controls=_controls(dry_run=False),
        )

    assert raised.value.failure["http_status"] == 422
    assert raised.value.failure["details"]["status"] == "invalid"
    assert realm.head == before
    assert realm.prepared == []
    assert realm.accepted == []


@pytest.mark.parametrize(
    ("label", "canvas", "effective_fps"),
    [
        ("canvas-null", None, 30),
        ("canvas-bool", True, 30),
        ("canvas-string", "canvas", 30),
        ("canvas-list", [], 30),
        ("fps-null", {"fps": None}, 30),
        ("fps-true", {"fps": True}, 1),
        ("fps-false", {"fps": False}, 30),
        ("fps-string", {"fps": "30"}, 30),
        ("fps-mapping", {"fps": {"arbitrary": 1}}, 30),
        ("fps-zero", {"fps": 0}, 30),
        ("fps-negative", {"fps": -1}, 30),
        ("fps-empty", {"fps": []}, 30),
        ("fps-one", {"fps": [30000]}, 30),
        ("fps-three", {"fps": [30000, 1001, 1]}, 30),
        ("fps-noninteger", {"fps": [30000.0, 1001]}, 30),
        ("fps-zero-pair", {"fps": [30000, 0]}, 30),
        ("fps-negative-pair", {"fps": [-30000, 1001]}, 30),
        ("fps-rational-list", {"fps": [30000, 1001]}, 30),
        ("fps-rational-map", {"fps": {"numerator": 30000, "denominator": 1001}}, 30),
        ("fps-positive-scalar", {"fps": 24}, 24),
    ],
)
@pytest.mark.parametrize("dry_run", [False, True])
def test_open_canvas_forms_follow_upstream_fallback_through_production_provider(
    label, canvas, effective_fps, dry_run, monkeypatch,
):
    del label
    observed = []
    original_compile = timing_validation.compile_timing

    def capture(inputs):
        observed.append(production_fps(inputs.bundle))
        return original_compile(inputs)

    monkeypatch.setattr(timing_validation, "compile_timing", capture)
    document = _document_with_canvas(canvas)
    original = copy.deepcopy(document["parent_revision"]["payload"]["config"]["theme_overrides"])
    realm = provider.DetachedRealm(document)

    result = _service_call(
        realm,
        [provider.track_create("d136-open-canvas")],
        controls=_controls(dry_run=dry_run),
    )

    data = result["data"]
    assert data["status"] == ("preview" if dry_run else "accepted")
    if dry_run:
        assert data["would_status"] == "accepted"
        assert result["receipt"] is None
    else:
        assert result["receipt"]["result"] == data
    assert observed[-1] == effective_fps
    payload = data["canonical_document"]["parent_revision"]["payload"]
    assert payload["config"]["theme_overrides"] == original
