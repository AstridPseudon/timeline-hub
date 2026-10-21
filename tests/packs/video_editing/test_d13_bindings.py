from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.packs.video_editing import d13_bindings


def _contract(tmp_path: Path) -> tuple[Path, Path]:
    profile = tmp_path / "profile.json"
    source = tmp_path / "site-packages"
    environment = tmp_path / "venv"
    bindings = tmp_path / "bindings.json"
    values = {
        "agent_commit": "a" * 40,
        "agent_tree": "b" * 40,
        "agent_wheel": str(tmp_path / "astrid.whl"),
        "agent_wheel_sha256": "c" * 64,
        "source_checkout": str(source),
        "source_digest": "d" * 64,
        "runtime_environment": str(environment),
    }
    profile.write_text(
        json.dumps({
            "profile": "astrid",
            "runtime_checkout": str(source),
            "source_checkout": str(source),
            "runtime_environment": str(environment),
        }),
        encoding="utf-8",
    )
    bindings.write_text(json.dumps(values), encoding="utf-8")
    return profile, bindings


def _env(monkeypatch, profile: Path, bindings: Path, tmp_path: Path) -> None:
    monkeypatch.setenv("ASTRID_D13_SOURCE_PROFILE", str(profile))
    monkeypatch.setenv("ASTRID_D13_EXPECTED_BINDINGS", str(bindings))
    for name, value in {
        "ASTRID_NODE_EXECUTABLE": tmp_path / "node",
        "ASTRID_D13_NODE_SHA256": "1" * 64,
        "ASTRID_REMOTION_PROJECT_DIR": tmp_path / "remotion",
        "ASTRID_D13_REMOTION_LOCK_SHA256": "2" * 64,
        "ASTRID_REMOTION_BROWSER_EXECUTABLE": tmp_path / "browser",
        "ASTRID_D13_BROWSER_SHA256": "3" * 64,
        "ASTRID_FFMPEG_EXECUTABLE": tmp_path / "ffmpeg",
        "ASTRID_D13_FFMPEG_SHA256": "4" * 64,
        "ASTRID_FFPROBE_EXECUTABLE": tmp_path / "ffprobe",
        "ASTRID_D13_FFPROBE_SHA256": "5" * 64,
        "ASTRID_TEST_NODE_MODULES": tmp_path / "node_modules",
    }.items():
        monkeypatch.setenv(name, str(value))


def test_d13_bindings_loader_accepts_existing_profile_and_seven_key_carrier(tmp_path, monkeypatch):
    profile, bindings = _contract(tmp_path)
    _env(monkeypatch, profile, bindings, tmp_path)

    inputs, failures = d13_bindings.load_inputs()

    assert failures == []
    assert inputs is not None
    assert inputs.agent_commit == "a" * 40
    assert inputs.source == tmp_path / "site-packages"
    assert inputs.environment == tmp_path / "venv"


def test_d13_bindings_loader_rejects_new_json_field(tmp_path, monkeypatch):
    profile, bindings = _contract(tmp_path)
    values = json.loads(bindings.read_text(encoding="utf-8"))
    values["launch_validation"] = "not-a-contract-field"
    bindings.write_text(json.dumps(values), encoding="utf-8")
    _env(monkeypatch, profile, bindings, tmp_path)

    inputs, failures = d13_bindings.load_inputs()

    assert inputs is not None
    assert any("exactly the existing seven" in failure for failure in failures)


def test_d13_named_collection_is_only_constructed_and_clears_forbidden_node_env(tmp_path):
    inputs = d13_bindings.D13Inputs(
        profile=tmp_path / "profile.json",
        bindings=tmp_path / "bindings.json",
        source=tmp_path / "site-packages",
        environment=tmp_path / "venv",
        agent_commit="a" * 40,
        agent_tree="b" * 40,
        agent_wheel=tmp_path / "astrid.whl",
        agent_wheel_sha256="c" * 64,
        source_digest="d" * 64,
        node=tmp_path / "node",
        node_sha256="1" * 64,
        remotion=tmp_path / "remotion",
        remotion_lock_sha256="2" * 64,
        browser=tmp_path / "browser",
        browser_sha256="3" * 64,
        ffmpeg=tmp_path / "ffmpeg",
        ffmpeg_sha256="4" * 64,
        ffprobe=tmp_path / "ffprobe",
        ffprobe_sha256="5" * 64,
        node_modules=tmp_path / "node_modules",
    )

    runtime_checkout = tmp_path / "runtime"
    runtime_checkout.mkdir()
    command, environment = d13_bindings.named_collection_command(
        inputs,
        tmp_path,
        runtime_checkout=runtime_checkout,
        run_root=Path("/tmp/d13-abcd"),
    )

    assert command[:4] == [str(inputs.environment / "bin" / "python"), "-B", "-m", "pytest"]
    assert command[-3:] == [d13_bindings._NATIVE_TEST, "--collect-only", "-q"]
    assert environment["ASTRID_RUNTIME_CHECKOUT"] == str(runtime_checkout)
    assert environment["ASTRID_D13_SOURCE_PROFILE"] == str(inputs.profile)
    assert environment["ASTRID_D13_EXPECTED_BINDINGS"] == str(inputs.bindings)
    assert environment["ASTRID_D13_NODE_SHA256"] == inputs.node_sha256
    assert environment["ASTRID_D13_REMOTION_LOCK_SHA256"] == inputs.remotion_lock_sha256
    assert environment["ASTRID_D13_BROWSER_SHA256"] == inputs.browser_sha256
    assert environment["ASTRID_D13_FFMPEG_SHA256"] == inputs.ffmpeg_sha256
    assert environment["ASTRID_D13_FFPROBE_SHA256"] == inputs.ffprobe_sha256
    assert environment["XDG_RUNTIME_DIR"] == "/tmp/d13-abcd/tmp"
    assert str(tmp_path) not in environment["TMPDIR"]
    assert not {"NODE_OPTIONS", "NODE_PATH", "PYTHONHOME", "PYTHONPATH"} & environment.keys()
    assert not any(name.startswith("LD_") for name in environment)
    with pytest.raises(ValueError, match="short"):
        d13_bindings.named_collection_command(
            inputs,
            tmp_path,
            runtime_checkout=runtime_checkout,
            run_root=Path("/tmp") / ("d13-" + "x" * 100),
        )
