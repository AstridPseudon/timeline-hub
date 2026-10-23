from __future__ import annotations

from typing import Any

import pytest

from astrid.core.timeline import validate_timeline, validate_timeline_config_for_container
from astrid.core.timeline.validators.meta import MetaValidationError, validate_meta


def _timeline() -> dict[str, Any]:
    return {
        "tracks": [{"id": "track", "kind": "visual", "label": "Picture"}],
        "clips": [{"id": "clip", "at": 0, "track": "track"}],
    }


def test_meta_preserves_opaque_canonical_json() -> None:
    meta = {
        "org.example.notes": {
            "missing_asset_id": "asset-not-in-registry",
            "nullable": None,
            "ordered": [2, 1],
        },
    }
    validate_meta(meta)
    assert meta["org.example.notes"]["ordered"] == [2, 1]


@pytest.mark.parametrize("location", ["top", "track", "clip"])
def test_invalid_meta_is_refused_at_each_known_timeline_location(location: str) -> None:
    config = _timeline()
    if location == "top":
        config["meta"] = {"org.example.notes": None}
    elif location == "track":
        config["tracks"][0]["meta"] = {"org.example.notes": None}
    else:
        config["clips"][0]["meta"] = {"org.example.notes": None}

    with pytest.raises(MetaValidationError) as error:
        validate_timeline(config)
    assert error.value.code == "invalid_meta"


def test_meta_limits_are_refused_without_broadening_unknown_fields() -> None:
    with pytest.raises(MetaValidationError) as error:
        validate_meta({"org.example.notes": {"value": "x" * 65_537}})
    assert error.value.code == "meta_limit_exceeded"

    with pytest.raises(MetaValidationError) as error:
        validate_meta({"org.example.notes": {"value": "x" * 300_000}})
    assert error.value.code == "meta_limit_exceeded"

    config = _timeline()
    config["unexpected"] = True
    # Timeline's domain loader keeps its existing passthrough behavior; the
    # strict container validator remains the refusal boundary for unknown keys.
    with pytest.raises(ValueError, match="unknown key"):
        validate_timeline_config_for_container(config)
