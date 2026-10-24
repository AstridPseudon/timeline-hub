from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
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
BOOTSTRAP_ARCHIVE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz")


@pytest.fixture(autouse=True)
def restore_private_fixture_directories(tmp_path: Path):
    """Let pytest remove sealed private fixtures after their assertions finish."""
    yield
    for path in [tmp_path, *tmp_path.rglob("*")]:
        if not path.is_symlink() and path.is_dir():
            path.chmod(path.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)


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
    console_script: str | None = None,
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
        if console_script:
            archive.writestr(
                f"{internal_name}-{internal_version}.dist-info/entry_points.txt",
                f"[console_scripts]\n{console_script}\n",
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
    source = MAKER.read_text() + (CANDIDATE / "request-child-venv").read_text() + VERIFY.read_text()
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


@pytest.mark.parametrize("metadata_name", ["jaraco.classes", "jaraco_classes", "jaraco-classes"])
def test_dotted_distribution_metadata_layout_is_standardized_narrowly(
    tmp_path: Path, metadata_name: str
) -> None:
    """The observed dotted jaraco.classes layout is oldRED and now newGREEN."""
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(
        wheelhouse,
        "jaraco.classes-3.4.0-py3-none-any.whl",
        internal_name=metadata_name,
        internal_version="3.4.0",
    )
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(
        f"jaraco.classes==3.4.0 --hash=sha256:{hashlib.sha256(artifact.read_bytes()).hexdigest()}\n"
    )
    result = run_verify(wheelhouse, requirements)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("metadata_name", "metadata_version"),
    [("jaraco.classes", "3.4.1"), ("other-package", "3.4.0")],
)
def test_dotted_distribution_layout_rejects_wrong_complete_identity(
    tmp_path: Path, metadata_name: str, metadata_version: str
) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(
        wheelhouse,
        "jaraco.classes-3.4.0-py3-none-any.whl",
        internal_name=metadata_name,
        internal_version=metadata_version,
    )
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(
        f"jaraco.classes==3.4.0 --hash=sha256:{hashlib.sha256(artifact.read_bytes()).hexdigest()}\n"
    )
    result = run_verify(wheelhouse, requirements)
    assert result.returncode != 0
    assert "metadata directory" in result.stderr


@pytest.mark.parametrize("mutation", ["multiple-metadata", "path-traversal", "hash-mutation"])
def test_dotted_distribution_layout_keeps_archive_and_hash_guards(
    tmp_path: Path, mutation: str
) -> None:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(
        wheelhouse,
        "jaraco.classes-3.4.0-py3-none-any.whl",
        internal_name="jaraco.classes",
        internal_version="3.4.0",
        unsafe_member="../escape.txt" if mutation == "path-traversal" else None,
    )
    if mutation == "multiple-metadata":
        with zipfile.ZipFile(artifact, "a") as archive:
            archive.writestr(
                "jaraco_classes-3.4.0.dist-info/METADATA",
                "Name: jaraco.classes\nVersion: 3.4.0\n",
            )
    requirements = tmp_path / "requirements.txt"
    lock(requirements, artifact)
    if mutation == "hash-mutation":
        artifact.write_bytes(artifact.read_bytes() + b"mutation")
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
    def ensure(self, component, identity, registration, build, verify, seal=None, failure_name=None):
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
  *" --bootstrap-identity "*) exec REAL_TEST_PYTHON "$@";;
  *" -m venv --copies "*) T="${@: -1}"; mkdir -p "$T/bin" "$T/lib/python3.13/site-packages"; cp "$0" "$T/bin/python"; cp "$0" "$T/bin/astrid-runtime"; cp "$0" "$T/bin/astrid-runtime-protocol"; chmod +x "$T/bin/python" "$T/bin/astrid-runtime" "$T/bin/astrid-runtime-protocol"; exit 0;;
  *"verify_dependency_seed.py"*) printf 'VERIFIER %s\n' "$*" >> "$FAKE_LOG"; exit 0;;
  *"-m pip install"*) printf 'PIP %s\n' "$*" >> "$FAKE_LOG"; exit 0;;
  *"-m pip freeze"*) exit 0;;
  *) exit 0;;
esac
"""
    )
    fake_python.write_text(fake_python.read_text().replace("REAL_TEST_PYTHON", shlex.quote(sys.executable)))
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
    pinned = [line for line in records if line.startswith("VERIFIER ") and "--install" in line.split() and ".dependency-wheelhouse" in line]
    assert len(pinned) == 1
    assert "--committed-lock" in pinned[0]
    assert ".dependency-wheelhouse" in pinned[0]
    assert str(wheelhouse) not in pinned[0]
    installed = [line for line in records if line.startswith("VERIFIER ") and "--installed" in line.split()]
    assert len(installed) == 1
    assert records.index(pinned[0]) < records.index(installed[0])
    assert records.index(installed[0]) < next(index for index, line in enumerate(records) if line.startswith("PIP ") and "--no-build-isolation" in line)


def load_helper(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pip_uses_sealed_lock_and_open_snapshot(tmp_path: Path, monkeypatch) -> None:
    helper = load_helper("seed_fixture", VERIFY)
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    requirements = b"seedpkg==1.0.0 --hash=sha256:" + b"a" * 64 + b"\n"
    (snapshot / "requirements.txt").write_bytes(requirements)
    observed = []

    def pip(args, *, pass_fds, check):
        import fcntl

        assert check
        lock_fd, directory_fd = pass_fds
        assert fcntl.fcntl(lock_fd, fcntl.F_GET_SEALS) & fcntl.F_SEAL_WRITE
        snapshot.rename(tmp_path / "renamed")
        snapshot.mkdir()
        (snapshot / "requirements.txt").write_text("attacker>=0\n")
        assert Path(f"/proc/self/fd/{lock_fd}").read_bytes() == requirements
        assert Path(f"/proc/self/fd/{directory_fd}/requirements.txt").read_bytes() == requirements
        assert {"--no-index", "--find-links", "--require-hashes", "--no-deps"}.issubset(args)
        observed.append(args)

    monkeypatch.setattr(helper.subprocess, "run", pip)
    helper.install_snapshot(snapshot, requirements, ["--no-cache-dir"])
    assert len(observed) == 1


def write_record(site: Path, metadata: str, files: dict[str, bytes]) -> None:
    import base64
    import csv

    for rel, content in files.items():
        target = site / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    record = site / metadata / "RECORD"
    record.parent.mkdir(parents=True, exist_ok=True)
    with record.open("w") as output:
        writer = csv.writer(output)
        for rel, content in files.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
            writer.writerow([rel, "sha256=" + digest, len(content)])
        writer.writerow([metadata + "/RECORD", "", ""])


def installed_dependency_fixture(
    tmp_path: Path,
    *,
    script: bytes | None = None,
    console_script: str = "seed-tool = seedpkg:main",
    reported_record: str = "seedpkg-1.0.0.dist-info/RECORD",
):
    helper = load_helper("installed_dependency_fixture", VERIFY)
    root = tmp_path / "child"
    site = root / "lib/python3.13/site-packages"
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(
        wheelhouse,
        "seedpkg-1.0.0-py3-none-any.whl",
        console_script=console_script,
    )
    data = artifact.read_bytes()
    with zipfile.ZipFile(artifact) as archive:
        files = {
            entry.filename: archive.read(entry)
            for entry in archive.infolist()
            if not entry.is_dir() and not entry.filename.endswith("/RECORD")
        }
    site.mkdir(parents=True)
    root.joinpath("bin").mkdir()
    root.joinpath("bin/python").write_bytes(Path(sys.executable).resolve().read_bytes())
    generated = (
        f"#!{root / 'bin/python'}\n"
        "import sys\n"
        "from seedpkg import main\n"
        "if __name__ == '__main__':\n"
        "    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n"
        "    sys.exit(main())\n"
    ).encode()
    script_path = root / "bin/seed-tool"
    script_path.write_bytes(generated if script is None else script)
    record = site / "seedpkg-1.0.0.dist-info/RECORD"
    record.parent.mkdir()
    import base64
    import csv

    with record.open("w", newline="") as output:
        writer = csv.writer(output)
        for rel, content in files.items():
            target = site / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
            writer.writerow([rel, "sha256=" + digest, len(content)])
        digest = base64.urlsafe_b64encode(hashlib.sha256((script_path).read_bytes()).digest()).decode().rstrip("=")
        writer.writerow(["../../../bin/seed-tool", "sha256=" + digest, len(script_path.read_bytes())])
        writer.writerow(["seedpkg-1.0.0.dist-info/RECORD", "", ""])

    class Distribution:
        def __init__(self) -> None:
            self.metadata = {"Name": "seedpkg"}
            self.version = "1.0.0"
            self._path = record.parent
            self.files = [Path(reported_record)]

    helper.md.distributions = lambda path: [Distribution()]
    return helper, root, data


def test_installed_console_script_record_is_oldred_newgreen(tmp_path: Path) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    base = tmp_path / "base-verifier.py"
    base.write_bytes(subprocess.check_output(["git", "show", "b330264b9:ops-handoff/child-dependency-reuse/candidate/verify_dependency_seed.py"]))
    old = load_helper("old_installed_dependency", base)
    old.md.distributions = helper.md.distributions
    with pytest.raises(SystemExit, match="unsafe or overlapping"):
        old.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})
    helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def test_installed_console_script_negatives_remain_strict(tmp_path: Path) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path, script=b"forged\n")
    with pytest.raises(SystemExit, match="generated dependency script"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("long_path", [False, True])
def test_installed_scripts_match_canonical_pip_and_survive_relocation(tmp_path: Path, long_path: bool) -> None:
    PipScriptMaker = importlib.import_module("pip._internal.operations.install.wheel").PipScriptMaker

    helper, root, data = installed_dependency_fixture(tmp_path)
    stage = tmp_path / ("stage-" + "x" * (140 if long_path else 1))
    (stage / "bin").mkdir(parents=True)
    maker = PipScriptMaker(None, str(stage / "bin"))
    maker.executable = str(stage / "bin/python")
    maker.variants = {""}
    maker.make("seed-tool = seedpkg:main")
    content = (stage / "bin/seed-tool").read_bytes()
    assert content.startswith(b"#!/bin/sh\n" if long_path else f"#!{stage}/bin/python\n".encode())
    site = root / "lib/python3.13/site-packages"
    files = {str(path.relative_to(site)): path.read_bytes() for path in site.rglob("*") if path.is_file() and path.name != "RECORD"}
    files["../../../bin/seed-tool"] = content
    stage_site = stage / "lib/python3.13/site-packages"
    write_record(stage_site, "seedpkg-1.0.0.dist-info", files)
    # Exercise the actual maker relocation body, including RECORD rehashing.
    (stage / ".provision-report").write_text("")
    (stage / ".astrid-distribution-metadata").write_text("")
    (stage / "bin/seed-tool").write_bytes(content.replace(str(stage).encode(), str(root).encode()))
    relocation = MAKER.read_text().split("<<'RELOCATE'\n", 1)[1].split("\nRELOCATE", 1)[0]
    result = subprocess.run([sys.executable, "-I", "-", str(stage), str(root)], input=relocation, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    for path in stage_site.rglob("*"):
        if path.is_file():
            (site / path.relative_to(stage_site)).write_bytes(path.read_bytes())
    (root / "bin/seed-tool").write_bytes((stage / "bin/seed-tool").read_bytes())
    helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("mutation", ["outside", "record-link", "target-link", "duplicate", "malformed"])
def test_maker_relocation_preflights_record_authority(tmp_path: Path, monkeypatch, mutation: str) -> None:
    import runpy

    stage = tmp_path / "stage"
    metadata = stage / "lib/python3.13/site-packages/seedpkg-1.0.0.dist-info"
    metadata.mkdir(parents=True)
    direct = metadata / "direct_url.json"
    original = json.dumps({"url": (stage / "source").as_uri()})
    direct.write_text(original)
    outside = tmp_path / "outside"
    outside.write_bytes(b"outside bytes never read")
    record = metadata / "RECORD"
    rows = "seedpkg-1.0.0.dist-info/RECORD,,\n"
    if mutation == "outside":
        rows += "../../../../outside,sha256=forged,23\n"
    elif mutation == "target-link":
        (metadata / "linked").symlink_to(outside)
        rows += "seedpkg-1.0.0.dist-info/linked,sha256=forged,23\n"
    elif mutation == "duplicate":
        rows += rows
    elif mutation == "malformed":
        rows += "only,two\n"
    record.write_text(rows)
    if mutation == "record-link":
        record.rename(tmp_path / "outside-record")
        record.symlink_to(tmp_path / "outside-record")
    relocation = MAKER.read_text().split("<<'RELOCATE'\n", 1)[1].split("\nRELOCATE", 1)[0]
    relocation_file = tmp_path / "maker-relocation.py"
    relocation_file.write_text(relocation)
    monkeypatch.setattr(sys, "argv", ["relocation", str(stage), str(tmp_path / "final")])
    read_bytes = Path.read_bytes

    def guarded_read(path):
        assert path.resolve() != outside, "outside RECORD target read"
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", guarded_read)
    with pytest.raises(SystemExit):
        runpy.run_path(str(relocation_file), run_name="__main__")
    assert direct.read_text() == original


@pytest.mark.parametrize("case", ["record-link", "owner-link", "site-parent-link"])
def test_metadata_record_is_never_read_before_physical_validation(tmp_path: Path, case: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    site = root / "lib/python3.13/site-packages"
    metadata_path = site / "seedpkg-1.0.0.dist-info"
    outside = tmp_path / "outside"
    if case == "record-link":
        (metadata_path / "RECORD").rename(outside)
        (metadata_path / "RECORD").symlink_to(outside)
    elif case == "owner-link":
        metadata_path.rename(outside)
        metadata_path.symlink_to(outside, target_is_directory=True)
    else:
        (root / "lib/python3.13").rename(outside)
        (root / "lib/python3.13").symlink_to(outside, target_is_directory=True)
    reads = []

    class Distribution:
        _path = metadata_path

        @property
        def metadata(self):
            reads.append("METADATA")
            raise AssertionError("metadata read before containment")

        @property
        def files(self):
            reads.append("RECORD")
            raise AssertionError("RECORD read before containment")

    helper.md.distributions = lambda path: [Distribution()]
    with pytest.raises(SystemExit):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})
    assert reads == []


@pytest.mark.parametrize("mutation", ["hash", "size", "symlink", "outside", "self-missing", "bookkeeping", "overlap"])
def test_console_record_integrity_and_bookkeeping_controls(tmp_path: Path, mutation: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    site = root / "lib/python3.13/site-packages"
    record = site / "seedpkg-1.0.0.dist-info/RECORD"
    lines = record.read_text().splitlines()
    script_row = next(row for row in lines if row.startswith("../../../bin/seed-tool,"))
    if mutation == "hash":
        lines[lines.index(script_row)] = script_row.replace("sha256=", "sha256=wrong")
    elif mutation == "size":
        lines[lines.index(script_row)] = script_row.rsplit(",", 1)[0] + ",1"
    elif mutation == "self-missing":
        lines = [row for row in lines if not row.startswith("seedpkg-1.0.0.dist-info/RECORD,")]
    elif mutation == "symlink":
        script = root / "bin/seed-tool"
        script.rename(root / "bin/original")
        script.symlink_to(root / "bin/original")
    elif mutation == "outside":
        lines.append("../../../../outside,,")
    elif mutation == "overlap":
        # Two original distributions cannot own the same generated script.
        import io

        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive, zipfile.ZipFile(io.BytesIO(data)) as original:
            for entry in original.infolist():
                content = original.read(entry).replace(b"Name: seedpkg", b"Name: otherpkg")
                archive.writestr(entry.filename.replace("seedpkg/", "otherpkg/").replace("seedpkg-1.0.0.dist-info", "otherpkg-1.0.0.dist-info"), content)
        other_metadata = site / "otherpkg-1.0.0.dist-info"
        other_metadata.mkdir()
        with zipfile.ZipFile(output) as archive:
            files = {entry.filename: archive.read(entry) for entry in archive.infolist()}
        files["../../../bin/seed-tool"] = (root / "bin/seed-tool").read_bytes()
        write_record(site, other_metadata.name, files)
        first = next(iter(helper.md.distributions(path=[])))
        second = type(first)()
        second._path = other_metadata
        second.metadata = {"Name": "otherpkg"}
        second.files = [Path("otherpkg-1.0.0.dist-info/RECORD")]
        helper.md.distributions = lambda path: [first, second]
        with pytest.raises(SystemExit, match="overlapping"):
            helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data, "otherpkg-1.0.0-py3-none-any.whl": output.getvalue()})
        return
    else:
        import base64

        content = b"arbitrary installer bytes"
        (record.parent / "INSTALLER").write_bytes(content)
        digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
        lines.append(f"seedpkg-1.0.0.dist-info/INSTALLER,sha256={digest},{len(content)}")
    record.write_text("\n".join(lines) + "\n")
    with pytest.raises(SystemExit):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize(
    "target",
    ["seedpkg:main:bad", "seedpkg", "seedpkg:", "seedpkg:main extra", "seedpkg:main [broken", "seedpkg:main [first, second-dash]"],
)
def test_installed_console_script_target_matches_distlib_grammar(
    tmp_path: Path, target: str
) -> None:
    helper, root, data = installed_dependency_fixture(
        tmp_path, console_script=f"seed-tool = {target}"
    )
    with pytest.raises(SystemExit, match="malformed console entry-point target"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def test_installed_record_owner_is_validated_before_record_read(tmp_path: Path, monkeypatch) -> None:
    outside = tmp_path / "outside.dist-info"
    outside.mkdir()
    (outside / "RECORD").write_text("seedpkg-1.0.0.dist-info/RECORD,,\n")
    helper, root, data = installed_dependency_fixture(
        tmp_path, reported_record="../../../../outside.dist-info/RECORD"
    )
    opened: list[Path] = []
    captured = helper.captured_bytes

    def observe(path: Path) -> bytes:
        opened.append(path)
        return captured(path)

    monkeypatch.setattr(helper, "captured_bytes", observe)
    with pytest.raises(SystemExit, match="unsafe dependency RECORD ownership"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})
    assert outside / "RECORD" not in opened


def test_installed_record_owner_rejects_another_in_child_metadata_dir(tmp_path: Path) -> None:
    helper, root, data = installed_dependency_fixture(
        tmp_path, reported_record="other-1.0.0.dist-info/RECORD"
    )
    with pytest.raises(SystemExit, match="not owned by distribution"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def test_installed_record_path_rejects_metadata_symlink(tmp_path: Path) -> None:
    helper, root, data = installed_dependency_fixture(
        tmp_path, reported_record="linked.dist-info/RECORD"
    )
    site = root / "lib/python3.13/site-packages"
    (site / "linked.dist-info").symlink_to(site / "seedpkg-1.0.0.dist-info", target_is_directory=True)
    with pytest.raises(SystemExit, match="symlinked dependency RECORD"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("mutation", ["traversal", "duplicate", "missing"])
def test_installed_console_script_record_path_controls_remain_strict(
    tmp_path: Path, mutation: str
) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    record = root / "lib/python3.13/site-packages/seedpkg-1.0.0.dist-info/RECORD"
    lines = record.read_text().splitlines()
    script_row = next(line for line in lines if line.startswith("../../../bin/seed-tool,"))
    if mutation == "traversal":
        lines[lines.index(script_row)] = script_row.replace(
            "../../../bin/seed-tool", "../../../../bin/seed-tool"
        )
    elif mutation == "duplicate":
        lines.append(script_row)
    else:
        lines.remove(script_row)
    record.write_text("\n".join(lines) + "\n")
    expected = "missing installed console script" if mutation == "missing" else "unsafe or overlapping"
    with pytest.raises(SystemExit, match=expected):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def retained_fixture(
    tmp_path: Path, *, managed: bool, provenance: str = "valid", make_existing: bool = True,
    source_archive: bool = False,
):
    """Tiny installed/source fixture; no pip, venv or production Store mutation."""
    import shutil

    store_module = load_helper("store_fixture", CANDIDATE / "bench_store.py")
    orch, work = tmp_path / "orch", tmp_path / "work"
    (orch / "tests").mkdir(parents=True)
    (orch / "tests/suites.conf").write_text("")
    (orch / "queue/pending").mkdir(parents=True)
    (orch / "bin").mkdir()
    shutil.copyfile(CANDIDATE / "bench_store.py", orch / "bin/bench_store.py")
    work.mkdir()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(wheelhouse, "seedpkg-1.0.0-py3-none-any.whl", b"VALUE = 1\n")
    lock_path = tmp_path / "lock"
    lock(lock_path, artifact)
    lock_bytes = lock_path.read_bytes()
    project = b"[project]\nname='astrid'\nversion='1.0'\n[tool.setuptools.packages.find]\ninclude=['astrid*']\n"
    client = b"CLIENT = True\n"
    agent_files = {"pyproject.toml": project, "requirements/proof.lock": lock_bytes,
                   "astrid/__init__.py": b"", "astrid_runtime_client/__init__.py": client}
    runtime_files = {"pyproject.toml": project.replace(b"name='astrid'", b"name='astrid-runtime'").replace(b"['astrid*']", b"['astrid_runtime*', 'runtime_protocol*']"),
                     "astrid_runtime/__init__.py": b"", "runtime_protocol/__init__.py": b"",
                     "packages/python/astrid_runtime_client/__init__.py": client}
    agent, runtime = tmp_path / "agent", tmp_path / "runtime"
    agent_sha, runtime_sha = git_repo(agent, agent_files), git_repo(runtime, runtime_files)
    identity = {"agent_sha": agent_sha, "backend_sha": runtime_sha,
                "client_tuple": {"packages/python/astrid_runtime_client/__init__.py": hashlib.sha256(client).hexdigest()}}
    maker_python = tmp_path / "maker-python"
    maker_python.write_text(f'#!/bin/bash\ncase "$*" in *verify_dependency_seed.py*|*bootstrap-identity*) exec {shlex.quote(sys.executable)} "$@";; esac\nexit 0\n')
    maker_python.chmod(0o755)
    bootstrap = load_helper("bootstrap_fixture", VERIFY)
    if provenance != "missing" and managed:
        identity["bootstrap_authority"] = bootstrap.bootstrap_identity(maker_python)
    name = "venv-agent-child-retained"
    store = store_module.Store.initialize(work / "bench-store", orch / "tests") if managed else None
    final = (work / "bench-store/entries" / ("child-" + store_module.key_for("child", identity))) if managed else work / name

    archive_inputs = {}
    if source_archive:
        archive_inputs = {name: subprocess.check_output(["git", "-C", str(checkout), "archive", "--format=tar", commit])
                          for name, checkout, commit in (("agent", agent, agent_sha), ("runtime", runtime, runtime_sha))}

    def build(stage, destination):
        source = destination / ".child-venv-source-fixture"
        source_urls = {name: (source / name).as_uri() for name in ("agent", "runtime")}
        if source_archive:
            (stage / ".source-inputs").mkdir()
            for name, content in archive_inputs.items():
                (stage / ".source-inputs" / (name + ".tar")).write_bytes(content)
                source_urls[name] = (destination / ".source-inputs" / (name + ".tar")).as_uri()
        site = stage / "lib/python3.13/site-packages"
        site.mkdir(parents=True)
        for directory, files in (("agent", agent_files), ("runtime", runtime_files)):
            for rel, content in files.items():
                path = stage / ".child-venv-source-fixture" / directory / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        for owner, modules, snapshot in (("astrid", ["astrid", "astrid_runtime_client"], "agent"),
                                         ("astrid_runtime", ["astrid_runtime", "runtime_protocol"], "runtime")):
            metadata = owner + "-1.0.dist-info"
            files = {module + "/__init__.py": client if module == "astrid_runtime_client" else b"" for module in modules}
            files[metadata + "/METADATA"] = f"Name: {owner.replace('_', '-')}\nVersion: 1.0\n".encode()
            direct = {"url": source_urls[snapshot]}
            if source_archive:
                direct["archive_info"] = {"hashes": {"sha256": hashlib.sha256(archive_inputs[snapshot]).hexdigest()}}
            else:
                direct["dir_info"] = {}
            files[metadata + "/direct_url.json"] = json.dumps(direct).encode()
            write_record(site, metadata, files)
        with zipfile.ZipFile(artifact) as archive:
            dependency_files = {entry.filename: archive.read(entry) for entry in archive.infolist()}
        if provenance == "forged-record":
            dependency_files["seedpkg/__init__.py"] = b"ATTACKER = True\n"
        write_record(site, "seedpkg-1.0.0.dist-info", dependency_files)
        if provenance == "unowned-file":
            (site / "seedpkg/injected.py").write_text("ATTACKER = True\n")
        if provenance in ("valid-pyc", "forged-pyc"):
            import py_compile

            py_compile.compile(str(site / "seedpkg/__init__.py"), doraise=True)
            pyc = next((site / "seedpkg/__pycache__").iterdir())
            if provenance == "forged-pyc":
                import marshal

                pyc.write_bytes(pyc.read_bytes()[:16] + marshal.dumps(compile("ATTACKER = True", str(site / "seedpkg/__init__.py"), "exec")))
            with (site / "seedpkg-1.0.0.dist-info/RECORD").open("a") as output:
                output.write(str(pyc.relative_to(site)) + ",,\n")
        if provenance != "missing":
            retained = stage / ".dependency-wheelhouse"
            retained.mkdir()
            (retained / artifact.name).write_bytes(artifact.read_bytes() if provenance != "wrong-wheel" else b"wrong")
            (retained / "requirements.txt").write_bytes(lock_bytes if provenance != "wrong-lock" else b"seedpkg>=0\n")
        (stage / "bin").mkdir()
        shutil.copyfile(maker_python, stage / "bin/python")
        (stage / "bin/python").chmod(0o755)
        if provenance != "missing" and managed:
            for alias in ("python3", "python3.13"):
                shutil.copyfile(maker_python, stage / "bin" / alias)
                (stage / "bin" / alias).chmod(0o755)
            # Genuine original wheels and trusted host templates, materialized
            # without installing or executing any package in this private fixture.
            bootstrap.write_snapshot(stage / ".bootstrap-wheelhouse", bootstrap.BOOTSTRAP_LOCK,
                                     bootstrap.bootstrap_artifacts(BOOTSTRAP_ARCHIVE))
            (stage / ".bootstrap-input.tgz").write_bytes(BOOTSTRAP_ARCHIVE.read_bytes())
            (stage / ".bootstrap-authority").write_text(identity["bootstrap_authority"] + "\n")
            for rel, content in bootstrap.venv_files(destination).items():
                (stage / rel).write_bytes(content)
            materialize_bootstrap(bootstrap, stage, destination)
        markers = {".astrid-source-commit": agent_sha, ".astrid-runtime-source-commit": runtime_sha,
                   ".astrid-runtime-client-identity": "\n".join(f"{key}={value}" for key, value in identity["client_tuple"].items()),
                   ".astrid-import-origins": "\n".join(f"{module}={destination}/lib/python3.13/site-packages/{module}/__init__.py" for module in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client")),
                   ".astrid-distribution-metadata": ""}
        for marker, value in markers.items():
            (stage / marker).write_text(value + ("\n" if value else ""))
        metadata_lines = []
        for owner, snapshot in (("astrid", "agent"), ("astrid-runtime", "runtime")):
            metadata_lines.extend((f"{owner}_name={owner}", f"{owner}_version=1.0",
                                   f"{owner}_direct_url={source_urls[snapshot]}",
                                   f"{owner}_provenance={'archive' if source_archive else 'directory'}"))
        markers[".astrid-distribution-metadata"] = "\n".join(metadata_lines) + "\n"
        (stage / ".astrid-distribution-metadata").write_text(markers[".astrid-distribution-metadata"])
        freeze_urls = {name: url + ("#sha256=" + hashlib.sha256(archive_inputs[name]).hexdigest() if source_archive else "")
                       for name, url in source_urls.items()}
        freeze = [("astrid", f"astrid @ {freeze_urls['agent']}"),
                  ("astrid-runtime", f"astrid-runtime @ {freeze_urls['runtime']}"),
                  ("seedpkg", "seedpkg==1.0.0")]
        if provenance != "missing" and managed:
            freeze.extend((name.split('-')[0], name.split('-')[0] + "==" + name.split('-')[1])
                          for name in bootstrap.BOOTSTRAP_WHEELS)
        report = (f"status=passed\nagent_sha={agent_sha}\nruntime_sha={runtime_sha}\n"
                  f"runtime_client_identity_sha256={hashlib.sha256(markers['.astrid-runtime-client-identity'].encode()).hexdigest()}\n"
                  f"requirements_path=requirements/proof.lock\nrequirements_lock_sha256={hashlib.sha256(lock_bytes).hexdigest()}\n"
                  f"installed_import_origins:\n{markers['.astrid-import-origins']}\ninstalled_distribution_metadata:\n{markers['.astrid-distribution-metadata']}pip_freeze:\n"
                  + "".join(line + "\n" for _, line in sorted(freeze)))
        (stage / ".provision-report").write_text(report)

    def seal(path):
        for item in [path, *path.rglob("*")]:
            item.chmod(item.stat().st_mode & ~0o222)

    if store is not None and make_existing:
        store.ensure("child", identity, {"name": "fixture", "env": "", "suite": "", "requires": []}, build, lambda path: None, seal=seal)
    elif store is None:
        final.mkdir()
        build(final, final)
        seal(final)
    env = os.environ.copy()
    env.pop("CHILD_VENV_DEPENDENCY_WHEELHOUSE", None)
    env.update({"CHILD_VENV_ORCH_ROOT": str(orch), "CHILD_VENV_WORK_ROOT": str(work),
                "CHILD_VENV_PYTHON": str(maker_python)})
    return env, [name, agent_sha, "--source-carrier", str(agent), str(runtime), runtime_sha], wheelhouse


def retain_caller_evidence(label: str, result: subprocess.CompletedProcess[str]) -> None:
    directory = os.environ.get("CHILD_DEPENDENCY_TEST_EVIDENCE")
    if directory:
        Path(directory, label + ".json").write_text(json.dumps({"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}, indent=2) + "\n")


def test_real_maker_preserves_existing_target_arguments(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=False)
    # Optional positional fields must survive parsing along with the carrier.
    args[2:2] = ["base-suite", "remotion-graph"]
    result = subprocess.run([str(MAKER), *args], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("legacy-argument-reuse", result)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "reused child venv path=" in result.stdout and "remotion=remotion-graph" in result.stdout


def private_maker(tmp_path: Path, args: list[str]) -> Path:
    # The production maker pins the approved real lock; the private fixture pins
    # its own tiny lock without changing production trust or installing anything.
    private = tmp_path / "maker-kit"
    private.mkdir()
    source = MAKER.read_text()
    agent = Path(args[3])
    digest = hashlib.sha256((agent / "requirements/proof.lock").read_bytes()).hexdigest()
    source = source.replace("EXPECTED_PROOF_LOCK_SHA256=236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778", "EXPECTED_PROOF_LOCK_SHA256=" + digest)
    maker = private / "make-child-venv"
    maker.write_text(source)
    maker.chmod(0o755)
    (private / VERIFY.name).write_bytes(VERIFY.read_bytes())
    return maker


@pytest.mark.parametrize("provenance", ["valid", "valid-pyc", "missing", "forged-record", "wrong-wheel", "wrong-lock", "unowned-file", "forged-pyc"])
def test_real_maker_seeded_store_reuse(tmp_path: Path, provenance: str) -> None:
    env, args, wheelhouse = retained_fixture(tmp_path, managed=True, provenance=provenance)
    maker = private_maker(tmp_path, args)
    result = subprocess.run([str(maker), *args, "--dependency-wheelhouse", str(wheelhouse)], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("seeded-store-" + provenance, result)
    if provenance in ("valid", "valid-pyc"):
        assert result.returncode == 0, result.stdout + result.stderr
        assert "reused child venv path=" in result.stdout
    else:
        assert result.returncode != 0
        assert "status=passed" not in result.stdout


def test_real_maker_refuses_seeded_top_level_old_child(tmp_path: Path) -> None:
    env, args, wheelhouse = retained_fixture(tmp_path, managed=False, provenance="missing")
    result = subprocess.run([str(MAKER), *args, "--dependency-wheelhouse", str(wheelhouse)], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("seeded-legacy-refusal", result)
    assert result.returncode == 2
    assert "seeded reuse requires Store custody and retained original wheels" in result.stderr


def test_real_maker_keeps_unseeded_store_compatibility(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True, provenance="missing")
    result = subprocess.run([str(MAKER), *args], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("unseeded-store-reuse", result)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "reused child venv path=" in result.stdout


def test_real_maker_rechecks_seeded_store_reuse_without_new_wheelhouse(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True, provenance="forged-record")
    maker = private_maker(tmp_path, args)
    result = subprocess.run([str(maker), *args], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("seeded-store-without-new-input", result)
    assert result.returncode != 0
    assert "status=passed" not in result.stdout
    assert "installed dependency differs from original wheel" in result.stderr


@pytest.mark.parametrize("case", ["valid", "helper-tampered", "helper-symlink", "unapproved-lock"])
def test_seeded_reuse_without_argument_authenticates_helper_and_lock(tmp_path: Path, case: str) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True)
    maker = private_maker(tmp_path, args)
    helper = maker.parent / VERIFY.name
    if case == "helper-tampered":
        helper.write_text("raise SystemExit('UNTRUSTED HELPER EXECUTED')\n")
    elif case == "helper-symlink":
        helper.rename(maker.parent / "original-helper")
        helper.symlink_to(maker.parent / "original-helper")
    elif case == "unapproved-lock":
        maker.write_text(re.sub(r"^EXPECTED_PROOF_LOCK_SHA256=.*$", "EXPECTED_PROOF_LOCK_SHA256=" + "0" * 64, maker.read_text(), flags=re.MULTILINE))
    result = subprocess.run([str(maker), *args], env=env, text=True, capture_output=True, check=False)
    if case == "valid":
        assert result.returncode == 0, result.stdout + result.stderr
        assert "reused child venv path=" in result.stdout
    else:
        assert result.returncode == 2
        assert "untrusted dependency seed verifier" in result.stderr if case.startswith("helper-") else "requires approved proof.lock" in result.stderr
        assert "UNTRUSTED HELPER EXECUTED" not in result.stderr


def test_real_maker_failure_evidence_survives_store_rollback(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True, provenance="missing", make_existing=False)
    failing_python = tmp_path / "failing-python"
    failing_python.write_text(
        """#!/usr/bin/env bash
set -u
case " $* " in
  *" -m venv --help "*) exit 0;;
  *" --bootstrap-identity "*) exec REAL_TEST_PYTHON "$@";;
  *" -m venv --copies "*) T="${@: -1}"; mkdir -p "$T/bin"; cp "$0" "$T/bin/python"; chmod +x "$T/bin/python"; exit 0;;
  *" -m pip install "*) printf '%s\\n' 'ERROR https://user:secret@example.invalid/simple?token=do-not-retain' 'Authorization: Bearer do-not-retain' >&2; exit 23;;
  *) exit 0;;
esac
"""
    )
    failing_python.chmod(0o755)
    env["CHILD_VENV_PYTHON"] = str(failing_python)
    result = subprocess.run([str(MAKER), *args], env=env, text=True, capture_output=True, check=False)
    retain_caller_evidence("stage-failure-rollback", result)
    assert result.returncode == 2
    assert "secret@example.invalid" not in result.stderr
    assert "do-not-retain" not in result.stderr

    failure_dir = Path(env["CHILD_VENV_ORCH_ROOT"]) / "tests/provision-failures"
    record = failure_dir / (args[0] + ".txt")
    assert record.is_file() and not record.is_symlink()
    assert stat.S_IMODE(failure_dir.stat().st_mode) == 0o700
    assert stat.S_IMODE(record.stat().st_mode) == 0o600
    evidence = record.read_text()
    assert evidence.startswith(
        "status=failed\n"
        "stage=bootstrap-pip\n"
        "rc=23\n"
    )
    assert re.search(r"^elapsed_seconds=[0-9]+$", evidence, re.MULTILINE)
    assert f"agent_sha={args[1]}\n" in evidence
    assert f"runtime_sha={args[5]}\n" in evidence
    assert "requirements_path=requirements/proof.lock\n" in evidence
    assert f"lock_sha256={hashlib.sha256((Path(args[3]) / 'requirements/proof.lock').read_bytes()).hexdigest()}\n" in evidence
    assert evidence.endswith("diagnostic=stage-command-failed\n")
    assert "secret@example.invalid" not in evidence
    assert "do-not-retain" not in evidence
    store_root = Path(env["CHILD_VENV_WORK_ROOT"]) / "bench-store"
    assert json.loads((store_root / "index.json").read_text())["entries"] == {}
    assert not (store_root / "pending.json").exists()
    assert list((store_root / "staging").iterdir()) == []


@pytest.mark.parametrize("case", ["oversize", "path", "symlink", "mode", "raw"])
def test_store_failure_evidence_rejects_unsafe_records(tmp_path: Path, case: str) -> None:
    env, _, _ = retained_fixture(tmp_path, managed=True, provenance="missing", make_existing=False)
    store_module = load_helper("failure_store", CANDIDATE / "bench_store.py")
    store = store_module.Store(
        Path(env["CHILD_VENV_WORK_ROOT"]) / "bench-store",
        Path(env["CHILD_VENV_ORCH_ROOT"]) / "tests",
    )
    valid = (
        "status=failed\nstage=bootstrap-pip\nrc=23\nelapsed_seconds=0\n"
        + "agent_sha=" + "a" * 40 + "\nruntime_sha=" + "b" * 40
        + "\nrequirements_path=requirements/proof.lock\nlock_sha256=" + "c" * 64
        + "\ndiagnostic=stage-command-failed\n"
    )
    if case == "oversize":
        with pytest.raises(store_module.Refused, match="failure evidence size"):
            store._record_failure("safe-name", "x" * (store.FAILURE_LIMIT + 1))
    elif case == "path":
        with pytest.raises(store_module.Refused, match="registration name required"):
            store._record_failure("../escape", valid)
    elif case == "symlink":
        folder = store.tests / "provision-failures"
        outside = tmp_path / "outside"
        outside.mkdir()
        folder.symlink_to(outside, target_is_directory=True)
        with pytest.raises(store_module.Refused, match="unsafe failure directory"):
            store._record_failure("safe-name", valid)
    elif case == "mode":
        folder = store.tests / "provision-failures"
        folder.mkdir(mode=0o700)
        folder.chmod(0o755)
        with pytest.raises(store_module.Refused, match="unsafe failure directory"):
            store._record_failure("safe-name", valid)
    else:
        with pytest.raises(store_module.Refused, match="failure evidence schema"):
            store._record_failure("safe-name", "environment=TOKEN=do-not-retain\n")


@pytest.mark.parametrize("changed", ["agent", "runtime", "client"])
def test_real_request_keeps_exact_source_checks(tmp_path: Path, changed: str) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=False)
    checkout = Path(args[3] if changed == "agent" else args[4])
    target = checkout / ("packages/python/astrid_runtime_client/__init__.py" if changed == "client" else "pyproject.toml")
    target.write_bytes(target.read_bytes() + b"# changed\n")
    result = subprocess.run([str(MAKER), *args], env=env, text=True, capture_output=True, check=False)
    assert result.returncode == 2
    assert "dirty" in result.stdout


@pytest.mark.parametrize("mutation", ["foreign-distribution", "foreign-package", "foreign-launcher"])
def test_complete_inventory_is_faithful_oldred_newgreen(tmp_path: Path, mutation: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    site = root / "lib/python3.13/site-packages"
    if mutation == "foreign-distribution":
        write_record(site, "foreign-1.0.dist-info", {
            "foreign-1.0.dist-info/METADATA": b"Name: foreign\nVersion: 1.0\n",
            "foreign/__init__.py": b"FOREIGN = True\n",
        })
        distributions = helper.md.distributions(path=[str(site)])
        helper.md.distributions = lambda path: [*distributions, helper.md.PathDistribution(site / "foreign-1.0.dist-info")]
    elif mutation == "foreign-package":
        (site / "foreign").mkdir()
        (site / "foreign/__init__.py").write_text("FOREIGN = True\n")
    else:
        (root / "bin/foreign-launcher").write_text("#!/bin/sh\nexit 0\n")
        (root / "bin/foreign-launcher").chmod(0o755)
    base = tmp_path / "parent-verifier.py"
    base.write_bytes(subprocess.check_output([
        "git", "show", "ffb92658995e10d3a55dac8bd60946ebe7a55899:ops-handoff/child-dependency-reuse/candidate/verify_dependency_seed.py",
    ]))
    old = load_helper("pre_inventory_verifier", base)
    old.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})
    with pytest.raises(SystemExit, match="unowned installed"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("mutation", [
    "pip", "setuptools", "wheel", "interpreter", "alias", "activation",
    "empty-package", "hidden-file", "bin-directory", "directory-link", "hardlink",
])
def test_inventory_bootstrap_allowlist_is_narrow(tmp_path: Path, mutation: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    site = root / "lib/python3.13/site-packages"
    expected = "unowned installed"
    if mutation in {"pip", "setuptools", "wheel"}:
        metadata = f"{mutation}-99.0.dist-info"
        write_record(site, metadata, {f"{metadata}/METADATA": f"Name: {mutation}\nVersion: 99.0\n".encode()})
        distributions = helper.md.distributions(path=[str(site)])
        helper.md.distributions = lambda path: [*distributions, helper.md.PathDistribution(site / metadata)]
        expected = f"missing authenticated original bootstrap wheel: {mutation}==99.0"
    elif mutation == "interpreter":
        (root / "bin/python").write_bytes(b"forged interpreter")
        expected = "child interpreter differs"
    elif mutation == "alias":
        (root / "bin/python3").write_bytes(b"forged alias")
        expected = "child interpreter differs"
    elif mutation == "activation":
        (root / "bin/activate").write_text("arbitrary shell code\n")
    elif mutation == "empty-package":
        (site / "foreign").mkdir()
    elif mutation == "hidden-file":
        (site / ".foreign.pth").write_text("import foreign\n")
    elif mutation == "bin-directory":
        (root / "bin/foreign").mkdir()
    elif mutation == "directory-link":
        (site / "foreign").symlink_to(site / "seedpkg", target_is_directory=True)
        expected = "symlinked or foreign"
    else:
        os.link(root / "bin/python", root / "bin/foreign")
        expected = "not a regular file"
    with pytest.raises(SystemExit, match=expected):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def test_inventory_does_not_exempt_bootstrap_record_additions(tmp_path: Path) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    site = root / "lib/python3.13/site-packages"
    import base64
    content = b"unowned pip bootstrap file\n"
    target = site / "pip/foreign.py"
    target.parent.mkdir()
    target.write_bytes(content)
    with (site / "seedpkg-1.0.0.dist-info/RECORD").open("a") as output:
        digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
        output.write(f"pip/foreign.py,sha256={digest},{len(content)}\n")
    with pytest.raises(SystemExit, match="unowned installed dependency file"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("alias", ["python3", "python3.13"])
def test_bootstrap_interpreter_copy_is_byte_authenticated(tmp_path: Path, alias: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    (root / "bin" / alias).write_bytes(Path(sys.executable).resolve().read_bytes())
    helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def run_source_ownership_verifier(env: dict[str, str], args: list[str]) -> subprocess.CompletedProcess[str]:
    root = Path(env["CHILD_VENV_WORK_ROOT"]) / args[0]
    source = MAKER.read_text().split("# STORE_VERIFY_BEGIN\n", 1)[1].split("# STORE_VERIFY_END", 1)[0]
    return subprocess.run([
        sys.executable, "-B", "-I", "-", str(root),
        (root / ".astrid-runtime-client-identity").read_text().rstrip("\n"),
        args[3], args[1], args[4], args[5], env["CHILD_VENV_WORK_ROOT"], env["CHILD_VENV_PYTHON"],
    ], input=source, text=True, capture_output=True, check=False)


def test_committed_local_ownership_composes_with_wheel_inventory(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=False)
    result = run_source_ownership_verifier(env, args)
    assert result.returncode == 0, result.stderr
    helper = load_helper("local_ownership_inventory", VERIFY)
    # Earlier fixtures replace the shared metadata discovery function.
    site = Path(env["CHILD_VENV_WORK_ROOT"]) / args[0] / "lib/python3.13/site-packages"
    helper.md.distributions = lambda path: [helper.md.PathDistribution(p) for p in site.glob("*.dist-info")]
    old_args = sys.argv
    try:
        sys.argv = [str(VERIFY), str(site.parents[2] / ".dependency-wheelhouse"), "-",
                    "--committed-lock", args[3], args[1], "requirements/proof.lock",
                    hashlib.sha256((Path(args[3]) / "requirements/proof.lock").read_bytes()).hexdigest(),
                    "--maker-python", env["CHILD_VENV_PYTHON"], "--installed", str(site.parents[2])]
        assert helper.main(local_inventory={k: set(v) for k, v in json.loads(result.stdout).items()}) == 0
    finally:
        sys.argv = old_args


@pytest.mark.parametrize("mutation", ["foreign-package", "foreign-launcher", "metadata", "installer"])
def test_source_record_cannot_launder_inventory_additions(tmp_path: Path, mutation: str) -> None:
    import base64

    env, args, _ = retained_fixture(tmp_path, managed=False)
    root = Path(env["CHILD_VENV_WORK_ROOT"]) / args[0]
    site = root / "lib/python3.13/site-packages"
    record = site / "astrid-1.0.dist-info/RECORD"
    rel = {
        "foreign-package": "foreign/__init__.py",
        "foreign-launcher": "../../../bin/foreign-launcher",
        "metadata": "astrid-1.0.dist-info/foreign-metadata",
        "installer": "astrid-1.0.dist-info/INSTALLER",
    }[mutation]
    target = site / rel
    target.parent.chmod(0o755) if target.parent.exists() else site.chmod(0o755)
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(b"arbitrary payload\n")
    record.chmod(0o644)
    digest = base64.urlsafe_b64encode(hashlib.sha256(target.read_bytes()).digest()).decode().rstrip("=")
    with record.open("a") as output:
        output.write(f"{rel},sha256={digest},{target.stat().st_size}\n")
    for path in [root, *root.rglob("*")]:
        path.chmod(path.stat().st_mode & ~0o222)
    result = run_source_ownership_verifier(env, args)
    assert result.returncode != 0
    assert "unowned local distribution" in result.stderr or "unexpected local installer" in result.stderr


def materialize_bootstrap(helper, stage: Path, destination: Path) -> dict[str, bytes]:
    """Materialize original wheel bytes plus canonical pip wrappers, no installs."""
    import configparser
    import io

    artifacts = helper.bootstrap_artifacts(BOOTSTRAP_ARCHIVE)
    site = stage / "lib/python3.13/site-packages"
    for filename, data in artifacts.items():
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            files = {entry.filename: archive.read(entry) for entry in archive.infolist()
                     if not entry.is_dir() and not entry.filename.endswith("/RECORD")}
        metadata = next(rel.split("/")[0] for rel in files if rel.endswith(".dist-info/METADATA"))
        parser = configparser.ConfigParser()
        entry = metadata + "/entry_points.txt"
        if entry in files:
            parser.read_string(files[entry].decode())
        scripts = dict(parser.items("console_scripts")) if parser.has_section("console_scripts") else {}
        if filename.startswith("pip-"):
            scripts["pip3.13"] = scripts["pip"]
        for name, target in scripts.items():
            module, function = target.split(":")
            executable = str(destination / "bin/python")
            if " " in executable:
                executable = '"' + executable + '"'
            files["../../../bin/" + name] = (
                f"#!{executable}\nimport sys\nfrom {module} import {function}\n"
                "if __name__ == '__main__':\n"
                "    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n"
                f"    sys.exit({function}())\n").encode()
        write_record(site, metadata, files)
    return artifacts


@pytest.mark.parametrize("rel", [
    "lib/python3.13/foreign-runtime-file.py", "foreign-runtime-file.py",
    "include/foreign.h", ".hidden/foreign-executable", "lib/python9.99/foreign.py",
])
def test_whole_root_inventory_is_faithful_oldred_newgreen(tmp_path: Path, rel: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("arbitrary payload\n")
    target.chmod(0o755)
    old_path = tmp_path / "old-whole-root.py"
    old_path.write_bytes(subprocess.check_output([
        "git", "show", "83353b588c122b05a1325687db4e7e2e6be973ae:ops-handoff/child-dependency-reuse/candidate/verify_dependency_seed.py",
    ]))
    old = load_helper("before_whole_root", old_path)
    old.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})
    with pytest.raises(SystemExit, match="unowned installed"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


@pytest.mark.parametrize("mutation", ["empty-sibling", "outside-link", "lib64-escape", "lib64-file"])
def test_whole_root_structural_allowances_are_narrow(tmp_path: Path, mutation: str) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    if mutation == "empty-sibling":
        (root / "lib/foreign").mkdir()
    elif mutation == "outside-link":
        (root / "foreign").symlink_to(tmp_path)
    elif mutation == "lib64-escape":
        (root / "lib64").symlink_to(tmp_path)
    else:
        (root / "lib64").write_text("payload")
    with pytest.raises(SystemExit, match="unowned installed|symlinked or foreign|escapes child"):
        helper.installed_integrity(root, {"seedpkg-1.0.0-py3-none-any.whl": data})


def bootstrap_fixture(tmp_path: Path, monkeypatch):
    helper = load_helper("genuine_bootstrap", VERIFY)
    root = tmp_path / "child with spaces"
    (root / "bin").mkdir(parents=True)
    (root / "lib/python3.13/site-packages").mkdir(parents=True)
    for alias in ("python", "python3", "python3.13"):
        (root / "bin" / alias).write_bytes(Path(sys.executable).resolve().read_bytes())
    for rel, data in helper.venv_files(root).items():
        (root / rel).write_bytes(data)
    monkeypatch.setattr(helper.md, "distributions", lambda path: [helper.md.PathDistribution(p) for p in Path(path[0]).glob("*.dist-info")])
    monkeypatch.setattr(sys, "argv", [str(VERIFY), "--prepare-bootstrap", str(BOOTSTRAP_ARCHIVE), str(root), sys.executable])
    assert helper.main() == 0
    artifacts = materialize_bootstrap(helper, root, root)
    helper.installed_integrity(root, artifacts, interpreter=Path(sys.executable), bootstrap=True)
    return helper, root, artifacts


def test_genuine_bootstrap_inputs_and_host_activation_are_usable(tmp_path: Path, monkeypatch) -> None:
    helper, root, artifacts = bootstrap_fixture(tmp_path, monkeypatch)
    assert len(artifacts) == 3
    assert not any(name.startswith(("execnet-", "pytest_xdist-")) for name in artifacts)
    assert helper.retained_bootstrap(root, Path(sys.executable)) == artifacts
    assert "child with spaces" in (root / "bin/activate").read_text()
    observed = []

    def installer(args, *, pass_fds, check):
        assert check and "runpy.run_module" in args[3]
        assert "--ignore-installed" in args
        assert "--require-hashes" in args and "--no-index" in args
        assert Path(args[4]).read_bytes() == artifacts[next(n for n in artifacts if n.startswith("pip-"))]
        observed.append(args)

    monkeypatch.setattr(helper.subprocess, "run", installer)
    helper.install_snapshot(root / ".bootstrap-wheelhouse", helper.BOOTSTRAP_LOCK, [], python=str(root / "bin/python"))
    assert len(observed) == 1


@pytest.mark.parametrize("rel", [
    "bin/activate", "bin/activate.csh", "bin/Activate.ps1", "pyvenv.cfg",
    "bin/python", ".bootstrap-authority", ".bootstrap-input.tgz",
    ".bootstrap-wheelhouse/requirements.txt",
    ".bootstrap-wheelhouse/pip-26.2.1-py3-none-any.whl",
    ".bootstrap-wheelhouse/foreign-file", "lib/python3.13/foreign.py",
])
def test_genuine_bootstrap_rejects_retained_input_and_activation_corruption(tmp_path: Path, monkeypatch, rel: str) -> None:
    helper, root, artifacts = bootstrap_fixture(tmp_path, monkeypatch)
    target = root / rel
    target.parent.chmod(0o755)
    if target.exists():
        target.chmod(0o644)
    target.write_bytes(b"arbitrary replacement\n")
    with pytest.raises(SystemExit):
        helper.installed_integrity(root, artifacts, interpreter=Path(sys.executable), bootstrap=True)


@pytest.mark.parametrize("mutation", ["source-extra", "source-empty-dir", "metadata", "report", "marker"])
def test_retained_source_and_maker_metadata_are_closed(tmp_path: Path, mutation: str) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=False, provenance="missing")
    root = Path(env["CHILD_VENV_WORK_ROOT"]) / args[0]
    target = {
        "source-extra": ".child-venv-source-fixture/agent/foreign.py",
        "source-empty-dir": ".child-venv-source-fixture/runtime/foreign",
        "metadata": ".astrid-distribution-metadata",
        "report": ".provision-report",
        "marker": ".astrid-source-commit",
    }[mutation]
    path = root / target
    path.parent.chmod(0o755)
    if mutation == "source-empty-dir":
        path.mkdir()
    else:
        if path.exists():
            path.chmod(0o644)
        with path.open("a") as output:
            output.write("arbitrary payload\n")
    for item in [root, *root.rglob("*")]:
        item.chmod(item.stat().st_mode & ~0o222)
    result = run_source_ownership_verifier(env, args)
    assert result.returncode != 0
    assert "unowned retained source" in result.stderr or "differs from" in result.stderr


def test_trusted_venv_source_identity_is_rechecked(tmp_path: Path, monkeypatch) -> None:
    helper, root, artifacts = bootstrap_fixture(tmp_path, monkeypatch)
    original = helper.trusted_venv_sources()
    source = next(name for name in original if name.endswith("/activate"))
    changed = {**original, source: original[source] + b"\n# changed host source\n"}
    monkeypatch.setattr(helper, "trusted_venv_sources", lambda: changed)
    with pytest.raises(SystemExit, match="trusted host source|source/interpreter authority"):
        helper.installed_integrity(root, artifacts, interpreter=Path(sys.executable), bootstrap=True)


def test_genuine_activation_support_is_faithful_oldred_newgreen(tmp_path: Path, monkeypatch) -> None:
    helper, root, data = installed_dependency_fixture(tmp_path)
    artifacts = {"seedpkg-1.0.0-py3-none-any.whl": data}
    for alias in ("python3", "python3.13"):
        (root / "bin" / alias).write_bytes(Path(sys.executable).resolve().read_bytes())
    for rel, content in helper.venv_files(root).items():
        (root / rel).write_bytes(content)
    helper.write_snapshot(root / ".bootstrap-wheelhouse", helper.BOOTSTRAP_LOCK,
                          helper.bootstrap_artifacts(BOOTSTRAP_ARCHIVE))
    (root / ".bootstrap-input.tgz").write_bytes(BOOTSTRAP_ARCHIVE.read_bytes())
    (root / ".bootstrap-authority").write_text(helper.bootstrap_identity(Path(sys.executable)) + "\n")
    old_path = tmp_path / "before-bootstrap-authority.py"
    old_path.write_bytes(subprocess.check_output([
        "git", "show", "1d3b123ee65a2f0204f9232ade0a0ef9ce3a4694:ops-handoff/child-dependency-reuse/candidate/verify_dependency_seed.py",
    ]))
    old = load_helper("before_bootstrap_authority", old_path)
    with pytest.raises(SystemExit, match="unowned installed file: bin/"):
        old.installed_integrity(root, artifacts, interpreter=Path(sys.executable))
    helper.installed_integrity(root, artifacts, interpreter=Path(sys.executable), bootstrap=True)


@pytest.mark.parametrize("mutation", ["valid", "archive", "archive-extra", "store-metadata"])
def test_normal_maker_reverifies_genuine_source_archive_custody(tmp_path: Path, mutation: str) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True, source_archive=True)
    root, = (Path(env["CHILD_VENV_WORK_ROOT"]) / "bench-store/entries").iterdir()
    if mutation != "valid":
        target = root / ({"archive": ".source-inputs/agent.tar", "archive-extra": ".source-inputs/foreign.tar",
                          "store-metadata": ".bench-owner.json"}[mutation])
        target.parent.chmod(0o755)
        if target.exists():
            target.chmod(0o644)
        target.write_bytes(b"arbitrary replacement\n")
        for item in [root, *root.rglob("*")]:
            item.chmod(item.stat().st_mode & ~0o222)
    maker = private_maker(tmp_path, args)
    result = subprocess.run([str(maker), *args], env=env, text=True, capture_output=True, check=False)
    if mutation == "valid":
        assert result.returncode == 0, result.stdout + result.stderr
        assert "reused child venv path=" in result.stdout
    else:
        assert result.returncode != 0
        assert "status=passed" not in result.stdout


@pytest.mark.parametrize("alias", ["python3", "python3.13"])
def test_bootstrap_reuse_requires_complete_interpreter_aliases(tmp_path: Path, monkeypatch, alias: str) -> None:
    helper, root, artifacts = bootstrap_fixture(tmp_path, monkeypatch)
    # Relocation of the fixture alias simulates a missing original venv file.
    (root / "bin" / alias).rename(tmp_path / alias)
    with pytest.raises(SystemExit, match="missing bootstrap interpreter"):
        helper.installed_integrity(root, artifacts, interpreter=Path(sys.executable), bootstrap=True)
