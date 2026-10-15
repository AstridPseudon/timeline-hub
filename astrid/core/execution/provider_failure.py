"""Explicit provider rejection contract; only safe-to-repeat failures opt in.

Executors must not mark ambiguous timeouts or accepted paid requests retryable.
Runtime owns all retry budgets, delays, and provider pacing.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

from astrid.core.contracts.errors import AstridError
from astrid.core.foundation.atomic_io import write_json_atomic

PROVIDER_FAILURE_FILE = ".astrid-provider-failure.json"


class ProviderFailure(AstridError):
    def __init__(self, message: str, *, provider_id: str, retryable: bool = False,
                 retry_after_seconds: float = 0):
        if not isinstance(provider_id, str) or not provider_id.strip():
            raise ValueError("provider_id must be non-empty")
        if type(retryable) is not bool:
            raise ValueError("retryable must be boolean")
        if (isinstance(retry_after_seconds, bool)
                or not isinstance(retry_after_seconds, (int, float))
                or not math.isfinite(retry_after_seconds) or retry_after_seconds < 0):
            raise ValueError("retry_after_seconds must be finite and non-negative")
        super().__init__(message, code="provider_failure")
        self.provider_id = provider_id.strip()
        self.retryable = retryable
        self.retry_after_seconds = float(retry_after_seconds)

    def to_envelope(self) -> dict[str, Any]:
        return {**super().to_envelope(), "provider_id": self.provider_id,
                "retryable": self.retryable,
                "retry_after_seconds": self.retry_after_seconds}

    def write(self, output_root: Path) -> None:
        output_root.mkdir(parents=True, exist_ok=True)
        write_json_atomic(output_root / PROVIDER_FAILURE_FILE, self.to_envelope())


def provider_failure(value: object) -> ProviderFailure | None:
    """Recognize only an explicit version of the rejection envelope."""
    if not isinstance(value, Mapping) or value.get("code") != "provider_failure":
        return None
    try:
        return ProviderFailure(str(value.get("message") or value.get("cause") or "provider failed"),
                               provider_id=value.get("provider_id"),
                               retryable=value.get("retryable"),
                               retry_after_seconds=value.get("retry_after_seconds"))
    except (TypeError, ValueError):
        return None
