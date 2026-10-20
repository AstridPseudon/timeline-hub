"""Normal artifact admission is a source-pair probe, not a group release."""
from __future__ import annotations

import json

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_official_runtime_schema_admits_existing_lane_capture_and_canonical_output():
    use_runtime()
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from tests.editing_conformance.test_recipe_m2_group_move import FIXTURE

    golden = json.loads(FIXTURE.read_text())
    validate_commit_value(golden['commands'][0], 'EditCommand')
    validate_commit_value(golden['output'], 'CanonicalDocument')
