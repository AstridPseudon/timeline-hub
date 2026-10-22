"""Execute the collected P1 ``doc.patch`` vectors against the real R1 provider."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import (
    _digest,
    bundle_from_document,
    create_runtime_commit_service,
    document_from_bundle,
)
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedPort,
    DetachedRealm,
    inverse,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi as runtime_abi,
)

CORPUS = Path(__file__).resolve().parent / "fixtures" / "p1_feasibility"
REQUESTS = json.loads((CORPUS / "doc_patch_requests.json").read_text(encoding="utf-8"))
VECTORS = {vector["id"]: vector for vector in REQUESTS["vectors"]}


def _fixture(vector_id: str) -> dict[str, Any]:
    vector = VECTORS[vector_id]
    return json.loads(
        (CORPUS / vector["source"]["fixture"]).read_text(encoding="utf-8")
    )


def _bundle(vector_id: str) -> dict[str, Any]:
    fixture = _fixture(vector_id)
    if "input" in fixture:
        return bundle_from_document(fixture["input"])
    return copy.deepcopy(fixture["bundle"])


def _service_call(
    realm: DetachedRealm,
    commands: list[dict[str, Any]],
    *,
    controls: dict[str, Any],
    base: dict[str, str] | None = None,
) -> dict[str, Any]:
    context = realm.context(commands, base=base)
    context["request"].update(copy.deepcopy(controls))
    context["invocation"]["body"] = copy.deepcopy(context["request"])
    context["request_hash"] = _digest(context["invocation"])
    return create_runtime_commit_service().commit(context, DetachedPort(realm, context))


def _realm_for(vector_id: str) -> DetachedRealm:
    document = document_from_bundle(_bundle(vector_id))
    return DetachedRealm(document)


def _round_trip(value: Any) -> Any:
    return json.loads(json.dumps(value, allow_nan=False))


@pytest.mark.parametrize("vector_id", list(VECTORS))
def test_collected_vectors_execute_against_real_r1(vector_id: str) -> None:
    """Keep every collected success as a real provider assertion."""
    vector = VECTORS[vector_id]
    fixture = _fixture(vector_id)
    plan = execute(
        _bundle(vector_id),
        vector["request"]["commands"],
        commit_request=vector["request"],
    )

    assert plan.records
    assert _round_trip(plan.bundle) == plan.bundle

    if vector_id in {
        "trim-internal-clip-window",
        "created-track-and-clip-list-inserts",
    }:
        actual = document_from_bundle(plan.bundle)
        expected = fixture["output"]
        assert actual["parent_revision"]["payload"] == expected["parent_revision"]["payload"]
    elif vector_id == "ordered-list-move-and-order-refusal":
        actual = document_from_bundle(plan.bundle)["parent_revision"]["payload"]
        assert [row["id"] for row in actual["clips"]] == ["clip-b", "clip-a"]


@pytest.mark.parametrize(
    "vector_id",
    ["trim-internal-clip-window", "created-track-and-clip-list-inserts"],
)
def test_parent_vectors_use_runtime_commit_service_and_inverse(
    vector_id: str, runtime_abi: Any
) -> None:
    vector = VECTORS[vector_id]
    fixture = _fixture(vector_id)
    realm = _realm_for(vector_id)
    result = _service_call(
        realm,
        vector["request"]["commands"],
        controls=vector["request"],
    )

    assert result["data"]["status"] == vector["expected"]["status"]
    actual = result["data"]["canonical_document"]
    assert actual["parent_revision"]["payload"] == fixture["output"]["parent_revision"]["payload"]
    assert _round_trip(actual) == actual

    if vector_id == "created-track-and-clip-list-inserts":
        undone = _service_call(
            realm,
            [inverse([result["receipt"]["receipt_id"]])],
            controls={},
        )
        original = fixture["input"]["parent_revision"]["payload"]
        assert undone["data"]["canonical_document"]["parent_revision"]["payload"] == original


def _doc_patch(change: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": None,
        "args": {"changes": [change]},
    }


def _present(value: Any) -> dict[str, Any]:
    return {"state": "present", "value": copy.deepcopy(value)}


@pytest.mark.parametrize(
    ("vector_id", "intervening", "expected_reason"),
    [
        (
            "same-field-refusal",
            {
                "op": "set",
                "ref": "parent",
                "path": ["clips", "id:clip-a", "from"],
                "before": _present(2),
                "value": 3,
            },
            "value_conflict",
        ),
        (
            "ordered-list-move-and-order-refusal",
            {
                "op": "list.move",
                "ref": "parent",
                "path": ["clips"],
                "id": "clip-b",
                "before": _present(
                    {
                        "id": "clip-b",
                        "track": "picture",
                        "asset": "picture",
                        "clipType": "media",
                        "at": 5,
                        "hold": 2,
                        "app": {"org.example": {"literal": "clip-a", "clear": None}},
                    }
                ),
                "order_before": ["clip-a", "clip-b"],
                "after_id": None,
            },
            "selection_changed",
        ),
        (
            "ordered-list-move-and-order-refusal",
            {
                "op": "list.remove",
                "ref": "parent",
                "path": ["clips"],
                "id": "clip-b",
                "before": _present(
                    {
                        "id": "clip-b",
                        "track": "picture",
                        "asset": "picture",
                        "clipType": "media",
                        "at": 5,
                        "hold": 2,
                        "app": {"org.example": {"literal": "clip-a", "clear": None}},
                    }
                ),
                "order_before": ["clip-a", "clip-b"],
            },
            "selection_changed",
        ),
    ],
)
def test_provider_refuses_stale_same_field_membership_and_order(
    vector_id: str,
    intervening: dict[str, Any],
    expected_reason: str,
    runtime_abi: Any,
) -> None:
    vector = VECTORS[vector_id]
    realm = _realm_for(vector_id)
    original_head = copy.deepcopy(realm.head)
    _service_call(realm, [_doc_patch(intervening)], controls={"merge": "fields", "reads": []})
    head_after_intervening = copy.deepcopy(realm.head)
    entries_after_intervening = len(realm.entries)

    with pytest.raises(CommitRejected) as error:
        _service_call(
            realm,
            vector["request"]["commands"],
            controls=vector["request"],
            base=original_head,
        )

    assert error.value.failure["details"]["reason"] == expected_reason
    assert realm.head == head_after_intervening
    assert len(realm.entries) == entries_after_intervening

