import json
import os
import zipfile
from dataclasses import dataclass

from astrid.core.gateway import dispatch, doctor_bundle


def test_redact_log_removes_token_and_credential_values():
    text = "api_key=sk-test credential: pass-123 Authorization: Bearer secret-value\n"

    redacted = doctor_bundle.redact_log(text)

    for secret in ("sk-test", "pass-123", "secret-value"):
        assert secret not in redacted
    assert "<redacted>" in redacted


def test_redact_log_handles_json_environment_urls_and_private_keys():
    private_key = "-----BEGIN PRIVATE KEY-----\nprivate-key-bytes\n-----END PRIVATE KEY-----"
    content = '\n'.join((
        '{"token":"json-token","credentials":{"key":"nested-key"}}',
        "ASTRID_WORKSPACE_CREDENTIAL=workspace-secret OPENAI_API_KEY=openai-secret",
        "fetch https://alice:url-password@example.test/path",
        private_key,
    ))

    redacted = doctor_bundle.redact_log(content)

    for secret in ("json-token", "nested-key", "workspace-secret", "openai-secret", "url-password", "private-key-bytes"):
        assert secret not in redacted
    assert "credentials" in redacted and "<redacted private key>" in redacted


def test_bundle_contains_redacted_logs_and_safe_manifest_projection(tmp_path, monkeypatch):
    support = tmp_path / "support"
    support.mkdir()
    (support / "install.json").write_text(json.dumps({
        "version": "v1", "data_root": "/home/alice/private", "token": "do-not-include",
        "versions": {"agent": {"sha": "abc123", "url": "https://user:pw@example.test"}},
    }))
    log = tmp_path / "runtime.log"
    log.write_text("access_token=tok-value password=pw-value\nhealthy\n")
    monkeypatch.setattr(doctor_bundle, "_logs", lambda *_args: [log])
    archive_path = doctor_bundle.write_bundle(
        tmp_path / "support.zip",
        {"ok": True, "credentials": {"key": "status-secret"},
         "env": {"CUSTOM_NAME": "private-env-value"},
         "path": "/home/alice/status-private-path",
         "runtime": {"services": [{"name": "chat", "state": "running"}]}},
        support,
    )

    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        assert {"status.json", "versions.json", "install-manifest.json"} <= names
        log_member = next(name for name in names if name.startswith("logs/") and name.endswith("runtime.log"))
        all_text = "\n".join(archive.read(name).decode() for name in names)
        assert "private" not in all_text and "status-secret" not in all_text
        assert "private-env-value" not in all_text and "status-private-path" not in all_text
        assert "tok-value" not in all_text and "pw-value" not in all_text
        assert "healthy" in archive.read(log_member).decode()
        assert "do-not-include" not in all_text and "alice" not in all_text
        manifest = json.loads(archive.read("install-manifest.json"))
        assert manifest == {"version": "v1", "versions": {"agent": {"sha": "abc123"}}}
        status = json.loads(archive.read("status.json"))
        assert status["runtime"]["services"][0]["state"] == "running"


def test_installed_runtime_version_uses_recorded_program_root(tmp_path, monkeypatch):
    import importlib.metadata

    import astrid.installer.core

    program_root = tmp_path / "custom-program-root"
    python = program_root / "versions" / "v1" / "py" / "bin" / "python"
    installed = type("Installed", (), {"python": python})()
    distribution = type("Distribution", (), {"metadata": {"Name": "astrid-runtime"}, "version": "2.3.4"})()
    monkeypatch.setattr(doctor_bundle, "_installed_record", lambda: (program_root, None))
    monkeypatch.setattr(astrid.installer.core, "current", lambda _root: installed)
    monkeypatch.setattr(importlib.metadata, "distributions", lambda *, path: [distribution])

    assert doctor_bundle._installed_runtime_version() == "2.3.4"


def test_install_manifest_uses_recorded_custom_program_root(tmp_path, monkeypatch):
    import astrid.installer.service

    default_root = tmp_path / "default"
    program_root = tmp_path / "custom-program-root"
    version_root = program_root / "versions" / "v1"
    python = version_root / "py" / "bin" / "python"
    python.parent.mkdir(parents=True)
    version_root.mkdir(exist_ok=True)
    (version_root / "profile.json").write_text("{}")
    (program_root / "current").write_text("v1\n")
    (version_root / "version.json").write_text(json.dumps({
        "root": str(version_root), "python": str(python),
        "profile": str(version_root / "profile.json"), "env": {},
    }))
    (version_root / "manifest.json").write_text(json.dumps({
        "schema_version": 1, "agent": {"sha": "a" * 40},
        "runtime": {"sha": "b" * 40},
        "tools": {"python": {"version": "3.11.9"}},
        "token": "must-not-ship",
    }))
    default_root.mkdir()
    (default_root / "service.json").write_text(json.dumps({
        "owner": astrid.installer.service.LABEL, "program_root": str(program_root),
    }))
    monkeypatch.setattr(astrid.installer.service, "default_program_root", lambda *_args: default_root)

    manifest = doctor_bundle._install_manifest(tmp_path / "support")

    assert manifest == {
        "schema_version": 1,
        "agent": {"sha": "a" * 40},
        "runtime": {"sha": "b" * 40},
        "tools": {"python": {"version": "3.11.9"}},
    }


def test_bundle_keeps_bounded_log_tail_and_discovers_managed_logs(tmp_path, monkeypatch):
    import runtime_protocol.platform

    runtime_logs = tmp_path / "runtime-logs"
    runtime_logs.mkdir()
    (runtime_logs / "astrid-runtime.log").write_text("runtime current\n")
    (runtime_logs / "astrid-runtime.log.1").write_text("runtime previous\n")
    (runtime_logs / "install.log").write_text("install current\n")
    (runtime_logs / "private.txt").write_text("must not include\n")
    monkeypatch.setattr(runtime_protocol.platform, "log_dir", lambda: runtime_logs)
    support = tmp_path / "support"
    support.mkdir()
    host_log = support / "generic-host.log"
    host_log.write_text("head-secret=" + "x" * (doctor_bundle._MAX_LOG_BYTES + 10) + "\ntail-visible\n")
    (support / "generic-host.log.1").write_text("host previous\n")

    discovered = doctor_bundle._logs(support)
    assert {"astrid-runtime.log", "astrid-runtime.log.1", "install.log", "generic-host.log", "generic-host.log.1"} <= {
        path.name for path in discovered
    }
    assert not any(path.name == "private.txt" for path in discovered)
    monkeypatch.setattr(doctor_bundle, "_logs", lambda *_args: [host_log])
    archive_path = doctor_bundle.write_bundle(tmp_path / "tail.zip", {"ok": True}, support)
    with zipfile.ZipFile(archive_path) as archive:
        text = archive.read(next(name for name in archive.namelist() if name.startswith("logs/"))).decode()
    assert "tail-visible" in text and "head-secret" not in text
    if os.name == "posix":
        assert (tmp_path / "tail.zip").stat().st_mode & 0o777 == 0o600


def test_bounded_log_tail_redacts_private_key_with_truncated_begin(tmp_path):
    log = tmp_path / "generic-host.log"
    log.write_text(
        "early log\n-----BEGIN PRIVATE KEY-----\n"
        + "private-fragment\n" * (doctor_bundle._MAX_LOG_BYTES // 12)
        + "-----END PRIVATE KEY-----\ntail-visible\n",
        encoding="utf-8",
    )

    text = doctor_bundle._read_tail(log).decode("utf-8", errors="replace")
    redacted = doctor_bundle.redact_log(text)

    assert "private-fragment" not in redacted
    assert "<redacted truncated private key>" in redacted
    assert "tail-visible" in redacted


def test_doctor_bundle_cli_writes_archive_without_mutating_services(tmp_path, monkeypatch, capsys):
    import astrid.core.gateway.diagnostics as diagnostics
    import astrid.runtime_cli
    import astrid.sdk.storage_root

    observed = type("Observed", (), {"data": {"ok": True, "runtime_health": {"services": [{"name": "pack-host", "state": "running"}]}}, "returncode": 0})()
    monkeypatch.setattr(diagnostics, "collect_diagnostic", lambda *_args, **_kwargs: ({"problemCode": None}, None, observed))
    monkeypatch.setattr(astrid.runtime_cli, "RuntimeCLI", type("RuntimeCLI", (), {}))
    monkeypatch.setattr(astrid.sdk.storage_root, "resolve_runtime_data_root", lambda: tmp_path)
    monkeypatch.setattr(doctor_bundle, "_logs", lambda *_args: [])
    target = tmp_path / "doctor.zip"

    assert dispatch._dispatch_doctor(["--bundle", str(target)]) == 0

    assert target.is_file()
    assert "Astrid doctor bundle:" in capsys.readouterr().out
    with zipfile.ZipFile(target) as archive:
        status = json.loads(archive.read("status.json"))
    assert status["runtime_health"]["services"][0]["state"] == "running"


def test_collect_diagnostic_preserves_runtime_service_states(tmp_path, monkeypatch):
    from astrid.core.gateway.diagnostics import collect_diagnostic

    @dataclass
    class Result:
        data: dict
        ok: bool = True
        returncode: int = 0

    class Runtime:
        def observe(self, command, **_kwargs):
            if command == "doctor":
                return Result({"ok": True, "healthy": True})
            return Result({"ok": True, "health": {"services": [{"name": "chat", "state": "running"}]}})

    monkeypatch.setattr("astrid.core.gateway.diagnostics.collect_product_observations", lambda *_args: {
        "cleanupLatch": {"blocked": False}, "packQuarantine": {},
        "runtimeClientCompatibility": {"observed": False, "value": None},
    })

    _diagnostic, _workspace, observed = collect_diagnostic(Runtime(), support_root=str(tmp_path), command="doctor")

    assert observed.data["runtime_health"]["services"][0] == {"name": "chat", "state": "running"}


def test_doctor_bundle_survives_unavailable_support_root(tmp_path, monkeypatch, capsys):
    import astrid.runtime_cli
    import astrid.sdk.storage_root

    monkeypatch.setattr(astrid.runtime_cli, "RuntimeCLI", type("RuntimeCLI", (), {}))
    monkeypatch.setattr(astrid.sdk.storage_root, "resolve_runtime_data_root", lambda: (_ for _ in ()).throw(ValueError("invalid selection")))
    monkeypatch.setattr(doctor_bundle, "_logs", lambda *_args: [])
    target = tmp_path / "unavailable.zip"

    assert dispatch._dispatch_doctor(["--bundle", str(target)]) == 1

    with zipfile.ZipFile(target) as archive:
        status = json.loads(archive.read("status.json"))
    assert status["state"] == "runtime_unavailable"
    assert "Astrid doctor bundle:" in capsys.readouterr().out
