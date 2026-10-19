"""Pinned user-local tool and source materialization. Never consult shell profiles."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import stat
import subprocess
import tarfile
import urllib.parse
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
        if "repo" in value[name]:
            local_repository(value[name]["repo"])
    for name in ("uv", "python", "bun", "omp", "node", "ffmpeg"):
        if not re.fullmatch(r"\d+\.\d+\.\d+", value["tools"][name]["version"]):
            raise ValueError(f"The {name} tool must have an exact version.")
        for asset in value["tools"][name].get("assets", {}).values():
            asset_downloads(asset)
    if value["tools"]["node"]["version"] != "20.19.4":
        raise ValueError("Remotion requires Node 20.19.4.")
    return value


def asset_downloads(asset: dict) -> list[tuple[str, str | None]]:
    """Pair each archive with its digest; retain legacy single-URL manifests."""
    if "urls" in asset:
        urls = asset["urls"]
        checksums = asset.get("sha256")
        if "url" in asset or not isinstance(urls, list) or not urls:
            raise ValueError("An installer asset needs either url or a nonempty urls list.")
        if not isinstance(checksums, list) or len(checksums) != len(urls):
            raise ValueError("Installer urls require an ordered sha256 list of equal length.")
    else:
        urls = [asset.get("url")]
        checksums = [asset.get("sha256")]
    for url, checksum in zip(urls, checksums):
        if not isinstance(url, str) or not url.startswith("https://"):
            raise ValueError("Installer asset downloads require HTTPS URLs.")
        # Omitted single-archive digests predate this manifest contract. Explicit
        # digests and every multi-archive digest must be a lowercase SHA256.
        if "sha256" in asset or "urls" in asset:
            if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
                raise ValueError("Installer asset sha256 must be 64 lowercase hex characters.")
    return list(zip(urls, checksums))


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
            for zip_member in bundle.infolist():
                relative = archive_path(zip_member.filename)
                if stat.S_ISLNK(zip_member.external_attr >> 16):
                    raise ValueError(f"Archive contains a link: {zip_member.filename}")
                target = destination / relative
                if zip_member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(zip_member) as source, target.open("wb") as output:
                        shutil.copyfileobj(source, output)
                    target.chmod(0o755 if zip_member.external_attr >> 16 & 0o111 else 0o644)
        return
    with tarfile.open(archive) as bundle:
        for member in bundle:
            target = destination / archive_path(member.name)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                tar_source = bundle.extractfile(member)
                if tar_source is None:
                    raise ValueError(f"Archive regular entry cannot be read: {member.name}")
                with tar_source, target.open("wb") as output:
                    shutil.copyfileobj(tar_source, output)
                target.chmod(0o755 if member.mode & 0o111 else 0o644)
            elif member.issym() or member.islnk():
                # Official Node archives contain npm/npx links. The installer
                # invokes npm-cli.js directly and needs neither link.
                continue
            else:
                raise ValueError(f"Archive contains a special entry: {member.name}")


def fetch_archive(url: str, destination: Path, *, sha256: str | None = None) -> None:
    archive = destination.with_name(destination.name + ".download")
    archive.parent.mkdir(parents=True, exist_ok=True)
    try:
        download(url, archive, sha256=sha256)
        extract(archive, destination)
    finally:
        archive.unlink(missing_ok=True)


def local_repository(value: str) -> Path:
    """Resolve a developer source override without permitting remote Git access."""
    if not isinstance(value, str) or not value:
        raise ValueError("A source repo must be an absolute local path or file:// URL.")
    if value.startswith("file://"):
        url = urllib.parse.urlsplit(value)
        if url.netloc not in {"", "localhost"} or url.query or url.fragment:
            raise ValueError("A source repo file:// URL must refer to this computer.")
        value = urllib.request.url2pathname(url.path)
    repository = Path(value)
    if not repository.is_absolute():
        raise ValueError("A source repo must be an absolute local path or file:// URL.")
    return repository


def local_source(repo: str, sha: str, archive: Path) -> None:
    """Archive a committed Git tree, without consulting the checkout's worktree."""
    repository = local_repository(repo)
    # Inherited Git overrides must not redirect reads to some other repository.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_NO_REPLACE_OBJECTS": "1"})

    def git(*args, **kwargs):
        try:
            result = subprocess.run(["git", "-C", str(repository), *args], env=env,
                                    stderr=subprocess.PIPE, check=False, **kwargs)
        except FileNotFoundError as error:
            raise ValueError("Local source overrides require Git on PATH.") from error
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise ValueError(f"Cannot read local source {repository} at {sha}: {detail}")
        return result

    if git("cat-file", "-t", sha, stdout=subprocess.PIPE).stdout.strip() != b"commit":
        raise ValueError("A local source SHA must identify a Git commit.")
    entries = git("ls-tree", "-r", "-z", sha, stdout=subprocess.PIPE).stdout
    for entry in entries.split(b"\0"):
        if entry and entry.split(b" ", 1)[0] not in {b"100644", b"100755"}:
            path = os.fsdecode(entry.split(b"\t", 1)[1])
            raise ValueError(f"Local source contains a link or submodule: {path}")
    with archive.open("wb") as output:
        git("archive", "--format=tar", sha, stdout=output)


def source(name: str, sha: str, destination: Path, *, repo: str | None = None) -> Path:
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError(f"The {name} source must be pinned to a full git SHA.")
    staging = destination.with_name(destination.name + ".unpack")
    archive = destination.with_name(destination.name + ".source.tar")
    try:
        if repo is not None:
            local_source(repo, sha, archive)
            extract(archive, staging)
            os.replace(staging, destination)
        else:
            fetch_archive(f"https://github.com/banodoco/astrid-{name}/archive/{sha}.tar.gz", staging)
            children = list(staging.iterdir())
            if len(children) != 1 or not children[0].is_dir():
                raise ValueError(f"Unexpected {name} source archive layout.")
            # Discard GitHub's long SHA directory name to keep Windows paths shallow.
            os.replace(children[0], destination)
    finally:
        archive.unlink(missing_ok=True)
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


def _media_tool_metadata(ffmpeg: Path, ffprobe: Path, run, origin: str) -> dict[str, str]:
    versions = {}
    for name, executable in (("ffmpeg", ffmpeg), ("ffprobe", ffprobe)):
        output = run([executable, "-version"])
        match = re.match(rf"{name} version (\S+)", output.strip())
        if not match:
            raise ValueError(f"Cannot identify the selected {name} version.")
        versions[name] = match[1]
    probe_ffmpeg(run([ffmpeg, "-hide_banner", "-encoders"]),
                 run([ffmpeg, "-hide_banner", "-filters"]))
    return {
        "ASTRID_FFMPEG_EXECUTABLE": str(ffmpeg),
        "ASTRID_FFPROBE_EXECUTABLE": str(ffprobe),
        "ASTRID_INSTALL_FFMPEG_SOURCE": origin,
        "ASTRID_INSTALL_FFMPEG_VERSION": versions["ffmpeg"],
        "ASTRID_INSTALL_FFPROBE_VERSION": versions["ffprobe"],
    }


def _media_tools(pin: dict, root: Path, target: str, run) -> dict[str, str]:
    selected = [Path(os.path.abspath(value)) for name in ("ffmpeg", "ffprobe")
                if (value := shutil.which(name))]
    versions = root.parent.parent
    # Managed versions are pruned after updates; they cannot supply a future
    # version's media executables, including through an external symlink.
    managed = versions.name == "versions" and any(
        path.is_relative_to(versions) or path.resolve().is_relative_to(versions) for path in selected)
    if len(selected) == 2 and not managed:
        try:
            return _media_tool_metadata(*selected, run, "path")
        except (OSError, ValueError, subprocess.SubprocessError):
            # An absent/broken capability falls back to the qualified release.
            pass
    asset = pin["assets"].get(target)
    if not asset:
        raise ValueError(f"There is no qualified ffmpeg build for {target}.")
    folder = root / "ffmpeg"
    for url, checksum in asset_downloads(asset):
        fetch_archive(url, folder, sha256=checksum)
    suffix = ".exe" if target.startswith("windows-") else ""
    return _media_tool_metadata(binary(folder, "ffmpeg" + suffix), binary(folder, "ffprobe" + suffix), run, "download")


def install_tools(manifest: dict, root: Path, target: str, run) -> dict[str, str]:
    pins = manifest["tools"]
    windows = target.startswith("windows-")
    suffix = ".exe" if windows else ""
    # Keep UTF-8 stdio without an interpreter startup override: the rendering
    # launch validation deliberately refuses PYTHONUTF8 in service environments.
    env = {"PYTHONIOENCODING": "utf-8"}
    paths = []
    for name in ("bun", "node"):
        pin = pins[name]
        asset = pin["assets"].get(target)
        if not asset:
            raise ValueError(f"There is no qualified {name} build for {target}.")
        folder = root / name
        for url, checksum in asset_downloads(asset):
            fetch_archive(url, folder, sha256=checksum)
        executable = binary(folder, name + suffix)
        paths.append(str(executable.parent))
        if name == "node":
            version = run([executable, "--version"]).strip()
            if version != "v" + pin["version"]:
                raise ValueError(f"The installed Node does not match {pin['version']}: {version}")
            env["ASTRID_NODE_EXECUTABLE"] = str(executable)
        else:
            if run([executable, "--version"]).strip() != pin["version"]:
                raise ValueError("The installed Bun does not match its pin.")
            env["ASTRID_BUN_EXECUTABLE"] = str(executable)
    env.update(_media_tools(pins["ffmpeg"], root, target, run))
    for name in ("ASTRID_FFMPEG_EXECUTABLE", "ASTRID_FFPROBE_EXECUTABLE"):
        directory = str(Path(env[name]).parent)
        if directory not in paths:
            paths.append(directory)
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
