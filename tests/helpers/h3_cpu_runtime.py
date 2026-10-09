"""Derived fixture-owned Runtime and VibeComfy harness for H3 CPU evidence.

Behavioral source: candidate-reference/d6/tests/helpers/h3_cpu_runtime.py,
SHA-256 9ff48550d4cdf1547bc10e58c5677b9606b35bb25988bef6259530b51cccc48e.
Its pinned installed/runtime tuple is retained as a prerequisite and is not
qualified for this integration checkout by this file's presence.
"""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import io
import tarfile
import uuid
from typing import Any, Mapping

ASTRID_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = ASTRID_ROOT.parents[2]
RECEIVING_ROOT = ASTRID_ROOT.parents[1]
RUNTIME_ROOT = Path(
    os.environ.get("ASTRID_STAGE1_RUNTIME_CHECKOUT")
    or RECEIVING_ROOT / "checkouts" / "banodoco-workspace-runtime--integration"
).resolve()
VIBECOMFY_ROOT = Path(
    os.environ.get("ASTRID_VIBECOMFY_CHECKOUT") or RECEIVING_ROOT / "repos" / "vibecomfy"
).resolve()
VIBECOMFY_SOURCE_ROOT = VIBECOMFY_ROOT
# The derived candidate must launch the VibeComfy revision selected by this
# Astrid integration checkout. The older pinned revision below describes only
# the preserved H3 object_info capture, not the runtime dependency.
PINNED_VIBECOMFY_REVISION = "31f90bb03d330283b76e7dbdda51197be787090d"
H3_SCHEMA_CAPTURE_VIBECOMFY_REVISION = "01f38461d633651c8857712b2331650aedaee461"
BEHAVIORAL_SOURCE_SHA256 = "9ff48550d4cdf1547bc10e58c5677b9606b35bb25988bef6259530b51cccc48e"
H3_RUNPOD_SCHEMA_SHA256 = "1133daa166d646db626e05d9aba1c8d5b689fa0a19216e3d10ea08e7a9fb6810"
H3_RUNPOD_GRAPH_CLOSURE_SHA256 = "af9271339890a3dcc36f1068a51eadb4f5a3ccb67652e7ec63c3ec41926b0e55"
H3_RUNPOD_OVERLAY_SHA256 = "50f38e439f2c3945f0fad13b11e565defb72433aabd92fe9d0dd379a014bd020"
APPROVED_CPU_MODEL_BOUNDARY = "approved_t9_v1"
CPU_MODEL_BOUNDARY_PURPOSE = "h3_character_swap_public_runtime_cpu_acceptance_v1"
H3_REQUIRED_OBJECT_INFO_CLASSES = frozenset(
    {
        "MiniMaxH3AVExtensionController",
        "MiniMaxH3AVSourceAudioModeParam",
        "MiniMaxH3AVStartModeParam",
        "MiniMaxH3AudioVAECompatibility",
        "MiniMaxH3CropTo32",
        "MiniMaxH3CustomKeyframes",
        "MiniMaxH3FinalizeVHSOutput",
        "MiniMaxH3GeneratedAVMaskedContext",
        "MiniMaxH3LastActiveVHSPreviewBarrier",
        "MiniMaxH3SourceAudioPolicy",
        "MiniMaxH3SourceAudioRegenLength",
        "MiniMaxH3SourceAudioRegenMask",
        "MiniMaxH3StartCanvasSelector",
        "MiniMaxH3StartMaskedContext",
        "MiniMaxH3StreamLiveExtensionAVToVHS",
        "MiniMaxH3Validate24FPSVideo",
    }
)
H3_GRAPH_CLOSURE_CLASSES = H3_REQUIRED_OBJECT_INFO_CLASSES | frozenset(
    {"MiniMaxH3ReferenceToVideo", "MiniMaxH3SigmaShift"}
)
T9_PROFILE = (
    Path(os.environ.get("ASTRID_H3_T9_READINESS_PROFILE"))
    if os.environ.get("ASTRID_H3_T9_READINESS_PROFILE")
    else RECEIVING_ROOT
    / "repos"
    / "Astrid"
    / ".otto"
    / "runs"
    / "h3-transform-pack-20260923"
    / "fixtures"
    / "t9-public-h3-20260925-9"
    / "support"
    / "runtime"
    / "t9-vibecomfy-readiness.json"
)
PUBLIC_WORKSPACE_FIXTURE = (
    RECEIVING_ROOT
    / "receiving"
    / "coordination"
    / "evidence"
    / "B"
    / "shared-public-workspace-fixture"
    / "public_workspace.py"
)
PUBLIC_WORKSPACE_FIXTURE_SHA256 = "5ec4cf02b2f72e571670c8aad26fa406d545551a1b8c6adc76945fe10c62a722"
PUBLIC_WORKSPACE_SOURCE_PROFILE = (
    RECEIVING_ROOT
    / "receiving"
    / "coordination"
    / "evidence"
    / "B"
    / "shared-public-workspace-fixture"
    / "astrid-integration-h3-v22-source-profile.json"
)
CANDIDATE_SOURCE_MANIFEST_SCHEMA = "astrid-h3-candidate-source-manifest/v1"


def candidate_manifest_path_from_environment(
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Resolve the explicitly selected candidate manifest before Runtime startup."""
    source = os.environ if environ is None else environ
    raw = source.get("ASTRID_H3_CANDIDATE_MANIFEST")
    if not isinstance(raw, str) or not raw:
        raise RuntimeError("ASTRID_H3_CANDIDATE_MANIFEST is required")
    path = Path(raw)
    if not path.is_absolute():
        raise RuntimeError("ASTRID_H3_CANDIDATE_MANIFEST must be an absolute path")
    if path.is_symlink() or not path.is_file():
        raise RuntimeError("ASTRID_H3_CANDIDATE_MANIFEST must be a regular non-symlink file")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("ASTRID_H3_CANDIDATE_MANIFEST must contain valid JSON") from exc
    if not isinstance(manifest, Mapping) or manifest.get("schema") != CANDIDATE_SOURCE_MANIFEST_SCHEMA:
        raise RuntimeError("candidate manifest schema is not supported")
    if (manifest.get("synthetic_inference") is not True
            or manifest.get("synthetic_inference_classification") != "synthetic-inference-only"):
        raise RuntimeError("candidate manifest must explicitly classify inference as synthetic-only")
    if any(key in manifest for key in ("candidate_manifest_path", "candidate_manifest_sha256")):
        raise RuntimeError("candidate manifest must not self-pin its path or hash")
    return path.resolve(strict=True)

# Match host_bootstrap: the selected Astrid source owns the vendored client;
# Runtime implementation modules come from the explicitly selected checkout.
_import_roots = [str(root) for root in (ASTRID_ROOT, RUNTIME_ROOT, RUNTIME_ROOT / "packages" / "python")]
sys.path[:] = _import_roots + [path for path in sys.path if path not in _import_roots]

from astrid.core.execution.generic_host import RuntimeProtocolClient, source_checkout_digest  # noqa: E402
from astrid.core.generation.backends.vibecomfy import (  # noqa: E402
    _canonical_sha256,
    _owner_session_command,
    _session_registry_binding,
    _verify_owned_vibe_session,
)
from astrid.core.generation.model_root import (  # noqa: E402
    canonical_model_inventory_digest,
    validate_model_root_binding,
)
from astrid.core.pack.source_setup import active_source_inventory  # noqa: E402
from astrid.packs.h3_av.src.request import normalize_request  # noqa: E402
from astrid.packs.vibecomfy.asset_manifest import read_archive  # noqa: E402
from astrid.sdk.client import AstridClient  # noqa: E402
from astrid.sdk.host_bootstrap import PACK_HOST_ACTOR, PACK_HOST_SCOPES, ensure_pack_host  # noqa: E402
from astrid.sdk.workspace_client import SCHEMA_DIGEST  # noqa: E402


def _load_public_workspace_fixture():
    """Load the single B-owned public lifecycle fixture at its pinned bytes."""
    if PUBLIC_WORKSPACE_FIXTURE.is_symlink() or not PUBLIC_WORKSPACE_FIXTURE.is_file():
        raise RuntimeError("shared public workspace fixture is unavailable or symlinked")
    observed = hashlib.sha256(PUBLIC_WORKSPACE_FIXTURE.read_bytes()).hexdigest()
    if observed != PUBLIC_WORKSPACE_FIXTURE_SHA256:
        raise RuntimeError(
            "shared public workspace fixture changed; refresh the source pin before use"
        )
    name = "_astrid_h3_public_workspace_fixture"
    module = sys.modules.get(name)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location(name, PUBLIC_WORKSPACE_FIXTURE)
    if spec is None or spec.loader is None:
        raise RuntimeError("shared public workspace fixture cannot be imported")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def _synthetic_model_root_binding(models_root: Path, model_paths: tuple[str, ...]) -> dict[str, Any]:
    """Build the runtime's digest-bound model-root object for test-owned files."""
    root = models_root.resolve(strict=True)
    if models_root.is_symlink() or not root.is_dir():
        raise RuntimeError("synthetic H3 model root must be an existing, non-symlink directory")
    inventory: list[dict[str, Any]] = []
    for name in model_paths:
        relative = Path(name)
        if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
            raise RuntimeError(f"synthetic H3 model path is not a safe relative path: {name!r}")
        candidate = root / relative
        if candidate.is_symlink() or not candidate.is_file():
            raise RuntimeError(f"synthetic H3 model fixture is missing or aliased: {relative}")
        subdir = relative.parent.as_posix()
        inventory.append({
            "name": relative.name,
            "sha256": "sha256:" + hashlib.sha256(candidate.read_bytes()).hexdigest(),
            "size": candidate.stat().st_size,
            "subdir": "" if subdir == "." else subdir,
        })
    inventory.sort(key=lambda entry: (entry["subdir"], entry["name"]))
    payload = {
        "schema_version": 1,
        "path": str(root),
        "inventory": inventory,
        "inventory_digest": canonical_model_inventory_digest(inventory),
        "qualification_identity": None,
    }
    validate_model_root_binding(payload, verify_files=True)
    return payload


def _public_workspace_environment() -> dict[str, str]:
    """Keep stale or checkout-injected authority out of the public CLI child."""
    environment = dict(os.environ)
    for key in (
        "ASTRID_HOST_READINESS_PROFILE_HASH",
        "ASTRID_HOST_READINESS_PROFILE_PATH",
        "ASTRID_C11_EVIDENCE_PATH",
        "ASTRID_C11_EXPECTED_PATH",
        "ASTRID_C11_SCHEMA_PATH",
        "ASTRID_C11_SESSION_DIR",
        "ASTRID_STAGE1_RUNTIME_CHECKOUT",
        "ASTRID_VIBECOMFY_CHECKOUT",
        "BANODOCO_LOCAL_DATA_ROOT",
        "BANODOCO_LOCAL_HOME",
        "BANODOCO_LOCAL_SOURCE_MANIFEST",
        "BANODOCO_RUNTIME_CREDENTIAL",
        "BANODOCO_RUNTIME_ENDPOINT",
        "PYTHONHOME",
        "PYTHONPATH",
    ):
        environment.pop(key, None)
    return environment


_SERVER_CODE = r"""
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import subprocess
import sys
import threading
import time

if sys.argv[1] == "serve":
    def option(name):
        return sys.argv[sys.argv.index(name) + 1]

    port = int(option("--port"))
    schema_path = Path(os.environ["ASTRID_C11_SCHEMA_PATH"])
    expected_path = Path(os.environ["ASTRID_C11_EXPECTED_PATH"])
    evidence_path = Path(os.environ["ASTRID_C11_EVIDENCE_PATH"])
    config = {
        "input_directory": option("--input-directory"),
        "output_directory": option("--output-directory"),
    }
else:
    port = int(sys.argv[1])
    schema_path = Path(sys.argv[2])
    config_path = Path(sys.argv[3])
    expected_path = Path(sys.argv[4])
    evidence_path = Path(sys.argv[5])
    config = json.loads(config_path.read_text(encoding="utf-8"))
schema = json.loads(schema_path.read_text(encoding="utf-8"))
input_directory = Path(config["input_directory"])
output_directory = Path(config["output_directory"])
session_dir = Path(os.environ["ASTRID_C11_SESSION_DIR"]) if os.environ.get("ASTRID_C11_SESSION_DIR") else None
histories = {}
queue_lock = threading.Lock()

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def respond(self, status, payload):
        body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        # Let the client close first so the fixed fixture port is available
        # when the owner immediately restarts this session.
        self.close_connection = False

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/view":
            try:
                query = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=True)
            except ValueError:
                self.send_error(400)
                return
            if set(query) != {"filename", "subfolder", "type"} or any(
                len(values) != 1 for values in query.values()
            ):
                self.send_error(400)
                return
            filename = query["filename"][0]
            subfolder = query["subfolder"][0]
            media_type = query["type"][0]
            descriptor = {
                "filename": filename,
                "subfolder": subfolder,
                "type": media_type,
            }
            published = any(
                item == descriptor
                for history in histories.values()
                for output in history.get("outputs", {}).values()
                for key in ("gifs", "images")
                for item in output.get(key, [])
                if isinstance(item, dict)
            )
            if not published or media_type != "output":
                self.send_error(404)
                return
            relative = Path(subfolder) / filename
            if (
                not filename
                or Path(filename).name != filename
                or Path(filename).is_absolute()
                or any(part in {".", ".."} for part in relative.parts)
                or relative.is_absolute()
            ):
                self.send_error(400)
                return
            root = output_directory.resolve()
            candidate = output_directory / relative
            resolved = candidate.resolve(strict=False)
            try:
                resolved.relative_to(root)
            except ValueError:
                self.send_error(403)
                return
            if candidate.is_symlink() or not resolved.is_file():
                self.send_error(404)
                return
            try:
                body = resolved.read_bytes()
            except OSError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self.close_connection = False
            return
        if parsed.path == "/object_info" and not parsed.query:
            payload = schema
        elif parsed.path == "/system_stats" and not parsed.query:
            # ServerSession probes health before publishing pid. Once pid is
            # published, the owner CLI must wait for the subsequent source
            # attestation before it can declare the registry ready.
            if session_dir is not None and (session_dir / "pid").is_file():
                attestations = (session_dir / "source_revision", session_dir / "source_content_digest")
                deadline = time.monotonic() + 10
                while not all(path.is_file() and path.read_text(encoding="utf-8").strip() for path in attestations):
                    if time.monotonic() >= deadline:
                        self.send_error(503, "fixture owner source attestation was not published")
                        return
                    time.sleep(0.02)
            payload = {
                "system": {
                    "comfyui_version": "0.36.0",
                    "comfyui_frontend_package": "1.39.19",
                    "python_version": sys.version.split()[0],
                    "argv": ["h3-c11-fixture"],
                    "embedded_python": False,
                },
                "devices": [],
            }
        elif parsed.path.startswith("/history/") and not parsed.query:
            prompt_id = parsed.path.removeprefix("/history/")
            payload = {prompt_id: histories[prompt_id]} if prompt_id in histories else {}
        else:
            self.send_error(404)
            return
        self.respond(200, payload)

    def do_POST(self):
        if self.path in {"/queue", "/api/free", "/interrupt"}:
            with queue_lock:
                # The fixture completes generation before acknowledging
                # /prompt, so no active or pending work remains to release.
                self.respond(200, {"ok": True, "completed": True, "status": "completed"})
            return
        if self.path != "/prompt":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 2_000_000:
                raise ValueError("prompt body length is invalid")
            request = json.loads(self.rfile.read(length))
            prompt = request["prompt"]
            expected = json.loads(expected_path.read_text(encoding="utf-8"))
            if expected.get("character_swap") is True:
                video_loaders = [node for node in prompt.values()
                                 if node.get("class_type") == "VHS_LoadVideoFFmpeg"]
                image_loaders = [node for node in prompt.values()
                                 if node.get("class_type") == "LoadImage"]
                if len(video_loaders) != 1 or len(image_loaders) != 1:
                    raise ValueError("Character Swap fixture requires one managed video and image reference")
                checks = [
                    (video_loaders[0]["inputs"].get("video"), expected["video_reference_members"], "video"),
                    (image_loaders[0]["inputs"].get("image"), expected["image_reference_members"], "image"),
                ]
                for member, allowed, modality in checks:
                    if not isinstance(member, str) or Path(member).name != member or member not in allowed:
                        raise ValueError(f"compiled Character Swap {modality} differs from its managed reference")
                    staged = input_directory / member
                    if staged.is_symlink() or not staged.is_file():
                        raise ValueError(f"managed Character Swap {modality} is absent from input_directory")
                    record = expected["asset_files"][member]
                    if (hashlib.sha256(staged.read_bytes()).hexdigest() != record["sha256"]
                            or staged.stat().st_size != record["size"]):
                        raise ValueError(f"staged Character Swap {modality} differs from the input bundle")
            else:
                loader = prompt["99"]
                basename = loader["inputs"]["video"]
                if loader["class_type"] != "VHS_LoadVideoFFmpeg" or basename != expected["basename"]:
                    raise ValueError("compiled node 99 video differs from the managed source basename")
                if not isinstance(basename, str) or Path(basename).name != basename:
                    raise ValueError("compiled source video is not a basename")
                staged = input_directory / basename
                if staged.is_symlink() or not staged.is_file():
                    raise ValueError("managed source video is absent from configured input_directory")
                digest = hashlib.sha256(staged.read_bytes()).hexdigest()
                if digest != expected["sha256"] or staged.stat().st_size != expected["size"]:
                    raise ValueError("staged source video differs from the managed archive digest")
            sinks = [node_id for node_id, node in prompt.items()
                     if node.get("class_type") in {"MiniMaxH3StreamLiveExtensionAVToVHS", "VHS_VideoCombine"}]
            if len(sinks) != 1:
                raise ValueError("fixture requires exactly one declared H3 video sink")
            with queue_lock:
                prompt_id = f"h3-c11-fixture-{len(histories) + 1:04d}"
                filename = f"{prompt_id}.mp4"
                output = output_directory / filename
                duration = float(expected.get("generated_seconds", 13))
                subprocess.run([
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", f"color=c=red:s=64x64:r=24:d={duration}",
                    "-f", "lavfi", "-i", f"sine=frequency=880:sample_rate=48000:duration={duration}",
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(output),
                ], check=True, capture_output=True)
                histories[prompt_id] = {
                    "status": {"status_str": "success", "completed": True, "messages": []},
                    "outputs": {sinks[0]: {"gifs": [{
                        "filename": filename, "subfolder": "", "type": "output",
                    }]}},
                }
                evidence_path.write_text(json.dumps({
                    "prompt_id": prompt_id,
                    "node_id": "99",
                    "video": basename,
                    "sha256": digest,
                    "size": staged.stat().st_size,
                    "output_node": sinks[0],
                    "output_filename": filename,
                }, sort_keys=True), encoding="utf-8")
            self.respond(200, {"prompt_id": prompt_id, "number": len(histories), "node_errors": {}})
        except (KeyError, TypeError, ValueError, OSError, subprocess.CalledProcessError) as exc:
            self.respond(400, {"error": f"C11 fixture rejected prompt: {exc}"})

    def log_message(self, *_args):
        pass

ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
"""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _write_runtime_asset_map(archive: Any, out: Path) -> Path:
    """Materialize bundle members and write the public transform's asset_map input."""

    out.mkdir(parents=True, exist_ok=True)
    asset_root = out / "asset-map-assets"
    asset_root.mkdir(parents=True, exist_ok=True)
    asset_map: dict[str, str] = {}
    for row in archive.manifest["assets"]:
        member = Path(str(row["member"]))
        target = (asset_root / member).resolve()
        if not target.is_relative_to(asset_root.resolve()):
            raise RuntimeError("managed input bundle member escapes the asset-map staging directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.members[str(row["member"])])
        asset_map[str(row["binding"])] = str(target)
    asset_map_path = out / "asset-map.json"
    asset_map_path.write_text(json.dumps(asset_map, sort_keys=True), encoding="utf-8")
    return asset_map_path


def _prepare_clean_vibecomfy_checkout(root: Path) -> Path:
    """Materialize the pinned VibeComfy object into the fixture's temporary root.

    The configured source can be an object-only repository with no checked-out
    package files.  The exact pinned commit and the extracted package below are
    the relevant source checks; requiring a package in the source worktree
    rejects valid object stores before the pinned archive can be materialized.
    """
    source_root = VIBECOMFY_SOURCE_ROOT
    pinned_revision = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "--verify", f"{PINNED_VIBECOMFY_REVISION}^{{commit}}"],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    if pinned_revision != PINNED_VIBECOMFY_REVISION:
        raise RuntimeError(
            "C11 requires the pinned VibeComfy source revision "
            f"{PINNED_VIBECOMFY_REVISION}, got {pinned_revision}"
        )

    checkout = (root / "dependencies" / "vibecomfy").resolve()
    checkout.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "git",
            "clone",
            "--shared",
            "--quiet",
            "--no-checkout",
            str(source_root),
            str(checkout),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    archive_bytes = subprocess.check_output(
        ["git", "-C", str(checkout), "archive", pinned_revision], timeout=20,
    )
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
        archive.extractall(checkout, filter="data")
    subprocess.run(
        ["git", "-C", str(checkout), "update-ref", "--no-deref", "HEAD", pinned_revision],
        capture_output=True, text=True, check=True, timeout=20,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "read-tree", pinned_revision],
        capture_output=True, text=True, check=True, timeout=20,
    )
    actual_revision = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    branch = subprocess.run(
        ["git", "-C", str(checkout), "symbolic-ref", "--quiet", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    status = subprocess.run(
        ["git", "-C", str(checkout), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout
    if actual_revision != PINNED_VIBECOMFY_REVISION or branch.returncode == 0 or status:
        raise RuntimeError(
            "C11 VibeComfy clone is not a clean detached checkout: "
            f"revision={actual_revision!r}, branch={branch.stdout.strip()!r}, status={status!r}"
        )
    if not (checkout / "vibecomfy" / "__init__.py").is_file():
        raise RuntimeError(f"C11 VibeComfy clone has no package initializer: {checkout}")
    return checkout


def _vibecomfy_child_pythonpath(checkout: Path) -> str:
    """Return the explicit import roots for fixture-owned child processes."""
    child_paths = (
        ASTRID_ROOT,
        RUNTIME_ROOT,
        RUNTIME_ROOT / "packages" / "python",
        checkout.resolve(),
    )
    return os.pathsep.join(str(path) for path in child_paths)


def _vibecomfy_child_environment(
    checkout: Path,
    *,
    extra: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Build a child-only environment for the clean detached checkout."""
    environment = dict(os.environ)
    environment["ASTRID_VIBECOMFY_CHECKOUT"] = str(checkout.resolve())
    environment["PYTHONPATH"] = _vibecomfy_child_pythonpath(checkout)
    if extra:
        environment.update({str(key): str(value) for key, value in extra.items()})
    return environment


@contextmanager
def _temporary_environment(values: Mapping[str, str], *, remove: tuple[str, ...] = ()):
    """Temporarily expose exact child launch values without leaking them."""
    prior = {key: os.environ.get(key) for key in (*values, *remove)}
    try:
        for key in remove:
            os.environ.pop(key, None)
        os.environ.update({str(key): str(value) for key, value in values.items()})
        yield
    finally:
        for key, value in prior.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _probe_vibecomfy_checkout(checkout: Path) -> dict[str, str]:
    """Attest the selected package in a fresh child interpreter."""
    source = checkout.resolve()
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import json; from pathlib import Path; import vibecomfy; "
                "from vibecomfy.runtime.session import "
                "current_source_content_digest,current_source_revision; "
                "print(json.dumps({'origin':str(Path(vibecomfy.__file__).resolve()),"
                "'revision':current_source_revision(),"
                "'content_digest':current_source_content_digest()},sort_keys=True))"
            ),
        ],
        cwd=str(source),
        env=_vibecomfy_child_environment(source),
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if probe.returncode != 0:
        raise RuntimeError(
            "could not attest the selected clean VibeComfy checkout: "
            + probe.stderr[-2000:]
        )
    try:
        identity = json.loads(probe.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("clean VibeComfy checkout probe returned malformed evidence") from exc
    origin = Path(str(identity.get("origin", ""))).resolve()
    revision = str(identity.get("revision", ""))
    content_digest = str(identity.get("content_digest", ""))
    digest_hex = content_digest.removeprefix("sha256:")
    if (
        not origin.is_relative_to(source)
        or revision != PINNED_VIBECOMFY_REVISION
        or not content_digest.startswith("sha256:")
        or len(digest_hex) != 64
        or any(character not in "0123456789abcdef" for character in digest_hex)
    ):
        raise RuntimeError(
            "could not attest the selected clean VibeComfy checkout: "
            f"origin={origin!s}, revision={revision!r}, digest={content_digest!r}"
        )
    return {
        "origin": str(origin),
        "revision": revision,
        "content_digest": content_digest,
    }


def _object_info_from_checkout(checkout: Path) -> dict[str, Any]:
    cache_root = checkout.resolve() / "vibecomfy" / "porting" / "cache" / "object_info"
    index = json.loads((cache_root / "index.json").read_text(encoding="utf-8"))
    payloads: dict[str, dict[str, Any]] = {}
    result: dict[str, Any] = {}

    def normalize_row(row: Mapping[str, Any]) -> dict[str, Any]:
        normalized = dict(row)
        if "input" not in normalized and isinstance(normalized.get("inputs"), Mapping):
            normalized["input"] = normalized["inputs"]
        if "output" not in normalized and isinstance(normalized.get("outputs"), list):
            normalized["output"] = [
                [item.get("type", "*"), item.get("name", "output")]
                for item in normalized["outputs"]
                if isinstance(item, Mapping)
            ]
        normalized.pop("inputs", None)
        normalized.pop("outputs", None)
        return normalized

    def payload_for(path: Path) -> dict[str, Any]:
        filename = path.name
        if filename not in payloads:
            raw = json.loads(path.read_text(encoding="utf-8"))
            payloads[filename] = raw if isinstance(raw, dict) else {}
        return payloads[filename]

    for class_type, filename in sorted(index.items()):
        if not isinstance(class_type, str) or not isinstance(filename, str):
            continue
        pack_path = (cache_root / filename).resolve()
        if not pack_path.is_relative_to(cache_root.resolve()) or not pack_path.is_file():
            continue
        row = payload_for(pack_path).get(class_type)
        if isinstance(row, Mapping):
            # TargetSchemaProvider consumes the same per-node schema shape as
            # ComfyUI's /object_info endpoint; the payload comes from this
            # explicit dirty checkout's indexed schema corpus.
            result[class_type] = normalize_row(row)

    # The index is intentionally authoritative for its existing rows, but
    # source-derived cache payloads can contain real node metadata that was
    # omitted from that index.  Add those rows without inventing schemas or
    # allowing a fallback payload to replace an indexed row.
    for pack_path in sorted(cache_root.glob("*.json")):
        if pack_path.name in {"index.json", "provenance.json"}:
            continue
        resolved = pack_path.resolve()
        if not resolved.is_relative_to(cache_root.resolve()) or not resolved.is_file():
            continue
        for class_type, row in sorted(payload_for(resolved).items()):
            if isinstance(class_type, str) and isinstance(row, Mapping):
                result.setdefault(class_type, normalize_row(row))

    fixture_root = ASTRID_ROOT / "tests" / "fixtures" / "h3_cpu"
    legacy_artifact = json.loads(
        (fixture_root / "object_info_legacy_import.json").read_text(encoding="utf-8")
    )
    assert hashlib.sha256(_canonical_json(legacy_artifact)).hexdigest() == (
        "0539a41691a06eb4a5209a20c4dbcc0a860eb1e15e670dab76f28fe71cf5202d"
    )
    assert "ModelAttentionBackend" in legacy_artifact
    for class_type, row in sorted(legacy_artifact.items()):
        if isinstance(class_type, str) and isinstance(row, Mapping):
            result.setdefault(class_type, normalize_row(row))

    h3_artifact = json.loads(
        (fixture_root / "object_info_h3_runpod.json").read_text(encoding="utf-8")
    )
    provenance = json.loads(
        (fixture_root / "object_info_h3_runpod.provenance.json").read_text(encoding="utf-8")
    )
    h3_digest = hashlib.sha256(_canonical_json(h3_artifact)).hexdigest()
    assert h3_digest == H3_RUNPOD_SCHEMA_SHA256
    assert provenance["filtered_object_info_sha256"] == H3_RUNPOD_SCHEMA_SHA256
    assert provenance["raw_object_info_sha256"] == (
        "505f7c31ebea6a48ea3db3ef77184923a529a6073fd373f780d48f693463154b"
    )
    assert provenance["vibecomfy_revision"] == H3_SCHEMA_CAPTURE_VIBECOMFY_REVISION
    assert provenance["h3_pack"]["revision"] == (
        "361624fb406b63eb6694442eac6c895fc1533a70"
    )
    assert set(h3_artifact) == H3_REQUIRED_OBJECT_INFO_CLASSES
    assert provenance["required_class_count"] == len(H3_REQUIRED_OBJECT_INFO_CLASSES)
    assert set(provenance["required_classes"]) == H3_REQUIRED_OBJECT_INFO_CLASSES
    for class_type, row in sorted(h3_artifact.items()):
        if isinstance(class_type, str) and isinstance(row, Mapping):
            result.setdefault(class_type, normalize_row(row))

    closure_artifact = json.loads(
        (fixture_root / "object_info_h3_runpod_graph_closure.json").read_text(encoding="utf-8")
    )
    closure_provenance = json.loads(
        (fixture_root / "object_info_h3_runpod_graph_closure.provenance.json").read_text(encoding="utf-8")
    )
    assert hashlib.sha256(_canonical_json(closure_artifact)).hexdigest() == (
        H3_RUNPOD_GRAPH_CLOSURE_SHA256
    )
    assert closure_provenance["filtered_object_info_sha256"] == H3_RUNPOD_GRAPH_CLOSURE_SHA256
    assert closure_provenance["parent_filtered_object_info_sha256"] == H3_RUNPOD_SCHEMA_SHA256
    assert closure_provenance["raw_object_info_sha256"] == provenance["raw_object_info_sha256"]
    assert closure_provenance["vibecomfy_revision"] == provenance["vibecomfy_revision"]
    assert closure_provenance["h3_pack"]["revision"] == provenance["h3_pack"]["revision"]
    assert set(closure_artifact) == H3_GRAPH_CLOSURE_CLASSES
    assert closure_provenance["required_class_count"] == len(H3_GRAPH_CLOSURE_CLASSES)
    assert set(closure_provenance["required_classes"]) == H3_GRAPH_CLOSURE_CLASSES
    assert set(closure_provenance["added_classes"]) == {
        "MiniMaxH3ReferenceToVideo",
        "MiniMaxH3SigmaShift",
    }
    for class_type, row in sorted(closure_artifact.items()):
        if isinstance(class_type, str) and isinstance(row, Mapping):
            result.setdefault(class_type, normalize_row(row))

    overlay_artifact = json.loads(
        (fixture_root / "object_info_h3_runpod_overlay.json").read_text(encoding="utf-8")
    )
    overlay_provenance = json.loads(
        (fixture_root / "object_info_h3_runpod_overlay.provenance.json").read_text(encoding="utf-8")
    )
    assert hashlib.sha256(_canonical_json(overlay_artifact)).hexdigest() == (
        H3_RUNPOD_OVERLAY_SHA256
    )
    assert set(overlay_artifact) == {"CLIPLoader"}
    assert overlay_provenance["filtered_object_info_sha256"] == H3_RUNPOD_OVERLAY_SHA256
    assert overlay_provenance["raw_object_info_sha256"] == (
        "505f7c31ebea6a48ea3db3ef77184923a529a6073fd373f780d48f693463154b"
    )
    assert overlay_provenance["filtered_closure_sha256"] == H3_RUNPOD_GRAPH_CLOSURE_SHA256
    assert overlay_provenance["vibecomfy_revision"] == H3_SCHEMA_CAPTURE_VIBECOMFY_REVISION
    assert overlay_provenance["h3_pack_revision"] == closure_provenance["h3_pack"]["revision"]
    assert overlay_provenance["comfy_revision"] == provenance["comfy_revision"]
    assert overlay_provenance["overlaid_class"] == "CLIPLoader"
    assert overlay_provenance["overlay_mode"] == "explicit_replace_after_cache_and_h3_closure"
    captured_clip_loader = overlay_artifact["CLIPLoader"]
    assert isinstance(captured_clip_loader, Mapping)
    result["CLIPLoader"] = dict(captured_clip_loader)
    assert result["CLIPLoader"] == captured_clip_loader
    clip_loader_choices = result["CLIPLoader"]["input"]["required"]["type"][0]
    assert "minimax" in clip_loader_choices
    return result


class ManagedSchemaSession:
    """A pinned VibeComfy owner session with a fixture-owned Comfy executable."""

    def __init__(
        self,
        root: Path,
        source_revision: str,
        source_digest: str,
        *,
        vibecomfy_checkout: Path,
    ) -> None:
        self.root = root.resolve()
        self.session_dir = self.root / "out" / "sessions" / "h3-c11"
        self.output_root = self.root / "output"
        self.input_root = self.root / "input"
        self.temp_root = self.root / "temp"
        for path in (self.output_root, self.input_root, self.temp_root):
            path.mkdir(parents=True)
        self.schema_path = self.root / "object-info.json"
        self.expected_path = self.root / "expected-source.json"
        self.queue_evidence_path = self.root / "queue-evidence.json"
        self.schema_path.write_bytes(
            _canonical_json(_object_info_from_checkout(vibecomfy_checkout))
        )
        executable_dir = self.root / "bin"
        executable_dir.mkdir(parents=True)
        executable = executable_dir / "comfyui"
        executable.write_text(f"#!{sys.executable}\n{_SERVER_CODE}", encoding="utf-8")
        executable.chmod(0o755)
        self.child_environment = _vibecomfy_child_environment(
            vibecomfy_checkout,
            extra={
                "PATH": str(executable_dir) + os.pathsep + os.environ.get("PATH", ""),
                "ASTRID_C11_SCHEMA_PATH": str(self.schema_path),
                "ASTRID_C11_EXPECTED_PATH": str(self.expected_path),
                "ASTRID_C11_EVIDENCE_PATH": str(self.queue_evidence_path),
                "ASTRID_C11_SESSION_DIR": str(self.session_dir),
            },
        )
        try:
            # vibecomfy.run's declared loopback network policy admits this port.
            port = 8188
            start = subprocess.run(
                [
                    sys.executable, "-m", "vibecomfy.cli", "--quiet", "session", "start",
                    "--id", self.session_dir.name, "--runtime-root", str(self.root),
                    "--port", str(port), "--ready-timeout-sec", "20",
                    "--input-directory", str(self.input_root),
                    "--output-directory", str(self.output_root),
                    "--temp-directory", str(self.temp_root),
                ],
                env=self.child_environment,
                capture_output=True, text=True, timeout=35,
            )
            if start.returncode != 0:
                log = self.session_dir / "daemon.log"
                detail = log.read_text(encoding="utf-8") if log.is_file() else start.stderr
                raise RuntimeError(f"managed schema session failed to start: {detail[-2000:]}")
            binding = self.registry_binding()
            self.server_url = binding["server_url"]
            self.pid = binding["pid"]
            self.comfy_pid = binding["comfy_pid"]
            _verify_owned_vibe_session(self.session_dir, self.pid)
            # The CLI can observe pid/url readiness just before the daemon
            # finishes publishing its source attestation files.
            source_paths = (self.session_dir / "source_revision", self.session_dir / "source_content_digest")
            deadline = time.monotonic() + 15
            while not all(path.is_file() for path in source_paths):
                if time.monotonic() >= deadline:
                    raise RuntimeError("managed schema session did not publish source attestation")
                time.sleep(0.05)
            config_bytes = (self.session_dir / "config.json").read_bytes()
            config = json.loads(config_bytes)
            if (
                config["runtime_root"] != str(self.root)
                or config["input_directory"] != str(self.input_root)
                or config["output_directory"] != str(self.output_root)
                or config["temp_directory"] != str(self.temp_root)
                or config["port"] != port
            ):
                raise RuntimeError("managed schema session configuration differs from its fixture roots")
            observed_revision = (self.session_dir / "source_revision").read_text(encoding="utf-8").strip()
            observed_digest = (self.session_dir / "source_content_digest").read_text(encoding="utf-8").strip()
            if (observed_revision, observed_digest) != (source_revision, source_digest):
                raise RuntimeError("managed schema session source identity differs from pinned checkout")
            self.session_binding = {
                "session_dir": str(self.session_dir),
                **binding,
                "source_revision": observed_revision,
                "source_content_digest": observed_digest,
                "config_digest": "sha256:" + hashlib.sha256(config_bytes).hexdigest(),
            }
        except BaseException:
            self.close()
            raise

    def registry_binding(self) -> dict[str, Any]:
        return _session_registry_binding(self.session_dir)

    def close(self) -> None:
        if (self.session_dir / "pid").is_file():
            stop = subprocess.run(
                _owner_session_command(self.session_dir, "stop"),
                env=self.child_environment,
                capture_output=True, text=True, timeout=20,
            )
            if stop.returncode != 0:
                raise RuntimeError(f"managed schema session stop failed: {stop.stderr}")
        if (self.session_dir / "pid").exists() or (self.session_dir / "comfy_pid").exists():
            raise RuntimeError("managed schema session owner did not clear its process registry")


class H3CpuRuntime:
    """Public Runtime workspace, ordinary pack host, and fixture Vibe session."""

    def __init__(self, root: Path, *, cpu_model_boundary: str | None = None,
                 source_capsule: Path | None = None) -> None:
        candidate_manifest = candidate_manifest_path_from_environment()
        self.candidate_manifest_path = candidate_manifest
        # Use the real producer's custody gate before creating any Runtime,
        # session or host. Never substitute a successful source measurement.
        self.source_identity = None
        if source_capsule is not None:
            from scripts.run_h3_canonical_on_runpod import assert_product_source_identity

            self.source_identity = assert_product_source_identity(capsule=source_capsule)
        if cpu_model_boundary not in {None, APPROVED_CPU_MODEL_BOUNDARY}:
            raise ValueError(f"unsupported CPU model boundary: {cpu_model_boundary!r}")
        if not RUNTIME_ROOT.is_dir():
            raise RuntimeError(f"Runtime checkout is unavailable: {RUNTIME_ROOT}")
        if not T9_PROFILE.is_file():
            raise RuntimeError(f"approved T9 readiness profile is unavailable: {T9_PROFILE}")
        if not VIBECOMFY_SOURCE_ROOT.is_dir():
            raise RuntimeError(f"VibeComfy source checkout is unavailable: {VIBECOMFY_SOURCE_ROOT}")
        self.root = root.resolve()
        self.cpu_model_boundary = cpu_model_boundary
        self.t9_child_evidence_root = self.root / "t9-child-evidence"
        self.t9_activation_marker_base_path = self.t9_child_evidence_root / "activation-marker.json"
        self.t9_child_calls_path = self.t9_child_evidence_root / "calls.jsonl"
        self.cpu_model_boundary_evidence_path = self.t9_child_evidence_root / "output-evidence.json"
        self._last_cpu_model_boundary_evidence_path: Path | None = None
        self._prior_sys_path = tuple(sys.path)
        self._prior_environment = {
            key: os.environ.get(key)
            for key in (
                "ASTRID_C11_EVIDENCE_PATH",
                "ASTRID_C11_EXPECTED_PATH",
                "ASTRID_C11_SCHEMA_PATH",
                "ASTRID_C11_SESSION_DIR",
                "ASTRID_STAGE1_RUNTIME_CHECKOUT",
                "ASTRID_HOST_READINESS_PROFILE_HASH",
                "ASTRID_HOST_READINESS_PROFILE_PATH",
                "ASTRID_VIBECOMFY_CHECKOUT",
                "ASTRID_H3_CANDIDATE_MANIFEST",
                "ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE",
                "BANODOCO_LOCAL_DATA_ROOT",
                "BANODOCO_LOCAL_HOME",
                "BANODOCO_LOCAL_SOURCE_MANIFEST",
                "BANODOCO_RUNTIME_CREDENTIAL",
                "BANODOCO_RUNTIME_ENDPOINT",
                "PATH",
                "PYTHONPATH",
            )
        }
        self._prior_vibecomfy_modules = {
            name: module
            for name, module in sys.modules.items()
            if name == "vibecomfy" or name.startswith("vibecomfy.")
        }
        self._closed = False
        self.public_workspace = None
        self.schema_session: ManagedSchemaSession | None = None
        self.owner: AstridClient | None = None
        self.host: Mapping[str, Any] | None = None
        self.host_pid: int | None = None
        self.host_state_path: Path | None = None
        self.host_errors: list[BaseException] = []
        self.worker_credential_file: Path | None = None
        self.public_workspace_provenance_path = self.root / "public-workspace-provenance.json"
        try:
            self.vibecomfy_root = _prepare_clean_vibecomfy_checkout(self.root)
            if not self.vibecomfy_root.is_relative_to(self.root):
                raise RuntimeError("C11 VibeComfy checkout escaped the fixture temporary root")
            self.vibecomfy_source_identity = _probe_vibecomfy_checkout(
                self.vibecomfy_root
            )
            source_revision = self.vibecomfy_source_identity["revision"]
            source_digest = self.vibecomfy_source_identity["content_digest"]
            self.data_root = (self.root / "runtime-data").resolve()
            self.support_root = self.data_root / "runtime"
            self.root.mkdir(parents=True, exist_ok=True)
            fixture = _load_public_workspace_fixture()
            self.public_workspace = fixture.start_public_workspace(
                python=Path(sys.executable),
                env=_public_workspace_environment(),
                home=self.root / "public-home",
                support_root=self.data_root,
                realm_root=self.root / "realm",
                source_manifest=PUBLIC_WORKSPACE_SOURCE_PROFILE,
                candidate_manifest=candidate_manifest,
                realm_id="h3-cpu-" + uuid.uuid4().hex,
                display_name="H3 Disposable CPU Qualification",
            )
            self.runtime_endpoint = self.public_workspace.endpoint
            self.runtime_instance_id = str(
                self.public_workspace.discovery.get("runtime_instance_id") or ""
            )
            if not self.runtime_instance_id:
                raise RuntimeError("public workspace discovery omitted the Runtime instance identity")
            owner_record = json.loads(
                self.public_workspace.credential_file.read_text(encoding="utf-8")
            )
            if (
                not isinstance(owner_record, Mapping)
                or owner_record.get("scope") != "astrid"
                or owner_record.get("actor_id") != self.public_workspace.actor_id
                or not isinstance(owner_record.get("token"), str)
                or not owner_record["token"].strip()
            ):
                raise RuntimeError("public workspace owner credential does not match its advertised actor")
            owner_record["token"] = ""
            self.owner = AstridClient.open(
                endpoint=self.runtime_endpoint,
                credential=self.public_workspace.credential_file,
                realm_id=self.public_workspace.realm_id,
                actor_id=self.public_workspace.actor_id,
                client_name="h3-av-c11-cpu-e2e",
                client_version="1",
                protocol_version="workspace.v1",
            )
            worker_value = self.public_workspace.up_result
            worker_path_text = str(
                worker_value.get("worker_credential_file")
                or self.public_workspace.discovery.get("worker_credential_file")
                or ""
            )
            self.worker_credential_file = Path(worker_path_text)
            worker_actor = str(
                worker_value.get("worker_actor")
                or self.public_workspace.discovery.get("worker_actor")
                or ""
            )
            worker_scopes = tuple(
                str(scope)
                for scope in (
                    worker_value.get("worker_scopes")
                    or self.public_workspace.discovery.get("worker_scopes")
                    or ()
                )
            )
            expected_worker_root = self.support_root / "credentials"
            if (
                not self.worker_credential_file.is_absolute()
                or self.worker_credential_file.is_symlink()
                or self.worker_credential_file.parent != expected_worker_root
                or not self.worker_credential_file.is_file()
                or self.worker_credential_file.stat().st_mode & 0o777 != 0o600
                or worker_actor != PACK_HOST_ACTOR
                or worker_scopes != PACK_HOST_SCOPES
            ):
                raise RuntimeError("public workspace worker handoff differs from the pack-host credential contract")
            worker_token = self.worker_credential_file.read_text(encoding="utf-8").strip()
            if not worker_token:
                raise RuntimeError("public workspace worker credential is empty")
            worker_client = RuntimeProtocolClient(self.runtime_endpoint, worker_token)
            health = worker_client.health()
            health_value = dict(health) if isinstance(health, Mapping) else {
                "status": getattr(health, "status", None),
                "runtime_instance_id": getattr(health, "runtime_instance_id", None),
                "runtime_epoch": getattr(health, "runtime_epoch", None),
                "runtime_session_id": getattr(health, "runtime_session_id", None),
                "schema_digest": getattr(health, "schema_digest", None),
            }
            runtime_epoch = health_value.get("runtime_epoch")
            schema_digest = str(health_value.get("schema_digest") or "")
            runtime_session_id = str(health_value.get("runtime_session_id") or "")
            if (
                health_value.get("status") != "ok"
                or str(health_value.get("runtime_instance_id") or "") != self.runtime_instance_id
                or isinstance(runtime_epoch, bool)
                or not isinstance(runtime_epoch, int)
                or runtime_epoch < 1
                or schema_digest != SCHEMA_DIGEST
                or not runtime_session_id
            ):
                raise RuntimeError(f"public Runtime health is not a valid bootstrap identity: {health_value!r}")
            self.public_workspace_health = {
                "status": "ok",
                "runtime_instance_id": self.runtime_instance_id,
                "runtime_epoch": runtime_epoch,
                "runtime_session_id": runtime_session_id,
                "schema_digest": schema_digest,
            }
            # Keep tokens short-lived in this test harness; the process receives
            # only the owner-only worker credential file, never the token value.
            worker_token = ""
            self.models_root = (self.data_root / "models").resolve()
            if self.models_root.is_symlink():
                raise RuntimeError("C11 model root must not be a symlink")
            self.models_root.mkdir(parents=True, exist_ok=True)
            model_paths = (
                "vae/minimax_h3_audio_vae_fp32.safetensors",
                "vae/minimax_h3_video_vae_int8_convrot.safetensors",
                "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
                "loras/h3_character_swap_pro4500_1000.safetensors",
                "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors",
                "text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors",
            )
            for relative in model_paths:
                model_path = self.models_root / relative
                model_path.parent.mkdir(parents=True, exist_ok=True)
                model_path.write_bytes(f"c11-model-fixture:{relative}\n".encode("utf-8"))
                if model_path.is_symlink() or not model_path.is_file() or model_path.stat().st_size == 0:
                    raise RuntimeError(f"C11 model fixture is not a regular non-empty file: {model_path}")
            # This is the normal unbound local pack-host path. It makes no
            # machine-placement claim; Worker-supervised placement is a
            # separate acceptance contract.
            self.schema_session = ManagedSchemaSession(
                self.root / "managed-session",
                source_revision,
                source_digest,
                vibecomfy_checkout=self.vibecomfy_root,
            )
            self.readiness_profile_path = self.support_root / "readiness-profile.json"
            approved = json.loads(T9_PROFILE.read_text(encoding="utf-8"))
            facts = {
                "exact": {
                    "interpreter": str(self.public_workspace.python),
                    "runtime_lock": "sha256:" + "1" * 64,
                    "engine_lock": "sha256:" + "2" * 64,
                    "model_digest": "sha256:" + "3" * 64,
                    "custom_node_digest": "sha256:" + "4" * 64,
                    "driver": "cpu-fixture",
                    "root": "sha256:" + "5" * 64,
                    "port": int(self.schema_session.server_url.rsplit(":", 1)[1]),
                },
                "minimum": {"vram_bytes": 1, "scratch_bytes": 1},
            }
            model_root_binding = _synthetic_model_root_binding(self.models_root, model_paths)
            profile = {
                **{key: value for key, value in approved.items() if key not in {"vibecomfy_candidate", "t9_model_substitute"}},
                "schema_version": "hc03-worker-readiness.v1",
                "status": "ready",
                "verified_facts": facts,
                "verified_facts_digest": _canonical_sha256(facts),
                "runtime": {
                    "runtime_instance_id": self.runtime_instance_id,
                    "comfyui_version": "==0.36.0",
                },
                "launch": {
                    "output_root": str(self.schema_session.output_root),
                    "model_root": model_root_binding,
                },
                "vibecomfy_candidate": {
                    "kind": "local_snapshot",
                    "checkout": str(self.vibecomfy_root),
                    "revision": source_revision,
                    "source_content_digest": source_digest,
                    "source_worktree_dirty": False,
                    "installation_mode": "explicit_checkout",
                },
                "vibecomfy_session": self.schema_session.session_binding,
            }
            if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY:
                boundary_source = (
                    ASTRID_ROOT / "tests" / "fixtures" / "h3_cpu"
                    / "approved_character_swap_cpu_boundary.py"
                ).resolve()
                if boundary_source.is_symlink() or not boundary_source.is_file():
                    raise RuntimeError("approved Character Swap CPU boundary source is unavailable")
                candidate_bytes = candidate_manifest.read_bytes()
                candidate_value = json.loads(candidate_bytes)
                source_files = candidate_value.get("source_files")
                fixture_relative = "tests/fixtures/h3_cpu/approved_character_swap_cpu_boundary.py"
                fixture_digest = hashlib.sha256(boundary_source.read_bytes()).hexdigest()
                if not isinstance(source_files, Mapping) or source_files.get(fixture_relative) != fixture_digest:
                    raise RuntimeError("selected candidate does not pin the approved T9 fixture source")
                executor_relatives = (
                    "astrid/packs/vibecomfy/executors/run/run.py",
                    "astrid/packs/vibecomfy/executors/run/executor.yaml",
                )
                for relative in executor_relatives:
                    executor_source = ASTRID_ROOT / relative
                    if (
                        executor_source.is_symlink()
                        or not executor_source.is_file()
                        or source_files.get(relative)
                        != hashlib.sha256(executor_source.read_bytes()).hexdigest()
                    ):
                        raise RuntimeError(f"selected candidate does not pin T9 executor source {relative}")
                model_rows = [
                    row for row in model_root_binding["inventory"]
                    if row.get("name") == "h3_character_swap_pro4500_1000.safetensors"
                    and row.get("subdir") == "loras"
                ]
                if len(model_rows) != 1:
                    raise RuntimeError("synthetic model root has no unique Character Swap LoRA")
                self.t9_child_evidence_root.mkdir(mode=0o700, parents=True, exist_ok=False)
                if self.t9_child_evidence_root.is_symlink() or not self.t9_child_evidence_root.is_dir():
                    raise RuntimeError("T9 child evidence directory is not a private case directory")
                profile["t9_model_substitute"] = {
                    "approved": True,
                    "mode": "deterministic_cpu_model_boundary_v1",
                    "purpose": CPU_MODEL_BOUNDARY_PURPOSE,
                    "candidate_manifest_path": str(candidate_manifest.resolve(strict=True)),
                    "candidate_manifest_sha256": hashlib.sha256(candidate_bytes).hexdigest(),
                    "source_path": str(boundary_source),
                    "source_sha256": "sha256:" + fixture_digest,
                    "model_asset": model_rows[0],
                    "activation_marker_path": str(self.t9_activation_marker_base_path),
                    "calls_path": str(self.t9_child_calls_path),
                    "evidence_path": str(self.cpu_model_boundary_evidence_path),
                }
            self.readiness_profile_path.write_bytes(_canonical_json(profile))
            self.readiness_profile_hash = "sha256:" + hashlib.sha256(self.readiness_profile_path.read_bytes()).hexdigest()
            project = self.owner.projects.create(
                slug="h3-c11-cpu",
                name="H3 C11 CPU integrated evidence",
                idempotency_key="h3-c11-project",
            )
            if not project.ok:
                raise RuntimeError(f"could not create C11 fixture project: {project.error}")
            self.project_id = str(project.data["project_id"])
            self.project_slug = "h3-c11-cpu"
            inventory = active_source_inventory()
            if source_capsule is not None:
                self.source_identity = assert_product_source_identity(capsule=source_capsule)
            launcher_value = {
                "endpoint": self.runtime_endpoint,
                "worker_credential_file": str(self.worker_credential_file),
                "worker_actor": PACK_HOST_ACTOR,
                "worker_scopes": PACK_HOST_SCOPES,
                "runtime_instance_id": self.runtime_instance_id,
                "runtime_session_id": runtime_session_id,
                "runtime_epoch": runtime_epoch,
                "schema_digest": schema_digest,
                "source_checkout": str(ASTRID_ROOT.resolve()),
                "source_checkout_digest": (
                    self.source_identity["scoped_source_digest"] if self.source_identity
                    else source_checkout_digest(ASTRID_ROOT)
                ),
                "source_inventory_identity": inventory.identity if inventory.sources else "",
                "readiness_profile_path": str(self.readiness_profile_path.resolve()),
                "readiness_profile_hash": self.readiness_profile_hash,
            }
            self.launcher_value = launcher_value
            host_environment = {
                key: self.schema_session.child_environment[key]
                for key in (
                    "ASTRID_C11_EVIDENCE_PATH",
                    "ASTRID_C11_EXPECTED_PATH",
                    "ASTRID_C11_SCHEMA_PATH",
                    "ASTRID_C11_SESSION_DIR",
                    "PATH",
                )
            }
            host_environment.update(
                {
                    "ASTRID_HOST_READINESS_PROFILE_PATH": str(self.readiness_profile_path),
                    "ASTRID_HOST_READINESS_PROFILE_HASH": self.readiness_profile_hash,
                    "ASTRID_VIBECOMFY_CHECKOUT": str(self.vibecomfy_root),
                    "BANODOCO_LOCAL_DATA_ROOT": str(self.data_root),
                    "BANODOCO_RUNTIME_ENDPOINT": self.runtime_endpoint,
                    "BANODOCO_RUNTIME_CREDENTIAL": str(self.worker_credential_file),
                    "PYTHONPATH": _vibecomfy_child_pythonpath(self.vibecomfy_root),
                    "ASTRID_H3_CANDIDATE_MANIFEST": str(candidate_manifest),
                }
            )
            if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY:
                host_environment["ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"] = str(self.readiness_profile_path)
            else:
                host_environment.pop("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE", None)
            with _temporary_environment(
                host_environment,
                remove=(
                    "BANODOCO_LOCAL_HOME",
                    "BANODOCO_LOCAL_SOURCE_MANIFEST",
                    "ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE",
                ),
            ):
                self.host = ensure_pack_host(
                    launcher_value,
                    reconfigure_action="repair C11 fixture host startup",
                )
            if self.host.get("host_status") != "ready":
                raise RuntimeError(f"C11 canonical host bootstrap did not become ready: {self.host!r}")
            self.host_pid = int(self.host["host_pid"])
            self.host_state_path = Path(self.host["host_ready_file"]).resolve().with_name("generic-host.json")
            ready = json.loads(Path(self.host["host_ready_file"]).read_text(encoding="utf-8"))
            attestation = ready.get("identity_attestation")
            # This harness starts the ordinary local pack host directly through
            # ensure_pack_host. Targeted host startup is only supported through
            # Worker-supervised activation, so the host readiness record must
            # not claim the task's Runtime placement target. The Runtime-side
            # credential/task binding remains checked at invocation time.
            if (
                not isinstance(attestation, Mapping)
                or attestation.get("target") is not None
                or attestation.get("target_digest") is not None
            ):
                raise RuntimeError(
                    "C11 direct local fixture host unexpectedly claims an execution target"
                )
            # This fixture starts the ordinary pack host directly. Its bootstrap
            # receipt attests readiness, host identity, Runtime epoch, and source
            # pins; supervised orchestration/executor lanes are a separate
            # Worker-placement contract and are not returned by this API.
        except BaseException:
            try:
                self.close()
            except BaseException:
                pass
            raise
        finally:
            self._restore_parent_state()

    def _restore_parent_state(self) -> None:
        """Restore the exact parent import and environment identities."""
        sys.path[:] = self._prior_sys_path
        prior_names = set(self._prior_vibecomfy_modules)
        for name in tuple(sys.modules):
            if (
                name == "vibecomfy" or name.startswith("vibecomfy.")
            ) and name not in prior_names:
                sys.modules.pop(name, None)
        for name, module in self._prior_vibecomfy_modules.items():
            sys.modules[name] = module
        for key, value in self._prior_environment.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def close(self) -> None:
        if self._closed:
            self._restore_parent_state()
            return
        self._closed = True
        cleanup_errors: list[BaseException] = []
        try:
            host_pid = self.host_pid
            if host_pid is not None:
                try:
                    state = json.loads(self.host_state_path.read_text(encoding="utf-8")) if self.host_state_path else {}
                    if int(state.get("pid")) == host_pid:
                        try:
                            if os.getpgid(host_pid) == host_pid:
                                os.killpg(host_pid, signal.SIGTERM)
                            else:
                                os.kill(host_pid, signal.SIGTERM)
                        except (OSError, ProcessLookupError):
                            pass
                        deadline = time.monotonic() + 8
                        while time.monotonic() < deadline:
                            try:
                                os.kill(host_pid, 0)
                            except OSError:
                                break
                            time.sleep(0.05)
                        else:
                            try:
                                if os.getpgid(host_pid) == host_pid:
                                    os.killpg(host_pid, signal.SIGKILL)
                                else:
                                    os.kill(host_pid, signal.SIGKILL)
                            except (OSError, ProcessLookupError):
                                pass
                except (OSError, TypeError, ValueError, json.JSONDecodeError):
                    pass
        except BaseException as exc:
            cleanup_errors.append(exc)
        try:
            if self.schema_session is not None:
                self.schema_session.close()
        except BaseException as exc:
            cleanup_errors.append(exc)
        try:
            if self.public_workspace is not None:
                stopped = self.public_workspace.stop()
                provenance = self.public_workspace.provenance()
                provenance.update(
                    {
                        "endpoint": self.public_workspace.endpoint,
                        "actor_id": self.public_workspace.actor_id,
                        "runtime_pid": self.public_workspace.runtime_pid,
                        "runtime_instance_id": self.runtime_instance_id,
                        "health": getattr(self, "public_workspace_health", None),
                        "stop": stopped,
                        "synthetic_inference": self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY,
                    }
                )
                self.public_workspace_provenance_path.write_bytes(_canonical_json(provenance))
        except BaseException as exc:
            cleanup_errors.append(exc)
        finally:
            self._restore_parent_state()
        if cleanup_errors:
            raise RuntimeError("C11 fixture cleanup was incomplete") from cleanup_errors[0]

    def create_project_asset(self, path: Path, *, idempotency_key: str) -> str:
        imported = self.owner.media.import_file(
            project=self.project_id,
            realm="managed_local",
            path=path,
            idempotency_key=idempotency_key,
        )
        if not imported.ok:
            raise RuntimeError(f"could not import C11 managed input {path.name}: {imported.error}")
        return str(imported.data["object_id"])

    def read_cpu_model_boundary_evidence(self) -> dict[str, Any]:
        if self.cpu_model_boundary != APPROVED_CPU_MODEL_BOUNDARY:
            raise RuntimeError("the Runtime was not configured with the approved CPU model boundary")
        evidence_path = self._last_cpu_model_boundary_evidence_path
        if evidence_path is None:
            raise RuntimeError("approved CPU model-boundary evidence has no child activation record")
        try:
            value = json.loads(evidence_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("approved CPU model-boundary evidence is unavailable") from exc
        if not isinstance(value, dict):
            raise RuntimeError("approved CPU model-boundary evidence is malformed")
        if value.get("evidence_path") != str(evidence_path):
            raise RuntimeError("approved CPU model-boundary evidence path does not match its child record")
        return value

    def run_public_transform(self, request_path: Path, bundle_path: Path, *, out: Path, key: str):
        request = normalize_request(json.loads(request_path.read_text(encoding="utf-8"))).value
        archive = read_archive(bundle_path)
        request_assets = archive.manifest["assets"]
        if int(request.get("version", 0)) == 1:
            source_binding = str(request["source"]["asset"])
        else:
            timeline_videos = [
                row for row in request.get("media", [])
                if isinstance(row, Mapping)
                and row.get("role") == "timeline"
                and row.get("modality") == "video"
            ]
            video_media = [
                row for row in request.get("media", [])
                if isinstance(row, Mapping) and row.get("modality") == "video"
            ]
            if len(timeline_videos) == 1:
                source_binding = str(timeline_videos[0]["asset"])
            elif len(video_media) == 1:
                source_binding = str(video_media[0]["asset"])
            else:
                raise AssertionError("C11 request does not identify exactly one source video")
        source_records = [
            record for record in request_assets
            if record["binding"] == source_binding
        ]
        if len(source_records) != 1 or self.schema_session is None:
            raise AssertionError("C11 requires one bundled source and a managed session")
        source_record = source_records[0]
        expected = {
            "basename": Path(source_record["member"]).name,
            "sha256": source_record["sha256"],
            "size": source_record["size"],
            "generated_seconds": (
                float(request["output"]["duration"]) - float(request["source"]["range"][1])
                if int(request.get("version", 0)) == 1 else 13
            ),
        }
        if isinstance(request.get("settings"), Mapping) and isinstance(request["settings"].get("adapter"), Mapping):
            media = request.get("media") if isinstance(request.get("media"), list) else []
            video_refs = [row for row in media if isinstance(row, Mapping) and row.get("role") == "reference" and row.get("modality") == "video"]
            image_refs = [row for row in media if isinstance(row, Mapping) and row.get("role") == "reference" and row.get("modality") == "image"]
            if len(video_refs) != 1 or len(image_refs) != 1:
                raise AssertionError("Character Swap CPU boundary expects one video and one image reference")
            by_binding = {str(row["binding"]): row for row in request_assets}
            video_asset = by_binding.get(str(video_refs[0]["asset"]))
            image_asset = by_binding.get(str(image_refs[0]["asset"]))
            if not isinstance(video_asset, Mapping) or not isinstance(image_asset, Mapping):
                raise AssertionError("Character Swap CPU boundary references are missing from the request bundle")
            expected.update({
                "character_swap": True,
                "video_reference_members": [Path(str(video_asset["member"])).name],
                "image_reference_members": [Path(str(image_asset["member"])).name],
                "asset_files": {
                    Path(str(row["member"])).name: {"sha256": row["sha256"], "size": row["size"]}
                    for row in (video_asset, image_asset)
                },
                "generated_seconds": float(request["duration"]),
            })
        self.schema_session.expected_path.write_bytes(_canonical_json(expected))
        safe_key = key.replace(":", "-")
        asset_map_path = _write_runtime_asset_map(archive, out)
        # The public command orchestrator calls open_from_launcher in an
        # isolated child. Carry only the selected nonsecret support root into
        # that launch scope so the SDK discovers this workspace instead of
        # falling back to a developer/default support directory.
        invoke_environment = {"BANODOCO_LOCAL_DATA_ROOT": str(self.data_root.resolve())}
        selected_candidate = getattr(self, "candidate_manifest_path", None)
        if selected_candidate is not None:
            invoke_environment["ASTRID_H3_CANDIDATE_MANIFEST"] = str(selected_candidate)
        remove_environment: tuple[str, ...] = ()
        if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY:
            substitute_profile = getattr(self, "readiness_profile_path", None)
            if substitute_profile is None:
                raise RuntimeError("approved T9 model boundary has no generated readiness profile")
            invoke_environment["ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE"] = str(substitute_profile)
        else:
            remove_environment = ("ASTRID_H3_T9_MODEL_SUBSTITUTE_PROFILE",)
        calls_path: Path | None = None
        calls_offset = 0
        if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY:
            calls_path = self.t9_child_calls_path
            if calls_path.is_symlink() or (calls_path.exists() and not calls_path.is_file()):
                raise RuntimeError("T9 child call log is not a regular case-owned file")
            calls_offset = calls_path.stat().st_size if calls_path.exists() else 0
            self._last_cpu_model_boundary_evidence_path = None
        with _temporary_environment(invoke_environment, remove=remove_environment):
            result = self.owner.invoke_result(
                "h3_av.transform",
                kind="orchestrator",
                project=self.project_id,
                out=out,
                # h3_av.transform is a local command orchestrator. Managed
                # descriptors are reserved for its executor child submissions,
                # which import bundled inputs through the connected Runtime client.
                inputs={
                    "request": str(request_path.resolve()),
                    "asset_map": str(asset_map_path.resolve()),
                },
                # Command orchestrator args are how the public launcher
                # forwards the selected Runtime project to run.py. The
                # SDK's separate project= value is used for parent-run
                # context, but is not a command placeholder.
                orchestrator_args=("--project", self.project_id),
                idempotency_context={"h3_submission_id": safe_key},
                wait=True,
                timeout_seconds=(
                    600
                    if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY
                    else 180
                ),
                poll_seconds=0.05,
            )
        if self.cpu_model_boundary == APPROVED_CPU_MODEL_BOUNDARY and result.ok:
            assert calls_path is not None
            try:
                call_bytes = calls_path.read_bytes()
                appended = call_bytes[calls_offset:]
                if not appended or not appended.endswith(b"\n"):
                    raise RuntimeError("T9 child did not append a complete activation call record")
                calls = [json.loads(line) for line in appended.splitlines() if line]
                if not calls or any(not isinstance(row, Mapping) for row in calls):
                    raise RuntimeError("T9 child activation call records are malformed")
                for call in calls:
                    evidence_path = Path(str(call.get("evidence_path") or ""))
                    if (
                        not evidence_path.is_absolute()
                        or evidence_path.is_symlink()
                        or not evidence_path.is_file()
                        or evidence_path.parent.resolve(strict=True)
                        != self.t9_child_evidence_root.resolve(strict=True)
                    ):
                        raise RuntimeError("T9 child evidence escaped its case-owned directory")
                    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
                    if not isinstance(evidence, Mapping):
                        raise RuntimeError("T9 child evidence is malformed")
                    for key in ("task_id", "attempt_id", "execution_id", "child_pid", "activation_marker_path"):
                        if evidence.get(key) != call.get(key):
                            raise RuntimeError(f"T9 child evidence differs from its call record: {key}")
                    marker = evidence.get("activation_marker")
                    if not isinstance(marker, Mapping) or marker.get("child_pid") != call.get("child_pid"):
                        raise RuntimeError("T9 child evidence is not bound to its activation marker")
                    outputs = evidence.get("outputs")
                    if not isinstance(outputs, list) or not outputs or call.get("outputs") != outputs:
                        raise RuntimeError("T9 child produced no output evidence")
                    for output in outputs:
                        if not isinstance(output, Mapping):
                            raise RuntimeError("T9 child output evidence is malformed")
                        output_path = Path(str(output.get("path") or ""))
                        if (
                            not output_path.is_absolute()
                            or output_path.is_symlink()
                            or not output_path.is_file()
                            or output_path.stat().st_nlink != 1
                            or hashlib.sha256(output_path.read_bytes()).hexdigest() != output.get("sha256")
                            or output_path.stat().st_size != output.get("bytes")
                        ):
                            raise RuntimeError("T9 child output differs from its evidence digest")
                    self._last_cpu_model_boundary_evidence_path = evidence_path
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError("T9 child activation evidence could not be read back") from exc
        return result


__all__ = [
    "APPROVED_CPU_MODEL_BOUNDARY",
    "ASTRID_ROOT",
    "H3CpuRuntime",
    "RUNTIME_ROOT",
    "VIBECOMFY_ROOT",
]
