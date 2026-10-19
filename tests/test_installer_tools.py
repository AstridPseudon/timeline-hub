"""Use qualified PATH media tools or the pinned archive, with recorded selection."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from astrid.installer import tools


def manifest():
    return {"tools": {
        name: {"version": version, "assets": {"linux-x64": {"url": f"https://example.invalid/{name}.zip"}}}
        for name, version in (("bun", "1.3.14"), ("node", "20.19.4"), ("ffmpeg", "7.0.2"), ("omp", "12.0.0"))
    }}


def media_binary(directory, name):
    directory.mkdir(parents=True, exist_ok=True)
    executable = directory / name
    executable.write_bytes(b"test executable")
    executable.chmod(0o755)
    return executable


def harness(tmp_path, monkeypatch, *, availability="qualified"):
    existing = tmp_path / "existing media"
    other = tmp_path / "unrelated path"
    other.mkdir()
    ffmpeg = media_binary(existing, "ffmpeg") if availability != "missing" else None
    ffprobe = media_binary(existing / "probe", "ffprobe") if availability not in {"missing", "missing_ffprobe"} else None
    monkeypatch.setenv("PATH", os.pathsep.join((str(existing), str(existing / "probe"), str(other))))
    root = tmp_path / "installed tools"
    downloads, calls = [], []

    def fetch(url, destination, **_kwargs):
        downloads.append(url)
        name = destination.name
        media_binary(destination / "bundle", name)
        if name == "ffmpeg":
            media_binary(destination / "bundle", "ffprobe")

    def run(argv, *, extra_env=None):
        executable, *args = [str(value) for value in argv]
        calls.append((executable, args))
        if args == ["--version"]:
            return "1.3.14" if Path(executable).name == "bun" else "v20.19.4"
        if args[:2] == ["install", "--global"]:
            media_binary(Path(extra_env["BUN_INSTALL_BIN"]), "omp")
            return ""
        host = executable in {str(ffmpeg), str(ffprobe)}
        if host and availability == "broken_ffprobe" and executable == str(ffprobe):
            raise subprocess.CalledProcessError(1, executable)
        if args == ["-version"]:
            name = Path(executable).name
            if host and availability == "unidentifiable":
                return "unknown tool"
            return f"{name} version {'6.1.2-system' if host else '7.0.2-static'} Copyright test"
        if args == ["-hide_banner", "-encoders"]:
            encoders = tools.ENCODERS - ({"libopus"} if host and availability == "missing_encoder" else set())
            return "\n".join(f" V..... {name} encoder" for name in encoders)
        if args == ["-hide_banner", "-filters"]:
            filters = tools.FILTERS - ({"loudnorm"} if host and availability == "missing_filter" else set())
            return "\n".join(f" ... {name} filter" for name in filters)
        raise AssertionError(f"Unexpected tool invocation: {argv}")

    monkeypatch.setattr(tools, "fetch_archive", fetch)
    return root, ffmpeg, ffprobe, other, downloads, calls, run


def test_qualified_path_media_tools_are_selected_and_recorded(tmp_path, monkeypatch):
    root, ffmpeg, ffprobe, other, downloads, calls, run = harness(tmp_path, monkeypatch)

    env = tools.install_tools(manifest(), root, "linux-x64", run)

    assert downloads == ["https://example.invalid/bun.zip", "https://example.invalid/node.zip"]
    assert env["ASTRID_FFMPEG_EXECUTABLE"] == str(ffmpeg)
    assert env["ASTRID_FFPROBE_EXECUTABLE"] == str(ffprobe)
    assert env["ASTRID_INSTALL_FFMPEG_SOURCE"] == "path"
    assert env["ASTRID_INSTALL_FFMPEG_VERSION"] == "6.1.2-system"
    assert env["ASTRID_INSTALL_FFPROBE_VERSION"] == "6.1.2-system"
    path = env["PATH"].split(os.pathsep)
    assert str(ffmpeg.parent) in path and str(ffprobe.parent) in path
    assert shutil.which("ffmpeg", path=env["PATH"]) == str(ffmpeg)
    assert shutil.which("ffprobe", path=env["PATH"]) == str(ffprobe)
    assert str(other) not in path
    assert (str(ffmpeg), ["-hide_banner", "-encoders"]) in calls
    assert (str(ffmpeg), ["-hide_banner", "-filters"]) in calls
    assert not (root / "ffmpeg").exists()


def test_generated_service_environment_satisfies_the_rendering_probe(tmp_path, monkeypatch):
    from astrid.core.rendering.remotion_runtime import RemotionValidationError, probe_context

    root, *_unused, run = harness(tmp_path, monkeypatch)
    env = tools.install_tools(manifest(), root, "linux-x64", run)
    environment = {"HOME": str(tmp_path), **env}

    context = probe_context(environment=environment, python_executable=sys.executable)

    assert env["PYTHONIOENCODING"] == "utf-8"
    assert context["policy"] == "clean-schema-env/v1"
    assert context["node_env"]["HOME"] == str(tmp_path)
    # The producer must comply with the unchanged startup-override contract.
    with pytest.raises(RemotionValidationError, match="unsupported loader/interpreter overrides"):
        probe_context(environment={**environment, "PYTHONUTF8": "1"}, python_executable=sys.executable)


@pytest.mark.parametrize("availability", ["missing", "missing_ffprobe", "missing_encoder", "missing_filter",
                                         "broken_ffprobe", "unidentifiable"])
def test_absent_or_unqualified_media_tools_download_pinned_fallback(tmp_path, monkeypatch, availability):
    root, host_ffmpeg, host_ffprobe, _other, downloads, calls, run = harness(tmp_path, monkeypatch, availability=availability)

    env = tools.install_tools(manifest(), root, "linux-x64", run)

    ffmpeg, ffprobe = root / "ffmpeg" / "bundle" / "ffmpeg", root / "ffmpeg" / "bundle" / "ffprobe"
    assert downloads == [f"https://example.invalid/{name}.zip" for name in ("bun", "node", "ffmpeg")]
    assert env["ASTRID_FFMPEG_EXECUTABLE"] == str(ffmpeg)
    assert env["ASTRID_FFPROBE_EXECUTABLE"] == str(ffprobe)
    assert env["ASTRID_INSTALL_FFMPEG_SOURCE"] == "download"
    assert env["ASTRID_INSTALL_FFMPEG_VERSION"] == "7.0.2-static"
    assert env["ASTRID_INSTALL_FFPROBE_VERSION"] == "7.0.2-static"
    assert (str(ffmpeg), ["-hide_banner", "-encoders"]) in calls
    assert (str(ffmpeg), ["-hide_banner", "-filters"]) in calls
    path = env["PATH"].split(os.pathsep)
    for executable in (host_ffmpeg, host_ffprobe):
        if executable:
            assert str(executable.parent) not in path


def test_downloaded_media_tools_still_require_every_capability(tmp_path, monkeypatch):
    root, *_unused, run = harness(tmp_path, monkeypatch, availability="missing")

    def missing_filter(argv, **kwargs):
        output = run(argv, **kwargs)
        if [str(value) for value in argv[1:]] == ["-hide_banner", "-filters"]:
            return output.replace("loudnorm", "absent")
        return output

    with pytest.raises(ValueError, match="loudnorm"):
        tools.install_tools(manifest(), root, "linux-x64", missing_filter)


def test_an_older_managed_version_cannot_supply_media_tools_to_its_successor(tmp_path, monkeypatch):
    _root, *_unused, run = harness(tmp_path, monkeypatch)
    versions = tmp_path / "program" / "versions"
    old_media = versions / "old" / "tools" / "ffmpeg"
    media_binary(old_media, "ffmpeg")
    media_binary(old_media, "ffprobe")
    monkeypatch.setenv("PATH", str(old_media))
    root = versions / "new" / "tools"

    env = tools.install_tools(manifest(), root, "linux-x64", run)

    assert env["ASTRID_INSTALL_FFMPEG_SOURCE"] == "download"
    assert Path(env["ASTRID_FFMPEG_EXECUTABLE"]).is_relative_to(root)
    assert Path(env["ASTRID_FFPROBE_EXECUTABLE"]).is_relative_to(root)
    assert str(old_media) not in env["PATH"].split(os.pathsep)
