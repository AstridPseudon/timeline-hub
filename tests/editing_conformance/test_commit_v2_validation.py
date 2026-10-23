"""Final-candidate validation stays atomic and leaves authored opaque data alone."""
from __future__ import annotations

import copy
import math
from fractions import Fraction

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.validation import validate_final_candidate
from tests.editing_conformance import test_recipe_scalar_commands as scalar_recipes
from tests.sdk.test_timeline_commit_provider_document import document_fixture

admitted_param_revisions = scalar_recipes.admitted_param_revisions
configured_project_pack = scalar_recipes.configured_project_pack


def candidate():
    return bundle_from_document(document_fixture(shared=False))


def test_valid_candidate_keeps_unknown_authored_fields_verbatim():
    value = candidate()
    before = copy.deepcopy(value)
    validate_final_candidate(value)
    assert value == before
    assert value["parent"]["unknown"] == {"opaque": ["parent-1", None]}
    assert value["shots"]["chapter-shot"]["internal_timeline"]["unknown"] == [1, 2]


def fps_locations(value):
    config = value["parent"]["config"]
    canvas = config.setdefault("theme_overrides", {}).setdefault("visual", {}).setdefault("canvas", {})
    return [config["output"], canvas, value["shots"]["chapter-shot"]["internal_timeline"]["output"]]


@pytest.mark.parametrize("numeric_owner", [0, 1, 2])
@pytest.mark.parametrize("parts", [(30000, 1001), (24000, 1001), (30, 1)])
def test_legacy_numeric_fps_matches_exact_canonical_serialization_without_rewriting(numeric_owner, parts):
    value = candidate()
    for location in fps_locations(value):
        location["fps"] = dict(zip(("numerator", "denominator"), parts))
    fps_locations(value)[numeric_owner]["fps"] = float(Fraction(*parts))
    before = copy.deepcopy(value)
    validate_final_candidate(value)
    assert value == before


@pytest.mark.parametrize("owner", [0, 1, 2])
@pytest.mark.parametrize("bad_rate", [
    29.97, 30, math.nextafter(30000 / 1001, math.inf),
    math.nextafter(30000 / 1001, -math.inf),
    {"numerator": 30001, "denominator": 1001},
    # Distinct exact rationals can have the same numeric serialization.
    {"numerator": 30000 * 10**15 + 1, "denominator": 1001 * 10**15},
])
def test_fps_parity_refuses_distinct_rates_in_every_location(owner, bad_rate):
    value = candidate()
    for location in fps_locations(value):
        location["fps"] = {"numerator": 30000, "denominator": 1001}
    fps_locations(value)[owner]["fps"] = bad_rate
    before = copy.deepcopy(value)
    with pytest.raises(AuthoringBundleError, match="same rational rate"):
        validate_final_candidate(value, baseline=before)
    assert value == before


@pytest.mark.parametrize("owner", [0, 1, 2])
@pytest.mark.parametrize("bad_rate", [
    True, 0, -30, "29.97002997002997", float("nan"), float("inf"), -float("inf"),
    {"numerator": 30000, "denominator": 0},
    {"numerator": True, "denominator": 1001},
])
def test_fps_compatibility_keeps_invalid_and_nonfinite_rates_refused(owner, bad_rate):
    value = candidate()
    fps_locations(value)[owner]["fps"] = bad_rate
    with pytest.raises(AuthoringBundleError):
        validate_final_candidate(value)


def test_numeric_only_fps_requires_exact_decimal_equality():
    value = candidate()
    locations = fps_locations(value)
    for location in locations:
        location["fps"] = 30000 / 1001
    validate_final_candidate(value)
    locations[2]["fps"] = math.nextafter(30000 / 1001, math.inf)
    with pytest.raises(AuthoringBundleError, match="same rational rate"):
        validate_final_candidate(value)


def test_mixed_legacy_fps_preserves_exact_canvas_frame_timing(monkeypatch):
    from astrid.sdk.timeline import _commit_timing_validation as timing

    value = candidate()
    locations = fps_locations(value)
    locations[0]["fps"] = locations[2]["fps"] = 30000 / 1001
    locations[1]["fps"] = {"numerator": 30000, "denominator": 1001}
    value["parent"]["clips"][0]["at"] = .97
    value["parent"]["config"]["clips"] = copy.deepcopy(value["parent"]["clips"])
    before = copy.deepcopy(value)
    results = []
    compile_timing = timing.compile_timing

    def compile_candidate(inputs):
        result = compile_timing(inputs)
        results.append(result)
        return result

    monkeypatch.setattr(timing, "compile_timing", compile_candidate)
    validate_final_candidate(value)
    interval = results[0].timings[("parent", "", value["parent"]["clips"][0]["id"])]
    assert interval["start_frame"] == 29
    assert interval["applied_start"] == Fraction(29029, 30000)
    assert value == before


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


@pytest.mark.parametrize("owner", ["parent", "child"])
def test_explicit_null_source_start_is_zero_for_arithmetic_and_remains_authored(owner):
    value = candidate()
    timeline = (value["parent"] if owner == "parent" else
                value["shots"]["chapter-shot"]["internal_timeline"])
    clip = timeline["clips"][0]
    clip.update(**{"from": None, "to": 2})
    timeline["registry"]["assets"]["picture"]["duration"] = 2
    if owner == "parent":
        timeline["config"]["clips"] = copy.deepcopy(timeline["clips"])
    before = copy.deepcopy(value)
    validate_final_candidate(value)
    assert value == before
    assert clip["from"] is None
    clip["to"] = 3
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


def test_production_validation_always_invokes_the_real_timing_adapter(monkeypatch):
    from astrid.sdk.timeline import _commit_timing_validation as timing

    value = candidate()
    before = copy.deepcopy(value)
    calls = []
    compile_candidate = timing.validate_candidate_timing

    def validate(bundle, *, baseline=None):
        calls.append(bundle)
        compile_candidate(bundle, baseline=baseline)

    monkeypatch.setattr(timing, "validate_candidate_timing", validate)
    validate_final_candidate(value)
    assert calls == [value]
    assert calls[0] is value
    assert value == before


@pytest.mark.parametrize(("owner", "field", "declaration"), [
    ("parent", "for", 0), ("parent", "for", -1),
    ("parent", "on", "c999"), ("parent", "until", "c999"),
    ("child", "for", -1), ("child", "on", "c999"), ("child", "until", "c999"),
    ("parent", "at_ms", 1000), ("parent", "from_ms", 0),
    ("parent", "to_ms", 2000), ("parent", "time_map", {}),
])
def test_production_validation_refuses_all_timing_probes(owner, field, declaration):
    value = candidate()
    rows = (value["parent"]["clips"] if owner == "parent" else
            value["shots"]["chapter-shot"]["internal_timeline"]["clips"])
    if field in ("for", "on", "until"):
        rows[0].setdefault("app", {}).setdefault("astrid", {})[field] = declaration
    else:
        rows[0][field] = declaration
        if field == "at_ms":
            rows[0].pop("at")
    if owner == "parent":
        value["parent"]["config"]["clips"] = copy.deepcopy(rows)
    before = copy.deepcopy(value)
    with pytest.raises(AuthoringBundleError, match="candidate.timing"):
        validate_final_candidate(value)
    assert value == before


def test_unchanged_selected_known_params_use_only_consumed_retained_schema(
        admitted_param_revisions, configured_project_pack):
    _, selected = admitted_param_revisions
    options = scalar_recipes.schema_options(configured_project_pack, selected)
    value = candidate()
    clip = value["parent"]["clips"][0]
    clip.update(clipType=selected["id"], elementRef=selected,
                params={"seed": 16, "opaque": {"keep": [None, False]}})
    value["parent"]["config"]["clips"] = copy.deepcopy(value["parent"]["clips"])
    baseline = copy.deepcopy(value)
    # An unrelated edit retains the authored literal without guessing a schema.
    validate_final_candidate(value, baseline=baseline)
    verified, _ = options["schema_inputs"][0]
    validate_final_candidate(value, baseline=baseline, realm_id="realm",
                             schema_inputs=[(verified, {})])
    # A consumed portable declaration is authority even for an unchanged field.
    with pytest.raises(AuthoringBundleError, match="16|10"):
        validate_final_candidate(value, baseline=baseline, **{
            key: options[key] for key in ("realm_id", "schema_inputs")})
    assert value == baseline
    clip["params"]["seed"] = 8
    value["parent"]["config"]["clips"] = copy.deepcopy(value["parent"]["clips"])
    with pytest.raises(AuthoringBundleError, match="declaration is unavailable"):
        validate_final_candidate(value, baseline=baseline, realm_id="realm",
                                 schema_inputs=[(verified, {})])
    validate_final_candidate(value, baseline=baseline, **{
        key: options[key] for key in ("realm_id", "schema_inputs")})
