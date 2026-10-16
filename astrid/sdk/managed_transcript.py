"""Shared source record and Runtime input helpers for managed transcripts."""

from __future__ import annotations

import copy
import json
import math
import re
from collections.abc import Mapping
from importlib.resources import files
from typing import Any, Literal, NotRequired, TypedDict, cast

import jsonschema

from astrid.sdk.documents import stable_document_id

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SHA256_WITH_PREFIX = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")

TRANSCRIPT_DOCUMENT_KIND = "media.transcript/v1"
TRANSCRIPT_SCHEMA_ID = TRANSCRIPT_DOCUMENT_KIND
TRANSCRIPT_RECORD_SCHEMA: dict[str, Any] = json.loads(
    files("astrid")
    .joinpath("packs")
    .joinpath("media")
    .joinpath("schemas")
    .joinpath("transcript-v1.json")
    .read_text(encoding="utf-8")
)
jsonschema.Draft202012Validator.check_schema(TRANSCRIPT_RECORD_SCHEMA)
_TRANSCRIPT_VALIDATOR = jsonschema.Draft202012Validator(TRANSCRIPT_RECORD_SCHEMA)


class TranscriptSubject(TypedDict):
    """Canonical immutable source-media identity."""

    media_object_id: str
    media_sha256: str


class TranscriptSource(TypedDict):
    """Stable transcript stream identity plus one content revision."""

    producer_id: str
    source_id: str
    lineage_id: str
    revision_id: str
    producer_digest: str
    parent_revision_id: NotRequired[str]


class MediaSecondsClock(TypedDict):
    kind: Literal["media"]
    unit: Literal["seconds"]
    origin_seconds: Literal[0]


class TranscriptWord(TypedDict):
    id: str
    text: str
    start_s: float
    end_s: float


class TranscriptSegment(TypedDict):
    id: str
    word_ids: list[str]


class TranscriptRecord(TypedDict):
    """Validated flat ``media.transcript/v1`` document content."""

    schema_version: Literal[1]
    subject: TranscriptSubject
    source: TranscriptSource
    clock: MediaSecondsClock
    words: list[TranscriptWord]
    segments: list[TranscriptSegment]
    metadata: NotRequired[dict[str, Any]]
    provenance: NotRequired[dict[str, Any]]


class TranscriptValidationError(ValueError):
    """A transcript source record does not satisfy its shared v1 contract."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _nonblank(mapping: Mapping[str, Any], key: str, *, label: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}.{key} must be a non-empty string")
    return value


def transcript_document_id(
    project: str,
    subject: Mapping[str, Any],
    source: Mapping[str, Any],
) -> str:
    """Return the stable ID for one project, immutable media subject, and source stream.

    Revision and content fields are deliberately excluded: publishing a new
    revision of the same producer/source updates the same project document.
    ``stable_document_id`` owns the outer project/kind/name serialization.
    """

    if not isinstance(subject, Mapping):
        raise TypeError("subject must be a mapping")
    if not isinstance(source, Mapping):
        raise TypeError("source must be a mapping")
    media_object_id = _nonblank(subject, "media_object_id", label="subject")
    media_sha256 = _nonblank(subject, "media_sha256", label="subject")
    if not _SHA256_WITH_PREFIX.fullmatch(media_sha256):
        raise ValueError("subject.media_sha256 must be a lowercase SHA-256 digest")
    media_sha256 = media_sha256.removeprefix("sha256:")
    producer_id = _nonblank(source, "producer_id", label="source")
    source_id = _nonblank(source, "source_id", label="source")
    identity_name = _canonical_json(
        {
            "subject": {
                "media_object_id": media_object_id,
                "media_sha256": media_sha256,
            },
            "source": {"producer_id": producer_id, "source_id": source_id},
        }
    )
    return stable_document_id(project, TRANSCRIPT_DOCUMENT_KIND, identity_name)


def validate_transcript_record(
    record: Mapping[str, Any],
    *,
    media_duration_s: float | None = None,
) -> TranscriptRecord:
    """Validate and losslessly copy a v1 record, including its opaque metadata.

    Pass an admitted source-media duration when the caller already has one; the
    pure validator does not discover media or infer an extent on its own.
    """

    if not isinstance(record, Mapping):
        raise TranscriptValidationError("transcript record must be a mapping")
    if media_duration_s is not None and (
        isinstance(media_duration_s, bool)
        or not isinstance(media_duration_s, (int, float))
        or not math.isfinite(float(media_duration_s))
        or media_duration_s < 0
    ):
        raise TranscriptValidationError("media_duration_s must be finite and non-negative")
    try:
        candidate = copy.deepcopy(dict(record))
    except Exception as exc:  # noqa: BLE001 - opaque values must still be JSON-copyable
        raise TranscriptValidationError(f"transcript record cannot be copied: {exc}") from exc

    errors = sorted(
        _TRANSCRIPT_VALIDATOR.iter_errors(candidate),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "record"
        raise TranscriptValidationError(f"{location}: {error.message}")

    words = candidate["words"]
    word_ids = [word["id"] for word in words]
    if any(not word_id.strip() for word_id in word_ids):
        raise TranscriptValidationError("word IDs must be non-empty strings")
    if len(word_ids) != len(set(word_ids)):
        raise TranscriptValidationError("word IDs must be unique")
    if any(not word["text"].strip() for word in words):
        raise TranscriptValidationError("word text must be non-empty")
    for index, word in enumerate(words):
        start_s, end_s = word["start_s"], word["end_s"]
        if not math.isfinite(float(start_s)) or not math.isfinite(float(end_s)):
            raise TranscriptValidationError(f"words[{index}] interval must be finite")
        if start_s < 0 or start_s > end_s:
            raise TranscriptValidationError(f"words[{index}] must satisfy 0 <= start_s <= end_s")
        if media_duration_s is not None and end_s > media_duration_s:
            raise TranscriptValidationError(
                f"words[{index}].end_s exceeds the admitted media duration"
            )

    segment_ids = [segment["id"] for segment in candidate["segments"]]
    if any(not segment_id.strip() for segment_id in segment_ids):
        raise TranscriptValidationError("segment IDs must be non-empty strings")
    if len(segment_ids) != len(set(segment_ids)):
        raise TranscriptValidationError("segment IDs must be unique")
    segmented_word_ids = [
        word_id
        for segment in candidate["segments"]
        for word_id in segment["word_ids"]
    ]
    if segmented_word_ids != word_ids:
        raise TranscriptValidationError(
            "segments must partition words exactly once and in source order"
        )

    try:
        _canonical_json(candidate)
    except (TypeError, ValueError, UnicodeError) as exc:
        raise TranscriptValidationError(f"transcript record is not canonical JSON: {exc}") from exc
    return cast(TranscriptRecord, candidate)


def canonical_transcript_json(
    record: Mapping[str, Any],
    *,
    media_duration_s: float | None = None,
) -> str:
    """Return the stable JSON text for a validated v1 source record."""

    validated = validate_transcript_record(record, media_duration_s=media_duration_s)
    return _canonical_json(validated)


def _digest(value: Any, *, label: str) -> str:
    raw = str(value or "").removeprefix("sha256:")
    if not _SHA256.fullmatch(raw):
        raise ValueError(f"transcript {label} must be a sha256 digest")
    return raw


def transcript_input_from_snapshot(
    config: Mapping[str, Any],
    registry: Mapping[str, Any] | None = None,
) -> dict[str, str] | None:
    """Return the host-managed transcript input for ``config.app.transcript``.

    The returned digest is derived only from the canonical Runtime snapshot.
    The host later fetches those bytes from Runtime CAS and the visualizer
    verifies them against the declaration; there is intentionally no local
    filename or sidecar discovery here.
    """

    app = config.get("app")
    if not isinstance(app, Mapping) or "transcript" not in app:
        return None
    declaration = app.get("transcript")
    if not isinstance(declaration, Mapping):
        raise ValueError("config.app.transcript must be an object")
    for key in ("source_id", "source_version", "producer", "file"):
        if not isinstance(declaration.get(key), str) or not declaration[key].strip():
            raise ValueError(f"config.app.transcript.{key} is required")
    media = declaration.get("media")
    if not isinstance(media, Mapping):
        raise ValueError("config.app.transcript.media is required")
    identities = [key for key in ("asset_key", "source_id") if isinstance(media.get(key), str) and media[key].strip()]
    if len(identities) != 1:
        raise ValueError("config.app.transcript.media requires exactly one identity")
    digest = _digest(declaration.get("sha256"), label="sha256")
    media_digest = media.get("sha256")
    if media_digest is not None:
        media_digest = _digest(media_digest, label="media.sha256")
        if identities == ["asset_key"] and isinstance(registry, Mapping):
            assets = registry.get("assets")
            asset = assets.get(media["asset_key"]) if isinstance(assets, Mapping) else None
            if not isinstance(asset, Mapping):
                raise ValueError(
                    f"config.app.transcript.media.asset_key {media['asset_key']!r} is not in the canonical registry"
                )
            admitted = next(
                (asset.get(key) for key in ("content_sha256", "digest", "sha256", "hash") if asset.get(key)),
                None,
            )
            if admitted is not None and _digest(admitted, label="registry media") != media_digest:
                raise ValueError("config.app.transcript.media.sha256 does not match the canonical media hash")
    return {
        "digest": "sha256:" + digest,
        "object_id": "sha256:" + digest,
    }


__all__ = [
    "MediaSecondsClock",
    "TRANSCRIPT_DOCUMENT_KIND",
    "TRANSCRIPT_RECORD_SCHEMA",
    "TRANSCRIPT_SCHEMA_ID",
    "TranscriptRecord",
    "TranscriptSegment",
    "TranscriptSource",
    "TranscriptSubject",
    "TranscriptValidationError",
    "TranscriptWord",
    "canonical_transcript_json",
    "transcript_document_id",
    "transcript_input_from_snapshot",
    "validate_transcript_record",
]
