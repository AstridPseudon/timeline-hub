"""Closed raw-OLD swap successor; existing selected-media lanes stay frozen."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import _SCHEMA, execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_occurrence_media_commands import (
    capture_occurrence_swap_media,
    capture_parent_swap_media,
)
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs
from tests.editing_conformance.test_recipe_parent_media import parent_input
from tests.sdk.test_timeline_commit_provider import CommitRejected, runtime_abi

pytestmark = pytest.mark.usefixtures(runtime_abi.__name__)


def _versions(op):
    return {
        branch["properties"]["version"]["const"]
        for clause in _SCHEMA["$defs"]["EditCommand"]["allOf"]
        if clause["if"]["properties"]["op"].get("const") == op
        for branch in clause["then"].get("anyOf", [clause["then"]])
    }


def _raw_inputs(owner):
    if owner == "parent":
        bundle, old, new, verified = parent_input("video")
        target = "parent/clip:clip-a"
        alias = "parent/asset:picture"
        command = capture_parent_swap_media
    else:
        document, old, new, verified = inputs("video")
        bundle = bundle_from_document(document)
        target = "occurrence:occ-a/clip:clip-a"
        alias = "occurrence:occ-a/asset:picture"
        command = capture_occurrence_swap_media
    raw = {"media_id": old["object_id"], "content_digest": old["object_id"]}
    State(bundle).entity(alias).clear()
    State(bundle).entity(alias).update(raw)
    raw_verified = [
        {"raw_pin": copy.deepcopy(raw), "media_info": {
            "object_id": raw["media_id"], "media_type": "video/mp4", "size": 9,
        }},
        copy.deepcopy(verified[1]),
    ]
    return bundle, target, raw, new, raw_verified, command


def test_new_versions_are_unoccupied_and_raw_old_is_exactly_two_fields():
    assert _versions("clip.swap-media") == {"1", "2"}
    assert _versions("occurrence.swap-media") == {"1", "2", "3"}

    command = {
        "schema_version": 1, "op": "clip.swap-media", "version": "2",
        "select": "parent/clip:clip-a", "args": {
            "old_media": {"media_id": "sha256:" + "a" * 64,
                           "content_digest": "sha256:" + "a" * 64},
            "media": {"asset": "new", "generation_id": "g", "variant_id": "v",
                      "object_id": "sha256:" + "b" * 64,
                      "catalog_digest": "sha256:" + "c" * 64},
        }, "intent": {"ownership": "parent"},
    }
    validate_command(command)
    for extra in ({"duration_seconds": 6}, {"generation_id": "g"}, {"owner": "parent"}):
        damaged = copy.deepcopy(command)
        damaged["args"]["old_media"].update(extra)
        with pytest.raises(CommandError):
            validate_command(damaged)

    occurrence_v2 = copy.deepcopy(command)
    occurrence_v2.update(op="occurrence.swap-media", version="2",
                          select="occurrence:occ-a/clip:clip-a",
                          intent={"ownership": "occurrence"})
    with pytest.raises(CommandError):
        validate_command(occurrence_v2)


@pytest.mark.parametrize("owner", ["parent", "occurrence"])
def test_raw_old_swap_preserves_original_scope_and_replays(owner):
    bundle, target, raw, new, verified, capture = _raw_inputs(owner)
    before = copy.deepcopy(bundle)
    command = capture(bundle, target, raw, new, verified_media=verified)
    assert command["version"] == ("2" if owner == "parent" else "3")
    plan = execute(bundle, [command], verified_media=verified)

    row = State(plan.bundle).entity(target)
    assert row["asset"] == new["asset"]
    assert row["from"] == 2 and row["to"] == 6 and row["hold"] == 4
    assert State(plan.bundle).entity(target.rsplit("/", 1)[0] + "/asset:picture") == raw
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    assert inverse(plan.bundle, plan.records).bundle == before


def test_raw_old_swap_keeps_aba_and_new_alias_guards():
    bundle, target, raw, new, verified, capture = _raw_inputs("parent")
    command = capture(bundle, target, raw, new, verified_media=verified)
    plan = execute(bundle, [command], verified_media=verified)
    with pytest.raises(CommandError, match="intervening"):
        inverse(plan.bundle, plan.records, [
            later(target, ["asset"], "picture"),
            later(target, ["asset"], new["asset"]),
        ])


def test_provider_without_optional_raw_reader_fails_closed_before_writes():
    bundle, target, raw, new, verified, capture = _raw_inputs("parent")
    command = capture(bundle, target, raw, new, verified_media=verified)
    realm = MediaRealm(document_from_bundle(bundle), verified)
    before = (copy.deepcopy(realm.head), copy.deepcopy(realm.entries))
    with pytest.raises(CommitRejected) as error:
        realm.call([command])
    assert error.value.failure["details"]["reason"] == "dependency_unavailable"
    assert (realm.head, realm.entries) == before
