"""Native sheet/Python goldens and the existing CLI move path share one recipe."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_m1_commands import FIXTURES, inverse
from tests.packs.timeline.test_cli_commit_move import command, sync_connection  # noqa: F401
from tests.sdk.test_timeline_sheet_native import edit_cell, sheet_for
from tests.sdk.test_timeline_sync import initial_bundle


@pytest.mark.parametrize("name", ["move", "occurrence", "shared", "track"])
def test_sheet_and_python_match_exact_portable_goldens(name):
    filename = "recipe_m2_scalar_track.json" if name == "track" else f"recipe_m1_{name}.json"
    fixture = json.loads((FIXTURES / filename).read_text())
    original = copy.deepcopy(fixture["bundle"])
    sheet = sheet_for(original)
    if name == "track":
        edited = edit_cell(sheet.text, fixture["select"], '"Picture"', label=True)
        python_command = capture_track_set(original, fixture["select"], **fixture["args"])
    else:
        edited = edit_cell(sheet.text, fixture["select"], str(fixture["on"]))
        python_command = capture_move(original, fixture["select"], fixture["on"])
    plan = sheet.preview(edited)
    assert plan.commands == [python_command] == [fixture["command"]]
    # JSON spelling as well as Python numeric equality must match the portable fixture.
    assert json.dumps(plan.commands, sort_keys=True) == json.dumps([fixture["command"]], sort_keys=True)
    assert plan.bundle == fixture["after_bundle"]
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original == fixture["bundle"]
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle


def test_cli_python_and_sheet_move_emit_identical_capture(command, capsys):  # noqa: F811
    run, generated = command
    sheet = sheet_for(initial_bundle())
    sheet_commands = sheet.preview(edit_cell(sheet.text, "parent/clip:a", "5")).commands
    assert run("edit", "move", "t", "--project", "p", "--clip", "parent/clip:a",
               "--on", "5", "--dry-run", "--json") == 0
    capsys.readouterr()
    body = json.loads(generated.calls[0][0])
    assert body["commands"] == sheet_commands == [capture_move(initial_bundle(), "parent/clip:a", 5)]
    assert generated.accepted == {}


def test_duplicate_display_names_reordered_rows_use_scoped_binding_and_preserve_unknown_data():
    fixture = json.loads((FIXTURES / "recipe_m1_shared.json").read_text())
    original = fixture["bundle"]
    sheet = sheet_for(original)
    lines = sheet.text.splitlines()
    first = next(i for i, line in enumerate(lines) if '"occurrence:o/clip:c"' in line)
    second = next(i for i, line in enumerate(lines) if '"occurrence:sibling/clip:c"' in line)
    lines[first], lines[second] = lines[second], lines[first]
    reordered = "\n".join(lines) + "\n"
    assert sheet.preview(reordered).commands == []
    plan = sheet.preview(edit_cell(reordered, fixture["select"], str(fixture["on"])))
    assert plan.commands == [fixture["command"]]
    assert plan.bundle == fixture["after_bundle"]
    assert State(plan.bundle).entity("occurrence:o/clip:c") == State(original).entity("occurrence:o/clip:c")


def test_same_sheet_command_rejects_changed_occurrence_map_and_keeps_its_original_guards():
    fixture = json.loads((FIXTURES / "recipe_m1_occurrence.json").read_text())
    original = fixture["bundle"]
    sheet = sheet_for(original)
    plan = sheet.preview(edit_cell(sheet.text, fixture["select"], str(fixture["on"])))
    head = copy.deepcopy(original)
    head["placements"][0]["placement"]["start_ms"] += 1000
    with pytest.raises(CommandError):
        execute(head, plan.commands)
    assert plan.commands == [fixture["command"]]
