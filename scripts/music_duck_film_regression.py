#!/usr/bin/env python3
"""Compare music.duck's gain curve with the approved R5 film mix.

The approved render is treated as read-only reference evidence. This script
does not edit a timeline or write anywhere beside the explicitly selected
scratch output directory.

Run from the Astrid checkout with its runtime environment active:

    python scripts/music_duck_film_regression.py --output-dir /private/tmp/...

Defaults point at the isolated film-mix scratch inputs used by the R5
regression. Paths can be overridden for a repeatable run elsewhere.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import wave
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from astrid.packs.music.actions.duck._audio import (
    Audio,
    integrated,
    load_audio,
    weighted_power,
)
from astrid.packs.music.actions.duck._audio import (
    moments as k_moments,
)
from astrid.packs.music.actions.duck.core import (
    DuckParameters,
    Placement,
    duck_audio,
    placed_samples,
)

SCRATCH = Path("/private/tmp/claude-501/-Users-hannahomalley/90fe1605-2f12-40a0-8c8d-452d3560fb7b/scratchpad/film-mix")
ALIGN = Path("/private/tmp/claude-501/-Users-hannahomalley/b08ce372-79ba-45f5-ab10-ef1283623db6/scratchpad/film-r5/spine/align/words")
DEFAULT_MAP = SCRATCH / "audio_map.json"
DEFAULT_MIX = SCRATCH / "R5-MUSIC-MIX-B8S3.wav"
DEFAULT_REFERENCE_GAIN = SCRATCH / "env_R5-MUSIC-MIX-B8S3.npy"
DEFAULT_MUSIC = Path("/private/tmp/claude-501/-Users-hannahomalley/b08ce372-79ba-45f5-ab10-ef1283623db6/scratchpad/film-r5/music/r5v10/R5-MUSIC-SONG-V10.wav")


def _read_pcm16(path: Path) -> tuple[np.ndarray, int]:
    """Read a PCM16 WAV as float32 [frame, channel] samples."""
    with wave.open(str(path), "rb") as source:
        if source.getcomptype() != "NONE" or source.getsampwidth() != 2:
            raise ValueError(f"expected uncompressed PCM16 WAV: {path}")
        channels, rate, frames = source.getnchannels(), source.getframerate(), source.getnframes()
        data = np.frombuffer(source.readframes(frames), dtype="<i2").reshape(-1, channels)
    return data.astype(np.float32) / 32768.0, rate


def _moments(power: np.ndarray, rate: int, times: np.ndarray) -> np.ndarray:
    """Return centered 400 ms BS.1770 K-weighted moments at requested times."""
    return k_moments(power, rate, times)


def _line_evidence(audio_map: dict[str, Any], words_dir: Path) -> list[dict[str, Any]]:
    """Resolve each VO clip to the aligned speech span used by build_s.py.

    N04b and N34 have no word JSON in the supplied evidence. For those clips,
    reproduce build_s.py's 20 ms, 95th-percentile-minus-25 dB energy fallback.
    """
    lines = []
    for clip in audio_map["vo"]:
        match = re.search(r"N\d+[a-z]?", clip["asset"])
        if not match:
            raise ValueError(f"cannot identify VO line number in {clip['asset']}")
        key = match.group(0)
        words_file = words_dir / f"{key}.words.json"
        start, end = float(clip["timeline_start"]), float(clip["timeline_end"])
        aligned = False
        if words_file.is_file():
            words = json.loads(words_file.read_text(encoding="utf-8"))
            if words:
                start = float(clip["timeline_start"]) + min(float(word["s"]) for word in words) - 0.03
                end = float(clip["timeline_start"]) + max(float(word["e"]) for word in words) + 0.05
                aligned = True
        if not aligned:
            voice_audio = load_audio(Path(clip["source_path"]))
            voice, rate = voice_audio.samples, voice_audio.rate
            frame = round(0.02 * rate)
            mono = voice.mean(axis=1)
            usable = len(mono) // frame
            if usable:
                blocks = mono[:usable * frame].reshape(usable, frame)
                db = 20 * np.log10(np.sqrt(np.mean(np.square(blocks.astype(np.float64)), axis=1)) + 1e-9)
                active = np.flatnonzero(db > np.percentile(db, 95) - 25)
                if active.size:
                    start = float(clip["timeline_start"]) + int(active[0]) * 0.02
                    end = float(clip["timeline_start"]) + (int(active[-1]) + 1) * 0.02
        lines.append({
            "clip_id": clip["clip_id"],
            "asset": clip["asset"],
            "start_s": max(0.0, start),
            "end_s": min(float(clip["timeline_end"]), end),
            "aligned_words": aligned,
            "clip": clip,
            "words_path": str(words_file) if words_file.is_file() else None,
        })
    return sorted(lines, key=lambda row: row["start_s"])


def _percentile(values: np.ndarray, q: float) -> float:
    return float(np.percentile(values, q)) if values.size else float("nan")


def _curve_motion(curve: np.ndarray, eligible: np.ndarray, times: np.ndarray) -> dict[str, float]:
    """Measure local slope and one-second movement on reliable 10 ms samples."""
    dt = float(np.median(np.diff(times)))
    pair_mask = eligible[1:] & eligible[:-1]
    slope = np.diff(curve) / np.diff(times)
    width = round(1.0 / dt)
    windows = np.lib.stride_tricks.sliding_window_view(curve, width + 1)
    valid = np.lib.stride_tricks.sliding_window_view(eligible, width + 1).all(axis=1)
    changes = np.abs(curve[width:] - curve[:-width])
    ranges = windows.max(axis=1) - windows.min(axis=1)
    choices = np.flatnonzero(valid)
    max_change = int(choices[np.argmax(changes[valid])])
    max_range = int(choices[np.argmax(ranges[valid])])
    return {
        "max_abs_slope_db_per_s": float(np.max(np.abs(slope[pair_mask]))),
        "max_1s_endpoint_change_db": float(changes[max_change]),
        "max_1s_endpoint_change_at_s": float(times[max_change]),
        "max_1s_range_db": float(ranges[max_range]),
        "max_1s_range_at_s": float(times[max_range]),
    }


def _hann_smooth_gain(curve: np.ndarray, *, dt: float = 0.01, smooth_s: float = 1.0) -> np.ndarray:
    """Mirror build_s.py's Hann smoothing for the measured implied gain curve."""
    n = int(smooth_s / dt) | 1
    window = np.hanning(n + 2)[1:-1]
    window /= window.sum()
    padded = np.concatenate((np.full(n, curve[0]), curve, np.full(n, curve[-1])))
    return np.convolve(padded, window, mode="same")[n:-n]


def _extract_curve(result: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """Normalize the intentionally small DuckResult curve API to numpy arrays."""
    times = np.asarray(result.times, dtype=np.float64)
    gain = np.asarray(result.gain_db, dtype=np.float64)
    target = getattr(result, "target_db", None)
    target_arr = None if target is None else np.asarray(target, dtype=np.float64)
    if times.ndim != 1 or gain.ndim != 1 or times.size != gain.size:
        raise ValueError("duck_audio returned incompatible times and gain_db arrays")
    return times, gain, target_arr


def _csv_write(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> dict[str, Any]:
    audio_map = json.loads(args.audio_map.read_text(encoding="utf-8"))
    music_clip = audio_map["music"][0]
    music_path = args.music.expanduser().resolve()
    approved_path = args.approved_mix.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # The only generated audio is an isolated regression artifact. Source and
    # approved WAVs are read as evidence and are never opened for writing.
    action_wav = output_dir / "music-duck-regression.wav"
    music = Placement(
        path=music_path,
        start=float(music_clip["timeline_start"]),
        duration=float(music_clip["duration"]),
        from_s=float(music_clip["source_from"]),
        speed=float(music_clip["speed"]),
        volume=float(music_clip["volume_authored"]),
        fade_in=float(music_clip["fadeIn"] or 0),
        fade_out=float(music_clip["fadeOut"] or 0),
        id=music_clip["clip_id"],
    )
    voices = [
        Placement(
            path=str(clip["source_path"]),
            start=float(clip["timeline_start"]),
            duration=float(clip["duration"]),
            from_s=float(clip["source_from"]),
            speed=float(clip["speed"]),
            volume=float(clip["volume_authored"]),
            id=clip["clip_id"],
        )
        for clip in audio_map["vo"]
    ]
    parameters = DuckParameters()
    result = duck_audio(music, voices, action_wav, parameters=parameters)
    curve_times, action_gain, target_gain = _extract_curve(result)

    source, source_rate = _read_pcm16(music_path)
    approved, approved_rate = _read_pcm16(approved_path)
    if source_rate != approved_rate or source.shape != approved.shape:
        raise ValueError(f"reference WAVs differ in format/length: {source.shape}@{source_rate} vs {approved.shape}@{approved_rate}")
    if source_rate != 48_000:
        raise ValueError(f"expected 48 kHz source, got {source_rate}")
    source_power = weighted_power(source, source_rate)
    approved_power = weighted_power(approved, approved_rate)
    window_times = np.arange(0, len(source), round(0.01 * source_rate)) / source_rate
    source_db = _moments(source_power, source_rate, window_times)
    approved_db = _moments(approved_power, approved_rate, window_times)
    actual_gain = approved_db - source_db
    # Curve timestamps are timeline-clock seconds; music starts at zero in this fixture.
    action_at_windows = np.interp(window_times, curve_times, action_gain, left=action_gain[0], right=action_gain[-1])
    residual = actual_gain - action_at_windows
    # The map places only the first 195.9667 s of this longer source. Outside
    # that timeline clip, the approved WAV's natural source fade approaches its
    # quantization floor, so a windowed ratio no longer measures authored gain.
    eligible = (window_times < float(music_clip["timeline_start"]) + float(music_clip["duration"])) & (source_db > -70.)
    reference_gain_report = {"available": False, "path": str(args.reference_gain)}
    reference_gain_at_windows: np.ndarray | None = None
    if args.reference_gain.is_file():
        reference_envelope = np.load(args.reference_gain, mmap_mode="r")
        if reference_envelope.ndim != 1 or len(reference_envelope) != len(source):
            raise ValueError("saved reference gain array must be one-dimensional and match the source frame count")
        hop = round(0.01 * source_rate)
        reference_gain_at_windows = np.asarray(reference_envelope[::hop][:len(window_times)], dtype=np.float64)
        if reference_gain_at_windows.size != window_times.size:
            raise ValueError("saved reference gain array does not cover all 10 ms comparison centers")
        ref_residual = actual_gain - reference_gain_at_windows
        # Rates use the same 10 ms centers as the action comparison. The stored
        # envelope is sample-clock data with a smooth curve, so this also avoids
        # allocating a second 48 kHz timeline vector.
        approved_motion = _curve_motion(actual_gain, eligible, window_times)
        approved_smoothed_motion = _curve_motion(_hann_smooth_gain(actual_gain), eligible, window_times)
        saved_motion = _curve_motion(reference_gain_at_windows, eligible, window_times)
        action_motion = _curve_motion(action_at_windows, eligible, window_times)
        reference_gain_report = {
            "available": True,
            "path": str(args.reference_gain),
            "frames": int(len(reference_envelope)),
            "eligible_windows": int(eligible.sum()),
            "approved_minus_saved_gain_db_median": round(float(np.median(ref_residual[eligible])), 4),
            "approved_minus_saved_gain_db_p95_abs": round(float(np.percentile(np.abs(ref_residual[eligible]), 95)), 4),
            "approved_minus_saved_gain_db_max_abs": round(float(np.max(np.abs(ref_residual[eligible]))), 4),
            "approved_minus_saved_gain_max_abs_at_s": round(float(window_times[np.flatnonzero(eligible)[np.argmax(np.abs(ref_residual[eligible]))]]), 3),
            "approved_implied_curve_motion": approved_motion,
            "approved_implied_hann_1s_smoothed_motion": approved_smoothed_motion,
            "saved_reference_curve_motion": saved_motion,
            "action_curve_motion": action_motion,
        }

    lines = _line_evidence(audio_map, args.words_dir)
    core_lines = {row["id"]: row for row in result.report.get("lines", [])}
    approved_audio = Audio(approved, approved_rate, 16, False)
    table = []
    for line in lines:
        start, end = line["start_s"], line["end_s"]
        active = (window_times >= start) & (window_times <= end)
        actual = actual_gain[active]
        modeled = action_at_windows[active]
        target_here = np.interp(window_times[active], curve_times, target_gain) if target_gain is not None else np.zeros_like(modeled)
        raw_music = source_db[active]
        actual_music = approved_db[active]
        if not actual.size:
            continue
        clip = line["clip"]
        voice_audio = load_audio(Path(clip["source_path"]))
        vo_audio, vo_rate = voice_audio.samples, voice_audio.rate
        if vo_rate != source_rate:
            raise ValueError(f"voice sample rate differs from music for {clip['clip_id']}")
        source_from = float(clip["source_from"])
        speed = float(clip["speed"])
        local_start = max(0, round((source_from + (start - float(clip["timeline_start"])) * speed) * vo_rate))
        local_end = min(len(vo_audio), round((source_from + (end - float(clip["timeline_start"])) * speed) * vo_rate))
        voice_power = weighted_power(vo_audio[local_start:local_end], vo_rate)
        voice_integrated = integrated(voice_power, vo_rate)
        voice_db = float("nan") if voice_integrated is None else voice_integrated + 20 * math.log10(max(float(clip["volume_authored"]), 1e-12))
        line_action_db = _percentile(modeled, 10)
        core_line = core_lines.get(line["clip_id"], {})
        music_i_word_ungated = integrated(
            source_power[round(start * source_rate):round(end * source_rate)], source_rate, gate=False
        )
        reference_word_bed = (
            None if voice_db is None or music_i_word_ungated is None
            else min(0., voice_db - parameters.bed_lu - music_i_word_ungated)
        )
        core_start = float(core_line.get("start_s", clip["timeline_start"]))
        core_end = float(core_line.get("end_s", clip["timeline_end"]))
        approved_placed = placed_samples(
            approved_audio, music, source_rate, core_start, core_end - core_start
        )
        approved_core_i = integrated(weighted_power(approved_placed, source_rate), source_rate)
        approved_core_gap = (
            None if approved_core_i is None or core_line.get("vo_i") is None
            else float(core_line["vo_i"]) - approved_core_i
        )
        action_core_gap = core_line.get("gap_after_lu")
        core_gap_delta = (
            None if approved_core_gap is None or action_core_gap is None
            else float(action_core_gap) - approved_core_gap
        )
        table.append({
            "clip_id": line["clip_id"],
            "asset": line["asset"],
            "start_s": round(start, 3),
            "end_s": round(end, 3),
            "span_source": "word_align" if line["aligned_words"] else "clip_fallback",
            "voice_lufs": round(voice_db, 2),
            "reference_word_music_i_ungated_lu": None if music_i_word_ungated is None else round(music_i_word_ungated, 2),
            "reference_word_gap_ungated_lu": None if music_i_word_ungated is None else round(voice_db - music_i_word_ungated, 2),
            "reference_word_bed_db": None if reference_word_bed is None else round(reference_word_bed, 2),
            "source_music_lufs_p10": round(_percentile(raw_music, 10), 2),
            "approved_music_lufs_p10": round(_percentile(actual_music, 10), 2),
            "approved_gap_db_p10": round(voice_db - _percentile(actual_music, 10), 2),
            "approved_gain_db_p10": round(_percentile(actual, 10), 2),
            "approved_gain_db_min": round(float(actual.min()), 2),
            "action_music_lufs_p10": round(_percentile(raw_music + modeled, 10), 2),
            "action_gap_db_p10": round(voice_db - _percentile(raw_music + modeled, 10), 2),
            "action_minus_approved_gap_db_p10": round(
                (voice_db - _percentile(raw_music + modeled, 10))
                - (voice_db - _percentile(actual_music, 10)), 2
            ),
            "action_gain_db_p10": round(line_action_db, 2),
            "action_core_vo_i_lu": core_line.get("vo_i"),
            "action_core_music_i_before_lu": core_line.get("music_i_before"),
            "action_core_bed_db": core_line.get("bed_db"),
            "action_minus_reference_word_bed_db": (
                None if reference_word_bed is None or core_line.get("bed_db") is None
                else round(float(core_line["bed_db"]) - reference_word_bed, 2)
            ),
            "approved_music_i_full_clip_lu": approved_core_i,
            "approved_gap_full_clip_lu": approved_core_gap,
            "action_core_music_i_after_lu": core_line.get("music_i_after"),
            "action_core_gap_after_lu": action_core_gap,
            "action_minus_approved_gap_full_clip_lu": core_gap_delta,
            "action_core_worst_voiced_gap_lu": core_line.get("worst_voiced_gap_lu"),
            "gain_residual_db_median": round(_percentile(actual - modeled, 50), 2),
            "gain_residual_db_p95_abs": round(_percentile(np.abs(actual - modeled), 95), 2),
            "actual_minus_target_db_median": round(_percentile(actual - target_here, 50), 2),
            "target_minus_action_db_median": round(_percentile(target_here - modeled, 50), 2),
        })

    core_report = result.report
    line_gap_delta = np.asarray([row["action_minus_approved_gap_db_p10"] for row in table], dtype=np.float64)
    full_clip_gap_delta = np.asarray(
        [float(row["action_minus_approved_gap_full_clip_lu"]) for row in table
         if row["action_minus_approved_gap_full_clip_lu"] is not None], dtype=np.float64
    )
    residual_candidates = np.flatnonzero(eligible)
    ranked = residual_candidates[np.argsort(np.abs(residual[residual_candidates]))[::-1]]
    residual_peaks = []
    for index in ranked:
        time_s = float(window_times[index])
        if any(abs(time_s - peak["time_s"]) < 1.0 for peak in residual_peaks):
            continue
        active_lines = [
            line for line in lines
            if float(line["clip"]["timeline_start"]) <= time_s < float(line["clip"]["timeline_end"])
        ]
        line_ids = [line["clip_id"] for line in active_lines]
        if not line_ids:
            nearest = min(
                lines,
                key=lambda line: min(
                    abs(time_s - float(line["clip"]["timeline_start"])),
                    abs(time_s - float(line["clip"]["timeline_end"])),
                ),
            )
            line_ids = [nearest["clip_id"]]
        target_at = 0.0 if target_gain is None else float(np.interp(time_s, curve_times, target_gain))
        action_at = float(action_at_windows[index])
        approved_at = float(actual_gain[index])
        residual_peaks.append({
            "time_s": round(time_s, 3),
            "line_ids": line_ids,
            "approved_gain_db": round(approved_at, 3),
            "action_target_db": round(target_at, 3),
            "action_gain_db": round(action_at, 3),
            "actual_minus_target_db": round(approved_at - target_at, 3),
            "target_minus_action_db": round(target_at - action_at, 3),
            "actual_minus_action_db": round(float(residual[index]), 3),
        })
        if len(residual_peaks) >= 10:
            break
    report = {
        "inputs": {
            "audio_map": str(args.audio_map),
            "music_source": str(music_path),
            "approved_mix": str(approved_path),
            "word_alignment_dir": str(args.words_dir),
            "action_wav": str(action_wav),
            "project": audio_map["project"],
            "timeline": audio_map["timeline"],
            "approved_mix_sha256": __import__("hashlib").sha256(approved_path.read_bytes()).hexdigest(),
        },
        "parameters": asdict(parameters) if hasattr(parameters, "__dataclass_fields__") else repr(parameters),
        "analysis": {
            "method": "centered 400 ms BS.1770 K-weighted moments at 10 ms hop; approved gain is approved_mix_LUFS minus source_LUFS",
            "eligibility": f"inside the music placement ({music_clip['timeline_start']:.4f}–{music_clip['timeline_end']:.4f} s) and source window above -70 LUFS",
            "windows": int(eligible.sum()),
            "actual_gain_db_min": round(float(actual_gain[eligible].min()), 3),
            "action_gain_db_min": round(float(action_at_windows[eligible].min()), 3),
            "median_actual_minus_action_db": round(float(np.median(residual[eligible])), 3),
            "p95_abs_actual_minus_action_db": round(float(np.percentile(np.abs(residual[eligible]), 95)), 3),
            "max_abs_actual_minus_action_db": round(float(np.max(np.abs(residual[eligible]))), 4),
            "lines": len(table),
            "word_aligned_lines": sum(bool(row["aligned_words"]) for row in lines),
            "fallback_lines": [row["clip_id"] for row in lines if not row["aligned_words"]],
            "line_gap_delta_p10_db": {
                "median": round(float(np.median(line_gap_delta)), 3),
                "mean_abs": round(float(np.mean(np.abs(line_gap_delta))), 3),
                "p95_abs": round(float(np.percentile(np.abs(line_gap_delta), 95)), 3),
                "max_abs": round(float(np.max(np.abs(line_gap_delta))), 3),
            },
            "full_clip_integrated_gap_delta_lu": {
                "median": round(float(np.median(full_clip_gap_delta)), 3),
                "mean_abs": round(float(np.mean(np.abs(full_clip_gap_delta))), 3),
                "p95_abs": round(float(np.percentile(np.abs(full_clip_gap_delta), 95)), 3),
                "max_abs": round(float(np.max(np.abs(full_clip_gap_delta))), 3),
            },
            "largest_residual_windows": residual_peaks,
            "saved_reference_gain_validation": reference_gain_report,
            "duck_report": {
                key: value for key, value in core_report.items()
                if key not in {"leaps", "lines", "speech_spans"}
            },
        },
        "line_table": table,
    }
    (output_dir / "music-duck-regression.json").write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    _csv_write(output_dir / "music-duck-regression-lines.csv", table)
    curve = [{
        "time_s": round(float(t), 4),
        "inside_music_placement": bool(t < float(music_clip["timeline_start"]) + float(music_clip["duration"])),
        "source_lufs": round(float(source_db[i]), 4),
        "approved_mix_lufs": round(float(approved_db[i]), 4),
        "eligible_for_gain_stats": bool(eligible[i]),
        "saved_reference_gain_db": None if reference_gain_at_windows is None else round(float(reference_gain_at_windows[i]), 4),
        "approved_minus_saved_gain_db": None if reference_gain_at_windows is None else round(float(actual_gain[i] - reference_gain_at_windows[i]), 4),
        "approved_gain_db": round(float(a), 4),
        "action_gain_db": round(float(g), 4),
        "action_target_db": None if target_gain is None else round(float(target_gain[i]), 4),
        "actual_minus_action_db": round(float(d), 4),
    } for i, (t, a, g, d) in enumerate(zip(window_times, actual_gain, action_at_windows, residual))]
    _csv_write(output_dir / "music-duck-regression-windows.csv", curve)
    print(json.dumps({key: value for key, value in report["analysis"].items() if key != "duck_report"}, indent=2, default=str))
    print(f"line table: {output_dir / 'music-duck-regression-lines.csv'}")
    print(f"window table: {output_dir / 'music-duck-regression-windows.csv'}")
    print(f"report: {output_dir / 'music-duck-regression.json'}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--music", type=Path, default=DEFAULT_MUSIC)
    parser.add_argument("--approved-mix", type=Path, default=DEFAULT_MIX)
    parser.add_argument("--reference-gain", type=Path, default=DEFAULT_REFERENCE_GAIN)
    parser.add_argument("--words-dir", type=Path, default=ALIGN)
    parser.add_argument("--output-dir", type=Path, required=True, help="scratch output directory for generated WAV and reports")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
