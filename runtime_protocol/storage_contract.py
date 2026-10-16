"""Storage discovery shapes; request arithmetic remains producer/host owned."""
import re

from .errors import ValidationError

# Pair components and their sum must round-trip exactly through JSON clients.
MAX_STORAGE_ESTIMATE_BYTES = (1 << 53) - 1
REQUEST_ESTIMATOR_PENDING = "request_estimator_execution_not_integrated"


def validate_storage_estimate(value):
    if not isinstance(value, dict):
        raise ValidationError("storage_estimate must be an object")
    if any(not isinstance(key, str) for key in value):
        raise ValidationError("storage_estimate keys must be strings")
    expected = {"scratch_bytes", "output_bytes"}
    if set(value) != expected:
        raise ValidationError("storage_estimate must contain exactly scratch_bytes and output_bytes",
                              details={"missing": sorted(expected - set(value)), "unexpected": sorted(set(value) - expected)})
    for key, count in value.items():
        if type(count) is not int:
            raise ValidationError(f"storage_estimate.{key} must be an integer")
        if not 0 <= count <= MAX_STORAGE_ESTIMATE_BYTES:
            raise ValidationError(f"storage_estimate.{key} is out of range",
                                  details={"minimum": 0, "maximum": MAX_STORAGE_ESTIMATE_BYTES})
    if sum(value.values()) > MAX_STORAGE_ESTIMATE_BYTES:
        raise ValidationError("storage_estimate total is out of range", details={"maximum": MAX_STORAGE_ESTIMATE_BYTES})
    return dict(value)


def storage_contract(descriptor):
    """Validate without loading any estimator code or trusting its arithmetic."""
    legacy = {"scratch_bytes": descriptor.get("estimated_scratch_bytes", 0),
              "output_bytes": descriptor.get("estimated_output_bytes", 0)}
    value = descriptor.get("storage_estimate_contract", {"mode": "static", **legacy})
    if not isinstance(value, dict):
        raise ValidationError("storage_estimate_contract must be an object")
    mode = value.get("mode")
    if mode == "static" and set(value) == {"mode", "scratch_bytes", "output_bytes"}:
        pair = validate_storage_estimate({key: value[key] for key in legacy})
        if pair != validate_storage_estimate(legacy):
            raise ValidationError("static storage contract must equal legacy estimates")
        return {"mode": mode, **pair}
    if mode == "unavailable" and set(value) == {"mode", "reason"}:
        if isinstance(value["reason"], str) and value["reason"]:
            return dict(value)
    if mode == "request_estimated" and set(value) == {"mode", "estimator"}:
        estimator = value["estimator"]
        if (isinstance(estimator, dict) and set(estimator) == {"id", "version", "implementation_digest"}
                and isinstance(estimator["id"], str) and estimator["id"]
                and type(estimator["version"]) is int and estimator["version"] > 0
                and isinstance(estimator["implementation_digest"], str)
                and re.fullmatch(r"sha256:[0-9a-f]{64}", estimator["implementation_digest"])):
            validate_storage_estimate(legacy)
            return {"mode": mode, "estimator": dict(estimator)}
    raise ValidationError("invalid storage_estimate_contract discriminator or fields")
