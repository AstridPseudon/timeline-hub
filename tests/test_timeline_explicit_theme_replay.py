"""Gate2: an explicit project Theme remains the identity of a retried render."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from runtime_protocol.errors import ConflictError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

pytestmark = pytest.mark.integration


def _files(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _state(service: RuntimeService, project: str) -> dict:
    """Observe admission/history/CAS state only through public APIs and files."""
    return {
        "tasks": copy.deepcopy(service.list_project_tasks(project)["items"]),
        "runs": copy.deepcopy(service.list_project_runs(project)["items"]),
        "history": copy.deepcopy(
            service.list_timeline_commits(project, "main", authorize=lambda: None)["items"]
        ),
        "cas": _files(service.store.cas_root),
        "staging": _files(service.store.staging_root),
    }


def _theme(service: RuntimeService, project: str, *, name: str, key: str) -> tuple[dict, bytes]:
    authored = json.dumps(
        {
            "id": name,
            "visual": {
                "canvas": {"width": 853, "height": 479, "fps": 23.976},
                "background": {"color": "#17243b" if name == "ThemeA" else "#4b2138", "opacity": 0.73},
                "font": {"family": "Project Theme Sans", "weight": 640},
            },
            "generation": {"references": [], "assets": []},
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    imported = service.ingest(
        project,
        authored,
        media_type="application/json",
        original_name="theme.json",
        idempotency_key=key,
    )["data"]
    descriptor = {
        "object_id": imported["object_id"],
        "digest": imported["digest"],
        "filename": "theme.json",
    }
    assert service.object(descriptor["object_id"])[1] == authored
    return descriptor, authored


def _render_request(project: str, version: int, theme: dict, *, key: str) -> dict:
    return {
        "project": project,
        "capability_id": "rendering.render",
        "capability_digest": "sha256:" + hashlib.sha256(b"rendering.render").hexdigest(),
        "input_object_ids": [theme["object_id"]],
        "idempotency_key": key,
        "spec": {
            "family": "render",
            "params": {"timeline_ref": "main", "expected_version": version, "selector": "rendering.remotion"},
            "inputs": {"theme": copy.deepcopy(theme)},
            "input_digests": [{"name": "theme", "digest": theme["digest"]}],
        },
    }


def _edit_head(service: RuntimeService, project: str) -> dict:
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document

    current = service.get_project_timeline(project, "main")
    document = service._timeline_commits()[0].revision_closure(
        project, "main", current["head_revision_id"]
    )
    command = capture_track_create(
        bundle_from_document(document),
        "parent",
        {"id": "picture", "kind": "visual", "role": "output"},
    )
    return service.commit_timeline(
        project,
        "main",
        {
            "api_version": 1,
            "project_id": project,
            "timeline_id": "main",
            "base_revision_id": current["head_revision_id"],
            "base_publication_id": current["head_publication_id"],
            "commands": [command],
            "source": {"via": "python"},
        },
        idempotency_key="newer-canonical-head",
        publisher="explicit-theme-replay",
        invocation_path=route_path(project, "main"),
        authorize=lambda: None,
    )


def test_explicit_theme_retry_reuses_original_admission_after_head_restart(tmp_path, astrid_importable, monkeypatch):
    def renderer_stopped(*args, **kwargs):
        raise AssertionError("render admission or edit imported the renderer")

    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    monkeypatch.setattr(service_module, "evaluate_closure", renderer_stopped)
    monkeypatch.setattr(visual_seam, "evaluate_closure", renderer_stopped)
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    project = service.create_project({"slug": "theme-replay", "name": "Theme replay"}, idempotency_key="project")["id"]
    service.create_timeline(project, "main", idempotency_key="timeline")
    capability_digest = "sha256:" + hashlib.sha256(b"rendering.render").hexdigest()
    service.register_capability({"capability_id": "rendering.render", "definition_digest": capability_digest})
    service.register_executor({"executor_id": "stopped-renderer", "capabilities": ["rendering.render"]})

    try:
        theme_a, bytes_a = _theme(service, project, name="ThemeA", key="theme-a")
        theme_b, bytes_b = _theme(service, project, name="ThemeB", key="theme-b")
        assert bytes_a != bytes_b
        version = service.get_project_timeline(project, "main")["version"]
        request = _render_request(project, version, theme_a, key="render-theme-replay")

        real_create_task = service.create_task
        lost_ack = {}

        def admit_then_lose_ack(*args, **kwargs):
            result = real_create_task(*args, **kwargs)
            lost_ack["result"] = copy.deepcopy(result)
            raise ConnectionError("simulated lost admission acknowledgement")

        monkeypatch.setattr(service, "create_task", admit_then_lose_ack)
        with pytest.raises(ConnectionError, match="lost admission acknowledgement"):
            service.create_task(copy.deepcopy(request))
        monkeypatch.setattr(service, "create_task", real_create_task)
        original = lost_ack["result"]
        original_task = original["task"]
        original_snapshot_ref = original_task["spec"]["spec"]["timeline_snapshot_ref"]
        original_snapshot = service.object(original_snapshot_ref["digest"])[1]
        assert original_task["spec"]["spec"]["inputs"]["theme"] == theme_a
        assert service.object(theme_a["digest"])[1] == bytes_a

        accepted = _edit_head(service, project)
        assert accepted["data"]["accepted_revision_id"] != original_task["spec"]["spec"]["inputs"]["timeline_authority"]["parent_revision_id"]

        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        before_replay = _state(service, project)
        replay = service.create_task(copy.deepcopy(request))

        assert replay == original
        assert replay["task"]["id"] == original_task["id"]
        assert replay["run"]["id"] == original["run"]["id"]
        assert replay["task"]["spec"]["spec"]["timeline_snapshot_ref"] == original_snapshot_ref
        assert replay["task"]["spec"]["spec"]["inputs"]["theme"] == theme_a
        assert service.object(original_snapshot_ref["digest"])[1] == original_snapshot
        assert service.object(theme_a["digest"])[1] == bytes_a
        assert len(service.list_project_tasks(project)["items"]) == 1
        assert _state(service, project) == before_replay

        changed = copy.deepcopy(request)
        changed["input_object_ids"] = [theme_b["object_id"]]
        changed["spec"]["inputs"]["theme"] = copy.deepcopy(theme_b)
        changed["spec"]["input_digests"] = [{"name": "theme", "digest": theme_b["digest"]}]
        before_refusal = _state(service, project)
        with pytest.raises(ConflictError):
            service.create_task(changed)
        assert _state(service, project) == before_refusal
    finally:
        service.close()
