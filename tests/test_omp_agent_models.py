"""Hermetic subprocess contracts for the Astrid OMP provider commands."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SNAPSHOT: dict[str, Any] = {
    "schemaVersion": 1,
    "currentModel": "alpha/model/team/name",
    "providers": [
        {
            "id": "alpha",
            "name": "Alpha Provider",
            "signedIn": True,
            "models": [
                {"id": "model/team/name", "name": "Team Model", "selector": "alpha/model/team/name"},
                {"id": "small", "name": "Small", "selector": "alpha/small"},
            ],
        },
        {"id": "closed", "name": "Closed Provider", "signedIn": False, "models": []},
        {
            "id": "keyless",
            "name": "Keyless Provider",
            "signedIn": False,
            "models": [{"id": "public", "name": "Public Model", "selector": "keyless/public"}],
        },
    ],
}

FAKE_OMP = r'''#!{python}
import json
import os
from pathlib import Path
import sys

log = Path(os.environ["FAKE_OMP_LOG"])
args = sys.argv[1:]
record = {{"argv": args, "selection": os.environ.get("ASTRID_OMP_MODEL_SELECTION")}}
if args[:2] == ["--mode", "rpc"]:
    record["input"] = sys.stdin.read()
with log.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(record) + "\n")

if args[:2] == ["--mode", "rpc"]:
    rpc_mode = os.environ.get("FAKE_OMP_RPC_MODE", "ok")
    if rpc_mode == "fail":
        print(json.dumps({{"id": "astrid-login-providers", "type": "response", "command": "get_login_providers", "success": False, "data": {{}}}}))
    elif rpc_mode == "missing":
        print(json.dumps({{"type": "notification", "message": "no provider response"}}))
    else:
        snapshot = json.loads(os.environ["FAKE_OMP_SNAPSHOT"])
        providers = json.loads(os.environ["FAKE_OMP_LOGIN_PROVIDERS"]) if "FAKE_OMP_LOGIN_PROVIDERS" in os.environ else [
            {{"id": p["id"], "name": p["name"], "authenticated": p["signedIn"]}}
            for p in snapshot["providers"]
        ]
        print(json.dumps({{"id": "astrid-login-providers", "type": "response", "command": "get_login_providers", "success": True, "data": {{"providers": providers}}}}))
    raise SystemExit(int(os.environ.get("FAKE_OMP_RPC_EXIT", "0")))

if args and args[0] == "usage":
    print(json.dumps(json.loads(os.environ.get("FAKE_OMP_USAGE", '{{"reports": []}}'))))
    raise SystemExit(int(os.environ.get("FAKE_OMP_USAGE_EXIT", "0")))

result_path = os.environ.get("ASTRID_OMP_MODELS_RESULT")
mode = os.environ.get("FAKE_OMP_MODE", "ok")
if mode == "no-result":
    raise SystemExit(0)
if mode == "malformed":
    Path(result_path).write_text("not-json", encoding="utf-8")
    raise SystemExit(0)

snapshot = json.loads(os.environ["FAKE_OMP_SNAPSHOT"])
selection = os.environ.get("ASTRID_OMP_MODEL_SELECTION")
state_path = Path(os.environ["FAKE_OMP_STATE"])
if selection is not None:
    if mode == "provider-only" and selection in {{"closed", "closed/model"}}:
        Path(result_path).write_text(json.dumps({{"error": "Sign in: run `omp`, then /login and pick Closed Provider"}}), encoding="utf-8")
        raise SystemExit(1)
    match = next((model for provider in snapshot["providers"] for model in provider["models"] if model["selector"] == selection), None)
    if not match:
        Path(result_path).write_text(json.dumps({{"error": "Unknown or unavailable model selector"}}), encoding="utf-8")
        raise SystemExit(1)
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {{}}
    state["roles"] = {{**state.get("roles", {{}}), "default": selection}}
    state_path.write_text(json.dumps(state), encoding="utf-8")
    snapshot["currentModel"] = selection

Path(result_path).write_text(json.dumps(snapshot), encoding="utf-8")
raise SystemExit(int(os.environ.get("FAKE_OMP_EXIT", "0")))
'''


def _setup(tmp_path: Path, *, snapshot: dict[str, Any] | None = None) -> tuple[dict[str, str], Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    fake_omp = tmp_path / "omp-fake"
    fake_omp.write_text(FAKE_OMP.format(python=sys.executable), encoding="utf-8")
    fake_omp.chmod(0o755)
    log = tmp_path / "calls.jsonl"
    state = tmp_path / "omp-state.json"
    state.write_text(json.dumps({"roles": {"default": "before/model", "coding": "keep/coding", "title": "keep/title"}, "other": "preserve"}), encoding="utf-8")
    env = os.environ.copy()
    for key in tuple(env):
        if key.startswith("FAKE_OMP_"):
            env.pop(key)
    for key in (
        "BANODOCO_LOCAL_DATA_ROOT",
        "BANODOCO_LOCAL_SOURCE_MANIFEST",
        "ASTRID_LOCAL_DATA_ROOT",
        "ASTRID_RUNTIME_DATA_ROOT",
        "ASTRID_LOCAL_SOURCE_MANIFEST",
        "ASTRID_AGENT_LAUNCHER",
        "OMP_AGENT_LAUNCHER",
    ):
        env.pop(key, None)
    fake_snapshot = json.loads(json.dumps(snapshot if snapshot is not None else SNAPSHOT))
    fake_snapshot["_catalogModel"] = "alpha/model/team/name"
    fake_snapshot.setdefault("_hiddenProviderIds", [])
    env.update(
        {
            "OMP_BIN": str(fake_omp),
            "ASTRID_STOCK_OMP": "1",
            "FAKE_OMP_LOG": str(log),
            "FAKE_OMP_STATE": str(state),
            "FAKE_OMP_SNAPSHOT": json.dumps(fake_snapshot),
            "HOME": str(tmp_path / "home"),
        }
    )
    return env, log, state


def _run(tmp_path: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", "from astrid.omp_agent import main; raise SystemExit(main())", *args],
        cwd=Path(__file__).parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _calls(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_models_json_returns_selector_snapshot_and_uses_only_fake_omp(tmp_path: Path) -> None:
    env, log, _state = _setup(tmp_path)

    result = _run(tmp_path, env, "agent", "models", "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == SNAPSHOT
    assert payload["providers"][0]["models"][0]["selector"] == "alpha/model/team/name"
    calls = _calls(log)
    assert calls[0]["argv"][:3] == ["models", "ls", "--json"]
    assert calls[0]["argv"][3] == "-e"
    assert calls[0]["argv"][4].endswith("astrid/omp_extensions/astrid-models.ts")
    assert [call["argv"][:2] for call in calls] == [
        ["models", "ls"], ["--mode", "rpc"], ["usage", "--json"]
    ]
    assert "--model" in calls[1]["argv"]
    assert calls[1]["argv"][calls[1]["argv"].index("--model") + 1] == "alpha/model/team/name"
    assert calls[1]["input"] == '{"id":"astrid-login-providers","type":"get_login_providers"}\n'
    assert "_catalogModel" not in result.stdout and "_hiddenProviderIds" not in result.stdout


def test_models_human_output_includes_provider_state_and_provider_only_hint(tmp_path: Path) -> None:
    env, log, _state = _setup(tmp_path)

    result = _run(tmp_path, env, "agent", "models")

    assert result.returncode == 0, result.stderr
    assert "Astrid default model: alpha/model/team/name" in result.stdout
    assert "Alpha Provider (alpha) — signed in" in result.stdout
    assert "alpha/model/team/name  Team Model" in result.stdout
    assert "Keyless Provider (keyless) — not signed in" in result.stdout
    assert "keyless/public  Public Model" in result.stdout
    assert "Closed Provider (closed) — not signed in" in result.stdout
    assert "Sign in: run `omp`, then /login and pick Closed Provider" in result.stdout
    assert _calls(log)[1]["argv"][:2] == ["--mode", "rpc"]


def test_login_only_provider_is_merged_and_hidden_provider_is_excluded(tmp_path: Path) -> None:
    snapshot = json.loads(json.dumps(SNAPSHOT))
    snapshot["_hiddenProviderIds"] = ["secret-hidden"]
    env, _log, _state = _setup(tmp_path, snapshot=snapshot)
    env["FAKE_OMP_LOGIN_PROVIDERS"] = json.dumps(
        [
            {"id": "alpha", "name": "Alpha Provider", "authenticated": True},
            {"id": "plugin-only", "name": "Custom Login Plugin", "authenticated": False},
            {"id": "secret-hidden", "name": "Must Stay Hidden", "authenticated": True},
        ]
    )

    result = _run(tmp_path, env, "agent", "models", "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert [provider["id"] for provider in payload["providers"]] == ["alpha", "closed", "keyless", "plugin-only"]
    plugin = payload["providers"][-1]
    assert plugin == {"id": "plugin-only", "name": "Custom Login Plugin", "signedIn": False, "models": []}
    assert "secret-hidden" not in result.stdout and "Must Stay Hidden" not in result.stdout


def test_login_only_signed_out_provider_gets_named_sign_in_hint(tmp_path: Path) -> None:
    env, _log, state_path = _setup(tmp_path)
    env["FAKE_OMP_LOGIN_PROVIDERS"] = json.dumps(
        [{"id": "plugin-only", "name": "Custom Login Plugin", "authenticated": False}]
    )
    before = state_path.read_text(encoding="utf-8")

    result = _run(tmp_path, env, "agent", "use", "plugin-only/model")

    assert result.returncode != 0
    assert result.stdout == ""
    assert result.stderr.strip() == "astrid: Sign in: run `omp`, then /login and pick Custom Login Plugin"
    assert state_path.read_text(encoding="utf-8") == before


def test_models_json_does_not_emit_raw_account_or_scope_usage_fields(tmp_path: Path) -> None:
    env, _log, _state = _setup(tmp_path)
    env["FAKE_OMP_USAGE"] = json.dumps(
        {
            "reports": [
                {
                    "provider": "alpha",
                    "fetchedAt": 1792404000000,
                    "account": "ACCOUNT_CANARY",
                    "scope": "SCOPE_CANARY",
                    "raw": "RAW_CANARY",
                    "limits": [{"label": "daily", "amount": {"remaining": 42, "unit": "usd"}, "window": {"id": "day", "label": "Day"}, "status": "ok", "account": "LIMIT_CANARY"}],
                }
            ]
        }
    )

    result = _run(tmp_path, env, "agent", "models", "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["providers"][0]["usage"] == [
        {"fetchedAt": 1792404000000, "limits": [{"label": "daily", "amount": {"remaining": 42, "unit": "usd"}, "window": {"id": "day", "label": "Day"}, "status": "ok"}]}
    ]
    for canary in ("ACCOUNT_CANARY", "SCOPE_CANARY", "RAW_CANARY", "LIMIT_CANARY"):
        assert canary not in result.stdout


def test_use_saves_exact_model_selector_and_preserves_other_roles(tmp_path: Path) -> None:
    env, log, state_path = _setup(tmp_path)

    result = _run(tmp_path, env, "agent", "use", "alpha/model/team/name", "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["currentModel"] == "alpha/model/team/name"
    assert json.loads(state_path.read_text(encoding="utf-8")) == {
        "roles": {
            "default": "alpha/model/team/name",
            "coding": "keep/coding",
            "title": "keep/title",
        },
        "other": "preserve",
    }
    calls = _calls(log)
    assert len(calls) == 3
    assert calls[0]["argv"][:3] == ["models", "ls", "--json"]
    assert calls[1]["argv"][:2] == ["--mode", "rpc"]
    assert calls[2]["selection"] == "alpha/model/team/name"
    assert calls[2]["argv"][:3] == ["models", "ls", "--json"]


def test_use_accepts_signed_out_provider_model(tmp_path: Path) -> None:
    env, _log, state_path = _setup(tmp_path)

    result = _run(tmp_path, env, "agent", "use", "keyless/public", "--json")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["currentModel"] == "keyless/public"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["roles"]["default"] == "keyless/public"


def test_provider_only_signed_out_selection_prints_one_line_sign_in_hint_without_mutation(tmp_path: Path) -> None:
    for selector in ("closed", "closed/model"):
        env, _log, state_path = _setup(tmp_path / selector.replace("/", "-"))
        before = state_path.read_text(encoding="utf-8")

        result = _run(tmp_path, env, "agent", "use", selector)

        assert result.returncode != 0
        assert result.stdout == ""
        assert result.stderr.count("\n") == 1
        assert "Sign in: run `omp`, then /login and pick Closed Provider" in result.stderr
        assert state_path.read_text(encoding="utf-8") == before


def test_invalid_provider_or_model_fails_without_state_mutation(tmp_path: Path) -> None:
    env, log, state_path = _setup(tmp_path)
    before = state_path.read_text(encoding="utf-8")

    for selector in ("unknown/model", "alpha/not-enabled", ""):
        result = _run(tmp_path, env, "agent", "use", selector)
        assert result.returncode != 0
        assert result.stdout == ""
        assert result.stderr.strip()
        assert state_path.read_text(encoding="utf-8") == before
    assert len(_calls(log)) == 6


def test_models_reports_missing_or_invalid_explicit_omp_path_without_starting_launcher(tmp_path: Path) -> None:
    env, log, _state = _setup(tmp_path)
    env.pop("OMP_BIN")
    env["PATH"] = str(tmp_path / "empty-path")

    missing = _run(tmp_path, env, "agent", "models", "--json")
    assert missing.returncode != 0
    assert "could not locate the OMP binary" in missing.stderr
    assert _calls(log) == []

    env["OMP_BIN"] = str(tmp_path / "does-not-exist")
    invalid = _run(tmp_path, env, "agent", "models", "--json")
    assert invalid.returncode != 0
    assert "does-not-exist" in invalid.stderr
    assert _calls(log) == []


def test_help_describes_model_commands_without_invoking_omp(tmp_path: Path) -> None:
    env, log, _state = _setup(tmp_path)

    result = _run(tmp_path, env, "--help")

    assert result.returncode == 0
    assert "astrid agent models [--json]" in result.stdout
    assert "astrid agent use PROVIDER/MODEL" in result.stdout
    assert _calls(log) == []
    for command in ("models", "use"):
        result = _run(tmp_path, env, "agent", command, "--help")
        assert result.returncode == 0
        assert "schemaVersion" in result.stdout
        assert "currentModel" in result.stdout
        assert "signedIn" in result.stdout
        assert _calls(log) == []


def test_usage_failure_or_unavailable_usage_is_optional(tmp_path: Path) -> None:
    env, _log, _state = _setup(tmp_path)
    env["FAKE_OMP_USAGE"] = json.dumps({"reports": [{"provider": "alpha", "account": "NO_USAGE_CANARY"}]})
    env["FAKE_OMP_USAGE_EXIT"] = "1"

    failed = _run(tmp_path, env, "agent", "models", "--json")
    assert failed.returncode == 0
    assert "usage" not in json.loads(failed.stdout)["providers"][0]
    assert "NO_USAGE_CANARY" not in failed.stdout

    env["FAKE_OMP_USAGE"] = "not-json"
    malformed = _run(tmp_path, env, "agent", "models", "--json")
    assert malformed.returncode == 0
    assert "usage" not in json.loads(malformed.stdout)["providers"][0]


def test_missing_or_malformed_snapshot_and_nonzero_omp_are_errors(tmp_path: Path) -> None:
    for mode, exit_code in (("no-result", "0"), ("malformed", "0"), ("ok", "2")):
        env, _log, _state = _setup(tmp_path / mode)
        env["FAKE_OMP_MODE"] = mode
        env["FAKE_OMP_EXIT"] = exit_code
        result = _run(tmp_path, env, "agent", "models", "--json")
        assert result.returncode != 0
        assert result.stdout == ""
        assert result.stderr.strip()


def test_login_provider_rpc_failure_or_missing_response_fails_without_mutation(tmp_path: Path) -> None:
    for mode in ("fail", "missing"):
        env, log, state_path = _setup(tmp_path / mode)
        env["FAKE_OMP_RPC_MODE"] = mode
        before = state_path.read_text(encoding="utf-8")

        models = _run(tmp_path, env, "agent", "models", "--json")
        assert models.returncode != 0
        assert models.stdout == ""
        assert "sign-in providers" in models.stderr
        assert len(_calls(log)) == 2
        assert state_path.read_text(encoding="utf-8") == before

        selection = _run(tmp_path, env, "agent", "use", "alpha/model/team/name")
        assert selection.returncode != 0
        assert selection.stdout == ""
        assert "sign-in providers" in selection.stderr
        assert len(_calls(log)) == 4
        assert state_path.read_text(encoding="utf-8") == before
