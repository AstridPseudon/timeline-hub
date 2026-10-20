"""Independent audit regressions for the held v1.0.3 scanner candidate."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def candidate(request: pytest.FixtureRequest) -> Any:
    path = Path(os.environ["SCANNER_CANDIDATE"]).resolve(strict=True)
    spec = importlib.util.spec_from_file_location("scanner_candidate", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def synthetic(candidate: Any) -> dict[str, Any]:
    tests_path = Path(candidate.__file__).with_name("tests").joinpath("test_owner_film_cliplook_scan.py")
    spec = importlib.util.spec_from_file_location("candidate_tests", tests_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.synthetic_document()


@pytest.mark.xfail(
    strict=True,
    reason="Candidate must inventory canonical incoming transition mappings that use type= when the manager patches it.",
)
def test_canonical_incoming_type_alias_is_not_silently_dropped(
    candidate: Any, synthetic: dict[str, Any]
) -> None:
    synthetic["parent_revision"]["payload"]["clips"][1]["transition"] = {
        "type": "crossfade",
        "duration": 0.2,
    }
    result = candidate.scan(synthetic, agent_root=os.environ["SCANNER_AGENT_ROOT"])
    boundary = next(row for row in result["transition_boundaries"] if row["clip_id"] == "element-b")
    assert boundary["transition_id"] == "crossfade"
    assert boundary["transition_type"] == "crossfade"
