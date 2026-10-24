from __future__ import annotations

import hashlib
import os
import shlex
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PACKET = Path(__file__).parents[1]
CANDIDATE = PACKET / "candidate"
MAKER = CANDIDATE / "make-child-venv"
VERIFY = CANDIDATE / "verify_dependency_seed.py"


def wheel(
    directory: Path,
    filename: str,
    data: bytes = b"finite fixture",
    *,
    internal_name: str = "seedpkg",
    internal_version: str = "1.0.0",
    internal_tag: str = "py3-none-any",
    unsafe_member: str | None = None,
    symlink_member: bool = False,
    duplicate_member: bool = False,
) -> Path:
    path = directory / filename
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("seedpkg/__init__.py", data)
        if unsafe_member:
            info = zipfile.ZipInfo(unsafe_member)
            if symlink_member:
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(info, b"unsafe")
        if duplicate_member:
            archive.writestr("duplicate.txt", b"one")
            archive.writestr("duplicate.txt", b"two")
        archive.writestr(
            f"{internal_name}-{internal_version}.dist-info/METADATA",
            f"Metadata-Version: 2.1\nName: {internal_name}\nVersion: {internal_version}\n",
        )
        archive.writestr(
            f"{internal_name}-{internal_version}.dist-info/WHEEL",
            f"Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: {internal_tag}\n",
        )
    return path


def lock(path: Path, wheel_path: Path, marker: str = "") -> None:
    digest = hashlib.sha256(wheel_path.read_bytes()).hexdigest()
    suffix = f" ; {marker}" if marker else ""
    path.write_text(f"seedpkg==1.0.0{suffix} \\\n    --hash=sha256:{digest}\n")


def run_verify(
    wheelhouse: Path, requirements: Path, snapshot: Path | None = None
) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, "-I", str(VERIFY), str(wheelhouse), str(requirements)]
    if snapshot is not None:
        args.append(str(snapshot))
    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        check=False,
    )


def test_candidate_baseline_is_preserved_and_maker_wires_verified_seed() -> None:
    baseline = CANDIDATE / "make-child-venv.baseline"
    assert baseline.read_bytes() == (Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv")).read_bytes()
    source = MAKER.read_text() + (CANDIDATE / "request-child-venv").read_text()
    assert 'CHILD_VENV_DEPENDENCY_WHEELHOUSE' in source
    assert '236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778' in source
    assert 'verify_dependency_seed.py' in source
    assert '--no-index' in source and '--find-links' in source and '--require-hashes' in source and '--no-deps' in source
    assert "DEPENDENCY_SEED SCRIPT_DIR;" in source
    verifier_hash = next(line.split("=", 1)[1] for line in MAKER.read_text().splitlines() if line.startswith("VERIFIER_SHA256="))
    assert verifier_hash == hashlib.sha256(VERIFY.read_bytes()).hexdigest()


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


@pytest.mark.parametrize(
    "kwargs",
    [
        {"internal_name": "attacker"},
        {"internal_version": "9.9.9"},
        {"internal_tag": "cp999-cp999"},
        {"unsafe_member": "../escape.txt"},
        {"unsafe_member": "link", "symlink_member": True},
        {"duplicate_member": True},
    ],
)
def test_seed_rejects_archive_identity_or_unsafe_contents(
    tmp_path: Path, kwargs: dict[str, object]
) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl", **kwargs)
    requirements = tmp_path / "requirements.txt"
    lock(requirements, artifact)
    result = run_verify(wheelhouse, requirements)
    assert result.returncode != 0
    assert "REFUSED: dependency seed:" in result.stderr


@pytest.mark.parametrize("requirement", ["seedpkg>=1.0.0", "seedpkg==1.*", "seedpkg~=1.0"])
def test_seed_rejects_non_exact_lock_pin(tmp_path: Path, requirement: str) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl")
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(f"{requirement} --hash=sha256:{hashlib.sha256(artifact.read_bytes()).hexdigest()}\n")
    result = run_verify(wheelhouse, requirements)
    assert result.returncode != 0
    assert "exact" in result.stderr


def test_verified_snapshot_is_immutable_install_input(tmp_path: Path) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl")
    requirements = tmp_path / "requirements.txt"
    lock(requirements, artifact)
    snapshot = tmp_path / "stage" / "wheelhouse"
    snapshot.parent.mkdir()
    result = run_verify(wheelhouse, requirements, snapshot)
    assert result.returncode == 0, result.stderr
    original_artifact = artifact.read_bytes()
    original_requirements = requirements.read_bytes()
    artifact.write_bytes(b"attacker mutation")
    requirements.write_text("seedpkg>=0\n")
    assert (snapshot / artifact.name).read_bytes() == original_artifact
    assert (snapshot / "requirements.txt").read_bytes() == original_requirements
    assert stat.S_IMODE((snapshot / artifact.name).stat().st_mode) == 0o400
    assert stat.S_IMODE(snapshot.stat().st_mode) == 0o500


def git_repo(path: Path, files: dict[str, bytes]) -> str:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "test"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "commit.gpgsign", "false"], check=True)
    for name, data in files.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-q", "-m", "fixture"], check=True)
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def test_real_request_queue_store_context_and_pip_flags(tmp_path: Path) -> None:
    """Exercise the request and maker text with tiny local process stubs."""
    orch = tmp_path / "orch"
    (orch / "queue/pending").mkdir(parents=True)
    (orch / "tests").mkdir()
    (orch / "bin").mkdir()
    work = tmp_path / "work"
    work.mkdir()
    wheelhouse = tmp_path / "authenticated-wheelhouse"
    wheelhouse.mkdir()
    lock_bytes = subprocess.check_output(
        ["git", "-C", "/home/user/work/agent", "show", "HEAD:requirements/proof.lock"]
    )
    agent = tmp_path / "agent"
    runtime = tmp_path / "runtime"
    agent_sha = git_repo(
        agent,
        {"requirements/proof.lock": lock_bytes, "pyproject.toml": b"[project]\nname='astrid'\nversion='1.0'\n"},
    )
    runtime_sha = git_repo(
        runtime,
        {
            "pyproject.toml": b"[project]\nname='astrid-runtime'\nversion='1.0'\n",
            "packages/python/astrid_runtime_client/client.py": b"CLIENT = True\n",
        },
    )
    (orch / "bin/bench_store.py").write_text(
        """
import os
from pathlib import Path
class Store:
    def __init__(self, root, tests):
        self.root, self.tests = Path(root), Path(tests)
    def ensure(self, component, identity, registration, build, verify, seal=None):
        context = os.environ['STORE_CONTEXT']
        assert 'DEPENDENCY_SEED=' in context
        assert 'CLIENT_IDENTITY=' in context and 'RUNTIME_SHA=' in context
        stage = self.root / 'stage'
        stage.mkdir(parents=True)
        build(stage, stage)
        build.__globals__['verified_reports'][str(stage)] = (stage / '.provision-report').read_bytes()
        report = self.tests / 'provision' / 'venv-agent-child-caller.txt'
        report.parent.mkdir(parents=True)
        report.write_bytes((stage / '.provision-report').read_bytes())
        return {'path': str(stage), 'reused': False, 'key': 'fixture'}
"""
    )
    fake_python = tmp_path / "fake-python"
    log = tmp_path / "process.log"
    fake_python.write_text(
        """#!/usr/bin/env bash
set -u
: "${FAKE_LOG:?}"
printf 'PY %s\n' "$*" >> "$FAKE_LOG"
case " $* " in
  *" -m venv --copies "*) T="${@: -1}"; mkdir -p "$T/bin" "$T/lib/python3.13/site-packages"; cp "$0" "$T/bin/python"; cp "$0" "$T/bin/astrid-runtime"; cp "$0" "$T/bin/astrid-runtime-protocol"; chmod +x "$T/bin/python" "$T/bin/astrid-runtime" "$T/bin/astrid-runtime-protocol"; exit 0;;
  *"verify_dependency_seed.py"*) printf 'VERIFIER %s\n' "$*" >> "$FAKE_LOG"; exit 0;;
  *"-m pip install"*) printf 'PIP %s\n' "$*" >> "$FAKE_LOG"; exit 0;;
  *"-m pip freeze"*) exit 0;;
  *) exit 0;;
esac
"""
    )
    fake_python.chmod(0o755)
    env = os.environ.copy()
    env.update(
        {
            "CHILD_VENV_ORCH_ROOT": str(orch),
            "CHILD_VENV_WORK_ROOT": str(work),
            "CHILD_VENV_AGENT_CHECKOUT": str(agent),
            "CHILD_VENV_RUNTIME_CHECKOUT": str(runtime),
            "CHILD_VENV_PYTHON": str(fake_python),
            "CHILD_VENV_DEPENDENCY_WHEELHOUSE": str(wheelhouse),
            "FAKE_LOG": str(log),
        }
    )
    request_result = subprocess.run(
        [
            str(CANDIDATE / "request-child-venv"),
            "venv-agent-child-caller",
            agent_sha,
            "--source-carrier",
            str(agent),
            str(runtime),
            runtime_sha,
        ],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert request_result.returncode == 0, request_result.stderr
    queue_file = orch / "queue/pending/childvenv-venv-agent-child-caller"
    queued = queue_file.read_text().strip()
    assert f"--dependency-wheelhouse {wheelhouse}" in queued
    assert "CHILD_VENV_DEPENDENCY_WHEELHOUSE" not in queued
    dispatch_env = env.copy()
    dispatch_env.pop("CHILD_VENV_DEPENDENCY_WHEELHOUSE")
    dispatch = subprocess.run(
        [
            "bash",
            "-c",
            f"exec {shlex.quote(str(MAKER))} $(sed 's/^CHILDVENV //' {shlex.quote(str(queue_file))})",
        ],
        env=dispatch_env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert dispatch.returncode == 0, dispatch.stdout + dispatch.stderr
    records = log.read_text().splitlines()
    assert any(line.startswith("VERIFIER ") for line in records)
    pinned = [line for line in records if line.startswith("PIP ") and "--no-index" in line]
    assert len(pinned) == 1
    assert "--find-links" in pinned[0] and "--require-hashes" in pinned[0] and "--no-deps" in pinned[0]
    assert ".dependency-wheelhouse" in pinned[0]
    assert str(wheelhouse) not in pinned[0]
