"""A headless shell holding authored content is never overwritten by an empty-default publication.

The shell is installed by direct rows (a historical image); the legacy publisher
that once wrote such shells is retired and must refuse before any write.
"""
from __future__ import annotations

import json

import pytest

from runtime_protocol.errors import RetiredRouteError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import digest

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
        with pytest.raises(RetiredRouteError) as error:
            _publish_empty(runtime, project, key)
        assert error.value.details["reason"] == "timeline_commit_required"
        assert _dump(runtime) == before
    assert _stored(runtime) == original
    assert json.loads(original) == AUTHORED
    assert runtime.store.conn.execute("SELECT publication_id FROM parent_composition_heads WHERE timeline_id='main'").fetchone()[0] is None


def test_empty_default_over_empty_headless_shell_has_no_legacy_writer(service):
    runtime, project = service
    _shell(runtime, project, EMPTY)
    before = _dump(runtime)
    with pytest.raises(RetiredRouteError):
        _publish_empty(runtime, project, "empty-default")
    assert _dump(runtime) == before


def test_fresh_creation_is_unchanged(service):
    runtime, project = service
    created = runtime.create_timeline(project, "second", idempotency_key="create-second")
    assert runtime.create_timeline(project, "second", idempotency_key="create-second") == created
