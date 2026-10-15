"""Focused configuration checks; real OS read evidence lives in the spike receipt."""
from pathlib import Path

import pytest

from astrid.core.execution import generic_host as host


def policy(tmp_path):
    grant = tmp_path / "grant"
    attempt = tmp_path / "attempt"
    private = attempt / "private"
    grant.mkdir()
    private.mkdir(parents=True)
    bootstrap = tmp_path / "bootstrap.py"
    bootstrap.write_text("pass\n")
    return host._FilesystemSandboxPolicy((grant,), (bootstrap,), (), private), attempt


def test_required_policy_missing_refuses_launch_without_endpoint(tmp_path):
    with pytest.raises(host.HostError, match="policy is missing"):
        host._network_sandbox_argv(["fixture"], tmp_path, None, require_filesystem_confinement=True)


@pytest.mark.parametrize("platform,backend", [("linux", "/usr/bin/sandbox-exec"), ("darwin", None)])
def test_required_backend_missing_refuses_launch(tmp_path, monkeypatch, platform, backend):
    config, attempt = policy(tmp_path)
    monkeypatch.setattr(host.sys, "platform", platform)
    monkeypatch.setattr(host.shutil, "which", lambda _: backend)
    with pytest.raises(host.HostError, match="sandbox"):
        host._network_sandbox_argv(["fixture"], attempt, None, filesystem_policy=config)


def test_private_writes_cannot_escape_attempt(tmp_path):
    config, attempt = policy(tmp_path)
    escaped = host._FilesystemSandboxPolicy(config.read_roots, config.bootstrap_files, (), tmp_path)
    with pytest.raises(host.HostError, match="writes must stay inside"):
        host._filesystem_sandbox_profile(escaped, attempt)


def test_root_or_relative_bootstrap_scope_refused(tmp_path):
    config, attempt = policy(tmp_path)
    for root in (Path("/"), Path("relative")):
        invalid = host._FilesystemSandboxPolicy(config.read_roots, (), (root,), config.private_write_root)
        with pytest.raises(host.HostError, match="scope|absolute"):
            host._filesystem_sandbox_profile(invalid, attempt)


def test_file_policy_has_no_implicit_broker_or_ambient_directory_grant(tmp_path, monkeypatch):
    config, attempt = policy(tmp_path)
    monkeypatch.setattr(host.sys, "platform", "darwin")
    monkeypatch.setattr(host.shutil, "which", lambda _: "/usr/bin/sandbox-exec")
    argv = host._network_sandbox_argv(["fixture"], attempt, None, filesystem_policy=config,
                                    require_filesystem_confinement=True)
    assert argv[:2] == ["/usr/bin/sandbox-exec", "-p"] and argv[3:] == ["fixture"]
    assert "(deny default)" in argv[2]
    assert "(allow file-read*)" not in argv[2]
    assert "network" not in argv[2]
    assert '(subpath "/tmp")' not in argv[2]
    assert '(subpath "/private/tmp")' not in argv[2]
    with pytest.raises(host.HostError, match="does not authorize a network endpoint"):
        host._network_sandbox_argv(["fixture"], attempt, "fixture-network-not-authorized", filesystem_policy=config)


def test_legacy_no_endpoint_path_is_unchanged(tmp_path):
    original = ["fixture"]
    assert host._network_sandbox_argv(original, tmp_path, None) is original
