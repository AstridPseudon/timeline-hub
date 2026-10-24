"""A headless shell holding authored content is never overwritten by publication.

The shell is installed by direct rows (a historical image). Current commit authority
refuses an absent public head before any provider or publication write; the retired
composition-revisions route remains a dedicated 410 boundary.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from runtime_protocol.errors import RetiredRouteError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import digest, route_path
from runtime_protocol.util import canonical_json
from test_timeline_commit_port import PreparedProvider, prepared

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
    runtime.register_timeline_commit_provider(
        PreparedProvider(lambda context, port: port.accept(prepared(context, port, same=True)))
    )
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


def _commit(runtime, project, key, *, base=None, replacement=None):
    base = base or runtime.get_project_timeline(project, "main")
    if replacement is None:
        command = {
            "schema_version": 1,
            "op": "clip.move",
            "version": "1",
            "select": "parent/clip:clip-1",
            "args": {"on": 2},
        }
        step_patch = []
    else:
        change = {
            "op": "set",
            "ref": "parent",
            "path": [],
            "before": {"state": "absent"},
            "value": copy.deepcopy(replacement),
        }
        command = {
            "schema_version": 1,
            "op": "doc.patch",
            "version": "1",
            "select": None,
            "args": {"changes": [change]},
        }
        step_patch = [change]
    return runtime.commit_timeline(
        project,
        "main",
        {
            "api_version": 1,
            "project_id": project,
            "timeline_id": "main",
            "base_revision_id": base["head_revision_id"] if "head_revision_id" in base else base["revision_id"],
            "base_publication_id": base["head_publication_id"] if "head_publication_id" in base else base["publication_id"],
            "commands": [command],
            "label": "Headless publication probe",
            "steps": [{
                "id": "headless-probe",
                "label": "Headless publication probe",
                "intent": "prove current publication authority",
                "tags": ["headless"],
                "command_ordinals": [0],
                "patch": step_patch,
            }],
            "merge": "fields",
            "reads": [],
            "dry_run": False,
            "source": {"via": "python", "detail": "headless overwrite family"},
            "rationale": "Preserve the headless publication boundary.",
            "group_id": "headless-overwrite-family",
        },
        idempotency_key=key,
        publisher="headless-test",
        invocation_path=route_path(project, "main"),
        authorize=lambda: None,
    )


def _unavailable_base():
    return {"revision_id": "unavailable-revision", "publication_id": "unavailable-publication"}


def _refused_headless_commit(runtime, project, key, replacement):
    # D16: the current commit authority rejects an absent public head before
    # provider execution, protecting the same no-overwrite property earlier
    # than the retired publisher's stale-head/content checks.
    with pytest.raises(RuntimeErrorBase) as error:
        _commit(runtime, project, key, base=_unavailable_base(), replacement=replacement)
    assert error.value.status == 409
    assert error.value.code == "conflict"
    details = error.value.details
    assert isinstance(details, dict)
    assert details["reason"] == "history_unavailable"


def _legacy_publish_empty(runtime, project, key):
    return runtime.publish_parent_composition(
        project,
        "main",
        {
            "project_id": project,
            "timeline_id": "main",
            "expected_head": None,
            "parent_revision_id": "empty-default",
            "parent_composition": EMPTY,
        },
        idempotency_key=key,
    )


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
        _refused_headless_commit(runtime, project, key, AUTHORED)
        assert _dump(runtime) == before
    assert _stored(runtime) == original
    assert json.loads(original) == AUTHORED
    assert runtime.store.conn.execute("SELECT publication_id FROM parent_composition_heads WHERE timeline_id='main'").fetchone()[0] is None


def test_empty_default_over_empty_headless_shell_is_refused_untouched(service):
    runtime, project = service
    _shell(runtime, project, EMPTY)
    before = _dump(runtime)
    _refused_headless_commit(runtime, project, "empty-default", EMPTY)
    assert _dump(runtime) == before


def test_empty_default_on_a_fresh_timeline_is_accepted_and_replays(service):
    runtime, project = service
    repaired = runtime.create_timeline(project, "main", idempotency_key="repair-empty")
    base = runtime.get_project_timeline(project, "main")
    accepted = _commit(runtime, project, "empty-default", base=base)
    assert accepted["data"]["status"] == "accepted"
    assert accepted["receipt"]["command_kind"] == "timeline.commit"
    assert accepted["data"]["previous_revision_id"] == repaired["data"]["head_revision_id"]
    assert runtime.get_project_timeline(project, "main")["head_publication_id"] == accepted["receipt"]["receipt_id"]
    before = _dump(runtime)
    assert _commit(runtime, project, "empty-default", base=base) == accepted
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
        _refused_headless_commit(runtime, project, key, body["parent_composition"])
        assert _dump(runtime) == before
    stored = runtime.store.conn.execute("SELECT content_json FROM project_documents WHERE id='timeline:main'").fetchone()[0]
    assert json.loads(stored) == content


def test_genuinely_empty_headless_timeline_still_accepts_expected_head_null(service):
    runtime, project = service
    _hide_content(runtime, project, {"config": {}, "registry": {"assets": {}}, "clips": []})
    repaired = runtime.create_timeline(project, "main", idempotency_key="repair-genuine-empty")
    accepted = _commit(runtime, project, "empty-default")
    assert accepted["data"]["status"] == "accepted"
    assert accepted["data"]["previous_revision_id"] == repaired["data"]["head_revision_id"]
    assert runtime.get_project_timeline(project, "main")["head_publication_id"] == accepted["receipt"]["receipt_id"]


def test_cas_correct_republish_after_reading_the_head_is_accepted(service):
    runtime, project = service
    runtime.create_timeline(project, "main", idempotency_key="repair-cas")
    first = _commit(runtime, project, "empty-default")
    head = runtime.get_project_timeline(project, "main")
    assert {"revision_id": head["head_revision_id"], "publication_id": head["head_publication_id"]} == {
        "revision_id": first["data"]["accepted_revision_id"],
        "publication_id": first["receipt"]["receipt_id"],
    }
    again = _commit(runtime, project, "second", base=head)
    assert again["data"]["status"] == "accepted"
    assert again["data"]["previous_revision_id"] == first["data"]["accepted_revision_id"]
    assert again["data"]["previous_publication_id"] == first["receipt"]["receipt_id"]
    assert _commit(runtime, project, "second", base=head) == again


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
        _refused_headless_commit(runtime, project, key, EMPTY)
        assert _dump(runtime) == before


def test_retired_parent_publication_route_stays_410_and_write_free(service):
    runtime, project = service
    before = _dump(runtime)
    for key in ("legacy-empty-default", "legacy-empty-default"):
        with pytest.raises(RetiredRouteError) as error:
            _legacy_publish_empty(runtime, project, key)
        assert error.value.status == 410
        assert error.value.code == "retired_route"
        details = error.value.details
        assert isinstance(details, dict)
        assert details["reason"] == "timeline_commit_required"
        assert _dump(runtime) == before
