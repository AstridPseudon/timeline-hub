from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import TypedDict, Union, get_args, get_origin, get_type_hints, is_typeddict

import pytest

from generators import timeline_commit_types


ROOT = Path(__file__).resolve().parents[1]


def union_members(alias, namespace):
    holder = TypedDict("Holder", {"args": alias})
    resolved = get_type_hints(holder, namespace)["args"]
    assert get_origin(resolved) is Union
    members = get_args(resolved)
    assert all(is_typeddict(member) for member in members)
    return members


@pytest.mark.parametrize(
    "module_name",
    ["runtime_protocol.timeline_commit_types", "astrid_runtime_client.timeline_commit_types"],
)
def test_track_label_union_imports_and_retains_field_types(module_name):
    dto = importlib.import_module(module_name)
    labeled, cleared = union_members(dto.TrackSetArgs, vars(dto))
    for branch in (labeled, cleared):
        assert branch.__required_keys__ == {"values", "clear"}
        assert branch.__optional_keys__ == set()
    label_values = get_type_hints(labeled)["values"]
    clear_values = get_type_hints(cleared)["values"]
    assert label_values.__required_keys__ == {"label"}
    assert label_values.__optional_keys__ == set()
    assert clear_values.__required_keys__ == set()
    assert clear_values.__optional_keys__ == {"label"}
    assert get_type_hints(label_values) == get_type_hints(clear_values) == {"label": str}
    assert labeled(values=label_values(label="é 🎬"), clear=[]) == {
        "values": {"label": "é 🎬"}, "clear": []
    }
    assert cleared(values=clear_values(), clear=["label"]) == {
        "values": {}, "clear": ["label"]
    }


@pytest.mark.parametrize("keyword", ["oneOf", "anyOf"])
def test_object_unions_keep_shared_and_branch_required_fields(tmp_path, monkeypatch, keyword):
    schemas = tmp_path / "contract/schemas"
    schemas.mkdir(parents=True)
    (schemas / "timeline-commit.json").write_text(json.dumps({"$defs": {}}))
    (schemas / "edit-command.json").write_text(json.dumps({"$defs": {
        "ChangeArgs": {
            "type": "object",
            "properties": {"target": {"type": "string"}},
            "required": ["target"],
            keyword: [
                {"properties": {"target": {}, "value": {"type": "string"}, "note": {"type": "string"}},
                 "required": ["value"], "additionalProperties": False},
                {"properties": {"target": {}, "clear": {"const": "value"}},
                 "required": ["clear"], "additionalProperties": False},
            ],
        },
    }}))
    openapi = tmp_path / "contract/openapi"
    openapi.mkdir()
    (openapi / "workspace-v1.yaml").write_text(json.dumps({"components": {"schemas": {
        "CommittedMutation": {"properties": {"receipt": {"type": "object"}}},
    }}}))
    monkeypatch.setattr(timeline_commit_types, "ROOT", tmp_path)
    outputs = timeline_commit_types.render()
    module = ModuleType("isolated_commit_dtos")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    namespace = vars(module)
    exec(outputs["runtime_protocol/timeline_commit_types.py"], namespace)
    set_value, clear_value = union_members(namespace["ChangeArgs"], namespace)
    assert set_value.__required_keys__ == {"target", "value"}
    assert set_value.__optional_keys__ == {"note"}
    assert clear_value.__required_keys__ == {"target", "clear"}
    assert clear_value.__optional_keys__ == set()
    assert get_type_hints(set_value, namespace) == {
        "target": str, "value": str, "note": str,
    }
    source = tmp_path / "generic.mts"
    source.write_text(outputs["packages/typescript/src/timeline-commit-types.ts"] + """
const setValue: ChangeArgs = { target: "t", value: "", note: "optional" };
const clearValue: ChangeArgs = { target: "t", clear: "value" };
// @ts-expect-error Shared required field is missing.
const missingTarget: ChangeArgs = { value: "x" };
// @ts-expect-error Neither branch has its required field.
const missingBranch: ChangeArgs = { target: "t", note: "optional" };
// @ts-expect-error Closed branches reject unrelated fields.
const unknownField: ChangeArgs = { target: "t", value: "x", extra: true };
""")
    subprocess.run(["tsc", "--noEmit", "--strict", "--target", "ES2022", str(source)], check=True)


def test_typescript_track_label_positive_and_negative_fixtures():
    subprocess.run([
        "tsc", "--noEmit", "--strict", "--module", "NodeNext", "--target", "ES2022",
        str(ROOT / "tests/fixtures/timeline-commit-types.mts"),
    ], check=True)


@pytest.mark.parametrize(
    "module_name",
    ["runtime_protocol.timeline_commit_types", "astrid_runtime_client.timeline_commit_types"],
)
def test_registered_command_union_preserves_every_source_branch(module_name):
    dto = importlib.import_module(module_name)
    schema = json.loads((ROOT / "contract/schemas/edit-command.json").read_text())
    for name in schema["$defs"]:
        assert hasattr(dto, name), name
    members = union_members(dto.EditCommand, vars(dto))
    expected = []
    for clause in schema["$defs"]["EditCommand"]["allOf"]:
        op = clause["if"]["properties"]["op"]["const"]
        then = clause["then"]
        for branch in then.get("anyOf", [then]):
            expected.append((op, branch["properties"]))
    assert len(members) == len(expected) == 41
    assert len({op for op, _ in expected}) == 29
    for member, (op, properties) in zip(members, expected):
        hints = get_type_hints(member)
        assert get_args(hints["op"]) == (op,)
        version = properties.get("version", {}).get("const")
        assert get_args(hints["version"]) == ((version,) if version else ())
        if version is None:
            assert hints["version"] is str
        name = properties["args"]["$ref"].rsplit("/", 1)[1]
        holder = TypedDict("Holder", {"args": getattr(dto, name)})
        assert hints["args"] == get_type_hints(holder, vars(dto))["args"]
        assert member.__required_keys__ == {"schema_version", "op", "version", "select", "args"}
        assert get_args(hints["reads"]) == (dto.AgentRead,)
    delete = next(member for member in members if get_args(get_type_hints(member)["op"]) == ("clip.delete",))
    delete_intent = get_type_hints(delete, vars(dto))["intent"]
    assert is_typeddict(delete_intent)
    assert get_type_hints(delete_intent) == {}
    assert delete_intent.__required_keys__ == set()
    assert delete_intent.__optional_keys__ == set()
    text, clear = union_members(dto.TextBindingSetArgs, vars(dto))
    assert text.__required_keys__ == {"binding", "text"}
    assert clear.__required_keys__ == {"binding", "clear"}
    for branch in (text, clear):
        assert set(get_type_hints(branch)) == {"binding", "text", "clear"}


def test_typescript_registered_command_versions_args_and_public_exports():
    subprocess.run([
        "tsc", "--noEmit", "--strict", "--module", "NodeNext", "--target", "ES2022",
        str(ROOT / "tests/fixtures/timeline-current-union-types.mts"),
    ], check=True)
