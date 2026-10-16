#!/usr/bin/env python3
"""Compose a tempo-locked chiptune cue and its beat grid (chiptune.compose).

Invoked by the Astrid runtime from the pack's V3 action declaration. The synthesis
lives in ``astrid.packs.chiptune.actions._synth``.
"""

from __future__ import annotations

from astrid.core.pack.entrypoint import guard_canonical_entrypoint, run_pack_main

guard_canonical_entrypoint("chiptune.compose")

# The canonical entrypoint guard must run before importing the pack runtime.
# ruff: noqa: E402
import argparse
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from astrid.core._shared.result_manifest import write_json_atomic, write_manifest
from astrid.packs.chiptune.actions import _synth as syn
from astrid.packs.chiptune.actions.compose import planner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chiptune.compose", description="Compose a chiptune music cue.")
    parser.add_argument("--duration-s", type=float, required=True, help="Exact cue length in seconds.")
    parser.add_argument("--bpm", type=float, default=132.0)
    parser.add_argument("--key", default="A minor", help="Tonic and mode, e.g. 'A minor' or 'F# major'.")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--sections", required=True, help="JSON array of {start_s, end_s, energy, mood}.")
    parser.add_argument("--hits", default=None, help="Optional JSON array of accent times or {t, kind} objects (kind: stab or thud).")
    parser.add_argument("--duck", default=None, help="Optional JSON array of {start_s, end_s, gain_db}.")
    parser.add_argument("--vo-mask", default=None, help="Optional JSON array of [start_s, end_s] speech spans.")
    parser.add_argument("--mutes", default=None, help="Optional JSON array of [start_s, end_s] hard-mute windows (exact silence).")
    parser.add_argument("--duck-db", type=float, default=-10.0)
    parser.add_argument("--master-db", type=float, default=-16.0)
    parser.add_argument("--style", default="nes")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    return parser


_parse_duck = planner.parse_duck
_parse_vo_mask = planner.parse_vo_mask
_parse_mutes = planner.parse_mutes


def _write_wav(path: Path, pcm: Any, sample_rate: int) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def main(argv: list[str] | None = None) -> int:
    def _run() -> int:
        args = build_parser().parse_args(argv)
        plan = planner.build_composition_plan({
            "duration_s": float(args.duration_s),
            "bpm": float(args.bpm),
            "key": args.key,
            "seed": int(args.seed),
            "sections": args.sections,
            "hits": args.hits,
            "duck": args.duck,
            "vo_mask": args.vo_mask,
            "duck_db": float(args.duck_db),
            "master_db": float(args.master_db),
            "style": args.style,
            "mutes": args.mutes,
        })
        buf, meta = syn.render_composition_plan(plan)
        out = args.out.expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)
        music_path = out / "music.wav"
        beats_path = out / "beats.json"
        music_path.unlink(missing_ok=True)
        beats_path.unlink(missing_ok=True)
        (out / "manifest.json").unlink(missing_ok=True)

        _write_wav(music_path, syn.to_int16_stereo(buf), syn.SAMPLE_RATE)

        section_metrics = []
        for sec in meta["sections"]:
            lo = int(round(sec["start_s"] * syn.SAMPLE_RATE))
            hi = int(round(sec["end_s"] * syn.SAMPLE_RATE))
            section_metrics.append(syn.measure_db(buf[:, lo:hi]))
        sections_out = planner.build_section_outputs(plan, section_metrics)
        peak_db, rms_db = syn.measure_db(buf)
        beats_doc = planner.build_beats_document(plan, sections_out)
        write_json_atomic(beats_path, beats_doc)

        created = datetime.now(timezone.utc).isoformat()
        manifest = planner.build_result_manifest(
            plan,
            sections_out=sections_out,
            created=created,
            peak_dbfs=peak_db,
            rms_dbfs=rms_db,
        )
        write_manifest(out / "manifest.json", manifest)
        return 0

    return run_pack_main("chiptune.compose", _run, argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
