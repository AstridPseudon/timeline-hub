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
    pinned = [line for line in records if line.startswith("VERIFIER ") and "--install" in line]
    assert len(pinned) == 1
    assert "--committed-lock" in pinned[0]
    assert ".dependency-wheelhouse" in pinned[0]
    assert str(wheelhouse) not in pinned[0]


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


def installed_dependency_fixture(tmp_path: Path, *, script: bytes | None = None):
    helper = load_helper("installed_dependency_fixture", VERIFY)
    root = tmp_path / "child"
    site = root / "lib/python3.13/site-packages"
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    artifact = wheel(
        wheelhouse,
        "seedpkg-1.0.0-py3-none-any.whl",
        console_script="seed-tool = seedpkg:main",
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
    root.joinpath("bin/python").write_bytes(b"python")
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
            self.files = [Path("seedpkg-1.0.0.dist-info/RECORD")]

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
    tmp_path: Path, *, managed: bool, provenance: str = "valid", make_existing: bool = True
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
    maker_python.write_text(f'#!/bin/bash\ncase "$*" in *verify_dependency_seed.py*) exec {shlex.quote(sys.executable)} "$@";; esac\nexit 0\n')
    maker_python.chmod(0o755)
    name = "venv-agent-child-retained"
    store = store_module.Store.initialize(work / "bench-store", orch / "tests") if managed else None
    final = (work / "bench-store/entries" / ("child-" + store_module.key_for("child", identity))) if managed else work / name

    def build(stage, destination):
        source = destination / ".child-venv-source-fixture"
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
            files[metadata + "/direct_url.json"] = json.dumps({"url": (source / snapshot).as_uri(), "dir_info": {}}).encode()
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
        markers = {".astrid-source-commit": agent_sha, ".astrid-runtime-source-commit": runtime_sha,
                   ".astrid-runtime-client-identity": "\n".join(f"{key}={value}" for key, value in identity["client_tuple"].items()),
                   ".astrid-import-origins": "\n".join(f"{module}={destination}/lib/python3.13/site-packages/{module}/__init__.py" for module in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client")),
                   ".astrid-distribution-metadata": ""}
        for marker, value in markers.items():
            (stage / marker).write_text(value + ("\n" if value else ""))
        report = (f"status=passed\nagent_sha={agent_sha}\nruntime_sha={runtime_sha}\nrequirements_path=requirements/proof.lock\nrequirements_lock_sha256={hashlib.sha256(lock_bytes).hexdigest()}\n"
                  f"runtime_client_identity_sha256={hashlib.sha256(markers['.astrid-runtime-client-identity'].encode()).hexdigest()}\n"
                  f"installed_import_origins:\n{markers['.astrid-import-origins']}\ninstalled_distribution_metadata:\npip_freeze:\n")
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


@pytest.mark.parametrize("provenance", ["valid", "valid-pyc", "missing", "forged-record", "wrong-wheel", "wrong-lock", "unowned-file", "forged-pyc"])
def test_real_maker_seeded_store_reuse(tmp_path: Path, provenance: str) -> None:
    env, args, wheelhouse = retained_fixture(tmp_path, managed=True, provenance=provenance)
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


def test_real_maker_failure_evidence_survives_store_rollback(tmp_path: Path) -> None:
    env, args, _ = retained_fixture(tmp_path, managed=True, provenance="missing", make_existing=False)
    failing_python = tmp_path / "failing-python"
    failing_python.write_text(
        """#!/usr/bin/env bash
set -u
case " $* " in
  *" -m venv --help "*) exit 0;;
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
