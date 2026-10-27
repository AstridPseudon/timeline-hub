"""Authenticate unchanged sequential images at their own command boundary."""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_auth import command_output
from runtime_protocol.timeline_commit_validation import digest

pytest_plugins = ("test_timeline_commit_authentication",)


def _request_with_admission(submitted, source, runtime=None, project=None):
    def find_pin(value):
        if isinstance(value, dict):
            if set(value) == {"media_id", "content_digest"}:
                return value
            if isinstance(value.get("object_id"), str):
                return {"media_id": value["object_id"], "content_digest": value["object_id"]}
            for child in value.values():
                found = find_pin(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = find_pin(child)
                if found is not None:
                    return found
        return None

    pin = source["dependency_manifest"]["media"][0] if source["dependency_manifest"]["media"] else None
    if pin is None and runtime is not None:
        media = next(command["args"]["media"] for command in submitted["commands"]
                     if "media" in command.get("args", {}))
        selection = runtime.get_project_media_selection(
            project, {key: media[key] for key in ("asset", "generation_id", "variant_id")},
            authorize=lambda: None,
        )
        pin = {"media_id": selection["object_id"], "content_digest": selection["object_id"]}
    if pin is None:
        pin = find_pin(submitted)
    assert pin is not None, json.dumps(submitted["commands"], indent=2)
    media_selection = next(command["args"]["media"] for command in submitted["commands"]
                           if "media" in command.get("args", {}))
    admission = {
        "schema_version": 1,
        "op": "media.admit",
        "version": "1",
        "select": None,
        "args": {"inputs": [{"pin": copy.deepcopy(pin), "selection": copy.deepcopy(media_selection)}]},
    }
    commands = [admission, *copy.deepcopy(submitted["commands"])]
    child_step = copy.deepcopy(submitted["steps"][0])
    child_step["id"] = "child"
    child_step["command_ordinals"] = list(range(1, len(commands)))
    return {
        **copy.deepcopy(submitted),
        "commands": commands,
        "steps": [
            {"id": "media", "label": "Capture media", "intent": "", "tags": [],
             "command_ordinals": [0], "patch": [], "reads": []},
            child_step,
        ],
    }


@pytest.mark.parametrize("created_child_public", [True], indirect=True)
def test_admission_step_uses_its_unchanged_parent_boundary(created_child_public):
    runtime, project, source, submitted, held, document, publish = created_child_public
    parent_media = next(command["args"]["row"] for command in submitted["commands"]
                        if command["op"] == "clip.add-media")
    submitted = _request_with_admission(submitted, source, runtime, project)

    result = publish(submitted, "intermediate-image")
    canonical = result["data"]["canonical_document"]

    assert result["data"]["status"] == "accepted"
    assert canonical == document()
    assert canonical["parent_revision"]["payload"]["clips"] == [parent_media]
    assert canonical["parent_revision"]["payload"]["config"]["clips"] == [parent_media]
    assert canonical["internal_timeline_revisions"][0]["payload"]["clips"] == [held]


@pytest.mark.parametrize("created_child_public", [True], indirect=True)
@pytest.mark.parametrize("damage", ["intermediate_image", "effect_ordinal", "changed_pin", "wrong_owner"])
def test_admission_step_rejects_forged_intermediate_authority(created_child_public, monkeypatch, damage):
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    runtime, project, source, submitted, _held, document, publish = created_child_public
    submitted = _request_with_admission(submitted, source, runtime, project)
    original_accept = RequestCommitPort.accept
    original_capture = RequestCommitPort.capture_sequential_execution

    def forge_capture(port, capture):
        capture = copy.deepcopy(capture)
        if damage == "intermediate_image":
            output = capture["landing"]["commands"][0]["output"]
            output["parent_revision"]["payload"]["forged"] = True
            output["parent_revision"]["content_digest"] = "sha256:" + "0" * 64
        return original_capture(port, capture)

    def forge_accept(port, prepared):
        prepared = copy.deepcopy(prepared)
        bindings = [binding for record in prepared["records"]["commands"]
                    for binding in record["bindings"]]
        if damage == "effect_ordinal":
            next(binding for binding in bindings if binding.get("key") == "commit.effect")["effect_ordinal"] = 99
        elif damage == "changed_pin":
            next(binding for binding in bindings if binding.get("key") == "commit.effect")["revision_id"] = "foreign"
        elif damage == "wrong_owner":
            binding = next(binding for binding in bindings if "owners" in binding)
            binding["owner"] = "occurrence:foreign/shot"
            binding["owners"] = ["occurrence:foreign/shot"]
        return original_accept(port, prepared)

    monkeypatch.setattr(RequestCommitPort, "capture_sequential_execution", forge_capture)
    monkeypatch.setattr(RequestCommitPort, "accept", forge_accept)
    before = document()
    with pytest.raises(RuntimeErrorBase) as error:
        publish(submitted, "intermediate-image-" + damage)

    assert error.value.details is not None
    assert error.value.details["reason"] == "invalid_records"
    assert document() == before == source


@pytest.mark.parametrize("path", [["clips"], ["config", "clips"]])
def test_command_output_requires_exact_clip_observation_and_preserves_order(path):
    before = [
        {"id": "clip-a", "track": "V1", "extension": {"keep": [1, None]}},
        {"id": "clip-b", "track": "V2", "extension": {"keep": [2, None]}},
    ]
    after = [copy.deepcopy(before[1]), copy.deepcopy(before[0])]
    payload = {"config": {"clips": copy.deepcopy(before)}, "clips": copy.deepcopy(before)}
    boundary = {"parent": {"revision_id": "parent-before", "content_digest": digest(payload),
                            "payload": payload}}
    record = {"ordinal": 0, "writes": [{
        "ref": "parent", "path": path,
        "before": {"state": "present", "value": copy.deepcopy(before)},
        "after": {"state": "present", "value": copy.deepcopy(after)},
    }], "derived_writes": [], "created": []}
    projected = copy.deepcopy(payload)
    projected["config"]["clips"] = copy.deepcopy(after)
    projected["clips"] = copy.deepcopy(after)
    following = {"bindings": [{"physical_ref": "parent", "revision_id": "parent-after",
                                "content_digest": digest(projected),
                                "boundary": {"phase": "input"}}], "reads": []}

    output = command_output(boundary, record, following)

    assert output["parent"]["revision_id"] == "parent-after"
    assert output["parent"]["payload"]["config"]["clips"] == after
    assert output["parent"]["payload"]["clips"] == after

    forged = copy.deepcopy(record)
    forged["writes"][0]["before"]["value"][0]["extension"]["keep"][0] = 9
    with pytest.raises(CommitRejected, match="different input observation"):
        command_output(boundary, forged, following)
