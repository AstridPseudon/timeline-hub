"""Internal Runtime snapshot handoff across the owned Python process tree.

The inherited environment anchors the binding file, not the file's own claims.
Only GenericPackHost mints it after Runtime claim and CAS materialization.
Public request JSON and backend configuration cannot carry this authority.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

SOURCE_ENV = "ASTRID_VERIFIED_TIMELINE_SOURCE"
RESERVED_SOURCE_KEYS = frozenset({"verified_source", "timeline_source", SOURCE_ENV})
_MINT = object()


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def reject_source_keys(value: Mapping[str, Any]) -> None:
    if RESERVED_SOURCE_KEYS.intersection(value):
        raise ValueError("verified timeline source is host-owned")


@dataclass(frozen=True, init=False)
class VerifiedTimelineSource:
    """Immutable anchor to the exact admitted source and prepared input pair."""

    _anchor: str

    def __init__(self, anchor: str, *, _mint: object = None) -> None:
        if _mint is not _MINT:
            raise ValueError("verified timeline source is host-owned")
        object.__setattr__(self, "_anchor", anchor)

    def read(self) -> dict[str, Any]:
        path, digest = json.loads(self._anchor)
        data = Path(path).read_bytes()
        if _digest(data) != digest:
            raise ValueError("verified source binding changed")
        return json.loads(data)

    def validate(self, timeline_path: str | Path, assets_path: str | Path | None) -> None:
        binding = self.read()
        for key, path in (("timeline", timeline_path), ("registry", assets_path)):
            expected = binding["prepared"][key]
            if path is None or str(Path(path).resolve()) != expected["path"]:
                raise ValueError(f"verified source prepared {key} path differs")
            if _digest(Path(path).read_bytes()) != expected["digest"]:
                raise ValueError(f"verified source prepared {key} bytes differ")

    def validate_snapshot(self, snapshot: Mapping[str, Any]) -> None:
        reject_source_keys(snapshot)
        original = self.read()["snapshot"]
        for key in ("config", "registry"):
            if snapshot.get(key) != original.get(key):
                raise ValueError(f"verified source capture {key} differs")
        if snapshot.get("metadata", {}).get("capture_authority") != original.get("metadata", {}).get("capture_authority"):
            raise ValueError("verified source capture authority differs")


class PreparedTimelineInputs(dict[str, Any]):
    """Keep authority outside the public executor input namespace."""

    timeline_source: VerifiedTimelineSource | None = None


def mint_prepared_source(
    *, ref: Mapping[str, Any], authority: Mapping[str, Any], snapshot: Mapping[str, Any],
    timeline_path: str | Path, assets_path: str | Path, attempt: Path,
) -> VerifiedTimelineSource:
    """Called only at the Runtime-admitted host materialization boundary."""
    for name, field in (("project_id", "project_id"), ("timeline_id", "timeline_id"),
                        ("revision_id", "parent_revision_id")):
        if not isinstance(ref.get(name), str) or not ref[name] or ref[name] != authority.get(field):
            raise ValueError(f"verified source {name} differs from admitted authority")
    if ref.get("source_kind") not in {"revision", "working_copy"}:
        raise ValueError("verified source requires a revision or working copy")
    revision_digest = ref.get("revision_digest")
    if (not isinstance(revision_digest, str) or not revision_digest.startswith("sha256:")
            or len(revision_digest) != 71 or any(c not in "0123456789abcdef" for c in revision_digest[7:])):
        raise ValueError("verified source requires an admitted revision digest")
    if ref["source_kind"] == "revision":
        if revision_digest != authority.get("parent_content_digest"):
            raise ValueError("verified source revision digest differs")
    else:
        marker = snapshot.get("metadata", {}).get("working_copy", {})
        base = marker.get("base_parent", {})
        expected = {"candidate_digest": marker.get("candidate_digest"),
                    "publication_digest": marker.get("publication_digest"),
                    "base_revision_id": base.get("revision_id"),
                    "base_revision_digest": base.get("content_digest")}
        if (marker.get("candidate_parent_revision_id") != ref["revision_id"]
                or expected != ref.get("working_copy")
                or revision_digest != expected["candidate_digest"]):
            raise ValueError("verified source working copy differs")
    if authority.get("snapshot_digest") is not None and authority["snapshot_digest"] != ref.get("digest"):
        raise ValueError("verified source snapshot digest differs from Runtime authority")
    prepared = {}
    for key, path in (("timeline", timeline_path), ("registry", assets_path)):
        resolved = Path(path).resolve(strict=True)
        resolved.relative_to(attempt.resolve())
        prepared[key] = {"path": str(resolved), "digest": _digest(resolved.read_bytes())}
    binding = {"ref": dict(ref), "authority": dict(authority), "snapshot": dict(snapshot), "prepared": prepared}
    data = json.dumps(binding, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    path = attempt.resolve() / "inputs" / "verified-timeline-source.json"
    path.write_bytes(data)
    path.chmod(0o600)
    return VerifiedTimelineSource(json.dumps([str(path), _digest(data)]), _mint=_MINT)


def inherited_source(timeline_path: str | Path, assets_path: str | Path | None = None) -> VerifiedTimelineSource | None:
    anchor = os.environ.get(SOURCE_ENV)
    if anchor is None:
        return None
    source = VerifiedTimelineSource(anchor, _mint=_MINT)
    source.validate(timeline_path, assets_path)
    return source


def source_for_timeline(timeline_path: str | Path) -> VerifiedTimelineSource | None:
    """Serializer entry: require the same pair even if only one path was passed."""
    anchor = os.environ.get(SOURCE_ENV)
    if anchor is None:
        return None
    source = VerifiedTimelineSource(anchor, _mint=_MINT)
    source.validate(timeline_path, source.read()["prepared"]["registry"]["path"])
    return source
