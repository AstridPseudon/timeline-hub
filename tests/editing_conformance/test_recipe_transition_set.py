"""Compact portable goldens for ordinary incoming transition capture."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from astrid.core.element.catalog import list_element_descriptors
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.commands import execute

FIXTURE = Path(__file__).parent / "fixtures" / "recipe_m2_app_transition_set.json"
SOURCE = {
    "commit": "0cfa4ad14664cec9df430637d8f68f2d1f2b487f",
    "operation": "clip.set",
    "capture": "astrid/sdk/timeline/_clip_scalar_commands.py",
}
def transition_bundle(*, initial=None, legacy_ref=False):
    rows = [
        {"id": "predecessor", "track": "picture", "asset": "direct", "at": 0, "hold": 3},
        {"id": "target", "track": "picture", "asset": "direct", "at": 3, "hold": 3},
    ]
    if initial is not None:
        rows[1]["transition"] = copy.deepcopy(initial)
    if legacy_ref:
        rows[1]["element_ref"] = {
            "id": "legacy-transition",
            "kind": "transition",
            "revision": "sha256:" + "e" * 64,
        }
    payload = {
        "clips": copy.deepcopy(rows),
        "config": {
            "clips": copy.deepcopy(rows),
            "opaque_parent_config": {"keep": True},
            "output": {"fps": 30},
            "tracks": [{"id": "picture", "kind": "visual"}],
        },
        "opaque_parent": {"keep": ["all", "fields"]},
        "registry": {"assets": {
            "direct": {"media_id": "sha256:" + "1" * 64},
        }},
    }
    digest = "sha256:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    return {
        "schema_version": 1,
        "project_id": "project-1",
        "timeline_id": "timeline-main",
        "base_parent": {"revision_id": "parent-r1", "content_digest": digest},
        "base_parent_payload": copy.deepcopy(payload),
        "base_placements": {},
        "parent": payload,
        "placements": [],
        "shots": {},
        "source_mapping": {"placements": {}, "shots": {}},
    }


def test_portable_transition_capture_goldens_are_generated_by_the_real_helpers():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture["source"] == SOURCE

    legacy = fixture["cases"]["legacy_update"]
    original = legacy["bundle"]
    command = capture_clip_set(original, legacy["select"], **legacy["capture"])
    plan = execute(original, [command])
    assert command == legacy["command"]
    assert plan.records == legacy["records"]
    assert plan.bundle == legacy["after_bundle"]
    assert execute(original, [legacy["request"]]).commands == [command]
    assert plan.bundle["parent"]["clips"][1]["transition"]["params"] is None

    selected = fixture["cases"]["selected_builtin"]
    selected_bundle = selected["bundle"]
    reference = selected["capture"]["values"]["elementRef"]
    descriptor = next(item for item in list_element_descriptors("transitions")
                      if item["id"] == reference["id"])
    assert reference == {key: descriptor[key] for key in ("id", "kind", "packId", "revision")}
    command = capture_clip_set(selected_bundle, selected["select"],
                               **selected["capture"])
    plan = execute(selected_bundle, [command])
    assert command == selected["command"]
    assert plan.records == selected["records"]
    assert plan.bundle == selected["after_bundle"]
    assert execute(selected_bundle, [selected["request"]]).commands == [command]
    target = plan.bundle["parent"]["clips"][1]
    assert target["transition"]["params"] == {
        "durationFrames": 23,
        "opaque": [None, False, 0, "future"],
    }
    assert "element_ref" not in target

