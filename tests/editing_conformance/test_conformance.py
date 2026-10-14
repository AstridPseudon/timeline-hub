"""One test per (scenario, path) over every tests/editing_scenarios/**/*.yaml. Run: python -m pytest tests/editing_conformance"""

from __future__ import annotations

import pytest

from tests.editing_conformance.runner import (
    SCENARIOS,
    classify,
    evaluate,
    load_scenario,
    run_scenario,
    xfail_reasons,
)

_SCENARIOS = [load_scenario(p) for p in sorted(SCENARIOS.rglob("*.yaml"))]
_IDS = [s.id for s in _SCENARIOS]
if len(set(_IDS)) != len(_IDS):
    raise RuntimeError(f"duplicate scenario ids: {sorted({i for i in _IDS if _IDS.count(i) > 1})}")
_CASES = [(s, name) for s in _SCENARIOS for name in s.present()]

_CACHE: dict[str, tuple[dict, dict]] = {}


def _evaluated(scenario):
    """Run a scenario once (all its paths) and evaluate it; later tests for the same scenario reuse it."""
    if scenario.id not in _CACHE:
        results = run_scenario(scenario)
        _CACHE[scenario.id] = (results, evaluate(scenario, results))
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
