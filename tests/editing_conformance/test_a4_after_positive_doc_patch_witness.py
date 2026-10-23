"""A4 witnesses for the App's exact positive parent ``doc.patch`` inputs.

The packet was independently reviewed from the mounted App editor path.  The
data below is a lossless, ordinary-checkout copy of that finite input: it is
not a Runtime response, media authority, or provider golden.  The registered
Agent provider is still the authority exercised by these tests.  If it cannot
accept the captured request, the test fails with the bounded provider cause;
that refusal is not treated as the intended positive behavior.
"""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from astrid.sdk.timeline._command_state import present
from astrid.sdk.timeline.commit import _digest, create_runtime_commit_service
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedPort,
    DetachedRealm,
    runtime_abi,  # noqa: F401 -- autouse detached ABI fixture
)

APP_CALL_BINDING = (
    "useMountedCommands(...).commands.addClip({ preparedAsset, trackId: V1, "
    "afterClipId: anchor, time: 0 }) -> useTimelineSave.applyEdit -> "
    "localSaveSession/outbox -> RuntimeDataProvider.commitTimeline -> "
    "AstridRuntimeClient/generated transport"
)
ORDER = ["anchor", "later", "sibling"]
STEP_IDS = {
    "old video with missing hold": "92a759c1-7e28-4788-acbc-367bc40ee4b7",
    "old video with explicit null hold": "7514a8e6-9b71-456f-8044-d5e12b45935f",
    "old video with subminimum duration": "77649057-4a0c-46e4-83b7-1e45ffec4af9",
    "old video with incoming transition": "3af2e725-c52f-43d9-aaaa-f74a6b45a2a3",
}
REQUEST_LENGTHS = {
    "old video with missing hold": 2368,
    "old video with explicit null hold": 2452,
    "old video with subminimum duration": 2656,
    "old video with incoming transition": 2416,
}
REQUEST_SHA256 = {
    "old video with missing hold": "38afc0473df1616da071f35c3362fcfb7a01dc3fe904a0a7b49b2a0c66c738a1",
    "old video with explicit null hold": "a422aaf915d72edb848029e74a394a8ba43897bc3551882a7982b00e268269f1",
    "old video with subminimum duration": "99cf8093817631e9df49a4093c3086522419009f58e855fc287bcb62603f17f5",
    "old video with incoming transition": "e1f05b38f044d4557f0e28c12c644d077f85e617590a1b2b9050fb4c93527ae5",
}
BASE_DIGESTS = {
    "old video with missing hold": "sha256:445b8013f7a0db22f5c961f041598012a265d025aa4557b2294df237da8e3431",
    "old video with explicit null hold": "sha256:6c97876532b4ac508b20824295a6ce2f4feed2387c922ec17ac9442083eda313",
    "old video with subminimum duration": "sha256:e0f6d16e3d8891e0d338222a52af2c7990bc1bda5ee9dc16b81c193f1b08526f",
    "old video with incoming transition": "sha256:94cf0261c216274f2559d9ac0b31b8d5a4782a0db8d53124ebf052d13f602825",
}


def _absent():
    return {"state": "absent"}


def _base(case):
    anchor = {
        "id": "anchor",
        "at": 1,
        "track": "V1",
        "clipType": "video",
        "asset": "asset-source",
        "opacity": 0.5,
        "effects": {"glow": 1},
        "params": {"opaque": {"ordered": [None, False, 0]}},
        "app": {"opaque": {"keep": None, "ordered": [False, 0, ""]}},
    }
    if case in {
        "old video with missing hold",
        "old video with explicit null hold",
        "old video with incoming transition",
    }:
        anchor.update({"from": 2, "to": 6, "speed": 2})
    if case == "old video with explicit null hold":
        anchor["hold"] = None
    if case == "old video with subminimum duration":
        anchor["hold"] = 0.01
    anchor["transition"] = (
        {"type": "crossfade", "duration": 0.5, "opaque": [False, None]}
        if case == "old video with incoming transition"
        else {"type": "crossfade", "duration": 0.5, "params": {"opaque": [None, False]}}
    )
    later = {"id": "later", "at": 5, "track": "V1", "clipType": "hold", "hold": 1, "asset": "asset-peer"}
    sibling = {"id": "sibling", "at": 5, "track": "V2", "clipType": "hold", "hold": 1, "asset": "asset-peer"}
    clips = [anchor, later, sibling]
    payload = {
        "config": {
            "output": {
                "resolution": "1280x720",
                "fps": 30,
                "file": "output.mp4",
                "background": None,
                "background_scale": None,
            },
            "clips": copy.deepcopy(clips),
            "tracks": [
                {"id": "V1", "kind": "visual", "label": "V1"},
                {"id": "V2", "kind": "visual", "label": "V2"},
            ],
        },
        "clips": copy.deepcopy(clips),
        "registry": {
            "assets": {
                "asset-source": {"file": "source.mp4", "type": "video/mp4", "media_id": "media-source"},
                "asset-peer": {"file": "peer.png", "type": "image/png"},
            }
        },
        "occurrences": [],
        "opaque": {"keep": None},
    }
    document = {
        "schema_version": 1,
        "project_id": "project-commit",
        "timeline_id": "timeline-1",
        "parent_revision": {"revision_id": "r0", "content_digest": _digest(payload), "payload": payload},
        "shot_revisions": [],
        "internal_timeline_revisions": [],
        "dependency_manifest": {"shots": [], "internal_timelines": [], "media": [], "documents": []},
    }
    pins = {
        "anchor": copy.deepcopy(anchor),
        "later": copy.deepcopy(later),
        "sibling": copy.deepcopy(sibling),
        "source_asset": {"file": "source.mp4", "type": "video/mp4", "media_id": "media-source"},
    }
    return document, pins


def _patch_change(case):
    suffix = case.removeprefix("old video with ").replace(" ", "-")
    asset = "asset-old-video-with-" + suffix
    value = {
        "id": "clip-0",
        "at": 1 if case == "old video with subminimum duration" else 3,
        "track": "V1",
        "asset": asset,
        "clipType": "video",
    }
    if case != "old video with subminimum duration":
        value.update({"from": 2, "to": 6, "speed": 2})
    if case == "old video with explicit null hold":
        value["hold"] = None
    if case == "old video with subminimum duration":
        value["hold"] = 0.0667
    value.update(
        {
            "opacity": 0.5,
            "transition": (
                {"type": "crossfade", "duration": 0.5, "opaque": [False, None]}
                if case == "old video with incoming transition"
                else {"type": "crossfade", "duration": 0.5, "params": {"opaque": [None, False]}}
            ),
            "effects": {"glow": 1},
            "params": {"opaque": {"ordered": [None, False, 0]}},
            "app": {"opaque": {"keep": None, "ordered": [False, 0, ""]}},
            "label": "source.mp4",
        }
    )
    changes = [
        {
            "op": "list.insert",
            "ref": "parent",
            "path": ["clips"],
            "id": "clip-0",
            "before": _absent(),
            "value": value,
            "order_before": ORDER,
            "after_id": "anchor",
        }
    ]
    if case == "old video with subminimum duration":
        changes.extend(
            [
                {
                    "op": "set",
                    "ref": "parent",
                    "path": ["clips", "id:anchor", "hold"],
                    "before": present(0.01),
                    "value": 0,
                },
                {
                    "op": "set",
                    "ref": "parent",
                    "path": ["clips", "id:later", "at"],
                    "before": present(5),
                    "value": 5.0667,
                },
            ]
        )
    else:
        changes.append(
            {
                "op": "set",
                "ref": "parent",
                "path": ["clips", "id:later", "at"],
                "before": present(5),
                "value": 7,
            }
        )
    changes.append(
        {
            "op": "set",
            "ref": "parent",
            "path": ["registry", "assets", asset],
            "before": _absent(),
            "value": {
                "file": "old-video-with-" + suffix + ".mp4",
                "type": "video/mp4",
                "media_id": "media-old-video-with-" + suffix,
                "generationId": "generation-old-video-with-" + suffix,
            },
        }
    )
    return changes


def _request(case):
    changes = _patch_change(case)
    command = {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": None,
        "created": ["parent/clip:clip-0"],
        "args": {"changes": changes},
    }
    request = {
        "api_version": 1,
        "project_id": "project-commit",
        "timeline_id": "timeline-1",
        "base_revision_id": "r0",
        "base_publication_id": "p0",
        "commands": [command],
        "source": {"via": "app"},
        "label": "Edit timeline",
        "dry_run": False,
        "steps": [
            {
                "id": STEP_IDS[case],
                "label": "Edit timeline",
                "intent": "Save local editor changes",
                "tags": [],
                "command_ordinals": [0],
                "patch": copy.deepcopy(changes),
            }
        ],
        "merge": "atomic",
    }
    return request


def _context(request):
    invocation = {
        "operation": "commitTimeline",
        "path": "/v1/projects/project-commit/timelines/timeline-1/commit",
        "body": copy.deepcopy(request),
    }
    return {
        "request": copy.deepcopy(request),
        "invocation": invocation,
        "request_hash": _digest(invocation),
        "idempotency_key": "a4-positive-" + request["steps"][0]["id"],
        "realm_id": "a4-positive-realm",
        "publisher": "a4-positive-app",
    }


def _case_names():
    return tuple(STEP_IDS)


@pytest.mark.parametrize("case", _case_names())
def test_app_positive_doc_patch_witness_replays_exact_input_through_registered_provider(case):
    document, source_pins = _base(case)
    request = _request(case)
    request_bytes = json.dumps(request, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()

    assert APP_CALL_BINDING.startswith("useMountedCommands")
    assert document["parent_revision"]["content_digest"] == BASE_DIGESTS[case]
    assert source_pins["anchor"] == document["parent_revision"]["payload"]["clips"][0]
    assert source_pins["later"] == document["parent_revision"]["payload"]["clips"][1]
    assert source_pins["sibling"] == document["parent_revision"]["payload"]["clips"][2]
    assert source_pins["source_asset"] == document["parent_revision"]["payload"]["registry"]["assets"]["asset-source"]
    assert len(request_bytes) == REQUEST_LENGTHS[case]
    assert hashlib.sha256(request_bytes).hexdigest() == REQUEST_SHA256[case]
    assert request["commands"][0]["op"] == "doc.patch"
    assert request["commands"][0]["args"]["changes"] == request["steps"][0]["patch"]
    assert request["commands"][0]["created"] == ["parent/clip:clip-0"]
    assert request["api_version"] == 1
    assert request["project_id"] == "project-commit"
    assert request["timeline_id"] == "timeline-1"
    assert (request["base_revision_id"], request["base_publication_id"]) == ("r0", "p0")
    assert request["commands"] == [_request(case)["commands"][0]]
    assert request["steps"] == [_request(case)["steps"][0]]
    assert request["source"] == {"via": "app"}
    assert request["label"] == "Edit timeline"
    assert request["dry_run"] is False
    # The mounted packet omits these controls.  Do not turn omission into an
    # explicit empty declaration by reading them with a default.
    assert "reads" not in request
    assert "declared_reads" not in request
    assert "declaredreads" not in request
    assert "reads" not in request["commands"][0]
    assert "reads" not in request["steps"][0]
    assert request["merge"] == "atomic"

    captured_request = copy.deepcopy(request)
    realm = DetachedRealm(document)
    realm.head["publication_id"] = "p0"
    realm.entries[0]["publication_id"] = "p0"
    realm.entries[0]["receipt"]["receipt_id"] = "p0"
    context = _context(request)
    before = {
        "head": copy.deepcopy(realm.head),
        "entries": copy.deepcopy(realm.entries),
        "documents": copy.deepcopy(realm.documents),
        "accepted": copy.deepcopy(realm.accepted),
    }

    try:
        result = create_runtime_commit_service().commit(context, DetachedPort(realm, context))
    except CommitRejected as error:
        assert context["request"] == captured_request
        assert request == captured_request
        assert realm.head == before["head"]
        assert realm.entries == before["entries"]
        assert realm.documents == before["documents"]
        assert realm.accepted == before["accepted"]
        details = error.failure["details"]
        pytest.fail(
            "captured positive App doc.patch was not accepted by the registered provider: "
            f"case={case!r}; source={APP_CALL_BINDING}; "
            f"request_sha256={REQUEST_SHA256[case]}; status={details.get('status')!r}; "
            f"reason={details.get('reason')!r}; path={details.get('path')!r}; "
            f"conflicts={details.get('conflicts')!r}; "
            "the request introduces prepared media outside the provider's verified inputs"
        )

    data = result["data"]
    assert data["status"] in {"accepted", "merged"}
    assert data["base_revision_id"] == "r0"
    assert data["base_publication_id"] == "p0"
    assert data["canonical_document"]["parent_revision"]["revision_id"] != "r0"
    assert set(data["canonical_document"]) == {
        "schema_version", "project_id", "timeline_id", "parent_revision",
        "shot_revisions", "internal_timeline_revisions", "dependency_manifest",
    }
    assert data["document_digest"] == _digest(data["canonical_document"])
    assert data["label"] == request["label"]
    assert data["merge_mode"] == request["merge"]
    assert data["commands"] == request["commands"]
    assert result["receipt"] is not None
    assert set(result["receipt"]) == {
        "receipt_id", "command_kind", "idempotency_key", "request_hash",
        "project_id", "project_seq", "event_ids", "result", "created_at",
    }
    assert result["receipt"]["result"] == data
    assert result["receipt"]["idempotency_key"] == context["idempotency_key"]
    assert result["receipt"]["request_hash"] == context["request_hash"]
    assert context["request"] == captured_request

    accepted_records = realm.entries[-1]["records"]
    assert set(accepted_records) == {
        "schema_version", "commands", "steps", "label", "merge_mode",
        "undo_of", "restored_from", "undo_steps",
    }
    command_record = accepted_records["commands"][0]
    assert accepted_records["label"] == request["label"]
    assert accepted_records["merge_mode"] == request["merge"]
    assert accepted_records["steps"][0]["patch"] == request["steps"][0]["patch"]
    accepted_step = accepted_records["steps"][0]
    assert set(accepted_step) == {
        "id", "label", "intent", "tags", "command_ordinals", "patch", "dependencies",
    }
    assert accepted_step["id"] == request["steps"][0]["id"]
    assert accepted_step["label"] == request["steps"][0]["label"]
    assert accepted_step["intent"] == request["steps"][0]["intent"]
    assert accepted_step["tags"] == request["steps"][0]["tags"]
    assert accepted_step["command_ordinals"] == request["steps"][0]["command_ordinals"]
    assert any(
        dependency == {"kind": "scope", "ref": "parent", "path": []}
        for dependency in accepted_step["dependencies"]
    )
    assert command_record["command"] == request["commands"][0]
    assert command_record["writes"]
    assert isinstance(command_record["bindings"], list)
    assert isinstance(command_record["dependencies"], list)
    assert command_record["derived_writes"] == []
    effect_bindings = [binding for binding in command_record["bindings"]
                       if binding["key"] == "commit.effect"]
    assert effect_bindings
    assert all(binding["policy"] == "fixed" for binding in effect_bindings)
    assert {binding["step_id"] for binding in effect_bindings} == {accepted_step["id"]}
    assert {binding["effect_ordinal"] for binding in effect_bindings} == set(range(len(accepted_step["patch"])))
    assert all(set(dependency) == {"key", "kind", "pin", "policy"}
               for dependency in command_record["dependencies"])
    assert accepted_records["undo_steps"] is None
    assert accepted_records["undo_of"] == []
    assert accepted_records["restored_from"] is None

    history_entry = realm.entries[-1]
    assert history_entry["intent"] == "recorded"
    assert history_entry["previous"] == before["head"]
    assert history_entry["revision_id"] == data["accepted_revision_id"]
    assert history_entry["receipt"] == result["receipt"]
    assert history_entry["records"] == accepted_records

    # These are the positive intended fields; acceptance must retain every
    # untouched sibling/opaque field and apply only the captured patch effects.
    payload = result["data"]["canonical_document"]["parent_revision"]["payload"]
    assert [row["id"] for row in payload["clips"]] == ["anchor", "clip-0", "later", "sibling"]
    inserted = next(row for row in payload["clips"] if row["id"] == "clip-0")
    expected = request["commands"][0]["args"]["changes"][0]["value"]
    assert inserted == expected
    if case == "old video with missing hold":
        assert "hold" not in inserted
    elif case == "old video with explicit null hold":
        assert inserted["hold"] is None
    elif case == "old video with subminimum duration":
        assert inserted["hold"] == 0.0667
    else:
        assert inserted["transition"] == {"type": "crossfade", "duration": 0.5, "opaque": [False, None]}
    assert payload["clips"][0] == source_pins["anchor"]
    assert payload["clips"][2]["at"] == request["commands"][0]["args"]["changes"][1]["value"]
    assert payload["clips"][3] == source_pins["sibling"]
    assert payload["config"]["clips"] == payload["clips"]
    assert payload["registry"]["assets"]["asset-source"] == source_pins["source_asset"]
    assert payload["registry"]["assets"]["asset-peer"] == {"file": "peer.png", "type": "image/png"}
    registry_change = request["commands"][0]["args"]["changes"][-1]
    assert payload["registry"]["assets"][registry_change["path"][-1]] == registry_change["value"]
