"""Draft 2020-12 coverage for the canonical shot-root reference spellings."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import validate_command

SCHEMA = json.loads(
    (Path(__file__).parents[2] / "astrid/core/timeline/schema/edit-command.schema.json").read_text()
)


def validator(definition: str) -> Draft202012Validator:
    return Draft202012Validator({"$defs": SCHEMA["$defs"], "$ref": f"#/$defs/{definition}"})


@pytest.mark.parametrize(
    ("definition", "value"),
    [
        ("ScopedId", "shot:shot-1"),
        ("EntityRef", "shot:shot-1"),
        ("AnchorIdentity", "shot:shot-1"),
        ("TargetKey", "shot:shot-1::"),
        ("TargetKey", "shot:shot-1::payload.metadata"),
    ],
)
def test_shot_root_refs_admit_root_and_empty_root_path(definition: str, value: str) -> None:
    validator(definition).validate(value)


@pytest.mark.parametrize("definition", ["ScopedId", "EntityRef", "AnchorIdentity"])
@pytest.mark.parametrize("value", ["shot:", "shot:shot/child", "shot:shot::other"])
def test_shot_root_ids_reject_empty_slash_and_ambiguous_ids(
    definition: str, value: str
) -> None:
    assert not validator(definition).is_valid(value)


@pytest.mark.parametrize(
    "value",
    ["shot:", "shot:shot/child::", "shot:shot::path::again", "shot::", "::"],
)
def test_shot_root_target_keys_reject_malformed_closed_forms(value: str) -> None:
    assert not validator("TargetKey").is_valid(value)


def test_sealed_group_wire_envelope_admits_shot_root_facts() -> None:
    """The root-bearing command shape is from the sealed a0dad5fc fixture.

    This checks the wire envelope only. The migration operation remains unknown to
    this branch's registry and therefore has no handler or Runtime acceptance claim.
    """
    command = json.loads(
        (Path(__file__).parent / "fixtures/recipe_m2_group_migration_command.json").read_text()
    )

    Draft202012Validator(SCHEMA).validate(command)
    with pytest.raises(CommandError, match="unsupported operation"):
        validate_command(command)


def test_original_m1_envelopes_remain_schema_valid() -> None:
    fixtures = Path(__file__).parent / "fixtures"
    for name in ("recipe_m1_move.json", "recipe_m1_occurrence.json", "recipe_m1_shared.json"):
        fixture = json.loads((fixtures / name).read_text())
        Draft202012Validator(SCHEMA).validate(fixture["command"])


def test_unknown_operation_schema_is_general_but_registry_meaning_is_separate() -> None:
    command = {
        "schema_version": 1,
        "op": "timeline.provider-defined",
        "version": "future",
        "select": "shot:shot-1",
        "args": {"opaque": {"shot": "shot:shot-1", "root": {"empty": True}}},
    }

    Draft202012Validator(SCHEMA).validate(command)
    with pytest.raises(CommandError, match="unsupported operation"):
        validate_command(command)
