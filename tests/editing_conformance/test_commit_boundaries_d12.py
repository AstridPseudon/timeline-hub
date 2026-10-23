"""D12a retains legacy bounds while written intervals and targets stay strict."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.validation import validate_final_candidate
from tests.editing_conformance.test_commit_v2_validation import candidate
from tests.editing_conformance.test_recipe_m2_clip_add import literal_row, with_track
from tests.sdk import test_timeline_commit_provider as provider
from tests.sdk.test_p1_doc_patch_provider import _service_call
from tests.sdk.test_timeline_commit_provider_document import document_fixture

runtime_abi = provider.runtime_abi


def encoded(value):
    return json.dumps(value, sort_keys=True, allow_nan=False)


def legacy_document(kind):
    document = document_fixture(shared=False)
    parent = document["parent_revision"]
    internal = document["internal_timeline_revisions"][0]
    if kind == "occurrence":
        parent["payload"]["occurrences"][0]["duration_ms"] = 100
    elif kind == "asset":
        internal["payload"]["registry"]["assets"]["picture"]["duration"] = 1
        internal["payload"]["clips"][0].update(**{"from": 0.5, "to": 2})
    else:
        internal["payload"]["clips"][0]["source_window"] = {"from": 20, "to": 30}
    for image in (parent, internal):
        image["content_digest"] = _digest(image["payload"])
    document["dependency_manifest"] = _manifest(
        document["shot_revisions"], document["internal_timeline_revisions"],
        document["dependency_manifest"]["media"], [],
    )
    return document


@pytest.mark.parametrize("kind", ["occurrence", "asset", "map"])
@pytest.mark.parametrize("dry_run", [False, True])
def test_production_unrelated_track_edit_preserves_legacy_boundaries(kind, dry_run):
    original = legacy_document(kind)
    realm = provider.DetachedRealm(original)
    result = _service_call(realm, [provider.track_create()], controls={
        "label": "Add track", "merge": "fields", "reads": [], "dry_run": dry_run,
        "source": {"via": "python"}, "rationale": "Unrelated track", "group_id": "bounds-d12",
        "steps": [{"id": "track", "label": "Add track", "intent": "Add audio",
                   "tags": ["test"], "command_ordinals": [0], "patch": [], "reads": []}],
    })
    data = result["data"]
    assert data["status"] == ("preview" if dry_run else "accepted")
    if dry_run:
        assert data["would_status"] == "accepted"
        assert result["receipt"] is None
    else:
        assert result["receipt"]["result"] == data
    assert encoded(data["canonical_document"]["internal_timeline_revisions"]) == encoded(
        original["internal_timeline_revisions"])
    assert data["canonical_document"]["parent_revision"]["payload"]["occurrences"] == (
        original["parent_revision"]["payload"]["occurrences"])
    records = data if dry_run else realm.prepared[-1]["records"]
    assert records["steps"][0]["patch"]


@pytest.mark.parametrize("damage", ["new", "interval", "bound", "owner"])
def test_new_changed_or_rebound_occurrence_intervals_are_strict(damage):
    baseline = bundle_from_document(legacy_document("occurrence"))
    value = copy.deepcopy(baseline)
    internal = value["shots"]["chapter-shot"]["internal_timeline"]
    if damage == "new":
        internal["clips"].append(dict(internal["clips"][0], id="new"))
    elif damage == "interval":
        internal["clips"][0]["at"] = 2
    elif damage == "bound":
        value["placements"][0]["duration_ms"] = 50
    else:
        value["source_mapping"]["shots"]["chapter-shot"]["internal_timeline_revision_id"] = "other"
    before = encoded(value)
    with pytest.raises(AuthoringBundleError, match="half-open bounds"):
        validate_final_candidate(value, baseline=baseline)
    assert encoded(value) == before


@pytest.mark.parametrize("damage", ["new", "interval", "asset"])
def test_new_changed_or_invalidated_asset_windows_are_strict(damage):
    baseline = bundle_from_document(legacy_document("asset"))
    value = copy.deepcopy(baseline)
    internal = value["shots"]["chapter-shot"]["internal_timeline"]
    if damage == "new":
        internal["clips"].append(dict(internal["clips"][0], id="new"))
    elif damage == "interval":
        internal["clips"][0]["to"] = 3
    else:
        internal["registry"]["assets"]["picture"]["duration"] = 0.5
    with pytest.raises(AuthoringBundleError, match="source interval exceeds"):
        validate_final_candidate(value, baseline=baseline)


@pytest.mark.parametrize("damage", ["new-map", "map", "timing", "new-declaration", "owner"])
def test_legacy_map_retention_never_exempts_a_changed_timing_basis(damage):
    baseline = bundle_from_document(legacy_document("map"))
    value = copy.deepcopy(baseline)
    clip = value["shots"]["chapter-shot"]["internal_timeline"]["clips"][0]
    if damage == "new-map":
        baseline["shots"]["chapter-shot"]["internal_timeline"]["clips"][0].pop("source_window")
    elif damage == "map":
        clip["source_window"]["to"] = 31
    elif damage == "timing":
        clip["at"] = 2
    elif damage == "new-declaration":
        clip.setdefault("app", {}).setdefault("astrid", {})["on"] = "c999"
    else:
        value["source_mapping"]["shots"]["chapter-shot"]["internal_timeline_revision_id"] = "other"
    with pytest.raises(AuthoringBundleError, match="unsupported explicit map"):
        validate_final_candidate(value, baseline=baseline)


def test_first_clip_original_literal_with_null_speed_reaches_final_validation():
    from astrid.sdk.timeline._clip_commands import capture_clip_add

    baseline = with_track()
    row = literal_row(speed=None)
    plan = execute(baseline, [capture_clip_add(baseline, "parent", row)])
    before = encoded(plan.bundle)
    validate_final_candidate(plan.bundle, baseline=baseline)
    assert encoded(plan.bundle) == before
    assert document_from_bundle(plan.bundle)["parent_revision"]["payload"]["clips"] == [row]


@pytest.mark.parametrize("speed", [0, -1, True, "1"])
def test_nullable_speed_preserves_numeric_guards(speed):
    value = candidate()
    value["parent"]["clips"][0]["speed"] = speed
    value["parent"]["config"]["clips"] = copy.deepcopy(value["parent"]["clips"])
    with pytest.raises(AuthoringBundleError, match="speed"):
        validate_final_candidate(value)
