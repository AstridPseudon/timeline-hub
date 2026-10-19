"""Portable App authoring-bundle goldens for native parent add and params edits."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import ABSENT, State, present
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse

FIXTURES = Path(__file__).parent / "fixtures"
ADD_FIXTURE = FIXTURES / "recipe_m2_app_clip_add.json"
PARAMS_FIXTURE = FIXTURES / "recipe_m2_app_clip_params.json"
SOURCE = "src/tools/video-editor/commands/fixtures/authoringBundle.json"
SCHEMA = json.loads(
    (Path(__file__).parents[2] / "astrid/core/timeline/schema/edit-command.schema.json").read_text()
)
PARENT_CLIP = {
    "id": "parent-clip",
    "track": "picture",
    "at": 1,
    "hold": 2,
    "app": {"on": None, "opaque": {"absent_sibling": [None, False, 0]}},
}
ADD_ROW = {
    "id": "app-hold-clip",
    "clipType": "hold",
    "track": "picture",
    "at": 3,
    "hold": 1.5,
    "params": {"empty": "", "null": None, "opaque": {"literal": [None, False, 0]}},
    "app": {
        "astrid": {"on": None, "opaque": {"added": [None, False, 0]}},
        "future": False,
    },
    "nullable": None,
    "sourceURL": None,
    "from": None,
    "opaque": {"id": "app-hold-clip", "ordered": [None, False, 0, {}, []]},
}


def _canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _assert_exact_app_source(bundle, fixture):
    """Keep the golden tied to the complete App parent-only closure."""
    assert fixture["source"] == SOURCE
    assert fixture["app_case"] == "parent-only"
    assert bundle["project_id"] == "project-main"
    assert bundle["timeline_id"] == "timeline-main"
    assert bundle["base_parent"] == {
        "revision_id": "parent-r1",
        "content_digest": "sha256:9f5ecaaac8431a4bdbf7e072461412360efbc00ffe56f68f5415dfa4faa64f44",
    }
    assert bundle["parent"]["config"]["tracks"] == [
        {"id": "picture", "kind": "visual", "extension": {"clear": None}}
    ]
    assert bundle["parent"]["clips"] == [PARENT_CLIP]
    assert bundle["parent"]["config"]["clips"] == [PARENT_CLIP]
    assert bundle["parent"]["registry"] == {
        "assets": {
            "media": {
                "object_id": "sha256:" + "a" * 64,
                "media_type": "video/mp4",
            }
        }
    }
    assert bundle["parent"]["unknown"] == {"opaque": [None, {"keep": True}], "number": 1.25}
    runtime = bundle["source_mapping"]["_runtime_document"]
    assert runtime["parent_revision"]["payload"]["unknown"] == bundle["parent"]["unknown"]
    assert hashlib.sha256(_canonical_bytes(runtime)).hexdigest() == fixture["source_runtime_document_sha256"]


def _assert_source_unchanged(before, after):
    before_runtime = before["source_mapping"]["_runtime_document"]
    after_runtime = after["source_mapping"]["_runtime_document"]
    assert _canonical_bytes(after_runtime) == _canonical_bytes(before_runtime)
    assert after["source_mapping"] == before["source_mapping"]
    assert after["base_parent"] == before["base_parent"]
    assert after["base_parent_payload"] == before["base_parent_payload"]
    assert after["base_placements"] == before["base_placements"]
    assert after["placements"] == before["placements"]
    assert after["shots"] == before["shots"]


def test_app_parent_hold_clip_add_golden_is_exact_and_portable():
    fixture = json.loads(ADD_FIXTURE.read_text())
    original = fixture["bundle"]
    _assert_exact_app_source(original, fixture)
    assert fixture["input"]["row"] == ADD_ROW
    assert State(original).get("parent/clip:app-hold-clip", []) == ABSENT

    command = capture_clip_add(original, fixture["select"], fixture["input"]["row"])
    plan = execute(original, [command])

    assert fixture["request"]["args"] == {"row": ADD_ROW}
    assert command == fixture["command"]
    assert execute(original, [fixture["request"]]).commands == [command]
    assert plan.commands == [fixture["command"]]
    assert plan.bundle == fixture["after_bundle"]
    assert command["created"] == ["parent/clip:app-hold-clip"]
    assert State(plan.bundle).entity("parent/clip:app-hold-clip") == ADD_ROW
    assert State(plan.bundle).collection("parent", "clip") == [PARENT_CLIP, ADD_ROW]
    assert plan.bundle["parent"]["config"]["clips"] == [PARENT_CLIP, ADD_ROW]
    assert plan.bundle["parent"]["registry"] == original["parent"]["registry"]
    assert plan.bundle["parent"]["unknown"] == original["parent"]["unknown"]
    _assert_source_unchanged(original, plan.bundle)
    assert inverse(plan.bundle, plan.records).bundle == original
    assert replay(plan, original).bundle == plan.bundle
    json.dumps(command, allow_nan=False)
    Draft202012Validator(SCHEMA).validate(command)


@pytest.mark.parametrize("name", ["set", "null"])
def test_app_parent_clip_params_golden_preserves_exact_presence_and_pins(name):
    fixture = json.loads(PARAMS_FIXTURE.read_text())
    case = fixture["cases"][name]
    original = fixture["bundle"]
    _assert_exact_app_source(original, fixture)
    assert State(original).get("parent/clip:parent-clip", ["params"]) == ABSENT
    assert case["before"] == {"state": "absent"}

    command = capture_clip_set_params(original, case["select"], **case["capture"])
    plan = execute(original, [command])

    assert case["request"]["args"] == command["args"]
    assert command == case["command"]
    assert execute(original, [case["request"]]).commands == [command]
    assert plan.bundle == case["after_bundle"]
    assert State(plan.bundle).entity("parent/clip:parent-clip")["params"] == case["expected_params"]
    assert State(plan.bundle).entity("parent/clip:parent-clip")["app"] == PARENT_CLIP["app"]
    assert plan.bundle["parent"]["clips"][0]["params"] == case["expected_params"]
    assert plan.bundle["parent"]["config"]["clips"][0]["params"] == case["expected_params"]
    _assert_source_unchanged(original, plan.bundle)
    assert inverse(plan.bundle, plan.records).bundle == original
    assert replay(plan, original).bundle == plan.bundle
    Draft202012Validator(SCHEMA).validate(command)


def test_app_parent_clip_params_explicit_clear_keeps_empty_container_and_exact_inverse():
    fixture = json.loads(PARAMS_FIXTURE.read_text())
    case = fixture["cases"]["explicit_clear"]
    original = case["bundle"]
    source = fixture["bundle"]
    _assert_exact_app_source(source, fixture)
    assert original["source_mapping"] == source["source_mapping"]
    assert State(original).get("parent/clip:parent-clip", ["params"]) == present({"null": None})

    command = capture_clip_set_params(original, case["select"], **case["capture"])
    plan = execute(original, [command])

    assert command == case["command"]
    assert execute(original, [case["request"]]).commands == [command]
    assert plan.bundle == case["after_bundle"]
    assert State(plan.bundle).entity("parent/clip:parent-clip")["params"] == {}
    assert "null" not in State(plan.bundle).entity("parent/clip:parent-clip")["params"]
    _assert_source_unchanged(source, plan.bundle)
    assert inverse(plan.bundle, plan.records).bundle == original
    assert replay(plan, original).bundle == plan.bundle
    Draft202012Validator(SCHEMA).validate(command)


def test_app_parent_clip_params_golden_has_closed_args_and_stable_null_empty_clear_edges():
    fixture = json.loads(PARAMS_FIXTURE.read_text())
    assert fixture["cases"]["set"]["capture"] == {"values": {"empty": ""}, "clear": []}
    assert fixture["cases"]["null"]["capture"] == {"values": {"null": None}, "clear": []}
    assert fixture["cases"]["explicit_clear"]["capture"] == {"values": {}, "clear": ["null"]}
    for case in fixture["cases"].values():
        assert set(case["request"]) == {"schema_version", "op", "version", "select", "args"}
        assert set(case["request"]["args"]) == {"values", "clear"}
        assert case["request"]["op"] == "clip.set-params"
        assert case["command"]["created"] == []
