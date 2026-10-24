"""Admitted, local execution of a pinned music.duck audio snapshot."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from astrid.core._shared.result_manifest import build_manifest, write_json_atomic, write_manifest
from astrid.core.contracts.errors import AstridError
from astrid.core.foundation.hash import sha256_file
from astrid.core.pack.entrypoint import guard_canonical_entrypoint, run_pack_main
from astrid.packs.music.actions.duck.core import (
    DuckParameters,
    Placement,
    duck_audio,
    select_music_clip,
)

guard_canonical_entrypoint("music.duck")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="music.duck")
    parser.add_argument("--snapshot", type=Path, required=True)
    for name, default in asdict(DuckParameters()).items():
        parser.add_argument("--" + name.replace("_", "-"), type=float, default=default)
    parser.add_argument("--out", type=Path, required=True)
    return parser


def analyze_snapshot(snapshot: Path, out: Path, *, parameters: DuckParameters = DuckParameters()) -> dict:
    """Analyze only admitted bytes; no workspace credentials cross the worker boundary."""
    parameters.validate()
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="duck-sources-", dir=out) as directory:
        root = Path(directory)
        with zipfile.ZipFile(snapshot) as archive:
            spec = json.loads(archive.read("snapshot.json"))
            if spec.get("schema_version") != 1:
                raise AstridError("unsupported music.duck snapshot version; prepare a new snapshot")
            music_spec = spec["music"]
            select_music_clip([music_spec["clip"]], music_spec["placement"]["id"])
            paths = {}
            for digest in spec["objects"]:
                if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
                    raise AstridError("invalid snapshot source digest")
                path = root / digest[7:]
                # Never extract caller-controlled archive paths.
                with archive.open("objects/" + digest[7:]) as source, path.open("wb") as dest:
                    shutil.copyfileobj(source, dest)
                if "sha256:" + sha256_file(path) != digest:
                    raise AstridError("snapshot audio does not match its source digest")
                paths[digest] = path
        def placement(row):
            return Placement(path=paths[row["digest"]], **row["placement"])
        result = duck_audio(placement(music_spec), [placement(row) for row in spec["voices"]],
                            out / "music.wav", parameters=parameters, resolve_source=paths.__getitem__)
    report = result.report
    context = {key: spec.get(key) for key in ("project", "timeline", "revision_id", "voice_tracks")}
    report.update(context)
    write_json_atomic(out / "duck.json", report)
    write_manifest(out / "manifest.json", build_manifest(
        kind="music.duck", inputs={**context, "clip": report["clip"], **asdict(parameters)},
        outputs=[{"name": "music", "path": "music.wav", "type": "file", "role": "result",
                  "is_primary": True, "media_type": "audio/wav"},
                 {"name": "duck", "path": "duck.json", "type": "file", "role": "analysis",
                  "media_type": "application/json"}],
        created=datetime.now(timezone.utc).isoformat(), source_digest=report["source_digest"],
        max_slope_db_per_s=report["max_slope_db_per_s"], max_excess_db=report["max_excess_db"],
        gain_caused_leaps=report["gain_caused_leaps"]))
    return report


def main(argv: list[str] | None = None) -> int:
    def _run() -> int:
        args = build_parser().parse_args(argv)
        parameters = DuckParameters(**{key: getattr(args, key) for key in asdict(DuckParameters())})
        analyze_snapshot(args.snapshot, args.out.resolve(), parameters=parameters)
        return 0
    return run_pack_main("music.duck", _run, argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
