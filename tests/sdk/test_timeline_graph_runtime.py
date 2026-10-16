"""Joined producer/Runtime proof with an explicitly selected source tree only."""
import copy
import os
import sys
from pathlib import Path

import pytest
import test_timeline_graph_commands as graph_fixtures
from test_timeline_graph_commands import add_call, shot_call  # noqa: F401
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command

closure = graph_fixtures.closure
pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def runtime(tmp_path, closure):
    source = os.environ.get("ASTRID_GRAPH_RUNTIME_ROOT")
    if not source:
        pytest.skip("explicit Runtime source required for this coupled proof")
    sys.path.insert(0, source)
    import runtime_protocol
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    assert Path(runtime_protocol.__file__).resolve().is_relative_to(Path(source).resolve())
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project(dict(slug="graph", name="Graph fixture"), idempotency_key="project")["id"]
    service.create_timeline(project, "t", idempotency_key="timeline")
    service.create_timeline(project, "inner", idempotency_key="internal-timeline")
    pub = dict(project_id=project, timeline_id="t", expected_head=None, parent_revision_id="rev-0", parent_composition=copy.deepcopy(closure["parent_revision"]["payload"]), shot_revisions=[{k: v for k, v in closure["shot_revisions"][0].items() if k not in {"project_id", "content_digest"}}], internal_timeline_revisions=[{k: v for k, v in closure["internal_timeline_revisions"][0].items() if k not in {"project_id", "content_digest"}}])
    pub["shot_revisions"][0]["payload"]["items"] = []
    pub["internal_timeline_revisions"][0]["payload"]["clips"] = [dict(id="picture", clipType="media", track="picture", at=0, hold=1)]
    service.publish_parent_composition(project, "t", pub, idempotency_key="initial")
    service.register_timeline_commit_provider(RuntimeCommitService())
    try:
        yield service, project
    finally:
        service.close()
        sys.path.remove(source)


def body(service, project, key, commands, base=None):
    head = service.head(project, "t")
    return dict(api_version=1, project_id=project, timeline_id="t", request_id=key, session_id="graph-session", session_sequence=1, base_revision_id=base or head["revision_id"], base_publication_id=head["publication_id"], scope=dict(target="parent", complete=[], projection_version=1), change=dict(commands=commands), source=dict(via="python"), dry_run=False)


def commit(service, project, request):
    return service.commit_timeline(project, "t", request, idempotency_key=request["request_id"], identity=dict(actor="graph-fixture", scopes=["projects:write"]))


def test_actual_commit_shared_source_add_retry_reload_and_one_undo(runtime, monkeypatch):
    service, project = runtime
    identity = dict(actor="graph-fixture", scopes=["projects:write"])
    first = body(service, project, "rename", [shot_call(values=dict(name="selected"))])
    before_port = service._request_commit_port(first, identity)
    before = RuntimeCommitService._load_revision(before_port, first, "rev-0")
    result = commit(service, project, first)
    assert result["status"] == "accepted", result
    exact = service._commit_revision_closure(project, "t", result["accepted_revision_id"])
    sibling = next(r for r in exact["parent_revision"]["payload"]["occurrences"] if r["occurrence_id"] == "b")
    assert sibling["shot_revision_id"] == "shot-1"
    assert service.get_project_shot_revision(project, "s", "shot-1")["payload"]["provenance"]["name"] == "old"
    # Pinned source remains rev-0 even though the request base has moved.
    second = body(service, project, "duplicate", [add_call()])
    durable = []
    def lose_response(value):
        durable.append(value)
        raise TimeoutError("response lost after durable acceptance")
    monkeypatch.setattr(service, "_after_timeline_commit", lose_response, raising=False)
    with pytest.raises(TimeoutError):
        commit(service, project, second)
    assert len(durable) == 1
    monkeypatch.delattr(service, "_after_timeline_commit")
    added = commit(service, project, second)
    assert added == durable[0]
    assert added["id_map"]["occurrence:new::shot_revision_id"] == "new-shot-rev"
    after_port = service._request_commit_port(body(service, project, "read", []), identity)
    after = RuntimeCommitService._load_revision(after_port, second, added["accepted_revision_id"])
    previous_body = body(service, project, "read-previous", [], base=result["accepted_revision_id"])
    previous_port = service._request_commit_port(previous_body, identity)
    previous = RuntimeCommitService._load_revision(previous_port, previous_body, result["accepted_revision_id"])
    inverse = inverse_command(added["change"]["commands"], previous, after, added["accepted_publication_id"])
    undo = commit(service, project, body(service, project, "undo", [inverse]))
    assert undo["status"] == "accepted", undo
    restored = service._commit_revision_closure(project, "t", undo["accepted_revision_id"])
    assert {r["occurrence_id"] for r in restored["parent_revision"]["payload"]["occurrences"]} == {"a", "b"}
    assert len(service.revisions(project, "t", {})) == 3
    assert before["base_parent"]["revision_id"] == "rev-0"


def test_actual_moved_head_rebase_and_conflict(runtime):
    from test_timeline_graph_commands import source

    service, project = runtime
    pending = body(service, project, "pending", [shot_call(values=dict(name="ours"))])
    other = dict(op="shot.set", select="occurrence:b/shot", args=dict(source=source("b"), values=dict(name="theirs")))
    advanced = commit(service, project, body(service, project, "advance", [other]))
    assert advanced["status"] == "accepted", advanced
    rebased = commit(service, project, pending)
    assert rebased["status"] == "accepted", rebased
    assert rebased["rebased_onto"] == advanced["accepted_revision_id"]
    conflict = commit(service, project, body(service, project, "stale-selected", [shot_call(values=dict(name="conflicting"))], base="rev-0"))
    assert conflict["status"] == "conflict", conflict


def test_exact_shot_source_outside_parent_closure(runtime):
    service, project = runtime
    original = service._commit_revision_closure(project, "t", "rev-0")
    service.create_timeline(project, "donor", idempotency_key="donor")
    internal = copy.deepcopy(original["internal_timeline_revisions"][0])
    internal.update(timeline_id="donor", revision_id="donor-int")
    shot = copy.deepcopy(original["shot_revisions"][0])
    shot.update(shot_id="donor-shot", revision_id="donor-rev", internal_timeline_revision_id="donor-int")
    shot["payload"]["internal_timeline_revision_id"] = "donor-int"
    for row in (internal, shot):
        row.pop("project_id", None)
        row.pop("content_digest", None)
    parent = copy.deepcopy(original["parent_revision"]["payload"])
    parent["occurrences"] = [dict(parent["occurrences"][0], shot_id="donor-shot", shot_revision_id="donor-rev")]
    service.publish_parent_composition(project, "donor", dict(project_id=project, timeline_id="donor", expected_head=None, parent_composition=parent,
        shot_revisions=[shot], internal_timeline_revisions=[internal]), idempotency_key="donor-publish")
    ref = dict(shot_id="donor-shot", shot_revision_id="donor-rev", internal_revision_id="donor-int")
    operation = add_call("linked", source=ref)
    result = commit(service, project, body(service, project, "direct-donor", [operation]))
    assert result["status"] == "accepted", result
    exact = service._commit_revision_closure(project, "t", result["accepted_revision_id"])
    added = next(row for row in exact["parent_revision"]["payload"]["occurrences"] if row["occurrence_id"] == "new")
    assert (added["shot_id"], added["shot_revision_id"]) == ("donor-shot", "donor-rev")
    assert service.get_project_shot_revision(project, "donor-shot", "donor-rev")["internal_timeline_id"] == "donor"
