"""Strict qualification of the canonical CPU backend, not Player parity.

The black/silent media fixtures prove export plumbing and stream shape only.
Browser denial and admission failures must fail this positive lane.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tarfile
from dataclasses import replace
from pathlib import Path

import pytest

from astrid.core.rendering.contracts import AudioOwnership
from astrid.core.rendering.errors import RendererException
from astrid.core.rendering.registry import load_default_registries
from astrid.core.rendering.remotion_runtime import resolve_remotion_project_dir
from astrid.core.rendering.service import RenderService
from tests.packs import test_renderer_parity as parity
from tests.packs.rendering._helpers import _probe

pytestmark = [pytest.mark.integration]
parity_media = parity.parity_media
remotion_launch_validation = parity.remotion_launch_validation
renderer_execution_environment = parity.renderer_execution_environment


@pytest.fixture
def installed_project(tmp_path: Path) -> Path:
    project = tmp_path / "remotion"
    package = project / "node_modules" / "@banodoco" / "timeline-composition"
    package.parent.mkdir(parents=True)
    archive = parity.REMOTION / "artifacts" / "banodoco-timeline-composition-0.0.8.tgz"
    with tarfile.open(archive) as source:
        source.extractall(package.parent, filter="data")
    (package.parent / "package").rename(package)
    shutil.copy2(parity.REMOTION / "package.json", project / "package.json")
    cli = project / "node_modules" / "@remotion" / "cli" / "remotion-cli.js"
    cli.parent.mkdir(parents=True)
    cli.touch()
    return project


def test_parity_environment_absent_install_is_optional(tmp_path: Path) -> None:
    with pytest.raises(pytest.skip.Exception, match="node_modules absent"):
        parity._require_remotion_environment(tmp_path)


def test_parity_environment_accepts_public_built_package(installed_project: Path) -> None:
    parity._require_remotion_environment(installed_project)
    assert not (installed_project / "node_modules/@banodoco/timeline-schema").exists()
    assert not (installed_project / "node_modules/@banodoco/timeline-theme-2rp").exists()


@pytest.mark.parametrize("broken", ["package.json", "dist/index.js", "cli"])
def test_parity_environment_broken_install_fails(installed_project: Path, broken: str) -> None:
    package = installed_project / "node_modules/@banodoco/timeline-composition"
    target = (
        installed_project / "node_modules/@remotion/cli/remotion-cli.js"
        if broken == "cli" else package / broken
    )
    target.unlink()
    with pytest.raises(AssertionError, match="missing"):
        parity._require_remotion_environment(installed_project)


def _package_hashes(project: Path) -> dict[str, str]:
    package = project / "node_modules/@banodoco/timeline-composition"
    return {
        str(path.relative_to(package)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(package.rglob("*")) if path.is_file()
    }


def _probe_color_metadata(path: Path) -> dict:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,pix_fmt,color_range,color_space,color_transfer,color_primaries",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(out)


@pytest.mark.timeout(600)
@pytest.mark.parametrize("fixture", ["media-only", "text-card", "transition-windows"])
def test_canonical_cpu_export_publishes_real_video(
    fixture: str,
    parity_media: Path,
    tmp_path: Path,
    remotion_launch_validation: None,
) -> None:
    project = resolve_remotion_project_dir()
    before = _package_hashes(project)
    service = RenderService(registries=load_default_registries(parity.ROOT))
    assets = parity._json(parity_media / "assets.json")
    objects = {}
    for key, entry in assets["assets"].items():
        source = parity_media / entry.pop("file")
        entry["object_id"] = f"cpu-export-{key}"
        entry["digest"] = hashlib.sha256(source.read_bytes()).hexdigest()
        objects[entry["object_id"]] = str(source)
    assets_path = tmp_path / "managed.assets.json"
    assets_path.write_text(json.dumps(assets, indent=2) + "\n")
    output = tmp_path / f"{fixture}-cpu-export.mp4"
    request = replace(
        parity._request(
            parity_media, fixture, output.name,
            audio=AudioOwnership.RENDERED,
            backend_config={"rendering.remotion": {
                "project_dir": str(project), "composition_id": "TimelineComposition",
            }},
        ),
        assets_registry_path=str(assets_path),
        materialized_root=str(parity_media),
        materialized_objects=objects,
    )
    try:
        assert service.render_request(
            request, selector="rendering.remotion", out_path=output,
        ) == output
    except RendererException as exc:
        details = json.dumps(exc.error.to_dict(), indent=2)
        (tmp_path / "cpu-export-failure.json").write_text(details + "\n")
        exc.add_note(details)
        raise
    assert output.is_file() and output.stat().st_size > 0
    sidecar = parity._json(Path(f"{output}.provenance.json"))
    assert sidecar["output"] == str(output.resolve())
    probe = _probe(output)
    # Keep the encoder's reported colour metadata beside the retained probe;
    # ffprobe omits unset fields, so retain those as null rather than guessing.
    color_probe = _probe_color_metadata(output)
    color_fields = (
        "pix_fmt",
        "color_range",
        "color_space",
        "color_transfer",
        "color_primaries",
    )
    assert len(color_probe["streams"]) == len(probe["streams"])
    for stream in probe["streams"]:
        matching = next(
            candidate
            for candidate in color_probe["streams"]
            if candidate.get("codec_type") == stream.get("codec_type")
        )
        stream.update({field: matching.get(field) for field in color_fields})
    # Retained with pytest's basetemp by the central qualification runner.
    (tmp_path / "cpu-export-probe.json").write_text(json.dumps(probe, indent=2) + "\n")
    assert _package_hashes(project) == before, "export modified the published package"
    duration = 2.0 if fixture == "transition-windows" else 0.6
    parity._assert_tiny_semantic_video(output, duration=duration)
    video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in probe["streams"] if stream["codec_type"] == "audio")
    assert video["codec_name"] == "h264"
    # artifacts.py:286-290,302 canonicalizes yuvj420p as the existing
    # equivalent spelling of yuv420p; accept either actual ffprobe spelling.
    assert video["pix_fmt"] in {"yuv420p", "yuvj420p"}
    assert int(video["nb_read_frames"]) == round(duration * parity.CANVAS["fps"])
    assert audio["codec_name"] == "aac"
    assert float(audio["duration"]) == pytest.approx(duration, abs=0.12)
    assert sidecar["routing"]["backend"] == "rendering.remotion"
    assert sidecar["routing"]["resolved_backends"] == ["rendering.remotion"]
    assert sidecar["audio_ownership"] == "rendered"
