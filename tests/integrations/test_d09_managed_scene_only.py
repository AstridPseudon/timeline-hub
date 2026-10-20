"""D09 proof through Runtime admission, the real pack host, and Scene."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest

from astrid.core.timeline.authoring_bundle import open_authoring_bundle, preview_authoring_candidate
from astrid.sdk import AstridClient, timeline_filmstrip
from tests.packs.rendering.real_pack_host import RealPackHost, start_real_pack_host

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
    monkeypatch.setenv("ASTRID_CHECKOUT", str(ROOT))
    profile_root = tmp_path / "public13-root"
    profile_root.mkdir()
    (profile_root / "astrid").symlink_to(ROOT / "astrid", target_is_directory=True)
    private_profile = profile_root / "remotion"
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
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join((str(ROOT), str(SCHEMA))))
    assert private_profile.is_dir()
    assert NODE.is_file() and os.access(NODE, os.X_OK)
    package = json.loads((private_profile / "package.json").read_text(encoding="utf-8"))
    assert package["dependencies"]["@banodoco/timeline-composition"] == (
        "file:artifacts/banodoco-timeline-composition-0.0.13.tgz"
    )
    from astrid.sdk.host_bootstrap import _prepare_render_validation

    launch_environment = dict(os.environ)
    _prepare_render_validation(
        ROOT,
        launch_environment,
        tmp_path,
        sys.executable,
        pack_roots=(ROOT / "astrid" / "packs" / "rendering",),
    )
    for name, value in launch_environment.items():
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
            "app": {"astrid": {"opaque": ["title", None]}},
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
    from astrid.sdk.timeline._clip_commands import capture_clip_add
    from astrid.sdk.timeline.capture import capture_track_create

    def commit(commands: list[dict[str, Any]], key: str) -> dict[str, Any]:
        history = client.timelines.history(project_id, "main")
        assert history.ok, history.as_dict()
        head = history.data["head"]
        body = {
            "api_version": 1,
            "project_id": project_id,
            "timeline_id": "main",
            "base_revision_id": head["revision_id"],
            "base_publication_id": head["publication_id"],
            "commands": commands,
        }
        result = client.timelines.commit(project_id, "main", body, idempotency_key=key)
        assert result.ok, result.as_dict()
        assert isinstance(result.data, dict)
        return result.data

    opened = client.timelines.open_bundle(project_id, "main")
    assert opened.ok, opened.as_dict()
    bundle = opened.data["bundle"]
    track = capture_track_create(
        bundle,
        "parent",
        {"id": "picture", "kind": "visual", "label": "Picture", "role": "output"},
    )
    commit([track], f"d09-track-{suffix}")
    opened = client.timelines.open_bundle(project_id, "main")
    assert opened.ok, opened.as_dict()
    clip = capture_clip_add(opened.data["bundle"], "parent", _config("saved")["clips"][0])
    accepted = commit([clip], f"d09-clip-{suffix}")
    parent_revision = str(accepted["accepted_revision_id"])
    return project_id, parent_revision


def _host(daemon: Any) -> RealPackHost:
    daemon.support_root.chmod(0o700)
    discovery = daemon.support_root / "discovery.json"
    value = json.loads(discovery.read_text(encoding="utf-8"))
    return start_real_pack_host(
        realm_dir=daemon.root,
        support_dir=daemon.support_root,
        discovery_file=discovery,
        source_checkout=ROOT,
        runtime_instance_id=value["runtime_instance_id"],
    )


def _run_one(host: RealPackHost, operation: Any) -> Any:
    operation_error: BaseException | None = None
    try:
        result = operation()
    except BaseException as exc:
        operation_error = exc
        raise
    finally:
        cleanup_error: BaseException | None = None
        try:
            host.close()
        except BaseException as exc:
            cleanup_error = exc
        if cleanup_error is not None and operation_error is None:
            raise cleanup_error
    return result


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
    assert payload["scene_clips"]["title"]["address"] == "title"
    return {"row": row, "manifest": manifest, "payload": payload}


def test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle(
    tmp_path: Path, real_runtime: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    daemon = real_runtime(authoring_profile="astrid")
    with _connect(daemon) as client:
        project_id, parent_revision = _publish(client, suffix="positive")
        parent = client._remote._transport.get_project_parent_composition_revision(
            project_id, "main", parent_revision
        )
        preview_bundle = open_authoring_bundle(
            parent, shot_revisions=[], internal_timeline_revisions=[]
        )
        preview_bundle["parent"]["config"]["clips"][0]["text"]["content"] = "candidate"
        preview_bundle["parent"]["clips"][0]["text"]["content"] = "candidate"
        candidate = preview_authoring_candidate(preview_bundle)
        host = _host(daemon)
        last_result: dict[str, Any] = {}
        from astrid.sdk import invocation

        original_invoke = invocation._invoke_internal_result

        def capture_result(*args: Any, **kwargs: Any) -> Any:
            result = original_invoke(*args, **kwargs)
            last_result["value"] = result
            return result

        monkeypatch.setattr(invocation, "_invoke_internal_result", capture_result)
        saved_spans, saved_context = _run_one(
            host,
            lambda: timeline_filmstrip._invoke_scene_only(
                {"timeline_ref": "main"}, project=project_id, client=client
            ),
        )
        result = last_result["value"]
        assert result.ok, result.error
        assert saved_spans[0].cls != "UNAVAILABLE", {
            "findings": saved_spans[0].findings,
            "context": saved_context,
            "result": result.to_dict(),
        }
        saved_rows = result.outputs["managed_outputs"]
        saved_bundle = _assert_managed_scene_bundle(client, saved_rows)
        assert saved_bundle["payload"]["snapshot_label"] == {
            "status": "committed",
            "label": f"committed revision {parent_revision}",
            "actual_revision_id": parent_revision,
            "base_revision_id": None,
        }

        host = _host(daemon)
        candidate_spans, candidate_context = _run_one(
            host,
            lambda: timeline_filmstrip._invoke_scene_only(
                {"timeline_ref": "main", "authoring_preview": candidate},
                project=project_id,
                client=client,
            ),
        )
        result = last_result["value"]
        assert result.ok, result.error
        assert candidate_spans[0].cls != "UNAVAILABLE", {
            "findings": candidate_spans[0].findings,
            "context": candidate_context,
            "result": result.to_dict(),
        }
        candidate_rows = result.outputs["managed_outputs"]
        candidate_bundle = _assert_managed_scene_bundle(client, candidate_rows)
        assert candidate_bundle["payload"]["snapshot_label"] == {
            "status": "candidate",
            "label": f"unsaved candidate based on committed revision {parent_revision}",
            "actual_revision_id": None,
            "base_revision_id": parent_revision,
        }

        stale_row = dict(saved_bundle["row"])
        stale_provenance = dict(stale_row["provenance"])
        stale_provenance["video_digest"] = "sha256:" + "0" * 64
        stale_row["provenance"] = stale_provenance
        stale_spans = timeline_filmstrip._scene_only_spans(
            {"ok": True, "outputs": {"managed_outputs": [stale_row]}},
            saved_context,
            client=client,
        )
        assert stale_spans[0].cls == "UNAVAILABLE"
        assert "scene source binding unavailable" in stale_spans[0].findings
