"""One-shot end-to-end smoke against the connected Astrid Runtime.

Creates a uniquely named disposable project, imports generated WAVs, publishes
its own audio timeline, invokes music.duck through Runtime, checks managed
outputs and source provenance, then archives the timeline. Runtime has no
project deletion operation, so the uniquely named project remains inspectable.

Run from the Astrid music-duck worktree so the launcher starts a host from this
source tree and an isolated Runtime realm. This avoids persisting a source
profile under the live Runtime data root:

    source /Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/env.sh
    PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}" python scripts/music_duck_runtime_smoke.py --sandbox-root /private/tmp/music-duck-runtime-smoke-unique

The script creates support and realm roots below that path through
``RuntimeCLI.configure("create", ...)`` and tears down only that isolated
Runtime through ``astrid-runtime down --data-root <support-root>``.
"""
from __future__ import annotations

import argparse
import json
import os
import uuid
import wave
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from astrid.packs.music.actions.duck._audio import read_duck_tag
from astrid.packs.music.actions.duck.api import duck_timeline
from astrid.packs.music.actions.duck.core import DuckParameters
from astrid.runtime_cli import RuntimeCLI
from astrid.sdk import AstridClient
from astrid.sdk.timeline import Checkout

WORKTREE_ROOT = Path(__file__).resolve().parents[1]


def _audio(path: Path, *, voice: bool) -> Path:
    rate, duration = 48_000, 8
    t = np.arange(rate * duration, dtype=np.float64) / rate
    samples = 0.055 * np.sin(2 * np.pi * 220 * t) + 0.02 * np.sin(2 * np.pi * 331 * t)
    if voice:
        samples[:] = 0
        t_voice = np.arange(round(0.24 * rate), dtype=np.float64) / rate
        envelope = np.sin(np.linspace(0, np.pi, len(t_voice))) ** 1.4
        syllable = 0.32 * envelope * np.sin(2 * np.pi * 185 * t_voice)
        for start in (1., 2., 3., 4., 5., 6.):
            begin = round(start * rate)
            samples[begin:begin + len(syllable)] += syllable
    pcm = np.rint(np.clip(samples, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(pcm.tobytes())
    return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sandbox-root", required=True, type=Path,
                        help="new isolated directory for the disposable Runtime realm and support data")
    parser.add_argument("--runtime-checkout", type=Path,
                        default=Path("/Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/Runtime"))
    parser.add_argument("--runtime-environment", type=Path,
                        default=Path("/Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/.venv"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    suffix = uuid.uuid4().hex[:12]
    slug = f"music-duck-smoke-{suffix}"
    project_id = None
    sandbox_root = args.sandbox_root.expanduser().absolute()
    if sandbox_root.exists():
        raise RuntimeError(f"sandbox root already exists; choose a new path: {sandbox_root}")
    support_root = sandbox_root / "support"
    realm_root = sandbox_root / "realm"
    sandbox_root.mkdir(parents=True)
    source_checkout = WORKTREE_ROOT
    runtime_checkout = args.runtime_checkout.expanduser().resolve()
    runtime_environment = args.runtime_environment.expanduser().resolve()
    manifest = sandbox_root / "source-profile.json"
    manifest.write_text(json.dumps({
        "profile": "astrid",
        "source_checkout": str(source_checkout),
        "runtime_checkout": str(runtime_checkout),
        "runtime_environment": str(runtime_environment),
    }, sort_keys=True))
    runtime = RuntimeCLI()
    realm_id = str(uuid.uuid4())
    configured = runtime.configure(
        "create", support_root=support_root, realm_root=realm_root, realm_id=realm_id,
        display_name=f"Music Duck Smoke {suffix}", source_manifest=manifest,
    )
    if not configured.ok:
        raise RuntimeError(f"isolated Runtime creation failed: {configured.data}")
    os.environ["ASTRID_RUNTIME_DATA_ROOT"] = str(support_root)
    os.environ["ASTRID_RUNTIME_SOURCE_MANIFEST"] = str(manifest)
    os.environ["ASTRID_RUNTIME_DOOR_PORT"] = "0"  # Own an ephemeral port, alongside any live workspace.
    old_pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = str(source_checkout) + (os.pathsep + old_pythonpath if old_pythonpath else "")
    client = None
    try:
        client = AstridClient.open_from_launcher()
        project = client.projects.create(
            slug=slug, name=f"Disposable music.duck smoke {suffix}",
            idempotency_key=f"music-duck-smoke-project-{suffix}",
        )
        if not project.ok:
            raise RuntimeError(f"project creation failed: {project.error}")
        project_id = project.data["project_id"]
        with TemporaryDirectory(prefix="music-duck-smoke-") as directory:
            root = Path(directory)
            bed_path = _audio(root / "bed.wav", voice=False)
            voice_path = _audio(root / "voice.wav", voice=True)

            def import_audio(path: Path) -> str:
                imported = client.media.import_file(
                    project=project_id, path=path,
                    idempotency_key=f"music-duck-smoke-{suffix}-{path.stem}",
                )
                if not imported.ok:
                    raise RuntimeError(f"media import failed: {imported.error}")
                return imported.data["object_id"]

            bed_id, voice_id = import_audio(bed_path), import_audio(voice_path)
            created = client.timelines.create_empty(
                project=project_id, timeline_id="music-duck-smoke",
                config={"tracks": []}, idempotency_key=f"music-duck-smoke-timeline-{suffix}",
            )
            if not created.ok:
                raise RuntimeError(f"timeline creation failed: {created.error}")
            tl = Checkout.open(project_id, "music-duck-smoke", client=client)
            parent = tl.bundle["parent"]
            parent["config"]["tracks"] = [
                {"id": "vo", "kind": "audio"},
                {"id": "music", "kind": "audio"},
            ]
            parent["registry"] = {"assets": {
                "bed": {"media_id": bed_id, "content_sha256": bed_id.removeprefix("sha256:"), "type": "audio/wav"},
                "voice": {"media_id": voice_id, "content_sha256": voice_id.removeprefix("sha256:"), "type": "audio/wav"},
            }}
            parent["clips"] = [
                {"id": "voice-1", "clipType": "media", "track": "vo", "asset": "voice", "at": 0, "from": 0, "to": 8},
                {"id": "music-1", "clipType": "media", "track": "music", "asset": "bed", "at": 0, "from": 0, "to": 8},
            ]
            published = tl.publish("seed disposable duck timeline", client=client,
                                   idempotency_key=f"music-duck-smoke-publish-{suffix}")
            print(f"published timeline revision: {published.get('new_head')}")

            before = client.timelines.open_bundle(project_id, "music-duck-smoke")
            if not before.ok:
                raise RuntimeError(f"could not inspect published smoke timeline: {before.error}")
            result = duck_timeline(
                client, project_id, "music-duck-smoke",
                parameters=DuckParameters(bed_lu=6, cap_lu=3, smooth_s=0.2),
            ).raise_for_error()
            after = client.timelines.open_bundle(project_id, "music-duck-smoke")
            if not after.ok or after.data["bundle"] != before.data["bundle"]:
                raise RuntimeError("music.duck changed its published input timeline")
            music_row, report_row = result.output("music"), result.output("duck")
            assert music_row["digest"] and report_row["digest"]
            report = json.loads(client.media.read_bytes(report_row["digest"]))
            wav = client.media.read_bytes(music_row["digest"])
            ducked = root / "ducked.wav"
            ducked.write_bytes(wav)
            tag = read_duck_tag(ducked)
            assert tag and tag["source_digest"] == bed_id
            assert report["source_digest"] == bed_id
            print(result)
            print(f"source digest verified: {bed_id}")
            print(f"ducked output bytes: {len(wav)}")
    finally:
        if project_id:
            archived = client.timelines.archive(
                project_id, "music-duck-smoke",
                idempotency_key=f"music-duck-smoke-archive-timeline-{suffix}",
            ) if client is not None else None
            if archived is not None and not archived.ok:
                print(f"warning: could not archive disposable timeline: {archived.error}")
            print(f"disposable project retained for inspection: {project_id}")
        if client is not None:
            client.close()
        stopped = runtime.invoke(("down", "--profile", "astrid", "--data-root", str(support_root), "--json"))
        if not stopped.ok:
            print(f"warning: isolated Runtime teardown reported: {stopped.data}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
