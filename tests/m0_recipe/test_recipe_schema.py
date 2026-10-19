"""Executable checks for the proposed schema, separate from unported producers."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

SCHEMA = json.loads((Path(__file__).resolve().parents[2] /
                     "schemas/change-contract/edit-command.schema.json").read_text())
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)


def command(op="clip.set", **args):
    return dict(schema_version=1, op=op, version="1", select=None, args=args)


def test_versioned_schema_and_explicit_inverse_restore_targets():
    jsonschema.Draft202012Validator.check_schema(SCHEMA)
    VALIDATOR.validate(command("timeline.inverse", publications=["receipt-a", "receipt-b"]))
    VALIDATOR.validate(command("timeline.restore", revision_id="rev", content_digest="sha256:" + "a" * 64))
    for invalid in (
        command("timeline.inverse", publications=[]),
        command("timeline.inverse", publications=["a", "a"]),
        command("timeline.inverse", group_id="ambiguous"),
        command("timeline.restore", revision_id="rev", content_digest="latest"),
        {**command(), "schema_version": 2},
        {**command(), "unknown": True},
    ):
        with pytest.raises(jsonschema.ValidationError):
            VALIDATOR.validate(invalid)


def test_tagged_presence_and_token_paths_cannot_conflate_null_with_absence():
    leaf = {"$defs": SCHEMA["$defs"], "$ref": "#/$defs/AgentState"}
    validator = jsonschema.Draft202012Validator(leaf)
    for state in ({"state": "absent"}, {"state": "present", "value": None},
                  {"state": "present", "value": {"op": "clear"}}):
        validator.validate(state)
    for invalid in ({"state": "present"}, {"state": "absent", "value": None}):
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(invalid)
    record = dict(ref="parent/clip:c", path=["params", "literal.key"],
                  before={"state": "absent"}, after={"state": "present", "value": None})
    write = jsonschema.Draft202012Validator({"$defs": SCHEMA["$defs"], "$ref": "#/$defs/AgentWrite"})
    write.validate(record)
    with pytest.raises(jsonschema.ValidationError):
        write.validate({**record, "path": "params.literal.key"})
