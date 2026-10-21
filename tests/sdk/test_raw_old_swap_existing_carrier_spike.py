"""Executable boundary spike for a raw OLD media binding in a future swap v2.

This is deliberately test-only.  It does not register an EditCommand or alter
the frozen v1 schema.  The fake port stands in for the reviewed Runtime
``raw_media_info`` / existing ``selected_media`` boundary.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass

import pytest

OLD_PIN = {
    "media_id": "sha256:" + "a" * 64,
    "content_digest": "sha256:" + "a" * 64,
}
NEW_SELECTION = {
    "asset": "new-key",
    "generation_id": "generation-new",
    "variant_id": "variant-new",
    "object_id": "sha256:" + "b" * 64,
    "catalog_digest": "sha256:" + "c" * 64,
}


def _new_registry_binding(selection, media_type):
    return {
        "media_id": selection["object_id"],
        "type": media_type,
        "generationId": selection["generation_id"],
        "variantId": selection["variant_id"],
    }


@dataclass
class FakeMediaPort:
    """Small custody boundary fake; callers cannot provide intrinsic metadata."""

    old_info: dict
    new_info: dict
    raw_reads: int = 0
    selected_reads: int = 0

    def raw_media_info(self, pin):
        self.raw_reads += 1
        if pin != OLD_PIN:
            raise ValueError("raw pin is not request-owned")
        return copy.deepcopy(self.old_info)

    def selected_media(self, selection):
        self.selected_reads += 1
        if selection != NEW_SELECTION:
            raise ValueError("new selection is not Runtime-verified")
        return copy.deepcopy(self.new_info)


def _port():
    return FakeMediaPort(
        old_info={
            "object_id": OLD_PIN["media_id"],
            "media_type": "video",
            "size": 9,
            "duration_seconds": 6,
        },
        new_info={
            "object_id": NEW_SELECTION["object_id"],
            "media_type": "video",
            "size": 10,
            "duration_seconds": 6,
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
            },
            "parent/clip:sibling": {"asset": "old-key", "at": 8},
            "occurrence:occ-1/clip:raw-2": {
                "asset": "occ-old",
                "clipType": "video",
                "at": 1,
                "from": 2,
                "to": 6,
                "hold": 4,
                "speed": 1,
            },
        },
        "registry": {
            "parent/asset:old-key": copy.deepcopy(OLD_PIN),
            "occurrence:occ-1/asset:occ-old": copy.deepcopy(OLD_PIN),
        },
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
    """Model the smallest closed successor without becoming product code."""
    target = f"{owner}/clip:{clip_id}"
    old_ref = f"{owner}/asset:{old_alias}"
    new_ref = f"{owner}/asset:{new_media['asset']}"
    expected_members = [target, old_ref, new_ref]

    if original_base != state["base"]:
        raise ValueError("original base guard changed")
    if (
        not (
            owner == "parent"
            or (owner.startswith("occurrence:") and "/" not in owner and "::" not in owner)
        )
        or target not in state["clips"]
    ):
        raise ValueError("raw owner/clip must be explicit and authored")
    if affected_members != expected_members:
        raise ValueError("affected member scope is not exact")
    row = state["clips"][target]
    if row["asset"] != old_alias:
        raise ValueError("old alias is not the selected clip binding")
    if set(old_media) != {"media_id", "content_digest"} or old_media != OLD_PIN:
        raise ValueError("OLD media must be the existing manifest pin")
    if state["registry"].get(old_ref) != old_media:
        raise ValueError("OLD registry binding changed")

    old_info = port.raw_media_info(old_media)
    new_info = port.selected_media(new_media)
    if old_info["object_id"] != old_media["media_id"]:
        raise ValueError("raw media identity changed")
    if new_info["object_id"] != new_media["object_id"]:
        raise ValueError("new media identity changed")
    if old_info["media_type"] != new_info["media_type"]:
        raise ValueError("media kind changed")
    if row["to"] - row["from"] != row["hold"] or row["to"] > old_info["duration_seconds"]:
        raise ValueError("OLD source window is invalid")
    if row["to"] > new_info["duration_seconds"]:
        raise ValueError("NEW source window is invalid")

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


def test_raw_old_swap_uses_manifest_old_and_exact_five_field_new():
    state = _state()
    port = _port()
    undo = _raw_old_swap(
        state,
        port,
        owner="parent",
        clip_id="raw-1",
        old_alias="old-key",
        old_media=OLD_PIN,
        new_media=NEW_SELECTION,
        affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        original_base=("revision-1", "publication-1"),
    )

    assert state["clips"]["parent/clip:raw-1"]["asset"] == "new-key"
    assert state["clips"]["parent/clip:sibling"]["asset"] == "old-key"
    assert state["registry"]["parent/asset:old-key"] == OLD_PIN
    assert state["registry"]["parent/asset:new-key"] == _new_registry_binding(
        NEW_SELECTION, "video"
    )
    assert (port.raw_reads, port.selected_reads) == (1, 1)

    undo(state)
    assert state == _state()


def test_raw_old_swap_occurrence_variant_is_scoped_to_one_occurrence():
    state = _state()
    port = _port()
    undo = _raw_old_swap(
        state,
        port,
        owner="occurrence:occ-1",
        clip_id="raw-2",
        old_alias="occ-old",
        old_media=OLD_PIN,
        new_media=NEW_SELECTION,
        affected_members=[
            "occurrence:occ-1/clip:raw-2",
            "occurrence:occ-1/asset:occ-old",
            "occurrence:occ-1/asset:new-key",
        ],
        original_base=("revision-1", "publication-1"),
    )

    assert state["clips"]["occurrence:occ-1/clip:raw-2"]["asset"] == "new-key"
    assert state["clips"]["parent/clip:raw-1"]["asset"] == "old-key"
    assert "occurrence:occ-1/asset:new-key" in state["registry"]
    assert "parent/asset:new-key" not in state["registry"]
    undo(state)
    assert state == _state()


@pytest.mark.parametrize(
    "change",
    [
        {"owner": "occurrence:display::not-an-owner", "clip_id": "raw-1"},
        {"owner": "parent", "clip_id": "raw-1", "affected_members": ["parent/clip:raw-1"]},
        {"owner": "parent", "clip_id": "sibling", "old_alias": "old-key"},
    ],
)
def test_raw_old_swap_refuses_ambiguous_owner_or_global_fanout(change):
    state = _state()
    port = _port()
    args = {
        "owner": "parent",
        "clip_id": "raw-1",
        "old_alias": "old-key",
        "old_media": OLD_PIN,
        "new_media": NEW_SELECTION,
        "affected_members": ["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        "original_base": ("revision-1", "publication-1"),
    }
    args.update(change)
    before = copy.deepcopy(state)
    with pytest.raises(ValueError):
        _raw_old_swap(state, port, **args)
    assert state == before


def test_raw_old_swap_refuses_caller_supplied_metadata_and_original_base_change():
    state = _state()
    port = _port()
    before = copy.deepcopy(state)
    caller_old = {**OLD_PIN, "duration_seconds": 999}
    with pytest.raises(ValueError):
        _raw_old_swap(
            state,
            port,
            owner="parent",
            clip_id="raw-1",
            old_alias="old-key",
            old_media=caller_old,
            new_media=NEW_SELECTION,
            affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
            original_base=("revision-0", "publication-0"),
        )
    assert state == before


def test_raw_old_swap_inverse_detects_aba_even_when_state_returns_equal():
    state = _state()
    port = _port()
    undo = _raw_old_swap(
        state,
        port,
        owner="parent",
        clip_id="raw-1",
        old_alias="old-key",
        old_media=OLD_PIN,
        new_media=NEW_SELECTION,
        affected_members=["parent/clip:raw-1", "parent/asset:old-key", "parent/asset:new-key"],
        original_base=("revision-1", "publication-1"),
    )
    state["clips"]["parent/clip:raw-1"]["asset"] = "old-key"
    state["write_epoch"] += 1
    state["clips"]["parent/clip:raw-1"]["asset"] = "new-key"
    with pytest.raises(ValueError, match="ABA"):
        undo(state)
