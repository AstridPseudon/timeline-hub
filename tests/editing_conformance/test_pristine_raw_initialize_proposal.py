"""Pure, unregistered spike for a raw-config pristine initializer.

This deliberately bypasses ``operations()`` and the public command schema: the
proposal is not registered.  It exercises only the existing Recording,
serialization, and guarded inverse primitives against the proposed v2 shape.
"""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import ABSENT, CommandError, equal
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from tests.editing_conformance.test_pristine_initialize import empty_document

RAW_CONFIG = {
    "tracks": [],
    "theme_overrides": {
        "visual": {
            "canvas": {"width": 1920, "height": 1080, "fps": 30, "background": None},
            "opaque_visual": {"enabled": False},
        },
        "opaque_theme": [None, False],
    },
    "opaque_sibling": {"literal": "preserve-me"},
}

# These are the known authored structure slots that a pristine initializer may
# carry only in their empty form.  The rest of the open config remains opaque
# JSON: in particular, theme metadata and namespaced arrays are not structure.
EMPTY_STRUCTURAL_PATHS = {
    ("tracks",),
    ("clips",),
    ("occurrences",),
    ("placements",),
    ("shots",),
    ("groups",),
    ("pinnedShotGroups",),
    ("media",),
    ("references",),
    ("reference",),
    ("assets",),
    ("registry", "assets"),
}


def raw_init_command(config=RAW_CONFIG):
    """The proposed closed outer envelope; it is intentionally unregistered."""
    return {
        "schema_version": 1,
        "op": "timeline.init",
        "version": "2",
        "select": "parent",
        "args": {"name": "Custom", "slug": "custom", "config": copy.deepcopy(config)},
    }


def _capture_raw_init_unchecked(bundle, *, config=RAW_CONFIG):
    """Capture the proposal before its empty-structure admission check.

    This is intentionally kept as a test-only counterexample seam: an open
    whole-config write otherwise makes structural births look like metadata.
    """
    command = raw_init_command(config)
    ctx = Recording(copy.deepcopy(bundle), command, 0)
    parent = ctx.read("parent")
    pristine = {"config": {"clips": [], "tracks": []}, "registry": {}, "clips": []}
    if (not equal(parent, pristine) or ctx.state.bundle["placements"]
            or ctx.state.bundle["shots"]):
        raise CommandError("initialization requires the pristine empty timeline", kind="not_pristine")
    ctx.read("parent", ("config",))
    for path in (("name",), ("slug",)):
        if ctx.state.get("parent", path) != ABSENT:
            raise CommandError("initialization field is already authored", kind="not_pristine")
        ctx.read("parent", path)
    ctx.write("parent", ["config"], config)
    ctx.write("parent", ["name"], command["args"]["name"])
    ctx.write("parent", ["slug"], command["args"]["slug"])
    return ctx.finish(capture=True), ctx.state.bundle


def _at_path(config, path):
    value = config
    for token in path:
        if not isinstance(value, dict) or token not in value:
            return ABSENT
        value = value[token]
    return value


def _require_empty_structure(config, record):
    """Reject unrecorded births while retaining arbitrary authored metadata."""
    if record["created"]:
        raise CommandError("raw initialization cannot create structural entities", kind="unrecorded_birth")
    for path in EMPTY_STRUCTURAL_PATHS:
        value = _at_path(config, path)
        if value != ABSENT and value not in ([], {}):
            raise CommandError(
                "nonempty raw initialization structure requires recorded creation facts",
                kind="unrecorded_birth",
                path=path,
            )


def capture_raw_init(bundle, *, config=RAW_CONFIG):
    """Capture only the proposed scoped config/name/slug writes."""
    record, candidate = _capture_raw_init_unchecked(bundle, config=config)
    _require_empty_structure(config, record)
    return record, candidate


def inverse(bundle, records, *, intervening=()):
    command = {
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": ["accepted-raw-init"]},
    }
    return execute(bundle, [command], inverse_records=records, intervening_records=intervening)


def test_raw_init_v2_remains_unregistered():
    with pytest.raises(CommandError):
        validate_command(raw_init_command())


def test_raw_config_roundtrip_reload_and_inverse():
    original = bundle_from_document(empty_document())
    record, initialized = capture_raw_init(original)

    assert [write["path"] for write in record["writes"]] == [["config"], ["name"], ["slug"]]
    assert all(write["ref"] == "parent" for write in record["writes"])
    assert record["command"]["version"] == "2"
    assert record["command"]["args"]["config"] == RAW_CONFIG
    assert initialized["parent"]["config"] == RAW_CONFIG
    assert "background_scale" not in initialized["parent"]["config"]["theme_overrides"]["visual"]["canvas"]

    reloaded = bundle_from_document(document_from_bundle(initialized))
    assert reloaded["parent"]["config"] == RAW_CONFIG
    assert reloaded["parent"]["config"]["theme_overrides"]["opaque_theme"] == [None, False]
    assert list(reloaded["parent"]["config"]["theme_overrides"]["visual"]["canvas"]) == [
        "width", "height", "fps", "background"
    ]
    undone = inverse(reloaded, [record])
    assert (document_from_bundle(undone.bundle)["parent_revision"]["payload"]
            == empty_document()["parent_revision"]["payload"])


@pytest.mark.parametrize(
    "path,value",
    [
        (("tracks",), [{"id": "born-track", "kind": "visual"}]),
        (("clips",), [{"id": "born-clip", "track": "born-track"}]),
        (("groups",), {"group-1": ["born-clip"]}),
        (("media",), {"asset-1": {"media_id": "sha256:born"}}),
        (("references",), {"ref-1": {"target": "born-clip"}}),
        (("registry", "assets"), {"asset-1": {"media_id": "sha256:born"}}),
    ],
)
def test_open_config_would_smuggle_unrecorded_structural_births(path, value):
    """The risk is real unless the proposed carrier applies the empty boundary."""
    config = copy.deepcopy(RAW_CONFIG)
    node = config
    for token in path[:-1]:
        node[token] = {}
        node = node[token]
    node[path[-1]] = value

    original = bundle_from_document(empty_document())
    unchecked_record, unchecked = _capture_raw_init_unchecked(original, config=config)
    assert unchecked["parent"]["config"][path[0]]
    assert unchecked_record["created"] == []
    assert not any(read["ref"].startswith("parent/") for read in unchecked_record["reads"])

    with pytest.raises(CommandError) as error:
        capture_raw_init(original, config=config)
    assert error.value.kind == "unrecorded_birth"


def test_raw_init_refuses_nonpristine_and_any_later_edit():
    original = bundle_from_document(empty_document())
    changed = copy.deepcopy(original)
    changed["parent"]["registry"]["opaque"] = [None, False]
    with pytest.raises(CommandError) as error:
        capture_raw_init(changed)
    assert error.value.kind == "not_pristine"

    record, initialized = capture_raw_init(original)
    with pytest.raises(CommandError) as error:
        capture_raw_init(initialized)
    assert error.value.kind == "not_pristine"

    later = capture_track_create(initialized, "parent", {"id": "later", "kind": "visual"})
    later_plan = execute(initialized, [later])
    with pytest.raises(CommandError) as error:
        inverse(later_plan.bundle, [record], intervening=later_plan.records)
    assert error.value.kind == "intervening_write"
