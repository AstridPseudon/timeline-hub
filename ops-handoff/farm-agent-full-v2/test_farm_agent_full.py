from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest

PACKET = Path(__file__).parent
ORCH = Path(os.environ.get(
    "FARM_ORCH_ROOT",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
))
BENCH_SOURCE = ORCH / "bin" / "bench_store.py"
SOURCE = json.loads((PACKET / "runtime-source-selection.json").read_bytes())
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
RUNTIME = "/home/user/work/wt/rt-pin-1d9ddba5"
SCHEMA = "/home/user/work/venv-agent/lib/python3.13/site-packages"


def _api():
    spec = importlib.util.spec_from_file_location("farm_v2_bench_store", BENCH_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _private_fixture(tmp_path: Path, full_farm: bytes = b""):
    orch = tmp_path / "orch"
    tests = orch / "tests"
    tests.mkdir(parents=True)
    full = b"agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n"
    (tests / "suites.conf").write_bytes(full + full_farm + b"agent outside /bin/true\n")
    return orch, tests, full


def _managed_runtime(api, root: Path, tests: Path, tmp_path: Path):
    # The production reserve is a host-capacity gate, not part of this small
    # private projection fixture. Keep Store.ensure itself unchanged while
    # allowing the fixture to run on the constrained worker volume.
    api.Store.RESERVE_BYTES = 0
    store = api.Store.initialize(root, tests)
    identity = {"remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db"}
    profile = tmp_path / "managed-profile"
    (profile / "node_modules" / "react").mkdir(parents=True)
    def build(stage: Path, _final: Path) -> None:
        source = stage / "runtime_protocol"
        source.mkdir()
        (source / "__init__.py").write_text("\n", encoding="utf-8")
        (source / "external_pack_sources.py").write_text(
            "MARKER = 'authenticated-runtime-source'\n", encoding="utf-8"
        )

    def verify(path: Path) -> None:
        assert (path / "runtime_protocol" / "external_pack_sources.py").is_file()

    env = (
        f"PATH={NODE.rsplit('/bin/', 1)[0]}/bin:/usr/bin:/bin\n"
        f"ASTRID_REMOTION_PROJECT_DIR={profile}\n"
        f"ASTRID_NODE_EXECUTABLE={NODE}\n"
        f"ASTRID_TIMELINE_SCHEMA_PYTHONPATH={SCHEMA}\n"
    )
    suite = "agent managed-runtime /home/user/work/venv-agent/bin/python -m pytest -q\n"
    entry = store.ensure(
        "runtime",
        identity,
        {"name": "managed-runtime", "env": env, "suite": suite},
        build,
        verify,
    )
    return store, entry, profile


def _row_command(row: bytes) -> str:
    fields = row.decode("utf-8").split(None, 2)
    assert fields[:2] == ["agent", "full-farm"] and len(fields) == 3
    return fields[2].rstrip("\n")


def _candidate_row() -> bytes:
    row = (PACKET / "registration-row.txt").read_bytes()
    assert row.endswith(b"\n") and row.count(b"\n") == 1
    command = _row_command(row)
    tokens = shlex.split(command)
    assert tokens[:2] == ["test", "-d"]
    assert "${FARM_RECEIPT_MANAGED_PROFILE:?normal managed Remotion receipt required}/node_modules/react" in tokens[2]
    assert "env" in tokens and "-i" in tokens
    assert f"PATH={NODE.rsplit('/bin/', 1)[0]}/bin:" in command
    assert f"ASTRID_NODE_EXECUTABLE={NODE}" in command
    assert f"ASTRID_TIMELINE_SCHEMA_PYTHONPATH={SCHEMA}" in command
    assert f"ASTRID_RUNTIME_CHECKOUT={RUNTIME}" in command
    assert f'PYTHONPATH="$PWD:{RUNTIME}"' in command
    assert command.endswith("/home/user/work/venv-agent/bin/python -m pytest -q -n 3")
    return row


def _suite_rows(data: bytes, repo: str, suite: str) -> list[bytes]:
    return [row for row in data.splitlines(keepends=True)
            if row.decode("utf-8").split(None, 2)[:2] == [repo, suite]]


def _replace_full_farm_row(api, store, tests: Path, expected: bytes, candidate: bytes) -> bytes:
    command = _row_command(candidate)
    if RUNTIME not in command or "rt-pin-45c3a7f4" in command:
        raise api.Refused("candidate uses an unauthenticated Runtime source")
    current = tests.joinpath("suites.conf").read_bytes()
    if current != expected:
        raise api.Refused("suite registry drift")
    old_rows = _suite_rows(current, "agent", "full-farm")
    if len(old_rows) != 1:
        raise api.Refused("full-farm row must exist exactly once")
    replacement = current.replace(old_rows[0], candidate, 1)
    with store.mutex():
        if tests.joinpath("suites.conf").read_bytes() != expected:
            raise api.Refused("suite registry drift")
        api.atomic(tests / "suites.conf", replacement.decode("utf-8"))
    try:
        names = store.names_for_suite("agent", "full-farm", command.rstrip("\n"))
        assert names == ["managed-runtime"]
    except Exception:
        with store.mutex():
            if tests.joinpath("suites.conf").read_bytes() == replacement:
                api.atomic(tests / "suites.conf", expected.decode("utf-8"))
        raise
    return replacement


def test_packet_source_and_candidate_row_are_explicit() -> None:
    assert hashlib.sha256(BENCH_SOURCE.read_bytes()).hexdigest() == (
        "6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8"
    )
    assert SOURCE["declared_runtime_source_commit"] == "45c3a7f476e1c5f74fafc15956a58b9871eee21f"
    assert SOURCE["required_runtime_source_commit"] == "1d9ddba546f8fb1300f55ff62607ed492719cbaa"
    assert SOURCE["status"].startswith("source checkout")
    row = _candidate_row()
    assert b"rt-pin-45c3a7f4" not in row
    assert b"ASTRID_RUNTIME_CHECKOUT=" in row and b'PYTHONPATH="$PWD:' in row


def test_candidate_template_holds_without_managed_receipt(tmp_path: Path) -> None:
    command = _row_command(_candidate_row())
    result = subprocess.run(
        ["bash", "-c", command],
        cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin"},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "normal managed Remotion receipt required" in result.stderr


def test_existing_store_replaces_one_full_farm_row_and_runs_selected_recipe(
    tmp_path: Path,
) -> None:
    api = _api()
    old = b"agent full-farm env OLD_PROFILE=/stale ASTRID_RUNTIME_CHECKOUT=/old /bin/false\n"
    _orch, tests, full = _private_fixture(tmp_path, old)
    root = tmp_path / "bench-store"
    store, _entry, _profile = _managed_runtime(api, root, tests, tmp_path)
    store = api.Store(root, tests)
    candidate = _candidate_row()
    baseline = tests.joinpath("suites.conf").read_bytes()
    assert baseline.endswith(b"\n") and baseline.count(full) == 1
    assert _suite_rows(baseline, "agent", "full-farm") == [old]
    post = _replace_full_farm_row(api, store, tests, baseline, candidate)
    assert tests.joinpath("suites.conf").read_bytes() == post
    assert _suite_rows(post, "agent", "full-farm") == [candidate]
    assert _suite_rows(post, "agent", "full") == [full]
    assert post.replace(candidate, b"") == baseline.replace(old, b"")
    selected = _suite_rows(post, "agent", "full-farm")[0]
    assert selected == candidate

    runtime = tmp_path / "runtime-source"
    (runtime / "runtime_protocol").mkdir(parents=True)
    (runtime / "runtime_protocol" / "__init__.py").write_text("\n", encoding="utf-8")
    (runtime / "runtime_protocol" / "external_pack_sources.py").write_text(
        "ORIGIN = 'external_pack_sources'\n", encoding="utf-8"
    )
    profile = tmp_path / "receipt-profile"
    (profile / "node_modules" / "react").mkdir(parents=True)
    child = (
        "import json, os, pathlib, subprocess, sys, "
        "runtime_protocol.external_pack_sources as p; "
        "print(json.dumps({'path': str(pathlib.Path(p.__file__).resolve()), "
        "'env': {k: os.environ[k] for k in ('PATH', 'ASTRID_REMOTION_PROJECT_DIR', "
        "'ASTRID_NODE_EXECUTABLE', 'ASTRID_TIMELINE_SCHEMA_PYTHONPATH', "
        "'ASTRID_RUNTIME_CHECKOUT', 'PYTHONPATH')}, 'node': subprocess.check_output(["
        "os.environ['ASTRID_NODE_EXECUTABLE'], '--version'], text=True).strip()}, "
        "sort_keys=True))"
    )
    command = _row_command(selected)
    command = command.replace(
        "/home/user/work/wt/rt-pin-1d9ddba5",
        str(runtime),
    ).replace(
        "/home/user/work/venv-agent/bin/python -m pytest -q -n 3",
        f"/home/user/work/venv-agent/bin/python -c {shlex.quote(child)}",
    )
    env = dict(os.environ, FARM_RECEIPT_MANAGED_PROFILE=str(profile))
    result = subprocess.run(["bash", "-c", command], cwd=tmp_path, env=env,
                            text=True, capture_output=True, check=True)
    observed = json.loads(result.stdout)
    assert observed["env"]["ASTRID_NODE_EXECUTABLE"] == NODE
    assert observed["env"]["ASTRID_RUNTIME_CHECKOUT"] == str(runtime)
    assert observed["env"]["ASTRID_REMOTION_PROJECT_DIR"] == str(profile)
    assert observed["env"]["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"] == SCHEMA
    assert observed["env"]["PYTHONPATH"].endswith(f":{runtime}")
    assert observed["path"].startswith(str(runtime))
    assert observed["node"] == "v20.19.4"


def test_projection_refuses_wrong_source_without_store_mutation(tmp_path: Path) -> None:
    api = _api()
    old = b"agent full-farm env OLD_PROFILE=/stale /bin/false\n"
    _orch, tests, _full = _private_fixture(tmp_path, old)
    store, _entry, _profile = _managed_runtime(api, tmp_path / "store", tests, tmp_path)
    valid = _candidate_row()
    baseline = tests.joinpath("suites.conf").read_bytes()
    bad = valid.replace(b"rt-pin-1d9ddba5", b"rt-pin-45c3a7f4")
    with pytest.raises(api.Refused, match="unauthenticated Runtime source"):
        _replace_full_farm_row(api, store, tests, baseline, bad)
    assert tests.joinpath("suites.conf").read_bytes() == baseline


def test_existing_store_replacement_refuses_registry_drift(tmp_path: Path) -> None:
    api = _api()
    old = b"agent full-farm env OLD_PROFILE=/stale /bin/false\n"
    _orch, tests, _full = _private_fixture(tmp_path, old)
    store, _entry, _profile = _managed_runtime(api, tmp_path / "store", tests, tmp_path)
    valid = _candidate_row()
    baseline = tests.joinpath("suites.conf").read_bytes()
    drifted = baseline + b"agent outside-drift /bin/true\n"
    tests.joinpath("suites.conf").write_bytes(drifted)
    with pytest.raises(api.Refused, match="suite registry drift"):
        _replace_full_farm_row(api, store, tests, baseline, valid)
    assert tests.joinpath("suites.conf").read_bytes() == drifted


def test_existing_store_replacement_rolls_back_on_post_update_refusal(tmp_path: Path) -> None:
    api = _api()
    old = b"agent full-farm env OLD_PROFILE=/stale /bin/false\n"
    _orch, tests, _full = _private_fixture(tmp_path, old)
    store, _entry, _profile = _managed_runtime(api, tmp_path / "store", tests, tmp_path)
    valid = _candidate_row()
    baseline = tests.joinpath("suites.conf").read_bytes()
    original = store.names_for_suite

    def refuse(*args):
        if args[1:3] == ("full-farm", _row_command(valid).rstrip("\n")):
            raise api.Refused("post-update source receipt unavailable")
        return original(*args)

    store.names_for_suite = refuse
    with pytest.raises(api.Refused, match="post-update source receipt unavailable"):
        _replace_full_farm_row(api, store, tests, baseline, valid)
    assert tests.joinpath("suites.conf").read_bytes() == baseline
    assert _suite_rows(baseline, "agent", "full-farm") == [old]
