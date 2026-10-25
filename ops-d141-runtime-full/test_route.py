from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import route
import receive


def test_config_has_two_unique_routes_and_frozen_runtime_identities() -> None:
    config = route.load_config()
    assert [entry["name"] for entry in config["routes"]] == [
        "full-d141-cut",
        "full-d141-pristine",
    ]
    assert config["routes"][0]["runtime"] == {
        "commit": "6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d",
        "tree": "ac5b862744bece65b2e30565db1777bacd60da28",
    }
    assert config["routes"][1]["runtime"] == {
        "commit": "fa9cd5464a8b37b02f971de375e56be846cd69e2",
        "tree": "124e10dbcd54fb90219e783ec11aa34f8c91590c",
    }


def test_pending_tuple_is_not_ready_and_cannot_render_or_install(tmp_path: Path) -> None:
    config = route.load_config()
    assert route.route_status(config) == (
        "NOT_READY",
        [
            "full-d141-cut: Agent cut checkout receipt",
            "full-d141-pristine: Agent cut checkout receipt",
        ],
    )
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.render_rows(config)
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.install_candidate(config, tmp_path / "candidate")
    assert list(tmp_path.rglob("*")) == []


def test_missing_and_duplicate_manifest_keys_fail_closed(tmp_path: Path) -> None:
    source = json.loads(route.CONFIG.read_text())
    source["required"] = source["required"][:-1]
    bad = tmp_path / "missing.json"
    bad.write_text(json.dumps(source))
    with pytest.raises(route.RouteError, match="required input manifest"):
        route.load_config(bad)

    source = json.loads(route.CONFIG.read_text())
    source["routes"][1]["name"] = source["routes"][0]["name"]
    bad = tmp_path / "duplicate.json"
    bad.write_text(json.dumps(source))
    with pytest.raises(route.RouteError, match="route names or order"):
        route.load_config(bad)


def test_wrong_source_tree_and_origin_fail_before_any_artifact(tmp_path: Path) -> None:
    config = json.loads(route.CONFIG.read_text())
    config["routes"][0]["agent"] = {
        "status": "qualified",
        "commit": "0" * 40,
        "tree": "1" * 40,
        "checkout": "/tmp/d141-agent",
        "receipt": "/tmp/d141-receipt.json",
        "provider_origin": "/tmp/d141-agent/provider.py",
        "client_origin": "/tmp/d141-agent/client.py",
        "schema_digest": "sha256:" + "a" * 64,
        "lock_values": {"runtime": "pending-check-control"},
    }
    config["routes"][1]["agent"] = dict(config["routes"][0]["agent"])
    bad = tmp_path / "wrong.json"
    bad.write_text(json.dumps(config))
    loaded = route.load_config(bad)
    assert route.route_status(loaded)[0] == "READY"
    destination = tmp_path / "candidate"
    with pytest.raises((route.RouteError, FileNotFoundError)):
        route.install_candidate(loaded, destination)
    assert not destination.exists()


def test_harmless_pytest_subprocess_writes_durable_junit(tmp_path: Path) -> None:
    config = route.load_config()
    result = route.run_stub(config, tmp_path / "output")
    assert result == 0
    assert (tmp_path / "output" / "stub.xml").is_file()
    assert "test_d141_route_stub" in (tmp_path / "output" / "stub.xml").read_text()


def test_status_cli_is_json_and_does_not_launch() -> None:
    completed = subprocess.run(
        [sys.executable, str(route.ROOT / "route.py"), "status"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert json.loads(completed.stdout)["status"] == "NOT_READY"
    assert completed.stderr == ""


def test_receiver_requires_and_records_durable_service_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "service"
    output.mkdir()
    (output / "exit").write_text("0\n")
    (output / "log.txt").write_text("pytest output\n")
    (output / "runtime-full.xml").write_text('<?xml version="1.0"?><testsuite tests="1"/>\n')
    (output / "KEEP").write_text("retain until independent comparison\n")
    receipt = tmp_path / "receipt.json"
    receive.receive(output, receipt)
    assert json.loads(receipt.read_text())["runner_exit"] == 0
