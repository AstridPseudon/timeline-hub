"""Unchanged intermediate images through the registered Runtime provider."""
from __future__ import annotations

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("later_edit, separate_steps", [(False, True), (True, False), (True, True)],
                         ids=["unchanged-final-parent", "grouped-step", "unchanged-intermediate-parent"])
def test_unchanged_step_preserves_its_parent_image(tmp_path, later_edit, separate_steps):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    try:
        project = service.create_project({"slug": "images", "name": "Images"})["id"]
        service.create_timeline(project, "film", idempotency_key="birth")
        head = service.get_project_timeline(project, "film")
        first = {"id": "first", "kind": "visual", "label": "Same"}
        second = {"id": "second", "kind": "visual"}
        calls = [
            {"schema_version": 1, "op": "track.create", "version": "1", "select": "parent",
             "args": {"row": first}},
            {"schema_version": 1, "op": "track.set", "version": "1",
             "select": "parent/track:first", "args": {"values": {"label": "Same"}, "clear": []}},
        ]
        if later_edit:
            calls.append({"schema_version": 1, "op": "track.create", "version": "1",
                          "select": "parent", "args": {"row": second}})
        request = {
            "api_version": 1, "project_id": project, "timeline_id": "film",
            "base_revision_id": head["head_revision_id"],
            "base_publication_id": head["head_publication_id"], "commands": calls,
            "label": "Keep the same label", "merge": "fields", "reads": [],
            "steps": [{"id": str(index), "label": "Edit track", "intent": "", "tags": [],
                       "command_ordinals": [index], "patch": []} for index in range(len(calls))],
            "dry_run": False, "source": {"via": "python"},
        }
        if not separate_steps:
            request["steps"] = [{"id": "all", "label": "Edit tracks", "intent": "", "tags": [],
                                 "command_ordinals": list(range(len(calls))), "patch": []}]
        result = service.commit_timeline(
            project, "film", request, idempotency_key="edit", publisher="editor",
            invocation_path=route_path(project, "film"), authorize=lambda: None)
        assert result["data"]["status"] == "accepted"
        assert result["receipt"]["result"] == result["data"]
        assert result["data"]["canonical_document"]["parent_revision"]["payload"]["config"][
            "tracks"] == ([first, second] if later_edit else [first])
        history = service.list_timeline_commits(project, "film", authorize=lambda: None)["items"]
        if separate_steps:
            assert history[-1]["records"]["steps"][1]["patch"] == []
    finally:
        service.close()
