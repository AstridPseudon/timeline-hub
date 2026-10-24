from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PACKET = Path(__file__).parents[1]
CANDIDATE = PACKET / "candidate"
MAKER = CANDIDATE / "make-child-venv"
VERIFY = CANDIDATE / "verify_dependency_seed.py"


def wheel(directory: Path, filename: str, data: bytes = b"finite fixture") -> Path:
    path = directory / filename
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("seedpkg/__init__.py", data)
        archive.writestr(
            "seedpkg-1.0.0.dist-info/METADATA",
            "Metadata-Version: 2.1\nName: seedpkg\nVersion: 1.0.0\n",
        )
        archive.writestr(
            "seedpkg-1.0.0.dist-info/WHEEL",
            "Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        )
    return path


def lock(path: Path, wheel_path: Path, marker: str = "") -> None:
    digest = hashlib.sha256(wheel_path.read_bytes()).hexdigest()
    suffix = f" ; {marker}" if marker else ""
    path.write_text(f"seedpkg==1.0.0{suffix} \\\n    --hash=sha256:{digest}\n")


def run_verify(wheelhouse: Path, requirements: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(VERIFY), str(wheelhouse), str(requirements)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_candidate_baseline_is_preserved_and_maker_wires_verified_seed() -> None:
    baseline = CANDIDATE / "make-child-venv.baseline"
    assert baseline.read_bytes() == (Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv")).read_bytes()
    source = MAKER.read_text()
    assert 'CHILD_VENV_DEPENDENCY_WHEELHOUSE' in source
    assert '236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778' in source
    assert 'verify_dependency_seed.py' in source
    assert '--no-index' in source and '--require-hashes' in source


def test_finite_wheelhouse_passes_active_lock(tmp_path: Path) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl")
    requirements = tmp_path / "requirements.txt"
    lock(requirements, artifact)
    result = run_verify(wheelhouse, requirements)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("case", ["wrong-lock", "altered-wheel", "extra-wheel", "missing-wheel", "marker-mismatch"])
def test_seed_rejects_untrusted_or_inapplicable_artifacts(tmp_path: Path, case: str) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl")
    requirements = tmp_path / "requirements.txt"
    lock(requirements, artifact, "python_version < '0'") if case == "marker-mismatch" else lock(requirements, artifact)
    if case == "wrong-lock":
        requirements.write_text(requirements.read_text().rsplit("sha256:", 1)[0] + "sha256:" + "f" * 64 + "\n")
    elif case == "altered-wheel":
        artifact.write_bytes(b"altered")
    elif case == "extra-wheel":
        wheel(wheelhouse, "otherpkg-1.0.0-py3-none-any.whl")
    elif case == "missing-wheel":
        artifact.unlink()
    result = run_verify(wheelhouse, requirements)
    assert result.returncode != 0
    assert "REFUSED: dependency seed:" in result.stderr


def test_seed_rejects_symlinked_wheelhouse(tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    linked = tmp_path / "linked"
    linked.symlink_to(real, target_is_directory=True)
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("seedpkg==1.0.0 --hash=sha256:" + "0" * 64 + "\n")
    result = run_verify(linked, requirements)
    assert result.returncode != 0
    assert "physical path" in result.stderr
