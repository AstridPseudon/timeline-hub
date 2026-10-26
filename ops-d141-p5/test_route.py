from __future__ import annotations

import json
import stat
import subprocess
from pathlib import Path

import pytest

import receive
import route


AGENT_CHECKOUT = Path("/home/user/work/wt/agt-pin-4c4ee35d")


def _qualified_config(tmp_path: Path) -> dict[str, object]:
    config = json.loads(route.CONFIG.read_text())
    commit = subprocess.check_output(["git", "-C", str(AGENT_CHECKOUT), "rev-parse", "HEAD"], text=True).strip()
    receipt = tmp_path / "queue" / "done" / f"checkout-agent-{commit}"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(f"created /home/user/work/wt/agt-pin-{commit[:8]} (detached at {commit}, KEEP)\n")
    keep = tmp_path / "workers" / f"agt-pin-{commit[:8]}" / "KEEP"
    keep.parent.mkdir(parents=True)
    keep.write_text("retain checkout\n")
    config["route"]["agent"] = {
        "status": "qualified",
        "expected_commit": commit,
        "receipt": str(receipt),
        "commit": None,
        "tree": None,
        "checkout": None,
        "provider_origin": None,
        "client_origin": None,
        "schema_digest": None,
        "lock_values": None,
    }
    return config


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
    assert route.route_status(config) == ("NOT_READY", ["genuine final Agent cut receipt is pending"])
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.render_rows(config)
    with pytest.raises(route.RouteError, match="pending tuple"):
        route.install_candidate(config, tmp_path / "cas")
    assert not (tmp_path / "cas").exists()


def test_genuine_done_receipt_derives_origins_schema_and_lock(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path)
    rows = route.render_rows(config)
    assert len(rows) == 1
    row = rows[0]
    assert row.startswith("runtime d141-p5-cut ")
    assert "$D66_OUTPUT_DIR/d141-p5-cut.xml" in row
    assert "-u NODE_OPTIONS -u NODE_PATH" in row
    assert "tests/test_timeline_commit_integration.py" in row
    assert "tests/test_timeline_commit_crash.py" in row
    with pytest.raises(route.RouteError, match="derived"):
        bad = json.loads(json.dumps(config))
        bad["route"]["agent"]["provider_origin"] = "/tmp/fabricated"
        route._validate_config(bad)


def test_bad_receipt_or_bound_checkout_fails_before_install_artifacts(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path)
    config["route"]["agent"]["expected_commit"] = "0" * 40
    with pytest.raises(route.RouteError, match="expected Agent tip"):
        route.render_rows(config)
    assert not list(tmp_path.glob("candidate*"))


def test_private_installer_is_atomic_and_rejects_symlink_traversal_and_modes(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path / "binding")
    outside = tmp_path / "outside"
    outside.mkdir()
    destination = tmp_path / "destination-link"
    destination.symlink_to(outside, target_is_directory=True)
    with pytest.raises(route.RouteError, match="symlink"):
        route.install_candidate(config, destination)
    with pytest.raises(route.RouteError, match="unsafe path"):
        route.install_candidate(config, tmp_path / "candidate" / ".." / "escape")
    safe = tmp_path / "safe-candidate"
    route.install_candidate(config, safe)
    assert {path.name for path in safe.iterdir()} == {"suites.conf", "d141-p5-cut.env"}
    assert stat.S_IMODE(safe.stat().st_mode) == 0o700
    assert stat.S_IMODE((safe / "suites.conf").stat().st_mode) == 0o600
    route.install_candidate(config, safe)
    (safe / "suites.conf").chmod(0o644)
    with pytest.raises(route.RouteError, match="unsafe mode"):
        route.install_candidate(config, safe)


def test_poison_control_refuses_with_zero_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "poison"
    with pytest.raises(route.RouteError, match="poison control"):
        route.run_control(output, poison=True)
    assert not output.exists()


def test_normal_control_and_receiver_validate_durable_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "service"
    assert route.run_control(output) == 0
    receipt = tmp_path / "receipt.json"
    receive.receive(output, receipt)
    data = json.loads(receipt.read_text())
    assert data["suite"] == ["d141-p5-cut"]
    assert data["runner_exit"] == 0
    assert data["testcases"][0]["id"] == "control::D141_P5_CONTROL_ONCE"


def test_receiver_rejects_malformed_artifact_and_duplicate_receipt(tmp_path: Path) -> None:
    output = tmp_path / "service"
    route.run_control(output)
    (output / "d66" / "d141-p5-cut.xml").write_text("<?xml version=\"1.0\"?>\n")
    receipt = tmp_path / "receipt.json"
    with pytest.raises(ValueError, match="malformed"):
        receive.receive(output, receipt)
    route.run_control(tmp_path / "service-two")
    receipt.write_text("existing\n")
    with pytest.raises(ValueError, match="already exists"):
        receive.receive(tmp_path / "service-two", receipt)
    assert receipt.read_text() == "existing\n"


def test_receiver_rejects_symlinked_terminal_artifact(tmp_path: Path) -> None:
    output = tmp_path / "service"
    route.run_control(output)
    outside = tmp_path / "outside-keep"
    outside.write_text("retain\n")
    keep = output / "d66" / "KEEP"
    keep.unlink()
    keep.symlink_to(outside)
    with pytest.raises(ValueError, match="regular file"):
        receive.receive(output, tmp_path / "receipt.json")


def test_status_cli_is_json_and_does_not_launch() -> None:
    completed = subprocess.run(
        [route.sys.executable, str(route.ROOT / "route.py"), "status"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert json.loads(completed.stdout)["status"] == "NOT_READY"
    assert completed.stderr == ""
