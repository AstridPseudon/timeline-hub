"""Pinned user-local tool and source materialization. Never consult shell profiles."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import stat
import tarfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

ENCODERS = {"libx264", "libx265", "libvpx-vp9", "libaom-av1", "libopus"}
FILTERS = {"ebur128", "silencedetect", "astats", "signalstats", "blackdetect",
           "loudnorm", "psnr", "ssim", "scale", "fps", "aresample"}


def validate_manifest(value: dict) -> dict:
    if value.get("schema_version") != 1:
        raise ValueError("Unsupported install manifest.")
    for name in ("agent", "runtime"):
        if not re.fullmatch(r"[0-9a-f]{40}", value[name]["sha"]):
            raise ValueError(f"The {name} source must be pinned to a full git SHA.")
    for name in ("uv", "python", "bun", "omp", "node", "ffmpeg"):
        if not re.fullmatch(r"\d+\.\d+\.\d+", value["tools"][name]["version"]):
            raise ValueError(f"The {name} tool must have an exact version.")
    if value["tools"]["node"]["version"] != "20.19.4":
        raise ValueError("Remotion requires Node 20.19.4.")
    return value


def download(url: str, target: Path, *, sha256: str | None = None) -> None:
    if not url.startswith("https://"):
        raise ValueError("Installer downloads require HTTPS.")
    with urllib.request.urlopen(url, timeout=120) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)
    if sha256 and hashlib.sha256(target.read_bytes()).hexdigest() != sha256:
        raise ValueError(f"Download checksum mismatch: {url}")


def archive_path(name: str) -> Path:
    value = PurePosixPath(name)
    if value.is_absolute() or ".." in value.parts or "\\" in name or ":" in name:
        raise ValueError(f"Unsafe archive entry: {name}")
    return Path(*value.parts)


def extract(archive: Path, destination: Path) -> None:
    """Extract regular files/directories only, including on Python 3.11/Windows."""
    destination.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                relative = archive_path(member.filename)
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise ValueError(f"Archive contains a link: {member.filename}")
                target = destination / relative
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(member) as source, target.open("wb") as output:
                        shutil.copyfileobj(source, output)
                    target.chmod(0o755 if member.external_attr >> 16 & 0o111 else 0o644)
        return
    with tarfile.open(archive) as bundle:
        for member in bundle:
            target = destination / archive_path(member.name)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with bundle.extractfile(member) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
                target.chmod(0o755 if member.mode & 0o111 else 0o644)
            elif member.issym() or member.islnk():
                # Official Node archives contain npm/npx links. The installer
                # invokes npm-cli.js directly and needs neither link.
                continue
            else:
                raise ValueError(f"Archive contains a special entry: {member.name}")


def fetch_archive(url: str, destination: Path, *, sha256: str | None = None) -> None:
    archive = destination.with_name(destination.name + ".download")
    try:
        download(url, archive, sha256=sha256)
        extract(archive, destination)
    finally:
        archive.unlink(missing_ok=True)


def source(name: str, sha: str, destination: Path) -> Path:
    staging = destination.with_name(destination.name + ".unpack")
    try:
        fetch_archive(f"https://github.com/banodoco/astrid-{name}/archive/{sha}.tar.gz", staging)
        children = list(staging.iterdir())
        if len(children) != 1 or not children[0].is_dir():
            raise ValueError(f"Unexpected {name} source archive layout.")
        # Discard GitHub's long SHA directory name to keep Windows paths shallow.
        os.replace(children[0], destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return destination


def binary(root: Path, name: str) -> Path:
    matches = sorted(p for p in root.rglob(name) if p.is_file())
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {name} in {root}, found {len(matches)}.")
    matches[0].chmod(0o755)
    return matches[0]


def probe_ffmpeg(encoders: str, filters: str) -> None:
    def names(output: str) -> set[str]:
        return {line.split()[1] for line in output.splitlines() if len(line.split()) >= 2}
    missing = sorted(ENCODERS - names(encoders)) + sorted(FILTERS - names(filters))
    if missing:
        raise ValueError("FFmpeg is missing required capabilities: " + ", ".join(missing))


def install_tools(manifest: dict, root: Path, target: str, run) -> dict[str, str]:
    pins = manifest["tools"]
    windows = target.startswith("windows-")
    suffix = ".exe" if windows else ""
    env = {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    paths = []
    for name in ("bun", "node", "ffmpeg"):
        pin = pins[name]
        asset = pin["assets"].get(target)
        if not asset:
            raise ValueError(f"There is no qualified {name} build for {target}.")
        folder = root / name
        for url in asset.get("urls", [asset.get("url")]):
            fetch_archive(url, folder, sha256=asset.get("sha256"))
        executable = binary(folder, name + suffix)
        paths.append(str(executable.parent))
        if name == "node":
            version = run([executable, "--version"]).strip()
            if version != "v" + pin["version"]:
                raise ValueError(f"The installed Node does not match {pin['version']}: {version}")
            env["ASTRID_NODE_EXECUTABLE"] = str(executable)
        elif name == "bun":
            if run([executable, "--version"]).strip() != pin["version"]:
                raise ValueError("The installed Bun does not match its pin.")
            env["ASTRID_BUN_EXECUTABLE"] = str(executable)
        else:
            binary(folder, "ffprobe" + suffix)
            probe_ffmpeg(run([executable, "-hide_banner", "-encoders"]),
                         run([executable, "-hide_banner", "-filters"]))
    # Deliberately construct the service PATH. No user profile or refreshed PATH.
    system_path = (str(Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32")
                   if windows else "/usr/bin:/bin:/usr/sbin:/sbin")
    omp = root / "omp"
    omp_bin = omp / "bin"
    omp_bin.mkdir(parents=True)
    env.update({"BUN_INSTALL": str(omp), "BUN_INSTALL_BIN": str(omp_bin),
                "PATH": (";" if windows else ":").join([str(omp_bin), *paths, system_path])})
    run([env["ASTRID_BUN_EXECUTABLE"], "install", "--global", "--no-progress",
         "@oh-my-pi/pi-coding-agent@" + pins["omp"]["version"]], extra_env=env)
    if not any((omp_bin / ("omp" + extension)).is_file() for extension in (suffix, ".cmd")):
        raise ValueError("OMP did not create its user-local launcher.")
    return env
