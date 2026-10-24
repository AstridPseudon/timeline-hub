"""Runtime-backed capture and local analysis for music.duck.

This test creates an isolated Runtime realm, imports deterministic audio, and
publishes a disposable timeline. It never connects to a user realm or project.
"""
from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np
import pytest

from astrid.core.pack.entrypoint import canonical_runtime_entrypoint
from astrid.packs.music.actions.duck.api import prepare_snapshot
from astrid.packs.music.actions.duck.core import DuckParameters
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline import Checkout

with canonical_runtime_entrypoint("music.duck"):
    from astrid.packs.music.actions.duck.run import analyze_snapshot

pytestmark = pytest.mark.integration


def _write_audio(path: Path, *, voice: bool = False) -> Path:
    rate = 48_000
    seconds = 8
    t = np.arange(rate * seconds, dtype=np.float64) / rate
    signal = 0.055 * np.sin(2 * np.pi * 220 * t) + 0.02 * np.sin(2 * np.pi * 331 * t)
    if voice:
        signal[:] = 0
        burst = np.arange(round(0.24 * rate), dtype=np.float64) / rate
        envelope = np.sin(np.linspace(0, np.pi, len(burst))) ** 1.4
        syllable = 0.32 * envelope * np.sin(2 * np.pi * 185 * burst)
        for start in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
            begin = round(start * rate)
            signal[begin:begin + len(syllable)] += syllable
    pcm = np.rint(np.clip(signal, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(pcm.tobytes())
    return path


def _open_client(daemon) -> AstridClient:
    return AstridClient.open(
        endpoint=daemon.endpoint,
        credential=daemon.credential_path,
        realm_id=daemon.service.realm["id"],
        actor_id="owner",
        client_name="music-duck-runtime-test",
        client_version="stage1",
        protocol_version="workspace.v1",
    )


def test_duck_snapshot_reads_runtime_timeline_and_analyzes_without_publishing(tmp_path, real_runtime):
    daemon = real_runtime()
    try:
        client = _open_client(daemon)
        project_id = client.projects.create(
            slug="duck-runtime-test", name="Disposable Duck Runtime Test",
            idempotency_key="duck-project",
        ).data["project_id"]

        def ingest(name: str, voice: bool) -> str:
            path = _write_audio(tmp_path / name, voice=voice)
            result = client.media.import_file(
                project=project_id, path=path, idempotency_key=f"media-{name}",
            )
            assert result.ok, result.error
            return result.data["object_id"]

        bed_id = ingest("bed.wav", False)
        voice_id = ingest("voice.wav", True)
        created = client.timelines.create_empty(
            project=project_id, timeline_id="duck-main", config={"tracks": []},
            idempotency_key="duck-timeline",
        )
        assert created.ok, created.error

        # Author and publish the disposable parent timeline through the SDK;
        # Runtime stores both imported media references in the published head.
        tl = Checkout.open(project_id, "duck-main", client=client)
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
                               idempotency_key="duck-publish-audio")
        assert published["new_head"]

        before = client.timelines.open_bundle(project_id, "duck-main")
        assert before.ok, before.error
        snapshot = tmp_path / "duck-snapshot.zip"
        spec = prepare_snapshot(client, project_id, "duck-main", snapshot)
        assert spec["revision_id"] == before.data["revision_id"]
        assert len(spec["voices"]) == 1
        assert spec["music"]["digest"] == bed_id

        report = analyze_snapshot(
            snapshot, tmp_path / "duck-output",
            parameters=DuckParameters(bed_lu=6, cap_lu=3, smooth_s=0.2),
        )
        assert report["source_digest"] == bed_id
        assert (tmp_path / "duck-output" / "music.wav").is_file()
        manifest = json.loads((tmp_path / "duck-output" / "manifest.json").read_text())
        outputs = manifest["outputs"]
        assert {row["name"] for row in outputs} == {"music", "duck"}
        assert next(row for row in outputs if row["name"] == "music")["is_primary"] is True

        after = client.timelines.open_bundle(project_id, "duck-main")
        assert after.ok, after.error
        assert after.data["revision_id"] == before.data["revision_id"]
        assert after.data["bundle"] == before.data["bundle"]
    finally:
        daemon.stop()
