from __future__ import annotations

import importlib
import json
import subprocess
from pathlib import Path
from typing import TypedDict, Union, get_args, get_origin, get_type_hints, is_typeddict

import pytest

from generators import generate, timeline_commit_types


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
    assert label_values.__required_keys__ == clear_values.__required_keys__ == set()
    assert label_values.__optional_keys__ == clear_values.__optional_keys__ == {"label", "muted"}
    assert get_type_hints(label_values) == get_type_hints(clear_values) == {"label": str, "muted": bool}
    assert get_type_hints(labeled)["clear"] == get_type_hints(cleared)["clear"]
    assert labeled(values=label_values(label="é 🎬"), clear=[]) == {
        "values": {"label": "é 🎬"}, "clear": []
    }
    assert cleared(values=clear_values(), clear=["label"]) == {
        "values": {}, "clear": ["label"]
    }
    assert labeled(values=label_values(muted=False), clear=[]) == {
        "values": {"muted": False}, "clear": []
    }
    assert cleared(values=clear_values(), clear=["muted"]) == {
        "values": {}, "clear": ["muted"]
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
    namespace = {}
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


def test_typescript_track_label_positive_and_negative_fixtures(tmp_path):
    source = (ROOT / "tests/fixtures/timeline-commit-types.mts").read_text()
    source = source.replace(
        "const noChange: TrackSetArgs = { values: {}, clear: [] };",
        "const noChange: NonEmptyTrackSetArgs = { values: {}, clear: [] };",
    )
    source = source.replace(
        'import type { TrackSetArgs } from "../../packages/typescript/src/timeline-commit-types.js";',
        f'import type {{ TrackSetArgs }} from "{ROOT / "packages/typescript/src/timeline-commit-types.js"}";\n'
        'type NonEmptyTrackSetArgs = TrackSetArgs & (\n'
        '  { values: { label: string } } |\n'
        '  { values: { muted: boolean } } |\n'
        '  { clear: ["label" | "muted", ...Array<"label" | "muted">] }\n'
        ');',
    )
    source += """

const muted: TrackSetArgs = { values: { muted: false }, clear: [] };
const clearMuted: TrackSetArgs = { values: {}, clear: ["muted"] };
const mutedOverlap: TrackSetArgs = { values: { muted: true }, clear: ["label", "muted"] };
// @ts-expect-error Muted remains boolean, not a string or null.
const wrongMuted: TrackSetArgs = { values: { muted: "false" }, clear: [] };
// @ts-expect-error Unknown fields stay closed.
const unknownMutedClear: TrackSetArgs = { values: {}, clear: ["unknown"] };

void [muted, clearMuted, mutedOverlap, wrongMuted, unknownMutedClear];
"""
    source_path = tmp_path / "timeline-commit-types-private016.mts"
    source_path.write_text(source)
    subprocess.run([
        "tsc", "--noEmit", "--strict", "--module", "NodeNext", "--target", "ES2022",
        str(source_path),
    ], check=True)


def test_python_package_root_discovers_new_canonical_args_without_variant_aliases():
    template = (ROOT / "generators/python_client_init_template.py").read_text()
    rendered = generate.render_python_package_init(
        template,
        {"$defs": {
            "TranscriptAssociateArgs": {"type": "object"},
            "NewArgs": {"type": "object"},
            "TranscriptAssociateArgsVariant1": {"type": "object"},
        }},
    )

    assert "    TranscriptAssociateArgs,\n" in rendered
    assert "    NewArgs,\n" in rendered
    assert "TranscriptAssociateArgsVariant1" not in rendered
    assert "'TranscriptAssociateArgs'" in rendered
    assert "'NewArgs'" in rendered


def test_agent_command_source_rejects_malformed_and_unpinned_inputs(tmp_path):
    malformed = tmp_path / "malformed.json"
    malformed.write_bytes(b"{")
    with pytest.raises(SystemExit, match="must be UTF-8 JSON"):
        generate.command_source(malformed)

    unpinned = tmp_path / "unpinned.json"
    unpinned.write_text('{"$defs": {}}')
    with pytest.raises(SystemExit, match="does not match the reviewed private freeze"):
        generate.command_source(unpinned)
