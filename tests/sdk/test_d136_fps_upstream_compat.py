"""D136 preserves the upstream two-integer FPS spelling through the provider."""
from __future__ import annotations

import copy

import pytest

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
