from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import time
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import (
    GenericPackHost,
    HostError,
    RuntimeProtocolClient,
    source_checkout_digest,
)
from astrid.packs.rendering.actions.assemble_timeline.run import build_authoring_proposal
from astrid.packs.rendering.shared.runtime_stitch import publish_authoring_proposal
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline.assembly import read_assembly_proposal
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError

_D13_PROFILE = Path(os.environ.get("ASTRID_D13_SOURCE_PROFILE", ""))
_D13_NODE = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node")
_D13_REMOTION = Path("/home/user/work/runtimes/agent-remotion-main95bd")
_D13_BROWSER = Path("/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell")
_D13_FFMPEG = Path("/usr/bin/ffmpeg")
_D13_FFPROBE = Path("/usr/bin/ffprobe")
_D13_NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
_D13_REMOTION_LOCK_SHA256 = "c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24"
_D13_BROWSER_SHA256 = "63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4"
_D13_FFMPEG_SHA256 = "ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41"
_D13_FFPROBE_SHA256 = "272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f"
_D13_REQUIRED_PROFILE_KEYS = frozenset(
    {"profile", "runtime_checkout", "source_checkout", "runtime_environment"}
)
_D13_REQUIRED_ORIGINS = (
    "host", "child", "action", "client", "sdk", "runtime_protocol",
    "runtime_protocol.platform", "astrid_runtime",
)


def _plain(value):
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _d13_resource_locks(profile: Mapping[str, str]) -> dict[str, str]:
    source = Path(profile["source_checkout"]).resolve()
    resources = {
        "source": str(source),
        "source_digest": source_checkout_digest(source),
        "node": _sha256_file(_D13_NODE),
        "remotion_package_lock": _sha256_file(_D13_REMOTION / "package-lock.json"),
        "browser": _sha256_file(_D13_BROWSER),
        "ffmpeg": _sha256_file(_D13_FFMPEG),
        "ffprobe": _sha256_file(_D13_FFPROBE),
    }
    return resources


def _d13_installed_profile(tmp_path: Path) -> tuple[dict[str, str], dict[str, str]]:
    failures: list[str] = []
    if not _D13_PROFILE.is_file() or _D13_PROFILE.is_symlink():
        failures.append(f"profile is not a regular file: {_D13_PROFILE}")
        return {}, {"failures": "; ".join(failures)}
    try:
        profile = json.loads(_D13_PROFILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, {"failures": f"profile unreadable: {exc}"}
    if not isinstance(profile, dict) or set(profile) != _D13_REQUIRED_PROFILE_KEYS:
        failures.append(f"profile keys are not the existing four-field carrier: {sorted(profile) if isinstance(profile, dict) else type(profile).__name__}")
        profile = {}
    if profile.get("profile") != "astrid":
        failures.append("profile id is not astrid")
    if profile:
        source = Path(str(profile["source_checkout"]))
        runtime = Path(str(profile["runtime_checkout"]))
        environment = Path(str(profile["runtime_environment"]))
        if not source.is_absolute() or source.is_symlink() or not source.is_dir():
            failures.append(f"installed source root is not a regular absolute directory: {source}")
        if source.resolve() != runtime.resolve():
            failures.append("runtime_checkout and source_checkout do not select the same installed tree")
        if not environment.is_absolute() or environment.is_symlink() or not environment.is_dir():
            failures.append(f"runtime environment is not a regular absolute directory: {environment}")
        interpreter = environment / "bin" / "python"
        if not interpreter.is_file() or interpreter.is_symlink():
            failures.append(f"installed interpreter is unavailable or symlinked: {interpreter}")
        elif Path(os.sys.executable).resolve() != interpreter.resolve():
            failures.append(f"pytest interpreter is not the selected installed interpreter: {os.sys.executable} != {interpreter}")
        for key in ("source_checkout", "runtime_checkout", "runtime_environment"):
            path = Path(str(profile[key]))
            if any(part.is_symlink() for part in (path, *path.parents)):
                failures.append(f"profile path traverses a symlink: {key}={path}")
        try:
            from astrid.sdk.host_bootstrap import _installed_execution_origins

            origins = _installed_execution_origins(source, str(interpreter))
            for key in _D13_REQUIRED_ORIGINS:
                if not origins.get(key):
                    failures.append(f"installed origin missing: {key}")
                elif not Path(str(origins[key])).resolve().is_relative_to(source.resolve()):
                    failures.append(f"installed origin escaped selected tree: {key}={origins[key]}")
        except (AttributeError, ImportError, KeyError, OSError, TypeError, ValueError) as exc:
            failures.append(f"installed origin probe failed: {exc}")
    for label, path, expected in (
        ("node", _D13_NODE, _D13_NODE_SHA256),
        ("Remotion package lock", _D13_REMOTION / "package-lock.json", _D13_REMOTION_LOCK_SHA256),
        ("browser", _D13_BROWSER, _D13_BROWSER_SHA256),
        ("ffmpeg", _D13_FFMPEG, _D13_FFMPEG_SHA256),
        ("ffprobe", _D13_FFPROBE, _D13_FFPROBE_SHA256),
    ):
        if not path.is_file() or path.is_symlink():
            failures.append(f"{label} is unavailable or symlinked: {path}")
        elif _sha256_file(path) != expected:
            failures.append(f"{label} hash changed: {path}")
    if not _D13_REMOTION.is_dir() or _D13_REMOTION.is_symlink():
        failures.append(f"Remotion project is unavailable or symlinked: {_D13_REMOTION}")
    fonts = _D13_REMOTION / "public" / "fonts"
    if not fonts.is_dir() or not (fonts / "FONT_PROVENANCE.md").is_file():
        failures.append("Remotion font provenance is unavailable")
    else:
        font_files = tuple(fonts.glob("*.woff2"))
        if not font_files or any(not item.is_file() or item.is_symlink() or item.stat().st_size == 0 for item in font_files):
            failures.append("Remotion font closure is empty, symlinked, or zero-sized")
    attempt = tmp_path / "preflight-attempt"
    if not attempt.is_relative_to(tmp_path):
        failures.append("attempt root is not private to this fixture")
    else:
        attempt.mkdir()
        probe = attempt / "writable-probe"
        probe.write_text("d13", encoding="utf-8")
        if probe.read_text(encoding="utf-8") != "d13" or probe.is_symlink():
            failures.append("private attempt root is not writable and isolated")
    usage = shutil.disk_usage(tmp_path)
    if usage.free < 5 * 1024**3:
        failures.append(f"free disk below 5 GiB: {usage.free}")
    if failures:
        return profile, {"failures": "; ".join(failures)}
    return profile, _d13_resource_locks(profile)


class _InstalledRuntimeService:
    """Small test-only facade over the generated installed Runtime client."""

    def __init__(self, owner, worker, realm_id: str):
        self.owner = owner
        self.worker = worker
        self.realm = {"id": realm_id}

    def health(self):
        return _plain(self.worker.health())

    def create_project(self, value, *, idempotency_key: str | None = None):
        result = self.owner._remote._transport.create_project(
            value["name"], slug=value.get("slug"),
            idempotency_key=idempotency_key or f"project-{value.get('slug', 'd13')}",
        )
        return {"id": result.get("project_id", result.get("id")), **dict(result)}

    def register_capability(self, value):
        return _plain(self.worker.register_capability(
            value["capability_id"], value["definition_digest"],
            status=value.get("status", "ready"),
            idempotency_key=value.get("idempotency_key"),
        ))

    def register_executor(self, value, *, idempotency_key: str):
        return _plain(self.worker.register_executor(value, idempotency_key=idempotency_key))

    def create_timeline(self, project_id: str, timeline_id: str, *, name: str | None = None, idempotency_key: str):
        return _plain(self.owner._remote._transport.create_timeline(project_id, timeline_id, name=name, idempotency_key=idempotency_key))

    def create_task(self, value):
        result = self.owner._remote._transport.admit_task(
            capability_id=value["capability_id"],
            capability_digest=value["capability_digest"],
            input_object_ids=value.get("input_object_ids", []),
            project_id=value.get("project"), spec=value.get("spec"),
            settlement_effect=value.get("settlement_effect"),
            idempotency_key=value["idempotency_key"],
        )
        task_id = result.get("task_id", result.get("id"))
        return {"task": self.task(task_id)["task"]}

    def claim_next(self, value, *, idempotency_key: str):
        claim = self.worker.claim_task(
            executor_id=value["executor_id"], capability_ids=value["capability_ids"],
            runtime_epoch=value["runtime_epoch"], idempotency_key=idempotency_key,
        )
        result = _plain(claim)
        if result is None:
            raise AssertionError("installed Runtime returned no claim")
        return {**result, "id": result.get("task_id"), "capability": result.get("capability_id")}

    def settle_attempt(self, attempt_id: str, settlement, *, idempotency_key: str):
        return _plain(self.worker.settle_attempt(attempt_id, settlement, idempotency_key=idempotency_key))

    def task(self, task_id: str):
        result = _plain(self.owner._remote._transport.get_task(task_id))
        result["id"] = result["task_id"]
        result["capability"] = result["capability_id"]
        return {"task": result}

    def managed_outputs(self, task_id: str):
        rows, cursor = self.owner._remote._transport.list_managed_outputs(task_id)
        assert cursor is None
        return [_plain(row) for row in rows]

    def object(self, object_id: str):
        result = self.owner._remote._transport.get_object(object_id)
        return result.media_type, result.data

    def count_tasks(self, project_id: str, capability: str) -> int:
        rows, cursor = self.owner._remote._transport.list_project_tasks(project_id, limit=100)
        assert cursor is None
        return sum(row.capability_id == capability for row in rows)


@pytest.fixture
def installed_runtime(tmp_path, monkeypatch):
    """Own the normal installed Runtime authority for the D13 positive."""
    profile, preflight = _d13_installed_profile(tmp_path)
    assert "failures" not in preflight, preflight["failures"]
    source = Path(profile["source_checkout"]).resolve()
    environment = Path(profile["runtime_environment"]).resolve()
    runtime_cli = environment / "bin" / "astrid-runtime"
    support = tmp_path / "runtime-support"
    realm_root = tmp_path / "realm"
    home = tmp_path / "home"
    temp_root = tmp_path / "tmp"
    for path in (support, realm_root, home, temp_root):
        path.mkdir()
    runtime_env = {
        "HOME": str(home),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": f"{_D13_NODE.parent}:{environment / 'bin'}:/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TMPDIR": str(temp_root),
        "ASTRID_HOST_EXECUTION_PROFILE": "installed",
        "ASTRID_PACK_HOST_PYTHON": str(environment / "bin" / "python"),
        "ASTRID_PACKS_PATH": str(source / "astrid" / "packs" / "rendering"),
        "ASTRID_REMOTION_PROJECT_DIR": str(_D13_REMOTION),
        "ASTRID_REMOTION_BROWSER_EXECUTABLE": str(_D13_BROWSER),
        "ASTRID_NODE_EXECUTABLE": str(_D13_NODE),
        "ASTRID_TEST_NODE_MODULES": str(_D13_REMOTION / "node_modules"),
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(source),
        "ASTRID_RUNTIME_SOURCE_MANIFEST": str(_D13_PROFILE),
    }
    def run_runtime(*args):
        completed = subprocess.run(
            [str(runtime_cli), *args, "--json"], env=runtime_env, cwd=tmp_path,
            check=False, text=True, capture_output=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        return json.loads(completed.stdout)

    bootstrap = None
    try:
        run_runtime(
            "workspace", "create", "--profile", "astrid", "--source-manifest", str(_D13_PROFILE),
            "--data-root", str(support), "--realm-root", str(realm_root),
            "--hosted-origin", "off",
        )
        bootstrap = run_runtime(
            "up", "--profile", "astrid", "--source-manifest", str(_D13_PROFILE),
            "--data-root", str(support), "--hosted-origin", "https://astrid.local",
            "--door-port", "0", "--wait",
        )
        worker_file = Path(bootstrap["worker_credential_file"])
        worker_token = worker_file.read_text(encoding="utf-8").strip()
        worker = RuntimeProtocolClient(bootstrap["endpoint"], worker_token, credential_file=worker_file)
        owner = AstridClient.open(
            endpoint=bootstrap["endpoint"], credential=Path(bootstrap["credential_file"]),
            realm_id=bootstrap["realm_id"], actor_id=bootstrap["actor_id"],
            client_name="astrid-d13-installed", client_version="stage1", protocol_version="workspace.v1",
        )
        service = _InstalledRuntimeService(owner, worker, bootstrap["realm_id"])
        yield SimpleNamespace(
            service=service, owner=owner, worker=worker, bootstrap=bootstrap,
            runtime_env=runtime_env, support=support, profile=profile,
            resource_locks=preflight,
        )
    finally:
        from astrid.sdk.upgrade import stop_pack_host

        if bootstrap is not None:
            stop_pack_host(support)
            completed = subprocess.run(
                [str(runtime_cli), "down", "--profile", "astrid", "--data-root", str(support), "--json"],
                env=runtime_env, cwd=tmp_path, check=False, text=True, capture_output=True,
            )
            assert completed.returncode == 0, completed.stdout + completed.stderr
            assert _d13_resource_locks(profile) == preflight


def test_d13_installed_native_preflight(tmp_path):
    """Check the exact installed tuple without opening Runtime or native tools."""
    profile, result = _d13_installed_profile(tmp_path)
    assert "failures" not in result, result["failures"]
    assert profile["profile"] == "astrid"
    assert result["source_digest"]


def _digest(value: str | bytes) -> str:
    raw = value.encode() if isinstance(value, str) else value
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _claim_child(service, capability: str, *, key: str) -> dict:
    epoch = service.health()["runtime_epoch"]
    claim = service.claim_next(
        {"executor_id": "chain-worker", "capability_ids": [capability], "runtime_epoch": epoch},
        idempotency_key=key,
    )
    row = service.store.conn.execute("SELECT * FROM attempts WHERE task_id=?", (claim["task_id"],)).fetchone()
    return {"task_id": claim["task_id"], "attempt_id": row["id"], "lease_id": row["lease_id"], "fence": row["fence"], "runtime_epoch": row["runtime_epoch"]}


def _settle_child(service, attempt: dict, *, index: int, value: bytes, digest: str) -> dict:
    service.settle_attempt(
        attempt["attempt_id"],
        {
            "attempt_id": attempt["attempt_id"],
            "lease_id": attempt["lease_id"],
            "fence": attempt["fence"],
            "runtime_epoch": attempt["runtime_epoch"],
            "outputs": [{
                "digest": digest,
                "data_base64": base64.b64encode(value).decode(),
                "media_type": "video/mp4",
                "name": f"child-{index}",
                "role": "primary",
                "is_primary": True,
                "duration_seconds": 1.0,
            }],
        },
        idempotency_key=f"chain-settle-{index}",
    )
    return {"task_id": attempt["task_id"], "digest": digest}


def _media_effect(project_id: str) -> dict:
    return {
        "effect_type": "generation.publish_v1",
        "target_id": project_id,
        "payload": {
            "version": 1,
            "modality": "video",
            "generation_type": "multi_output_render",
            "metadata": {"params": {"duration_seconds": 1.0, "width": 64, "height": 36}},
            "partial_success_policy": "reject",
            "groups": [{"group_key": "main", "selectors": [{
                "selector": "primary", "ordinal": 0, "variant_key": "primary", "output_port": "video",
            }]}],
        },
    }


@pytest.mark.integration
def test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task(tmp_path, real_runtime):
    """Exercise child settlement -> authoring -> fenced publication -> render admission."""
    daemon = real_runtime()
    service = daemon.service
    try:
        project = service.create_project({"slug": "chain", "name": "Chain"})
        child_cap, author_cap, render_cap = "video.child", "rendering.assemble_timeline", "rendering.render"
        digests = {cap: _digest(cap) for cap in (child_cap, author_cap, render_cap)}
        for capability, digest in digests.items():
            service.register_capability({"capability_id": capability, "definition_digest": digest, "status": "ready"})
        service.register_executor(
            {"executor_id": "chain-worker", "capabilities": [child_cap, author_cap, render_cap], "max_concurrency": 4},
            idempotency_key="chain-register",
        )
        service.create_timeline_document(
            project["id"], {"timeline_id": "main", "slug": "main", "name": "Main", "config": {}, "registry": {}},
            idempotency_key="chain-timeline",
        )
        child_ids = []
        for index in range(2):
            task = service.create_task({
                "project": project["id"], "capability_id": child_cap, "capability_digest": digests[child_cap],
                "input_object_ids": [], "spec": {"index": index}, "idempotency_key": f"chain-child-{index}",
            })
            child_ids.append(task["task"]["id"])
        service.create_task({
            "project": project["id"], "capability_id": author_cap, "capability_digest": digests[author_cap],
            "input_object_ids": [], "idempotency_key": "chain-author",
            "spec": {"runtime_dependencies": {"edges": [
                {"from_task_id": task_id, "to": "self", "requires_event": "task.succeeded", "fence": "runtime_task"}
                for task_id in child_ids
            ], "aggregation": {"kind": "ordered_cas_inputs", "order": []}}},
        })
        outputs = [_digest(b"child-zero"), _digest(b"child-one")]
        claims = [_claim_child(service, child_cap, key=f"chain-claim-child-{index}") for index in range(2)]
        assert {claim["task_id"] for claim in claims} == set(child_ids)
        by_task = {claim["task_id"]: claim for claim in claims}
        # Deliberately settle ordinal 1 before ordinal 0; claim order is
        # runtime-owned and may differ from admission order.
        _settle_child(service, by_task[child_ids[1]], index=1, value=b"child-one", digest=outputs[1])
        _settle_child(service, by_task[child_ids[0]], index=0, value=b"child-zero", digest=outputs[0])

        author_claim = service.claim_next(
            {"executor_id": "chain-worker", "capability_ids": [author_cap], "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key="chain-claim-author",
        )
        author_row = service.store.conn.execute("SELECT * FROM attempts WHERE task_id=?", (author_claim["task_id"],)).fetchone()
        runtime_attempt = {"attempt_id": author_row["id"], "lease_id": author_row["lease_id"], "fence": author_row["fence"], "runtime_epoch": author_row["runtime_epoch"]}
        author_task = service.task(author_claim["task_id"])["task"]
        # Feed the exact Runtime claim envelope into the authoring executor;
        # no enriched test-only descriptors are inserted here.
        proposal = build_authoring_proposal({
            "task_id": author_task["id"],
            "capability_id": author_task["capability"],
            "input_object_ids": author_task["spec"]["input_object_ids"],
            "spec": author_task["spec"],
        })
        client = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=service.realm["id"], actor_id="owner", client_name="astrid-chain-test",
            client_version="stage1", protocol_version="workspace.v1",
        )
        result = publish_authoring_proposal(
            client, proposal=proposal, timeline_id="main", expected_version=1,
            runtime_attempt=runtime_attempt, render_capability_digest=digests[render_cap],
            output_name="chain.mp4", idempotency_key="chain-publish",
        )
        assert result["timeline_version"] == 2
        assert service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability=?", (render_cap,)).fetchone()[0] == 1
        render = service.task(result["render_task_id"])["task"]
        assert render["spec"]["spec"]["inputs"]["timeline_snapshot"]["config"] == proposal["timeline"]
        assert render["spec"]["spec"]["inputs"]["expected_version"] == 2
        # The checkpoint admits the ordinary public renderer; the next worker
        # claim therefore sees rendering.render without a stitch-specific task.
        render_claim = service.claim_next(
            {"executor_id": "chain-worker", "capability_ids": [render_cap], "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key="chain-claim-render",
        )
        assert render_claim["task_id"] == result["render_task_id"]
    finally:
        daemon.stop()


@pytest.mark.xfail(strict=True, reason="D13 removes the legacy assembler publication hook; native requester commit is required")
def test_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke(tmp_path):
    """The registered authoring host hook has one Runtime publication route."""
    proposal_path = tmp_path / "attempt" / "outputs" / "authoring-proposal.json"
    proposal_path.parent.mkdir(parents=True)
    proposal_path.write_text(json.dumps({
        "timeline": {"tracks": [], "clips": []}, "registry": {"assets": {}},
        "publication": {"authority": "workspace_runtime", "render_capability": "rendering.render"},
    }))

    class Runtime:
        def __init__(self): self.calls = []
        def publish_timeline_render(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            return {"timeline_version": 2, "render_task_id": "render-1"}

    runtime = Runtime()
    host = GenericPackHost.__new__(GenericPackHost)
    host.client = runtime
    host.capabilities = {}
    result = host._publish_assembled_timeline(
        task_data={"id": "author-1", "spec": {"family": "stitch_finalization", "runtime_dependencies": {
            "publication": {"timeline_id": "main", "expected_version": 1, "render": {
                "capability_id": "rendering.render", "capability_digest": _digest("rendering.render"),
                "spec": {"inputs": {"selector": "rendering.ffmpeg"}},
            }},
        }}},
        attempt_id="attempt-1", fence=1, lease_token="lease-1",
        outputs=[{"path": str(proposal_path), "artifact_type": "timeline/authoring-proposal"}],
        attempt_root=proposal_path.parents[1],
    )
    assert result["render_task_id"] == "render-1"
    assert len(runtime.calls) == 1
    args, kwargs = runtime.calls[0]
    assert args[:2] == ("attempt-1", "lease-1")
    assert kwargs["timeline_id"] == "main"
    assert kwargs["expected_version"] == 1
    assert "save" not in repr(runtime.calls) and "invoke" not in repr(runtime.calls)


def test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts(tmp_path):
    """Unsafe legacy admission is visible, terminal, and leaves its artifact untouched."""
    proposal_path = tmp_path / "attempt" / "outputs" / "authoring-proposal.json"
    proposal_path.parent.mkdir(parents=True)
    original = json.dumps({
        "timeline": {"tracks": [], "clips": []}, "registry": {"assets": {}},
        "publication": {"authority": "workspace_runtime", "render_capability": "rendering.render"},
    }).encode()
    proposal_path.write_bytes(original)

    class Runtime:
        def __init__(self):
            self.calls = []

        def fail(self, *args, **kwargs):
            self.calls.append((args, kwargs))

        def heartbeat(self, *args, **kwargs):
            self.calls.append((args, kwargs))

        def task(self, *args, **kwargs):
            self.calls.append((args, kwargs))

        def settle(self, *args, **kwargs):
            self.calls.append((args, kwargs))

        def upload_object(self, *args, **kwargs):
            self.calls.append((args, kwargs))

    runtime = Runtime()
    host = GenericPackHost(pack_roots=[], client=runtime, attempt_root=tmp_path / "host-attempt")
    host.capabilities = {
        "rendering.assemble_timeline": SimpleNamespace(
            ready=True, definition=SimpleNamespace(metadata={}), matrix={},
        )
    }
    host.preflight = lambda _capability: None
    host._registration_admission_reason = lambda: None
    task = {
        "id": "author-1", "capability": "rendering.assemble_timeline",
        "spec": {"runtime_dependencies": {"publication": {"timeline_id": "main"}}},
        "input_object_ids": [], "project_id": "project-1", "attempt_id": "attempt-1",
        "fence": 1, "runtime_epoch": 1,
    }
    try:
        with pytest.raises(HostError, match="immutable original target"):
            host.run_task(task, lease_token="lease-1", attempt_id="attempt-1", fence=1)
    finally:
        host.shutdown()
    assert proposal_path.read_bytes() == original
    assert len(runtime.calls) == 1
    args, _kwargs = runtime.calls[0]
    assert args[:2] == ("author-1", "lease-1")
    assert not any("publish_timeline_render" in repr(call) for call in runtime.calls)


@pytest.mark.integration
def test_daemon_backed_host_executes_authoring_and_final_render(tmp_path, monkeypatch, installed_runtime):
    """Run registered native assembly through requester, host, Runtime, and render."""
    bootstrap = installed_runtime.bootstrap
    service = installed_runtime.service
    source = Path(installed_runtime.profile["source_checkout"]).resolve()
    allowed = set(installed_runtime.runtime_env)
    for name, value in installed_runtime.runtime_env.items():
        monkeypatch.setenv(name, value)
    for name in tuple(os.environ):
        if name.startswith("ASTRID_") and name not in allowed:
            monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("PYTHONPATH", raising=False)
    from astrid.sdk.host_bootstrap import ensure_pack_host

    pack_roots = (source / "astrid/packs/rendering",)
    client = None
    host = GenericPackHost(
        pack_roots=pack_roots,
        client=installed_runtime.worker,
        executor_id="astrid-pack-host",
        attempt_root=tmp_path / "attempt",
    )
    try:
        host.discover()
        assemble_digest = host.capabilities["rendering.assemble_timeline"].capability_digest
        ensure_pack_host(
            bootstrap,
            reconfigure_action="restart the D13 installed pack host",
            startup_idle_seconds=30,
        )
        child_capability = "video.child"
        child_digest = _digest(child_capability)
        project = service.create_project({"slug": "host-chain", "name": "Host chain"})
        service.register_capability(
            {"capability_id": child_capability, "definition_digest": child_digest, "status": "ready"}
        )
        service.register_executor(
            {
                "executor_id": "chain-worker",
                "capabilities": [child_capability],
                "max_concurrency": 2,
            },
            idempotency_key="host-chain-register-child",
        )
        client = installed_runtime.owner
        service.create_timeline(project["id"], "main", name="Main", idempotency_key="host-chain-timeline")
        blobs = []
        for index, colour in enumerate(("blue", "red")):
            path = tmp_path / f"child-{index}.mp4"
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", f"color=c={colour}:s=64x36:r=30:d=1", "-an", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", str(path),
                ],
                check=True,
                capture_output=True,
            )
            blobs.append(path.read_bytes())
        child_ids = []
        for index in range(2):
            child_ids.append(
                service.create_task(
                    {
                        "project": project["id"],
                        "capability_id": child_capability,
                        "capability_digest": child_digest,
                        "input_object_ids": [],
                        "spec": {"index": index},
                        "settlement_effect": _media_effect(project["id"]),
                        "idempotency_key": f"host-chain-child-{index}",
                    }
                )["task"]["id"]
            )
        claims = []
        for index in range(2):
            claim = service.claim_next(
                {
                    "executor_id": "chain-worker",
                    "capability_ids": [child_capability],
                    "runtime_epoch": service.health()["runtime_epoch"],
                },
                idempotency_key=f"host-chain-claim-child-{index}",
            )
            claims.append(claim)
        by_task = {claim["task_id"]: claim for claim in claims}
        assert set(by_task) == set(child_ids)
        # Finish ordinal 1 first; Runtime still resolves the declared order.
        for index in (1, 0):
            claim = by_task[child_ids[index]]
            service.settle_attempt(
                claim["attempt_id"],
                {
                    "attempt_id": claim["attempt_id"],
                    "lease_id": claim["lease_id"],
                    "fence": claim["fence"],
                    "runtime_epoch": claim["runtime_epoch"],
                    "outputs": [{
                        "digest": _digest(blobs[index]),
                        "data_base64": base64.b64encode(blobs[index]).decode(),
                        "media_type": "video/mp4",
                        "name": f"child-{index}",
                        "output_port": "video",
                        "group_key": "main",
                        "variant_key": "primary",
                        "ordinal": 0,
                        "role": "primary",
                        "is_primary": True,
                        "duration_seconds": 1.0,
                    }],
                    "effect": _media_effect(project["id"]),
                },
                idempotency_key=f"host-chain-settle-child-{index}",
            )
        selectors = []
        for child_id in child_ids:
            associations = service.managed_outputs(child_id)
            association = next(row for row in associations if row["output_port"] == "video")
            selectors.append({
                "association_id": association["association_id"],
                "object_id": association["object_id"],
                "version": association["lifecycle"]["version"],
            })
        session = TimelineSession.open(
            project["id"], "main", client=client, outbox_path=tmp_path / "host-chain-outbox.json",
        )
        admission = session.admit_assembly(
            selectors, replace_clips=[], assembler_digest=assemble_digest,
            idempotency_key="host-chain-author",
        )
        author = admission["data"]["task_id"]
        admitted_task = service.task(author)["task"]
        admitted_spec = admitted_task["spec"]["spec"]
        admitted_capture = admitted_spec["inputs"]["resolved_children"]
        admitted_target = admitted_capture["admitted_target"]
        assert admitted_task["capability"] == "rendering.assemble_timeline"
        assert admitted_spec["runtime_dependencies"]["publication"]["admitted_target"] == admitted_target
        assert admitted_capture["replace_clips"] == []
        assert [child["association"] for child in admitted_capture["children"]] == selectors
        assert [child["media"]["object_id"] for child in admitted_capture["children"]] == [
            selector["object_id"] for selector in selectors
        ]
        assert admitted_spec["runtime_dependencies"]["aggregation"]["order"] == [
            selector["object_id"] for selector in selectors
        ]
        assert admitted_spec["outputs"]["authoring_proposal"] == {
            "type": "file", "artifact_type": "timeline/authoring-proposal",
        }
        author_claim = None
        for _ in range(600):
            author_task = service.task(author)["task"]
            if author_task.get("state") == "succeeded":
                author_claim = {"attempt_id": author_task["attempt_id"]}
                break
            if author_task.get("state") in {"failed", "cancelled"}:
                raise AssertionError(f"installed pack host did not settle authoring task: {author_task}")
            time.sleep(0.1)
        assert author_claim is not None, "installed pack host did not settle authoring task"
        author_result = service.task(author)["task"]["result"]
        assert {item["name"] for item in author_result["outputs"]} >= {"authoring_proposal", "timeline", "assets"}
        settled = read_assembly_proposal(session, author, attempt_id=author_claim["attempt_id"])
        assert [command["op"] for command in settled["commands"][:3]] == [
            "timeline.assembled-target", "track.create", "clip.add-media",
        ]
        assert [command["args"]["media"]["object_id"] for command in settled["commands"] if command["op"] == "clip.add-media"] == [
            selector["object_id"] for selector in selectors
        ]
        assert settled["admitted_target"] == admitted_target
        assert settled["commands"][0]["args"]["replace_clips"] == admitted_capture["replace_clips"]
        session.queue_assembly(author, attempt_id=author_claim["attempt_id"])
        pending = json.loads((tmp_path / "host-chain-outbox.json").read_text())
        assert pending["pending"][0]["op"] == "producer.guard"
        original_commit = client.timelines.commit

        def lose_ack(*args, **kwargs):
            original_commit(*args, **kwargs)
            raise WorkspaceClientError(0, "transport_error", "lost commit acknowledgement")

        client.timelines.commit = lose_ack
        with pytest.raises(WorkspaceClientError, match="lost commit acknowledgement"):
            session.flush(idempotency_key="host-chain-commit")
        saved_flight = json.loads((tmp_path / "host-chain-outbox.json").read_text())["flight"]
        assert saved_flight["key"] == "host-chain-commit"
        client.timelines.commit = original_commit
        restarted = TimelineSession.open(
            project["id"], "main", client=client, outbox_path=tmp_path / "host-chain-outbox.json",
        )
        committed = restarted.flush(idempotency_key="host-chain-commit")
        accepted_revision = committed["data"]["accepted_revision_id"]
        accepted_publication = committed["data"]["accepted_publication_id"]
        assert accepted_revision and accepted_publication
        assert json.loads((tmp_path / "host-chain-outbox.json").read_text())["flight"] is None

        scope = client.timelines.resolve_scope(project["id"], "main")
        assert scope.ok and isinstance(scope.data.get("version"), int)
        render_admission = client.invoke_result(
            "rendering.render", kind="executor", project=project["id"],
            inputs={"timeline_ref": "main", "expected_version": scope.data["version"], "output_name": "host-chain.mp4"},
            wait=False,
        )
        assert render_admission.ok
        render_task_id = render_admission.kernel_task_id
        assert isinstance(render_task_id, str) and render_task_id
        assert service.count_tasks(project["id"], "rendering.render") == 1
        for _ in range(1200):
            render_task = service.task(render_task_id)["task"]
            if render_task.get("state") == "succeeded":
                break
            if render_task.get("state") in {"failed", "cancelled"}:
                raise AssertionError(f"installed pack host did not settle render task: {render_task}")
            time.sleep(0.1)
        else:
            raise AssertionError("installed pack host did not settle render task")
        render_result = service.task(render_task_id)["task"]["result"]
        assert {item["name"] for item in render_result["outputs"]} >= {"video", "provenance"}
        video = next(item for item in render_result["outputs"] if item["name"] == "video")
        _, video_bytes = service.object(video["digest"])
        assert len(video_bytes) > 100
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", "-"],
            input=video_bytes,
            capture_output=True,
        )
        assert probe.returncode == 0
        assert float(probe.stdout.strip()) > 0
        render_task = service.task(render_task_id)["task"]
        render_inputs = render_task["spec"]["spec"]["inputs"]
        assert render_inputs["timeline_authority"]["config_version"] == scope.data["version"]
        assert render_inputs["timeline_authority"]["parent_revision_id"] == accepted_revision
        undone = restarted.undo([accepted_publication], idempotency_key="host-chain-undo")
        assert undone["data"]["accepted_revision_id"]
    finally:
        host.shutdown()
