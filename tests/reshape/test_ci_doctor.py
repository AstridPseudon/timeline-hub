"""The CI doctor gate accepts either public envelope when C2 is consistent."""

from __future__ import annotations

from astrid.core.gateway import diagnostics
from scripts.reshape import ci_doctor


def _healthy_report() -> dict:
    return diagnostics.build_diagnostic(mode="local", facts={})


def _failed_report() -> dict:
    return diagnostics.build_diagnostic(
        mode="local",
        facts={},
        problem_code="runtime_unavailable",
        failure_boundary="runtime-contact",
        next_actions=[
            {
                "commandId": "runtime-up",
                "arguments": [],
                "effects": diagnostics.COMMAND_EFFECTS["runtime-up"],
                "authorizationRequired": True,
                "executable": True,
            }
        ],
    )


def test_ci_doctor_accepts_observed_report_shape() -> None:
    payload = {
        "healthy": False,
        "issues": ["runtime unavailable"],
        "diagnostic": _failed_report(),
    }

    assert ci_doctor.contract_errors(payload, 1) == []


def test_ci_doctor_accepts_fail_closed_report_shape() -> None:
    payload = {
        "ok": False,
        "problem_code": "runtime_unavailable",
        "diagnostic": _failed_report(),
    }

    assert ci_doctor.contract_errors(payload, 1) == []


def test_ci_doctor_rejects_missing_or_malformed_c2_payload() -> None:
    assert ci_doctor.contract_errors({"ok": False}, 1)

    malformed = _failed_report()
    malformed.pop("contractDigest")
    errors = ci_doctor.contract_errors({"diagnostic": malformed}, 1)
    assert any("C2 identity is invalid" in error for error in errors)


def test_ci_doctor_rejects_exit_and_health_mismatches() -> None:
    failed = _failed_report()
    assert any(
        "disagrees with exit" in error
        for error in ci_doctor.contract_errors({"diagnostic": failed}, 0)
    )
    assert any(
        "healthy disagrees" in error
        for error in ci_doctor.contract_errors(
            {"healthy": True, "diagnostic": failed}, 1
        )
    )
    assert any(
        "ok disagrees" in error
        for error in ci_doctor.contract_errors(
            {"ok": True, "diagnostic": failed}, 1
        )
    )
    assert ci_doctor.contract_errors({"diagnostic": _healthy_report()}, 1)


def test_ci_doctor_environment_ignores_inherited_roots_and_secrets(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", "/live/runtime")
    monkeypatch.setenv("ASTRID_STATE_HOME", "/live/state")
    monkeypatch.setenv("XDG_CONFIG_HOME", "/live/config")
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", "/legacy/data")
    monkeypatch.setenv("OPENAI_API_KEY", "not-for-the-doctor-gate")

    env = ci_doctor.hermetic_env(tmp_path)

    assert env["ASTRID_RUNTIME_DATA_ROOT"] == str(tmp_path / "data")
    assert env["ASTRID_STATE_HOME"] == str(tmp_path / "astrid-state")
    assert env["HOME"] == str(tmp_path)
    assert env["TMPDIR"] == str(tmp_path)
    for name in ("XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"):
        assert env[name] == str(tmp_path / name.lower())
    assert "BANODOCO_LOCAL_DATA_ROOT" not in env
    assert "OPENAI_API_KEY" not in env
