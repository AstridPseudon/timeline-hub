from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PACKET = Path(__file__).parent
ORCH = Path(os.environ.get(
    "FARM_ORCH_ROOT",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
))
BENCH_SOURCE = ORCH / "bin" / "bench_store.py"
SOURCE = json.loads((PACKET / "runtime-source-selection.json").read_bytes())


def _api():
    spec = importlib.util.spec_from_file_location("farm_v2_bench_store", BENCH_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _snapshot(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def _private_fixture(tmp_path: Path):
    orch = tmp_path / "orch"
    tests = orch / "tests"
    tests.mkdir(parents=True)
    full = b"agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n"
    (tests / "suites.conf").write_bytes(full + b"agent outside /bin/true\n")
    return orch, tests, full


def _managed_runtime(api, root: Path, tests: Path, tmp_path: Path):
    # The production reserve is a host-capacity gate, not part of this small
    # private projection fixture. Keep Store.ensure itself unchanged while
    # allowing the fixture to run on the constrained worker volume.
    api.Store.RESERVE_BYTES = 0
    store = api.Store.initialize(root, tests)
    identity = {"remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db"}
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
        "PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/bin:/bin\n"
        f"ASTRID_REMOTION_PROJECT_DIR={tmp_path / 'managed-profile'}\n"
        "ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node\n"
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages\n"
    )
    suite = "agent managed-runtime /home/user/work/venv-agent/bin/python -m pytest -q\n"
    entry = store.ensure(
        "runtime",
        identity,
        {"name": "managed-runtime", "env": env, "suite": suite},
        build,
        verify,
    )
    return store, entry


def test_packet_source_and_candidate_row_are_explicit() -> None:
    assert hashlib.sha256(BENCH_SOURCE.read_bytes()).hexdigest() == (
        "6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8"
    )
    assert SOURCE["declared_runtime_source_commit"] == "45c3a7f476e1c5f74fafc15956a58b9871eee21f"
    assert SOURCE["required_runtime_source_commit"] == "1d9ddba546f8fb1300f55ff62607ed492719cbaa"
    assert SOURCE["status"].startswith("source checkout")
    row = (PACKET / "registration-row.txt").read_text(encoding="utf-8")
    assert row.endswith("\n") and row.count("\n") == 1
    assert "rt-pin-1d9ddba5" in row
    assert "rt-pin-45c3a7f4" not in row
    assert "ASTRID_RUNTIME_CHECKOUT=" in row and 'PYTHONPATH="$PWD:' in row


def test_production_store_projection_and_subprocess_env(tmp_path: Path) -> None:
    api = _api()
    _orch, tests, full = _private_fixture(tmp_path)
    root = tmp_path / "bench-store"
    store, _entry = _managed_runtime(api, root, tests, tmp_path)
    candidate = (PACKET / "registration-row.txt").read_bytes()
    baseline = tests.joinpath("suites.conf").read_bytes()
    assert baseline.endswith(b"\n") and baseline.count(full) == 1
    assert b"agent full-farm " not in baseline

    with store.mutex():
        assert tests.joinpath("suites.conf").read_bytes() == baseline
        api.atomic(tests / "suites.conf", (baseline + candidate).decode())
    assert tests.joinpath("suites.conf").read_bytes() == baseline + candidate
    names = store.names_for_suite(
        "agent", "full-farm", candidate.decode().split(None, 2)[2].rstrip("\n")
    )
    assert names == ["managed-runtime"]

    runtime = tmp_path / "runtime-source"
    (runtime / "runtime_protocol").mkdir(parents=True)
    (runtime / "runtime_protocol" / "__init__.py").write_text("\n", encoding="utf-8")
    (runtime / "runtime_protocol" / "external_pack_sources.py").write_text(
        "ORIGIN = 'external_pack_sources'\n", encoding="utf-8"
    )
    schema = tmp_path / "schema-site"
    (schema / "timeline_schema").mkdir(parents=True)
    (schema / "timeline_schema" / "__init__.py").write_text(
        "ORIGIN = 'schema'\n", encoding="utf-8"
    )
    profile = tmp_path / "remotion-profile"
    profile.mkdir()
    node_bin = tmp_path / "node20" / "bin"
    node_bin.mkdir(parents=True)
    node = node_bin / "node"
    node.write_text("#!/bin/sh\nprintf 'v20.19.4\\n'\n", encoding="utf-8")
    node.chmod(0o755)
    child = (
        "import json, os, pathlib, subprocess, runtime_protocol.external_pack_sources as p, "
        "timeline_schema; print(json.dumps({'path': str(pathlib.Path(p.__file__).resolve()), "
        "'schema': str(pathlib.Path(timeline_schema.__file__).resolve()), 'env': "
        "{k: os.environ[k] for k in ('PATH', 'ASTRID_REMOTION_PROJECT_DIR', "
        "'ASTRID_NODE_EXECUTABLE', 'ASTRID_TIMELINE_SCHEMA_PYTHONPATH', "
        "'ASTRID_RUNTIME_CHECKOUT')}, 'node': subprocess.check_output(["
        "os.environ['ASTRID_NODE_EXECUTABLE'], '--version'], text=True).strip()}, "
        "sort_keys=True))"
    )
    env = dict(os.environ)
    env.update(
        PATH=f"{node_bin}:/usr/bin:/bin",
        ASTRID_REMOTION_PROJECT_DIR=str(profile),
        ASTRID_NODE_EXECUTABLE=str(node),
        ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(schema),
        ASTRID_RUNTIME_CHECKOUT=str(runtime),
        PYTHONPATH=f"{runtime}:{schema}",
    )
    with store.acquire(names):
        result = subprocess.run([sys.executable, "-c", child], cwd=tmp_path, env=env,
                                text=True, capture_output=True, check=True)
    observed = json.loads(result.stdout)
    assert observed["env"]["ASTRID_NODE_EXECUTABLE"] == str(node)
    assert observed["env"]["ASTRID_RUNTIME_CHECKOUT"] == str(runtime)
    assert observed["env"]["ASTRID_REMOTION_PROJECT_DIR"] == str(profile)
    assert observed["env"]["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"] == str(schema)
    assert observed["path"].startswith(str(runtime))
    assert observed["schema"].startswith(str(schema))
    assert observed["node"] == "v20.19.4"
    assert tests.joinpath("suites.conf").read_bytes().startswith(baseline)
    assert tests.joinpath("suites.conf").read_bytes()[len(baseline):] == candidate


def test_projection_refuses_wrong_source_without_store_mutation(tmp_path: Path) -> None:
    api = _api()
    _orch, tests, _full = _private_fixture(tmp_path)
    store, _entry = _managed_runtime(api, tmp_path / "store", tests, tmp_path)
    valid = (PACKET / "registration-row.txt").read_bytes()
    bad = valid.replace(b"rt-pin-1d9ddba5", b"rt-pin-45c3a7f4")
    tests.joinpath("suites.conf").write_bytes(tests.joinpath("suites.conf").read_bytes() + bad)
    before_index = _snapshot(store.root / "index.json")
    with pytest.raises(api.Refused, match="suite absent, ambiguous or changed"):
        store.names_for_suite(
            "agent", "full-farm", valid.decode().split(None, 2)[2].rstrip("\n")
        )
    assert _snapshot(store.root / "index.json") == before_index
