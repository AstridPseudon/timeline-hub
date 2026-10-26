from __future__ import annotations

import json
import os
import shutil
import xml.etree.ElementTree as ET
import stat
import subprocess
import sys
from pathlib import Path

import pytest

import receive
import route


AGENT_COMMIT = "28e56cacb42d3da85b02e5b3543895b44f3d0f70"
AGENT_RECEIPT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/queue/done/checkout-agent-" + AGENT_COMMIT
)


def _qualified_config(tmp_path: Path) -> dict[str, object]:
    config = json.loads(route.CONFIG.read_text())
    config["route"]["agent"] = {
        "status": "qualified",
        "expected_commit": AGENT_COMMIT,
        "receipt": str(AGENT_RECEIPT),
    }
    return route._validate_config(config)


def _inventory(root: Path) -> dict[str, object]:
    result = {}
    for path in [root, *root.rglob("*")]:
        info = path.lstat()
        content = os.readlink(path) if path.is_symlink() else path.read_bytes() if path.is_file() else None
        result[str(path.relative_to(root))] = (info.st_mode, info.st_mtime_ns, content)
    return result


def _copy_output(base: Path, destination: Path) -> Path:
    shutil.copytree(base, destination)
    argv_path = destination / "d66/argv.json"
    argv = json.loads(argv_path.read_text())
    argv[-1] = f"--junitxml={destination}/d66/d141-p5-cut.xml"
    argv_path.write_text(json.dumps(argv))
    return destination


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
    candidate_config = tmp_path / "qualified-config.json"
    candidate_config.write_text(json.dumps(config))
    completed = subprocess.run(
        [sys.executable, str(route.ROOT / "route.py"), "--config", str(candidate_config), "render"],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == row + "\n"
    assert subprocess.run(["bash", "-n"], input=row.split(" ", 2)[2], text=True, capture_output=True).returncode == 0
    candidate = tmp_path / "cli-candidate"
    completed = subprocess.run(
        [sys.executable, str(route.ROOT / "route.py"), "--config", str(candidate_config), "install", str(candidate)],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert (candidate / "suites.conf").read_text() == completed.stdout + row + "\n"
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


def test_private_installer_is_atomic_and_rejects_symlink_traversal_and_modes(tmp_path: Path, monkeypatch) -> None:
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
    before = _inventory(tmp_path)
    route.install_candidate(config, safe)
    assert _inventory(tmp_path) == before
    safe.chmod(0o755)
    before = _inventory(tmp_path)
    with pytest.raises(route.RouteError, match="unsafe mode"):
        route.install_candidate(config, safe)
    assert _inventory(tmp_path) == before
    safe.chmod(0o700)
    (safe / "suites.conf").chmod(0o644)
    before = _inventory(tmp_path)
    with pytest.raises(route.RouteError, match="unsafe mode"):
        route.install_candidate(config, safe)
    assert _inventory(tmp_path) == before
    (safe / "suites.conf").chmod(0o600)
    for index, name in enumerate(("suites.conf", "d141-p5-cut.env")):
        candidate = tmp_path / f"conflict-{index}"
        route.install_candidate(config, candidate)
        (candidate / name).write_text("outside bytes must survive\n")
        before = _inventory(tmp_path)
        with pytest.raises(route.RouteError, match="different rows"):
            route.install_candidate(config, candidate)
        assert _inventory(tmp_path) == before
        linked = tmp_path / f"linked-{index}"
        route.install_candidate(config, linked)
        target = linked / name
        target.rename(tmp_path / f"outside-target-{index}")
        target.symlink_to(tmp_path / f"outside-target-{index}")
        before = _inventory(tmp_path)
        with pytest.raises(route.RouteError, match="unsafe"):
            route.install_candidate(config, linked)
        assert _inventory(tmp_path) == before
    nested = outside / "nested"
    nested.mkdir()
    route.install_candidate(config, outside / "existing")
    for target in (destination / "candidate", destination / "nested/candidate", destination / "existing"):
        before = _inventory(tmp_path)
        with pytest.raises(route.RouteError, match="parent"):
            route.install_candidate(config, target)
        assert _inventory(tmp_path) == before
    unsafe_parent = tmp_path / "unsafe-parent"
    unsafe_parent.mkdir(mode=0o777)
    unsafe_parent.chmod(0o777)
    before = _inventory(tmp_path)
    with pytest.raises(route.RouteError, match="unsafe owner or mode"):
        route.install_candidate(config, unsafe_parent / "candidate")
    assert _inventory(tmp_path) == before
    unsafe_parent.chmod(0o755)
    route.install_candidate(config, unsafe_parent / "safe-under-0755")
    assert stat.S_IMODE((unsafe_parent / "safe-under-0755").stat().st_mode) == 0o700
    before = _inventory(tmp_path)
    with monkeypatch.context() as patch:
        patch.setattr(route.os, "getuid", lambda: -1)
        with pytest.raises(route.RouteError, match="unsafe owner or mode"):
            route.install_candidate(config, tmp_path / "owner-mismatch")
    assert _inventory(tmp_path) == before
    def refuse_publish(source, destination):
        raise OSError("injected atomic publish refusal")
    outside_before = _inventory(outside)
    with monkeypatch.context() as patch:
        patch.setattr(route.os, "replace", refuse_publish)
        with pytest.raises(OSError, match="atomic publish refusal"):
            route.install_candidate(config, tmp_path / "rollback")
    assert not (tmp_path / "rollback").exists()
    assert _inventory(outside) == outside_before


def test_poison_control_refuses_with_zero_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "poison"
    with pytest.raises(route.RouteError, match="poison control"):
        route.run_control(output, poison=True)
    assert not output.exists()


def test_normal_control_and_receiver_validate_durable_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "service"
    assert route.run_control(output, config=_qualified_config(tmp_path)) == 0
    receipt = tmp_path / "receipt.json"
    receive.receive(output, receipt)
    data = json.loads(receipt.read_text())
    assert data["suite"] == ["pytest"]
    assert data["runner_exit"] == 0
    assert data["testcases"][0]["id"] == "test_control::test_D141_P5_CONTROL_ONCE"
    assert data["provenance"]["source"]["agent"]["commit"] == AGENT_COMMIT
    assert data["provenance"]["argv"][-1] == f"--junitxml={output}/d66/d141-p5-cut.xml"
    cli_receipt = tmp_path / "nested/cli-receipt.json"
    completed = subprocess.run(
        [sys.executable, str(route.ROOT / "receive.py"), str(output), str(cli_receipt)],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(cli_receipt.read_text()) == data


def test_receiver_rejects_malformed_artifact_and_duplicate_receipt(tmp_path: Path) -> None:
    base = tmp_path / "service"
    route.run_control(base, config=_qualified_config(tmp_path))
    xml = (base / "d66/d141-p5-cut.xml").read_text()
    argv = json.loads((base / "d66/argv.json").read_text())
    origins = json.loads((base / "d66/module-origin.json").read_text())
    hashes = json.loads((base / "d66/source-hashes.json").read_text())
    malformed = [
        ("d66/d141-p5-cut.xml", '<?xml version="1.0"?>'),
        ("d66/d141-p5-cut.xml", xml.replace('name="pytest"', 'name="wrong-suite"')),
        ("d66/d141-p5-cut.xml", xml.replace('name="pytest"', 'name="d141-p5-cut"')),
        ("d66/d141-p5-cut.xml", '<testsuites><testsuite name="pytest" tests="0" failures="0" errors="0" skipped="0"/></testsuites>'),
        ("d66/d141-p5-cut.xml", xml.replace('tests="1"', 'tests="2"')),
        ("d66/d141-p5-cut.xml", xml.replace('failures="0"', 'failures="1"')),
        ("d66/d141-p5-cut.xml", xml.replace('classname="test_control"', 'classname=""')),
        ("d66/d141-p5-cut.xml", xml.replace('name="test_D141_P5_CONTROL_ONCE"', 'name=""')),
        ("d66/d141-p5-cut.xml", xml.replace("</testsuite>", "<invented/></testsuite>")),
        ("d66/d141-p5-cut.xml", xml.replace(" />", "><invented/></testcase>")),
        ("request", ""),
        ("request", "repo=runtime\nsuite=wrong\n"),
        ("request", "repo=runtime\nsuite=d141-p5-cut\nsuite=d141-p5-cut\n"),
        ("snap", ""),
        ("snap", (base / "snap").read_text().replace(route.EXPECTED_RUNTIME["tree"], "0" * 40)),
        ("snap", (base / "snap").read_text().replace("worktree=/home/user/work/runtime", "worktree=/home/user/work/wt/agt-pin-28e56cac")),
        ("summary", ""),
        ("summary", "cmd: true\n"),
        ("summary", (base / "summary").read_text() * 2),
        ("summary", (base / "summary").read_text().replace(" -q -n3 ", " -q -n3 -k lost ")),
        ("log.txt", ""),
        ("exit", ""),
        ("exit", "256\n"),
        ("exit", "00\n"),
        ("exit", "1\n"),
        ("d66/runner-exit", "oops\n"),
        ("d66/argv.json", "{"),
        ("d66/argv.json", "[]"),
        ("d66/argv.json", json.dumps(argv[:-2])),
        ("d66/argv.json", json.dumps([*argv, "-k", "lost"])),
        ("d66/module-origin.json", "{}"),
        ("d66/module-origin.json", json.dumps({**origins, "agent_provider": "/tmp/invented"})),
        ("d66/module-origin.json", '{"runtime_protocol":"a","runtime_protocol":"b"}'),
        ("d66/source-hashes.json", "{}"),
        ("d66/source-hashes.json", json.dumps({key: "0" * 64 for key in hashes})),
        ("d66/disk-start", ""),
        ("d66/disk-stop", "Filesystem\n9000000000\n"),
        ("d66/disk-stop", "Avail\nnot-bytes\n"),
        ("d66/KEEP", "\n"),
        ("d66/KEEP", "invented\n"),
    ]
    for index, (name, text) in enumerate(malformed):
        output = _copy_output(base, tmp_path / f"malformed-{index}")
        (output / name).write_text(text)
        receipt = tmp_path / f"absent-{index}/receipt.json"
        before = _inventory(tmp_path)
        with pytest.raises(ValueError):
            receive.receive(output, receipt)
        assert _inventory(tmp_path) == before, (index, name)
    for attack in ("duplicate-id", "contradictory", "exit-outcome", "failed-outcome"):
        output = _copy_output(base, tmp_path / attack)
        junit = output / "d66/d141-p5-cut.xml"
        root = ET.fromstring(junit.read_text())
        suite = root.find("testsuite")
        case = suite.find("testcase")
        if attack == "duplicate-id":
            suite.append(ET.fromstring(ET.tostring(case)))
            suite.set("tests", "2")
        elif attack == "contradictory":
            ET.SubElement(case, "failure")
            ET.SubElement(case, "skipped")
        elif attack == "exit-outcome":
            (output / "exit").write_text("1\n")
            (output / "d66/runner-exit").write_text("1\n")
        else:
            ET.SubElement(case, "failure")
            suite.set("failures", "1")
        junit.write_text(ET.tostring(root, encoding="unicode"))
        before = _inventory(tmp_path)
        with pytest.raises(ValueError):
            receive.receive(output, tmp_path / f"{attack}-receipt.json")
        assert _inventory(tmp_path) == before
    # A genuine failed result is retained as a failed result, never made green.
    failed = _copy_output(base, tmp_path / "failed-result")
    junit = failed / "d66/d141-p5-cut.xml"
    root = ET.fromstring(junit.read_text())
    suite = root.find("testsuite")
    ET.SubElement(suite.find("testcase"), "failure")
    suite.set("failures", "1")
    junit.write_text(ET.tostring(root, encoding="unicode"))
    (failed / "exit").write_text("1\n")
    (failed / "d66/runner-exit").write_text("1\n")
    failed_receipt = tmp_path / "failed-receipt.json"
    receive.receive(failed, failed_receipt)
    assert json.loads(failed_receipt.read_text())["runner_exit"] == 1
    for index, text in enumerate(("existing\n", "")):
        receipt = tmp_path / f"receipt-{index}.json"
        receipt.write_text(text)
        before = _inventory(tmp_path)
        with pytest.raises(ValueError, match="already exists"):
            receive.receive(base, receipt)
        assert _inventory(tmp_path) == before


def test_receiver_rejects_symlinked_terminal_artifact(tmp_path: Path) -> None:
    base = tmp_path / "service"
    route.run_control(base, config=_qualified_config(tmp_path))
    for index, name in enumerate([*receive.REQUIRED_SERVICE, *(f"d66/{name}" for name in receive.REQUIRED_D66)]):
        output = _copy_output(base, tmp_path / f"symlink-{index}")
        artifact = output / name
        outside = tmp_path / f"outside-{index}"
        artifact.rename(outside)
        artifact.symlink_to(outside)
        before = _inventory(tmp_path)
        with pytest.raises(ValueError, match="regular file"):
            receive.receive(output, tmp_path / f"receipt-{index}.json")
        assert _inventory(tmp_path) == before, name
    outside = tmp_path / "outside-parent"
    outside.mkdir()
    link = tmp_path / "parent-link"
    link.symlink_to(outside, target_is_directory=True)
    for receipt in (link / "receipt.json", link / "missing/deeper/receipt.json", link / "existing/receipt.json"):
        (outside / "existing").mkdir(exist_ok=True)
        before = _inventory(tmp_path)
        with pytest.raises(ValueError, match="unsafe parent"):
            receive.receive(base, receipt)
        assert _inventory(tmp_path) == before
    terminal = tmp_path / "receipt-link"
    terminal.symlink_to(outside / "absent.json")
    before = _inventory(tmp_path)
    with pytest.raises(ValueError, match="already exists"):
        receive.receive(base, terminal)
    assert _inventory(tmp_path) == before
    for receipt in (Path("relative.json"), tmp_path / "nested/../receipt.json"):
        before = _inventory(tmp_path)
        with pytest.raises(ValueError, match="absolute path without traversal"):
            receive.receive(base, receipt)
        assert _inventory(tmp_path) == before
    # A service artifact directory or any of its ancestors cannot be a link.
    for output in (link / "service", tmp_path / "output-link"):
        if output == tmp_path / "output-link":
            output.symlink_to(base, target_is_directory=True)
        before = _inventory(tmp_path)
        with pytest.raises(ValueError):
            receive.receive(output, tmp_path / "directory-link-receipt.json")
        assert _inventory(tmp_path) == before


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
