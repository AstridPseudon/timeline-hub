"""A headless shell holding authored content is never overwritten by an empty-default publication.

The shell is installed by direct rows (a historical image). The composition-revisions
route stays available for an empty timeline, but its head guard refuses the overwrite
before any write.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from runtime_protocol.errors import ConflictError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import digest
from runtime_protocol.util import canonical_json

AUTHORED = {
    "config": {"fps": 24, "extension": {"keep": [None, False, {"__proto__": 1}]}},
    "registry": {"assets": {"a": {"object_id": "x", "type": "video"}}},
    "clips": [{"id": "edited", "asset": "a", "at": 0, "duration": 3}],
    "occurrences": [],
}
EMPTY = {"config": {}, "registry": {}, "clips": [], "occurrences": []}


@pytest.fixture
def service(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    runtime = RuntimeService(root)
    project = runtime.create_project({"slug": "shell", "name": "Shell"}, idempotency_key="project")["id"]
    runtime.create_timeline(project, "main", idempotency_key="create-main")
    try:
        yield runtime, project
    finally:
        runtime.close()


def _shell(runtime, project, payload):
    conn = runtime.store.conn
    with runtime.store._mutex, runtime.store._transaction():
        conn.execute(
            "INSERT INTO parent_composition_revisions(id, project_id, timeline_id, payload_json, content_digest, created_at) VALUES (?,?,?,?,?,?)",
            ("shell-rev", project, "main", json.dumps(payload), digest(payload), "2026-01-01T00:00:00Z"))
        conn.execute(
            "INSERT INTO composition_revision_dependencies(parent_revision_id, dependency_kind, dependency_id, content_digest, ordinal) VALUES (?,?,?,?,0)",
            ("shell-rev", "object", "x", "0" * 64))
        conn.execute(
            "INSERT OR REPLACE INTO parent_composition_heads(timeline_id, project_id, revision_id, publication_id, updated_at) VALUES (?,?,?,NULL,?)",
            ("main", project, "shell-rev", "2026-01-01T00:00:00Z"))


def _publish_empty(runtime, project, key):
    return runtime.publish_parent_composition(project, "main", {
        "project_id": project, "timeline_id": "main", "expected_head": None,
        "parent_revision_id": "empty-default", "parent_composition": EMPTY,
    }, idempotency_key=key)


def _dump(runtime):
    return tuple(runtime.store.conn.iterdump())


def _stored(runtime):
    return runtime.store.conn.execute("SELECT payload_json FROM parent_composition_revisions WHERE id='shell-rev'").fetchone()[0]


def test_empty_default_over_authored_headless_shell_is_refused_untouched(service):
    runtime, project = service
    _shell(runtime, project, AUTHORED)
    original = _stored(runtime)
    before = _dump(runtime)
    for key in ("empty-default", "empty-default"):  # the retry is refused the same way
        with pytest.raises(ConflictError) as error:
            _publish_empty(runtime, project, key)
        assert error.value.details["reason"] == "stale_head"
        assert _dump(runtime) == before
    assert _stored(runtime) == original
    assert json.loads(original) == AUTHORED
    assert runtime.store.conn.execute("SELECT publication_id FROM parent_composition_heads WHERE timeline_id='main'").fetchone()[0] is None


def test_empty_default_over_empty_headless_shell_is_refused_untouched(service):
    runtime, project = service
    _shell(runtime, project, EMPTY)
    before = _dump(runtime)
    with pytest.raises(ConflictError) as error:
        _publish_empty(runtime, project, "empty-default")
    assert error.value.details["reason"] == "stale_head"
    assert _dump(runtime) == before


def test_empty_default_on_a_fresh_timeline_is_accepted_and_replays(service):
    runtime, project = service
    accepted = _publish_empty(runtime, project, "empty-default")
    assert accepted["data"]["revision_id"] == "empty-default" and accepted["data"]["old_head"] is None
    assert runtime.store.conn.execute("SELECT revision_id, publication_id FROM parent_composition_heads WHERE timeline_id='main'").fetchone()[:] == ("empty-default", None)
    before = _dump(runtime)
    assert _publish_empty(runtime, project, "empty-default") == accepted
    assert _dump(runtime) == before


def _hide_content(runtime, project, content):
    with runtime.store.conn:
        runtime.store.conn.execute(
            "INSERT INTO project_documents VALUES (?, ?, ?, ?, 1, ?, ?)",
            ("timeline:main", project, "timeline", canonical_json(content), "2026-10-20T00:00:00Z", "2026-10-20T00:00:00Z"))


def test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched(service):
    """App's probe: head is None publicly while project_documents holds authored content."""
    runtime, project = service
    fixture = json.loads((Path(__file__).parent / "fixtures" / "headless_hidden_content_candidate.json").read_text())
    content = {"slug": "edited", "config": fixture["hiddenAuthored"], "registry": {"assets": {}}}
    _hide_content(runtime, project, content)
    assert runtime.get_project_timeline(project, "main")["head_revision_id"] is None
    body = {**copy.deepcopy(fixture["submitted"]), "project_id": project, "timeline_id": "main"}
    before = _dump(runtime)
    for key in ("repair-shell", "repair-shell"):  # the retry is refused the same way
        with pytest.raises(ConflictError) as error:
            runtime.publish_parent_composition(project, "main", body, idempotency_key=key)
        assert error.value.details["reason"] == "headless_content_not_empty"
        assert _dump(runtime) == before
    stored = runtime.store.conn.execute("SELECT content_json FROM project_documents WHERE id='timeline:main'").fetchone()[0]
    assert json.loads(stored) == content


def test_genuinely_empty_headless_timeline_still_accepts_expected_head_null(service):
    runtime, project = service
    _hide_content(runtime, project, {"config": {}, "registry": {"assets": {}}, "clips": []})
    assert _publish_empty(runtime, project, "empty-default")["data"]["revision_id"] == "empty-default"


def test_cas_correct_republish_after_reading_the_head_is_accepted(service):
    runtime, project = service
    _publish_empty(runtime, project, "empty-default")
    again = runtime.publish_parent_composition(project, "main", {
        "project_id": project, "timeline_id": "main", "expected_head": "empty-default",
        "parent_revision_id": "second", "parent_composition": AUTHORED,
    }, idempotency_key="second")
    assert again["data"]["revision_id"] == "second" and again["data"]["old_head"] == "empty-default"


def test_fresh_creation_is_unchanged(service):
    runtime, project = service
    created = runtime.create_timeline(project, "second", idempotency_key="create-second")
    assert runtime.create_timeline(project, "second", idempotency_key="create-second") == created


def _scoped_rows(runtime, project, kind):
    conn = runtime.store.conn
    with runtime.store._mutex, runtime.store._transaction():
        if kind == "timeline_references":
            conn.execute("INSERT INTO timeline_references(id, timeline_id, object_id, role) VALUES ('r1','main','obj',NULL)")
        elif kind == "timeline_shots":
            conn.execute("INSERT INTO timeline_shots(id, timeline_id, start_ms, duration_ms, reference_ids_json) VALUES ('s1','main',0,1000,'[]')")
        elif kind == "snapshot":
            conn.execute("INSERT INTO timeline_revisions(timeline_id, version, shots_json, references_json, created_at) VALUES ('main',2,'[{\"id\":\"s1\"}]','[]','2026-01-01T00:00:00Z')")
        else:  # a dependency row on an unpublished parent revision of the headless timeline
            conn.execute(
                "INSERT INTO parent_composition_revisions(id, project_id, timeline_id, payload_json, content_digest, created_at) VALUES (?,?,?,?,?,?)",
                ("orphan-rev", project, "main", json.dumps(EMPTY), digest(EMPTY), "2026-01-01T00:00:00Z"))
            conn.execute(
                "INSERT INTO composition_revision_dependencies(parent_revision_id, dependency_kind, dependency_id, content_digest, ordinal) VALUES (?,?,?,?,0)",
                ("orphan-rev", "object", "x", "0" * 64))


@pytest.mark.parametrize("kind", ["timeline_references", "timeline_shots", "snapshot", "dependency"])
def test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched(service, kind):
    runtime, project = service
    _scoped_rows(runtime, project, kind)
    before = _dump(runtime)
    for key in ("scope-deny", "scope-deny"):  # the retry is refused the same way
        with pytest.raises(ConflictError) as error:
            _publish_empty(runtime, project, key)
        assert error.value.details["reason"] == "headless_content_not_empty"
        assert _dump(runtime) == before
