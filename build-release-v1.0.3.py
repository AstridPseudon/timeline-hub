"""Build reproducible owner-scanner ZIP and flat TGZ artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DELIVERY = ROOT / "delivery"
ZIP_PATH = ROOT / "owner_film_cliplook_scan-v1.0.3.zip"
TGZ_PATH = ROOT / "owner-film-viewing-tools-v1.0.3.tgz"
ZIP_SHA_PATH = ROOT / "owner_film_cliplook_scan-v1.0.3.sha256"
TGZ_SHA_PATH = ROOT / "owner-film-viewing-tools-v1.0.3.sha256"
MEMBERS = (
    Path("FILELIST.md"),
    Path("ORCHREPORT.md"),
    Path("README.md"),
    Path("VERSION"),
    Path("owner_film_cliplook_scan.py"),
    Path("reference/extension-ORCHREPORT.md"),
    Path("reference/extension-owner-film-differences-scan.json"),
    Path("reference/predecessor-ORCHREPORT.md"),
    Path("reference/predecessor-owner-film-cliplook-scan.json"),
    Path("tests/conftest.py"),
    Path("tests/test_owner_film_cliplook_scan.py"),
    Path("semantic-policy.patch"),
)


def _data(path: Path) -> bytes:
    return (DELIVERY / path).read_bytes()


def build_zip() -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for member in MEMBERS:
            info = zipfile.ZipInfo(member.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, _data(member))


def build_tgz() -> None:
    with TGZ_PATH.open("wb") as output:
        import gzip

        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0, filename="") as compressed:
            with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as archive:
                for member in MEMBERS:
                    info = tarfile.TarInfo(member.as_posix())
                    payload = _data(member)
                    info.size = len(payload)
                    info.mode = 0o644
                    info.mtime = 0
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    archive.addfile(info, io.BytesIO(payload))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_metadata() -> None:
    metadata = {
        "version": "1.0.3",
        "zip": {"name": ZIP_PATH.name, "size": ZIP_PATH.stat().st_size, "sha256": digest(ZIP_PATH)},
        "tgz": {"name": TGZ_PATH.name, "size": TGZ_PATH.stat().st_size, "sha256": digest(TGZ_PATH)},
        "members": [member.as_posix() for member in MEMBERS],
    }
    (ROOT / "artifact-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    ZIP_SHA_PATH.write_text(f"{metadata['zip']['sha256']}\n", encoding="ascii")
    TGZ_SHA_PATH.write_text(f"{metadata['tgz']['sha256']}\n", encoding="ascii")


if __name__ == "__main__":
    build_zip()
    build_tgz()
    write_metadata()
