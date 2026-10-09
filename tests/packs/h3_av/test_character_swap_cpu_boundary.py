from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from astrid.packs.h3_av.src.input_bundle import build_input_bundle
from astrid.packs.h3_av.src.request import normalize_request
from astrid.packs.vibecomfy.asset_manifest import read_archive
from astrid.sdk.pagination import paged_rows


def _field(value, name: str, default=None):
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _boundary_blockers() -> list[str]:
    checkout = Path(__file__).resolve().parents[3]
    receiving_root = checkout.parents[1]
    runtime_root = Path(
        os.environ.get("ASTRID_STAGE1_RUNTIME_CHECKOUT")
        or receiving_root / "checkouts" / "banodoco-workspace-runtime--integration"
    )
    vibecomfy_root = Path(
        os.environ.get("ASTRID_VIBECOMFY_CHECKOUT") or receiving_root / "repos" / "vibecomfy"
    )
    profile = (
        Path(os.environ.get("ASTRID_H3_T9_READINESS_PROFILE"))
        if os.environ.get("ASTRID_H3_T9_READINESS_PROFILE")
        else receiving_root
        / "repos"
        / "Astrid"
        / ".otto/runs/h3-transform-pack-20260923/fixtures/t9-public-h3-20260925-9/support/runtime/t9-vibecomfy-readiness.json"
    )
    blockers = []
    if not runtime_root.is_dir():
        blockers.append(f"Runtime checkout unavailable at {runtime_root}")
    if not vibecomfy_root.is_dir():
        blockers.append(f"VibeComfy checkout unavailable at {vibecomfy_root}")
    if not profile.is_file():
        blockers.append(f"approved T9 readiness profile unavailable at {profile}")
    return blockers


def test_public_cpu_boundary_preflight_does_not_require_a_prior_qualification_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout = Path(__file__).resolve().parents[3]
    receiving_root = checkout.parents[1]
    profile = tmp_path / "synthetic-t9-template.json"
    profile.write_text(json.dumps({"profile_template": "test-only"}), encoding="utf-8")
    monkeypatch.setenv("ASTRID_STAGE1_RUNTIME_CHECKOUT", str(
        receiving_root / "checkouts" / "banodoco-workspace-runtime--integration"
    ))
    monkeypatch.setenv("ASTRID_VIBECOMFY_CHECKOUT", str(receiving_root / "repos" / "vibecomfy"))
    monkeypatch.setenv("ASTRID_H3_T9_READINESS_PROFILE", str(profile))
    monkeypatch.delenv("ASTRID_H3_CHARACTER_SWAP_CPU_QUALIFICATION_RECEIPT", raising=False)

    assert _boundary_blockers() == []


def test_h3_public_workspace_helper_pin_matches_current_shared_fixture() -> None:
    from tests.helpers import h3_cpu_runtime

    fixture = h3_cpu_runtime.PUBLIC_WORKSPACE_FIXTURE
    assert fixture.is_file() and not fixture.is_symlink()
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == (
        h3_cpu_runtime.PUBLIC_WORKSPACE_FIXTURE_SHA256
    )


def test_cpu_harness_asset_map_matches_public_transform_input_contract(tmp_path: Path) -> None:
    from tests.helpers.h3_cpu_runtime import _write_runtime_asset_map

    raw = {
        "version": 2,
        "prompt": "Describe the reference image.",
        "duration": 1,
        "media": [{"id": "look", "asset": "look.png", "role": "reference", "modality": "image"}],
        "settings": {},
    }
    image = tmp_path / "look.png"
    image.write_bytes(b"small deterministic image fixture")
    bundle = tmp_path / "input-bundle.zip"
    build_input_bundle(normalize_request(raw), {"look.png": str(image)}, bundle)

    asset_map_path = _write_runtime_asset_map(read_archive(bundle), tmp_path / "staged")
    asset_map = json.loads(asset_map_path.read_text(encoding="utf-8"))

    assert set(asset_map) == {"look.png"}
    materialized = Path(asset_map["look.png"])
    assert materialized.is_file()
    assert materialized.read_bytes() == image.read_bytes()


def test_cpu_harness_invokes_transform_unbound_without_request_or_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from types import SimpleNamespace

    import tests.helpers.h3_cpu_runtime as runtime_module

    request_path = tmp_path / "request.json"
    request_path.write_text("{}", encoding="utf-8")
    asset_map_path = tmp_path / "asset-map.json"
    asset_map_path.write_text("{}", encoding="utf-8")
    expected_path = tmp_path / "expected.json"
    archive = SimpleNamespace(manifest={"assets": [{
        "binding": "source.mp4", "member": "source.mp4", "sha256": "a" * 64, "size": 17,
    }]})
    monkeypatch.setattr(
        runtime_module,
        "normalize_request",
        lambda _value: SimpleNamespace(value={
            "version": 1, "source": {"asset": "source.mp4", "range": [0, 2]},
            "output": {"duration": 3},
        }),
    )
    monkeypatch.setattr(runtime_module, "read_archive", lambda _path: archive)

    def write_asset_map(_archive, out: Path) -> Path:
        out.mkdir(parents=True, exist_ok=True)
        return asset_map_path

    monkeypatch.setattr(runtime_module, "_write_runtime_asset_map", write_asset_map)

    captured = {}

    class Owner:
        def invoke_result(self, capability_id, **kwargs):
            captured.update({
                "capability_id": capability_id,
                "support_root_at_invocation": os.environ.get("BANODOCO_LOCAL_DATA_ROOT"),
                "model_substitute_profile_at_invocation": os.environ.get(
                    "ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"
                ),
                **kwargs,
            })
            return SimpleNamespace(ok=True)

    runtime = runtime_module.H3CpuRuntime.__new__(runtime_module.H3CpuRuntime)
    runtime.schema_session = SimpleNamespace(expected_path=expected_path)
    runtime.data_root = tmp_path / "selected-support-root"
    runtime.owner = Owner()
    runtime.project_id = "fixture-project"
    runtime.cpu_model_boundary = "test-only"
    out = tmp_path / "out"
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", "/tmp/stale-runtime-support")
    monkeypatch.setenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", "/tmp/stale-model-profile.json")

    result = runtime.run_public_transform(request_path, tmp_path / "bundle.zip", out=out, key="fixture")

    assert result.ok
    assert captured["capability_id"] == "h3_av.transform"
    assert captured["project"] == runtime.project_id
    assert captured["orchestrator_args"] == ("--project", runtime.project_id)
    assert captured["support_root_at_invocation"] == str(runtime.data_root.resolve())
    assert captured["model_substitute_profile_at_invocation"] is None
    assert "execution_request" not in captured
    assert set(captured["inputs"]) == {"request", "asset_map"}
    assert "execution_target" not in captured
    assert os.environ["BANODOCO_LOCAL_DATA_ROOT"] == "/tmp/stale-runtime-support"
    assert os.environ["ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"] == "/tmp/stale-model-profile.json"


def test_h3_synthetic_readiness_profile_uses_digest_bound_model_root(tmp_path: Path) -> None:
    from astrid.core.generation.model_root import model_root_binding_from_profile
    from tests.helpers.h3_cpu_runtime import _synthetic_model_root_binding

    model_root = tmp_path / "models"
    model_paths = (
        "vae/minimax_h3_audio_vae_fp32.safetensors",
        "vae/minimax_h3_video_vae_int8_convrot.safetensors",
        "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
        "loras/h3_character_swap_pro4500_1000.safetensors",
        "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors",
        "text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors",
    )
    for relative in model_paths:
        model = model_root / relative
        model.parent.mkdir(parents=True, exist_ok=True)
        model.write_bytes(f"synthetic model fixture: {relative}".encode())

    payload = _synthetic_model_root_binding(model_root, model_paths)
    binding = model_root_binding_from_profile({"launch": {"model_root": payload}})

    assert payload["schema_version"] == 1
    assert binding.path == model_root.resolve()
    assert len(binding.inventory) == len(model_paths)
    assert binding.qualification_identity is None


def test_character_swap_public_managed_cpu_boundary(tmp_path: Path) -> None:
    blockers = _boundary_blockers()
    if blockers:
        pytest.skip("public managed CPU boundary is not qualified: " + "; ".join(blockers))
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        pytest.skip("public managed CPU boundary requires ffmpeg and ffprobe")

    from PIL import Image

    from tests.helpers.h3_cpu_runtime import (
        APPROVED_CPU_MODEL_BOUNDARY,
        H3CpuRuntime,
    )

    caller = tmp_path / "caller"
    caller.mkdir()
    source = caller / "baseline.mp4"
    performance = caller / "performance.mp4"
    for path, color, tone in ((source, "blue", 440), (performance, "green", 660)):
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"color=c={color}:s=64x64:r=24:d=15",
            "-f", "lavfi", "-i", f"sine=frequency={tone}:sample_rate=48000:duration=15",
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", str(path),
        ], check=True, capture_output=True, timeout=60)
    replacement = caller / "replacement.png"
    Image.new("RGB", (64, 64), (32, 96, 160)).save(replacement)

    raw = {
        "version": 2,
        "prompt": "Replace the person in <Video 1> with the person in <Picture 1>.",
        "duration": 15,
        "media": [
            {"id": "baseline", "asset": "baseline.mp4", "role": "timeline", "modality": "video",
             "at": {"frame": 0}, "range": [0, 15],
             "edit": [{"stream": "video", "during": [0, 15], "mask": {"full_frame": True}}]},
            {"id": "performance", "asset": "performance.mp4", "role": "reference", "modality": "video",
             "range": [0, 15], "audio": False},
            {"id": "replacement", "asset": "replacement.png", "role": "reference", "modality": "image"},
        ],
        "settings": {"adapter": {"id": "character_swap_v1"}},
    }
    request_path = tmp_path / "request.json"
    request_path.write_text(json.dumps(raw, sort_keys=True), encoding="utf-8")
    request = normalize_request(raw)
    bundle_path = tmp_path / "input-bundle.zip"
    build_input_bundle(request, {
        "baseline.mp4": str(source),
        "performance.mp4": str(performance),
        "replacement.png": str(replacement),
    }, bundle_path)
    input_digests = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (source, performance, replacement)}
    for path in (source, performance, replacement):
        path.unlink()

    runtime = H3CpuRuntime(tmp_path / "runtime", cpu_model_boundary=APPROVED_CPU_MODEL_BOUNDARY)
    try:
        outcome = runtime.run_public_transform(
            request_path, bundle_path, out=tmp_path / "public-transform", key="h3-character-swap-cpu-boundary",
        )
        assert outcome.ok, outcome.error
        rows = paged_rows(runtime.owner.tasks.list, runtime.project_id, limit=100)
        assert rows is not None
        tasks = list(rows)
        capabilities = [_field(task, "capability_id") for task in tasks]
        for expected in (
            "h3_av.prepare", "h3_av.compile", "vibecomfy.validate", "vibecomfy.run",
            "h3_av.compose", "h3_av.verify", "h3_av.publication_finalizer",
        ):
            assert expected in capabilities
        boundary = runtime.read_cpu_model_boundary_evidence()
        assert boundary["schema_version"] == "h3-character-swap-cpu-boundary.v2"
        assert boundary["synthetic_inference"] is True
        assert boundary["queued_to_comfy"] is False
        assert boundary["production_model_bytes_observed"] is False
        assert boundary["task_id"] and boundary["attempt_id"] and boundary["execution_id"]
        assert boundary["child_pid"] != os.getpid()
        marker = boundary["activation_marker"]
        assert marker["schema_version"] == "h3-t9-child-activation.v1"
        assert marker["child_pid"] == boundary["child_pid"]
        assert marker["task_id"] == boundary["task_id"]
        assert marker["attempt_id"] == boundary["attempt_id"]
        assert marker["execution_id"] == boundary["execution_id"]
        assert marker["synthetic_inference"] is True
        assert marker["queued_to_comfy"] is False
        assert marker["production_model_bytes_observed"] is False
        assert marker["profile_sha256"] == runtime.readiness_profile_hash
        assert marker["candidate_manifest_sha256"] == "sha256:" + hashlib.sha256(
            runtime.candidate_manifest_path.read_bytes()
        ).hexdigest()
        calls = [
            json.loads(line)
            for line in runtime.t9_child_calls_path.read_text(encoding="utf-8").splitlines()
            if line
        ]
        assert any(
            call.get("task_id") == boundary["task_id"]
            and call.get("attempt_id") == boundary["attempt_id"]
            and call.get("execution_id") == boundary["execution_id"]
            and call.get("child_pid") == boundary["child_pid"]
            and call.get("evidence_path") == boundary["evidence_path"]
            for call in calls
        )
        for output in boundary["outputs"]:
            output_path = Path(output["path"])
            assert output_path.is_file() and not output_path.is_symlink()
            assert hashlib.sha256(output_path.read_bytes()).hexdigest() == output["sha256"]
        observed = {row["member"]: row["sha256"] for row in boundary["managed_inputs"]}
        for name in ("performance.mp4", "replacement.png"):
            assert input_digests[name] in observed.values()
        finalizer = next(task for task in tasks if _field(task, "capability_id") == "h3_av.publication_finalizer")
        finalizer_result = _field(finalizer, "result", {}) or {}
        outputs = _field(finalizer_result, "outputs", [])
        assert any(row.get("name") == "verified_candidate" for row in outputs if isinstance(row, dict))
    finally:
        runtime.close()

    workspace_provenance = json.loads(
        runtime.public_workspace_provenance_path.read_text(encoding="utf-8")
    )
    assert workspace_provenance["profile"] == "astrid"
    assert workspace_provenance["candidate_manifest_sha256"]
    assert "execution_target" not in workspace_provenance
    assert workspace_provenance["synthetic_inference"] is True
    assert workspace_provenance["stop"]["owner_stopped"] is True
    assert workspace_provenance["stop"]["runtime_pid"] == workspace_provenance["runtime_pid"]


def test_candidate_manifest_resolves_from_environment_without_runtime_startup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.helpers.h3_cpu_runtime import (
        CANDIDATE_SOURCE_MANIFEST_SCHEMA,
        candidate_manifest_path_from_environment,
    )

    manifest_path = tmp_path / "candidate.json"
    manifest_path.write_text(json.dumps({
        "schema": CANDIDATE_SOURCE_MANIFEST_SCHEMA,
        "synthetic_inference": True,
        "synthetic_inference_classification": "synthetic-inference-only",
    }), encoding="utf-8")
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", str(manifest_path))

    assert candidate_manifest_path_from_environment() == manifest_path.resolve()


@pytest.mark.parametrize("bad_value", [None, "relative-candidate.json"])
def test_candidate_manifest_rejects_missing_or_relative_environment_path(
    bad_value: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.helpers.h3_cpu_runtime import candidate_manifest_path_from_environment

    if bad_value is None:
        monkeypatch.delenv("ASTRID_H3_CANDIDATE_MANIFEST", raising=False)
    else:
        monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", bad_value)

    with pytest.raises(RuntimeError, match="ASTRID_H3_CANDIDATE_MANIFEST"):
        candidate_manifest_path_from_environment()


def test_candidate_manifest_rejects_symlink_environment_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.helpers.h3_cpu_runtime import candidate_manifest_path_from_environment

    target = tmp_path / "target.json"
    target.write_text(json.dumps({
        "schema": "astrid-h3-candidate-source-manifest/v1",
        "synthetic_inference": True,
        "synthetic_inference_classification": "synthetic-inference-only",
    }), encoding="utf-8")
    link = tmp_path / "candidate-link.json"
    link.symlink_to(target)
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", str(link))

    with pytest.raises(RuntimeError, match="non-symlink"):
        candidate_manifest_path_from_environment()


def test_candidate_manifest_reaches_declared_orchestrator_child_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import yaml

    from astrid.core.subprocess_env import build_child_subprocess_env

    checkout = Path(__file__).resolve().parents[3]
    orchestrator_path = checkout / "astrid/packs/h3_av/orchestrators/transform/orchestrator.yaml"
    compile_path = checkout / "astrid/packs/h3_av/executors/compile/executor.yaml"
    orchestrator = yaml.safe_load(orchestrator_path.read_text(encoding="utf-8"))
    compile_executor = yaml.safe_load(compile_path.read_text(encoding="utf-8"))
    allowed = orchestrator["isolation"]["env_passthrough"]
    compile_allowed = compile_executor["isolation"]["env_passthrough"]
    assert "ASTRID_H3_CANDIDATE_MANIFEST" in allowed
    assert "ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE" in allowed
    assert "ASTRID_H3_CANDIDATE_MANIFEST" in compile_allowed
    assert "ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE" in compile_allowed
    assert "BANODOCO_LOCAL_DATA_ROOT" in allowed
    assert "*" not in allowed
    assert "*" not in compile_allowed

    candidate = "/tmp/selected-h3-candidate.json"
    model_profile = "/tmp/selected-t9-model-substitute.json"
    support = "/tmp/selected-support-root"
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", candidate)
    monkeypatch.setenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", model_profile)
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", support)
    monkeypatch.setenv("ASTRID_H3_UNDECLARED_TEST_VALUE", "must-not-cross")
    child_env = build_child_subprocess_env(
        base=os.environ,
        parent={},
        passthrough=allowed,
        declared_passthrough=allowed,
    )
    compile_child_env = build_child_subprocess_env(
        base=os.environ,
        parent={},
        passthrough=compile_allowed,
        declared_passthrough=compile_allowed,
    )

    assert child_env["ASTRID_H3_CANDIDATE_MANIFEST"] == candidate
    assert child_env["ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"] == model_profile
    assert compile_child_env["ASTRID_H3_CANDIDATE_MANIFEST"] == candidate
    assert compile_child_env["ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"] == model_profile
    assert child_env["BANODOCO_LOCAL_DATA_ROOT"] == support
    assert "ASTRID_H3_UNDECLARED_TEST_VALUE" not in child_env


def test_character_swap_digest_override_is_source_and_inventory_bound(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from astrid.packs.h3_av.src import generation

    production_digest = generation.CHARACTER_SWAP_SHA256
    assert production_digest == "4b2a3f420ae804c0aa3422761ff84dbd1bf52eef6900ffab6d2e66df63cb4e79"
    monkeypatch.delenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", raising=False)
    assert generation.character_swap_asset_sha256() == production_digest

    checkout = Path(__file__).resolve().parents[3]
    fixture_relative = "tests/fixtures/h3_cpu/approved_character_swap_cpu_boundary.py"
    source_relatives = (
        fixture_relative,
        "astrid/packs/vibecomfy/executors/run/run.py",
        "astrid/packs/vibecomfy/executors/run/executor.yaml",
        "astrid/packs/h3_av/src/generation.py",
        "astrid/packs/h3_av/src/compile.py",
    )
    source_files = {
        relative: hashlib.sha256((checkout / relative).read_bytes()).hexdigest()
        for relative in source_relatives
    }
    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(json.dumps({
        "schema": "astrid-h3-candidate-source-manifest/v1",
        "synthetic_inference": True,
        "synthetic_inference_classification": "synthetic-inference-only",
        "source_files": source_files,
    }, sort_keys=True), encoding="utf-8")

    model_root = tmp_path / "models"
    model_path = model_root / "loras" / generation.CHARACTER_SWAP_FILENAME
    model_path.parent.mkdir(parents=True)
    model_path.write_bytes(b"source-bound synthetic Character Swap model")
    model_digest = "sha256:" + hashlib.sha256(model_path.read_bytes()).hexdigest()
    model_asset = {
        "name": generation.CHARACTER_SWAP_FILENAME,
        "subdir": "loras",
        "sha256": model_digest,
        "size": model_path.stat().st_size,
    }
    from astrid.core.generation.model_root import canonical_model_inventory_digest

    bound_model_root = {
        "schema_version": 1,
        "path": str(model_root.resolve()),
        "inventory": [model_asset],
        "inventory_digest": canonical_model_inventory_digest([model_asset]),
        "qualification_identity": None,
    }
    fixture_path = checkout / fixture_relative
    evidence_root = tmp_path / "t9-child-evidence"
    evidence_root.mkdir(mode=0o700)
    marker_base = evidence_root / "activation-marker.json"
    calls_path = evidence_root / "calls.jsonl"
    evidence_base = evidence_root / "output-evidence.json"
    profile_path = tmp_path / "t9-model-substitute.json"
    profile_path.write_text(json.dumps({
        "schema_version": "hc03-worker-readiness.v1",
        "status": "ready",
        "launch": {
            "model_root": bound_model_root,
        },
        "t9_model_substitute": {
            "approved": True,
            "mode": "deterministic_cpu_model_boundary_v1",
            "purpose": "h3_character_swap_public_runtime_cpu_acceptance_v1",
            "candidate_manifest_path": str(candidate_path.resolve()),
            "candidate_manifest_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "source_path": str(fixture_path.resolve()),
            "source_sha256": "sha256:" + source_files[fixture_relative],
            "model_asset": model_asset,
            "activation_marker_path": str(marker_base),
            "calls_path": str(calls_path),
            "evidence_path": str(evidence_base),
        },
    }, sort_keys=True), encoding="utf-8")
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", str(candidate_path))
    monkeypatch.setenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", str(profile_path))

    assert generation.character_swap_asset_sha256() == model_digest.removeprefix("sha256:")

    workflow = generation.build_generation_workflow(
        references=["replacement.png"],
        prompt="Keep the replacement identity stable.",
        frames=24,
        model="minimax_h3_ref2va_pruned_int8_convrot.safetensors",
        steps=8,
        seed=1,
        adapter_strength=0.7,
        turbo_enabled=False,
        character_swap_sha256=model_digest.removeprefix("sha256:"),
    )
    adapter_rows = [
        row for row in workflow.metadata["model_assets"]
        if row.get("name") == generation.CHARACTER_SWAP_FILENAME
    ]
    assert len(adapter_rows) == 1
    assert adapter_rows[0]["sha256"] == model_digest.removeprefix("sha256:")
    assert adapter_rows[0]["hf_revision"] == generation.CHARACTER_SWAP_REVISION


def test_character_swap_digest_override_fails_closed_on_source_pin_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from astrid.packs.h3_av.src.generation import character_swap_asset_sha256

    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(json.dumps({
        "schema": "astrid-h3-candidate-source-manifest/v1",
        "synthetic_inference": True,
        "synthetic_inference_classification": "synthetic-inference-only",
        "source_files": {
            "tests/fixtures/h3_cpu/approved_character_swap_cpu_boundary.py": "0" * 64,
        },
    }), encoding="utf-8")
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps({
        "schema_version": "hc03-worker-readiness.v1",
        "status": "ready",
        "t9_model_substitute": {
            "approved": True,
            "mode": "deterministic_cpu_model_boundary_v1",
            "purpose": "h3_character_swap_public_runtime_cpu_acceptance_v1",
            "candidate_manifest_path": str(candidate_path.resolve()),
            "candidate_manifest_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        },
    }), encoding="utf-8")
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", str(candidate_path))
    monkeypatch.setenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", str(profile_path))

    with pytest.raises(ValueError, match="fixture source does not match"):
        character_swap_asset_sha256()


def test_character_swap_digest_override_rejects_production_classification(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from astrid.packs.h3_av.src.generation import character_swap_asset_sha256

    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(json.dumps({
        "schema": "astrid-h3-candidate-source-manifest/v1",
        "synthetic_inference": False,
        "synthetic_inference_classification": "production-inference",
        "source_files": {},
    }), encoding="utf-8")
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps({
        "schema_version": "hc03-worker-readiness.v1",
        "status": "ready",
        "t9_model_substitute": {
            "approved": True,
            "mode": "deterministic_cpu_model_boundary_v1",
            "purpose": "h3_character_swap_public_runtime_cpu_acceptance_v1",
            "candidate_manifest_path": str(candidate_path.resolve()),
            "candidate_manifest_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        },
    }), encoding="utf-8")
    monkeypatch.setenv("ASTRID_H3_CANDIDATE_MANIFEST", str(candidate_path))
    monkeypatch.setenv("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", str(profile_path))

    with pytest.raises(ValueError, match="synthetic-only"):
        character_swap_asset_sha256()
