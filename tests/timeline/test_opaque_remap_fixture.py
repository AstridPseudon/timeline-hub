"""Shared opaque-remap fixture: the Python authority, also loaded by App's remapItems."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.core.timeline.authoring_bundle import (
    _canonical_json,
    _digest,
    _remap_known_item_references,
)

FIXTURE = json.loads(
    (Path(__file__).resolve().parents[1] / "editing_conformance/fixtures/opaque_remap.json").read_text()
)


@pytest.mark.parametrize("case", FIXTURE["cases"], ids=lambda case: case["name"])
def test_remap_matches_shared_fixture_byte_for_byte(case):
    payload = copy.deepcopy(case["payload"])
    result = _remap_known_item_references(payload, case["item_ids"])
    assert _canonical_json(result) == _canonical_json(case["expected"])
    assert payload == case["payload"]


def test_prototype_keys_round_trip_as_plain_own_data():
    payload = {"items": [{"item_id": "item-1", "metadata": {"source_item_id": "item-1"}}]}
    payload["__proto__"] = {"constructor": {"prototype": "item-1"}}
    payload["constructor"] = "item-1"
    payload["prototype"] = {"__proto__": None}
    assert payload["__proto__"] == {"constructor": {"prototype": "item-1"}}
    encoded = _canonical_json(payload)
    decoded = json.loads(encoded)
    assert _canonical_json(decoded) == encoded
    assert _digest(decoded) == _digest(payload)
    remapped = _remap_known_item_references(payload, {"item-1": "item-9"})
    assert remapped["__proto__"] == payload["__proto__"]
    assert remapped["constructor"] == "item-1"
    assert remapped["items"][0]["item_id"] == "item-9"
    restored = _remap_known_item_references(remapped, {"item-9": "item-1"})
    assert _canonical_json(restored) == encoded
    assert _digest(restored) == _digest(payload)
