"""The frozen Agent union is packaged and publicly typed without changing Runtime DTOs."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import get_args, get_type_hints

import astrid_runtime_client as client
import pytest
from astrid_runtime_client import timeline_commit_types as dto

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit_validation import validate_commit_value
from test_timeline_bundle2_contract import CASES as ORDINARY_CASES, DIGEST, MEDIA

ROOT = Path(__file__).resolve().parents[1]
TARGET = {"project_id": "p", "timeline_id": "t", "base_revision_id": "r", "base_publication_id": "txn"}
PRODUCER = {"task_id": "task", "attempt_id": "attempt", "executor_id": "executor", "fence": 1, "runtime_epoch": 1}
PIN = {**PRODUCER, "admitted_target": TARGET, "proposal_digest": DIGEST}
PRIVATE_RAW_SHA256 = "9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec"
PRIVATE_CANONICAL_SHA256 = "322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc"
ORDINARY_RAW_SHA256 = "6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d"
CASES = ORDINARY_CASES + [
    ("shot.set", "occurrence:o/shot", {"values": {"name": "Shot", "settings": {"enhancePrompt": False, "batchVideoFrames": 1.5}}, "clear": []}),
    ("clip.set-element", "parent/clip:c", {"elementRef": {"id": "element", "kind": "component", "revision": "r"}}),
    ("placement.create", "occurrence:o", {"id": "c", "on": 0, "hold": 1.5, "media": MEDIA, "consumed": ["existing"]}),
    ("placement.unplace", "occurrence:o/clip:c", {}),
    ("shot.pool", "occurrence:o", {"action": "add", "media": MEDIA}),
    ("occurrence.duplicate", "occurrence:o", {"occurrence_id": "new", "shot_id": "new-shot"}),
    ("occurrence.delete", "occurrence:o", {}),
    ("producer.guard", None, {"pin": PIN}),
]
NEW_OPERATIONS = {
    "timeline.assembled-target",
    "clip.add-media",
    "timeline.init",
    "clip.anchor",
    "occurrence.create",
    "clip.swap-media",
    "text-binding.set",
}
PRIVATE_OPERATIONS = {
    "clip.move-set",
    "track.reorder",
    "timeline.migrate-groups",
    "occurrence.move",
    "occurrence.resize",
    "transcript.associate",
    "project-data.write",
    "timeline.reference",
}


def command(op, select, args):
    return {"schema_version": 1, "op": op, "version": "1", "select": select, "args": copy.deepcopy(args)}


def _ordinary_schema_bytes(private_schema):
    """Strip private016 additions and restore the exact ordinary6ba JSON bytes."""
    ordinary = copy.deepcopy(private_schema)
    for name in (
        "ClipMoveSetArgs", "TrackReorderArgs", "MediaManifestEntry", "RawOldSwapMediaArgs",
        "MigrateGroupsArgs", "ProjectDataWriteArgs", "TimelineReferenceArgs", "OccurrenceMoveArgs",
        "OccurrenceResizeArgs", "TranscriptAssociateArgs",
    ):
        ordinary["$defs"].pop(name)
    for name in ("EntityRef", "TargetKey", "ScopedId"):
        ordinary["$defs"][name]["anyOf"].pop()
    anchor_pattern = ordinary["$defs"]["AnchorIdentity"]["pattern"]
    ordinary["$defs"]["AnchorIdentity"]["pattern"] = anchor_pattern[3:].split(
        "$)|(?:^shot:", 1
    )[0] + "$"

    clip = ordinary["$defs"]["ClipSetArgs"]
    clip["properties"]["values"]["properties"].pop("opacity")
    clip["properties"]["clear"]["items"]["enum"].pop()
    clip["description"] = (
        "Bounded raw clip fields. Set hold in source seconds; explicitly remove hold, asset or "
        "incoming transition. Clear removes presence, never sets null/empty. Asset assignment "
        "requires the scoped clip.swap-media or occurrence.swap-media; transition authoring is "
        "outside v1."
    )
    track = ordinary["$defs"]["TrackSetArgs"]
    track["properties"]["values"]["properties"].pop("muted")
    track["properties"]["clear"]["items"] = {"const": "label"}
    track["description"] = "Set raw track.label or explicitly remove it. Null is not a label. Unmentioned fields survive."
    shot = ordinary["$defs"]["ShotSetArgs"]
    shot["properties"]["values"]["properties"].pop("metadata")
    shot["properties"]["clear"]["items"]["enum"].pop()
    shot["description"] = (
        "Occurrence-owned raw shot payload fields: canonical root name and bounded scalar settings roots. "
        "Null is a value; clear removes presence. Unmentioned fields survive. Compound settings roots "
        "(steerableMotionSettings, phaseConfig, pairConfigs, shotImageIds, loras, structureVideo, "
        "modelSettingsByModel) are unsupported."
    )

    ordinary["$defs"]["EditCommand"]["allOf"] = []
    for clause in private_schema["$defs"]["EditCommand"]["allOf"]:
        operation = clause["if"]["properties"]["op"]["const"]
        if operation in PRIVATE_OPERATIONS:
            continue
        restored = copy.deepcopy(clause)
        if "anyOf" in restored["then"]:
            restored["then"] = restored["then"]["anyOf"][0]
        ordinary["$defs"]["EditCommand"]["allOf"].append(restored)
    return (json.dumps(ordinary, indent=2) + "\n").encode()


def test_exact_frozen_schema_and_operation_inventory_are_packaged():
    raw = (ROOT / "contract/schemas/edit-command.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PRIVATE_RAW_SHA256
    schema = json.loads(raw)
    assert hashlib.sha256((json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode()).hexdigest() == PRIVATE_CANONICAL_SHA256
    assert len(schema["$defs"]) == 65
    assert len(schema["$defs"]["EditCommand"]["allOf"]) == 37
    expected_operations = {c[0] for c in CASES} | NEW_OPERATIONS | PRIVATE_OPERATIONS
    assert {c["if"]["properties"]["op"]["const"] for c in schema["$defs"]["EditCommand"]["allOf"]} == expected_operations
    bundle = json.loads((ROOT / "runtime_protocol/schemas/timeline-commit-bundle.json").read_bytes())
    assert bundle["resources"]["https://astrid.haus/workspace/v1/schemas/edit-command.json"] == schema
    ordinary_raw = _ordinary_schema_bytes(schema)
    assert hashlib.sha256(ordinary_raw).hexdigest() == ORDINARY_RAW_SHA256
    ordinary = json.loads(ordinary_raw)
    assert len(ordinary["$defs"]) == 55
    assert len(ordinary["$defs"]["EditCommand"]["allOf"]) == 29


@pytest.mark.parametrize("values,clear", [
    ({"label": "Picture"}, []),
    ({}, ["label"]),
    ({"label": "Picture"}, ["label"]),
    ({"muted": False}, []),
    ({}, ["muted"]),
    ({"muted": True}, ["label", "muted"]),
], ids=["label-set", "label-clear", "label-overlap", "muted-set", "muted-clear", "muted-overlap"])
def test_track_set_preserves_old_label_and_adds_private_muted_shapes(values, clear):
    validate_commit_value(command("track.set", "parent/track:video", {"values": values, "clear": clear}), "EditCommand")


@pytest.mark.parametrize("args", [
    {"values": {}, "clear": []},
    {"values": {"muted": "false"}, "clear": []},
    {"values": {"muted": None}, "clear": []},
    {"values": {"label": "Picture", "unknown": True}, "clear": []},
    {"values": {}, "clear": ["unknown"]},
    {"values": {"label": "Picture"}, "clear": None},
], ids=["empty", "wrong-muted-type", "null-muted", "unknown-value", "unknown-clear", "null-clear"])
def test_track_set_refuses_empty_wrong_typed_null_and_unknown_shapes(args):
    with pytest.raises(ValidationError):
        validate_commit_value(command("track.set", "parent/track:video", args), "EditCommand")


@pytest.mark.parametrize("op,select,args", CASES, ids=[c[0] for c in CASES])
def test_all_registered_operations_keep_args_and_refuse_unknown_keys(op, select, args):
    value = command(op, select, args)
    original = copy.deepcopy(value)
    validate_commit_value(value, "EditCommand")
    assert value == original
    value["args"]["unknown"] = None
    with pytest.raises(ValidationError):
        validate_commit_value(value, "EditCommand")


@pytest.mark.parametrize("op", ["placement.create", "occurrence.add-media"])
@pytest.mark.parametrize("consumed", [["a", "b"], [], ["a", "a"], ["a/b"], ["a::b"], [True]])
def test_consumed_ids_keep_uniqueness_and_raw_id_patterns(op, consumed):
    _, select, args = next(c for c in CASES if c[0] == op)
    value = command(op, select, {**args, "consumed": consumed})
    if consumed in (["a", "b"], []):
        validate_commit_value(value, "EditCommand")
    else:
        with pytest.raises(ValidationError):
            validate_commit_value(value, "EditCommand")


@pytest.mark.parametrize("field,bad", [
    ("fence", True), ("runtime_epoch", False), ("fence", 0), ("runtime_epoch", 1.5),
    ("task_id", " "), ("proposal_digest", "sha256:" + "a" * 63),
    ("admitted_target", {**TARGET, "unknown": None}),
])
def test_producer_pin_constraints_are_retained(field, bad):
    value = command("producer.guard", None, {"pin": {**PIN, field: bad}})
    with pytest.raises(ValidationError):
        validate_commit_value(value, "EditCommand")


@pytest.mark.parametrize("field,bad", [("enhancePrompt", 1), ("batchVideoFrames", True)])
def test_shot_settings_keep_boolean_number_distinction(field, bad):
    value = command("shot.set", "occurrence:o/shot", {"values": {"settings": {field: bad}}, "clear": []})
    with pytest.raises(ValidationError):
        validate_commit_value(value, "EditCommand")


@pytest.mark.parametrize("read", [
    {"ref": "parent/clip:c", "path": ["at"], "state": {"state": "present", "value": 1}},
    {"ref": "parent/clip:c", "path": "at", "state": {"state": "present", "value": 1}},
    {"ref": "parent/clip:c", "path": ["at"], "state": {"state": "absent", "value": None}},
])
def test_packaged_read_shape_keeps_token_paths_and_presence(read):
    if isinstance(read["path"], list) and read["state"]["state"] == "present":
        validate_commit_value(read, "AgentRead")
    else:
        with pytest.raises(ValidationError):
            validate_commit_value(read, "AgentRead")


def test_public_python_union_types_and_nested_item_references_resolve():
    schema = json.loads((ROOT / "contract/schemas/edit-command.json").read_bytes())
    names = [name for name in schema["$defs"] if name.endswith("Args") or name.startswith("Producer")]
    names += ["ElementRef", "SettledProducerProposal", "WordAnchor"]
    for name in names:
        assert getattr(client, name) is getattr(dto, name)
        assert name in client.__all__
    assert get_type_hints(dto.ClipSetElementArgs)["schema_source"] is dto.DocumentPin
    assert get_type_hints(dto.ProducerGuardArgs)["pin"] is dto.ProducerAttemptPin
    assert get_type_hints(dto.ProducerAttemptPin)["admitted_target"] is dto.ProducerAdmittedTarget
    assert get_type_hints(dto.SettledProducerProposal)["producer"] is dto.ProducerIdentity
    assert get_args(get_type_hints(dto.SettledProducerProposal)["commands"]) == (dto.EditCommand,)
    assert get_args(get_type_hints(dto.EditCommand)["reads"]) == (dto.AgentRead,)
    assert get_args(get_type_hints(dto.AgentRead)["path"]) == (str,)
    assert get_args(get_type_hints(dto.PlacementCreateArgs)["consumed"]) == (str,)
    assert get_type_hints(dto.OccurrenceAddMediaArgs)["row"] is dto.ClipAddArgsRow


@pytest.mark.parametrize("op,select,args", [
    ("placement.create", "occurrence:o", {"id": "c", "on": True, "hold": 1, "media": MEDIA}),
    ("placement.create", "occurrence:o", {"id": "c", "on": 0, "hold": 0, "media": MEDIA}),
    ("placement.create", "occurrence:o", {"id": "c", "on": -1, "hold": 1, "media": MEDIA}),
    ("producer.guard", "parent", {"pin": PIN}),
    ("producer.guard", None, {"pin": {**PIN, "admitted_target": {**TARGET, "timeline_id": " "}}}),
    ("shot.set", "shot:s", {"values": {"name": "Shot"}, "clear": []}),
])
def test_registered_constraints_refuse_invalid_numbers_and_targets(op, select, args):
    with pytest.raises(ValidationError):
        validate_commit_value(command(op, select, args), "EditCommand")


@pytest.mark.parametrize("key,valid", [("parent/clip:c::at", True), ('parent/clip:c::["literal.key"]', True), ("parent/clip:c::at[0]", True), ("parent/clip:c::at[-1]", False), ("parent/clip:c::at[01]", False)])
def test_recorder_target_key_patterns_are_retained(key, valid):
    value = command("clip.move", "parent/clip:c", {"on": 1.5})
    value["expect"] = {key: {"state": "present", "value": 1}}
    if valid:
        validate_commit_value(value, "EditCommand")
    else:
        with pytest.raises(ValidationError):
            validate_commit_value(value, "EditCommand")


def test_s2_only_adds_the_optional_retained_element_document_pin_to_s1():
    s1 = json.loads((ROOT / "tests/fixtures/published-command-schemas/agent-0a0ac7ba.json").read_bytes())
    s2 = json.loads((ROOT / "tests/fixtures/published-command-schemas/agent-26ef2bbb.json").read_bytes())
    before = copy.deepcopy(s2)
    element = s2["$defs"]["ClipSetElementArgs"]
    assert element["properties"].pop("schema_source") == {"$ref": "#/$defs/DocumentPin"}
    element["description"] = s1["$defs"]["ClipSetElementArgs"]["description"]
    assert s2 == s1
    assert before["$defs"]["ClipSetElementArgs"]["required"] == ["elementRef"]


@pytest.mark.parametrize("pin,valid", [
    ({"document_id": "pack", "version": 1, "content_digest": DIGEST}, True),
    ({"document_id": "pack", "version": True, "content_digest": DIGEST}, False),
    ({"document_id": "pack", "version": 1}, False),
    ({"document_id": "pack", "version": 1, "content_digest": DIGEST, "extra": None}, False),
])
def test_element_schema_source_keeps_existing_document_pin_constraints(pin, valid):
    value = command("clip.set-element", "parent/clip:c", {
        "elementRef": {"id": "element", "kind": "component", "revision": "r"}, "schema_source": pin,
    })
    if valid:
        validate_commit_value(value, "EditCommand")
    else:
        with pytest.raises(ValidationError):
            validate_commit_value(value, "EditCommand")
