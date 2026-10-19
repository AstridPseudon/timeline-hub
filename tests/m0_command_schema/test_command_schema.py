"""M0 schema design examples, not provider or product acceptance tests."""

import copy
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

DESIGN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design"
)
SCHEMA = json.loads((DESIGN / "edit-command.schema.json").read_text())
HANDOFF = DESIGN / "command-schema-handoff.md"


def validator(definition="EditCommand"):
    return Draft202012Validator({**SCHEMA, "$ref": f"#/$defs/{definition}"})


def command(op="clip.move", **overrides):
    value = {
        "schema_version": 1,
        "op": op,
        "version": "1",
        "select": "occurrence:opening/clip:title",
        "args": {"on": 2.5},
    }
    if op == "timeline.inverse":
        value.update(select=None, args={"publications": ["txn-a", "txn-b"]})
    elif op == "timeline.restore":
        value.update(
            select=None,
            args={"revision_id": "parent-old", "content_digest": "sha256:" + "a" * 64},
        )
    return {**value, **overrides}


def test_draft_2020_12_and_all_local_references():
    assert SCHEMA["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(SCHEMA)

    def walk(value):
        if isinstance(value, dict):
            if "$ref" in value:
                assert value["$ref"].startswith("#/$defs/")
                assert value["$ref"].removeprefix("#/$defs/") in SCHEMA["$defs"]
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(SCHEMA)


@pytest.mark.parametrize("key", ["schema_version", "op", "version", "select", "args"])
def test_required_wire_fields(key):
    value = command()
    del value[key]
    assert not validator().is_valid(value)


@pytest.mark.parametrize(
    "overrides",
    [
        {"schema_version": 2},
        {"schema_version": True},
        {"version": None},
        {"version": 1},
        {"version": ""},
        {"version": "0.9.0"},
        {"op": "move"},
        {"args": None},
        {"args": {"on": None}},
        {"args": {"on": -1}},
        {"args": {"on": 1, "clear": ["on"]}},
        {"select": "title"},
        {"select": "shot:shared/clip:title"},
        {"reason": "old spelling"},
        {"publisher": "spoofed actor"},
        {"writes": []},
        {"rationale": None},
        {"group_id": ""},
        {"resolved": ["title"]},
        {"created": ["parent/clip:x", "parent/clip:x"]},
        {"created": None},
        {"bindings": {"word": {"id": "parent/clip:x"}}},
        {"expect": {"at": None}},
        {"expect": {"at": {"state": "present"}}},
        {"expect": {"at": {"state": "absent", "value": None}}},
        {"authorship": {"at": "alice"}},
        {"intent": {"ripple": "ripple"}},
        {"intent": {"anchor": "follow"}},
    ],
)
def test_invalid_envelopes_and_minimal_move(overrides):
    assert not validator().is_valid(command(**overrides))


@pytest.mark.parametrize("op", ["timeline.inverse", "timeline.restore"])
def test_history_operations_are_not_selected_or_version_guessed(op):
    assert validator().is_valid(command(op))
    assert not validator().is_valid(command(op, select="parent"))
    assert not validator().is_valid(command(op, version="2"))
    assert not validator().is_valid(command(op, intent={"position": "relative"}))


@pytest.mark.parametrize(
    "args",
    [
        {},
        {"publications": []},
        {"publications": ["txn-a", "txn-a"]},
        {"publications": [""]},
        {"publications": [None]},
        {"publications": ["txn-a"], "group_id": "gesture"},
        {"publication": "txn-a"},
        {"publications": ["txn-a"], "writes": []},
        {"publications": ["txn-a"], "expected_head": "revision"},
    ],
)
def test_inverse_requires_explicit_unique_publications(args):
    assert not validator().is_valid(command("timeline.inverse", args=args))


def test_inverse_preserves_publication_order_without_guessing_ancestry():
    value = command("timeline.inverse")
    original = copy.deepcopy(value)
    validator().validate(value)
    assert value == original
    # Order/ancestry/scope are provider checks against accepted Runtime history.
    value["args"]["publications"].reverse()
    validator().validate(value)


@pytest.mark.parametrize(
    "args",
    [
        {},
        {"revision_id": "old"},
        {"revision_id": "old", "content_digest": "a" * 64},
        {"revision_id": "old", "content_digest": "sha256:" + "A" * 64},
        {"revision_id": "", "content_digest": "sha256:" + "a" * 64},
        {"revision_id": "old", "content_digest": "sha256:" + "a" * 64, "publication_id": "txn"},
        {"revision_id": "old", "content_digest": "sha256:" + "a" * 64, "expected_head": "current"},
        {"revision_id": "old", "content_digest": "sha256:" + "a" * 64, "document": {}},
    ],
)
def test_restore_has_only_exact_historical_pins(args):
    assert not validator().is_valid(command("timeline.restore", args=args))


def test_restore_is_the_sole_command_in_a_batch():
    check = validator("CommandBatch")
    check.validate([command("timeline.restore")])
    assert not check.is_valid([])
    assert not check.is_valid([command(), command("timeline.restore")])
    assert not check.is_valid([command("timeline.restore"), command()])
    check.validate([command(), command("timeline.inverse")])


@pytest.mark.parametrize(
    "path",
    [
        "",
        "params.x",
        "paramsExtra",
        'params["x.y"]',
        "params[0]",
        '["x::y"]',
        'modifiers["fade-in"].params.opacity',
        'app["org.example"].payload',
        'app["quoted\\"key"]',
        'app["line\\nfeed"]',
    ],
)
def test_r4_property_token_paths(path):
    validator("PropertyPath").validate(path)
    validator("TargetKey").validate("occurrence:opening/clip:title::" + path)
    validator("TargetKey").validate(path)


@pytest.mark.parametrize(
    "path",
    [
        ".params",
        "params..x",
        "params[x]",
        "params[-1]",
        "params/0",
        "params[01]",
        "params[01x]",
        'params["bad\nkey"]',
    ],
)
def test_invalid_property_paths(path):
    assert not validator("PropertyPath").is_valid(path)


def test_opaque_objects_and_presence_are_preserved():
    opaque = {"op": "clear", "$absent": True, "nested": [None, {"id": "parent/clip:x"}]}
    value = command(
        "vendor.decorate",
        args={"payload": opaque},
        version="2.4",
        expect={"params": {"state": "present", "value": None}},
        bindings={"clip-start title": "parent/clip:x", "beat 2": "beat:1"},
        authorship={"params": "direct", "at": "consequence"},
        resolved=["parent/clip:x"],
        created=[],
    )
    original = json.loads(json.dumps(value))
    validator().validate(value)
    assert value == original
    validator("AgentState").validate({"state": "absent"})
    validator("AgentState").validate({"state": "present", "value": opaque})


def test_recorder_leaves_keep_unchanged_writes_and_r4_maps():
    state = {"state": "present", "value": None}
    validator("AgentWrite").validate(
        {"ref": "parent/clip:x", "path": ["params"], "before": state, "after": state}
    )
    validator("AgentDerivedWrite").validate(
        {"ref": "parent/clip:x", "path": ["at"], "before": state, "after": state, "cause": 0}
    )
    validator("AgentRead").validate({"ref": "parent", "path": ["config", "app"], "state": state})
    validator("AgentBinding").validate(
        {"key": "beat 2", "ref": "beat:1", "policy": "fixed", "dependencies": ["source"]}
    )
    validator("AgentCreatedID").validate(
        {"ref": "occurrence:opening/clip:x", "kind": "clip", "owner": "occurrence:opening"}
    )
    validator("AgentDependency").validate(
        {"key": "source", "kind": "entity", "pin": {"ref": "parent/clip:music"}, "policy": "exact"}
    )
    validator("AgentSelection").validate(
        {
            "key": "ripple.members",
            "query_version": 1,
            "owner": "parent",
            "members": ["parent/clip:x"],
            "order": ["parent/clip:x"],
            "boundaries": [],
            "policy": "guard-membership",
        }
    )


@pytest.mark.parametrize(
    "definition,value",
    [
        ("AgentRead", {"id": "parent", "path": "config", "state": {"state": "absent"}}),
        ("AgentRead", {"ref": "parent", "path": [0], "state": {"state": "absent"}}),
        ("AgentBinding", {"beat 2": "beat:1"}),
        ("AgentCreatedID", "parent/clip:x"),
        ("AgentCreatedID", {"ref": "parent/clip:x", "kind": "clip", "owner": ""}),
        ("AgentDependency", {"key": "x", "kind": "media", "pin": None, "policy": "exact"}),
        ("AgentDependency", {"key": "x", "kind": "media", "pin": {}, "policy": "latest"}),
        (
            "AgentDerivedWrite",
            {
                "ref": "parent/clip:x",
                "path": ["at"],
                "before": {"state": "absent"},
                "after": {"state": "absent"},
            },
        ),
    ],
)
def test_enriched_recorder_leaves_do_not_replace_old_command_field_types(definition, value):
    assert not validator(definition).is_valid(value)


def handoff_examples():
    pattern = r"<!-- schema: (accept|reject)-(command|batch) -->\s*```json\n(.*?)\n```"
    return [
        (status, kind, json.loads(raw))
        for status, kind, raw in re.findall(pattern, HANDOFF.read_text(), re.S)
    ]


@pytest.mark.parametrize("status,kind,value", handoff_examples())
def test_handoff_json_examples(status, kind, value):
    check = validator("CommandBatch" if kind == "batch" else "EditCommand")
    assert check.is_valid(value) == (status == "accept"), list(check.iter_errors(value))


def test_handoff_has_both_accepted_and_rejected_examples():
    statuses = {status for status, _, _ in handoff_examples()}
    assert statuses == {"accept", "reject"}
