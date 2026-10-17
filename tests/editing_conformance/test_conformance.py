"""One test per (scenario, path) over every tests/editing_scenarios/**/*.yaml. Run: python -m pytest tests/editing_conformance"""

from __future__ import annotations

import json
import re

import pytest

from tests.editing_conformance.runner import (
    SCENARIOS,
    classify,
    load_scenario,
    run_scenario,
    xfail_reasons,
)
from tests.editing_conformance.runner import (
    evaluate as _evaluate,
)

_CUT_ID = re.compile(r"c0*(\d+)([a-z]?)\Z")
_RESERVATION_KEY = "cut_id_high_water"

_SCENARIOS = [load_scenario(p) for p in sorted(SCENARIOS.rglob("*.yaml"))]
_IDS = [s.id for s in _SCENARIOS]
if len(set(_IDS)) != len(_IDS):
    raise RuntimeError(f"duplicate scenario ids: {sorted({i for i in _IDS if _IDS.count(i) > 1})}")
_CASES = [(s, name) for s in _SCENARIOS for name in s.present()]

_CACHE: dict[str, tuple[dict, dict]] = {}


def _cut_ids(document: str) -> set[str]:
    """Return authored cut identities without changing or normalizing the document."""
    from astrid.core.timeline.astrid_ns import read_app

    bundle = json.loads(document)
    result = set()
    for shot in (bundle.get("shots") or {}).values():
        for clip in ((shot.get("internal_timeline") or {}).get("clips") or []):
            cut_id = read_app(clip).get("cut")
            if isinstance(cut_id, str) and _CUT_ID.fullmatch(cut_id):
                result.add(cut_id)
    return result


def _reservation_state(document: str) -> dict:
    """Read the exact canonical high-water field and derive marks from active cut IDs."""
    bundle = json.loads(document)
    config = ((bundle.get("parent") or {}).get("config") or {})
    app = config.get("app") or {}
    namespace = app.get("astrid") or {}
    stored = _RESERVATION_KEY in namespace
    raw = namespace.get(_RESERVATION_KEY, {})
    if not isinstance(raw, dict) or set(raw) - {"number", "suffixes"}:
        raise ValueError(f"invalid app.astrid.{_RESERVATION_KEY}: {raw!r}")
    number = raw.get("number", 0)
    suffixes = raw.get("suffixes", {})
    if type(number) is not int or number < 0 or not isinstance(suffixes, dict):
        raise ValueError(f"invalid app.astrid.{_RESERVATION_KEY}: {raw!r}")
    normalized_suffixes = {}
    for key, value in suffixes.items():
        if not isinstance(key, str) or not key.isdigit() or str(int(key)) != key \
                or type(value) is not int or not 1 <= value <= 26:
            raise ValueError(f"invalid app.astrid.{_RESERVATION_KEY} suffix: {key!r}={value!r}")
        normalized_suffixes[key] = value

    max_suffix_number = max((int(key) for key in normalized_suffixes), default=0)
    reservation_number = max(number, max_suffix_number)
    effective_number = reservation_number
    effective_suffixes = dict(normalized_suffixes)
    for cut_id in _cut_ids(document):
        match = _CUT_ID.fullmatch(cut_id)
        cut_number, suffix = int(match[1]), match[2]
        effective_number = max(effective_number, cut_number)
        if suffix:
            key = str(cut_number)
            effective_suffixes[key] = max(effective_suffixes.get(key, 0), ord(suffix) - 96)
    return {
        "stored": stored,
        "raw_number": number,
        "reservation_number": reservation_number,
        "raw_suffixes": normalized_suffixes,
        "number": effective_number,
        "suffixes": effective_suffixes,
    }


def _authored_restoration_matches(base: str, undone: str) -> bool:
    """Ignore only the reservation value and empty containers created solely to hold it."""
    expected = json.loads(base)
    restored = json.loads(undone)
    path = ("parent", "config", "app", "astrid", _RESERVATION_KEY)
    owner = restored
    for key in path[:-1]:
        if not isinstance(owner, dict) or key not in owner or not isinstance(owner[key], dict):
            owner = None
            break
        owner = owner[key]
    if owner is not None:
        owner.pop(path[-1], None)

    # Film namespace shells are created to store the reservation. Remove a shell
    # only when it is empty after removing that field and did not exist in the base.
    for depth in range(len(path) - 2, -1, -1):
        container_path = path[:depth + 1]
        candidate_owner = restored
        expected_owner = expected
        exists_in_base = True
        for key in container_path:
            if not isinstance(expected_owner, dict) or key not in expected_owner:
                exists_in_base = False
                break
            expected_owner = expected_owner[key]
        if exists_in_base:
            continue
        for key in container_path[:-1]:
            candidate_owner = candidate_owner.get(key) if isinstance(candidate_owner, dict) else None
        container_key = container_path[-1]
        if isinstance(candidate_owner, dict) and candidate_owner.get(container_key) == {}:
            candidate_owner.pop(container_key, None)
    return restored == expected


def _reservation_invariant_error(result) -> str | None:
    labels = ("base", "after", "undone", "redone")
    try:
        states = [_reservation_state(getattr(result, label)) for label in labels]
    except (TypeError, ValueError) as exc:
        return str(exc)
    for previous_label, current_label, previous, current in zip(labels, labels[1:], states, states[1:]):
        if previous["stored"] and not current["stored"]:
            return f"{_RESERVATION_KEY} metadata disappeared from {previous_label} to {current_label}"
        if current["raw_number"] < previous["raw_number"]:
            return f"{_RESERVATION_KEY}.number lowered from {previous_label} to {current_label}"
        for key, value in previous["raw_suffixes"].items():
            if current["raw_suffixes"].get(key, 0) < value:
                return f"{_RESERVATION_KEY}.suffixes[{key!r}] lowered from {previous_label} to {current_label}"
        if current["number"] < previous["number"]:
            return f"effective cut number reservation lowered from {previous_label} to {current_label}"
        for key, value in previous["suffixes"].items():
            if current["suffixes"].get(key, 0) < value:
                return f"effective suffix reservation {key!r} lowered from {previous_label} to {current_label}"

    base, after = states[0], states[1]
    new_ids = _cut_ids(result.after) - _cut_ids(result.base)
    for cut_id in sorted(new_ids):
        match = _CUT_ID.fullmatch(cut_id)
        number, suffix = int(match[1]), match[2]
        if (number <= base["number"] if not suffix else
                ord(suffix) - 96 <= base["suffixes"].get(str(number), 0)):
            return f"new cut identity {cut_id!r} reuses an existing reservation"
        if not after["stored"]:
            return f"new cut identity {cut_id!r} has no persisted reservation metadata"
        if number > after["reservation_number"] or (suffix and ord(suffix) - 96 > after["raw_suffixes"].get(str(number), 0)):
            return f"persisted reservation metadata does not cover new cut identity {cut_id!r}"
    return None


def reservation_aware_evaluate(scenario, results: dict[str, object]) -> dict[tuple[str, str], str]:
    """Keep raw results intact while separating reservation monotonicity from authored restoration."""
    failures = _evaluate(scenario, results)
    for name, result in results.items():
        invariant_error = _reservation_invariant_error(result)
        if invariant_error:
            failures[(name, "reservation")] = invariant_error
            continue
        if (result.new_steps >= 1 and result.undo_error is None
                and _authored_restoration_matches(result.base, result.undone)):
            failures.pop((name, "undo"), None)
        if (result.new_steps >= 1 and result.redo_error is None
                and _authored_restoration_matches(result.after, result.redone)):
            failures.pop((name, "redo"), None)
    return failures


def _evaluated(scenario):
    """Run a scenario once (all its paths) and evaluate it; later tests for the same scenario reuse it."""
    if scenario.id not in _CACHE:
        results = run_scenario(scenario)
        _CACHE[scenario.id] = (results, reservation_aware_evaluate(scenario, results))
    return _CACHE[scenario.id]


@pytest.mark.parametrize(("scenario", "path"), _CASES, ids=[f"{s.id}-{p}" for s, p in _CASES])
def test_conformance(scenario, path):
    spec = scenario.paths[path]
    if spec.missing is not None:
        pytest.xfail(f"missing: {spec.missing}")

    _results, failures = _evaluated(scenario)
    unexpected, expected, fixed = classify(scenario, failures)

    bad = [k for k in unexpected if k[0] == path]
    if bad:
        pytest.fail("\n\n".join(f"{p} {c}: {failures[(p, c)]}" for p, c in bad))

    stale = [k for k in fixed if k[0] == path]
    if stale:
        pytest.fail("; ".join(f"fixed? remove the xfail: {p} {c}" for p, c in stale))

    known = [k for k in expected if k[0] == path]
    if known:
        reasons = xfail_reasons(scenario)
        pytest.xfail("; ".join(f"{p} {c}: {reasons.get((p, c), 'missing')}" for p, c in known))
