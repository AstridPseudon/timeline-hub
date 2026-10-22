from __future__ import annotations

import json

import pytest

from astrid.core.timeline import (
    MetaValidationError,
    validate_meta,
    validate_registry,
    validate_timeline,
)


def _canonical_size(value: object) -> int:
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def _value_at_size(target: int) -> dict[str, str]:
    value = {"value": ""}
    value["value"] = "x" * (target - _canonical_size(value))
    assert _canonical_size(value) == target
    return value


def test_meta_accepts_and_preserves_opaque_json_without_discovery() -> None:
    meta = {
        "org.example.notes": {
            "missing_asset_id": "asset-not-in-registry",
            "nullable": None,
            "ordered": [2, 1],
        },
    }
    original = json.loads(json.dumps(meta))

    validate_meta(meta)

    assert meta == original


def test_meta_reports_structured_invalid_and_limit_errors() -> None:
    with pytest.raises(MetaValidationError) as invalid:
        validate_meta({"org.example.notes": None})
    assert invalid.value.code == "invalid_meta"
    assert invalid.value.path == "meta.org.example.notes"
    assert invalid.value.hint

    with pytest.raises(MetaValidationError) as limited:
        validate_meta({"org.example.notes": _value_at_size(65_537)})
    assert limited.value.code == "meta_limit_exceeded"
    assert limited.value.path == "meta.org.example.notes"
    assert limited.value.hint


def test_meta_accepts_exact_size_and_depth_boundaries() -> None:
    validate_meta({"org.example.notes": _value_at_size(65_536)})

    whole = {f"org.example.n{index}": {"value": ""} for index in range(4)}
    fill = 262_144 - _canonical_size(whole)
    each, remainder = divmod(fill, 4)
    for index in range(4):
        whole[f"org.example.n{index}"]["value"] = "x" * (each + (index == 0) * remainder)
    assert _canonical_size(whole) == 262_144
    validate_meta(whole)

    whole["org.example.n0"]["value"] += "x"
    with pytest.raises(MetaValidationError, match="canonical UTF-8 bytes"):
        validate_meta(whole)

    value: dict[str, object] = {}
    for _ in range(31):
        value = {"nested": value}
    validate_meta({"org.example.notes": value})

    with pytest.raises(MetaValidationError, match="nested containers"):
        validate_meta({"org.example.notes": {"nested": value}})


def test_known_timeline_and_registry_meta_locations_are_admitted() -> None:
    meta = {"org.example.notes": {"id_like": "missing-is-allowed"}}
    config = {
        "meta": meta,
        "tracks": [{"id": "track", "kind": "visual", "label": "Picture", "meta": meta}],
        "clips": [{"id": "clip", "at": 0, "track": "track", "meta": meta}],
    }
    validate_timeline(config)
    validate_registry({"assets": {"asset": {"media_id": "managed", "meta": meta}}})
