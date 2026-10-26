from __future__ import annotations

import json
import hashlib
import os
import re
import shlex
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import route
import receive


def _qualified_config(
    tmp_path: Path,
    checkouts: tuple[Path, Path] | None = None,
) -> dict[str, object]:
    config = json.loads(route.CONFIG.read_text())
    for entry, checkout in zip(
        config["routes"],
        checkouts
        or (
            Path("/home/user/work/wt/agt-pin-4c4ee35d"),
            Path("/home/user/work/wt/agt-pin-8b6ed211"),
        ),
    ):
        commit = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
        ).strip()
        tree = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD^{tree}"], text=True
        ).strip()
        receipt = tmp_path / "queue" / "done" / f"checkout-agent-{commit}"
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(f"created {checkout} (detached at {commit}, KEEP)\n")
        (tmp_path / "workers" / checkout.name / "KEEP").parent.mkdir(
            parents=True, exist_ok=True
        )
        (tmp_path / "workers" / checkout.name / "KEEP").write_text("keep\n")
        metadata = checkout / "astrid_runtime_client" / "contract_metadata.py"
        schema_digest = re.search(
            r"SCHEMA_DIGEST\s*=\s*['\"](sha256:[0-9a-f]{64})['\"]",
            metadata.read_text(),
        ).group(1)
        lock = checkout / "runtime.lock.json"
        entry["agent"] = {
            "status": "qualified",
            "expected_commit": entry["agent"]["expected_commit"],
            "expected_tree": entry["agent"]["expected_tree"],
            "commit": commit,
            "tree": tree,
            "checkout": str(checkout),
            "receipt": str(receipt),
            "provider_origin": str(checkout / "astrid" / "sdk" / "timeline" / "api.py"),
            "client_origin": str(checkout / "astrid_runtime_client" / "generated.py"),
            "schema_digest": schema_digest,
            "lock_values": {
                "runtime.lock.json": "sha256:" + hashlib.sha256(lock.read_bytes()).hexdigest()
            },
        }
    return config


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
            "full-d141-pristine: pristine Agent request-checkout receipt",
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
    config["routes"][1]["agent"]["expected_commit"] = "8b6ed2116fd1803d24b2be5bc08bd9490407fe4a"
    config["routes"][1]["agent"]["expected_tree"] = "0a3691a49b63fd7b0c22fb3478e9cf1947f266ed"
    bad = tmp_path / "wrong.json"
    bad.write_text(json.dumps(config))
    with pytest.raises(route.RouteError, match="expected frozen tip"):
        route.load_config(bad)


def test_harmless_pytest_subprocess_writes_durable_junit(tmp_path: Path) -> None:
    config = route.load_config()
    result = route.run_stub(config, tmp_path / "output")
    assert result == 0
    assert (tmp_path / "output" / "stub.xml").is_file()
    assert "test_d141_route_stub" in (tmp_path / "output" / "stub.xml").read_text()


def test_genuine_done_receipts_bind_distinct_cut_and_pristine_rows(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path)
    rows = route.render_rows(config)
    assert len(rows) == 2
    assert all("python -m pytest -q -n3" in row for row in rows)
    assert all("disk-start" in row and "runner-exit" in row and "KEEP" in row for row in rows)
    assert route.route_status(config) == ("READY", [])


def _installed_row(config: dict[str, object], tmp_path: Path, name: str) -> str:
    destination = tmp_path / "installed"
    route.install_candidate(config, destination)
    rows = [
        line.split(None, 2)[2]
        for line in (destination / "suites.conf").read_text().splitlines()
        if line.split(None, 2)[:2] == ["runtime", name]
    ]
    assert len(rows) == 1
    return rows[0]


def _substitute_harmless_pytest(
    config: dict[str, object], row: str, stub: Path
) -> str:
    pytest_config = config["pytest"]
    assert isinstance(pytest_config, dict)
    interpreter = pytest_config["interpreter"]
    arguments = pytest_config["arguments"]
    junit_name = pytest_config["junit_name"]
    assert isinstance(interpreter, str)
    assert isinstance(arguments, list)
    assert isinstance(junit_name, str)
    normal = (
        f"{shlex.quote(interpreter)} "
        f"{' '.join(shlex.quote(argument) for argument in arguments)} "
        f'--junitxml="$D66_OUTPUT_DIR/{junit_name}"'
    )
    harmless = (
        f"{shlex.quote(interpreter)} -m pytest -q -p no:cacheprovider "
        f'--junitxml="$D66_OUTPUT_DIR/{junit_name}" {shlex.quote(str(stub))}'
    )
    assert row.count(normal) == 1
    return row.replace(normal, harmless)


def test_installed_rendered_row_initializes_private_output_and_keeps_witnesses(
    tmp_path: Path,
) -> None:
    config = _qualified_config(
        tmp_path / "bindings",
        (
            Path("/home/user/work/wt/agt-pin-28e56cac"),
            Path("/home/user/work/wt/agt-pin-8b6ed211"),
        ),
    )
    stub = tmp_path / "test_d141_output.py"
    stub.write_text("def test_d141_output_stub():\n    assert True\n")
    row = _installed_row(config, tmp_path, "full-d141-cut")
    row = _substitute_harmless_pytest(config, row, stub)
    output = tmp_path / "service" / "d66"
    output.parent.mkdir()
    assert not output.exists()

    completed = subprocess.run(
        ["bash", "-c", row],
        cwd="/home/user/work/runtime",
        env={**dict(os.environ), "D66_OUTPUT_DIR": str(output)},
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert output.is_dir() and not output.is_symlink()
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    assert (output / "disk-start").is_file()
    assert (output / "disk-stop").is_file()
    assert (output / "runner-exit").read_text() == "0\n"
    assert (output / "KEEP").read_text() == "KEEP before service cleanup\n"
    junit = ET.parse(output / "runtime-full.xml").getroot()
    assert junit.tag in {"testsuite", "testsuites"}
    assert list(junit.iter("testcase"))
    output.chmod(0o750)
    rerun = subprocess.run(
        ["bash", "-c", row],
        cwd="/home/user/work/runtime",
        env={**dict(os.environ), "D66_OUTPUT_DIR": str(output)},
        check=False,
        capture_output=True,
        text=True,
    )
    assert rerun.returncode == 0, rerun.stderr
    assert stat.S_IMODE(output.stat().st_mode) == 0o750


@pytest.mark.parametrize("poison", ["missing", "symlink"])
def test_installed_rendered_row_source_poison_does_not_launch_or_create_output(
    tmp_path: Path, poison: str
) -> None:
    config = _qualified_config(
        tmp_path / "bindings",
        (
            Path("/home/user/work/wt/agt-pin-28e56cac"),
            Path("/home/user/work/wt/agt-pin-8b6ed211"),
        ),
    )
    marker = tmp_path / "launched"
    launcher = tmp_path / "launcher.py"
    launcher.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('launched')\n"
    )
    row = _installed_row(config, tmp_path, "full-d141-cut")
    normal = (
        "/home/user/work/venv-runtime/bin/python -m pytest -q -n3 "
        '--junitxml="$D66_OUTPUT_DIR/runtime-full.xml"'
    )
    assert row.count(normal) == 1
    row = row.replace(normal, f"{shlex.quote(sys.executable)} {shlex.quote(str(launcher))}")
    actual_checkout = config["routes"][0]["agent"]["checkout"]
    assert isinstance(actual_checkout, str)
    poisoned = tmp_path / f"agent-{poison}"
    if poison == "missing":
        replacement = str(poisoned)
    else:
        poisoned.symlink_to(actual_checkout, target_is_directory=True)
        replacement = str(poisoned)
    row = row.replace(shlex.quote(actual_checkout), shlex.quote(replacement))
    output = tmp_path / "service" / "d66"

    completed = subprocess.run(
        ["bash", "-c", row],
        cwd="/home/user/work/runtime",
        env={**dict(os.environ), "D66_OUTPUT_DIR": str(output)},
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert not marker.exists()
    assert not output.exists()


def test_installed_rendered_row_output_symlink_refuses_without_outside_writes(
    tmp_path: Path,
) -> None:
    config = _qualified_config(
        tmp_path / "bindings",
        (
            Path("/home/user/work/wt/agt-pin-28e56cac"),
            Path("/home/user/work/wt/agt-pin-8b6ed211"),
        ),
    )
    stub = tmp_path / "test_d141_output.py"
    stub.write_text("def test_d141_output_stub():\n    assert True\n")
    row = _substitute_harmless_pytest(
        config, _installed_row(config, tmp_path, "full-d141-cut"), stub
    )
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "sentinel").write_text("unchanged\n")
    output = tmp_path / "service" / "d66"
    output.parent.mkdir()
    output.symlink_to(outside, target_is_directory=True)
    before = (outside / "sentinel").read_bytes()

    completed = subprocess.run(
        ["bash", "-c", row],
        cwd="/home/user/work/runtime",
        env={**dict(os.environ), "D66_OUTPUT_DIR": str(output)},
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert not (outside / "disk-start").exists()
    assert not (outside / "runtime-full.xml").exists()
    assert (outside / "sentinel").read_bytes() == before


def test_qualified_path_rejects_poisoned_receipt_and_origin(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path)
    config["routes"][1]["agent"]["receipt"] = str(tmp_path / "missing")
    with pytest.raises(route.RouteError, match="receipt"):
        route.render_rows(config)
    config = _qualified_config(tmp_path / "second")
    config["routes"][1]["agent"]["provider_origin"] = "/tmp/not-the-checkout.py"
    with pytest.raises(route.RouteError, match="provider_origin"):
        route.render_rows(config)


def test_private_installer_rejects_symlink_destination_parent_and_target(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path / "bindings")
    outside = tmp_path / "outside"
    outside.mkdir()
    destination = tmp_path / "destination-link"
    destination.symlink_to(outside, target_is_directory=True)
    with pytest.raises(route.RouteError, match="symlink"):
        route.install_candidate(config, destination)
    parent = tmp_path / "parent-link"
    parent.symlink_to(outside, target_is_directory=True)
    with pytest.raises(route.RouteError, match="symlink"):
        route.install_candidate(config, parent / "candidate")
    target = tmp_path / "target-candidate"
    target.mkdir()
    (target / "suites.conf").symlink_to(outside / "escaped")
    with pytest.raises(route.RouteError, match="unsafe"):
        route.install_candidate(config, target)
    with pytest.raises(route.RouteError, match="unsafe path"):
        route.install_candidate(config, tmp_path / "candidate" / ".." / "escape")
    safe = tmp_path / "safe-candidate"
    route.install_candidate(config, safe)
    assert (safe / "suites.conf").is_file()
    assert (safe / "full-d141-pristine.env").is_file()


@pytest.mark.parametrize("existing_destination", [True, False])
def test_private_installer_rejects_existing_symlinked_ancestor(
    tmp_path: Path, existing_destination: bool
) -> None:
    config = _qualified_config(tmp_path / "bindings")
    outside = tmp_path / "outside"
    existing_parent = outside if existing_destination else outside / "existing-parent"
    existing_parent.mkdir(parents=True)
    (outside / "sentinel").write_bytes(b"outside\x00unchanged\n")
    if existing_destination:
        (existing_parent / "candidate").mkdir()
    parent = tmp_path / "parent-link"
    parent.symlink_to(outside, target_is_directory=True)
    before = {
        path.relative_to(outside): path.read_bytes() if path.is_file() else None
        for path in outside.rglob("*")
    }

    with pytest.raises(route.RouteError, match="symlink"):
        route.install_candidate(config, parent / existing_parent.relative_to(outside) / "candidate")

    assert {
        path.relative_to(outside): path.read_bytes() if path.is_file() else None
        for path in outside.rglob("*")
    } == before


def test_private_installer_checks_existing_ancestor_mode(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path / "bindings")
    parent = tmp_path / "unsafe-parent"
    destination = parent / "existing-parent" / "candidate"
    destination.mkdir(parents=True)
    parent.chmod(0o777)
    with pytest.raises(route.RouteError, match="unsafe owner or mode"):
        route.install_candidate(config, destination)
    assert list(destination.iterdir()) == []


@pytest.mark.parametrize("target", ["suites.conf", "full-d141-cut.env", "full-d141-pristine.env"])
@pytest.mark.parametrize("symlink", [True, False])
def test_private_installer_preserves_bytes_on_child_or_cas_refusal(
    tmp_path: Path, target: str, symlink: bool
) -> None:
    config = _qualified_config(tmp_path / "bindings")
    destination = tmp_path / "candidate"
    destination.mkdir()
    sentinel = tmp_path / "outside-sentinel"
    sentinel.write_bytes(b"outside\x00unchanged\n")
    (destination / "keep").write_bytes(b"private unchanged\n")
    child = destination / target
    if symlink:
        child.symlink_to(sentinel)
    else:
        child.write_bytes(b"different existing bytes\n")
    before = {path.name: path.read_bytes() for path in destination.iterdir()}

    with pytest.raises(route.RouteError, match="unsafe" if symlink else "private CAS"):
        route.install_candidate(config, destination)

    assert {path.name: path.read_bytes() for path in destination.iterdir()} == before
    assert child.is_symlink() == symlink
    assert sentinel.read_bytes() == b"outside\x00unchanged\n"


def test_private_installer_normal_nested_path_is_idempotent(tmp_path: Path) -> None:
    config = _qualified_config(tmp_path / "bindings")
    destination = tmp_path / "private" / "candidate"
    route.install_candidate(config, destination)
    assert (destination / "suites.conf").read_text() == "\n".join(route.render_rows(config)) + "\n"
    for entry in config["routes"]:
        env = (destination / f"{entry['name']}.env").read_text()
        assert f"D141_RUNTIME_COMMIT={entry['runtime']['commit']}\n" in env
        assert f"D141_AGENT_COMMIT={entry['agent']['commit']}\n" in env
    (destination / "keep").write_bytes(b"private unchanged\n")
    before = {
        path.name: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in destination.iterdir()
    }
    route.install_candidate(config, destination)
    assert {
        path.name: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in destination.iterdir()
    } == before


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
    (output / "request").write_text(
        "target=integration:runtime\nrepo=runtime\nsuite=full-d141-pristine\n"
    )
    runtime = Path("/home/user/work/runtime")
    runtime_tree = subprocess.check_output(
        ["git", "-C", str(runtime), "rev-parse", "HEAD^{tree}"], text=True
    ).strip()
    (output / "snap").write_text(f"tree={runtime_tree}\nworktree={runtime}\n")
    agent = "/home/user/work/wt/agt-pin-8b6ed211"
    (output / "summary").write_text(
        "cmd: env ASTRID_CHECKOUT="
        + agent
        + ' df -B1 --output=avail /home/user > "$D66_OUTPUT_DIR/disk-start"; '
        + "/home/user/work/venv-runtime/bin/python -m pytest -q -n3 "
        + '--junitxml="$D66_OUTPUT_DIR/runtime-full.xml"; rc=$?; '
        + 'df -B1 --output=avail /home/user > "$D66_OUTPUT_DIR/disk-stop"; '
        + 'printf "$rc" > "$D66_OUTPUT_DIR/runner-exit"; '
        + 'printf KEEP > "$D66_OUTPUT_DIR/KEEP"\n'
    )
    d66 = output / "d66"
    d66.mkdir()
    (d66 / "runtime-full.xml").write_text(
        '<?xml version="1.0"?><testsuite name="pytest" tests="1">'
        '<testcase classname="test_route" name="test_one"/></testsuite>\n'
    )
    (d66 / "disk-start").write_text("Filesystem\n9000000000\n")
    (d66 / "disk-stop").write_text("Filesystem\n8999999999\n")
    (d66 / "runner-exit").write_text("0\n")
    (d66 / "KEEP").write_text("retain until independent comparison\n")
    receipt = tmp_path / "receipt.json"
    receive.receive(output, receipt)
    assert json.loads(receipt.read_text())["runner_exit"] == 0
    assert json.loads(receipt.read_text())["testcases"] == [
        {"id": "test_route::test_one", "outcome": "passed"}
    ]
