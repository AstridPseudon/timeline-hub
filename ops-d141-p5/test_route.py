from __future__ import annotations

import json
from pathlib import Path

import pytest

import receive
import route


def test_frozen_runtime_and_exact_two_file_selector() -> None:
    config = route.load_config()
    assert config["route"]["runtime"] == {
        "commit": "6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d",
        "tree": "ac5b862744bece65b2e30565db1777bacd60da28",
        "checkout": "/home/user/work/runtime",
        "origin": "https://github.com/banodoco/banodoco-workspace-runtime",
    }
    assert config["pytest"]["arguments"][-2:] == [
        "tests/test_timeline_commit_integration.py",
        "tests/test_timeline_commit_crash.py",
    ]


def test_pending_agent_refuses_rows_and_install_without_artifacts(tmp_path: Path) -> None:
    config = route.load_config()
    assert route.route_status(config) == (
        "NOT_READY", ["genuine final Agent cut receipt is pending"]
    )
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.render_rows(config)
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.install_candidate(config, tmp_path / "cas")
    assert not (tmp_path / "cas").exists()


def test_wrong_source_tree_origin_lock_and_duplicate_manifest_fail_before_artifacts(tmp_path: Path) -> None:
    source = json.loads(route.CONFIG.read_text())
    source["route"]["runtime"]["tree"] = "1" * 40
    with pytest.raises(route.RouteError, match="frozen Runtime identity"):
        route._validate_config(source)
    source = json.loads(route.CONFIG.read_text())
    source["route"]["runtime"]["origin"] = "/wrong/origin"
    with pytest.raises(route.RouteError, match="Runtime origin"):
        route._validate_config(source)
    source = json.loads(route.CONFIG.read_text())
    source["route"]["agent"] = {
        "status": "qualified", "commit": "0" * 40, "tree": "1" * 40,
        "checkout": "/tmp/agent", "receipt": "/tmp/receipt",
        "provider_origin": "/tmp/provider", "client_origin": "/tmp/client",
        "schema_digest": "sha256:" + "a" * 64, "lock_values": {},
    }
    with pytest.raises(route.RouteError, match="lock values"):
        route._validate_config(source)
    source = json.loads(route.CONFIG.read_text())
    source["route"]["agent"] = {
        "status": "qualified", "commit": "0" * 40, "tree": "1" * 40,
        "checkout": "/tmp/agent", "receipt": "/tmp/receipt",
        "provider_origin": "/tmp/provider", "client_origin": "/tmp/client",
        "schema_digest": "sha256:" + "a" * 64, "lock_values": {"runtime": "actual"},
    }
    source["required"] = source["required"] + ["duplicate"]
    with pytest.raises(route.RouteError, match="required input manifest"):
        route._validate_config(source)
    assert list(tmp_path.iterdir()) == []


def test_poison_control_refuses_with_zero_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "poison"
    with pytest.raises(route.RouteError, match="poison control"):
        route.run_control(output, poison=True)
    assert not output.exists()


def test_positive_named_control_runs_once_and_keeps_durable_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "positive"
    assert route.run_control(output) == 0
    assert (output / "exit").read_text() == "0\n"
    assert json.loads((output / "argv.json").read_text())[1] == "-c"
    assert (output / "KEEP").is_file()
    assert (output / "d141-p5-cut.xml").read_text().count("testsuite") == 1


def test_receiver_requires_all_durable_artifacts_and_records_paths(tmp_path: Path) -> None:
    output = tmp_path / "service"
    route.run_control(output)
    receipt = tmp_path / "receipt.json"
    receive.receive(output, receipt)
    data = json.loads(receipt.read_text())
    assert data["route"] == "d141-p5-cut"
    assert data["runner_exit"] == 0
    assert data["keep"].endswith("/KEEP")


def test_receiver_rejects_duplicate_receipt_without_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "service"
    route.run_control(output)
    receipt = tmp_path / "receipt.json"
    receipt.write_text("existing\n")
    with pytest.raises(ValueError, match="already exists"):
        receive.receive(output, receipt)
    assert receipt.read_text() == "existing\n"
