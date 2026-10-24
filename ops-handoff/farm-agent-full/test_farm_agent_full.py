from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

PACKET = Path(__file__).parent
ORCH = Path(os.environ.get(
    "FARM_ORCH_ROOT",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
))
BENCH_SOURCE = ORCH / "bin" / "bench_store.py"
HELPER = PACKET / "init-bench-store.py"


def _snapshot(root: Path) -> tuple:
    if not root.exists() and not root.is_symlink():
        return ("absent",)
    rows = []
    for path in sorted((root, *root.rglob("*")), key=str):
        info = path.lstat()
        relative = "." if path == root else str(path.relative_to(root))
        if path.is_symlink():
            value = (relative, "symlink", os.readlink(path))
        elif path.is_file():
            value = (relative, "file", hashlib.sha256(path.read_bytes()).hexdigest(), info.st_mode)
        else:
            value = (relative, "directory", info.st_mode)
        rows.append(value)
    return tuple(rows)


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    orch = tmp_path / "orch"
    tests = orch / "tests"
    tests.mkdir(parents=True)
    (tests / "suites.conf").write_bytes(b"agent full /bin/true\n")
    return orch, tests, BENCH_SOURCE


def _run(orch: Path, root: Path, bench_store: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = str(orch.parent / "tmp")
    Path(env["TMPDIR"]).mkdir(exist_ok=True)
    return subprocess.run(
        [
            sys.executable,
            str(HELPER),
            "--orch-root",
            str(orch),
            "--store-root",
            str(root),
            "--bench-store",
            str(bench_store),
        ],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_absent_store_initializes_reopens_and_reuses(tmp_path: Path) -> None:
    orch, _tests, bench_store = _fixture(tmp_path)
    root = tmp_path / "bench-store"
    first = _run(orch, root, bench_store)
    assert first.returncode == 0, first.stderr
    assert first.stdout.startswith("initialized owner=")
    owner_before = (root / "owner.json").read_bytes()
    index_before = (root / "index.json").read_bytes()
    second = _run(orch, root, bench_store)
    assert second.returncode == 0, second.stderr
    assert second.stdout.startswith("reused owner=")
    assert second.stdout == first.stdout.replace("initialized", "reused")
    assert (root / "owner.json").read_bytes() == owner_before
    assert (root / "index.json").read_bytes() == index_before


def _assert_refused_without_write(orch: Path, root: Path, bench_store: Path) -> None:
    before = _snapshot(root)
    result = _run(orch, root, bench_store)
    assert result.returncode == 2
    assert result.stderr.startswith("REFUSED:")
    assert _snapshot(root) == before


def test_unknown_partial_symlink_foreign_wrong_tests_and_root_identity_refuse(tmp_path: Path) -> None:
    orch, _tests, bench_store = _fixture(tmp_path)

    unknown = tmp_path / "unknown"
    unknown.mkdir()
    (unknown / "unowned").write_bytes(b"keep")
    _assert_refused_without_write(orch, unknown, bench_store)

    partial = tmp_path / "partial"
    partial.mkdir()
    (partial / "owner.json").write_text("{}", encoding="utf-8")
    _assert_refused_without_write(orch, partial, bench_store)

    target = tmp_path / "symlink-target"
    target.mkdir()
    symlink = tmp_path / "symlink"
    symlink.symlink_to(target, target_is_directory=True)
    _assert_refused_without_write(orch, symlink, bench_store)
    assert _snapshot(target) == ((".", "directory", target.lstat().st_mode),)

    foreign = tmp_path / "foreign"
    assert _run(orch, foreign, bench_store).returncode == 0
    owner = json.loads((foreign / "owner.json").read_text(encoding="utf-8"))
    owner["uid"] = owner["uid"] + 1
    (foreign / "owner.json").write_text(json.dumps(owner), encoding="utf-8")
    _assert_refused_without_write(orch, foreign, bench_store)

    wrong_orch = tmp_path / "wrong-orch"
    wrong_tests = wrong_orch / "tests"
    wrong_tests.mkdir(parents=True)
    (wrong_tests / "suites.conf").write_bytes(b"agent other /bin/false\n")
    valid = tmp_path / "valid"
    assert _run(orch, valid, bench_store).returncode == 0
    before = _snapshot(valid)
    result = _run(wrong_orch, valid, bench_store)
    assert result.returncode == 2
    assert result.stderr.startswith("REFUSED:")
    assert _snapshot(valid) == before

    identity = tmp_path / "root-identity"
    assert _run(orch, identity, bench_store).returncode == 0
    owner = json.loads((identity / "owner.json").read_text(encoding="utf-8"))
    owner["root"] = str(tmp_path / "not-the-root")
    (identity / "owner.json").write_text(json.dumps(owner), encoding="utf-8")
    _assert_refused_without_write(orch, identity, bench_store)


def test_approved_template_attachments_are_byte_exact() -> None:
    row_source = ORCH / "design" / "peer-app2-to-app2-20261023T1835-remotion-env-nodes.row.b64"
    env_source = ORCH / "design" / "peer-app2-to-app2-20261023T1835-agent-remotion.env.b64"
    assert (PACKET / "remotion-env-nodes.row.b64").read_bytes() == row_source.read_bytes()
    assert (PACKET / "agent-remotion.env.b64").read_bytes() == env_source.read_bytes()
    row = base64.b64decode((PACKET / "remotion-env-nodes.row.b64").read_bytes())
    env = base64.b64decode((PACKET / "agent-remotion.env.b64").read_bytes())
    assert len(row) == 709 and row.endswith(b"\n")
    assert hashlib.sha256(row[:-1]).hexdigest() == "ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036"
    assert hashlib.sha256(env).hexdigest() == "e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02"


def test_full_farm_row_extends_the_current_full_command_without_repinning() -> None:
    current = next(
        line for line in (ORCH / "tests" / "suites.conf").read_bytes().splitlines()
        if line.split(None, 2)[:2] == [b"agent", b"full"]
    )
    candidate = (PACKET / "registration-row.txt").read_text(encoding="utf-8").rstrip("\n")
    current_command = current.split(None, 2)[2].decode()
    assert candidate.startswith("agent full-farm ")
    assert candidate.endswith(current_command)
    runtime = "/home/user/work/wt/rt-pin-45c3a7f4"
    assert f"ASTRID_RUNTIME_CHECKOUT={runtime}" in candidate
    assert f'PYTHONPATH="$PWD:{runtime}"' in candidate
    lock = json.loads((Path("/home/user/work/agent") / "runtime.lock.json").read_text(encoding="utf-8"))
    assert lock["source_commit"] == "45c3a7f476e1c5f74fafc15956a58b9871eee21f"
