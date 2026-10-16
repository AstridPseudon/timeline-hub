"""Select source words from an explicitly frozen transcript dependency.

This is a pure compiler-input check, not source admission or a resolver. The
command owner supplies the reference from authenticated accepted history and
the exact CAS bytes already resolved for it. Publication, shared schema/media
extent validation and document-key authority belong to the source producer.
No document, latest-version, network, path or derived word cache is consulted.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Mapping
from typing import Any

from astrid.sdk.managed_transcript import _digest
from astrid.sdk.timeline._common import TimelineEditError

_PINS = {
    "document": ("id", "version", "content_digest"),
    "snapshot": ("object_id", "sha256"),
    "subject": ("media_object_id", "media_sha256"),
    "source": ("producer_id", "source_id", "lineage_id", "revision_id", "producer_digest"),
    "clock": ("kind", "unit", "origin_seconds"),
}


def _object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TimelineEditError(f"transcript {label} must be an object")
    return value


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise TimelineEditError(f"transcript snapshot has duplicate JSON key {key!r}")
        result[key] = value
    return result


def _media_clock(clock):
    if (clock.get("kind") != "media" or clock.get("unit") != "seconds"
            or type(clock.get("origin_seconds")) not in (int, float) or clock["origin_seconds"] != 0):
        raise TimelineEditError("transcript binding requires the media-seconds clock")


def bound_source_words(
    binding: Mapping[str, Any],
    *,
    frozen_reference: Mapping[str, Any],
    snapshot_bytes: bytes,
    occurrence_id: str,
) -> tuple[dict[str, Any], ...]:
    """Return detached selected rows in source order, retaining opaque word IDs.

    ``frozen_reference`` carries schema_version and the five immutable pin
    objects in a binding, without occurrence_id/word_ids. It MUST come from the
    accepted command dependency set, not from the caller's proposed binding.
    Equality here cannot authenticate a caller-created reference. A missing
    dependency is a refusal, including during offline replay.

    Rows retain media seconds. Feed them to the existing word projection and
    its source_to_timeline_time conversion, never through a second clock. This
    helper neither mints IDs nor infers correspondence from text/segmentation.
    """
    binding = _object(binding, "binding")
    frozen_reference = _object(frozen_reference, "frozen reference")
    if (type(binding.get("schema_version")) is not int or binding["schema_version"] != 1
            or type(frozen_reference.get("schema_version")) is not int
            or frozen_reference["schema_version"] != 1):
        raise TimelineEditError("transcript binding requires schema_version 1")
    if (not isinstance(occurrence_id, str) or not occurrence_id
            or binding.get("occurrence_id") != occurrence_id):
        raise TimelineEditError("transcript binding occurrence does not match its target")
    for name, fields in _PINS.items():
        proposed = _object(binding.get(name), name)
        frozen = _object(frozen_reference.get(name), f"frozen {name}")
        if (any(field not in proposed or field not in frozen for field in fields)
                or proposed != frozen
                or any(type(proposed[field]) is not type(frozen[field]) for field in fields)):
            raise TimelineEditError(f"transcript {name} differs from frozen dependency")
        for field in fields:
            value = proposed[field]
            if name == "clock" and field == "origin_seconds":
                continue
            if name == "document" and field == "version":
                if type(value) is int and value > 0 or isinstance(value, str) and value:
                    continue
            elif isinstance(value, str) and value:
                continue
            raise TimelineEditError(f"transcript {name}.{field} is invalid")
    _media_clock(binding["clock"])
    if not isinstance(snapshot_bytes, bytes):
        raise TimelineEditError("transcript frozen snapshot bytes are required")
    try:
        actual = hashlib.sha256(snapshot_bytes).hexdigest()
        if any(_digest(value, label=label) != actual for label, value in (
                ("snapshot.sha256", binding["snapshot"]["sha256"]),
                ("document.content_digest", binding["document"]["content_digest"]))):
            raise TimelineEditError("transcript frozen snapshot digest mismatch")
        content = _object(json.loads(snapshot_bytes, object_pairs_hook=_unique_object), "snapshot")
    except (ValueError, UnicodeError) as exc:
        raise TimelineEditError(f"invalid transcript frozen snapshot: {exc}") from None
    if type(content.get("schema_version")) is not int or content["schema_version"] != 1:
        raise TimelineEditError("transcript snapshot requires schema_version 1")
    for name in ("subject", "source", "clock"):
        actual = _object(content.get(name), f"snapshot {name}")
        if any(actual.get(field) != binding[name][field] for field in _PINS[name]):
            raise TimelineEditError(f"transcript snapshot {name} differs from binding")
        if name == "clock":
            _media_clock(actual)
    rows = content.get("words")
    selected = binding.get("word_ids")
    if not isinstance(rows, list) or not isinstance(selected, list):
        raise TimelineEditError("transcript words and selected word_ids must be arrays")
    by_id = {}
    for row in rows:
        row = _object(row, "word")
        word_id = row.get("id")
        if not isinstance(word_id, str) or not word_id or word_id in by_id:
            raise TimelineEditError("transcript source word IDs must be nonempty and unique")
        start, end = row.get("start_s"), row.get("end_s")
        if (not isinstance(row.get("text"), str)
                or any(type(t) not in (int, float) or not math.isfinite(t) for t in (start, end))
                or not 0 <= start <= end):
            raise TimelineEditError("transcript words require finite source-media intervals and text")
        by_id[word_id] = row
    if (any(not isinstance(key, str) or key not in by_id for key in selected)
            or len(set(selected)) != len(selected)):
        raise TimelineEditError("transcript selection contains missing or duplicate word IDs")
    wanted = set(selected)
    if [key for key in by_id if key in wanted] != selected:
        raise TimelineEditError("transcript selected word IDs must retain source order")
    return tuple(copy.deepcopy(dict(by_id[key])) for key in selected)
