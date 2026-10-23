"""Final-candidate validation stays atomic and leaves authored opaque data alone."""
from __future__ import annotations

import copy

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.validation import validate_final_candidate
from tests.sdk.test_timeline_commit_provider_document import document_fixture


def candidate():
    return bundle_from_document(document_fixture(shared=False))


def test_valid_candidate_keeps_unknown_authored_fields_verbatim():
    value = candidate()
    before = copy.deepcopy(value)
    validate_final_candidate(value)
    assert value == before
    assert value["parent"]["unknown"] == {"opaque": ["parent-1", None]}
    assert value["shots"]["chapter-shot"]["internal_timeline"]["unknown"] == [1, 2]


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda value: value["parent"]["config"]["output"].update(
            fps={"numerator": 0, "denominator": 1}), "fps rational must be positive"),
        (lambda value: value["parent"]["clips"][0].update(at=-1), "must not be negative"),
        (lambda value: value["placements"][0].update(duration_ms=500), "half-open bounds"),
        (lambda value: value["parent"]["config"]["tracks"].append(
            {"id": "picture", "kind": "visual"}), "duplicate id"),
        (lambda value: value["parent"]["clips"][0].update(track="missing"), "existing track"),
    ],
)
def test_invalid_final_candidate_is_refused(change, message):
    value = candidate()
    change(value)
    with pytest.raises(AuthoringBundleError, match=message):
        validate_final_candidate(value)


def test_source_interval_is_checked_against_retained_asset_extent():
    value = candidate()
    internal = value["shots"]["chapter-shot"]["internal_timeline"]
    internal["registry"]["assets"]["picture"]["duration"] = 1
    internal["clips"][0].update(**{"from": 0.5, "to": 2})
    with pytest.raises(AuthoringBundleError, match="source interval exceeds"):
        validate_final_candidate(value)


def test_known_element_parameter_uses_declared_value_schema():
    value = candidate()
    clip = value["parent"]["clips"][0]
    clip.update(clipType="am-sprite", params={"scale": 0})
    value["parent"]["config"]["clips"][0].update(clipType="am-sprite", params={"scale": 0})
    with pytest.raises(AuthoringBundleError, match="minimum"):
        validate_final_candidate(value)


def test_sealed_builtin_rejects_new_undeclared_parameter_but_retains_opaque_history():
    before = candidate()
    value = copy.deepcopy(before)
    clip = value["parent"]["clips"][0]
    clip.update(clipType="am-flap", params={"legacy": {"keep": [None, False]}})
    value["parent"]["config"]["clips"][0].update(
        clipType="am-flap", params={"legacy": {"keep": [None, False]}})
    with pytest.raises(AuthoringBundleError, match="not declared"):
        validate_final_candidate(value, baseline=before)

    clip["params"]["opaque"] = {"keep": [None, False, {}]}
    value["parent"]["config"]["clips"][0]["params"]["opaque"] = copy.deepcopy(
        clip["params"]["opaque"])
    # Existing opaque values remain eligible for round-trip retention.
    baseline = copy.deepcopy(value)
    clip["params"]["opaque"] = {"keep": [None, False, {}, "changed"]}
    value["parent"]["config"]["clips"][0]["params"]["opaque"] = copy.deepcopy(
        clip["params"]["opaque"])
    validate_final_candidate(value, baseline=baseline)
