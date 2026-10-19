"""Optional timeline-check adapter.

The R4 Pack V3 discovery host is intentionally outside this M0 timeline-core
spike.  Keep the public names importable so the SDK package has a clean import
closure; a future pack integration can provide the implementation at its
declared boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from astrid.sdk.timeline.commands import CommandError


class UnsupportedCheck(CommandError):
    code = "unsupported"


@dataclass(frozen=True)
class CheckHostContext:
    host: str
    document: Any
    selected_assets: Callable[[], Iterable[Mapping[str, Any]]] | None = None


@dataclass(frozen=True)
class PackCheck:
    identity: str
    implementation_digest: str = ""
    pack_root: Any = None
    descriptor_path: str = ""
    descriptor: Mapping[str, Any] = None  # type: ignore[assignment]
    source_kind: str = "unavailable"
    eligible: bool = False
    eligibility_reason: str = "Pack V3 check host is not part of the M0 timeline core"


def discover_checks(*, project_root=None, extra_pack_roots=(), _admission_context=None):
    del project_root, extra_pack_roots, _admission_context
    return ()


def resolve_check(identity, **discovery):
    del discovery
    raise UnsupportedCheck(f"unsupported timeline check identity: {identity!r}")


def invoke_check(check, host_context, *, host="sdk"):
    del check, host_context, host
    raise UnsupportedCheck("timeline Pack V3 checks are not available in the M0 core")


__all__ = [
    "CheckHostContext",
    "PackCheck",
    "UnsupportedCheck",
    "discover_checks",
    "invoke_check",
    "resolve_check",
]
