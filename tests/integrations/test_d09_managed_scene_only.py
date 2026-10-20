"""D09 proof through Runtime admission, the real pack host, and Scene."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import sys
import threading
import uuid
import zipfile
from pathlib import Path
from typing import Any

import pytest

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.core.timeline.authoring_bundle import open_authoring_bundle, preview_authoring_candidate
from astrid.sdk import AstridClient, timeline_filmstrip
from astrid.sdk.pagination import paged_rows

ROOT = Path(__file__).resolve().parents[2]
REMOTION = Path("/home/user/work/runtimes/agent-remotion-0013").resolve()
NODE = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node").resolve()
SCHEMA = Path("/home/user/work/venv-agent/lib/python3.13/site-packages").resolve()

# This node is selected only by the explicit central live test request.  It is
# intentionally not marked ``integration`` because the bounded targeted lane
# otherwise applies the repository's default ``not integration`` expression.


@pytest.fixture(autouse=True)
def _public13_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Pin this proof to the read-only public13 installed profile."""
    monkeypatch.delenv("NODE_OPTIONS", raising=False)
    monkeypatch.delenv("NODE_PATH", raising=False)
    for name in tuple(os.environ):
        if name.startswith("GIT_") and name not in {
            "GIT_EDITOR",
            "GIT_SEQUENCE_EDITOR",
            "GIT_PAGER",
            "GIT_TERMINAL_PROMPT",
            "GIT_ASKPASS",
            "GIT_SSH",
            "GIT_SSH_COMMAND",
            "GIT_SSH_VARIANT",
            "GIT_MERGE_AUTOEDIT",
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL",
        }:
            monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", "/home/user/work/runtime")
    private_profile = tmp_path / "public13-profile"
    shutil.copytree(
        REMOTION,
        private_profile,
        symlinks=True,
        ignore=shutil.ignore_patterns("node_modules"),
    )
    shutil.copytree(
        REMOTION / "node_modules",
        private_profile / "node_modules",
        symlinks=False,
    )
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(private_profile))
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", str(NODE))
    monkeypatch.setenv("ASTRID_TIMELINE_SCHEMA_PYTHONPATH", str(SCHEMA))
    assert private_profile.is_dir()
    assert NODE.is_file() and os.access(NODE, os.X_OK)
    package = json.loads((private_profile / "package.json").read_text(encoding="utf-8"))
    assert package["dependencies"]["@banodoco/timeline-composition"] == (
        "file:artifacts/banodoco-timeline-composition-0.0.13.tgz"
    )
    from astrid.core.rendering.remotion_runtime import prepare_remotion_validation

    validation = prepare_remotion_validation(
        artifact_directory=tmp_path / "remotion-validation",
        host_environment=dict(os.environ),
        python_executable=sys.executable,
        launch_id=uuid.uuid4().hex,
        contexts={"host": dict(os.environ)},
    )
    for name, value in validation.items():
        monkeypatch.setenv(name, value)


def _config(content: str) -> dict[str, Any]:
    return {
        "theme": "banodoco-default",
        "theme_overrides": {
            "visual": {"canvas": {"width": 160, "height": 90, "fps": 10}}
        },
        "tracks": [{"id": "picture", "kind": "visual", "label": "Picture"}],
        "clips": [{
            "id": "title",
            "track": "picture",
            "clipType": "text",
            "at": 0,
            "hold": 1,
            "text": {"content": content},
            "app": {"astrid": {"cut": "c01", "layer": "title"}},
        }],
        "effects": [],
        "audio": [],
    }


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _connect(daemon: Any) -> AstridClient:
    return AstridClient.open(
        endpoint=daemon.endpoint,
        credential=daemon.credential_path,
        realm_id=daemon.service.realm["id"],
        actor_id="owner",
        client_name="d09-managed-scene-test",
        client_version="test",
        protocol_version="workspace.v1",
    )


def _publish(client: AstridClient, *, suffix: str) -> tuple[str, str]:
    transport = client._remote._transport
    created = transport.create_project(
        f"D09 {suffix}", idempotency_key=f"d09-project-{suffix}", slug=f"d09-{suffix}"
    )
    project = created.get("data", created)
    project_id = str(project.get("project_id") or project.get("id"))
    transport.create_timeline(project_id, "main", idempotency_key=f"d09-timeline-{suffix}")
    config = _config("saved")
    registry = {"assets": {}}
    parent_revision = f"d09-parent-{suffix}"
    publication = {
        "project_id": project_id,
        "timeline_id": "main",
        "expected_head": None,
        "parent_revision_id": parent_revision,
        "parent_composition": {
            "config": config,
            "registry": registry,
            "clips": config["clips"],
            "occurrences": [],
        },
        "shot_revisions": [],
        "internal_timeline_revisions": [],
    }
    result = transport.publish_parent_composition(
        project_id, "main", publication, idempotency_key=f"d09-publish-{suffix}"
    )
    assert result
    data = result.get("data", result)
    assert str(data.get("new_head") or data.get("parent_revision_id")) == parent_revision
    return project_id, parent_revision


def _host(daemon: Any, tmp_path: Path) -> GenericPackHost:
    worker = RuntimeProtocolClient(
        daemon.endpoint,
        daemon.worker_credential_path.read_text(encoding="utf-8").strip(),
        credential_file=daemon.worker_credential_path,
    )
    host = GenericPackHost(
        pack_roots=[ROOT / "astrid" / "packs" / "rendering"],
        client=worker,
        executor_id="astrid-pack-host",
        attempt_root=tmp_path / "attempts",
    )
    records = {record.id: record for record in host.discover()}
    assert "rendering.render" in records
    assert "rendering.timeline_visualize" in records
    host.preflight("rendering.render")
    host.preflight("rendering.timeline_visualize")
    assert host.capabilities["rendering.render"].ready
    assert host.capabilities["rendering.timeline_visualize"].ready
    registration = host.register()
    assert registration["registration"].executor_id == "astrid-pack-host"
    return host


def _run_one(host: GenericPackHost, operation: Any) -> Any:
    errors: list[BaseException] = []

    def serve() -> None:
        try:
            host.run(max_tasks=1, poll_seconds=0.05)
        except Exception as exc:  # noqa: BLE001 - surface host failure in the test
            errors.append(exc)

    thread = threading.Thread(target=serve, name="d09-pack-host")
    thread.start()
    try:
        result = operation()
    finally:
        if thread.is_alive():
            host.shutdown()
        thread.join(timeout=30)
    assert not thread.is_alive(), "pack host did not settle the managed task"
    assert not errors, errors[0] if errors else None
    return result


def _latest_scene_task(client: AstridClient, project_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    tasks = paged_rows(client._remote._transport.list_project_tasks, project_id, limit=50)
    assert tasks
    rows = [row for row in tasks if isinstance(row, dict)]
    scene = next(
        row for row in reversed(rows)
        if row.get("capability") == "rendering.timeline_visualize"
        and row.get("state") in {"succeeded", "completed"}
    )
    task_id = str(scene.get("task_id") or scene.get("id"))
    managed = client.tasks.list_managed_outputs(task_id)
    assert managed.ok and managed.data
    output_rows = managed.data[0] if isinstance(managed.data, (list, tuple)) else managed.data
    assert isinstance(output_rows, list)
    return scene, [row for row in output_rows if isinstance(row, dict)]


def _assert_managed_scene_bundle(client: AstridClient, rows: list[dict[str, Any]]) -> dict[str, Any]:
    bundles = [row for row in rows if row.get("output_port") == "filmstrip_bundle"]
    assert len(bundles) == 1
    row = bundles[0]
    digest = str(row["digest"])
    data = client.media.read_bytes(digest)
    assert len(data) == row["size"]
    assert hashlib.sha256(data).hexdigest() == digest.removeprefix("sha256:")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert archive.namelist() == ["manifest.json", "scene-answers.json"]
        manifest = json.loads(archive.read("manifest.json"))
        payload = json.loads(archive.read("scene-answers.json"))
    assert manifest["kind"] == "timeline_filmstrip"
    assert payload["answers"]
    assert payload["scene_clips"]["title"]["address"] == "c01.title"
    return {"row": row, "manifest": manifest, "payload": payload}


def _render(client: AstridClient, host: GenericPackHost, project_id: str) -> None:
    result = _run_one(
        host,
        lambda: client.invoke_result(
            "rendering.render",
            kind="executor",
            project=project_id,
            inputs={
                "timeline_ref": "main",
                "selector": "rendering.remotion",
                "output_name": "d09-base.mp4",
                "backend_config": {
                    "rendering.remotion": {
                        "project_dir": os.environ["ASTRID_REMOTION_PROJECT_DIR"],
                        "composition_id": "TimelineComposition",
                    }
                },
            },
            wait=True,
            timeout_seconds=300,
            poll_seconds=0.05,
        ),
    )
    assert result.ok, result.to_dict()


def test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle(
    tmp_path: Path, real_runtime: Any
) -> None:
    daemon = real_runtime()
    with _connect(daemon) as client:
        project_id, parent_revision = _publish(client, suffix="positive")
        host = _host(daemon, tmp_path)
        _render(client, host, project_id)

        host = _host(daemon, tmp_path)
        saved_spans, saved_context = _run_one(
            host,
            lambda: timeline_filmstrip._invoke_scene_only(
                {"timeline_ref": "main"}, project=project_id, client=client
            ),
        )
        assert saved_spans[0].cls == "COVERED"
        assert saved_context["snapshot_label"] == {
            "status": "committed",
            "label": f"committed revision {parent_revision}",
            "actual_revision_id": parent_revision,
            "base_revision_id": None,
        }
        _, saved_rows = _latest_scene_task(client, project_id)
        saved_bundle = _assert_managed_scene_bundle(client, saved_rows)
        assert saved_bundle["payload"]["snapshot_label"]["status"] == "committed"

        parent = client._remote._transport.get_project_parent_composition_revision(
            project_id, "main", parent_revision
        )
        preview_bundle = open_authoring_bundle(
            parent, shot_revisions=[], internal_timeline_revisions=[]
        )
        preview_bundle["parent"]["config"]["clips"][0]["text"]["content"] = "candidate"
        candidate = preview_authoring_candidate(preview_bundle)
        host = _host(daemon, tmp_path)
        candidate_spans, candidate_context = _run_one(
            host,
            lambda: timeline_filmstrip._invoke_scene_only(
                {"timeline_ref": "main", "authoring_preview": candidate},
                project=project_id,
                client=client,
            ),
        )
        assert candidate_spans[0].cls == "COVERED"
        assert candidate_context["snapshot_label"]["status"] == "candidate"
        assert candidate_context["snapshot_label"]["base_revision_id"] == parent_revision
        _, candidate_rows = _latest_scene_task(client, project_id)
        candidate_bundle = _assert_managed_scene_bundle(client, candidate_rows)
        assert candidate_bundle["payload"]["snapshot_label"]["status"] == "candidate"
        assert candidate_bundle["payload"]["snapshot_label"]["base_revision_id"] == parent_revision

        stale_context = dict(saved_context)
        stale_context["capture_identity"] = "sha256:" + "0" * 64
        stale_spans = timeline_filmstrip._scene_only_spans(
            {"ok": True, "outputs": {"managed_outputs": [saved_bundle["row"]]}},
            stale_context,
            client=client,
        )
        assert stale_spans[0].cls == "UNAVAILABLE"
        assert "scene source binding unavailable" in stale_spans[0].findings
