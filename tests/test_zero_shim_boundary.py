"""Adversarial checks for the installed neutral runtime boundary."""

import inspect
import os
import sys
from pathlib import Path

import pytest

from astrid_runtime import cli
from astrid_runtime.bootstrap import SourceProfile
from astrid_runtime.runtime_boundary import LocalRuntimeBoundary
from runtime_protocol.backup import verify_backup


def test_cli_accepts_only_canonical_spellings():
    parse = cli.parser().parse_args
    parse(["backup", "--destination", "backup"])
    parse(["prepare-reboot", "--attempt-id", "a", "--lease-id", "l", "--fence", "1", "--runtime-epoch", "1"])
    parse(["recovery", "--expected-realm-id", "realm", "--expected-version", "1", "--non-interactive"])
    for argv in (
        ["backup", "--out", "backup"],
        ["prepare"],
        ["recover"],
        ["recovery", "--realm-id", "realm", "--expected-version", "1", "--non-interactive"],
        ["migrate", "--source", "source", "--archive", "archive", "--destination", "destination"],
        ["rehearse", "--source", "source", "--archive", "archive", "--destination", "destination"],
        ["migrate", "--source-root", "source", "--archive-root", "archive", "--destination-root", "destination"],
    ):
        with pytest.raises(SystemExit):
            parse(argv)


def test_backup_verifier_has_no_live_legacy_switch():
    assert "allow_legacy" not in inspect.signature(verify_backup).parameters


def test_http_surface_has_no_removed_route_aliases():
    source = Path(__file__).parents[1].joinpath("runtime_protocol", "server.py").read_text()
    for removed in (
        'path in (["health"]',
        'path in (["v1", "workers"]',
        'path in (["v1", "recovery", "reboot"], ["v1", "runtime", "reboot"]',
        'path in (["v1", "recovery", "resume"], ["v1", "runtime", "resume"]',
    ):
        assert removed not in source
    assert "self.runtime.claim(task_id" not in source
    assert "self.runtime.heartbeat(task_id" not in source


def test_connect_uses_installed_client_without_mutating_import_path(monkeypatch):
    class FakeClient:
        def __init__(self, endpoint, credential):
            self.endpoint = endpoint
            self.credential = credential

    monkeypatch.setitem(sys.modules, "astrid_runtime_client", type("M", (), {"WorkspaceClient": FakeClient}))
    boundary = LocalRuntimeBoundary()
    boundary.configure_source(
        SourceProfile(
            profile="astrid",
            runtime_checkout="/checkout-that-must-not-be-consulted",
            source_checkout="/source-provenance-only",
            runtime_command=(),
            runtime_environment="",
            protocol_version="workspace.v1",
            schema_version="workspace-schema-v1",
            capability_digest="digest",
        )
    )
    before = list(sys.path)
    connection = boundary.connect(endpoint="http://127.0.0.1:1", credential="token")
    assert list(sys.path) == before
    assert connection._client.endpoint == "http://127.0.0.1:1"


def test_start_does_not_inject_checkout_into_child(monkeypatch, tmp_path):
    captured = {}

    class FakeProcess:
        pid = 123
        returncode = None

        def poll(self):
            return None

    def fake_popen(argv, **kwargs):
        captured.update(argv=argv, kwargs=kwargs)
        return FakeProcess()

    class FakeBroker:
        # The custody broker is the one substituted layer: it normally waits for
        # the real wrapper child to seal itself, and the fake Popen starts none.
        # The launch arguments under test are still the ones start() builds.
        def __init__(self, **_kwargs):
            pass

        def child_environment(self, argv, *, start_new_session):
            return {"ASTRID_RUNTIME_CUSTODY_ROLE": "runtime_owner"}

        def wait_until_sealed(self):
            pass

        def bind_ready_token(self, **_kwargs):
            pass

    boundary = LocalRuntimeBoundary()
    # The fake broker and wrapper environment assertions cover the broker-backed
    # launch path; Linux otherwise correctly uses native custody and has no
    # broker-provided environment to inspect.
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr("astrid_runtime.runtime_boundary.RoleBoundCustodyBroker", FakeBroker)
    monkeypatch.setattr(
        "astrid_runtime.runtime_boundary.default_process_identity",
        lambda pid: {"pid": pid, "uid": os.getuid(), "birth_id": "birth"},
    )
    monkeypatch.setattr("astrid_runtime.runtime_boundary.publish_active_capability", lambda *_a, **_k: None)
    monkeypatch.setattr("astrid_runtime.runtime_boundary.subprocess.Popen", fake_popen)
    monkeypatch.setattr(boundary, "_wait_endpoint", lambda _support, _process: "http://127.0.0.1:1")
    monkeypatch.setattr(boundary, "_read_discovery", lambda _support: {"process_birth_id": "birth"})
    source_checkout = tmp_path / "product-source"
    source_checkout.mkdir()
    profile = SourceProfile(
        profile="astrid",
        runtime_checkout=str(tmp_path / "runtime-checkout-that-must-not-be-used"),
        source_checkout=str(source_checkout),
        runtime_command=(sys.executable, "-c", "pass"),
        runtime_environment="",
        protocol_version="workspace.v1",
        schema_version="workspace-schema-v1",
        capability_digest="digest",
    )
    owner_lock = tmp_path / "support" / "owner.lock"
    boundary.start(realm_id="realm", realm_root=tmp_path / "realm", owner_lock=owner_lock, source_profile=profile)
    kwargs = captured["kwargs"]
    assert "cwd" not in kwargs
    # The custody wrapper needs its own variables in env; nothing derived from
    # either checkout may be added, so the import path is the host's own.
    assert kwargs["env"].get("PYTHONPATH") == os.environ.get("PYTHONPATH")
    assert not any(str(source_checkout) in str(value) for value in kwargs["env"].values())
    assert not any(str(source_checkout) in part for part in captured["argv"])
    assert "PYTHONPATH" not in kwargs


def test_wait_endpoint_does_not_adopt_incumbent_discovery(monkeypatch, tmp_path):
    class Process:
        pid = 123

        def poll(self):
            return None

    boundary = LocalRuntimeBoundary()
    observations = iter(
        [
            {"pid": 99, "endpoint": "http://127.0.0.1:43123"},
            {"pid": 123, "endpoint": "http://127.0.0.1:43124"},
        ]
    )
    monkeypatch.setattr(boundary, "_read_discovery", lambda _support: next(observations))
    monkeypatch.setattr(boundary, "_http_health", lambda _endpoint: True)

    assert boundary._wait_endpoint(tmp_path, Process()) == "http://127.0.0.1:43124"
