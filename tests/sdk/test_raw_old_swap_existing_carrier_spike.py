"""Executable source-only spike for a future raw-OLD media swap.

This file intentionally does not register an operation or change the command
schema.  It models the smallest closed successor at the existing Agent/Runtime
read boundary while the Runtime/App pair is still awaiting ACK.

The current floor is important here: v1 uses two five-field selections, and
occurrence.swap-media@2 is already the source-bound materialization variant.
The proposed raw-OLD widening therefore leaves those captures untouched and
would use clip.swap-media@2 and occurrence.swap-media@3 only after paired
review.  Those future versions are not registered by this spike.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass

import pytest

from astrid.sdk.timeline._materialization import SOURCE_BOUND_OPERATIONS
from astrid.sdk.timeline.commands import _SCHEMA

OLD_MEDIA = {
    "media_id": "sha256:" + "a" * 64,
    "content_digest": "sha256:" + "a" * 64,
}
NEW_MEDIA = {
    "asset": "new-key",
    "generation_id": "generation-new",
    "variant_id": "variant-new",
    "object_id": "sha256:" + "b" * 64,
    "catalog_digest": "sha256:" + "c" * 64,
}

FUTURE_VERSIONS = {"clip.swap-media": "2", "occurrence.swap-media": "3"}


def _new_registry_binding(selection, media_type):
    return {
        "media_id": selection["object_id"],
        "type": media_type,
        "generationId": selection["generation_id"],
        "variantId": selection["variant_id"],
    }


def _operation_versions(op):
    return {
        branch["properties"]["version"]["const"]
        for condition in _SCHEMA["$defs"]["EditCommand"]["allOf"]
        if condition["if"]["properties"]["op"].get("const") == op
        for branch in condition["then"].get("anyOf", [condition["then"]])
    }


@dataclass
class FakeMediaPort:
    """Custody boundary fake; intrinsic metadata is never caller input."""

    old_info: dict
    new_info: dict
    raw_reads: int = 0
    selected_reads: int = 0

    def raw_media_info(self, pin):
        self.raw_reads += 1
        if pin != OLD_MEDIA:
            raise ValueError("raw pin is not request-owned")
        return copy.deepcopy(self.old_info)

    def selected_media(self, selection):
        self.selected_reads += 1
        if selection != NEW_MEDIA:
            raise ValueError("new selection is not Runtime-verified")
        return copy.deepcopy(self.new_info)


def _port(*, old_duration=6, new_duration=6, old_type="video", new_type="video"):
    return FakeMediaPort(
        old_info={
            "object_id": OLD_MEDIA["media_id"],
            "media_type": old_type,
            "size": 9,
            "duration_seconds": old_duration,
        },
        new_info={
            "object_id": NEW_MEDIA["object_id"],
            "media_type": new_type,
            "size": 10,
            "duration_seconds": new_duration,
        },
    )


def _state():
    return {
        "base": ("revision-1", "publication-1"),
        "write_epoch": 0,
        "clips": {
            "parent/clip:raw-1": {
                "asset": "old-key",
                "clipType": "video",
                "at": 1,
                "from": 2,
                "to": 6,
                "hold": 4,
                "speed": 1,
                "opaque": {"keep": [None, False, "clip"]},
            },
            "parent/clip:sibling": {
                "asset": "old-key",
                "at": 8,
                "opaque": {"keep": "sibling"},
            },
            "occurrence:occ-1/clip:raw-2": {
                "asset": "occ-old",
                "clipType": "video",
                "at": 1,
                "from": 2,
                "to": 6,
                "hold": 4,
                "speed": 1,
                "opaque": {"keep": "occurrence"},
            },
        },
        "registry": {
            "parent/asset:old-key": copy.deepcopy(OLD_MEDIA),
            "occurrence:occ-1/asset:occ-old": copy.deepcopy(OLD_MEDIA),
        },
    }


def _future_command(*, owner, clip_id, old_media=OLD_MEDIA, media=NEW_MEDIA):
    """Build the proposed existing-envelope widening, without registration."""
    operation = "clip.swap-media" if owner == "parent" else "occurrence.swap-media"
    return {
        "schema_version": 1,
        "op": operation,
        "version": FUTURE_VERSIONS[operation],
        "select": f"{owner}/clip:{clip_id}",
        "args": {
            # OLD deliberately reuses the existing two-field manifest entry;
            # NEW remains the existing five-field selected-media envelope.
            "old_media": copy.deepcopy(old_media),
            "media": copy.deepcopy(media),
        },
        "intent": {"ownership": "parent" if owner == "parent" else "occurrence"},
    }


def _raw_old_swap(
    state,
    port,
    *,
    owner,
    clip_id,
    old_alias,
    old_media,
    new_media,
    affected_members,
    original_base,
):
    """Model the closed future widening; this is not product command code."""
    target = f"{owner}/clip:{clip_id}"
    old_ref = f"{owner}/asset:{old_alias}"
    new_ref = f"{owner}/asset:{new_media['asset']}"
    expected_members = [target, old_ref, new_ref]

    # These are the original guards the real recorder must capture.  They are
    # checked before any write, including a NEW alias birth.
    if original_base != state["base"]:
        raise ValueError("original base guard changed")
    if not (
        owner == "parent"
        or (re.fullmatch(r"occurrence:(?!.*::)[^/]+", owner) is not None)
    ):
        raise ValueError("raw owner must be explicit and authored")
    if target not in state["clips"]:
        raise ValueError("raw clip is missing")
    if affected_members != expected_members:
        raise ValueError("affected member scope is not exact")

    row = state["clips"][target]
    if row["asset"] != old_alias:
        raise ValueError("old alias is not the selected clip binding")
    if set(old_media) != {"media_id", "content_digest"} or old_media != OLD_MEDIA:
        raise ValueError("OLD media must be the existing manifest entry")
    if state["registry"].get(old_ref) != old_media:
        raise ValueError("OLD alias binding changed")

    old_info = port.raw_media_info(old_media)
    new_info = port.selected_media(new_media)
    if old_info["object_id"] != old_media["media_id"]:
        raise ValueError("raw media identity changed")
    if new_info["object_id"] != new_media["object_id"]:
        raise ValueError("new media identity changed")
    if old_info["media_type"] != new_info["media_type"]:
        raise ValueError("media kind changed")
    if row["to"] - row["from"] != row["hold"]:
        raise ValueError("authored source window differs from hold")
    if row["to"] > old_info["duration_seconds"] or row["to"] > new_info["duration_seconds"]:
        raise ValueError("authored source window exceeds intrinsic media")

    before = copy.deepcopy(state)
    existing_new = state["registry"].get(new_ref)
    expected_new = _new_registry_binding(new_media, new_info["media_type"])
    if existing_new is not None and existing_new != expected_new:
        raise ValueError("NEW alias is occupied by a different binding")
    if existing_new is None:
        state["registry"][new_ref] = expected_new
    state["clips"][target]["asset"] = new_media["asset"]
    state["write_epoch"] += 1
    after = copy.deepcopy(state)

    def undo(current):
        if current["write_epoch"] != after["write_epoch"] or current != after:
            raise ValueError("inverse guard changed, including ABA")
        current.clear()
        current.update(copy.deepcopy(before))

    return undo


def test_existing_versions_are_untouched_and_future_versions_are_unregistered():
    assert _operation_versions("clip.swap-media") == {"1"}
    assert _operation_versions("occurrence.swap-media") == {"1", "2"}
    assert "occurrence.swap-media" in SOURCE_BOUND_OPERATIONS
    assert "clip.swap-media" not in SOURCE_BOUND_OPERATIONS
    assert FUTURE_VERSIONS == {"clip.swap-media": "2", "occurrence.swap-media": "3"}


def test_future_envelope_has_raw_manifest_old_and_exact_selected_new_only():
    command = _future_command(owner="parent", clip_id="raw-1")
    assert command["args"]["old_media"] == OLD_MEDIA
    assert set(command["args"]["old_media"]) == {"media_id", "content_digest"}
    assert command["args"]["media"] == NEW_MEDIA
    assert set(command["args"]["media"]) == {
        "asset", "generation_id", "variant_id", "object_id", "catalog_digest"
    }
    assert "owner" not in command["args"]
    assert "duration_seconds" not in command["args"]["old_media"]


def test_raw_old_swap_parent_preserves_sibling_opaque_window_and_old_alias():
    state = _state()
    before_sibling = copy.deepcopy(state["clips"]["parent/clip:sibling"])
    before_window = {
        key: state["clips"]["parent/clip:raw-1"][key]
        for key in ("at", "from", "to", "hold", "speed", "opaque")
    }
    port = _port()
    undo = _raw_old_swap(
        state,
        port,
        owner="parent",
        clip_id="raw-1",
        old_alias="old-key",
        old_media=OLD_MEDIA,
        new_media=NEW_MEDIA,
        affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        original_base=("revision-1", "publication-1"),
    )

    row = state["clips"]["parent/clip:raw-1"]
    assert row["asset"] == "new-key"
    assert {key: row[key] for key in before_window} == before_window
    assert state["clips"]["parent/clip:sibling"] == before_sibling
    assert state["registry"]["parent/asset:old-key"] == OLD_MEDIA
    assert state["registry"]["parent/asset:new-key"] == _new_registry_binding(NEW_MEDIA, "video")
    assert (port.raw_reads, port.selected_reads) == (1, 1)

    undo(state)
    assert state == _state()


def test_raw_old_swap_occurrence_isolated_and_create_or_require_accepts_equal_new_alias():
    state = _state()
    state["registry"]["occurrence:occ-1/asset:new-key"] = _new_registry_binding(NEW_MEDIA, "video")
    before_parent = copy.deepcopy(state["clips"]["parent/clip:raw-1"])
    undo = _raw_old_swap(
        state,
        _port(),
        owner="occurrence:occ-1",
        clip_id="raw-2",
        old_alias="occ-old",
        old_media=OLD_MEDIA,
        new_media=NEW_MEDIA,
        affected_members=[
            "occurrence:occ-1/clip:raw-2",
            "occurrence:occ-1/asset:occ-old",
            "occurrence:occ-1/asset:new-key",
        ],
        original_base=("revision-1", "publication-1"),
    )

    assert state["clips"]["occurrence:occ-1/clip:raw-2"]["asset"] == "new-key"
    assert state["clips"]["parent/clip:raw-1"] == before_parent
    assert "parent/asset:new-key" not in state["registry"]
    undo(state)
    state["registry"].pop("occurrence:occ-1/asset:new-key")
    assert state == _state()


@pytest.mark.parametrize(
    "change",
    [
        {"owner": "occurrence:display::not-an-owner", "clip_id": "raw-1"},
        {"owner": "parent", "clip_id": "raw-1", "affected_members": ["parent/clip:raw-1"]},
        {"owner": "parent", "clip_id": "sibling", "old_alias": "old-key"},
    ],
)
def test_raw_old_swap_refuses_ambiguous_owner_or_global_fanout_without_writes(change):
    state = _state()
    before = copy.deepcopy(state)
    args = {
        "owner": "parent",
        "clip_id": "raw-1",
        "old_alias": "old-key",
        "old_media": OLD_MEDIA,
        "new_media": NEW_MEDIA,
        "affected_members": ["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        "original_base": ("revision-1", "publication-1"),
    }
    args.update(change)
    with pytest.raises(ValueError):
        _raw_old_swap(state, _port(), **args)
    assert state == before


@pytest.mark.parametrize("failure", ["caller-old-metadata", "old-window", "kind", "raw-read", "new-read"])
def test_raw_old_swap_invalid_source_refuses_before_any_write(failure):
    state = _state()
    before = copy.deepcopy(state)
    port = _port(old_duration=3 if failure == "old-window" else 6,
                 new_type="image" if failure == "kind" else "video")
    old_media = {**OLD_MEDIA, "duration_seconds": 999} if failure == "caller-old-metadata" else OLD_MEDIA
    if failure == "raw-read":
        port.old_info["object_id"] = "sha256:" + "d" * 64
    if failure == "new-read":
        port.new_info["object_id"] = "sha256:" + "e" * 64
    with pytest.raises(ValueError):
        _raw_old_swap(
            state,
            port,
            owner="parent",
            clip_id="raw-1",
            old_alias="old-key",
            old_media=old_media,
            new_media=NEW_MEDIA,
            affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
            original_base=("revision-1", "publication-1"),
        )
    assert state == before


def test_raw_old_swap_rejects_conflicting_new_alias_without_writes():
    state = _state()
    state["registry"]["parent/asset:new-key"] = {"media_id": "different"}
    before = copy.deepcopy(state)
    with pytest.raises(ValueError, match="NEW alias"):
        _raw_old_swap(
            state,
            _port(),
            owner="parent",
            clip_id="raw-1",
            old_alias="old-key",
            old_media=OLD_MEDIA,
            new_media=NEW_MEDIA,
            affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
            original_base=("revision-1", "publication-1"),
        )
    assert state == before


def test_raw_old_swap_inverse_detects_aba_even_when_state_returns_equal():
    state = _state()
    undo = _raw_old_swap(
        state,
        _port(),
        owner="parent",
        clip_id="raw-1",
        old_alias="old-key",
        old_media=OLD_MEDIA,
        new_media=NEW_MEDIA,
        affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        original_base=("revision-1", "publication-1"),
    )
    state["clips"]["parent/clip:raw-1"]["asset"] = "old-key"
    state["write_epoch"] += 1
    state["clips"]["parent/clip:raw-1"]["asset"] = "new-key"
    with pytest.raises(ValueError, match="ABA"):
        undo(state)
