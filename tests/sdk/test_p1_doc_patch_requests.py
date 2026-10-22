"""Fixture-only validation for the early P1 ``doc.patch`` request set.

The provider does not implement ``doc.patch`` on this branch.  These tests
check that the collected operands are contract-shaped, point at real physical
closure roots, retain fixture provenance, and carry exact tagged guards.  They
deliberately do not apply a patch or emulate provider execution.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CORPUS = Path(__file__).resolve().parent / "fixtures" / "p1_feasibility"
REQUESTS = json.loads(
    (CORPUS / "doc_patch_requests.json").read_text(encoding="utf-8")
)
MANIFEST = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
MANIFEST_CASES = MANIFEST["cases"]


def _fixture(vector: dict[str, Any]) -> dict[str, Any]:
    return json.loads(
        (CORPUS / vector["source"]["fixture"]).read_text(encoding="utf-8")
    )


def _source_case(vector: dict[str, Any]) -> dict[str, Any]:
    source = vector["source"]
    matches = [
        case
        for case in MANIFEST_CASES
        if case["fixture"] == source["fixture"]
        and case["provenance"] == source["provenance"]
    ]
    assert len(matches) == 1
    return matches[0]


def _internal_payload(fixture: dict[str, Any], timeline_id: str) -> dict[str, Any]:
    for revision in fixture["input"]["internal_timeline_revisions"]:
        if revision["timeline_id"] == timeline_id:
            return revision["payload"]
    raise AssertionError(f"missing internal timeline {timeline_id}")


def _bundle_clip(bundle: dict[str, Any], occurrence_id: str, clip_id: str) -> dict[str, Any]:
    placement = next(
        item for item in bundle["placements"] if item["occurrence_id"] == occurrence_id
    )
    shot = bundle["shots"][placement["shot_id"]]
    return next(
        clip for clip in shot["internal_timeline"]["clips"] if clip["id"] == clip_id
    )


def _root_for_change(vector: dict[str, Any], ref: str) -> Any:
    fixture = _fixture(vector)
    if ref == "parent":
        return fixture["input"]["parent_revision"]["payload"]
    if ref.startswith("internal:"):
        return _internal_payload(fixture, ref.removeprefix("internal:"))
    if ref.startswith("occurrence:"):
        occurrence, _, clip = ref.removeprefix("occurrence:").partition("/clip:")
        return _bundle_clip(fixture["bundle"], occurrence, clip)
    raise AssertionError(f"unhandled fixture root {ref}")


def _walk(root: Any, path: list[str]) -> Any:
    value = root
    for token in path:
        if isinstance(value, list):
            assert token.startswith("id:")
            identity = token.removeprefix("id:")
            value = next(item for item in value if item["id"] == identity)
        else:
            assert isinstance(value, dict)
            assert token in value, token
            value = value[token]
    return value


def _tagged(value: Any) -> dict[str, Any]:
    return {"state": "present", "value": copy.deepcopy(value)}


def _expected_change(vector: dict[str, Any], change: dict[str, Any]) -> dict[str, Any]:
    root = _root_for_change(vector, change["ref"])
    if change["op"].startswith("list."):
        if change["op"] == "list.insert":
            return {"state": "absent"}
        collection = _walk(root, change["path"])
        item = next(item for item in collection if item["id"] == change["id"])
        return _tagged(item)
    try:
        return _tagged(_walk(root, change["path"]))
    except (AssertionError, KeyError, StopIteration):
        return {"state": "absent"}


def _all_changes(vector: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        change
        for command in vector["request"]["commands"]
        for change in command["args"]["changes"]
    ]


def test_request_set_is_provenanced_to_the_merged_corpus() -> None:
    assert REQUESTS["status"] == "collection-only; provider execution pending"
    assert len(REQUESTS["vectors"]) == 8

    for vector in REQUESTS["vectors"]:
        source = vector["source"]
        case = _source_case(vector)
        canonical = CORPUS / source["fixture"]
        original = ROOT / source["source"]
        assert canonical.is_file()
        assert original.is_file()
        assert hashlib.sha256(canonical.read_bytes()).hexdigest() == source["source_sha256"]
        assert hashlib.sha256(original.read_bytes()).hexdigest() == source["source_sha256"]
        assert case["source_sha256"] == source["source_sha256"]
        assert vector["scope"]["physical_root"]
        assert vector["unexecuted_provider_cases"]


def test_commands_use_the_contract_doc_patch_shape() -> None:
    for vector in REQUESTS["vectors"]:
        request = vector["request"]
        assert request["merge"] in {"fields", "atomic"}
        assert isinstance(request["reads"], list)
        assert request["commands"]
        for command in request["commands"]:
            assert command == {
                key: command[key]
                for key in ("schema_version", "op", "version", "select", "created", "args")
                if key in command
            }
            assert command["schema_version"] == 1
            assert command["op"] == "doc.patch"
            assert command["version"] == "1"
            assert command["select"] is None
            assert isinstance(command.get("created", []), list)
            assert command["args"].keys() == {"changes"}
            assert command["args"]["changes"]
            for change in command["args"]["changes"]:
                assert change["op"] in {"set", "remove", "list.insert", "list.remove", "list.move"}
                assert isinstance(change["ref"], str)
                assert isinstance(change["path"], list)
                assert all(isinstance(token, str) for token in change["path"])
                assert set(change["before"]) == {"state"} or set(change["before"]) == {
                    "state",
                    "value",
                }
                if change["op"] == "set":
                    assert "value" in change
                if change["op"] == "remove":
                    assert change["before"]["state"] == "present"
                if change["op"].startswith("list."):
                    assert "id" in change
                    assert "order_before" in change
                    assert "after_id" in change or change["op"] == "list.remove"
                if change["op"] == "list.insert":
                    assert change["before"] == {"state": "absent"}
                    assert change["value"]["id"] == change["id"]


def test_guards_are_exact_values_from_the_fixture_inputs() -> None:
    for vector in REQUESTS["vectors"]:
        for change in _all_changes(vector):
            assert change["before"] == _expected_change(vector, change), (
                vector["id"],
                change,
            )


def test_expected_authored_deltas_match_the_submitted_operands() -> None:
    for vector in REQUESTS["vectors"]:
        expected = vector["expected"]
        changes = _all_changes(vector)
        authored = expected.get("authored_deltas", [])
        assert len(authored) == sum(change["op"] in {"set", "remove"} for change in changes)
        for delta, change in zip(authored, [c for c in changes if c["op"] in {"set", "remove"}]):
            assert delta["path"] == change["path"]
            assert delta.get("ref", change["ref"]) == change["ref"]
            expected_before = (
                change["before"]
                if isinstance(delta["before"], dict) and "state" in delta["before"]
                else change["before"].get("value", change["before"])
            )
            assert delta["before"] == expected_before
            after = {"state": "absent"} if change["op"] == "remove" else change["value"]
            assert delta["after"] == after


def test_real_opaque_values_and_tagged_states_are_not_normalized() -> None:
    params_absent = next(v for v in REQUESTS["vectors"] if v["id"] == "params-absent-to-explicit-values")
    params_null = next(v for v in REQUESTS["vectors"] if v["id"] == "params-null-to-object")
    params_remove = next(v for v in REQUESTS["vectors"] if v["id"] == "params-remove-and-preserve-opaque")

    assert params_absent["expected"]["tagged_states"] == {
        "params": "absent",
        "params.null": "absent",
        "params.old": "absent",
    }
    assert params_null["request"]["commands"][0]["args"]["changes"][0]["before"] == {
        "state": "present",
        "value": None,
    }
    assert params_remove["expected"]["opaque_preserved"] == {
        "params.opaque": {"keep": [False, {}, ""]},
        "params.x": 1,
        "params.y": None,
    }
    remove = params_remove["request"]["commands"][0]["args"]["changes"][0]
    assert remove["op"] == "remove"
    assert remove["before"] == {"state": "present", "value": None}


def test_collection_vectors_guard_membership_and_order_without_execution() -> None:
    vector = next(v for v in REQUESTS["vectors"] if v["id"] == "ordered-list-move-and-order-refusal")
    change = vector["request"]["commands"][0]["args"]["changes"][0]
    assert change["op"] == "list.move"
    assert change["order_before"] == ["clip-a", "clip-b"]
    assert vector["expected"]["order_after"] == ["clip-b", "clip-a"]
    assert vector["expected"]["order_refusal"]["code"] == "selection_changed"
    assert vector["expected"]["membership_refusal"]["code"] == "selection_changed"


def test_provider_execution_is_explicitly_pending() -> None:
    assert not any("executor" in vector for vector in REQUESTS["vectors"])
    assert not any("provider_result" in vector for vector in REQUESTS["vectors"])
    assert {vector["expected"]["status"] for vector in REQUESTS["vectors"]} == {
        "accepted",
        "merged",
        "conflict",
    }
