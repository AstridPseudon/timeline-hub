"""Pure composition planning and storage accounting for ``chiptune.compose``.

The planner owns input normalization and the section/hit/grid plan consumed by
both the estimator and the renderer. It does not allocate audio samples or
touch the filesystem.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from astrid.core._shared.result_manifest import build_manifest
from astrid.core.contracts.errors import AstridError
from astrid.packs.chiptune.actions import _synth as syn

_PARAM_NAMES = frozenset({
    "duration_s", "bpm", "key", "seed", "sections", "hits", "duck", "vo_mask",
    "duck_db", "master_db", "style", "mutes",
})
# measure_db rounds to three decimals in [-120.0, PEAK_CEILING_DB]. Its widest
# JSON float spelling is eight ASCII bytes (for example, ``-100.123``).
_JSON_METRIC_BOUND = -100.123
_TIMESTAMP_BOUND = "2000-01-01T00:00:00.000000+00:00"
_SHA256_PLACEHOLDER = "sha256:" + "0" * 64
_MAX_SAFE_INTEGER = (1 << 53) - 1


@dataclass(frozen=True)
class CompositionPlan:
    """Validated canonical inputs and one renderer-ready composition plan."""

    duration_s: float
    sample_count: int
    bpm: float
    key: str
    root_pc: int
    mode: str
    seed: int
    style: str
    duck_db: float
    master_db: float
    raw_sections: list[dict[str, Any]]
    raw_hits: list[Any]
    raw_duck: Any
    raw_vo_mask: Any
    sections: list[dict[str, Any]]
    planned_sections: list[dict[str, Any]]
    hit_events: list[tuple[float, str]]
    duck_items: list[tuple[float, float, float]]
    vo_mask: list[tuple[float, float]]
    mute_windows: list[tuple[float, float]]
    beats: list[float]
    downbeats: list[float]
    bars: list[float]
    bar_s: float
    canonical_key: str
    manifest_inputs: dict[str, Any]


@dataclass(frozen=True)
class StorageEstimate:
    """Exact output sizes and conservative peak scratch for one composition."""

    output_breakdown: Mapping[str, int]
    scratch_breakdown: Mapping[str, int]
    output_bytes: int
    scratch_bytes: int
    total_bytes: int


def _json_text(value: Any, *, label: str) -> str:
    try:
        return json.dumps(value, allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise AstridError(f"{label} must contain only finite JSON values") from exc


def _finite_float(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise AstridError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise AstridError(f"{name} must be a finite number") from exc
    if not math.isfinite(number):
        raise AstridError(f"{name} must be a finite number")
    return number


def parse_duck(raw: Any, default_db: float) -> list[tuple[float, float, float]]:
    items = syn.parse_structured(raw, "duck") or []
    if not isinstance(items, list):
        raise AstridError("duck must be a JSON array of {start_s, end_s, gain_db}")
    out: list[tuple[float, float, float]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or "start_s" not in item or "end_s" not in item:
            raise AstridError(f"duck[{index}] needs start_s and end_s")
        out.append((
            _finite_float(item["start_s"], f"duck[{index}].start_s"),
            _finite_float(item["end_s"], f"duck[{index}].end_s"),
            _finite_float(item.get("gain_db", default_db), f"duck[{index}].gain_db"),
        ))
    return out


def parse_vo_mask(raw: Any) -> list[tuple[float, float]]:
    items = syn.parse_structured(raw, "vo_mask") or []
    if not isinstance(items, list):
        raise AstridError("vo_mask must be a JSON array of [start_s, end_s] pairs")
    out: list[tuple[float, float]] = []
    for index, item in enumerate(items):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise AstridError(f"vo_mask[{index}] must be [start_s, end_s]")
        out.append((
            _finite_float(item[0], f"vo_mask[{index}][0]"),
            _finite_float(item[1], f"vo_mask[{index}][1]"),
        ))
    return out


def parse_mutes(raw: Any) -> list[tuple[float, float]]:
    items = syn.parse_structured(raw, "mutes") or []
    if not isinstance(items, list):
        raise AstridError("mutes must be a JSON array of [start_s, end_s] pairs")
    out: list[tuple[float, float]] = []
    for index, item in enumerate(items):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise AstridError(f"mutes[{index}] must be [start_s, end_s]")
        out.append((
            _finite_float(item[0], f"mutes[{index}][0]"),
            _finite_float(item[1], f"mutes[{index}][1]"),
        ))
    return out


def build_composition_plan(params: Mapping[str, Any]) -> CompositionPlan:
    """Validate canonical action params and build the shared renderer plan.

    ``params`` is the action's parameter mapping, with omitted optional fields
    receiving the same defaults as ``compose.run`` and the declaration.
    Unknown top-level fields are refused; raw extras inside structured values
    remain intact when the manifest records them.
    """
    if not isinstance(params, Mapping) or any(type(key) is not str for key in params):
        raise AstridError("chiptune.compose params must be a JSON object with string keys")
    params_text = _json_text(dict(params), label="chiptune.compose params")
    try:
        values = json.loads(params_text)
    except (TypeError, ValueError) as exc:  # defensive; _json_text already checks this.
        raise AstridError("chiptune.compose params must be finite JSON") from exc
    unknown = set(values) - _PARAM_NAMES
    if unknown:
        raise AstridError(f"unknown chiptune.compose param(s): {', '.join(sorted(unknown))}")
    if "duration_s" not in values or "sections" not in values:
        raise AstridError("duration_s and sections are required")

    duration_s = _finite_float(values["duration_s"], "duration_s")
    bpm = _finite_float(values.get("bpm", 132), "bpm")
    duck_db = _finite_float(values.get("duck_db", -10), "duck_db")
    master_db = _finite_float(values.get("master_db", -16), "master_db")
    if not 30.0 <= bpm <= 240.0:
        raise AstridError("bpm must be between 30 and 240", recovery_command="pass bpm such as 132")
    if not 1.0 <= duration_s <= 3600.0:
        raise AstridError("duration_s must be between 1 and 3600", recovery_command="pass duration_s in seconds")

    seed = values.get("seed", 1)
    if type(seed) is not int or seed < 0:
        raise AstridError("seed must be an integer supported by numpy's default random generator")
    key = values.get("key", "A minor")
    style = values.get("style", "nes")
    if not isinstance(key, str):
        raise AstridError("key must be a string")
    if not isinstance(style, str) or style not in syn.STYLES:
        raise AstridError(f"unsupported style {style!r}", valid_options=list(syn.STYLES), recovery_command="use style nes")
    root_pc, mode = syn.parse_key(key)

    raw_sections = syn.parse_structured(values["sections"], "sections")
    raw_hits = syn.parse_hits(values.get("hits"))
    raw_duck = syn.parse_structured(values.get("duck"), "duck")
    raw_vo_mask = syn.parse_structured(values.get("vo_mask"), "vo_mask")
    for index, section in enumerate(raw_sections if isinstance(raw_sections, list) else []):
        if isinstance(section, Mapping):
            for field, default in (("start_s", None), ("end_s", None), ("energy", 0.5)):
                if field in section or default is None:
                    _finite_float(section.get(field), f"sections[{index}].{field}")
            cadence = section.get("cadence_bars", 0) or 0
            if isinstance(cadence, bool):
                raise AstridError(f"sections[{index}].cadence_bars must be a finite integer")
            try:
                if not math.isfinite(float(cadence)):
                    raise AstridError(f"sections[{index}].cadence_bars must be finite")
            except (TypeError, ValueError, OverflowError) as exc:
                raise AstridError(f"sections[{index}].cadence_bars must be a finite integer") from exc
    sections = syn.validate_sections(raw_sections, duration_s)
    hit_events = syn.normalize_hits(raw_hits, duration_s)
    duck_items = parse_duck(raw_duck, duck_db)
    vo_mask = parse_vo_mask(raw_vo_mask)
    mute_windows = parse_mutes(values.get("mutes"))
    for start_s, end_s in mute_windows:
        if not 0.0 <= start_s < end_s <= duration_s:
            raise AstridError(f"mute [{start_s}, {end_s}] must satisfy 0 <= start < end <= duration_s")

    sample_count = int(round(duration_s * syn.SAMPLE_RATE))
    beat_s = 60.0 / bpm
    bar_s = 4.0 * beat_s
    planned_sections = syn._plan_sections(sections, bar_s, duration_s)
    beats: set[float] = set()
    downbeats: set[float] = set()
    phrase_starts: set[float] = set()
    for section in planned_sections:
        origin = section["start_s"]
        span = section["end_s"] - section["start_s"]
        section["chords"] = (
            syn._section_chords(mode, section["mood"], section["n_bars"], section["cadence_bars"])
            if section["mood"] != "silent" else []
        )
        beats.update(round(origin + k * beat_s, 6) for k in range(int(math.ceil(span / beat_s - 1e-9))))
        downbeats.update(round(origin + k * bar_s, 6) for k in range(section["n_bars"]))
        phrase_starts.update(
            round(origin + k * 4 * bar_s, 6)
            for k in range(int(math.ceil(section["n_bars"] / 4)))
        )

    canonical_key = f"{syn._NOTE_NAMES[root_pc]} {mode}"
    manifest_inputs = {
        "duration_s": duration_s,
        "bpm": bpm,
        "key": key,
        "seed": seed,
        "sections": raw_sections,
        "hits": raw_hits,
        "duck": raw_duck,
        "vo_mask": raw_vo_mask,
        "duck_db": duck_db,
        "master_db": master_db,
        "style": style,
        "mutes": mute_windows,
    }
    _json_text(manifest_inputs, label="serialized chiptune inputs")
    return CompositionPlan(
        duration_s=duration_s,
        sample_count=sample_count,
        bpm=bpm,
        key=key,
        root_pc=root_pc,
        mode=mode,
        seed=seed,
        style=style,
        duck_db=duck_db,
        master_db=master_db,
        raw_sections=raw_sections,
        raw_hits=raw_hits,
        raw_duck=raw_duck,
        raw_vo_mask=raw_vo_mask,
        sections=sections,
        planned_sections=planned_sections,
        hit_events=hit_events,
        duck_items=duck_items,
        vo_mask=vo_mask,
        mute_windows=mute_windows,
        beats=sorted(beats),
        downbeats=sorted(downbeats),
        bars=sorted(phrase_starts),
        bar_s=bar_s,
        canonical_key=canonical_key,
        manifest_inputs=manifest_inputs,
    )


def build_section_metadata(plan: CompositionPlan) -> list[dict[str, Any]]:
    """Build the planned section rows, before renderer-measured level fields."""
    outputs: list[dict[str, Any]] = []
    for section in plan.planned_sections:
        outputs.append({
            "index": section["index"],
            "mood": section["mood"],
            "energy": round(section["energy"], 4),
            "start_s": round(section["start_s"], 6),
            "end_s": round(section["end_s"], 6),
            "grid_origin_s": round(section["start_s"], 6),
            "bars": section["n_bars"],
            "cadence_bars": min(section["cadence_bars"], section["n_bars"]),
            "chords": [syn._chord_name(plan.root_pc, chord) for chord in section["chords"]],
        })
    return outputs


def build_section_outputs(
    plan: CompositionPlan,
    section_metrics: Sequence[tuple[float, float]] | None = None,
) -> list[dict[str, Any]]:
    """Build section rows with the two measured fields used by both JSON files."""
    metrics = section_metrics or [(_JSON_METRIC_BOUND, _JSON_METRIC_BOUND)] * len(plan.planned_sections)
    if len(metrics) != len(plan.planned_sections):
        raise AstridError("section metrics do not match the composition plan")
    outputs = build_section_metadata(plan)
    for section, (peak_dbfs, rms_dbfs) in zip(outputs, metrics, strict=True):
        section["peak_dbfs"] = _finite_float(peak_dbfs, "section peak_dbfs")
        section["rms_dbfs"] = _finite_float(rms_dbfs, "section rms_dbfs")
    return outputs


def build_beats_document(
    plan: CompositionPlan,
    sections_out: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": "chiptune.compose",
        "bpm": plan.bpm,
        "key": plan.canonical_key,
        "seed": plan.seed,
        "duration_s": round(plan.sample_count / syn.SAMPLE_RATE, 6),
        "sample_rate": syn.SAMPLE_RATE,
        "bar_s": round(plan.bar_s, 6),
        "bars_per_phrase": 4,
        "beats": plan.beats,
        "downbeats": plan.downbeats,
        "bars": plan.bars,
        "sections": list(sections_out),
        "hits": [{"t": round(time_s, 6), "kind": kind} for time_s, kind in plan.hit_events],
        "mutes": [[round(start_s, 6), round(end_s, 6)] for start_s, end_s in plan.mute_windows],
    }


def build_renderer_metadata(plan: CompositionPlan) -> dict[str, Any]:
    """Return the planned metadata shape consumed by the audio renderer."""
    return {
        "bpm": plan.bpm,
        "bar_s": round(plan.bar_s, 6),
        "beats": plan.beats,
        "downbeats": plan.downbeats,
        "bars": plan.bars,
        "sections": build_section_metadata(plan),
        "hits": [{"t": round(time_s, 6), "kind": kind} for time_s, kind in plan.hit_events],
        "mutes": [[round(start_s, 6), round(end_s, 6)] for start_s, end_s in plan.mute_windows],
        "key": plan.canonical_key,
    }


def build_result_manifest(
    plan: CompositionPlan,
    *,
    sections_out: Sequence[Mapping[str, Any]],
    created: str,
    peak_dbfs: float,
    rms_dbfs: float,
) -> dict[str, Any]:
    return build_manifest(
        kind="chiptune.compose",
        inputs=plan.manifest_inputs,
        outputs=[
            {
                "name": "music",
                "path": "music.wav",
                "type": "file",
                "artifact_type": "audio",
                "role": "result",
                "is_primary": True,
                "media_type": "audio/wav",
                "duration_seconds": round(plan.sample_count / syn.SAMPLE_RATE, 6),
            },
            {"name": "beats", "path": "beats.json", "type": "file", "role": "auxiliary", "media_type": "application/json"},
        ],
        created=created,
        sample_rate=syn.SAMPLE_RATE,
        channels=2,
        peak_dbfs=_finite_float(peak_dbfs, "peak_dbfs"),
        rms_dbfs=_finite_float(rms_dbfs, "rms_dbfs"),
        sections=list(sections_out),
    )


def _json_file_bytes(payload: Any) -> int:
    """Match atomic_io.write_json_atomic: sorted, two-space JSON plus LF."""
    text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    return len(text.encode("utf-8"))


def _estimated_manifest(
    plan: CompositionPlan,
    *,
    sections_out: Sequence[Mapping[str, Any]],
    music_bytes: int,
    beats_bytes: int,
) -> dict[str, Any]:
    # These are the exact fields complete_output_metadata adds for the two
    # regular files. Hash content is data-dependent but its SHA-256 form is 71
    # ASCII bytes, and the byte counts are already known without reading files.
    manifest = build_result_manifest(
        plan,
        sections_out=sections_out,
        created=_TIMESTAMP_BOUND,
        peak_dbfs=_JSON_METRIC_BOUND,
        rms_dbfs=_JSON_METRIC_BOUND,
    )
    for output, size in zip(manifest["outputs"], (music_bytes, beats_bytes), strict=True):
        output["content_hash"] = _SHA256_PLACEHOLDER
        output["bytes"] = size
    return manifest


def estimate_compose_storage(params: Mapping[str, Any]) -> StorageEstimate:
    """Return the producer-owned parameter-sensitive whole-output estimate.

    Output JSON sizes are serializer-derived. Metrics use their actual format's
    widest finite value (an eight-byte spelling, ``-100.123``); the creation
    timestamp uses the 32-byte UTC ``datetime.isoformat()`` maximum. Scratch
    follows the existing command: no file inputs, persisted progress/logs, or
    host copy stage; its two sequential atomic JSON writes each use one sibling
    temp. The peak is the larger temp, not their sum.
    """
    plan = build_composition_plan(params)
    section_metrics = [(_JSON_METRIC_BOUND, _JSON_METRIC_BOUND)] * len(plan.planned_sections)
    sections_out = build_section_outputs(plan, section_metrics)
    beats_bytes = _json_file_bytes(build_beats_document(plan, sections_out))
    music_bytes = 4 * plan.sample_count + 44
    manifest_bytes = _json_file_bytes(_estimated_manifest(
        plan,
        sections_out=sections_out,
        music_bytes=music_bytes,
        beats_bytes=beats_bytes,
    ))
    output_breakdown = {
        "music_wav_bytes": music_bytes,
        "beats_json_bytes": beats_bytes,
        "manifest_json_bytes": manifest_bytes,
    }
    # All of these are zero for this exact action implementation: it has no
    # file/CAS ports, emits no progress, captures child streams in host memory,
    # and writes directly into the attempt's outputs directory.
    scratch_breakdown = {
        "atomic_json_temporary_peak_bytes": max(beats_bytes, manifest_bytes),
        "input_staging_bytes": 0,
        "control_staging_bytes": 0,
        "captured_log_files_bytes": 0,
        "host_evidence_files_bytes": 0,
        "host_copy_artifacts_bytes": 0,
    }
    output_bytes = sum(output_breakdown.values())
    scratch_bytes = sum(scratch_breakdown.values())
    total_bytes = output_bytes + scratch_bytes
    if any(value > _MAX_SAFE_INTEGER for value in (*output_breakdown.values(), *scratch_breakdown.values(), output_bytes, scratch_bytes, total_bytes)):
        raise AstridError("chiptune.compose storage estimate exceeds the interoperable safe-integer range")
    return StorageEstimate(
        output_breakdown=output_breakdown,
        scratch_breakdown=scratch_breakdown,
        output_bytes=output_bytes,
        scratch_bytes=scratch_bytes,
        total_bytes=total_bytes,
    )


__all__ = [
    "CompositionPlan",
    "StorageEstimate",
    "build_beats_document",
    "build_composition_plan",
    "build_result_manifest",
    "build_renderer_metadata",
    "build_section_metadata",
    "build_section_outputs",
    "estimate_compose_storage",
    "parse_duck",
    "parse_mutes",
    "parse_vo_mask",
]
